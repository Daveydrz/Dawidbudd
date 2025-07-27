#!/usr/bin/env python3
"""
Simple Name Memory Test - Test the exact scenario mentioned by Daveydrz
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

def test_name_memory():
    """Test the exact scenario: 'I'm David' -> 'What's my name?'"""
    print("🧠 TESTING NAME MEMORY SCENARIO")
    print("="*50)
    
    try:
        from ai.local_memory_manager import local_memory_manager, MemoryEntry
        from datetime import datetime
        
        user_id = "test_user"
        
        # Clear any existing memory for clean test
        local_memory_manager.memory_data["users"] = {}
        
        print("🔄 Step 1: User says 'I'm David'")
        
        # Simulate the name introduction processing
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
        print("✅ Name 'David' stored in memory")
        
        print("\n🔄 Step 2: Getting memory context...")
        context = local_memory_manager.get_user_context(user_id)
        print(f"Memory context retrieved: {context}")
        
        print("\n🔄 Step 3: User asks 'What's my name?'")
        
        # Check if the name is properly retrieved
        facts = context.get('facts', [])
        user_name = None
        
        for fact in facts:
            if 'david' in fact.lower() or 'name' in fact.lower():
                user_name = "David"
                break
        
        if user_name:
            print(f"✅ SUCCESS: Found user name '{user_name}' in memory")
            print(f"   Buddy should respond: 'Your name is {user_name}'")
        else:
            print("❌ FAILURE: Name not found in memory!")
            print("   This is the bug - Buddy would say 'I don't hold any memory'")
        
        # Test memory persistence
        print("\n🔄 Step 4: Testing memory persistence...")
        local_memory_manager._save_memory()
        
        # Create new instance to test loading
        from ai.local_memory_manager import LocalMemoryManager
        new_manager = LocalMemoryManager()
        new_context = new_manager.get_user_context(user_id)
        
        if new_context.get('facts'):
            print("✅ Memory persists across instances")
        else:
            print("❌ Memory does not persist!")
        
        # Show detailed memory structure
        print("\n📊 DETAILED MEMORY STRUCTURE:")
        if user_id in local_memory_manager.memory_data["users"]:
            user_data = local_memory_manager.memory_data["users"][user_id]
            print(f"Facts: {user_data.get('facts', [])}")
            print(f"Preferences: {user_data.get('preferences', [])}")
            print(f"Context: {user_data.get('context', [])}")
        
        return user_name is not None
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_consciousness_integration():
    """Test port 5002 consciousness processing"""
    print("\n🧠 TESTING PORT 5002 CONSCIOUSNESS INTEGRATION")
    print("="*50)
    
    try:
        from ai.extractor_client import process_full_consciousness
        
        # Test with the name introduction
        result = process_full_consciousness("I'm David", "test_user")
        
        print("✅ Port 5002 consciousness processing result:")
        print(f"  Classification: {result.get('classification', {})}")
        print(f"  Memory Updates: {result.get('memory_updates', {})}")
        print(f"  Emotional State: {result.get('emotional_state', {})}")
        
        return True
        
    except Exception as e:
        print(f"❌ Port 5002 processing failed: {e}")
        print("   This means Gemma server is not running on port 5002")
        return False

def test_port_5001_response():
    """Test port 5001 response generation only"""
    print("\n🎯 TESTING PORT 5001 RESPONSE GENERATION")
    print("="*50)
    
    try:
        from ai.simple_llm_handler import generate_response_with_consciousness
        
        consciousness_context = """BUDDY'S CONSCIOUSNESS STATE:
Current Emotion: friendly
Motivation Level: 0.8
Active Goals: help user effectively, remember user information
Current Focus: user question
Personality: friendly, empathetic, good memory

USER MEMORY:
Facts: User's name is David
Preferences: 
Recent Context: User introduced themselves as David"""
        
        print("Testing response to 'What's my name?' with consciousness context...")
        
        response_chunks = []
        for chunk in generate_response_with_consciousness("What's my name?", "test_user", consciousness_context):
            response_chunks.append(chunk)
            print(f"Chunk: '{chunk}'")
        
        full_response = ''.join(response_chunks)
        print(f"\nFull response: {full_response}")
        
        # Check if response includes the name
        if 'david' in full_response.lower():
            print("✅ SUCCESS: Response includes the user's name")
            return True
        else:
            print("❌ FAILURE: Response doesn't include the user's name")
            return False
        
    except Exception as e:
        print(f"❌ Port 5001 response generation failed: {e}")
        print("   This means main LLM server is not running on port 5001")
        return False

def main():
    print("🧪 COMPREHENSIVE BUDDY MEMORY & CONSCIOUSNESS TEST")
    print("="*80)
    
    test_results = {
        "name_memory": test_name_memory(),
        "consciousness_integration": test_consciousness_integration(),
        "response_generation": test_port_5001_response()
    }
    
    print("\n📊 TEST RESULTS SUMMARY:")
    print("="*50)
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name.replace('_', ' ').title()}")
    
    total_passed = sum(test_results.values())
    total_tests = len(test_results)
    
    print(f"\nOverall: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("🎉 ALL TESTS PASSED - Buddy consciousness is working correctly!")
    else:
        print("🚨 SOME TESTS FAILED - Issues need to be fixed")
        
        # Provide specific guidance
        if not test_results["consciousness_integration"]:
            print("   → Start Gemma-2-2B server on port 5002")
        
        if not test_results["response_generation"]:
            print("   → Start main LLM server on port 5001")
        
        if not test_results["name_memory"]:
            print("   → Fix memory storage and retrieval system")

if __name__ == "__main__":
    main()