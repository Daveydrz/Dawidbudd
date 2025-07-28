#!/usr/bin/env python3
"""
Test Optimized Buddy System - Verify single LLM call mode and local memory
Created: 2025-01-17
Purpose: Test the new performance-optimized Buddy system
"""

import time
import json
from config import *
from ai.local_memory_manager import local_memory_manager
from ai.single_llm_call_system import single_llm_system, get_performance_stats
from ai.background_consciousness_processor_optimized import background_consciousness_processor, schedule_consciousness_processing

def test_optimized_buddy():
    """Test the optimized Buddy system"""
    print("=" * 60)
    print("🧠 BUDDY OPTIMIZED SYSTEM TEST")
    print("=" * 60)
    
    # Display configuration
    print(f"\n⚙️ CONFIGURATION:")
    print(f"  🧠 Inner Thoughts: {'ENABLED' if ENABLE_INNER_THOUGHTS else 'DISABLED'}")
    print(f"  🔄 Self Reflection: {'ENABLED' if ENABLE_SELF_REFLECTION else 'DISABLED'}")
    print(f"  ⚡ Single LLM Call Mode: {'ENABLED' if SINGLE_LLM_CALL_MODE else 'DISABLED'}")
    print(f"  💾 Local Memory Updates: {'ENABLED' if LOCAL_MEMORY_UPDATES else 'DISABLED'}")
    print(f"  🎯 Target Response Time: {TARGET_RESPONSE_TIME_SECONDS}s")
    print(f"  📊 Max LLM Calls Per Turn: {MAX_LLM_CALLS_PER_TURN}")
    
    # Start background processor
    print(f"\n🚀 Starting background consciousness processor...")
    background_consciousness_processor.start()
    
    # Test cases
    test_cases = [
        "How are you?",
        "I'm going to the shop",
        "I like pizza",
        "What time is it?",
        "I'm back from the shop"
    ]
    
    test_user = "TestUser"
    
    print(f"\n📝 TESTING WITH USER: {test_user}")
    print("=" * 60)
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n🧪 TEST {i}: '{test_input}'")
        print("-" * 40)
        
        # Test local memory processing
        start_time = time.time()
        memory_result = local_memory_manager.process_user_input(test_input, test_user)
        memory_time = time.time() - start_time
        
        print(f"💾 Memory Processing: {memory_time:.3f}s")
        print(f"📊 Memories Extracted: {memory_result['memories_extracted']}")
        
        if memory_result['last_action']:
            print(f"🎬 Last Action: {memory_result['last_action']}")
        
        # Schedule consciousness processing in background
        schedule_consciousness_processing(test_input, test_user, {"test": True})
        
        # Test consciousness context generation (no LLM call)
        consciousness_context = single_llm_system._get_consciousness_context(test_user)
        print(f"🧠 Consciousness Context: {consciousness_context[:100]}...")
        
        # Simulate response generation (don't actually call LLM in test)
        print(f"⚡ Would make 1 LLM call for response generation")
        
        time.sleep(0.5)  # Brief pause between tests
    
    # Display final statistics
    print(f"\n📊 FINAL STATISTICS:")
    print("=" * 60)
    
    # Memory statistics
    recent_memories = local_memory_manager.get_recent_memories(test_user, 10)
    print(f"💾 MEMORY STATISTICS:")
    print(f"  Actions: {len(recent_memories['actions'])}")
    print(f"  Preferences: {len(recent_memories['preferences'])}")
    print(f"  Facts: {len(recent_memories['facts'])}")
    print(f"  Context: {len(recent_memories['context'])}")
    
    # Background processor statistics
    bg_stats = background_consciousness_processor.get_stats()
    print(f"\n🧠 CONSCIOUSNESS STATISTICS:")
    print(f"  Tasks Processed: {bg_stats['tasks_processed']}")
    print(f"  Inner Thoughts Generated: {bg_stats['inner_thoughts_generated']}")
    print(f"  Queue Size: {bg_stats['queue_size']}")
    print(f"  Background Processing: {'RUNNING' if bg_stats['is_running'] else 'STOPPED'}")
    
    # Performance statistics
    perf_stats = get_performance_stats()
    print(f"\n⚡ PERFORMANCE STATISTICS:")
    print(f"  LLM Calls Made: {perf_stats['llm_calls_made']}")
    print(f"  Average Response Time: {perf_stats['average_response_time']:.2f}s")
    print(f"  Target Response Time: {perf_stats['target_response_time']}s")
    print(f"  Performance Target Met: {'YES' if perf_stats['performance_target_met'] else 'NO'}")
    print(f"  Single LLM Call Mode: {'ENABLED' if perf_stats['single_llm_call_mode'] else 'DISABLED'}")
    
    # Configuration recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    if not SINGLE_LLM_CALL_MODE:
        print("  ⚠️ Consider enabling Single LLM Call Mode for faster responses")
    if ENABLE_INNER_THOUGHTS:
        print("  💭 Inner thoughts are enabled - may increase processing time")
    if not LOCAL_MEMORY_UPDATES:
        print("  ⚠️ Consider enabling Local Memory Updates for faster memory processing")
    
    print(f"\n✅ OPTIMIZATION STATUS:")
    if SINGLE_LLM_CALL_MODE and LOCAL_MEMORY_UPDATES:
        print("  🚀 FULLY OPTIMIZED - Maximum performance configuration")
    elif SINGLE_LLM_CALL_MODE or LOCAL_MEMORY_UPDATES:
        print("  ⚡ PARTIALLY OPTIMIZED - Some optimizations enabled")
    else:
        print("  🐌 NOT OPTIMIZED - Consider enabling optimizations for better performance")
    
    # Stop background processor
    background_consciousness_processor.stop()
    
    print(f"\n🎉 TEST COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    test_optimized_buddy()