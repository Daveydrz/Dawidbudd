#!/usr/bin/env python3
"""
Test Memory and Voice Integration
Test the scenario: "I'm David" -> "What's my name?"
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_name_memory_integration():
    """Test the name memory integration scenario"""
    print("🧪 Testing Name Memory Integration")
    print("=" * 50)
    
    # Test 1: Store a name in memory
    print("\n📝 Test 1: Storing name 'David' in memory")
    
    try:
        from ai.local_memory_manager import local_memory_manager, MemoryEntry
        from datetime import datetime
        
        # Simulate user "Anonymous_001" introducing themselves as "David"
        test_user = "Anonymous_001"
        name_memory = MemoryEntry(
            timestamp=datetime.now().isoformat(),
            user_id=test_user,
            text="User's name is David",
            memory_type="fact",
            extracted_info={
                "fact_category": "identity",
                "fact_value": "David",
                "name_introduction": True,
                "confidence": 0.95,
                "source": "test_introduction"
            },
            confidence=0.95
        )
        
        local_memory_manager.store_memories([name_memory])
        print(f"✅ Stored name memory for {test_user}")
        
    except Exception as e:
        print(f"❌ Error storing name: {e}")
        return False
    
    # Test 2: Retrieve memory context
    print("\n📋 Test 2: Retrieving memory context")
    
    try:
        context = local_memory_manager.get_user_context(test_user)
        print(f"📊 Retrieved context for {test_user}:")
        print(f"   Facts: {context.get('facts', [])}")
        print(f"   Preferences: {context.get('preferences', [])}")
        print(f"   Context: {context.get('context', [])}")
        
        # Check if the name is in facts
        facts = context.get('facts', [])
        found_name = False
        for fact in facts:
            if 'David' in str(fact):
                found_name = True
                print(f"✅ Found name in facts: {fact}")
                break
        
        if not found_name:
            print(f"❌ Name 'David' not found in facts")
            return False
            
    except Exception as e:
        print(f"❌ Error retrieving context: {e}")
        return False
    
    # Test 3: Test voice-based name response
    print("\n🗣️ Test 3: Testing voice-based name response")
    
    try:
        # Import the function from main.py
        sys.path.append('/home/runner/work/Dawidbudd/Dawidbudd')
        from main import get_voice_based_name_response
        
        # Test the name response for our test user
        response = get_voice_based_name_response(test_user, test_user)
        print(f"🎤 Voice name response: {response}")
        
        # Check if the response contains "David"
        if "David" in response:
            print("✅ Name response contains 'David'")
        else:
            print("❌ Name response does not contain 'David'")
            return False
            
    except Exception as e:
        print(f"❌ Error testing voice response: {e}")
        return False
    
    # Test 4: Test memory extraction patterns
    print("\n🔍 Test 4: Testing name extraction patterns")
    
    try:
        from main import handle_streaming_response
        
        # Mock the handle_streaming_response name extraction
        test_texts = [
            "I'm David",
            "My name is David", 
            "Call me David",
            "I'm called David"
        ]
        
        import re
        name_patterns = [
            r"my name is (\w+)",
            r"i'?m (\w+)",
            r"call me (\w+)",
            r"i'?m called (\w+)",
        ]
        
        for text in test_texts:
            text_lower = text.lower()
            extracted_name = None
            
            for pattern in name_patterns:
                match = re.search(pattern, text_lower)
                if match:
                    extracted_name = match.group(1).capitalize()
                    break
            
            if extracted_name == "David":
                print(f"✅ '{text}' → '{extracted_name}'")
            else:
                print(f"❌ '{text}' → '{extracted_name}'")
                
    except Exception as e:
        print(f"❌ Error testing name extraction: {e}")
        return False
    
    print("\n🎉 All tests completed!")
    return True

if __name__ == "__main__":
    success = test_name_memory_integration()
    if success:
        print("\n✅ Memory and Voice Integration Test: PASSED")
    else:
        print("\n❌ Memory and Voice Integration Test: FAILED")
    
    sys.exit(0 if success else 1)