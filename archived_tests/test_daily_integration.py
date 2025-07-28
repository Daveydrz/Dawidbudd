#!/usr/bin/env python3
"""
Daily Integration Test - Run this to verify all systems working
"""

import sys
import os
sys.path.insert(0, os.getcwd())

def test_all_systems():
    """Test all integrated systems"""
    print("🧪 Running Daily Integration Test...")
    
    tests = []
    
    # Test 1: Import all components
    try:
        from ai.consciousness_tokenizer import tokenize_consciousness_for_llm
        from ai.llm_handler import generate_consciousness_integrated_response
        from ai.memory_context_corrector import MemoryContextCorrector
        from ai.belief_qualia_linking import BeliefQualiaLinker
        from ai.value_system import ValueSystem
        from ai.conscious_prompt_builder import ConsciousPromptBuilder
        from ai.introspection_loop import IntrospectionLoop
        print("   ✅ All component imports successful")
        tests.append(("Component Imports", True))
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        tests.append(("Component Imports", False))
    
    # Test 2: LLM Connection
    try:
        import requests
        from config import KOBOLD_URL
        response = requests.get(KOBOLD_URL.replace('/v1/chat/completions', '/v1/models'), timeout=5)
        if response.status_code == 200:
            print("   ✅ LLM connection successful")
            tests.append(("LLM Connection", True))
        else:
            print(f"   ❌ LLM connection failed: {response.status_code}")
            tests.append(("LLM Connection", False))
    except Exception as e:
        print(f"   ❌ LLM connection error: {e}")
        tests.append(("LLM Connection", False))
    
    # Test 3: Tokenization
    try:
        from ai.consciousness_tokenizer import tokenize_consciousness_for_llm
        test_state = {'emotion_engine': {'primary_emotion': 'testing'}}
        result = tokenize_consciousness_for_llm(test_state)
        if result:
            print(f"   ✅ Tokenization working: {len(result)} chars")
            tests.append(("Tokenization", True))
        else:
            print("   ❌ Tokenization failed")
            tests.append(("Tokenization", False))
    except Exception as e:
        print(f"   ❌ Tokenization error: {e}")
        tests.append(("Tokenization", False))
    
    # Test 4: End-to-end
    try:
        from ai.llm_handler import process_user_input_with_consciousness
        result = process_user_input_with_consciousness("Hello", "test_user")
        if result:
            print("   ✅ End-to-end processing working")
            tests.append(("End-to-End", True))
        else:
            print("   ❌ End-to-end processing failed")
            tests.append(("End-to-End", False))
    except Exception as e:
        print(f"   ❌ End-to-end error: {e}")
        tests.append(("End-to-End", False))
    
    # Results
    passed = sum(1 for _, success in tests if success)
    total = len(tests)
    
    print(f"\n📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All systems integrated and working!")
        return True
    else:
        print("⚠️ Some systems need attention")
        return False

if __name__ == "__main__":
    success = test_all_systems()
    sys.exit(0 if success else 1)
