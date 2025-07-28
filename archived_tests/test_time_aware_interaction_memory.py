#!/usr/bin/env python3
"""
Test Time-Aware Greetings and Interaction Thread Memory System
"""

import sys
sys.path.append('.')

import datetime
from ai.memory import UserMemorySystem

def test_time_aware_greetings():
    """Test time-based greeting functionality"""
    print("🕐 Testing Time-Aware Greetings...")
    
    memory = UserMemorySystem('test_user')
    
    # Test different times of day
    greeting = memory.get_time_based_greeting("Dawid")
    print(f"✅ Current time greeting: {greeting}")
    
    # Should include time-appropriate greeting and follow-up
    assert any(phrase in greeting.lower() for phrase in ["good morning", "good afternoon", "good evening", "hello"])
    assert any(phrase in greeting.lower() for phrase in ["did you sleep", "how's your day", "how was your day", "everything okay"])
    
    print("✅ Time-aware greetings working correctly")

def test_interaction_thread_memory():
    """Test interaction thread tracking and resolution"""
    print("📋 Testing Interaction Thread Memory...")
    
    memory = UserMemorySystem('test_user')
    
    # Simulate user asking for internet search
    search_request = "Can you find me information about bike repair?"
    thread_id = memory.add_interaction_thread(search_request, "internet_search", "bike repair information")
    
    print(f"✅ Added search thread #{thread_id}")
    
    # Simulate user later asking about the search
    later_query = "Did you find what I was looking for?"
    reference = memory.resolve_thread_reference(later_query)
    
    print(f"✅ Reference resolution: {reference}")
    assert reference is not None
    assert "bike repair" in reference.lower()
    
    # Complete the thread
    memory.complete_interaction_thread(thread_id, "Here's information about bike repair...")
    
    print("✅ Interaction thread memory working correctly")

def test_episodic_turn_memory():
    """Test episodic conversation turn tracking"""
    print("🧠 Testing Episodic Turn Memory...")
    
    memory = UserMemorySystem('test_user')
    
    # Add conversation turns
    turn1 = memory.add_episodic_turn(
        "I'm going to my niece's birthday party today",
        "That sounds wonderful! I hope you have a great time.",
        "general",
        ["niece", "birthday party"],
        "positive"
    )
    
    turn2 = memory.add_episodic_turn(
        "What are my plans for the weekend?", 
        "You mentioned earlier you're going to your niece's birthday party today.",
        "question",
        [],
        "neutral"
    )
    
    print(f"✅ Added turns #{turn1} and #{turn2}")
    
    # Verify episodic memory
    assert len(memory.episodic_memory) >= 2
    assert "niece" in memory.episodic_memory[0].entities_mentioned
    
    print("✅ Episodic turn memory working correctly")

def test_conversation_context_injection():
    """Test natural language context for LLM"""
    print("💬 Testing Conversation Context Injection...")
    
    memory = UserMemorySystem('test_user')
    
    # Add some conversation history
    memory.add_interaction_thread("Can you help me find a good restaurant?", "task_request", "restaurant recommendation")
    memory.add_episodic_turn("Can you help me find a good restaurant?", "I'd be happy to help you find a restaurant!", "task_request", ["restaurant"], "helpful")
    
    # Test context generation
    context = memory.get_conversation_context_for_llm("Did you find anything good?")
    
    print(f"✅ Generated context: {context}")
    
    # Should include time, user, and reference resolution
    assert "Current time:" in context
    assert "User: test_user" in context
    assert "restaurant" in context.lower()
    
    print("✅ Conversation context injection working correctly")

def main():
    """Run all tests"""
    print("🧪 Testing Time-Aware and Interaction Memory Features...")
    print("=" * 60)
    
    try:
        test_time_aware_greetings()
        print()
        
        test_interaction_thread_memory()
        print()
        
        test_episodic_turn_memory()
        print()
        
        test_conversation_context_injection()
        print()
        
        print("🎉 All tests passed! Time-aware and interaction memory features working correctly.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)