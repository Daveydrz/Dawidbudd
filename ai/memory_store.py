"""
SQLite-based memory storage helpers with interference and decay dynamics.
"""
import sqlite3
import json
import os
import math
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple

# Handle numpy import gracefully
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    # Create a mock numpy for basic array operations
    class MockNumpy:
        @staticmethod
        def array(data, dtype=None):
            return data
        @staticmethod
        def float32():
            return float
    np = MockNumpy()

# Handle numpy import gracefully
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    # Create a mock numpy for basic array operations
    class MockNumpy:
        @staticmethod
        def array(data, dtype=None):
            return data
        @staticmethod
        def float32():
            return float
    np = MockNumpy()

# Try to import get_dim function safely
try:
    from .text_embedder import get_dim
except ImportError:
    def get_dim():
        return 384  # Default dimension


# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "memory.db")

# Initialize vector store for similarity search
_vector_store = None


def _get_vector_store():
    """Get or create the vector store instance."""
    global _vector_store
    if _vector_store is None and NUMPY_AVAILABLE:
        try:
            from .vector_store import VectorStore
            vector_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "vector.index")
            _vector_store = VectorStore(get_dim(), vector_path)
        except ImportError:
            pass
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
    Insert or update a memory entry with interference and decay dynamics.
    
    Args:
        record: Dictionary containing memory data with 'id' key required
    """
    _init_db()
    
    if 'id' not in record:
        raise ValueError("Memory record must have 'id' field")
    
    # Step 8: Interference - reduce strength of similar memories
    _apply_interference(record)
    
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


def _apply_interference(new_record: Dict[str, Any]) -> None:
    """
    Apply interference by reducing strength of similar memories.
    
    Args:
        new_record: The new memory record being inserted
    """
    try:
        from config import INTERFERENCE_SIM_THRESHOLD, INTERFERENCE_PENALTY
    except ImportError:
        INTERFERENCE_SIM_THRESHOLD = 0.80
        INTERFERENCE_PENALTY = 0.08
    
    # Get embedding for the new memory
    if 'text' not in new_record:
        return
    
    try:
        from .text_embedder import embed_text_batch
        embeddings = embed_text_batch([new_record['text']])
        new_embedding = embeddings[0]
        
        # Find similar memories
        similar_memories = neighbors_by_vector(new_embedding, k=10)
        
        # Reduce strength of similar memories
        if similar_memories:
            _init_db()
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            interfered_count = 0
            for memory_id, similarity in similar_memories:
                if similarity >= INTERFERENCE_SIM_THRESHOLD and memory_id != new_record.get('id'):
                    # Reduce strength but don't go below 0
                    cursor.execute('''
                        UPDATE memories 
                        SET strength = MAX(0, strength - ?)
                        WHERE id = ? AND deleted = 0
                    ''', (INTERFERENCE_PENALTY, memory_id))
                    interfered_count += 1
            
            if interfered_count > 0:
                print(f"[Memory] 🔄 Interference: Reduced strength of {interfered_count} similar memories")
            
            conn.commit()
            conn.close()
            
    except Exception as e:
        print(f"[Memory] ⚠️ Interference failed: {e}")


def access_memory(memory_id: str) -> None:
    """
    Update memory access patterns and apply strength boost.
    
    Args:
        memory_id: ID of the memory being accessed
    """
    try:
        from config import RECALL_BOOST, MAX_STRENGTH
    except ImportError:
        RECALL_BOOST = 0.35
        MAX_STRENGTH = 4.0
    
    _init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    current_time = datetime.utcnow().isoformat()
    
    # Update access count, last_access, and add strength boost (capped at MAX_STRENGTH)
    cursor.execute('''
        UPDATE memories 
        SET access_count = access_count + 1,
            last_access = ?,
            strength = MIN(?, strength + ?)
        WHERE id = ? AND deleted = 0
    ''', (current_time, MAX_STRENGTH, RECALL_BOOST, memory_id))
    
    conn.commit()
    conn.close()


def apply_decay_to_all_memories() -> int:
    """
    Apply time-based decay to all memories based on their age.
    
    Returns:
        Number of memories that had decay applied
    """
    try:
        from config import DECAY_HALF_LIFE_DAYS
    except ImportError:
        DECAY_HALF_LIFE_DAYS = 21
    
    _init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    current_time = datetime.utcnow()
    decay_count = 0
    
    # Get all non-deleted memories
    cursor.execute('SELECT id, created_at, strength FROM memories WHERE deleted = 0')
    memories = cursor.fetchall()
    
    for memory_id, created_at, current_strength in memories:
        try:
            # Parse creation time
            created_time = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            if created_time.tzinfo is None:
                created_time = created_time.replace(tzinfo=None)
                current_time_naive = current_time.replace(tzinfo=None)
            else:
                current_time_naive = current_time
            
            # Calculate days since creation
            days_since_created = (current_time_naive - created_time).total_seconds() / (24 * 3600)
            
            # Apply exponential decay: strength * exp(-ln(2) * days / half_life)
            decay_factor = math.exp(-math.log(2) * days_since_created / DECAY_HALF_LIFE_DAYS)
            new_strength = current_strength * decay_factor
            
            # Update strength if it has decayed significantly
            if abs(new_strength - current_strength) > 0.01:
                cursor.execute(
                    'UPDATE memories SET strength = ? WHERE id = ?',
                    (new_strength, memory_id)
                )
                decay_count += 1
                
        except Exception as e:
            print(f"[Memory] ⚠️ Decay failed for {memory_id}: {e}")
    
    conn.commit()
    conn.close()
    
    return decay_count


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


def save_embedding(memory_id: str, embedding) -> None:
    """
    Save an embedding vector for a memory.
    
    Args:
        memory_id: ID of the associated memory
        embedding: Numpy array containing the embedding or raw data
    """
    if not NUMPY_AVAILABLE:
        print(f"[Memory] ⚠️ Cannot save embedding {memory_id}: NumPy not available")
        return
    
    _init_db()
    
    # Store in both SQLite and vector store
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Serialize embedding as bytes
    if hasattr(embedding, 'astype'):
        embedding_bytes = embedding.astype(np.float32).tobytes()
        dim = embedding.shape[0] if embedding.ndim == 1 else embedding.shape[1]
    else:
        # Fallback for non-numpy data
        embedding_bytes = str(embedding).encode('utf-8')
        dim = len(embedding) if hasattr(embedding, '__len__') else 0
    
    cursor.execute('''
        INSERT OR REPLACE INTO embeddings (id, dim, blob)
        VALUES (?, ?, ?)
    ''', (memory_id, dim, embedding_bytes))
    
    conn.commit()
    conn.close()
    
    # Also store in vector store for efficient similarity search
    vector_store = _get_vector_store()
    if vector_store and hasattr(embedding, 'reshape'):
        if embedding.ndim == 1:
            embedding = embedding.reshape(1, -1)
        vector_store.upsert([memory_id], embedding)


def load_embedding(memory_id: str):
    """
    Load an embedding vector for a memory.
    
    Args:
        memory_id: ID of the associated memory
        
    Returns:
        Numpy array containing the embedding or None if not found
    """
    if not NUMPY_AVAILABLE:
        return None
    
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
    try:
        embedding = np.frombuffer(blob, dtype=np.float32).reshape(-1)
        return embedding
    except:
        return None


def neighbors_by_vector(query_vector, k: int = 10) -> List[Tuple[str, float]]:
    """
    Find the k nearest neighbor memories by vector similarity.
    
    Args:
        query_vector: Vector to search for
        k: Number of neighbors to return
        
    Returns:
        List of (memory_id, similarity_score) tuples
    """
    if not NUMPY_AVAILABLE:
        print("[Memory] ⚠️ Vector search requires NumPy")
        return []
    
    vector_store = _get_vector_store()
    if vector_store:
        return vector_store.search(query_vector, k)
    return []


def daily_memory_replay() -> Dict[str, int]:
    """
    Daily memory replay and consolidation routine.
    
    Returns:
        Dictionary with statistics about the replay operation
    """
    try:
        from config import (REPLAY_DAILY_TOP_N, REPLAY_SUMMARY_KEEP, 
                          COMPRESS_EPISODES_AFTER_DAYS)
    except ImportError:
        REPLAY_DAILY_TOP_N = 40
        REPLAY_SUMMARY_KEEP = True
        COMPRESS_EPISODES_AFTER_DAYS = 45
    
    print(f"[Memory] 🔄 Starting daily memory replay...")
    
    stats = {
        'decay_applied': 0,
        'top_memories_processed': 0,
        'episodes_compressed': 0,
        'duplicates_summarized': 0
    }
    
    # 1. Apply decay to all memories
    stats['decay_applied'] = apply_decay_to_all_memories()
    
    # 2. Select top N memories by (importance + strength - decay)
    _init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all memories with calculated priority score
    cursor.execute('''
        SELECT id, text, kind, importance, strength, created_at
        FROM memories 
        WHERE deleted = 0
        ORDER BY (importance + strength) DESC
        LIMIT ?
    ''', (REPLAY_DAILY_TOP_N,))
    
    top_memories = cursor.fetchall()
    stats['top_memories_processed'] = len(top_memories)
    
    # 3. Summarize duplicates if enabled
    if REPLAY_SUMMARY_KEEP and len(top_memories) > 1:
        stats['duplicates_summarized'] = _summarize_duplicate_memories(cursor, top_memories)
    
    # 4. Compress old episodes
    cutoff_date = datetime.utcnow() - timedelta(days=COMPRESS_EPISODES_AFTER_DAYS)
    cutoff_iso = cutoff_date.isoformat()
    
    cursor.execute('''
        SELECT COUNT(*) FROM episodic_raw 
        WHERE created_at < ?
    ''', (cutoff_iso,))
    
    old_episodes_count = cursor.fetchone()[0]
    
    if old_episodes_count > 0:
        # Compress by creating a summary and removing details
        cursor.execute('''
            SELECT utterance FROM episodic_raw 
            WHERE created_at < ?
            ORDER BY created_at
            LIMIT 100
        ''', (cutoff_iso,))
        
        old_episodes = [row[0] for row in cursor.fetchall()]
        
        if old_episodes:
            # Create a compressed summary
            summary_text = f"Compressed {len(old_episodes)} old conversations from before {cutoff_date.strftime('%Y-%m-%d')}"
            summary_id = f"compress_{int(datetime.utcnow().timestamp())}"
            
            cursor.execute('''
                INSERT INTO episodic_raw (id, created_at, utterance)
                VALUES (?, ?, ?)
            ''', (summary_id, datetime.utcnow().isoformat(), summary_text))
            
            # Remove the old episodes
            cursor.execute('''
                DELETE FROM episodic_raw 
                WHERE created_at < ?
            ''', (cutoff_iso,))
            
            stats['episodes_compressed'] = old_episodes_count
    
    conn.commit()
    conn.close()
    
    print(f"[Memory] ✅ Daily replay complete: {stats}")
    return stats


def _summarize_duplicate_memories(cursor, memories: List[Tuple]) -> int:
    """
    Find and summarize similar memories to reduce duplication.
    
    Args:
        cursor: Database cursor
        memories: List of memory tuples
        
    Returns:
        Number of duplicates summarized
    """
    duplicates_found = 0
    
    try:
        from .text_embedder import embed_text_batch
        
        # Group memories by similarity
        memory_groups = []
        processed_ids = set()
        
        for i, (mem_id, text, kind, importance, strength, created_at) in enumerate(memories):
            if mem_id in processed_ids:
                continue
                
            similar_group = [(mem_id, text, kind, importance, strength, created_at)]
            processed_ids.add(mem_id)
            
            # Find similar memories in the remaining set
            mem_embedding = embed_text_batch([text])[0]
            
            for j, (other_id, other_text, other_kind, other_imp, other_str, other_created) in enumerate(memories[i+1:], i+1):
                if other_id in processed_ids:
                    continue
                    
                other_embedding = embed_text_batch([other_text])[0]
                similarity = np.dot(mem_embedding, other_embedding) / (
                    np.linalg.norm(mem_embedding) * np.linalg.norm(other_embedding)
                )
                
                if similarity > 0.85:  # High similarity threshold for grouping
                    similar_group.append((other_id, other_text, other_kind, other_imp, other_str, other_created))
                    processed_ids.add(other_id)
            
            if len(similar_group) > 1:
                memory_groups.append(similar_group)
        
        # Summarize each group
        for group in memory_groups:
            if len(group) > 1:
                _create_summary_memory(cursor, group)
                duplicates_found += len(group) - 1  # All but one are duplicates
    
    except Exception as e:
        print(f"[Memory] ⚠️ Duplicate summarization failed: {e}")
    
    return duplicates_found


def _create_summary_memory(cursor, similar_memories: List[Tuple]) -> None:
    """
    Create a summary memory from a group of similar memories.
    
    Args:
        cursor: Database cursor
        similar_memories: List of similar memory tuples
    """
    try:
        # Find the strongest memory to keep as base
        strongest_memory = max(similar_memories, key=lambda x: x[4])  # x[4] is strength
        
        # Create summary text
        all_texts = [mem[1] for mem in similar_memories]  # mem[1] is text
        summary_text = f"Summary of {len(similar_memories)} similar memories: {strongest_memory[1]}"
        
        # Update the strongest memory to be the summary
        cursor.execute('''
            UPDATE memories 
            SET text = ?, 
                kind = 'summary',
                strength = strength + 0.1,
                importance = importance + 0.1
            WHERE id = ?
        ''', (summary_text, strongest_memory[0]))
        
        # Mark other memories as summarized (soft delete)
        for mem_id, _, _, _, _, _ in similar_memories[1:]:
            if mem_id != strongest_memory[0]:
                cursor.execute('''
                    UPDATE memories 
                    SET deleted = 1, 
                        text = text || ' [SUMMARIZED]'
                    WHERE id = ?
                ''', (mem_id,))
        
        print(f"[Memory] 📝 Summarized {len(similar_memories)} similar memories into {strongest_memory[0]}")
        
    except Exception as e:
        print(f"[Memory] ⚠️ Summary creation failed: {e}")


def get_memory_statistics() -> Dict[str, Any]:
    """
    Get comprehensive memory system statistics.
    
    Returns:
        Dictionary containing memory statistics
    """
    _init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    stats = {}
    
    # Basic counts
    cursor.execute('SELECT COUNT(*) FROM memories WHERE deleted = 0')
    stats['total_memories'] = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM memories WHERE deleted = 1')
    stats['deleted_memories'] = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM episodic_raw')
    stats['episodic_raw_count'] = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM embeddings')
    stats['embeddings_count'] = cursor.fetchone()[0]
    
    # Strength and importance statistics
    cursor.execute('''
        SELECT AVG(strength), AVG(importance), AVG(access_count)
        FROM memories WHERE deleted = 0
    ''')
    avg_stats = cursor.fetchone()
    stats['avg_strength'] = avg_stats[0] or 0
    stats['avg_importance'] = avg_stats[1] or 0
    stats['avg_access_count'] = avg_stats[2] or 0
    
    # Memory kinds distribution
    cursor.execute('''
        SELECT kind, COUNT(*) 
        FROM memories WHERE deleted = 0 
        GROUP BY kind
    ''')
    stats['memory_kinds'] = dict(cursor.fetchall())
    
    conn.close()
    return stats