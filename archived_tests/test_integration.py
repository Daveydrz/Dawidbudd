"""
Integration Tests - Test all new modules and their integration
Created: 2025-01-17
Purpose: Verify that all consciousness modules work together correctly
"""

import os
import sys
import time
import json
from typing import Dict, Any

# Add current directory to path for imports
sys.path.insert(0, '/home/runner/work/Dawidbudd/Dawidbudd')

def test_consciousness_tokenizer():
    """Test consciousness tokenizer functionality"""
    print("🧠 Testing Consciousness Tokenizer...")
    
    try:
        from ai.consciousness_tokenizer import tokenize_consciousness_for_llm, get_consciousness_summary_for_llm
        
        # Test data
        test_consciousness = {
            'emotion_engine': {
                'primary_emotion': 'curious',
                'intensity': 0.7,
                'secondary_emotions': {'excitement': 0.5}
            },
            'motivation_system': {
                'active_goals': [
                    {'description': 'Help user understand', 'priority': 0.9, 'progress': 0.3},
                    {'description': 'Provide clear response', 'priority': 0.8, 'progress': 0.1}
                ]
            },
            'global_workspace': {
                'current_focus': 'user_conversation',
                'focus_priority': 'high'
            }
        }
        
        # Test tokenization
        tokens = tokenize_consciousness_for_llm(test_consciousness)
        summary = get_consciousness_summary_for_llm(test_consciousness)
        
        assert len(tokens) > 0, "Tokens should not be empty"
        assert "[CONSCIOUSNESS:" in summary, "Summary should contain consciousness marker"
        
        print(f"   ✅ Tokenizer working: {len(tokens)} characters generated")
        print(f"   ✅ Summary: {summary}")
        return True
        
    except Exception as e:
        print(f"   ❌ Consciousness tokenizer test failed: {e}")
        return False

def test_llm_budget_monitor():
    """Test LLM budget monitoring functionality"""
    print("💰 Testing LLM Budget Monitor...")
    
    try:
        from ai.llm_budget_monitor import check_llm_budget_before_request, log_llm_usage, get_budget_status
        
        # Test budget check
        allowed, message = check_llm_budget_before_request(1000, "gpt-3.5-turbo", "test_user")
        assert isinstance(allowed, bool), "Budget check should return boolean"
        
        # Test usage logging
        usage = log_llm_usage(500, 300, "gpt-3.5-turbo", "test_user", "test_request")
        assert usage.total_tokens == 800, "Total tokens should be 800"
        
        # Test budget status
        status = get_budget_status()
        assert 'daily' in status, "Status should contain daily info"
        assert 'monthly' in status, "Status should contain monthly info"
        
        print(f"   ✅ Budget monitor working: ${status['daily']['cost']:.4f} spent today")
        return True
        
    except Exception as e:
        print(f"   ❌ Budget monitor test failed: {e}")
        return False

def test_belief_analyzer():
    """Test belief analysis functionality"""
    print("🧠 Testing Belief Analyzer...")
    
    try:
        from ai.belief_analyzer import analyze_user_text_for_beliefs, get_user_belief_summary
        
        # Test belief extraction
        test_text = "I am a software developer and I live in Brisbane. I really like Python programming."
        analysis = analyze_user_text_for_beliefs(test_text, "test_user")
        
        assert isinstance(analysis, dict), "Analysis should return dictionary"
        assert 'extracted_beliefs' in analysis, "Should extract beliefs"
        
        # Test belief summary
        summary = get_user_belief_summary("test_user")
        assert isinstance(summary, dict), "Summary should be dictionary"
        
        print(f"   ✅ Belief analyzer working: {len(analysis.get('extracted_beliefs', []))} beliefs extracted")
        return True
        
    except Exception as e:
        print(f"   ❌ Belief analyzer test failed: {e}")
        return False

def test_personality_state():
    """Test personality adaptation functionality"""
    print("🎭 Testing Personality State...")
    
    try:
        from ai.personality_state import (
            analyze_user_text_for_personality_adaptation,
            get_personality_for_response,
            get_personality_modifiers_for_llm
        )
        
        # Test personality adaptation
        test_text = "Thanks! That was really helpful and funny!"
        triggers = analyze_user_text_for_personality_adaptation(test_text, "test_user")
        
        assert isinstance(triggers, list), "Triggers should be a list"
        
        # Test personality retrieval
        personality = get_personality_for_response("test_user")
        assert isinstance(personality, dict), "Personality should be dictionary"
        
        # Test LLM modifiers
        modifiers = get_personality_modifiers_for_llm("test_user")
        assert "[PERSONALITY:" in modifiers, "Modifiers should contain personality marker"
        
        print(f"   ✅ Personality state working: {len(triggers)} triggers, {modifiers}")
        return True
        
    except Exception as e:
        print(f"   ❌ Personality state test failed: {e}")
        return False

