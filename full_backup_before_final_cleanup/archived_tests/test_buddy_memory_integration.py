"""
Simple integration test to verify memory classifier works with Buddy system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai.memory_classifier import classify_memory_type
from ai.local_memory_manager import local_memory_manager

def test_buddy_integration():
    """Test that the memory classifier integrates correctly with Buddy"""
    print("🤖 Testing Memory Classifier Integration with Buddy")
    print("=" * 60)
    
    # Simulate user interactions that Buddy would process
    test_user = "buddy_integration_test"
    
    interactions = [
        # Mixed conversation
        ("Hi, how are you today?", "context"),
        ("I like pizza", "preference"),
        ("My name is David", "fact"),
        ("I'm going to the shop", "context"),
        ("I hate rain", "preference"),
        ("I work as a programmer", "fact"),
        ("I just got back home", "context"),
        ("My birthday is March 15", "fact"),
        ("I love chocolate", "preference"),
        ("What time is it?", "context"),
    ]
    
    correct_classifications = 0
    total_interactions = len(interactions)
    
    print(f"\n📝 Processing {total_interactions} user interactions:")
    
    for i, (text, expected) in enumerate(interactions, 1):
        # Process the interaction 
        result = local_memory_manager.process_user_input(text, test_user)
        
        # Check what was classified
        memory_types = result.get("memory_types_extracted", {})
        
        # Determine if classification was correct
        classified_correctly = expected in memory_types
        status = "✅" if classified_correctly else "❌"
        
        if classified_correctly:
            correct_classifications += 1
        
        print(f"   {status} {i:2d}. '{text}' -> {list(memory_types.keys())} (expected: {expected})")
    
    # Calculate accuracy
    accuracy = (correct_classifications / total_interactions) * 100
    print(f"\n📊 Classification Accuracy: {accuracy:.1f}% ({correct_classifications}/{total_interactions})")
    
    # Show memory breakdown
    memory_summary = local_memory_manager.get_memory_summary_by_type(test_user)
    print(f"\n📋 Final Memory Summary:")
    print(f"   Facts: {memory_summary['facts']}")
    print(f"   Preferences: {memory_summary['preferences']}")
    print(f"   Context: {memory_summary['context']}")
    print(f"   Total: {memory_summary['total']}")
    
    # Show what Buddy would use for context
    llm_context = local_memory_manager.get_memory_context_for_llm(test_user)
    print(f"\n💭 Context for Buddy's LLM:")
    print(f"   {llm_context}")
    
    # Performance check
    classifier_stats = local_memory_manager.get_classifier_performance_stats()
    print(f"\n⚡ Performance Metrics:")
    print(f"   Model loaded: {classifier_stats.get('model_loaded', False)}")
    print(f"   Avg inference time: {classifier_stats.get('average_inference_time_ms', 0):.2f}ms")
    print(f"   Performance target met: {'✅' if classifier_stats.get('performance_target_met', False) else '❌'}")
    
    # Test direct API usage
    print(f"\n🧠 Direct API Test:")
    api_tests = [
        "I like coffee",
        "My age is 30", 
        "I'm at work"
    ]
    
    for text in api_tests:
        classification = classify_memory_type(text)
        print(f"   classify_memory_type('{text}') -> '{classification}'")
    
    success = accuracy >= 80 and classifier_stats.get('model_loaded', False)
    
    print(f"\n{'✅ SUCCESS' if success else '❌ FAILED'}: Memory classifier is {'ready' if success else 'not ready'} for Buddy integration")
    
    return success

if __name__ == "__main__":
    success = test_buddy_integration()
    print(f"\n🎯 Integration test {'PASSED' if success else 'FAILED'}")
    exit(0 if success else 1)