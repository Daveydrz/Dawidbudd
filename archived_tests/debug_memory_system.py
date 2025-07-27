#!/usr/bin/env python3
"""
Memory System Debugging Script
Specifically tests the "I'm David" -> "What's my name?" scenario
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

def debug_name_memory_workflow():
    """Debug the complete name memory workflow"""
    print("🔍 DEBUGGING NAME MEMORY WORKFLOW")
    print("="*50)
    
    try:
        from ai.local_memory_manager import local_memory_manager, MemoryEntry
        from datetime import datetime
        
        # Step 1: Clear memory for clean test
        user_id = "debug_user"
        if "users" in local_memory_manager.memory_data:
            if user_id in local_memory_manager.memory_data["users"]:
                del local_memory_manager.memory_data["users"][user_id]
        
        print("🧹 Cleared previous memory data")
        
        # Step 2: Simulate "I'm David" input
        print("\n👤 User says: 'I'm David'")
        
        # Create name memory entry
        name_memory = MemoryEntry(
            timestamp=datetime.now().isoformat(),
            user_id=user_id,
            text="User's name is David",
            memory_type="fact",
            extracted_info={
                "fact_category": "identity",
                "fact_value": "David",
                "name_introduction": True,
                "confidence": 0.95,
                "source": "immediate_extraction"
            },
            confidence=0.95
        )
        
        local_memory_manager.store_memories([name_memory])
        print("✅ Name stored in memory system")
        
        # Step 3: Check memory storage
        print("\n🔍 Checking memory storage...")
        user_data = local_memory_manager.memory_data.get("users", {}).get(user_id, {})
        facts = user_data.get("facts", [])
        
        print(f"Raw facts stored: {len(facts)}")
        for i, fact in enumerate(facts):
            print(f"  Fact {i+1}: {fact}")
        
        # Step 4: Test memory retrieval
        print("\n📋 Testing memory retrieval...")
        context = local_memory_manager.get_user_context(user_id)
        print(f"Retrieved context: {context}")
        
        # Step 5: Simulate "What's my name?" query
        print("\n❓ User asks: 'What's my name?'")
        
        # Check if name can be found
        found_name = None
        facts_list = context.get('facts', [])
        
        for fact in facts_list:
            fact_lower = fact.lower()
            if 'david' in fact_lower or ('name' in fact_lower and 'david' in fact_lower):
                found_name = "David"
                break
        
        if found_name:
            print(f"✅ SUCCESS: Found name '{found_name}' in memory")
            print(f"   Buddy should respond: 'Your name is {found_name}'")
        else:
            print("❌ FAILURE: Name not found in memory")
            print("   This would cause Buddy to say 'I don't hold any memory'")
        
        # Step 6: Test memory persistence
        print("\n💾 Testing memory persistence...")
        local_memory_manager._save_memory()
        
        # Load fresh instance
        from ai.local_memory_manager import LocalMemoryManager
        fresh_manager = LocalMemoryManager()
        fresh_context = fresh_manager.get_user_context(user_id)
        
        if fresh_context.get('facts'):
            print("✅ Memory persists across instances")
        else:
            print("❌ Memory does not persist across instances")
        
        # Step 7: Show detailed memory structure
        print("\n📊 DETAILED MEMORY STRUCTURE:")
        memory_file = local_memory_manager.memory_file
        if os.path.exists(memory_file):
            with open(memory_file, 'r') as f:
                memory_data = json.load(f)
            
            if user_id in memory_data.get("users", {}):
                user_memory = memory_data["users"][user_id]
                print(f"Facts: {len(user_memory.get('facts', []))}")
                print(f"Preferences: {len(user_memory.get('preferences', []))}")
                print(f"Context: {len(user_memory.get('context', []))}")
                
                print("\nDetailed facts:")
                for fact in user_memory.get('facts', []):
                    print(f"  - {fact}")
        
        return found_name is not None
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def debug_relationship_memory():
    """Debug relationship memory like 'My nephew name is Zac'"""
    print("\n👨‍👩‍👧‍👦 DEBUGGING RELATIONSHIP MEMORY")
    print("="*50)
    
    try:
        from ai.local_memory_manager import local_memory_manager, MemoryEntry
        from datetime import datetime
        
        user_id = "relationship_user"
        
        # Test relationship memory
        print("👤 User says: 'My nephew name is Zac'")
        
        relationship_memory = MemoryEntry(
            timestamp=datetime.now().isoformat(),
            user_id=user_id,
            text="My nephew name is Zac",
            memory_type="fact",
            extracted_info={
                "fact_category": "family",
                "fact_value": "nephew name is Zac",
                "relationship": "nephew",
                "name": "Zac",
                "confidence": 0.9
            },
            confidence=0.9
        )
        
        local_memory_manager.store_memories([relationship_memory])
        print("✅ Relationship stored")
        
        # Test retrieval
        context = local_memory_manager.get_user_context(user_id)
        print(f"Retrieved context: {context}")
        
        # Check if relationship is found
        facts = context.get('facts', [])
        found_relationship = any('zac' in fact.lower() and 'nephew' in fact.lower() for fact in facts)
        
        if found_relationship:
            print("✅ SUCCESS: Relationship memory working")
            print("   Buddy should respond: 'Your nephew's name is Zac'")
        else:
            print("❌ FAILURE: Relationship memory not working")
        
        return found_relationship
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def debug_multi_day_memory():
    """Debug memory persistence across days"""
    print("\n📅 DEBUGGING MULTI-DAY MEMORY PERSISTENCE")
    print("="*50)
    
    try:
        from ai.local_memory_manager import local_memory_manager
        
        # Check if memory file exists and has data
        memory_file = local_memory_manager.memory_file
        
        if os.path.exists(memory_file):
            with open(memory_file, 'r') as f:
                memory_data = json.load(f)
            
            total_users = len(memory_data.get("users", {}))
            total_memories = 0
            
            for user_id, user_data in memory_data.get("users", {}).items():
                user_memories = (len(user_data.get('facts', [])) + 
                               len(user_data.get('preferences', [])) + 
                               len(user_data.get('context', [])))
                total_memories += user_memories
                
                print(f"User {user_id}: {user_memories} memories")
            
            print(f"\n📊 Total: {total_users} users, {total_memories} memories")
            
            if total_memories > 0:
                print("✅ Memory persistence is working")
                return True
            else:
                print("⚠️  No memories found in file")
                return False
        else:
            print("❌ Memory file does not exist")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    print("🔍 COMPREHENSIVE MEMORY SYSTEM DEBUG")
    print("="*60)
    
    results = {
        "name_memory": debug_name_memory_workflow(),
        "relationship_memory": debug_relationship_memory(),
        "multi_day_persistence": debug_multi_day_memory()
    }
    
    print("\n📊 DEBUG RESULTS SUMMARY:")
    print("="*40)
    
    for test_name, result in results.items():
        status = "✅ WORKING" if result else "❌ BROKEN"
        print(f"{status} {test_name.replace('_', ' ').title()}")
    
    working_count = sum(results.values())
    total_count = len(results)
    
    print(f"\n🎯 Overall: {working_count}/{total_count} memory systems working")
    
    if working_count == total_count:
        print("🎉 MEMORY SYSTEM FULLY FUNCTIONAL!")
    else:
        print("🚨 MEMORY SYSTEM NEEDS FIXES")
        
        if not results["name_memory"]:
            print("   → Fix name storage and retrieval")
        if not results["relationship_memory"]:
            print("   → Fix relationship memory processing")
        if not results["multi_day_persistence"]:
            print("   → Fix memory file persistence")

if __name__ == "__main__":
    main()
