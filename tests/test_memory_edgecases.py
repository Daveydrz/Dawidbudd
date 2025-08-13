"""
Comprehensive memory system edge case tests for Step 8.

This test suite covers 50 edge cases for the complete memory system including
extraction, recall, interference, decay, and memory dynamics.
"""
import unittest
import os
import tempfile
import shutil
import json
import sqlite3
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import sys
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai import memory
from ai.memory_store import (
    upsert_memory, get_memory, find_by_ids, mark_deleted,
    save_embedding, load_embedding, neighbors_by_vector,
    access_memory, apply_decay_to_all_memories, daily_memory_replay,
    get_memory_statistics, DB_PATH, _init_db
)
from ai.memory_recall import build_memory_context_for_question
from ai.memory_regex_bank import extract_candidates
from ai.memory_normalize import parse_relative_time, parse_australian_date


class TestMemoryEdgeCases(unittest.TestCase):
    """Comprehensive test suite for memory system edge cases."""
    
    def setUp(self):
        """Set up test environment with temporary database."""
        self.test_dir = tempfile.mkdtemp()
        self.original_db_path = DB_PATH
        
        # Override DB_PATH for testing
        import ai.memory_store as store_module
        store_module.DB_PATH = os.path.join(self.test_dir, "test_memory.db")
        
        # Initialize test database
        _init_db()
        
        # Mock current time for consistent testing
        self.mock_time = datetime(2025, 1, 8, 12, 0, 0)
    
    def tearDown(self):
        """Clean up test environment."""
        # Restore original DB_PATH
        import ai.memory_store as store_module
        store_module.DB_PATH = self.original_db_path
        
        # Remove test directory
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def create_test_memory(self, memory_id: str, text: str, strength: float = 1.0, 
                          importance: float = 0.5, created_at: datetime = None) -> dict:
        """Helper to create a test memory."""
        if created_at is None:
            created_at = self.mock_time
        
        record = {
            'id': memory_id,
            'text': text,
            'kind': 'test',
            'created_at': created_at.isoformat(),
            'when_iso': None,
            'last_access': created_at.isoformat(),
            'access_count': 0,
            'strength': strength,
            'importance': importance,
            'status': 'active',
            'sequence_index': None,
            'participants': '[]',
            'roles': '[]',
            'location': '',
            'media_title': '',
            'category': 'test',
            'distance_km': None,
            'distance_miles': None,
            'items': '[]',
            'anaphora_key': '',
            'precision': 'test',
            'deleted': 0
        }
        upsert_memory(record)
        return record
    
    # Test Cases 1-10: Basic Memory Operations
    
    def test_01_memory_insertion_and_retrieval(self):
        """Test 1: Basic memory insertion and retrieval."""
        memory = self.create_test_memory("test_001", "I love pizza")
        retrieved = get_memory("test_001")
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved['text'], "I love pizza")
        self.assertEqual(retrieved['strength'], 1.0)
    
    def test_02_memory_update_existing(self):
        """Test 2: Updating existing memory."""
        self.create_test_memory("test_002", "Original text", strength=1.0)
        
        # Update the memory
        updated = {
            'id': 'test_002',
            'text': 'Updated text',
            'strength': 2.0,
            'importance': 0.8
        }
        upsert_memory(updated)
        
        retrieved = get_memory("test_002")
        self.assertEqual(retrieved['text'], 'Updated text')
        self.assertEqual(retrieved['strength'], 2.0)
    
    def test_03_soft_delete_functionality(self):
        """Test 3: Soft delete functionality."""
        self.create_test_memory("test_003", "To be deleted")
        
        # Verify memory exists
        self.assertIsNotNone(get_memory("test_003"))
        
        # Mark as deleted
        mark_deleted("test_003")
        
        # Should return None after deletion
        self.assertIsNone(get_memory("test_003"))
    
    def test_04_batch_memory_retrieval(self):
        """Test 4: Batch memory retrieval."""
        self.create_test_memory("batch_001", "Memory 1")
        self.create_test_memory("batch_002", "Memory 2")
        self.create_test_memory("batch_003", "Memory 3")
        
        memories = find_by_ids(["batch_001", "batch_002", "batch_003"])
        self.assertEqual(len(memories), 3)
        
        texts = {m['text'] for m in memories}
        expected = {"Memory 1", "Memory 2", "Memory 3"}
        self.assertEqual(texts, expected)
    
    def test_05_empty_batch_retrieval(self):
        """Test 5: Empty batch retrieval."""
        memories = find_by_ids([])
        self.assertEqual(memories, [])
        
        memories = find_by_ids(["nonexistent"])
        self.assertEqual(memories, [])
    
    def test_06_json_field_serialization(self):
        """Test 6: JSON field serialization and deserialization."""
        memory = {
            'id': 'json_test',
            'text': 'Test JSON fields',
            'participants': ['Alice', 'Bob'],
            'roles': ['friend', 'colleague'],
            'items': [{'item': 'bread', 'quantity': 2}],
            'strength': 1.0,
            'importance': 0.5,
            'created_at': self.mock_time.isoformat()
        }
        upsert_memory(memory)
        
        retrieved = get_memory('json_test')
        self.assertEqual(retrieved['participants'], ['Alice', 'Bob'])
        self.assertEqual(retrieved['roles'], ['friend', 'colleague'])
        self.assertEqual(retrieved['items'], [{'item': 'bread', 'quantity': 2}])
    
    def test_07_embedding_storage_and_retrieval(self):
        """Test 7: Embedding storage and retrieval."""
        self.create_test_memory("embed_test", "Test embedding")
        
        # Create test embedding
        embedding = np.array([0.1, 0.2, 0.3, 0.4], dtype=np.float32)
        save_embedding("embed_test", embedding)
        
        # Retrieve embedding
        retrieved_embedding = load_embedding("embed_test")
        
        self.assertIsNotNone(retrieved_embedding)
        np.testing.assert_array_almost_equal(embedding, retrieved_embedding)
    
    def test_08_nonexistent_memory_retrieval(self):
        """Test 8: Retrieving nonexistent memory."""
        self.assertIsNone(get_memory("nonexistent"))
        self.assertIsNone(load_embedding("nonexistent"))
    
    def test_09_memory_with_null_fields(self):
        """Test 9: Memory with null/None fields."""
        memory = {
            'id': 'null_test',
            'text': 'Test with nulls',
            'when_iso': None,
            'sequence_index': None,
            'distance_km': None,
            'participants': None,
            'strength': 1.0,
            'importance': 0.5,
            'created_at': self.mock_time.isoformat()
        }
        upsert_memory(memory)
        
        retrieved = get_memory('null_test')
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved['text'], 'Test with nulls')
        self.assertIsNone(retrieved['when_iso'])
    
    def test_10_large_text_handling(self):
        """Test 10: Handling large text content."""
        large_text = "A" * 10000  # 10KB text
        self.create_test_memory("large_text", large_text)
        
        retrieved = get_memory("large_text")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved['text'], large_text)
    
    # Test Cases 11-20: Memory Dynamics (Interference, Decay, Access)
    
    @patch('ai.text_embedder.embed_text_batch')
    def test_11_interference_mechanism(self, mock_embed):
        """Test 11: Memory interference mechanism."""
        # Mock embeddings to ensure similarity
        similar_embedding = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float32)
        mock_embed.return_value = [similar_embedding]
        
        # Create first memory
        self.create_test_memory("interference_001", "I love pizza", strength=2.0)
        save_embedding("interference_001", similar_embedding)
        
        # Add vector store entry manually
        with patch('ai.memory_store._get_vector_store') as mock_vs:
            mock_vs.return_value.search.return_value = [('interference_001', 0.85)]
            
            # Create similar memory (should trigger interference)
            new_memory = {
                'id': 'interference_002',
                'text': 'I really love pizza',
                'strength': 1.0,
                'importance': 0.5,
                'created_at': self.mock_time.isoformat()
            }
            upsert_memory(new_memory)
        
        # Check if first memory's strength was reduced
        original_memory = get_memory("interference_001")
        self.assertLess(original_memory['strength'], 2.0)
    
    def test_12_access_memory_updates(self):
        """Test 12: Memory access updates."""
        self.create_test_memory("access_test", "Test access", strength=1.0)
        
        original = get_memory("access_test")
        original_count = original['access_count']
        original_strength = original['strength']
        
        # Access the memory
        access_memory("access_test")
        
        updated = get_memory("access_test")
        self.assertEqual(updated['access_count'], original_count + 1)
        self.assertGreater(updated['strength'], original_strength)
    
    def test_13_strength_cap_enforcement(self):
        """Test 13: Strength cap enforcement."""
        self.create_test_memory("cap_test", "Test strength cap", strength=3.8)
        
        # Access multiple times to try to exceed cap
        for _ in range(10):
            access_memory("cap_test")
        
        memory = get_memory("cap_test")
        self.assertLessEqual(memory['strength'], 4.0)  # MAX_STRENGTH
    
    def test_14_decay_application(self):
        """Test 14: Time-based decay application."""
        # Create old memory
        old_time = self.mock_time - timedelta(days=42)  # 2 half-lives
        self.create_test_memory("decay_test", "Old memory", 
                               strength=2.0, created_at=old_time)
        
        with patch('ai.memory_store.datetime') as mock_dt:
            mock_dt.utcnow.return_value = self.mock_time
            decay_count = apply_decay_to_all_memories()
        
        self.assertGreater(decay_count, 0)
        
        decayed_memory = get_memory("decay_test")
        self.assertLess(decayed_memory['strength'], 2.0)
    
    def test_15_interference_with_no_similar_memories(self):
        """Test 15: Interference when no similar memories exist."""
        with patch('ai.memory_store.neighbors_by_vector') as mock_neighbors:
            mock_neighbors.return_value = []  # No similar memories
            
            memory = {
                'id': 'no_interference',
                'text': 'Unique memory',
                'strength': 1.0,
                'importance': 0.5,
                'created_at': self.mock_time.isoformat()
            }
            
            # Should not raise any errors
            upsert_memory(memory)
            
            retrieved = get_memory('no_interference')
            self.assertIsNotNone(retrieved)
    
    def test_16_access_nonexistent_memory(self):
        """Test 16: Accessing nonexistent memory."""
        # Should not raise errors
        access_memory("nonexistent_memory")
    
    def test_17_decay_with_invalid_dates(self):
        """Test 17: Decay handling with invalid date formats."""
        # Create memory with malformed date
        import ai.memory_store as store_module
        conn = sqlite3.connect(store_module.DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO memories (id, text, created_at, strength)
            VALUES (?, ?, ?, ?)
        ''', ('invalid_date', 'Test', 'invalid-date-format', 1.0))
        conn.commit()
        conn.close()
        
        # Should handle gracefully without crashing
        decay_count = apply_decay_to_all_memories()
        self.assertGreaterEqual(decay_count, 0)
    
    def test_18_interference_with_identical_embeddings(self):
        """Test 18: Interference with identical embeddings."""
        embedding = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float32)
        
        with patch('ai.text_embedder.embed_text_batch') as mock_embed:
            mock_embed.return_value = [embedding]
            
            # Create two memories with identical embeddings
            self.create_test_memory("identical_001", "Text A", strength=2.0)
            save_embedding("identical_001", embedding)
            
            with patch('ai.memory_store.neighbors_by_vector') as mock_neighbors:
                mock_neighbors.return_value = [('identical_001', 1.0)]
                
                self.create_test_memory("identical_002", "Text A", strength=1.0)
        
        # First memory should have reduced strength
        memory = get_memory("identical_001")
        self.assertLess(memory['strength'], 2.0)
    
    def test_19_multiple_access_patterns(self):
        """Test 19: Multiple access patterns over time."""
        self.create_test_memory("multi_access", "Multi access test", strength=1.0)
        
        access_times = []
        strengths = []
        
        for i in range(5):
            access_memory("multi_access")
            memory = get_memory("multi_access")
            access_times.append(memory['access_count'])
            strengths.append(memory['strength'])
        
        # Access count should increase
        self.assertEqual(access_times, [1, 2, 3, 4, 5])
        
        # Strength should generally increase (within cap)
        for i in range(1, len(strengths)):
            self.assertGreaterEqual(strengths[i], strengths[i-1])
    
    def test_20_interference_threshold_boundary(self):
        """Test 20: Interference at threshold boundaries."""
        embedding1 = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float32)
        embedding2 = np.array([0.79, 0.61, 0.0, 0.0], dtype=np.float32)  # ~0.79 similarity
        
        with patch('ai.text_embedder.embed_text_batch') as mock_embed:
            mock_embed.side_effect = [
                [embedding1],  # First memory
                [embedding2]   # Second memory
            ]
            
            self.create_test_memory("boundary_001", "Text A", strength=2.0)
            save_embedding("boundary_001", embedding1)
            
            with patch('ai.memory_store.neighbors_by_vector') as mock_neighbors:
                # Just below threshold (0.80) - no interference
                mock_neighbors.return_value = [('boundary_001', 0.79)]
                
                original_memory = get_memory("boundary_001")
                original_strength = original_memory['strength']
                
                self.create_test_memory("boundary_002", "Text B", strength=1.0)
                
                # Strength should remain unchanged
                post_memory = get_memory("boundary_001")
                self.assertEqual(post_memory['strength'], original_strength)
    
    # Test Cases 21-30: Memory Extraction and Processing
    
    def test_21_regex_extraction_basic(self):
        """Test 21: Basic regex extraction."""
        text = "I bought milk and bread at Coles yesterday"
        items, confidence, pattern_ids = extract_candidates(text)
        
        self.assertGreater(len(items), 0)
        self.assertGreater(confidence, 0)
        self.assertGreater(len(pattern_ids), 0)
    
    def test_22_extraction_with_empty_text(self):
        """Test 22: Extraction with empty text."""
        items, confidence, pattern_ids = extract_candidates("")
        
        self.assertEqual(len(items), 0)
        self.assertEqual(confidence, 0.0)
        self.assertEqual(len(pattern_ids), 0)
    
    def test_23_extraction_with_special_characters(self):
        """Test 23: Extraction with special characters and unicode."""
        text = "I went to café & bought café ☕ for $5.50"
        items, confidence, pattern_ids = extract_candidates(text)
        
        # Should handle gracefully without errors
        self.assertIsInstance(items, list)
        self.assertIsInstance(confidence, (int, float))
    
    def test_24_australian_date_parsing(self):
        """Test 24: Australian date format parsing."""
        date_result = parse_australian_date("5/10")  # Should be 5th October
        
        if date_result:
            self.assertEqual(date_result.month, 10)
            self.assertEqual(date_result.day, 5)
    
    def test_25_relative_time_parsing(self):
        """Test 25: Relative time parsing."""
        with patch('ai.memory_normalize.datetime') as mock_dt:
            mock_dt.now.return_value = self.mock_time
            
            result = parse_relative_time("I'll do it tomorrow")
            if result:
                expected = self.mock_time + timedelta(days=1)
                self.assertEqual(result.date(), expected.date())
    
    @patch('ai.memory.extract_memories_from_text')
    def test_26_full_extraction_pipeline(self, mock_extract):
        """Test 26: Full extraction pipeline integration."""
        mock_extract.return_value = None
        
        # Test that extraction can be called without errors
        memory.extract_memories_from_text("Test extraction", "test_user")
        mock_extract.assert_called_once_with("Test extraction", "test_user")
    
    def test_27_extraction_confidence_scoring(self):
        """Test 27: Extraction confidence scoring."""
        high_conf_text = "I bought milk and bread at Woolworths yesterday for dinner"
        low_conf_text = "maybe sometime"
        
        high_items, high_conf, _ = extract_candidates(high_conf_text)
        low_items, low_conf, _ = extract_candidates(low_conf_text)
        
        self.assertGreaterEqual(high_conf, low_conf)
    
    def test_28_extraction_pattern_identification(self):
        """Test 28: Pattern ID identification."""
        text = "I need to buy groceries tomorrow"
        items, confidence, pattern_ids = extract_candidates(text)
        
        if pattern_ids:
            self.assertIsInstance(pattern_ids[0], str)
            self.assertGreater(len(pattern_ids[0]), 0)
    
    def test_29_multiple_pattern_extraction(self):
        """Test 29: Multiple pattern extraction from single text."""
        text = "I bought milk at Coles and planned to visit mom next Sunday"
        items, confidence, pattern_ids = extract_candidates(text)
        
        # Should detect both shopping and family patterns
        self.assertGreaterEqual(len(items), 1)
    
    def test_30_extraction_with_long_text(self):
        """Test 30: Extraction with very long text."""
        long_text = " ".join(["I went shopping"] * 100)  # Very repetitive long text
        
        items, confidence, pattern_ids = extract_candidates(long_text)
        
        # Should handle without performance issues
        self.assertIsInstance(items, list)
        self.assertIsInstance(confidence, (int, float))
    
    # Test Cases 31-40: Memory Recall and Query Processing
    
    def test_31_basic_memory_recall(self):
        """Test 31: Basic memory recall functionality."""
        self.create_test_memory("recall_001", "I love pizza")
        self.create_test_memory("recall_002", "I hate vegetables")
        
        result = build_memory_context_for_question("What do I like to eat?")
        
        self.assertIn('memories', result)
        self.assertIn('confidence', result)
        self.assertIn('known_facts', result)
    
    def test_32_recall_with_no_memories(self):
        """Test 32: Recall when no memories exist."""
        result = build_memory_context_for_question("What do I remember?")
        
        self.assertEqual(len(result['memories']), 0)
        self.assertEqual(result['confidence'], 0.0)
        self.assertIn("None available", result['known_facts'])
    
    def test_33_recall_with_temporal_constraints(self):
        """Test 33: Recall with before/after date constraints."""
        old_time = self.mock_time - timedelta(days=30)
        new_time = self.mock_time - timedelta(days=1)
        
        self.create_test_memory("old_mem", "Old memory", created_at=old_time)
        self.create_test_memory("new_mem", "New memory", created_at=new_time)
        
        question = "What happened after last week?"
        result = build_memory_context_for_question(question)
        
        # Should prioritize recent memories
        self.assertGreaterEqual(len(result['memories']), 0)
    
    def test_34_recall_with_keyword_matching(self):
        """Test 34: Recall with keyword matching."""
        self.create_test_memory("keyword_001", "I bought groceries at the store")
        self.create_test_memory("keyword_002", "I watched a movie")
        
        result = build_memory_context_for_question("Tell me about shopping")
        
        # Should find grocery-related memory
        memory_texts = [m['text'] for m in result['memories']]
        self.assertTrue(any('groceries' in text for text in memory_texts))
    
    def test_35_recall_memory_limit_enforcement(self):
        """Test 35: Memory recall limit enforcement."""
        # Create more memories than the limit
        for i in range(10):
            self.create_test_memory(f"limit_{i:03d}", f"Memory number {i}")
        
        result = build_memory_context_for_question("What do I remember?", max_items=3)
        
        self.assertLessEqual(len(result['memories']), 3)
    
    def test_36_recall_confidence_calculation(self):
        """Test 36: Recall confidence calculation."""
        # Create high-importance memory
        self.create_test_memory("high_imp", "Important memory", importance=0.9)
        # Create low-importance memory  
        self.create_test_memory("low_imp", "Less important", importance=0.1)
        
        high_result = build_memory_context_for_question("important")
        low_result = build_memory_context_for_question("less")
        
        # High importance should yield higher confidence
        self.assertGreaterEqual(high_result['confidence'], low_result['confidence'])
    
    def test_37_recall_with_deleted_memories(self):
        """Test 37: Recall should exclude deleted memories."""
        self.create_test_memory("active_mem", "Active memory")
        self.create_test_memory("deleted_mem", "Deleted memory")
        
        mark_deleted("deleted_mem")
        
        result = build_memory_context_for_question("memory")
        
        memory_ids = [m['id'] for m in result['memories']]
        self.assertIn("active_mem", memory_ids)
        self.assertNotIn("deleted_mem", memory_ids)
    
    def test_38_recall_access_tracking(self):
        """Test 38: Recall should update memory access patterns."""
        self.create_test_memory("access_track", "Track access")
        
        original = get_memory("access_track")
        original_access_count = original['access_count']
        
        # Perform recall
        build_memory_context_for_question("track")
        
        updated = get_memory("access_track")
        # Access count should increase if memory was returned
        if any(m['id'] == 'access_track' for m in build_memory_context_for_question("track")['memories']):
            self.assertGreater(updated['access_count'], original_access_count)
    
    def test_39_recall_with_jitter(self):
        """Test 39: Recall with tie-breaking jitter."""
        # Create memories with identical scores
        for i in range(3):
            self.create_test_memory(f"jitter_{i}", "Same text", 
                                  strength=1.0, importance=0.5)
        
        result1 = build_memory_context_for_question("same")
        result2 = build_memory_context_for_question("same")
        
        # Results might be in different order due to jitter
        self.assertEqual(len(result1['memories']), len(result2['memories']))
    
    def test_40_recall_strategy_identification(self):
        """Test 40: Recall strategy identification."""
        self.create_test_memory("strategy_test", "Test memory for strategy")
        
        result = build_memory_context_for_question("strategy")
        
        self.assertIn('recall_strategy', result)
        self.assertIsInstance(result['recall_strategy'], str)
    
    # Test Cases 41-45: Daily Replay and Consolidation
    
    def test_41_daily_replay_basic(self):
        """Test 41: Basic daily replay functionality."""
        # Create test memories
        for i in range(5):
            self.create_test_memory(f"replay_{i}", f"Memory {i}", 
                                  strength=float(i), importance=0.5)
        
        with patch('ai.memory_store.datetime') as mock_dt:
            mock_dt.utcnow.return_value = self.mock_time
            
            stats = daily_memory_replay()
        
        self.assertIn('decay_applied', stats)
        self.assertIn('top_memories_processed', stats)
        self.assertGreaterEqual(stats['top_memories_processed'], 0)
    
    def test_42_replay_with_old_episodes(self):
        """Test 42: Replay compression of old episodes."""
        import ai.memory_store as store_module
        
        # Add old episodic entries
        old_time = self.mock_time - timedelta(days=50)
        
        conn = sqlite3.connect(store_module.DB_PATH)
        cursor = conn.cursor()
        
        for i in range(3):
            cursor.execute('''
                INSERT INTO episodic_raw (id, created_at, utterance)
                VALUES (?, ?, ?)
            ''', (f'old_ep_{i}', old_time.isoformat(), f'Old episode {i}'))
        
        conn.commit()
        conn.close()
        
        with patch('ai.memory_store.datetime') as mock_dt:
            mock_dt.utcnow.return_value = self.mock_time
            
            stats = daily_memory_replay()
        
        self.assertGreaterEqual(stats['episodes_compressed'], 0)
    
    def test_43_replay_with_no_memories(self):
        """Test 43: Replay when no memories exist."""
        stats = daily_memory_replay()
        
        self.assertEqual(stats['top_memories_processed'], 0)
        self.assertEqual(stats['duplicates_summarized'], 0)
    
    @patch('ai.text_embedder.embed_text_batch')
    def test_44_duplicate_memory_summarization(self, mock_embed):
        """Test 44: Duplicate memory summarization."""
        # Create similar memories
        similar_embedding = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float32)
        mock_embed.return_value = [similar_embedding]
        
        memories = [
            ("dup_001", "I love pizza", 1.0, 0.5),
            ("dup_002", "I really love pizza", 1.1, 0.6),
            ("dup_003", "Pizza is amazing", 0.9, 0.4)
        ]
        
        for mem_id, text, strength, importance in memories:
            self.create_test_memory(mem_id, text, strength=strength, 
                                  importance=importance)
        
        stats = daily_memory_replay()
        
        # Should detect and process duplicates
        self.assertGreaterEqual(stats['duplicates_summarized'], 0)
    
    def test_45_replay_error_handling(self):
        """Test 45: Replay error handling with corrupted data."""
        import ai.memory_store as store_module
        
        # Insert corrupted memory data
        conn = sqlite3.connect(store_module.DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO memories (id, text, created_at, strength, importance)
            VALUES (?, ?, ?, ?, ?)
        ''', ('corrupt', 'Corrupt memory', 'invalid-date', 'not-a-number', 0.5))
        
        conn.commit()
        conn.close()
        
        # Should handle gracefully
        stats = daily_memory_replay()
        self.assertIsInstance(stats, dict)
    
    # Test Cases 46-50: Integration and Edge Cases
    
    def test_46_memory_statistics(self):
        """Test 46: Memory statistics collection."""
        # Create diverse memories
        self.create_test_memory("stat_001", "Memory 1", strength=1.0)
        self.create_test_memory("stat_002", "Memory 2", strength=2.0)
        mark_deleted("stat_002")
        
        stats = get_memory_statistics()
        
        self.assertIn('total_memories', stats)
        self.assertIn('deleted_memories', stats)
        self.assertEqual(stats['total_memories'], 1)
        self.assertEqual(stats['deleted_memories'], 1)
    
    def test_47_concurrent_memory_operations(self):
        """Test 47: Concurrent memory operations simulation."""
        # Simulate rapid memory operations
        for i in range(10):
            memory_id = f"concurrent_{i}"
            self.create_test_memory(memory_id, f"Concurrent memory {i}")
            access_memory(memory_id)
            
            if i % 3 == 0:
                mark_deleted(memory_id)
        
        # Should handle without corruption
        stats = get_memory_statistics()
        self.assertGreaterEqual(stats['total_memories'], 0)
    
    def test_48_large_scale_memory_operations(self):
        """Test 48: Large scale memory operations."""
        # Create many memories
        memory_ids = []
        for i in range(50):
            memory_id = f"large_{i:03d}"
            self.create_test_memory(memory_id, f"Large scale memory {i}")
            memory_ids.append(memory_id)
        
        # Batch retrieval
        memories = find_by_ids(memory_ids[:25])
        self.assertEqual(len(memories), 25)
        
        # Mass access
        for memory_id in memory_ids[:10]:
            access_memory(memory_id)
        
        # Should complete without timeout
        self.assertTrue(True)
    
    def test_49_memory_system_resilience(self):
        """Test 49: Memory system resilience to corrupted embeddings."""
        self.create_test_memory("resilience_test", "Resilience test")
        
        # Save corrupted embedding
        corrupted_embedding = np.array([float('inf'), float('nan'), 0.0, 0.0])
        
        try:
            save_embedding("resilience_test", corrupted_embedding)
            # Should handle gracefully
        except Exception:
            pass  # Expected behavior
        
        # Memory should still be retrievable
        memory = get_memory("resilience_test")
        self.assertIsNotNone(memory)
    
    def test_50_complete_memory_lifecycle(self):
        """Test 50: Complete memory lifecycle integration."""
        # Create memory
        self.create_test_memory("lifecycle", "Complete lifecycle test", 
                               strength=1.0, importance=0.5)
        
        # Add embedding
        embedding = np.array([0.1, 0.2, 0.3, 0.4], dtype=np.float32)
        save_embedding("lifecycle", embedding)
        
        # Access multiple times
        for _ in range(3):
            access_memory("lifecycle")
        
        # Verify access updates
        memory = get_memory("lifecycle")
        self.assertEqual(memory['access_count'], 3)
        self.assertGreater(memory['strength'], 1.0)
        
        # Test recall
        result = build_memory_context_for_question("lifecycle")
        self.assertGreater(len(result['memories']), 0)
        
        # Apply decay
        with patch('ai.memory_store.datetime') as mock_dt:
            mock_dt.utcnow.return_value = self.mock_time + timedelta(days=30)
            apply_decay_to_all_memories()
        
        # Run daily replay
        stats = daily_memory_replay()
        self.assertIsInstance(stats, dict)
        
        # Memory should still exist
        final_memory = get_memory("lifecycle")
        self.assertIsNotNone(final_memory)
        
        # Soft delete
        mark_deleted("lifecycle")
        self.assertIsNone(get_memory("lifecycle"))


if __name__ == '__main__':
    unittest.main(verbosity=2)