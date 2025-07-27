#!/usr/bin/env python3
"""
Test LLM Integration with Consciousness and Tokenization
Created: 2025-01-17
Purpose: Test all LLM integrations as requested by @Daveydrz
"""

import sys
import os
import time
import json
import requests
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, '/home/runner/work/Dawidbudd/Dawidbudd')

def test_llm_connection():
    """Test basic LLM connection to KoboldCPP"""
    print("🔌 Testing LLM Connection to KoboldCPP...")
    
    try:
        from config import KOBOLD_URL, MAX_TOKENS, TEMPERATURE
        print(f"   📍 LLM URL: {KOBOLD_URL}")
        print(f"   🎯 Max tokens: {MAX_TOKENS}")
        print(f"   🌡️ Temperature: {TEMPERATURE}")
        
        # Test basic connection
        payload = {
            "model": "llama3",
            "messages": [{"role": "user", "content": "Hello, are you working?"}],
            "max_tokens": 10,
            "temperature": 0.7,
            "stream": False
        }
        
        response = requests.post(KOBOLD_URL, json=payload, timeout=10)
        
        if response.status_code == 200:
            print("   ✅ LLM Connection: SUCCESS")
            data = response.json()
            if 'choices' in data and len(data['choices']) > 0:
                content = data['choices'][0]['message']['content']
                print(f"   💬 Response: {content[:100]}...")
                return True
            else:
                print("   ❌ Invalid response format")
                return False
        else:
            print(f"   ❌ LLM Connection: FAILED (Status: {response.status_code})")
            return False
            
    except requests.exceptions.ConnectionError:
        print("   ❌ LLM Connection: REFUSED - KoboldCPP not running")
        print("   💡 Please start KoboldCPP server at localhost:5001")
        return False
    except Exception as e:
        print(f"   ❌ LLM Connection: ERROR - {e}")
        return False

def test_consciousness_tokenizer():
    """Test consciousness tokenizer integration"""
    print("\n🧠 Testing Consciousness Tokenizer Integration...")
    
    try:
        from ai.consciousness_tokenizer import (
            tokenize_consciousness_for_llm,
            get_consciousness_summary_for_llm
        )
        
        # Test consciousness state
        test_state = {
            'emotion_engine': {'primary_emotion': 'engaged', 'intensity': 0.8},
            'motivation_system': {'active_goals': [{'description': 'Help user', 'priority': 0.9}]},
            'global_workspace': {'current_focus': 'user_conversation'},
            'self_model': {'reflection': 'I am responding to user questions'},
            'inner_monologue': {'current_thought': 'The user seems curious about AI'}
        }
        
        tokenized = tokenize_consciousness_for_llm(test_state)
        summary = get_consciousness_summary_for_llm(test_state)
        
        print(f"   ✅ Tokenizer working: {len(tokenized)} characters")
        print(f"   📝 Tokenized: {tokenized[:80]}...")
        print(f"   📋 Summary: {summary}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Consciousness Tokenizer: ERROR - {e}")
        return False

def test_integrated_prompt_generation():
    """Test integrated prompt generation with consciousness"""
    print("\n🎯 Testing Integrated Prompt Generation...")
    
    try:
        from ai.llm_handler import process_user_input_with_consciousness
        
        test_input = "Hello! Can you help me understand AI consciousness?"
        test_user = "integration_test"
        
        analysis = process_user_input_with_consciousness(test_input, test_user)
        
        if analysis:
            print("   ✅ Integrated analysis working")
            print(f"   🏷️ Components: {list(analysis.keys())}")
            
            # Check for consciousness integration
            if 'consciousness' in analysis:
                print(f"   🧠 Consciousness: {analysis['consciousness'][:50]}...")
            
            # Check for tokenization
            if 'tokenized_prompt' in analysis:
                print(f"   🏷️ Tokenized prompt: {len(analysis['tokenized_prompt'])} chars")
                
            return True
        else:
            print("   ❌ No analysis returned")
            return False
            
    except Exception as e:
        print(f"   ❌ Integrated Prompt Generation: ERROR - {e}")
        return False

