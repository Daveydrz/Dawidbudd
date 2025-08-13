#!/usr/bin/env python3
"""
Memory Inspector Tool - Debug and explore the memory system.

This tool provides utilities to list, search, and analyze memories,
show neighbor relationships, display strength/decay values, mark superseded memories,
and delete/forget functionality.
"""
import os
import sys
import json
import argparse
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import textwrap

# Handle numpy import gracefully
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("[Inspector] ⚠️ NumPy not available, some features disabled")

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from ai.memory_store import (
        get_memory, find_by_ids, neighbors_by_vector, mark_deleted,
        load_embedding, get_memory_statistics, apply_decay_to_all_memories,
        daily_memory_replay, DB_PATH, _init_db
    )
    from ai.memory_recall import build_memory_context_for_question
    MEMORY_STORE_AVAILABLE = True
except ImportError as e:
    print(f"[Inspector] ⚠️ Memory store import failed: {e}")
    MEMORY_STORE_AVAILABLE = False

try:
    from ai.text_embedder import embed_text_batch
    TEXT_EMBEDDER_AVAILABLE = True
except ImportError:
    TEXT_EMBEDDER_AVAILABLE = False
    print("[Inspector] ⚠️ Text embedder not available")


class MemoryInspector:
    """Memory system inspector and debugging tool."""
    
    def __init__(self):
        """Initialize the memory inspector."""
        if not MEMORY_STORE_AVAILABLE:
            print("[Inspector] ❌ Memory store not available")
            return
            
        _init_db()
        print(f"[Inspector] 🔍 Memory Inspector initialized")
        print(f"[Inspector] 📍 Database: {DB_PATH}")
    
    def list_memories(self, limit: int = 20, kind: str = None, 
                     min_strength: float = None, order_by: str = 'created_at') -> None:
        """
        List memories with optional filtering.
        
        Args:
            limit: Maximum number of memories to show
            kind: Filter by memory kind
            min_strength: Minimum strength threshold
            order_by: Sort order (created_at, strength, importance, access_count)
        """
        print(f"\n[Inspector] 📋 Listing memories (limit: {limit})")
        
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Build query
        where_clauses = ["deleted = 0"]
        params = []
        
        if kind:
            where_clauses.append("kind = ?")
            params.append(kind)
        
        if min_strength is not None:
            where_clauses.append("strength >= ?")
            params.append(min_strength)
        
        where_clause = " AND ".join(where_clauses)
        
        # Validate order_by
        valid_orders = ['created_at', 'strength', 'importance', 'access_count', 'last_access']
        if order_by not in valid_orders:
            order_by = 'created_at'
        
        query = f'''
            SELECT id, text, kind, created_at, strength, importance, access_count, last_access
            FROM memories 
            WHERE {where_clause}
            ORDER BY {order_by} DESC
            LIMIT ?
        '''
        params.append(limit)
        
        cursor.execute(query, params)
        memories = cursor.fetchall()
        conn.close()
        
        if not memories:
            print("No memories found matching criteria.")
            return
        
        print(f"\nFound {len(memories)} memories:")
        print("=" * 100)
        
        for memory in memories:
            self._print_memory_summary(dict(memory))
        
        print("=" * 100)
    
    def search_memories(self, query: str, limit: int = 10) -> None:
        """
        Search memories by text content or similarity.
        
        Args:
            query: Search query
            limit: Maximum results to return
        """
        print(f"\n[Inspector] 🔎 Searching memories for: '{query}'")
        
        # First try text search
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, text, kind, created_at, strength, importance
            FROM memories 
            WHERE deleted = 0 AND text LIKE ?
            ORDER BY strength DESC
            LIMIT ?
        ''', (f'%{query}%', limit))
        
        text_matches = cursor.fetchall()
        conn.close()
        
        print(f"\n📝 Text matches ({len(text_matches)}):")
        for memory in text_matches:
            self._print_memory_summary(dict(memory))
        
        # Try vector similarity search
        if NUMPY_AVAILABLE and TEXT_EMBEDDER_AVAILABLE:
            try:
                embeddings = embed_text_batch([query])
                query_embedding = embeddings[0]
                
                similar_memories = neighbors_by_vector(query_embedding, k=limit)
                
                print(f"\n🎯 Vector similarity matches ({len(similar_memories)}):")
                
                if similar_memories:
                    memory_ids = [mem_id for mem_id, _ in similar_memories]
                    memories = find_by_ids(memory_ids)
                    
                    # Create lookup for similarities
                    sim_lookup = {mem_id: sim for mem_id, sim in similar_memories}
                    
                    for memory in memories:
                        similarity = sim_lookup.get(memory['id'], 0.0)
                        print(f"  Similarity: {similarity:.3f}")
                        self._print_memory_summary(memory, indent="    ")
                
            except Exception as e:
                print(f"Vector search failed: {e}")
        else:
            print(f"\n🎯 Vector similarity search: NumPy and text embedder required")
    
    def show_memory_details(self, memory_id: str) -> None:
        """
        Show detailed information about a specific memory.
        
        Args:
            memory_id: ID of the memory to inspect
        """
        print(f"\n[Inspector] 🔍 Memory details for: {memory_id}")
        
        memory = get_memory(memory_id)
        if not memory:
            print(f"Memory {memory_id} not found or deleted.")
            return
        
        print("\n" + "=" * 80)
        print(f"ID: {memory['id']}")
        print(f"Text: {memory['text']}")
        print(f"Kind: {memory['kind']}")
        print(f"Created: {memory['created_at']}")
        print(f"When: {memory.get('when_iso', 'N/A')}")
        print(f"Last Access: {memory['last_access']}")
        print(f"Access Count: {memory['access_count']}")
        print(f"Strength: {memory['strength']:.3f}")
        print(f"Importance: {memory['importance']:.3f}")
        print(f"Status: {memory['status']}")
        print(f"Category: {memory.get('category', 'N/A')}")
        print(f"Location: {memory.get('location', 'N/A')}")
        print(f"Participants: {memory.get('participants', '[]')}")
        print(f"Roles: {memory.get('roles', '[]')}")
        print(f"Items: {memory.get('items', '[]')}")
        print("=" * 80)
        
        # Show embedding info
        if NUMPY_AVAILABLE:
            embedding = load_embedding(memory_id)
            if embedding is not None:
                print(f"Embedding: {embedding.shape} {embedding.dtype}")
                print(f"Embedding norm: {np.linalg.norm(embedding):.3f}")
            else:
                print("Embedding: Not found")
        else:
            print("Embedding: NumPy not available")
        
        # Show similar memories
        if NUMPY_AVAILABLE:
            self.show_neighbors(memory_id, limit=5)
        else:
            print("Similar memories: NumPy required for vector similarity")
    
    def show_neighbors(self, memory_id: str, limit: int = 10) -> None:
        """
        Show memories similar to the given memory.
        
        Args:
            memory_id: ID of the reference memory
            limit: Maximum neighbors to show
        """
        print(f"\n[Inspector] 👥 Similar memories to {memory_id}:")
        
        if not NUMPY_AVAILABLE:
            print("Vector similarity requires NumPy. Install numpy to use this feature.")
            return
        
        embedding = load_embedding(memory_id)
        if embedding is None:
            print("No embedding found for this memory.")
            return
        
        similar_memories = neighbors_by_vector(embedding, k=limit + 1)  # +1 to exclude self
        
        # Filter out the memory itself
        similar_memories = [(mid, sim) for mid, sim in similar_memories if mid != memory_id]
        
        if not similar_memories:
            print("No similar memories found.")
            return
        
        memory_ids = [mem_id for mem_id, _ in similar_memories[:limit]]
        memories = find_by_ids(memory_ids)
        
        # Create lookup for similarities
        sim_lookup = {mem_id: sim for mem_id, sim in similar_memories}
        
        print(f"\nTop {len(memories)} similar memories:")
        for memory in memories:
            similarity = sim_lookup.get(memory['id'], 0.0)
            print(f"\n  📊 Similarity: {similarity:.3f}")
            self._print_memory_summary(memory, indent="    ")
    
    def show_strengths_over_time(self, days: int = 30) -> None:
        """
        Show memory strength distribution over time.
        
        Args:
            days: Number of days to look back
        """
        print(f"\n[Inspector] 📈 Memory strengths over last {days} days:")
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        cutoff_iso = cutoff_date.isoformat()
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                DATE(created_at) as date,
                COUNT(*) as count,
                AVG(strength) as avg_strength,
                MAX(strength) as max_strength,
                AVG(importance) as avg_importance
            FROM memories 
            WHERE deleted = 0 AND created_at >= ?
            GROUP BY DATE(created_at)
            ORDER BY date DESC
        ''', (cutoff_iso,))
        
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            print("No memories found in the specified time range.")
            return
        
        print("\nDate       | Count | Avg Strength | Max Strength | Avg Importance")
        print("-" * 70)
        
        for row in results:
            date, count, avg_str, max_str, avg_imp = row
            print(f"{date} | {count:5d} | {avg_str:8.3f}     | {max_str:8.3f}     | {avg_imp:8.3f}")
    
    def mark_superseded(self, memory_id: str, reason: str = "superseded") -> None:
        """
        Mark a memory as superseded.
        
        Args:
            memory_id: ID of the memory to mark
            reason: Reason for superseding
        """
        print(f"\n[Inspector] ⚠️ Marking memory {memory_id} as superseded: {reason}")
        
        memory = get_memory(memory_id)
        if not memory:
            print(f"Memory {memory_id} not found.")
            return
        
        # Update status and add reason to text
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        updated_text = f"{memory['text']} [SUPERSEDED: {reason}]"
        
        cursor.execute('''
            UPDATE memories 
            SET status = 'superseded', text = ?, strength = strength * 0.1
            WHERE id = ?
        ''', (updated_text, memory_id))
        
        conn.commit()
        conn.close()
        
        print(f"Memory {memory_id} marked as superseded.")
    
    def forget_memory(self, memory_id: str, permanent: bool = False) -> None:
        """
        Forget (delete) a memory.
        
        Args:
            memory_id: ID of the memory to forget
            permanent: If True, permanently delete; otherwise soft delete
        """
        print(f"\n[Inspector] 🗑️ Forgetting memory {memory_id} (permanent: {permanent})")
        
        memory = get_memory(memory_id)
        if not memory:
            print(f"Memory {memory_id} not found.")
            return
        
        if permanent:
            # Permanent deletion
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM memories WHERE id = ?', (memory_id,))
            cursor.execute('DELETE FROM embeddings WHERE id = ?', (memory_id,))
            
            conn.commit()
            conn.close()
            
            print(f"Memory {memory_id} permanently deleted.")
        else:
            # Soft delete
            mark_deleted(memory_id)
            print(f"Memory {memory_id} soft deleted.")
    
    def show_statistics(self) -> None:
        """Show comprehensive memory system statistics."""
        print("\n[Inspector] 📊 Memory System Statistics:")
        
        stats = get_memory_statistics()
        
        print("\n" + "=" * 50)
        print("GENERAL STATISTICS")
        print("=" * 50)
        print(f"Total memories: {stats['total_memories']}")
        print(f"Deleted memories: {stats['deleted_memories']}")
        print(f"Episodic raw entries: {stats['episodic_raw_count']}")
        print(f"Embeddings stored: {stats['embeddings_count']}")
        
        print(f"\nAverage strength: {stats['avg_strength']:.3f}")
        print(f"Average importance: {stats['avg_importance']:.3f}")
        print(f"Average access count: {stats['avg_access_count']:.1f}")
        
        if stats['memory_kinds']:
            print("\n" + "=" * 50)
            print("MEMORY TYPES")
            print("=" * 50)
            for kind, count in stats['memory_kinds'].items():
                print(f"{kind}: {count}")
        
        # Additional detailed statistics
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Strength distribution
        cursor.execute('''
            SELECT 
                CASE 
                    WHEN strength < 0.5 THEN 'Very Weak (< 0.5)'
                    WHEN strength < 1.0 THEN 'Weak (0.5-1.0)'
                    WHEN strength < 2.0 THEN 'Medium (1.0-2.0)'
                    WHEN strength < 3.0 THEN 'Strong (2.0-3.0)'
                    ELSE 'Very Strong (3.0+)'
                END as strength_category,
                COUNT(*) as count
            FROM memories 
            WHERE deleted = 0
            GROUP BY strength_category
        ''')
        
        strength_dist = cursor.fetchall()
        
        if strength_dist:
            print("\n" + "=" * 50)
            print("STRENGTH DISTRIBUTION")
            print("=" * 50)
            for category, count in strength_dist:
                print(f"{category}: {count}")
        
        # Access patterns
        cursor.execute('''
            SELECT 
                CASE 
                    WHEN access_count = 0 THEN 'Never accessed'
                    WHEN access_count = 1 THEN 'Accessed once'
                    WHEN access_count <= 5 THEN 'Low access (2-5)'
                    WHEN access_count <= 10 THEN 'Medium access (6-10)'
                    ELSE 'High access (10+)'
                END as access_category,
                COUNT(*) as count
            FROM memories 
            WHERE deleted = 0
            GROUP BY access_category
        ''')
        
        access_dist = cursor.fetchall()
        
        if access_dist:
            print("\n" + "=" * 50)
            print("ACCESS PATTERNS")
            print("=" * 50)
            for category, count in access_dist:
                print(f"{category}: {count}")
        
        conn.close()
    
    def run_maintenance(self) -> None:
        """Run memory system maintenance."""
        print("\n[Inspector] 🔧 Running memory system maintenance...")
        
        print("\n1. Applying decay to all memories...")
        decay_count = apply_decay_to_all_memories()
        print(f"   Applied decay to {decay_count} memories")
        
        print("\n2. Running daily replay and consolidation...")
        stats = daily_memory_replay()
        print(f"   Decay applied: {stats['decay_applied']}")
        print(f"   Top memories processed: {stats['top_memories_processed']}")
        print(f"   Episodes compressed: {stats['episodes_compressed']}")
        print(f"   Duplicates summarized: {stats['duplicates_summarized']}")
        
        print("\n✅ Maintenance complete!")
    
    def test_recall(self, question: str) -> None:
        """
        Test memory recall for a given question.
        
        Args:
            question: Question to test recall with
        """
        print(f"\n[Inspector] 🧠 Testing recall for: '{question}'")
        
        result = build_memory_context_for_question(question)
        
        print(f"\nRecall Results:")
        print(f"Confidence: {result['confidence']:.3f}")
        print(f"Strategy: {result['recall_strategy']}")
        print(f"Memories found: {len(result['memories'])}")
        
        print(f"\nKnown Facts:")
        print(result['known_facts'])
        
        if result['memories']:
            print(f"\nDetailed memories:")
            for i, memory in enumerate(result['memories'], 1):
                print(f"\n{i}. {memory['id']}")
                print(f"   Text: {memory['text']}")
                print(f"   Strength: {memory['strength']:.3f}")
                print(f"   Importance: {memory['importance']:.3f}")
                print(f"   Access count: {memory['access_count']}")
    
    def _print_memory_summary(self, memory: Dict[str, Any], indent: str = "") -> None:
        """Print a concise memory summary."""
        text = memory['text']
        if len(text) > 80:
            text = text[:77] + "..."
        
        created = memory.get('created_at', '')
        if created:
            try:
                dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                created = dt.strftime('%Y-%m-%d %H:%M')
            except:
                pass
        
        strength = memory.get('strength', 0)
        importance = memory.get('importance', 0)
        access_count = memory.get('access_count', 0)
        
        print(f"{indent}🧠 {memory['id']} | S:{strength:.2f} I:{importance:.2f} A:{access_count}")
        print(f"{indent}   {text}")
        print(f"{indent}   📅 {created} | {memory.get('kind', 'unknown')}")


