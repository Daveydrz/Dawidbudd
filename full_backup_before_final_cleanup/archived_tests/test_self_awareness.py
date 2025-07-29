#!/usr/bin/env python3
"""
Test script for new self-awareness components
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_memory_context_corrector():
    """Test memory context corrector"""
    print("🧠 Testing Memory Context Corrector...")
    try:
        from ai.memory_context_corrector import correct_speech_with_context, learn_speech_correction
        
        # Test basic correction
        corrected, corrections = correct_speech_with_context("I have a problem with my niece", "test_user")
        print(f"   ✅ Corrected: '{corrected}' (corrections: {corrections})")
        
        # Test learning
        learn_speech_correction("phyton", "python", "test_user", 0.9)
        print(f"   ✅ Learning: taught 'phyton' → 'python'")
        
        # Test with learned correction
        corrected2, corrections2 = correct_speech_with_context("I love phyton programming", "test_user")
        print(f"   ✅ Applied learning: '{corrected2}' (corrections: {corrections2})")
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_belief_qualia_linking():
    """Test belief-qualia linking"""
    print("🌟 Testing Belief-Qualia Linking...")
    try:
        from ai.belief_qualia_linking import link_belief_to_qualia_experience, get_current_qualia_state
        
        # Test linking
        belief_id, qualia_ids = link_belief_to_qualia_experience("I feel excited about learning AI", "test_user")
        print(f"   ✅ Linked belief {belief_id} to qualia: {qualia_ids}")
        
        # Test state
        state = get_current_qualia_state()
        print(f"   ✅ Current qualia state: {state['active_qualia_count']} active")
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_internal_state_verbalizer():
    """Test internal state verbalizer"""
    print("🗣️ Testing Internal State Verbalizer...")
    try:
        from ai.internal_state_verbalizer import speak_qualia, verbalize_internal_state
        
        # Test qualia verbalization
        qualia_data = {
            'dominant_qualia': {'type': 'emotional', 'intensity': 'moderate'},
            'average_valence': 0.8,
            'average_clarity': 0.7
        }
        
        verbalization = speak_qualia(qualia_data)
        print(f"   ✅ Qualia verbalization: '{verbalization}'")
        
        # Test internal state
        cognitive_state = {'clarity': 0.8}
        emotional_state = {'primary_emotion': 'curiosity', 'confidence': 0.7}
        
        internal_comment = verbalize_internal_state(cognitive_state, emotional_state, "processing user question")
        print(f"   ✅ Internal state: '{internal_comment}'")
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_value_system():
    """Test value system"""
    print("⚖️ Testing Value System...")
    try:
        from ai.value_system import evaluate_value_based_decision, get_current_value_priorities
        
        # Test value priorities
        priorities = get_current_value_priorities()
        print(f"   ✅ Value priorities: {priorities[:3]}")
        
        # Test decision evaluation
        decision = evaluate_value_based_decision(
            "How should I respond to user request?",
            ["Give detailed answer", "Give brief answer", "Ask for clarification"]
        )
        print(f"   ✅ Decision: '{decision['recommended_option']}' (confidence: {decision['confidence']:.2f})")
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_conscious_prompt_builder():
    """Test conscious prompt builder"""
    print("🧠 Testing Conscious Prompt Builder...")
    try:
        from ai.conscious_prompt_builder import build_consciousness_integrated_prompt, get_consciousness_summary
        
        # Test prompt building
        prompt = build_consciousness_integrated_prompt(
            "Hello, how are you?", 
            "test_user", 
            "greeting conversation"
        )
        print(f"   ✅ Built prompt: {len(prompt)} characters")
        
        # Test summary
        summary = get_consciousness_summary("test_user")
        print(f"   ✅ Consciousness summary: {len(summary)} characters")
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_introspection_loop():
    """Test introspection loop"""
    print("🔄 Testing Introspection Loop...")
    try:
        from ai.introspection_loop import trigger_introspection, get_introspection_status
        from ai.introspection_loop import IntrospectionTrigger, IntrospectionDepth
        
        # Test introspection trigger
        trigger_introspection(IntrospectionTrigger.LEARNING_INTEGRATION, IntrospectionDepth.MODERATE)
        print(f"   ✅ Triggered introspection")
        
        # Test status
        status = get_introspection_status()
        print(f"   ✅ Status: {status['total_sessions']} sessions")
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_remaining_components():
    """Test remaining components"""
    print("🎯 Testing Remaining Components...")
    try:
        # Test emotion response modulator
        from ai.emotion_response_modulator import get_modulation_for_emotion
        modulation = get_modulation_for_emotion("excitement")
        print(f"   ✅ Emotion modulation: {modulation['tone']}")
        
        # Test dialogue confidence filter
        from ai.dialogue_confidence_filter import analyze_response_confidence
        confidence, _ = analyze_response_confidence("I think this might be correct", "What is 2+2?", "math question", "test_user")
        print(f"   ✅ Confidence analysis: {confidence:.2f}")
        
        # Test qualia analytics
        from ai.qualia_analytics import capture_current_qualia_state
        snapshot = capture_current_qualia_state("test_user", "testing")
        print(f"   ✅ Qualia snapshot: {snapshot['dominant_qualia']}")
        
        # Test belief memory refiner
        from ai.belief_memory_refiner import refine_belief_from_repetition
        from ai.belief_memory_refiner import BeliefSource
        belief_id = refine_belief_from_repetition("I enjoy programming", "test_user", "personal statement", BeliefSource.USER_STATEMENT)
        print(f"   ✅ Belief refined: {belief_id}")
        
        # Test self-model updater
        from ai.self_model_updater import get_current_personality_state
        personality = get_current_personality_state()
        print(f"   ✅ Personality state: {len(personality)} traits")
        
        # Test goal reasoning
        from ai.goal_reasoning import generate_goals_from_current_state
        goals = generate_goals_from_current_state(
            {"primary_emotion": "curiosity", "intensity": 0.8},
            [{"content": "I want to learn more", "confidence": 0.7}],
            [("learning", 0.9), ("curiosity", 0.8)],
            "learning context",
            "test_user"
        )
        print(f"   ✅ Generated goals: {len(goals)}")
        
        # Test motivation reasoner
        from ai.motivation_reasoner import get_decision_recommendations
        recommendations = get_decision_recommendations("How should I respond?")
        print(f"   ✅ Decision recommendations: {len(recommendations)}")
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing Self-Awareness Components")
    print("=" * 50)
    
    tests = [
        test_memory_context_corrector,
        test_belief_qualia_linking,
        test_internal_state_verbalizer,
        test_value_system,
        test_conscious_prompt_builder,
        test_introspection_loop,
        test_remaining_components
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"   ❌ Test failed: {e}")
            results.append(False)
    
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"🧪 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All self-awareness components working correctly!")
    else:
        print("⚠️ Some components need attention")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)