def test_end_to_end_integration():
    """Test complete end-to-end integration"""
    print("\n🔄 Testing End-to-End Integration...")
    
    try:
        from ai.llm_handler import generate_consciousness_integrated_response
        
        test_input = "What is artificial intelligence?"
        test_user = "e2e_test"
        
        print(f"   📝 Testing with: '{test_input}'")
        print(f"   👤 User: {test_user}")
        
        # Try to generate response
        response_chunks = []
        chunk_count = 0
        
        for chunk in generate_consciousness_integrated_response(test_input, test_user):
            if chunk:
                response_chunks.append(chunk)
                chunk_count += 1
                print(f"   📦 Chunk {chunk_count}: {chunk[:30]}...")
                
                # Only get first few chunks for testing
                if chunk_count >= 3:
                    break
        
        if response_chunks:
            full_response = ''.join(response_chunks)
            print(f"   ✅ E2E Integration: SUCCESS")
            print(f"   📊 Generated {chunk_count} chunks, {len(full_response)} chars total")
            print(f"   💬 Sample: {full_response[:100]}...")
            return True
        else:
            print("   ❌ No response chunks generated")
            return False
            
    except Exception as e:
        print(f"   ❌ End-to-End Integration: ERROR - {e}")
        return False

def test_voice_integration():
    """Test voice system integration"""
    print("\n🎤 Testing Voice System Integration...")
    
    try:
        # Test voice manager integration
        from main import voice_manager
        
        if hasattr(voice_manager, 'handle_voice_identification'):
            print("   ✅ Voice manager: Available")
            
            # Test session stats
            if hasattr(voice_manager, 'get_session_stats'):
                stats = voice_manager.get_session_stats()
                print(f"   📊 Session stats: {stats}")
                
            return True
        else:
            print("   ❌ Voice manager: Missing handle_voice_identification method")
            return False
            
    except Exception as e:
        print(f"   ❌ Voice Integration: ERROR - {e}")
        return False

def test_memory_integration():
    """Test memory system integration"""
    print("\n💾 Testing Memory System Integration...")
    
    try:
        from ai.memory import add_to_conversation_history, get_conversation_context
        
        # Test adding memory
        test_user = "memory_test"
        test_question = "How does memory work?"
        test_response = "Memory works by storing and retrieving information."
        
        add_to_conversation_history(test_user, test_question, test_response)
        
        # Test retrieving memory
        context = get_conversation_context(test_user, 2)
        
        if context:
            print("   ✅ Memory system: Working")
            print(f"   📝 Context: {len(context)} items")
            return True
        else:
            print("   ❌ Memory system: No context retrieved")
            return False
            
    except Exception as e:
        print(f"   ❌ Memory Integration: ERROR - {e}")
        return False

def main():
    """Run all integration tests"""
    print("🚀 LLM Integration Test Suite")
    print("=" * 50)
    
    tests = [
        ("LLM Connection", test_llm_connection),
        ("Consciousness Tokenizer", test_consciousness_tokenizer),
        ("Integrated Prompts", test_integrated_prompt_generation),
        ("End-to-End Integration", test_end_to_end_integration),
        ("Voice Integration", test_voice_integration),
        ("Memory Integration", test_memory_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"   ❌ {test_name}: CRITICAL ERROR - {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("🧪 Integration Test Results")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if success:
            passed += 1
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All integration tests passed!")
    else:
        print("⚠️ Some tests failed - check LLM server connection")
        
        # Specific guidance for failures
        if not results[0][1]:  # LLM connection failed
            print("\n💡 To fix LLM connection:")
            print("   1. Start KoboldCPP server:")
            print("      cd /path/to/koboldcpp")
            print("      python koboldcpp.py --host 0.0.0.0 --port 5001")
            print("   2. Or update config.py with correct LLM URL")
            print("   3. Ensure firewall allows connections to port 5001")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)