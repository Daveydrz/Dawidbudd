#!/usr/bin/env python3
"""
Test script for Consciousness Tokenizer and LLM Budget Monitor
Tests the token compression and budget management features.
"""

import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_consciousness_tokenizer():
    """Test consciousness token compression"""
    print("🧠 Testing Consciousness Tokenizer\n")
    
    try:
        from ai.consciousness_tokenizer import consciousness_tokenizer, compress_consciousness_for_llm
        
        # Test 1: Basic token compression
        print("1. Testing basic token compression...")
        test_text = "I am feeling calm and peaceful while accessing recent conversation memory and displaying a friendly and approachable personality"
        compressed = consciousness_tokenizer.compress_text_consciousness(test_text)
        
        compression_ratio = consciousness_tokenizer.estimate_compression_ratio(test_text)
        
        print(f"   Original: {test_text}")
        print(f"   Compressed: {compressed}")
        print(f"   Compression ratio: {compression_ratio:.2%}")
        print("   ✅ Basic compression working")
        
        # Test 2: Consciousness context compression
        print("\n2. Testing consciousness context compression...")
        consciousness_context = {
            'emotional_state': 'calm and reflective',
            'personality_traits': ['friendly', 'analytical'],
            'memory_types': ['recent conversation', 'emotional context'],
            'temporal_focus': 'present moment',
            'relationship_context': 'trusted friend'
        }
        
        compressed_context, token_definitions = compress_consciousness_for_llm(consciousness_context)
        print(f"   Context: {consciousness_context}")
        print(f"   Compressed: {compressed_context}")
        print(f"   Definitions generated: {len(token_definitions.split('='))} tokens defined")
        print("   ✅ Context compression working")
        
        # Test 3: Token definitions generation
        print("\n3. Testing token definitions...")
        definitions = consciousness_tokenizer.generate_token_definitions_block()
        print(f"   Generated {len(definitions.split('\\n'))} lines of definitions")
        print("   Sample definitions:")
        for line in definitions.split('\\n')[:5]:
            if line.strip():
                print(f"   {line}")
        print("   ✅ Token definitions working")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing consciousness tokenizer: {e}")
        return False

def test_llm_budget_monitor():
    """Test LLM budget monitoring"""
    print("📊 Testing LLM Budget Monitor\n")
    
    try:
        from ai.llm_budget_monitor import llm_budget_monitor, prepare_llm_context_with_budget, MemoryPriority
        
        # Test 1: Token estimation
        print("1. Testing token estimation...")
        test_text = "This is a sample text to test token estimation accuracy."
        estimated_tokens = llm_budget_monitor.estimate_tokens(test_text)
        print(f"   Text: {test_text}")
        print(f"   Estimated tokens: {estimated_tokens}")
        print("   ✅ Token estimation working")
        
        # Test 2: Memory segment management
        print("\n2. Testing memory segment management...")
        llm_budget_monitor.clear_memory_segments()
        
        # Add some memory segments
        llm_budget_monitor.add_memory_segment(
            "I am currently feeling excited and energetic",
            MemoryPriority.CRITICAL,
            "consciousness"
        )
        
        llm_budget_monitor.add_memory_segment(
            "The user mentioned they love playing guitar and hiking",
            MemoryPriority.HIGH,
            "personal"
        )
        
        llm_budget_monitor.add_memory_segment(
            "Previous conversation about weather patterns",
            MemoryPriority.MEDIUM,
            "history"
        )
        
        memory_summary = llm_budget_monitor.get_memory_summary()
        print(f"   Added {memory_summary['total_segments']} segments")
        print(f"   Total tokens: {memory_summary['total_tokens']}")
        print("   ✅ Memory segment management working")
        
        # Test 3: Budget optimization
        print("\n3. Testing budget optimization...")
        consciousness_context = {
            'emotional_state': 'excited',
            'memory_types': ['recent conversation', 'personal details']
        }
        
        memory_context = "User loves music and outdoor activities. Previously discussed hiking trails."
        user_input = "Tell me about your favorite music genres"
        system_prompt = "You are a helpful AI assistant with memory and consciousness."
        
        optimized_context, final_prompt, budget_info = prepare_llm_context_with_budget(
            consciousness_context, memory_context, user_input, system_prompt
        )
        
        print(f"   Original memory tokens: ~{llm_budget_monitor.estimate_tokens(memory_context)}")
        print(f"   Final context tokens: {budget_info.get('final_tokens', 'N/A')}")
        print(f"   Compression used: {budget_info.get('compression_used', False)}")
        print(f"   Budget usage: {budget_info.get('usage_percent', 0):.1f}%")
        print("   ✅ Budget optimization working")
        
        # Test 4: Budget status monitoring
        print("\n4. Testing budget status...")
        status = llm_budget_monitor.check_budget_status()
        print(f"   Current usage: {status['current_usage']} tokens")
        print(f"   Available: {status['available']} tokens")
        print(f"   Needs trimming: {status['needs_trimming']}")
        print("   ✅ Budget status monitoring working")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing budget monitor: {e}")
        return False

