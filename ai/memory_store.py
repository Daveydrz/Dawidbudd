"""
SQLite-based memory storage helpers.
"""
import sqlite3
import numpy as np
import json
import os
from typing import List, Dict, Any, Optional, Tuple
from .vector_store import VectorStore
from .text_embedder import get_dim


# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "memory.db")

# Initialize vector store for similarity search
_vector_store = None


def _get_vector_store() -> VectorStore:
    """Get or create the vector store instance."""
    global _vector_store
    if _vector_store is None:
        vector_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "vector.index")
        _vector_store = VectorStore(get_dim(), vector_path)
    return _vector_store


def _init_db() -> None:
    """Initialize the SQLite database with required tables."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create memories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS memories (
            id TEXT PRIMARY KEY,
            text TEXT,
            kind TEXT,
            created_at TEXT,
            when_iso TEXT NULL,
            last_access TEXT,
            access_count INTEGER,
            strength REAL,
            importance REAL,
            status TEXT,
            sequence_index INTEGER NULL,
            participants TEXT,
            roles TEXT,
            location TEXT,
            media_title TEXT,
            category TEXT,
            distance_km REAL,
            distance_miles REAL,
            items TEXT,
            anaphora_key TEXT,
            precision TEXT,
            deleted INTEGER DEFAULT 0
        )
    ''')
    
    # Create episodic_raw table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS episodic_raw (
            id TEXT PRIMARY KEY,
            created_at TEXT,
            utterance TEXT
        )
    ''')
    
    # Create embeddings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS embeddings (
            id TEXT PRIMARY KEY,
            dim INTEGER,
            blob BLOB
        )
    ''')
    
    conn.commit()
    conn.close()


def _serialize_json_field(value: Any) -> str:
    """Serialize a value to JSON string if it's not None."""
    if value is None:
        return None
    if isinstance(value, str):
        # Already a string, assume it's JSON
        return value
    return json.dumps(value)


def _deserialize_json_field(value: str) -> Any:
    """Deserialize a JSON string field."""
    if value is None:
        return None
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return value


def upsert_memory(record: Dict[str, Any]) -> None:
    """
    Insert or update a memory entry.
    
    Args:
        record: Dictionary containing memory data with 'id' key required
    """
    _init_db()
    
    if 'id' not in record:
        raise ValueError("Memory record must have 'id' field")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Serialize JSON fields
    processed_record = record.copy()
    json_fields = ['participants', 'roles', 'items']
    for field in json_fields:
        if field in processed_record:
            processed_record[field] = _serialize_json_field(processed_record[field])
    
    # Build the upsert query
    columns = list(processed_record.keys())
    placeholders = ', '.join(['?' for _ in columns])
    update_clauses = ', '.join([f'{col} = excluded.{col}' for col in columns if col != 'id'])
    
    query = f'''
        INSERT INTO memories ({', '.join(columns)})
        VALUES ({placeholders})
        ON CONFLICT(id) DO UPDATE SET {update_clauses}
    '''
    
    cursor.execute(query, list(processed_record.values()))
    conn.commit()
    conn.close()


def get_memory(memory_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a memory by ID.
    
    Args:
        memory_id: ID of the memory to retrieve
        
    Returns:
        Dictionary containing memory data or None if not found
    """
    _init_db()
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM memories WHERE id = ? AND deleted = 0', (memory_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        return None
    
    # Convert row to dictionary and deserialize JSON fields
    result = dict(row)
    json_fields = ['participants', 'roles', 'items']
    for field in json_fields:
        if field in result:
            result[field] = _deserialize_json_field(result[field])
    
    return result


def find_by_ids(memory_ids: List[str]) -> List[Dict[str, Any]]:
    """
    Retrieve multiple memories by their IDs.
    
    Args:
        memory_ids: List of memory IDs to retrieve
        
    Returns:
        List of memory dictionaries (excludes deleted memories)
    """
    if not memory_ids:
        return []
    
    _init_db()
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Create placeholders for the IN clause
    placeholders = ', '.join(['?' for _ in memory_ids])
    query = f'SELECT * FROM memories WHERE id IN ({placeholders}) AND deleted = 0'
    
    cursor.execute(query, memory_ids)
    rows = cursor.fetchall()
    conn.close()
    
    # Convert rows to dictionaries and deserialize JSON fields
    results = []
    json_fields = ['participants', 'roles', 'items']
    
    for row in rows:
        result = dict(row)
        for field in json_fields:
            if field in result:
                result[field] = _deserialize_json_field(result[field])
        results.append(result)
    
    return results


def mark_deleted(memory_id: str) -> None:
    """
    Mark a memory as deleted (soft delete).
    
    Args:
        memory_id: Memory ID to mark as deleted
    """
    _init_db()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('UPDATE memories SET deleted = 1 WHERE id = ?', (memory_id,))
    conn.commit()
    conn.close()


def save_embedding(memory_id: str, embedding: np.ndarray) -> None:
    """
    Save an embedding vector for a memory.
    
    Args:
        memory_id: ID of the associated memory
        embedding: Numpy array containing the embedding
    """
    _init_db()
    
    # Store in both SQLite and vector store
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Serialize embedding as bytes
    embedding_bytes = embedding.astype(np.float32).tobytes()
    dim = embedding.shape[0] if embedding.ndim == 1 else embedding.shape[1]
    
    cursor.execute('''
        INSERT OR REPLACE INTO embeddings (id, dim, blob)
        VALUES (?, ?, ?)
    ''', (memory_id, dim, embedding_bytes))
    
    conn.commit()
    conn.close()
    
    # Also store in vector store for efficient similarity search
    vector_store = _get_vector_store()
    if embedding.ndim == 1:
        embedding = embedding.reshape(1, -1)
    vector_store.upsert([memory_id], embedding)


def load_embedding(memory_id: str) -> Optional[np.ndarray]:
    """
    Load an embedding vector for a memory.
    
    Args:
        memory_id: ID of the associated memory
        
    Returns:
        Numpy array containing the embedding or None if not found
    """
    _init_db()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT dim, blob FROM embeddings WHERE id = ?', (memory_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        return None
    
    dim, blob = row
    # Deserialize embedding from bytes
    embedding = np.frombuffer(blob, dtype=np.float32).reshape(-1)
    
    return embedding


def neighbors_by_vector(query_vector: np.ndarray, k: int = 10) -> List[Tuple[str, float]]:
    """
    Find the k nearest neighbor memories by vector similarity.
    
    Args:
        query_vector: Vector to search for
        k: Number of neighbors to return
        
    Returns:
        List of (memory_id, similarity_score) tuples
    """
    vector_store = _get_vector_store()
    return vector_store.search(query_vector, k)