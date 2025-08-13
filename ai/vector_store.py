"""
Vector storage and retrieval for memory embeddings.
"""
import numpy as np
import os
import json
import pickle
from typing import List, Tuple, Optional, Dict

# Try to import FAISS, fall back to numpy if not available
try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False


class VectorStore:
    """
    Vector storage interface for managing embeddings and similarity search.
    Uses FAISS for efficient similarity search with numpy fallback.
    """
    
    def __init__(self, dim: int, persist_path: str):
        """
        Initialize vector store.
        
        Args:
            dim: Dimension of the embeddings
            persist_path: Path to persist the vector index
        """
        self.dim = dim
        self.persist_path = persist_path
        self.use_faiss = FAISS_AVAILABLE
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(persist_path), exist_ok=True)
        
        if self.use_faiss:
            # Use FAISS for efficient similarity search with cosine similarity
            self.index = faiss.IndexFlatIP(dim)  # Inner product for cosine similarity with normalized vectors
            self.ids = []  # Track IDs separately
        else:
            # Pure numpy fallback
            self.vectors = {}  # id -> vector mapping
            self.vector_array = None  # Cached array for batch operations
            self.id_list = []  # Ordered list of IDs
        
        # Load existing index if available
        self._load_index()
        
    def _load_index(self) -> None:
        """Load existing index from disk."""
        if self.use_faiss:
            # Load FAISS index
            if os.path.exists(self.persist_path):
                try:
                    self.index = faiss.read_index(self.persist_path)
                    ids_path = self.persist_path + ".ids"
                    if os.path.exists(ids_path):
                        with open(ids_path, 'r') as f:
                            self.ids = json.load(f)
                except Exception as e:
                    print(f"Warning: Failed to load FAISS index: {e}")
                    # Reset to empty index
                    self.index = faiss.IndexFlatIP(self.dim)
                    self.ids = []
        else:
            # Load numpy fallback
            npz_path = self.persist_path + ".npz"
            if os.path.exists(npz_path):
                try:
                    data = np.load(npz_path, allow_pickle=True)
                    self.vectors = data['vectors'].item()
                    self.id_list = data['ids'].tolist()
                    self._update_vector_array()
                except Exception as e:
                    print(f"Warning: Failed to load numpy index: {e}")
                    self.vectors = {}
                    self.id_list = []
    
    def _save_index(self) -> None:
        """Save index to disk."""
        try:
            if self.use_faiss:
                # Save FAISS index
                faiss.write_index(self.index, self.persist_path)
                # Save IDs separately
                ids_path = self.persist_path + ".ids"
                with open(ids_path, 'w') as f:
                    json.dump(self.ids, f)
            else:
                # Save numpy fallback
                npz_path = self.persist_path + ".npz"
                np.savez(npz_path, vectors=self.vectors, ids=self.id_list)
        except Exception as e:
            print(f"Warning: Failed to save index: {e}")
    
    def _update_vector_array(self) -> None:
        """Update cached vector array for numpy fallback."""
        if not self.use_faiss and self.id_list:
            vectors_list = [self.vectors[id_] for id_ in self.id_list]
            self.vector_array = np.stack(vectors_list)
        else:
            self.vector_array = None
            
    def upsert(self, ids_or_pairs, vectors: Optional[np.ndarray] = None) -> None:
        """
        Insert or update vectors by ID.
        
        Args:
            ids_or_pairs: Either a list of IDs (when vectors is provided) or 
                         a list of (id, vector) pairs for backwards compatibility
            vectors: Array of vectors to store (shape: [n_vectors, dim]) - optional when using pairs format
        """
        # Handle backwards compatibility for list of pairs format
        if vectors is None and len(ids_or_pairs) > 0 and isinstance(ids_or_pairs[0], (list, tuple)):
            # Unpack pairs format: [(id1, vec1), (id2, vec2), ...]
            ids = []
            vector_list = []
            for pair in ids_or_pairs:
                if len(pair) != 2:
                    raise ValueError("Each pair must contain exactly 2 elements: (id, vector)")
                ids.append(pair[0])
                vector_list.append(pair[1])
            
            # Convert to numpy array
            vectors = np.array(vector_list, dtype=np.float32)
            if len(vectors.shape) == 1:
                vectors = vectors.reshape(1, -1)
        else:
            # Standard format: separate ids and vectors arrays
            ids = ids_or_pairs
        
        if len(ids) != len(vectors):
            raise ValueError(f"Number of IDs ({len(ids)}) must match number of vectors ({len(vectors)})")
        
        if len(vectors) > 0 and vectors.shape[1] != self.dim:
            raise ValueError(f"Vector dimension ({vectors.shape[1]}) must match index dimension ({self.dim})")
        
        # Ensure vectors are normalized for cosine similarity
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1  # Avoid division by zero
        normalized_vectors = vectors / norms
        
        if self.use_faiss:
            # For FAISS: remove existing vectors first, then add new ones
            for i, id_ in enumerate(ids):
                if id_ in self.ids:
                    # Remove existing vector (rebuild index for simplicity)
                    old_idx = self.ids.index(id_)
                    self.ids.pop(old_idx)
                    
                    # Rebuild index without the removed vector
                    if len(self.ids) > 0:
                        # Get all vectors except the removed one
                        all_vectors = []
                        for j in range(self.index.ntotal):
                            if j != old_idx:
                                vec = self.index.reconstruct(j)
                                all_vectors.append(vec)
                        
                        # Rebuild index
                        self.index = faiss.IndexFlatIP(self.dim)
                        if all_vectors:
                            self.index.add(np.stack(all_vectors).astype(np.float32))
                    else:
                        self.index = faiss.IndexFlatIP(self.dim)
                
                # Add new vector
                self.ids.append(id_)
                self.index.add(normalized_vectors[i:i+1].astype(np.float32))
        else:
            # For numpy fallback: update vectors dictionary
            for i, id_ in enumerate(ids):
                self.vectors[id_] = normalized_vectors[i].astype(np.float32)
                if id_ not in self.id_list:
                    self.id_list.append(id_)
            
            self._update_vector_array()
        
        # Save to disk
        self._save_index()
        
    def search(self, query_vector: np.ndarray, k: int = 10) -> List[Tuple[str, float]]:
        """
        Search for most similar vectors using cosine similarity.
        
        Args:
            query_vector: Vector to search for (shape: [dim])
            k: Number of results to return
            
        Returns:
            List of (id, similarity_score) tuples sorted by similarity (highest first)
        """
        if len(query_vector.shape) == 1:
            query_vector = query_vector.reshape(1, -1)
        
        if query_vector.shape[1] != self.dim:
            raise ValueError(f"Query vector dimension ({query_vector.shape[1]}) must match index dimension ({self.dim})")
        
        # Normalize query vector for cosine similarity
        norm = np.linalg.norm(query_vector)
        if norm == 0:
            return []
        normalized_query = query_vector / norm
        
        if self.use_faiss:
            if self.index.ntotal == 0:
                return []
            
            # FAISS search (returns cosine similarities since we use inner product with normalized vectors)
            k_actual = min(k, self.index.ntotal)
            similarities, indices = self.index.search(normalized_query.astype(np.float32), k_actual)
            
            results = []
            for i, (sim, idx) in enumerate(zip(similarities[0], indices[0])):
                if idx >= 0 and idx < len(self.ids):  # Valid index
                    results.append((self.ids[idx], float(sim)))
            
            return results
        else:
            # Numpy fallback with cosine similarity
            if not self.id_list or self.vector_array is None:
                return []
            
            # Compute cosine similarities
            similarities = np.dot(self.vector_array, normalized_query.T).flatten()
            
            # Get top-k indices
            k_actual = min(k, len(similarities))
            top_indices = np.argpartition(similarities, -k_actual)[-k_actual:]
            top_indices = top_indices[np.argsort(similarities[top_indices])[::-1]]  # Sort by similarity desc
            
            results = []
            for idx in top_indices:
                id_ = self.id_list[idx]
                sim = similarities[idx]
                results.append((id_, float(sim)))
            
            return results
        
    def delete(self, ids: List[str]) -> None:
        """
        Delete vectors by ID.
        
        Args:
            ids: List of IDs to delete
        """
        if self.use_faiss:
            # For FAISS: rebuild index without deleted vectors
            remaining_ids = []
            remaining_vectors = []
            
            for i, id_ in enumerate(self.ids):
                if id_ not in ids:
                    remaining_ids.append(id_)
                    vec = self.index.reconstruct(i)
                    remaining_vectors.append(vec)
            
            # Rebuild index
            self.index = faiss.IndexFlatIP(self.dim)
            self.ids = remaining_ids
            
            if remaining_vectors:
                vectors_array = np.stack(remaining_vectors)
                self.index.add(vectors_array.astype(np.float32))
        else:
            # For numpy fallback: remove from dictionary and list
            for id_ in ids:
                if id_ in self.vectors:
                    del self.vectors[id_]
                if id_ in self.id_list:
                    self.id_list.remove(id_)
            
            self._update_vector_array()
        
        # Save to disk
        self._save_index()

    def get_stats(self) -> Dict:
        """Get statistics about the vector store."""
        if self.use_faiss:
            return {
                "backend": "FAISS",
                "total_vectors": self.index.ntotal,
                "dimension": self.dim,
                "index_type": "IndexFlatIP (cosine similarity)"
            }
        else:
            return {
                "backend": "Numpy",
                "total_vectors": len(self.vectors),
                "dimension": self.dim,
                "index_type": "In-memory dictionary"
            }


