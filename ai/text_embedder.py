"""
Text embedding functionality for memory system.
"""
import numpy as np
import hashlib
from typing import List
from collections import defaultdict


# Fixed embedding dimension
EMBEDDING_DIM = 384


def get_dim() -> int:
    """
    Get the embedding dimension.
    
    Returns:
        Embedding dimension (384)
    """
    return EMBEDDING_DIM


def _deterministic_text_to_vector(text: str, dim: int = EMBEDDING_DIM) -> np.ndarray:
    """
    Create a deterministic embedding from text using hashing and char n-grams.
    This provides a consistent fallback when no ML model is available.
    
    Args:
        text: Input text string
        dim: Output dimension
        
    Returns:
        Normalized embedding vector of specified dimension
    """
    if not text.strip():
        return np.zeros(dim, dtype=np.float32)
    
    text = text.lower().strip()
    
    # Initialize vector with text hash
    text_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
    vector = np.zeros(dim, dtype=np.float32)
    
    # Use hash to seed deterministic randomness
    hash_seed = int(text_hash[:8], 16) % (2**31)
    np.random.seed(hash_seed)
    vector += np.random.normal(0, 0.1, dim).astype(np.float32)
    
    # Add char n-grams (1-3 grams) for better text representation
    char_counts = defaultdict(int)
    
    # Unigrams
    for char in text:
        if char.isalnum():
            char_counts[f"1_{char}"] += 1
    
    # Bigrams  
    for i in range(len(text) - 1):
        if text[i].isalnum() and text[i+1].isalnum():
            char_counts[f"2_{text[i:i+2]}"] += 1
    
    # Trigrams
    for i in range(len(text) - 2):
        if all(c.isalnum() for c in text[i:i+3]):
            char_counts[f"3_{text[i:i+3]}"] += 1
    
    # Map n-grams to vector positions using hash
    for ngram, count in char_counts.items():
        ngram_hash = hashlib.md5(ngram.encode('utf-8')).hexdigest()
        positions = [int(ngram_hash[i:i+2], 16) % dim for i in range(0, min(len(ngram_hash), 8), 2)]
        
        for pos in positions:
            vector[pos] += count * 0.01
    
    # Normalize to unit vector
    norm = np.linalg.norm(vector)
    if norm > 0:
        vector = vector / norm
    
    return vector.astype(np.float32)


def embed_text_batch(texts: List[str]) -> np.ndarray:
    """
    Convert a batch of text strings into embeddings.
    Uses a deterministic fallback based on hashing and char n-grams.
    
    Args:
        texts: List of text strings to embed
        
    Returns:
        numpy array of shape (len(texts), embedding_dim) containing embeddings
    """
    if not texts:
        return np.array([]).reshape(0, EMBEDDING_DIM).astype(np.float32)
    
    embeddings = []
    for text in texts:
        embedding = _deterministic_text_to_vector(text, EMBEDDING_DIM)
        embeddings.append(embedding)
    
    return np.stack(embeddings).astype(np.float32)


if __name__ == "__main__":
    """Self-test for text embedder."""
    print("🧪 Testing Text Embedder...")
    
    # Test basic functionality
    test_texts = [
        "Hello world",
        "The quick brown fox jumps over the lazy dog",
        "This is a test sentence for embeddings",
        "Hello world"  # Duplicate to test consistency
    ]
    
    embeddings = embed_text_batch(test_texts)
    
    # Check shape
    expected_shape = (len(test_texts), EMBEDDING_DIM)
    assert embeddings.shape == expected_shape, f"Wrong shape: {embeddings.shape} vs {expected_shape}"
    print(f"✅ Shape correct: {embeddings.shape}")
    
    # Check data type
    assert embeddings.dtype == np.float32, f"Wrong dtype: {embeddings.dtype}"
    print(f"✅ Data type correct: {embeddings.dtype}")
    
    # Check determinism - same text should give same embedding
    assert np.allclose(embeddings[0], embeddings[3]), "Embeddings not deterministic!"
    print("✅ Deterministic: Same text produces same embedding")
    
    # Check different texts give different embeddings
    assert not np.allclose(embeddings[0], embeddings[1]), "Different texts give same embedding!"
    print("✅ Distinctive: Different texts produce different embeddings")
    
    # Check vectors are normalized
    norms = np.linalg.norm(embeddings, axis=1)
    expected_norm = 1.0
    assert np.allclose(norms, expected_norm, atol=1e-5), f"Vectors not normalized: {norms}"
    print(f"✅ Normalized: All vectors have unit norm (~{expected_norm})")
    
    # Test get_dim function
    assert get_dim() == EMBEDDING_DIM, f"get_dim() returned {get_dim()}, expected {EMBEDDING_DIM}"
    print(f"✅ get_dim() returns correct dimension: {get_dim()}")
    
    # Test empty input
    empty_embeddings = embed_text_batch([])
    assert empty_embeddings.shape == (0, EMBEDDING_DIM), "Empty input handling failed"
    print("✅ Empty input handled correctly")
    
    print("🎉 Text Embedder tests passed!")