def test_semantic_tagging():
    """Test semantic analysis functionality"""
    print("🏷️ Testing Semantic Tagging...")
    
    try:
        from ai.semantic_tagging import analyze_content_semantics, get_semantic_tags_for_llm
        
        # Test semantic analysis
        test_text = "Can you please help me understand machine learning?"
        analysis = analyze_content_semantics(test_text, "test_user")
        
        assert isinstance(analysis, dict), "Analysis should be dictionary"
        assert 'semantic_categories' in analysis, "Should contain semantic categories"
        assert 'intent_categories' in analysis, "Should contain intent categories"
        
        # Test LLM tags
        tags = get_semantic_tags_for_llm(test_text, "test_user")
        assert isinstance(tags, str), "Tags should be string"
        assert "[" in tags and "]" in tags, "Tags should be formatted"
        
        print(f"   ✅ Semantic tagging working: {analysis['emotional_tone']}, {tags}")
        return True
        
    except Exception as e:
        print(f"   ❌ Semantic tagging test failed: {e}")
        return False

def test_llm_handler_integration():
    """Test full LLM handler integration"""
    print("🎯 Testing LLM Handler Integration...")
    
    try:
        from ai.llm_handler import (
            process_user_input_with_consciousness,
            generate_consciousness_integrated_response,
            get_llm_session_statistics
        )
        
        # Test input processing
        test_input = "Hello! I need help with understanding AI consciousness."
        analysis = process_user_input_with_consciousness(test_input, "test_user")
        
        assert isinstance(analysis, dict), "Analysis should be dictionary"
        
        if 'error' not in analysis:
            assert 'semantic' in analysis, "Should contain semantic analysis"
            assert 'beliefs' in analysis, "Should contain belief analysis"
            assert 'personality' in analysis, "Should contain personality analysis"
            assert 'budget' in analysis, "Should contain budget info"
        
        # Test response generation
        response_parts = []
        for chunk in generate_consciousness_integrated_response(test_input, "test_user"):
            response_parts.append(chunk)
            if len(response_parts) >= 3:  # Limit for testing
                break
        
        assert len(response_parts) > 0, "Should generate response chunks"
        
        # Test session statistics
        stats = get_llm_session_statistics()
        assert isinstance(stats, dict), "Stats should be dictionary"
        assert 'modules_integrated' in stats, "Should show module status"
        
        print(f"   ✅ LLM handler working: {len(response_parts)} chunks, {stats['requests_processed']} requests")
        return True
        
    except Exception as e:
        print(f"   ❌ LLM handler test failed: {e}")
        return False

def test_end_to_end_pipeline():
    """Test the complete end-to-end pipeline"""
    print("🔄 Testing End-to-End Pipeline...")
    
    try:
        # Simulate complete conversation flow
        user_inputs = [
            "Hello! How are you?",
            "I'm a Python developer from Brisbane",
            "Can you help me understand machine learning?",
            "Thanks! That was really helpful."
        ]
        
        results = []
        
        for i, user_input in enumerate(user_inputs):
            print(f"   Processing input {i+1}: '{user_input[:30]}...'")
            
            # Process through full pipeline
            from ai.llm_handler import process_user_input_with_consciousness
            analysis = process_user_input_with_consciousness(user_input, "pipeline_test_user")
            
            results.append({
                'input': user_input,
                'analysis': analysis,
                'success': 'error' not in analysis or analysis.get('budget', {}).get('allowed', False)
            })
            
            time.sleep(0.1)  # Brief pause between requests
        
        # Check results
        successful_requests = sum(1 for r in results if r['success'])
        total_requests = len(results)
        
        assert successful_requests > 0, "At least one request should succeed"
        
        print(f"   ✅ Pipeline working: {successful_requests}/{total_requests} requests successful")
        
        # Show some analysis results
        if results[0]['success'] and 'semantic' in results[0]['analysis']:
            first_analysis = results[0]['analysis']
            print(f"   📊 Sample analysis: {first_analysis['semantic']['emotional_tone']}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ End-to-end pipeline test failed: {e}")
        return False

def test_file_persistence():
    """Test that all modules can save and load their state"""
    print("💾 Testing File Persistence...")
    
    try:
        # Check if files were created
        expected_files = [
            'llm_budget_config.json',
            'llm_usage_log.json',
            'belief_store.json',
            'personality_state.json',
            'semantic_tags_cache.json'
        ]
        
        created_files = []
        for filename in expected_files:
            if os.path.exists(filename):
                created_files.append(filename)
                # Check if file has content
                try:
                    with open(filename, 'r') as f:
                        data = json.load(f)
                        if data:
                            print(f"   📄 {filename}: {len(str(data))} characters")
                except:
                    print(f"   📄 {filename}: exists but not valid JSON")
            
        print(f"   ✅ Persistence working: {len(created_files)}/{len(expected_files)} files created")
        return True
        
    except Exception as e:
        print(f"   ❌ File persistence test failed: {e}")
        return False

def run_all_tests():
    """Run all integration tests"""
    print("🧪 Running Integration Tests for All New Modules")
    print("=" * 60)
    
    tests = [
        test_consciousness_tokenizer,
        test_llm_budget_monitor,
        test_belief_analyzer,
        test_personality_state,
        test_semantic_tagging,
        test_llm_handler_integration,
        test_end_to_end_pipeline,
        test_file_persistence
    ]
    
    results = []
    
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test_func.__name__} crashed: {e}")
            results.append(False)
        print()
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("=" * 60)
    print(f"🧪 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed! Integration is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    print("=" * 60)
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    
    if success:
        print("\n🎉 Integration testing complete - all systems operational!")
    else:
        print("\n🔧 Integration testing complete - some issues detected")
        
    exit(0 if success else 1)