if __name__ == "__main__":
    """Self-test for vector store."""
    import tempfile
    import shutil
    
    print("🧪 Testing Vector Store...")
    print(f"🔧 FAISS Available: {FAISS_AVAILABLE}")
    
    # Create temporary directory for testing
    test_dir = tempfile.mkdtemp()
    test_index_path = os.path.join(test_dir, "test.index")
    
    try:
        # Test with 384-dimensional vectors (matching text embedder)
        from text_embedder import embed_text_batch, get_dim
        
        dim = get_dim()
        vs = VectorStore(dim, test_index_path)
        
        print(f"✅ VectorStore initialized with {vs.get_stats()}")
        
        # Generate some test embeddings
        test_texts = [
            "Hello world",
            "The quick brown fox",
            "Python programming is fun"
        ]
        
        embeddings = embed_text_batch(test_texts)
        ids = [f"doc_{i}" for i in range(len(test_texts))]
        
        # Test upsert
        vs.upsert(ids, embeddings)
        stats = vs.get_stats()
        assert stats["total_vectors"] == 3, f"Expected 3 vectors, got {stats['total_vectors']}"
        print(f"✅ Upserted {stats['total_vectors']} vectors")
        
        # Test search
        query_embedding = embeddings[0]  # Search for first text
        results = vs.search(query_embedding, k=3)
        
        assert len(results) == 3, f"Expected 3 results, got {len(results)}"
        assert results[0][0] == ids[0], f"Top result should be '{ids[0]}', got '{results[0][0]}'"
        assert results[0][1] > 0.99, f"Self-similarity should be ~1.0, got {results[0][1]}"
        
        print(f"✅ Search returned {len(results)} results")
        print(f"   Top result: {results[0][0]} (similarity: {results[0][1]:.4f})")
        
        # Test update existing vector
        new_embedding = embed_text_batch(["Updated hello world"])[0:1]
        vs.upsert([ids[0]], new_embedding)
        
        # Verify still 3 vectors (update, not insert)
        stats = vs.get_stats()
        assert stats["total_vectors"] == 3, f"After update, expected 3 vectors, got {stats['total_vectors']}"
        print("✅ Vector update works correctly")
        
        # Test delete
        vs.delete([ids[1]])
        stats = vs.get_stats()
        assert stats["total_vectors"] == 2, f"After delete, expected 2 vectors, got {stats['total_vectors']}"
        print("✅ Vector deletion works correctly")
        
        # Test persistence - create new instance
        vs2 = VectorStore(dim, test_index_path)
        stats2 = vs2.get_stats()
        assert stats2["total_vectors"] == 2, f"After reload, expected 2 vectors, got {stats2['total_vectors']}"
        print("✅ Index persistence works correctly")
        
        # Test search on reloaded index
        results2 = vs2.search(query_embedding, k=2)
        assert len(results2) >= 1, "Reloaded index should return results"
        print(f"✅ Search on reloaded index works: {len(results2)} results")
        
        print("🎉 Vector Store tests passed!")
        
    finally:
        # Cleanup
        shutil.rmtree(test_dir)