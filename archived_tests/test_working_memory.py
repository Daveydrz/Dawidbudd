#!/usr/bin/env python3
"""
Test script for the new Working Memory Tracking system
"""

import sys
sys.path.append('.')

from ai.memory import UserMemorySystem

def test_working_memory_features():
    """Test the new working memory tracking features"""
    print("🧪 Testing Working Memory Tracking System\n")
    
    # Create a test user memory system
    memory = UserMemorySystem('test_user')
    
    # Test 1: Working Memory Tracking
    print("1. Testing Working Memory Tracking:")
    memory.extract_memories_from_text("I'm going to the shop to buy groceries")
    print(f"   Action: {memory.working_memory.last_action}")
    print(f"   Place: {memory.working_memory.last_place}")
    print(f"   Topic: {memory.working_memory.last_topic}")
    print(f"   Status: {memory.working_memory.action_status}\n")
    
    # Test 2: Reference Resolution
    print("2. Testing Reference Resolution:")
    resolution = memory.detect_and_resolve_references("I just came back")
    if resolution:
        print(f"   Resolved: '{resolution.vague_phrase}' → '{resolution.likely_referent}'")
        print(f"   Confidence: {resolution.confidence}")
    else:
        print("   No resolution found")
    print()
    
    # Test 3: Intent Slot Memory
    print("3. Testing Intent Slot Memory:")
    memory.extract_memories_from_text("Let me first check what I need")
    memory.extract_memories_from_text("Alright, I'm ready to go")
    active_intents = [intent for intent in memory.intent_slots.values() 
                     if intent.status in ["preparing", "ready"]]
    if active_intents:
        intent = active_intents[0]
        print(f"   Intent: {intent.intent}")
        print(f"   Status: {intent.status}")
        print(f"   Prep Steps: {intent.prep_steps}")
    else:
        print("   No active intents found")
    print()
    
    # Test 4: Natural Language Context for LLM
    print("4. Testing Natural Language Context for LLM:")
    context = memory.get_natural_language_context_for_llm("It went well")
    print(f"   Context: {context}")
    print()
    
    # Test 5: Full Working Memory Context
    print("5. Testing Full Working Memory Context:")
    working_context = memory.get_working_memory_context_for_llm()
    print(f"   Working Memory Context: {working_context}")
    print()
    
    print("✅ Working Memory Tests Complete!")

if __name__ == "__main__":
    test_working_memory_features()