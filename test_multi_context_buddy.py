#!/usr/bin/env python3
"""
Test Multi-Context Conversation Handling for Buddy AI
Tests the exact user scenario: "I'm going for my niece's birthday and then also to gp for my annual check"
"""

import sys
import os
sys.path.append('.')

from ai.memory import UserMemorySystem, get_user_memory
from ai.context_window_manager import ContextWindowManager
from ai.consciousness_tokenizer import ConsciousnessTokenizer

def test_multi_context_parsing():
    """Test parsing compound statements with multiple events"""
    print("🧪 TEST 1: Multi-Context Parsing")
    print("=" * 50)
    
    # Create memory system
    memory = UserMemorySystem("test_multicontext_user")
    
    # Test the exact user scenario
    user_input = "I'm going for my niece's birthday and then also to gp for my annual check"
    print(f"📝 User input: {user_input}")
    
    # Extract memories (this should trigger multi-context parsing)
    memory.extract_memories_from_text(user_input)
    
    # Check active contexts
    active_contexts = memory.working_memory.active_contexts
    print(f"🧠 Active contexts detected: {len(active_contexts)}")
    
    for context_id, context in active_contexts.items():
        print(f"  🎯 Context {context_id}:")
        print(f"    Description: {context.description}")
        print(f"    Event Type: {context.event_type}")
        print(f"    Place: {context.place}")
        print(f"    Status: {context.status}")
        print(f"    Priority: {context.priority}")
        print(f"    Time Reference: {context.time_reference}")
    
    # Test multi-context summary
    summary = memory.get_multi_context_summary()
    print(f"\n📋 Multi-context summary: {summary}")
    
    return len(active_contexts) >= 2  # Should detect both events

def test_reference_resolution():
    """Test reference resolution with multiple contexts"""
    print("\n🧪 TEST 2: Multi-Context Reference Resolution")
    print("=" * 50)
    
    memory = get_user_memory("test_multicontext_user")
    
    # Test various reference resolutions
    test_cases = [
        ("Both went well", "multiple_completion"),
        ("I finished", "completion"),
        ("The first one was fun", "sequence_reference"),
        ("I'm back", "return"),
        ("I'm ready for the next one", "ready")
    ]
    
    success_count = 0
    for test_input, expected_type in test_cases:
        print(f"\n📝 Testing: '{test_input}'")
        
        resolution = memory.detect_and_resolve_references(test_input)
        if resolution:
            print(f"  ✅ Resolved to: '{resolution.likely_referent}'")
            print(f"  🎯 Confidence: {resolution.confidence:.2f}")
            print(f"  📍 Source: {resolution.context_source}")
            success_count += 1
        else:
            print(f"  ❌ No resolution found")
    
    return success_count >= 3  # Should resolve at least 3 references

def test_context_window_preservation():
    """Test that multi-context survives 8k context window rollovers"""
    print("\n🧪 TEST 3: Context Window Preservation")
    print("=" * 50)
    
    context_manager = ContextWindowManager()
    memory = get_user_memory("test_multicontext_user")
    
    # Simulate conversation history
    conversation_history = [
        {"user": "I'm going for my niece's birthday and then also to gp for my annual check"},
        {"assistant": "That sounds like a busy day! How old is your niece turning?"},
        {"user": "She's turning 7. I need to pick up a gift before the party."},
        {"assistant": "What kind of gift are you thinking of getting for her?"}
    ]
    
    # Create context snapshot
    working_memory = {
        "active_contexts": {
            ctx_id: {
                "context_id": ctx_id,
                "description": ctx.description,
                "event_type": ctx.event_type,
                "place": ctx.place,
                "status": ctx.status,
                "priority": ctx.priority,
                "time_reference": ctx.time_reference,
                "completion_status": ctx.completion_status,
                "related_contexts": ctx.related_contexts
            } for ctx_id, ctx in memory.working_memory.active_contexts.items()
        },
        "last_action": memory.working_memory.last_action,
        "last_place": memory.working_memory.last_place,
        "context_sequence": memory.working_memory.context_sequence
    }
    
    # Test snapshot creation
    snapshot = context_manager.create_context_snapshot(
        user_id="test_multicontext_user",
        current_context="Test conversation context",
        conversation_history=conversation_history,
        working_memory=working_memory
    )
    
    if snapshot:
        print(f"✅ Snapshot created successfully")
        print(f"📝 Summary: {snapshot.conversation_summary[:100]}...")
        
        # Test fresh context building
        fresh_context = context_manager.build_fresh_context(
            user_id="test_multicontext_user",
            new_input="How did everything go?"
        )
        
        print(f"🔄 Fresh context includes multi-context: {'Active contexts:' in fresh_context}")
        print(f"📏 Fresh context length: {len(fresh_context)} chars")
        
        return True
    else:
        print("❌ Snapshot creation failed")
        return False

