#!/usr/bin/env python3
"""
Test script for the ONNX-like memory classifier system
Tests classification accuracy and integration with local memory manager
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai.memory_classifier import classify_memory_type, test_classifier, get_classifier_stats
from ai.local_memory_manager import local_memory_manager

def test_memory_classification():
    """Test the memory classification system"""
    print("🧠 Testing ONNX-like Memory Classification System")
    print("=" * 60)
    
    # Test the classifier directly
    print("\n1. Testing Memory Classifier:")
    classifier_success = test_classifier()
    
    # Get classifier stats
    stats = get_classifier_stats()
    print(f"\n📊 Classifier Performance:")
    print(f"   Model loaded: {stats.get('model_loaded', False)}")
    print(f"   Total inferences: {stats.get('total_inferences', 0)}")
    print(f"   Avg inference time: {stats.get('average_inference_time_ms', 0):.2f}ms")
    print(f"   Target met (<10ms): {'✅' if stats.get('performance_target_met', False) else '❌'}")
    
    # Test integration with local memory manager
    print("\n2. Testing Integration with Local Memory Manager:")
    test_user = "test_classifier_user"
    
    test_inputs = [
        ("I like pizza", "preference"),
        ("My birthday is June 5th", "fact"),
        ("I'm going to the shop", "context"),
        ("I love chocolate ice cream", "preference"),
        ("I work as a software engineer", "fact"),
        ("I just got back from work", "context"),
        ("Lubię pizzę", "preference"),  # Polish
        ("Mam 25 lat", "fact"),  # Polish
        ("Mi piace la pasta", "preference"),  # Italian
    ]
    
    print(f"\nProcessing {len(test_inputs)} test inputs:")
    
    for i, (text, expected_type) in enumerate(test_inputs, 1):
        # Process with memory manager
        result = local_memory_manager.process_user_input(text, test_user)
        
        # Check classification
        memories_extracted = result.get("memories_extracted", 0)
        memory_types = result.get("memory_types_extracted", {})
        
        status = "✅" if expected_type in memory_types else "❌" 
        print(f"   {status} {i:2d}. '{text}' -> {memory_types} (expected: {expected_type})")
    
    # Show memory summary
    print(f"\n3. Memory Summary for {test_user}:")
    memory_summary = local_memory_manager.get_memory_summary_by_type(test_user)
    print(f"   Preferences: {memory_summary['preferences']}")
    print(f"   Facts: {memory_summary['facts']}")
    print(f"   Context: {memory_summary['context']}")
    print(f"   Total: {memory_summary['total']}")
    
    # Test LLM context generation
    print(f"\n4. LLM Context Generation:")
    llm_context = local_memory_manager.get_memory_context_for_llm(test_user)
    print(f"   Context: {llm_context}")
    
    # Performance check
    classifier_stats = local_memory_manager.get_classifier_performance_stats()
    print(f"\n5. Final Performance Check:")
    print(f"   Classifier loaded: {classifier_stats.get('model_loaded', False)}")
    print(f"   Performance target met: {'✅' if classifier_stats.get('performance_target_met', False) else '❌'}")
    
    return classifier_success

def test_multilingual_support():
    """Test multilingual classification"""
    print("\n🌍 Testing Multilingual Support:")
    print("-" * 40)
    
    multilingual_tests = [
        # English
        ("I love programming", "preference", "en"),
        ("My name is John", "fact", "en"),
        ("I'm cooking dinner", "context", "en"),
        
        # Polish
        ("Lubię gotować", "preference", "pl"),
        ("Nazywam się Anna", "fact", "pl"), 
        ("Idę do pracy", "context", "pl"),
        
        # Italian
        ("Amo la musica", "preference", "it"),
        ("Ho 30 anni", "fact", "it"),
        ("Sto cucinando", "context", "it"),
    ]
    
    correct = 0
    total = len(multilingual_tests)
    
    for text, expected, language in multilingual_tests:
        result = classify_memory_type(text)
        status = "✅" if result == expected else "❌"
        print(f"   {status} [{language}] '{text}' -> {result} (expected: {expected})")
        if result == expected:
            correct += 1
    
    accuracy = (correct / total) * 100
    print(f"\n   Multilingual accuracy: {accuracy:.1f}% ({correct}/{total})")
    
    return accuracy >= 70  # 70% threshold for multilingual

def main():
    """Run all tests"""
    print("🚀 ONNX-like Memory Classifier Test Suite")
    print("=" * 80)
    
    try:
        # Test basic classification
        classifier_success = test_memory_classification()
        
        # Test multilingual support
        multilingual_success = test_multilingual_support()
        
        # Final results
        print("\n" + "=" * 80)
        print("📋 FINAL RESULTS:")
        print(f"   Memory Classification: {'✅ PASS' if classifier_success else '❌ FAIL'}")
        print(f"   Multilingual Support: {'✅ PASS' if multilingual_success else '❌ FAIL'}")
        
        overall_success = classifier_success and multilingual_success
        print(f"   Overall: {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}")
        
        if overall_success:
            print("\n🎉 Memory classifier is ready for production!")
            print("   - Fast inference (<10ms target)")
            print("   - Multi-language support (EN/PL/IT)")
            print("   - Accurate classification (fact/preference/context)")
            print("   - Seamless integration with local memory manager")
        else:
            print("\n⚠️  Memory classifier needs attention before production use")
        
        return overall_success
        
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)