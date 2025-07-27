#!/usr/bin/env python3
"""
Test Gemma Extractor Client Integration
Tests the new architecture with Gemma-2-2B classification on CPU
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_extractor_client():
    """Test the Gemma extractor client"""
    print("🧪 Testing Gemma Extractor Client")
    
    try:
        from ai.extractor_client import classify_message, get_extractor_status
        
        # Test status
        status = get_extractor_status()
        print(f"📊 Extractor status: {status}")
        
        # Test messages
        test_messages = [
            "I like pizza",
            "My name is David",
            "I'm going to the shop",
            "What time is it?",
            "I'm feeling sad today"
        ]
        
        print("\n🔍 Testing message classification:")
        for msg in test_messages:
            result = classify_message(msg)
            print(f"'{msg}' -> {result}")
            
        return True
        
    except Exception as e:
        print(f"❌ Extractor client test failed: {e}")
        return False

def test_memory_manager_update():
    """Test the new update_memory function"""
    print("\n🧪 Testing Memory Manager Update")
    
    try:
        from ai.local_memory_manager import LocalMemoryManager
        
        manager = LocalMemoryManager()
        
        # Test classification result
        test_classification = {
            "memory_type": "preference",
            "intent": "statement",
            "emotion": "joy",
            "name_introduction": False
        }
        
        result = manager.update_memory("test_user", "I love chocolate cake", test_classification)
        print(f"✅ Memory update result: {result}")
        
        # Test name introduction
        name_classification = {
            "memory_type": "fact",
            "intent": "statement", 
            "emotion": "neutral",
            "name_introduction": True
        }
        
        result = manager.update_memory("test_user", "My name is John", name_classification)
        print(f"✅ Name introduction result: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Memory manager test failed: {e}")
        return False

def test_llm_handler():
    """Test the LLM handler with minimal prompts"""
    print("\n🧪 Testing LLM Handler")
    
    try:
        from ai.llm_handler import LLMHandler
        
        handler = LLMHandler()
        
        # Test minimal prompt building
        prompt = handler._build_minimal_prompt("How are you?", "test_user")
        print(f"✅ Minimal prompt generated ({len(prompt)} chars)")
        print(f"Preview: {prompt[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ LLM handler test failed: {e}")
        return False

def test_integration_flow():
    """Test the full integration flow"""
    print("\n🧪 Testing Full Integration Flow")
    
    try:
        # Step 1: Classify with Gemma (fallback)
        from ai.extractor_client import classify_message
        classification = classify_message("I like programming")
        print(f"1️⃣ Classification: {classification}")
        
        # Step 2: Update memory
        from ai.local_memory_manager import LocalMemoryManager
        manager = LocalMemoryManager()
        memory_result = manager.update_memory("test_user", "I like programming", classification)
        print(f"2️⃣ Memory update: {memory_result}")
        
        # Step 3: Build LLM prompt
        from ai.llm_handler import LLMHandler
        handler = LLMHandler()
        prompt = handler._build_minimal_prompt("Tell me about programming", "test_user")
        print(f"3️⃣ LLM prompt ready: {len(prompt)} chars")
        
        print("✅ Full integration flow successful!")
        return True
        
    except Exception as e:
        print(f"❌ Integration flow test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Gemma Extractor Integration")
    print("=" * 50)
    
    tests = [
        test_extractor_client,
        test_memory_manager_update,
        test_llm_handler,
        test_integration_flow
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed! Gemma extractor integration ready.")
    else:
        print("⚠️ Some tests failed. Check configuration and dependencies.")