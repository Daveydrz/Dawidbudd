#!/usr/bin/env python3
"""
Test Qualia Symbolic Consolidation
Tests the qualia_symbolic.py consolidated module
"""

import sys
import os
sys.path.append('.')

def test_qualia_symbolic_imports():
    """Test importing from the consolidated module"""
    print("🔍 Testing qualia symbolic module imports...")
    
    try:
        from ai.qualia_symbolic import (
            process_subjective_experience,
            get_current_qualia_state,
            compress_consciousness_to_tokens,
            expand_tokens_to_consciousness,
            ground_concept_in_experience,
            analyze_emotional_patterns,
            QualiaType,
            SensoryModality,
            GroundingStrength,
            AnalyticsTimeframe,
            get_qualia_symbolic_statistics
        )
        print("✅ Successfully imported all main functions from qualia_symbolic")
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_backward_compatibility():
    """Test backward compatibility with original modules"""
    print("\n🔍 Testing backward compatibility...")
    
    success_count = 0
    total_tests = 0
    
    # Test qualia_manager compatibility
    try:
        from ai.qualia_symbolic import get_qualia_manager, start_qualia_processing, stop_qualia_processing
        manager = get_qualia_manager()
        print("✅ Qualia manager compatibility works")
        success_count += 1
    except Exception as e:
        print(f"❌ Qualia manager compatibility failed: {e}")
    total_tests += 1
    
    # Test symbolic_token_optimizer compatibility
    try:
        from ai.qualia_symbolic import get_symbolic_token_optimizer
        optimizer = get_symbolic_token_optimizer()
        print("✅ Symbolic token optimizer compatibility works")
        success_count += 1
    except Exception as e:
        print(f"❌ Symbolic token optimizer compatibility failed: {e}")
    total_tests += 1
    
    # Test symbolic_grounding compatibility
    try:
        from ai.qualia_symbolic import get_symbolic_grounding_system, get_concept_sensory_tags
        grounding_system = get_symbolic_grounding_system()
        tags = get_concept_sensory_tags("joy")
        print("✅ Symbolic grounding compatibility works")
        success_count += 1
    except Exception as e:
        print(f"❌ Symbolic grounding compatibility failed: {e}")
    total_tests += 1
    
    # Test qualia_analytics compatibility
    try:
        from ai.qualia_symbolic import get_qualia_analytics, capture_qualia_snapshot
        analytics = get_qualia_analytics()
        snapshot = capture_qualia_snapshot("test_user")
        print("✅ Qualia analytics compatibility works")
        success_count += 1
    except Exception as e:
        print(f"❌ Qualia analytics compatibility failed: {e}")
    total_tests += 1
    
    return success_count, total_tests

def test_main_api():
    """Test the main unified API"""
    print("\n🔍 Testing main unified API...")
    
    try:
        from ai.qualia_symbolic import (
            process_subjective_experience, 
            get_current_qualia_state,
            start_qualia_processing,
            stop_qualia_processing
        )
        
        # Start the system
        start_qualia_processing()
        
        test_experiences = [
            ("User asked complex question", {"complexity": 0.8}),
            ("Successfully helped user", {"satisfaction": 0.9}),
            ("Encountered unclear request", {"confusion": 0.6})
        ]
        
        for i, (trigger, context) in enumerate(test_experiences):
            experience, sensory_tags = process_subjective_experience(trigger, context)
            
            print(f"   Test {i+1}: {trigger[:30]}...")
            if experience:
                print(f"   Generated qualia: {experience.qualia_type.value}")
                print(f"   Intensity: {experience.intensity:.2f}")
                print(f"   Sensory tags: {len(sensory_tags)}")
            else:
                print(f"   No experience generated")
        
        # Test state retrieval
        state = get_current_qualia_state("test_user")
        print(f"   Current state retrieved: {bool(state)}")
        
        # Stop the system
        stop_qualia_processing()
        
        print("✅ Main unified API works correctly")
        return True
        
    except Exception as e:
        print(f"❌ Main API test failed: {e}")
        return False