def main():
    """Main CLI interface for the memory inspector."""
    parser = argparse.ArgumentParser(description='Memory System Inspector')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List memories
    list_parser = subparsers.add_parser('list', help='List memories')
    list_parser.add_argument('--limit', type=int, default=20, help='Maximum memories to show')
    list_parser.add_argument('--kind', help='Filter by memory kind')
    list_parser.add_argument('--min-strength', type=float, help='Minimum strength threshold')
    list_parser.add_argument('--order-by', choices=['created_at', 'strength', 'importance', 'access_count'], 
                            default='created_at', help='Sort order')
    
    # Search memories
    search_parser = subparsers.add_parser('search', help='Search memories')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--limit', type=int, default=10, help='Maximum results')
    
    # Show memory details
    show_parser = subparsers.add_parser('show', help='Show memory details')
    show_parser.add_argument('memory_id', help='Memory ID to inspect')
    
    # Show neighbors
    neighbors_parser = subparsers.add_parser('neighbors', help='Show similar memories')
    neighbors_parser.add_argument('memory_id', help='Reference memory ID')
    neighbors_parser.add_argument('--limit', type=int, default=10, help='Maximum neighbors')
    
    # Show strengths over time
    strengths_parser = subparsers.add_parser('strengths', help='Show strength distribution over time')
    strengths_parser.add_argument('--days', type=int, default=30, help='Days to look back')
    
    # Mark superseded
    supersede_parser = subparsers.add_parser('supersede', help='Mark memory as superseded')
    supersede_parser.add_argument('memory_id', help='Memory ID to supersede')
    supersede_parser.add_argument('--reason', default='superseded', help='Reason for superseding')
    
    # Forget memory
    forget_parser = subparsers.add_parser('forget', help='Forget (delete) memory')
    forget_parser.add_argument('memory_id', help='Memory ID to forget')
    forget_parser.add_argument('--permanent', action='store_true', help='Permanent deletion')
    
    # Show statistics
    subparsers.add_parser('stats', help='Show memory statistics')
    
    # Run maintenance
    subparsers.add_parser('maintenance', help='Run memory maintenance')
    
    # Test recall
    recall_parser = subparsers.add_parser('recall', help='Test memory recall')
    recall_parser.add_argument('question', help='Question to test')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    inspector = MemoryInspector()
    
    try:
        if args.command == 'list':
            inspector.list_memories(
                limit=args.limit,
                kind=args.kind,
                min_strength=args.min_strength,
                order_by=args.order_by
            )
        elif args.command == 'search':
            inspector.search_memories(args.query, args.limit)
        elif args.command == 'show':
            inspector.show_memory_details(args.memory_id)
        elif args.command == 'neighbors':
            inspector.show_neighbors(args.memory_id, args.limit)
        elif args.command == 'strengths':
            inspector.show_strengths_over_time(args.days)
        elif args.command == 'supersede':
            inspector.mark_superseded(args.memory_id, args.reason)
        elif args.command == 'forget':
            inspector.forget_memory(args.memory_id, args.permanent)
        elif args.command == 'stats':
            inspector.show_statistics()
        elif args.command == 'maintenance':
            inspector.run_maintenance()
        elif args.command == 'recall':
            inspector.test_recall(args.question)
    
    except KeyboardInterrupt:
        print("\n\n[Inspector] 👋 Inspector stopped by user")
    except Exception as e:
        print(f"\n[Inspector] ❌ Error: {e}")
        if '--debug' in sys.argv:
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    main()