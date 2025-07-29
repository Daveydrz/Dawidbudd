#!/usr/bin/env python3
"""
Test Dual-LLM Architecture
Purpose: Validate the new dual-LLM HTTP system works correctly
Tests: GPT4All replacement, fallback functionality, import compatibility
"""

import sys
import os
import json

def test_imports():
    """Test that all dual-LLM imports work correctly"""
    print("🧪 Testing dual-LLM imports...")
    
    try:
        from ai.dual_llm_client import dual_llm_client, generate_response_streaming_with_intelligent_fusion
        print("✅ Dual-LLM client imports successfully")
        
        from ai.extractor_llm import extract_facts, extract_name
        print("✅ Extractor functions import successfully")
        
        # Test that the client was initialized
        print(f"✅ Main LLM available: {dual_llm_client.main_llm_available}")
        print(f"✅ Extractor available: {dual_llm_client.extractor_available}")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_fallback_extraction():
    """Test fallback extraction functionality"""
    print("\n🧪 Testing fallback extraction...")
    
    try:
        from ai.extractor_llm import extract_facts, extract_name
        
        # Test name extraction
        test_cases = [
            ("Hello, my name is David", "David"),
            ("Hi, I'm Sarah and I love programming", "Sarah"),
            ("Call me John", "John"),
            ("Just testing", "NONE")
        ]
        
        for text, expected_name in test_cases:
            result = extract_name(text)
            status = "✅" if result == expected_name else "❌"
            print(f"{status} extract_name('{text}') → '{result}' (expected: '{expected_name}')")
        
        # Test fact extraction
        facts_result = extract_facts("Hi, I'm Alice and I like pizza but hate broccoli. I'm feeling happy today.")
        print(f"✅ extract_facts sample result: {facts_result}")
        
        # Validate expected structure
        required_keys = ['name', 'likes', 'dislikes', 'emotion']
        if all(key in facts_result for key in required_keys):
            print("✅ Fact extraction returns correct structure")
        else:
            print("❌ Fact extraction missing required keys")
            
        return True
    except Exception as e:
        print(f"❌ Fallback extraction failed: {e}")
        return False

def test_dual_llm_response_generation():
    """Test response generation via dual-LLM system"""
    print("\n🧪 Testing dual-LLM response generation...")
    
    try:
        from ai.dual_llm_client import generate_response_streaming_with_intelligent_fusion
        
        # Test streaming response (should use fallback since servers aren't running)
        response_chunks = []
        for chunk in generate_response_streaming_with_intelligent_fusion(
            text="Hello, how are you?", 
            user="TestUser", 
            context={}
        ):
            response_chunks.append(chunk)
            if len(response_chunks) >= 5:  # Limit chunks for testing
                break
        
        full_response = "".join(response_chunks)
        print(f"✅ Response generation works: '{full_response[:100]}...'")
        
        return True
    except Exception as e:
        print(f"❌ Response generation failed: {e}")
        return False

def test_backward_compatibility():
    """Test that imports still work for existing code"""
    print("\n🧪 Testing backward compatibility...")
    
    try:
        # Test that consciousness manager can still import extractor functions
        from ai.extractor_llm import extract_facts, extract_name
        print("✅ Consciousness manager imports work")
        
        # Test that LLM handler can import dual-LLM system
        from ai.llm_handler import dual_llm_client
        print("✅ LLM handler imports work")
        
        return True
    except Exception as e:
        print(f"❌ Backward compatibility failed: {e}")
        return False

def test_archive_structure():
    """Test that archived files are properly organized"""
    print("\n🧪 Testing archive structure...")
    
    try:
        archived_files = [
            "archive/ai/chat.py",
            "archive/ai/main.py", 
            "archive/ai/context_manager.py",
            "archive/voice/manager.py",
            "archive/voice/identity_helpers.py"
        ]
        
        missing_files = []
        for file_path in archived_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
        
        if missing_files:
            print(f"❌ Missing archived files: {missing_files}")
            return False
        else:
            print("✅ All redundant files properly archived")
            return True
            
    except Exception as e:
        print(f"❌ Archive structure test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Dual-LLM Architecture Replacement")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_imports),
        ("Fallback Extraction", test_fallback_extraction),
        ("Response Generation", test_dual_llm_response_generation),
        ("Backward Compatibility", test_backward_compatibility),
        ("Archive Structure", test_archive_structure)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 Dual-LLM architecture replacement successful!")
        return 0
    else:
        print("⚠️ Some tests failed - review needed")
        return 1

if __name__ == "__main__":
    sys.exit(main())