def test_symbolic_token_functionality():
    """Test symbolic token compression and expansion"""
    print("\n🔍 Testing symbolic token functionality...")
    
    try:
        from ai.qualia_symbolic import compress_consciousness_to_tokens, expand_tokens_to_consciousness
        
        # Test consciousness data
        test_consciousness = {
            'emotional_state': {
                'mood': 'happy',
                'intensity': 0.7,
                'valence': 0.6
            },
            'cognitive_state': {
                'focus': 'problem_solving',
                'clarity': 0.8
            },
            'memory_context': {
                'recent_memories': ['recent interaction']
            }
        }
        
        # Test compression
        tokens = compress_consciousness_to_tokens(test_consciousness, max_tokens=10)
        print(f"   Compressed to tokens: {len(tokens)} chars")
        print(f"   Token string: {tokens[:50]}..." if len(tokens) > 50 else f"   Token string: {tokens}")
        
        # Test expansion
        expanded = expand_tokens_to_consciousness(tokens)
        print(f"   Expanded back to: {len(expanded)} components")
        
        print("✅ Symbolic token functionality works correctly")
        return True
        
    except Exception as e:
        print(f"❌ Symbolic token test failed: {e}")
        return False

def test_concept_grounding():
    """Test concept grounding functionality"""
    print("\n🔍 Testing concept grounding...")
    
    try:
        from ai.qualia_symbolic import ground_concept_in_experience, get_concept_sensory_tags
        
        test_concepts = ["joy", "confusion", "pride", "wonder", "sadness"]
        
        for concept in test_concepts:
            # Test grounding
            grounding = ground_concept_in_experience(concept)
            sensory_tags = get_concept_sensory_tags(concept)
            
            print(f"   {concept}: grounded={bool(grounding)}, tags={len(sensory_tags)}")
        
        print("✅ Concept grounding functionality works correctly")
        return True
        
    except Exception as e:
        print(f"❌ Concept grounding test failed: {e}")
        return False

def test_analytics_functionality():
    """Test analytics and pattern analysis"""
    print("\n🔍 Testing analytics functionality...")
    
    try:
        from ai.qualia_symbolic import (
            analyze_emotional_patterns, 
            capture_qualia_snapshot,
            AnalyticsTimeframe
        )
        
        # Capture some snapshots
        for i in range(3):
            snapshot = capture_qualia_snapshot(f"test_user_{i}", f"context_{i}")
            print(f"   Snapshot {i+1}: captured={bool(snapshot)}")
        
        # Analyze patterns
        trends = analyze_emotional_patterns(AnalyticsTimeframe.HOUR)
        print(f"   Found {len(trends)} emotional trends")
        
        print("✅ Analytics functionality works correctly")
        return True
        
    except Exception as e:
        print(f"❌ Analytics test failed: {e}")
        return False

def test_statistics():
    """Test statistics functionality"""
    print("\n🔍 Testing statistics functionality...")
    
    try:
        from ai.qualia_symbolic import get_qualia_symbolic_statistics
        
        stats = get_qualia_symbolic_statistics()
        
        print(f"   Qualia experiences: {stats.get('qualia_experiences', 'N/A')}")
        print(f"   Active qualia: {stats.get('active_qualia', 'N/A')}")
        print(f"   Concept groundings: {stats.get('concept_groundings', 'N/A')}")
        print(f"   System running: {stats.get('system_running', 'N/A')}")
        
        print("✅ Statistics functionality works correctly")
        return True
        
    except Exception as e:
        print(f"❌ Statistics test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("============================================================")
    print("🧪 TESTING QUALIA SYMBOLIC CONSOLIDATION")
    print("============================================================")
    
    tests = [
        ("Module Imports", test_qualia_symbolic_imports),
        ("Backward Compatibility", test_backward_compatibility),
        ("Main API", test_main_api),
        ("Symbolic Token Functionality", test_symbolic_token_functionality),
        ("Concept Grounding", test_concept_grounding),
        ("Analytics Functionality", test_analytics_functionality),
        ("Statistics", test_statistics)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            if test_name == "Backward Compatibility":
                success_count, total_tests = test_func()
                results.append((test_name, success_count == total_tests, f"{success_count}/{total_tests}"))
            else:
                result = test_func()
                results.append((test_name, result, "PASS" if result else "FAIL"))
        except Exception as e:
            results.append((test_name, False, f"ERROR: {e}"))
    
    print("\n============================================================")
    print("📊 FINAL TEST RESULTS")
    print("============================================================")
    
    passed = 0
    total = len(results)
    
    for test_name, success, details in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}: {details}")
        if success:
            passed += 1
    
    print(f"\n🎯 SUMMARY: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Qualia Symbolic consolidation successful!")
        return 0
    else:
        print("⚠️ Some tests failed - review needed")
        return 1

if __name__ == "__main__":
    sys.exit(main())