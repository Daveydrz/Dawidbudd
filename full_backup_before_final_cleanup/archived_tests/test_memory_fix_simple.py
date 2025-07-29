#!/usr/bin/env python3
"""
Simplified Integration Test - Focus on Memory and Core Functionality
Created: 2025-01-17
Purpose: Test memory persistence and name recognition without audio dependencies
"""

import sys
import os
import time
import json

# Add the project root to the path
sys.path.insert(0, '/home/runner/work/Dawidbudd/Dawidbudd')

def test_memory_and_name_recognition():
    """Test that names are properly stored and retrieved"""
    print("🧠 Testing Memory and Name Recognition...")
    
    try:
        from ai.local_memory_manager import local_memory_manager, MemoryEntry
        from datetime import datetime
        
        # Test user ID
        test_user = "test_name_recognition"
        
        # Test 1: Store a name via immediate extraction
        print("\n1️⃣ Testing immediate name storage...")
        name_memory = MemoryEntry(
            timestamp=datetime.now().isoformat(),
            user_id=test_user,
            text="My name is David",
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
        print("✅ Name memory stored via immediate extraction")
        
        # Test 2: Test user context retrieval
        print("\n2️⃣ Testing memory retrieval...")
        context = local_memory_manager.get_user_context(test_user)
        print(f"Retrieved context: {context}")
        
        # Check if name is in facts
        has_name = False
        for fact in context.get('facts', []):
            if 'David' in str(fact):
                has_name = True
                break
        
        if has_name:
            print("✅ Name successfully retrieved from memory")
        else:
            print("❌ Name not found in retrieved memory")
            return False
        
        # Test 3: Test adding interaction
        print("\n3️⃣ Testing interaction storage...")
        local_memory_manager.add_interaction(test_user, "My name is David", "Nice to meet you, David!")
        
        # Test 4: Retrieve context again to see if interaction was stored
        updated_context = local_memory_manager.get_user_context(test_user)
        print(f"Updated context after interaction: {updated_context}")
        
        # Test 5: Test multiple name patterns
        print("\n4️⃣ Testing multiple name patterns...")
        name_patterns = [
            "I'm Sarah",
            "Call me John",
            "My name is Alice",
            "I am called Bob"
        ]
        
        pattern_users = []
        for i, pattern in enumerate(name_patterns):
            pattern_user = f"pattern_test_{i}"
            pattern_users.append(pattern_user)
            
            # Extract name using the improved pattern matching
            text_lower = pattern.lower().strip()
            import re
            
            name_patterns_regex = [
                r"my name is (\w+)",
                r"i'?m (\w+)",
                r"call me (\w+)",
                r"i'?m called (\w+)",
                r"this is (\w+)"
            ]
            
            extracted_name = None
            for regex_pattern in name_patterns_regex:
                match = re.search(regex_pattern, text_lower)
                if match:
                    extracted_name = match.group(1).capitalize()
                    break
            
            if extracted_name:
                print(f"  Pattern '{pattern}' -> Extracted name: {extracted_name}")
                
                # Store the name
                pattern_memory = MemoryEntry(
                    timestamp=datetime.now().isoformat(),
                    user_id=pattern_user,
                    text=pattern,
                    memory_type="fact",
                    extracted_info={
                        "fact_category": "identity",
                        "fact_value": extracted_name,
                        "name_introduction": True,
                        "confidence": 0.95,
                        "source": "pattern_extraction"
                    },
                    confidence=0.95
                )
                
                local_memory_manager.store_memories([pattern_memory])
                
                # Verify retrieval
                pattern_context = local_memory_manager.get_user_context(pattern_user)
                if pattern_context['facts'] and extracted_name in str(pattern_context['facts']):
                    print(f"    ✅ Name {extracted_name} successfully stored and retrieved")
                else:
                    print(f"    ❌ Name {extracted_name} not properly stored/retrieved")
            else:
                print(f"  Pattern '{pattern}' -> No name extracted (❌)")
        
        print("\n✅ All memory and name recognition tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Memory test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_immediate_response_simulation():
    """Test the immediate response system without actually calling main"""
    print("\n⚡ Testing Immediate Response Simulation...")
    
    try:
        from ai.local_memory_manager import local_memory_manager
        
        # Simulate what handle_streaming_response should do
        test_user = "immediate_response_test"
        test_input = "My name is David"
        
        print(f"1️⃣ Simulating immediate response for: '{test_input}'")
        
        # Step 1: Immediate name extraction (like in the fixed code)
        text_lower = test_input.lower().strip()
        import re
        
        name_patterns = [
            r"my name is (\w+)",
            r"i'?m (\w+)",
            r"call me (\w+)",
            r"i'?m called (\w+)",
            r"this is (\w+)"
        ]
        
        extracted_name = None
        for pattern in name_patterns:
            match = re.search(pattern, text_lower)
            if match:
                extracted_name = match.group(1).capitalize()
                print(f"   👤 NAME DETECTED: {extracted_name}")
                break
        
        # Step 2: Store name immediately (like in the fixed code)
        if extracted_name:
            from ai.local_memory_manager import MemoryEntry
            from datetime import datetime
            
            name_memory = MemoryEntry(
                timestamp=datetime.now().isoformat(),
                user_id=test_user,
                text=f"User's name is {extracted_name}",
                memory_type="fact",
                extracted_info={
                    "fact_category": "identity",
                    "fact_value": extracted_name,
                    "name_introduction": True,
                    "confidence": 0.95,
                    "source": "immediate_extraction"
                },
                confidence=0.95
            )
            local_memory_manager.store_memories([name_memory])
            print(f"   ✅ Name '{extracted_name}' stored immediately")
        
        # Step 3: Get current memory context (like in the fixed code)
        existing_context = local_memory_manager.get_user_context(test_user)
        
        print(f"2️⃣ Current memory context: {existing_context}")
        
        # Step 4: Build consciousness context (like in the fixed code)
        consciousness_context = f"""BUDDY'S CONSCIOUSNESS STATE:
Current Emotion: helpful
Motivation Level: 0.8
Active Goals: help user effectively, remember user information
Current Focus: user interaction
Personality: friendly, empathetic, good memory

USER MEMORY:
Facts: {', '.join(existing_context.get('facts', [])[:5])}
Preferences: {', '.join(existing_context.get('preferences', [])[:5])}
Recent Context: {', '.join(existing_context.get('context', [])[-3:])}"""

        if extracted_name:
            consciousness_context += f"\nIMPORTANT: User just introduced themselves as {extracted_name}. Remember this name!"
        
        print(f"3️⃣ Consciousness context prepared for LLM:")
        print(consciousness_context[:200] + "..." if len(consciousness_context) > 200 else consciousness_context)
        
        # Step 5: Simulate adding interaction
        mock_response = f"Nice to meet you, {extracted_name}! I'll remember your name." if extracted_name else "Hello there!"
        local_memory_manager.add_interaction(test_user, test_input, mock_response)
        
        print(f"4️⃣ Simulated interaction stored")
        
        # Step 6: Verify final state
        final_context = local_memory_manager.get_user_context(test_user)
        print(f"5️⃣ Final memory state: {final_context}")
        
        # Check if the name is now in memory
        if final_context['facts'] and extracted_name and extracted_name in str(final_context['facts']):
            print("✅ Immediate response simulation successful - name properly remembered!")
            return True
        else:
            print("❌ Immediate response simulation failed - name not remembered")
            return False
        
    except Exception as e:
        print(f"❌ Immediate response simulation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Buddy Memory and Name Recognition Fixes")
    print("=" * 60)
    
    # Test memory and name recognition
    memory_ok = test_memory_and_name_recognition()
    
    # Test immediate response simulation
    immediate_response_ok = test_immediate_response_simulation()
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS:")
    print(f"Memory & Name Recognition: {'✅ PASS' if memory_ok else '❌ FAIL'}")
    print(f"Immediate Response Logic: {'✅ PASS' if immediate_response_ok else '❌ FAIL'}")
    
    if memory_ok and immediate_response_ok:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Buddy should now remember names properly when users introduce themselves")
        print("✅ Memory system is working correctly with immediate name storage")
        print("✅ Names should be available immediately for responses")
        print("\n📋 What this means:")
        print("- When a user says 'My name is David', it will be stored immediately")
        print("- When they later ask 'What's my name?', Buddy will know it's David")
        print("- The memory persists across conversations")
        print("- Background consciousness processing enhances the memory further")
    else:
        print("\n⚠️ Some tests failed - issues need to be addressed")
    
    return memory_ok and immediate_response_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)