def test_tokenizer_optimization():
    """Test tokenizer optimization for multi-context"""
    print("\n🧪 TEST 4: Tokenizer Optimization")
    print("=" * 50)
    
    tokenizer = ConsciousnessTokenizer()
    memory = get_user_memory("test_multicontext_user")
    
    # Test multi-context tokenization
    tokens = tokenizer.tokenize_multi_context_memory(memory)
    print(f"🏷️ Multi-context tokens: {tokens}")
    
    # Estimate token efficiency
    if tokens:
        token_count = len(tokens.split())
        char_count = len(tokens)
        efficiency = token_count / char_count if char_count > 0 else 0
        
        print(f"📊 Token efficiency: {token_count} tokens in {char_count} chars")
        print(f"📈 Efficiency ratio: {efficiency:.4f}")
        
        return efficiency > 0.01  # Should be reasonably efficient
    else:
        print("❌ No tokens generated")
        return False

def test_cross_user_isolation():
    """Test that contexts are isolated between users"""
    print("\n🧪 TEST 5: Cross-User Memory Isolation")
    print("=" * 50)
    
    # Create two users
    user1_memory = UserMemorySystem("user1")
    user2_memory = UserMemorySystem("user2")
    
    # User 1 adds contexts
    user1_memory.extract_memories_from_text("I'm going to the doctor and then shopping")
    user1_contexts = len(user1_memory.working_memory.active_contexts)
    
    # User 2 adds different contexts
    user2_memory.extract_memories_from_text("I'm cooking dinner and then watching a movie")
    user2_contexts = len(user2_memory.working_memory.active_contexts)
    
    print(f"👤 User 1 contexts: {user1_contexts}")
    print(f"👤 User 2 contexts: {user2_contexts}")
    
    # Verify isolation
    isolation_success = (
        user1_contexts > 0 and 
        user2_contexts > 0 and
        user1_memory.working_memory.active_contexts != user2_memory.working_memory.active_contexts
    )
    
    print(f"🔒 Memory isolation: {'✅ Success' if isolation_success else '❌ Failed'}")
    
    return isolation_success

def run_comprehensive_test():
    """Run all multi-context tests"""
    print("🚀 COMPREHENSIVE MULTI-CONTEXT BUDDY TEST")
    print("=" * 70)
    
    tests = [
        ("Multi-Context Parsing", test_multi_context_parsing),
        ("Reference Resolution", test_reference_resolution),
        ("Context Window Preservation", test_context_window_preservation),
        ("Tokenizer Optimization", test_tokenizer_optimization),
        ("Cross-User Isolation", test_cross_user_isolation)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            print(f"\n{'✅' if result else '❌'} {test_name}: {'PASSED' if result else 'FAILED'}")
        except Exception as e:
            print(f"\n💥 {test_name}: ERROR - {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status:12} {test_name}")
    
    print(f"\n🏆 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Multi-context system is working perfectly!")
    else:
        print("⚠️ Some tests failed. Multi-context system needs fixes.")
    
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)