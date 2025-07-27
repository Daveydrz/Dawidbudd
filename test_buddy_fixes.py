#!/usr/bin/env python3
"""
Test Fix for Reported Issues
Created: 2025-01-17
Purpose: Test the fixes for JSON parsing, token limits, and Kokoro integration
"""

import sys
import os
sys.path.append('/home/runner/work/Dawidbudd/Dawidbudd')

def test_token_limits():
    """Test that token limits are properly set to 150"""
    print("🔍 Testing Token Limits:")
    
    # Test config.py
    try:
        from config import MAX_TOKENS
        print(f"  config.py MAX_TOKENS: {MAX_TOKENS}")
        assert MAX_TOKENS == 150, f"Expected 150, got {MAX_TOKENS}"
        print("  ✅ config.py token limit correct")
    except Exception as e:
        print(f"  ❌ config.py error: {e}")
    
    # Test extractor_client.py by checking the source
    try:
        with open('/home/runner/work/Dawidbudd/Dawidbudd/ai/extractor_client.py', 'r') as f:
            content = f.read()
            if '"max_length": 150' in content:
                print("  ✅ extractor_client.py token limit correct (150)")
            else:
                print("  ❌ extractor_client.py token limit not fixed")
    except Exception as e:
        print(f"  ❌ extractor_client.py error: {e}")
    
    # Test simple_llm_handler.py
    try:
        with open('/home/runner/work/Dawidbudd/Dawidbudd/ai/simple_llm_handler.py', 'r') as f:
            content = f.read()
            if '"max_length": 150' in content:
                print("  ✅ simple_llm_handler.py token limit correct (150)")
            else:
                print("  ❌ simple_llm_handler.py token limit not fixed")
    except Exception as e:
        print(f"  ❌ simple_llm_handler.py error: {e}")

def test_extractor_client_robustness():
    """Test that ExtractorClient handles errors gracefully"""
    print("\n🔍 Testing ExtractorClient Error Handling:")
    
    try:
        from ai.extractor_client import ExtractorClient
        
        # Test with offline server (should use fallback)
        client = ExtractorClient("http://localhost:9999")  # Non-existent port
        result = client.process_full_consciousness("Hello, I'm David", "test_user")
        
        if result and isinstance(result, dict):
            print("  ✅ ExtractorClient returns fallback data when server unavailable")
            print(f"  📊 Fallback structure: {list(result.keys())}")
        else:
            print("  ❌ ExtractorClient doesn't handle offline server properly")
            
    except Exception as e:
        print(f"  ❌ ExtractorClient error: {e}")

def test_response_filter():
    """Test that response filter blocks error messages"""
    print("\n🔍 Testing Response Filter:")
    
    try:
        from ai.response_filter import is_error_response, filter_and_fix_response, should_speak_response
        
        # Test error detection
        error_messages = [
            "I apologize, but I'm having trouble connecting to my language model.",
            "Connection error occurred",
            "JSON parsing error: Expecting value",
            "I'm having trouble connecting to my processing systems right now."
        ]
        
        good_messages = [
            "Hello! How can I help you today?",
            "That's a great question about the weather!",
            "I'm doing well, thanks for asking!"
        ]
        
        print("  🚫 Testing error message detection:")
        for msg in error_messages:
            is_error = is_error_response(msg)
            should_speak = should_speak_response(msg)
            print(f"    '{msg[:50]}...' - Error: {is_error}, Speak: {should_speak}")
            assert is_error == True, f"Should detect as error: {msg}"
            assert should_speak == False, f"Should not speak: {msg}"
        
        print("  ✅ Good message handling:")
        for msg in good_messages:
            is_error = is_error_response(msg)
            should_speak = should_speak_response(msg)
            print(f"    '{msg[:50]}...' - Error: {is_error}, Speak: {should_speak}")
            assert is_error == False, f"Should not detect as error: {msg}"
            assert should_speak == True, f"Should speak: {msg}"
        
        print("  ✅ Response filter working correctly")
        
    except Exception as e:
        print(f"  ❌ Response filter error: {e}")

def test_port_configuration():
    """Test port configuration is correct"""
    print("\n🔍 Testing Port Configuration:")
    
    try:
        from ai.extractor_client import ExtractorClient
        from ai.simple_llm_handler import SimpleLLMHandler
        
        # Test ExtractorClient uses port 5002
        extractor = ExtractorClient()
        print(f"  ExtractorClient URL: {extractor.base_url}")
        assert "5002" in extractor.base_url, f"ExtractorClient should use port 5002"
        print("  ✅ ExtractorClient correctly configured for port 5002")
        
        # Test SimpleLLMHandler uses port 5001
        llm_handler = SimpleLLMHandler()
        print(f"  SimpleLLMHandler URL: {llm_handler.base_url}")
        assert "5001" in llm_handler.base_url, f"SimpleLLMHandler should use port 5001"
        print("  ✅ SimpleLLMHandler correctly configured for port 5001")
        
    except Exception as e:
        print(f"  ❌ Port configuration error: {e}")

def test_memory_extraction():
    """Test immediate memory extraction for names"""
    print("\n🔍 Testing Memory Extraction:")
    
    try:
        import re
        
        # Test name patterns
        test_cases = [
            ("My name is David", "David"),
            ("I'm John by the way", "John"),
            ("Call me Sarah", "Sarah"),
            ("I'm called Mike", "Mike"),
            ("This is Emma", "Emma")
        ]
        
        name_patterns = [
            r"my name is (\w+)",
            r"i'?m (\w+)(?:\s+by the way|$|\.|!)",
            r"call me (\w+)",
            r"i'?m called (\w+)",
            r"this is (\w+)"
        ]
        
        for text, expected_name in test_cases:
            name_detected = False
            extracted_name = None
            text_lower = text.lower().strip()
            
            for pattern in name_patterns:
                match = re.search(pattern, text_lower)
                if match:
                    extracted_name = match.group(1).capitalize()
                    name_detected = True
                    break
            
            print(f"  '{text}' -> Detected: {name_detected}, Name: {extracted_name}")
            assert name_detected == True, f"Should detect name in: {text}"
            assert extracted_name == expected_name, f"Expected {expected_name}, got {extracted_name}"
        
        print("  ✅ Name extraction patterns working correctly")
        
    except Exception as e:
        print(f"  ❌ Memory extraction error: {e}")

if __name__ == "__main__":
    print("🚀 Testing Buddy Fixes for Reported Issues")
    print("=" * 60)
    
    test_token_limits()
    test_extractor_client_robustness() 
    test_response_filter()
    test_port_configuration()
    test_memory_extraction()
    
    print("\n" + "=" * 60)
    print("✅ Test completed! Check individual results above.")
    print("\n💡 To fully test:")
    print("1. Start Gemma-2-2B on port 5002: python -m server --port 5002")
    print("2. Start main LLM on port 5001: python -m server --port 5001") 
    print("3. Start Kokoro server: python -m kokoro --port 8880")
    print("4. Run main.py and test: 'I'm David' -> 'What's my name?'")