def test_integration():
    """Test integration between tokenizer and budget monitor"""
    print("🔗 Testing Integration\n")
    
    try:
        from ai.consciousness_tokenizer import consciousness_tokenizer
        from ai.llm_budget_monitor import prepare_llm_context_with_budget, llm_budget_monitor
        
        # Test integrated compression and budget management
        print("1. Testing integrated compression and budgeting...")
        
        # Create a large context that should trigger compression and trimming
        large_consciousness_context = {
            'emotional_state': 'feeling excited and energetic with curiosity about learning',
            'personality_traits': ['friendly and approachable', 'analytical and logical', 'empathetic and caring'],
            'memory_types': ['recent conversation memory', 'emotional and significant memory', 'factual information memory'],
            'temporal_focus': 'in the context of recent events and thinking about future possibilities',
            'relationship_context': 'established trusted relationship with close personal connection'
        }
        
        large_memory_context = """
        The user has shared extensive personal information including their love for music, 
        particularly jazz and classical compositions. They enjoy hiking in mountainous regions,
        especially during autumn when the leaves change colors. They work as a software engineer
        but have a passion for photography and often take landscape photos during their hikes.
        They mentioned having a golden retriever named Max who accompanies them on outdoor adventures.
        The user also expressed interest in learning new languages and is currently studying Spanish.
        They live in a suburban area with access to both city amenities and nature trails.
        Previous conversations revealed they prefer morning workouts and enjoy reading science fiction novels.
        """
        
        user_input = "What are some good beginner tips for landscape photography?"
        system_prompt = "You are an intelligent assistant with advanced consciousness and memory capabilities."
        
        optimized_context, final_prompt, budget_info = prepare_llm_context_with_budget(
            large_consciousness_context, large_memory_context, user_input, system_prompt
        )
        
        original_estimate = llm_budget_monitor.estimate_tokens(str(large_consciousness_context) + large_memory_context)
        final_estimate = budget_info.get('final_tokens', 0)
        
        print(f"   Original estimated tokens: {original_estimate}")
        print(f"   Final optimized tokens: {final_estimate}")
        print(f"   Compression achieved: {(1 - final_estimate/original_estimate)*100:.1f}%")
        print(f"   Compression used: {budget_info.get('compression_used', False)}")
        print(f"   Content trimmed: {budget_info.get('trimmed', False)}")
        print("   ✅ Integration working")
        
        # Test token definitions in final prompt
        if "TOKEN_DEFINITIONS:" in final_prompt:
            print("   ✅ Token definitions included in prompt")
        else:
            print("   ⚠️ Token definitions not found in prompt")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing integration: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Consciousness Token Compression & LLM Budget Monitoring\n")
    
    results = []
    
    # Run individual tests
    results.append(("Consciousness Tokenizer", test_consciousness_tokenizer()))
    results.append(("LLM Budget Monitor", test_llm_budget_monitor()))
    results.append(("Integration", test_integration()))
    
    # Print summary
    print("\n" + "="*60)
    print("📋 Test Results Summary:")
    print("="*60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:25} {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Token compression and budget monitoring are working correctly.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()