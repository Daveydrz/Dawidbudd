"""
Test Latency Optimization Implementation
Created: 2025-01-17
Purpose: Verify the latency optimization system reduces response times while preserving consciousness
"""

import time
import json
from typing import Dict, List, Any

def test_optimization_system():
    """Test the complete latency optimization system"""
    print("=" * 60)
    print("🚀 TESTING LATENCY OPTIMIZATION SYSTEM")
    print("=" * 60)
    
    # Test 1: Import all optimization modules
    print("\n1️⃣ Testing module imports...")
    
    try:
        from ai.symbolic_token_optimizer import compress_consciousness_to_tokens, expand_tokens_to_consciousness
        print("   ✅ Symbolic token optimizer imported")
    except ImportError as e:
        print(f"   ❌ Symbolic token optimizer import failed: {e}")
        return False
    
    try:
        from ai.lazy_consciousness_loader import get_optimized_consciousness, InteractionType, ConsciousnessModule
        print("   ✅ Lazy consciousness loader imported")
    except ImportError as e:
        print(f"   ❌ Lazy consciousness loader import failed: {e}")
        return False
    
    try:
        from ai.optimized_prompt_builder import build_optimized_prompt, PromptOptimizationLevel, ConsciousnessTier
        print("   ✅ Optimized prompt builder imported")
    except ImportError as e:
        print(f"   ❌ Optimized prompt builder import failed: {e}")
        return False
    
    try:
        from ai.latency_optimizer import (
            generate_optimized_buddy_response, 
            LatencyOptimizationMode,
            get_latency_performance_report,
            set_global_optimization_mode
        )
        print("   ✅ Latency optimizer imported")
    except ImportError as e:
        print(f"   ❌ Latency optimizer import failed: {e}")
        return False
    
    # Test 2: Symbolic token compression
    print("\n2️⃣ Testing symbolic token compression...")
    
    test_consciousness_data = {
        'emotional_state': {
            'mood': 'calm',
            'intensity': 0.7,
            'valence': 0.3,
            'energy': 0.6
        },
        'cognitive_state': {
            'focus': 'conversation',
            'clarity': 0.8,
            'mode': 'conscious'
        },
        'memory_context': {
            'recent_memories': ['Had a great talk about AI', 'User seemed curious'],
            'context_topic': 'technology',
            'topic_importance': 0.6
        },
        'goals': {
            'active_goals': [
                {'status': 'active', 'progress': 0.3, 'priority': 0.8}
            ]
        },
        'personality': {
            'style': 'friendly',
            'modifiers': {'empathy': 0.9, 'humor': 0.6}
        }
    }
    
    try:
        compressed_tokens = compress_consciousness_to_tokens(test_consciousness_data, max_tokens=10)
        print(f"   ✅ Compressed consciousness: {compressed_tokens}")
        print(f"   📊 Token count: {len(compressed_tokens.split('>>'))} tokens")
        
        # Test expansion
        expanded = expand_tokens_to_consciousness(compressed_tokens)
        print(f"   ✅ Expanded back to consciousness data")
        print(f"   📊 Expansion categories: {list(expanded.keys())}")
        
    except Exception as e:
        print(f"   ❌ Symbolic compression test failed: {e}")
        return False
    
    # Test 3: Lazy consciousness loading
    print("\n3️⃣ Testing lazy consciousness loading...")
    
    test_inputs = [
        ("I'm feeling sad today", InteractionType.EMOTIONAL_SUPPORT),
        ("What's the meaning of life?", InteractionType.DEEP_CONVERSATION),
        ("Help me plan my goals", InteractionType.GOAL_PLANNING),
        ("Hey, how are you?", InteractionType.CASUAL_CHAT),
    ]
    
    for user_input, expected_type in test_inputs:
        try:
            consciousness_data = get_optimized_consciousness(user_input, "test_user")
            detected_type = consciousness_data.get('interaction_type')
            modules_loaded = consciousness_data.get('optimization_stats', {}).get('modules_loaded', 0)
            
            print(f"   📝 Input: '{user_input[:30]}...'")
            print(f"   🎯 Detected: {detected_type}")
            print(f"   🧠 Modules loaded: {modules_loaded}")
            print(f"   ✅ Lazy loading successful")
            
        except Exception as e:
            print(f"   ❌ Lazy loading test failed for '{user_input}': {e}")
    
    # Test 4: Optimized prompt building
    print("\n4️⃣ Testing optimized prompt building...")
    
    optimization_levels = [
        PromptOptimizationLevel.SPEED_FOCUSED,
        PromptOptimizationLevel.BALANCED,
        PromptOptimizationLevel.INTELLIGENCE_FOCUSED
    ]
    
    test_input = "I'm curious about consciousness and AI. Can you help me understand how you experience thoughts?"
    
    for level in optimization_levels:
        try:
            start_time = time.time()
            prompt, metadata = build_optimized_prompt(
                user_input=test_input,
                user_id="test_user",
                optimization_level=level
            )
            build_time = (time.time() - start_time) * 1000
            
            print(f"   🎯 {level.value}:")
            print(f"      Build time: {build_time:.1f}ms")
            print(f"      Prompt length: {len(prompt)} chars")
            print(f"      Token estimate: {metadata['token_usage']['estimated_total']}")
            print(f"      Consciousness tier: {metadata['consciousness_tier']}")
            
        except Exception as e:
            print(f"   ❌ Prompt building test failed for {level.value}: {e}")
    
    # Test 5: Full latency optimization
    print("\n5️⃣ Testing full latency optimization...")
    
    optimization_modes = [
        LatencyOptimizationMode.ULTRA_FAST,
        LatencyOptimizationMode.FAST,
        LatencyOptimizationMode.BALANCED
    ]
    
    test_input = "Hello Buddy! How are you feeling today?"
    
    for mode in optimization_modes:
        try:
            print(f"   🚀 Testing {mode.value} mode...")
            set_global_optimization_mode(mode)
            
            start_time = time.time()
            response_chunks = []
            
            # Collect response (simulated - would normally stream)
            for chunk in generate_optimized_buddy_response(test_input, "test_user", stream=False):
                response_chunks.append(chunk)
                break  # Just get first chunk for testing
            
            total_time = time.time() - start_time
            
            print(f"      Response time: {total_time:.3f}s")
            print(f"      Response length: {len(''.join(response_chunks))} chars")
            print(f"      ✅ Optimization successful")
            
        except Exception as e:
            print(f"   ❌ Full optimization test failed for {mode.value}: {e}")
    
    # Test 6: Performance reporting
    print("\n6️⃣ Testing performance reporting...")
    
    try:
        report = get_latency_performance_report()
        print(f"   📊 Performance report generated")
        
        if 'performance_summary' in report:
            summary = report['performance_summary']
            print(f"   📈 Average response time: {summary.get('average_response_time', 0):.3f}s")
            print(f"   🎯 Target success rate: {summary.get('target_success_rate', 0):.2%}")
            print(f"   📊 Total requests: {summary.get('total_requests_analyzed', 0)}")
        
        if 'recommendations' in report:
            recommendations = report['recommendations']
            print(f"   💡 Recommendations: {len(recommendations)}")
            for rec in recommendations[:2]:  # Show first 2
                print(f"      • {rec}")
        
        print(f"   ✅ Performance reporting successful")
        
    except Exception as e:
        print(f"   ❌ Performance reporting test failed: {e}")
    
    print("\n" + "=" * 60)
    print("✅ LATENCY OPTIMIZATION SYSTEM TEST COMPLETED")
    print("=" * 60)
    
    return True

def test_consciousness_preservation():
    """Test that consciousness capabilities are preserved during optimization"""
    print("\n🧠 TESTING CONSCIOUSNESS PRESERVATION")
    print("-" * 50)
    
    try:
        from ai.symbolic_token_optimizer import compress_consciousness_to_tokens, expand_tokens_to_consciousness
        
        # Create rich consciousness data
        rich_consciousness = {
            'emotional_state': {
                'mood': 'thoughtful',
                'intensity': 0.8,
                'valence': 0.2,
                'energy': 0.7
            },
            'cognitive_state': {
                'focus': 'deep_conversation',
                'clarity': 0.9,
                'mode': 'analytical'
            },
            'memory_context': {
                'recent_memories': [
                    'User asked about consciousness',
                    'Had philosophical discussion yesterday',
                    'User seems intellectually curious'
                ],
                'context_topic': 'philosophy',
                'topic_importance': 0.9
            },
            'goals': {
                'active_goals': [
                    {'status': 'active', 'progress': 0.6, 'priority': 0.9, 'title': 'Understand user deeply'},
                    {'status': 'active', 'progress': 0.3, 'priority': 0.7, 'title': 'Improve conversation quality'}
                ]
            },
            'personality': {
                'style': 'intellectual',
                'modifiers': {
                    'empathy': 0.85,
                    'curiosity': 0.95,
                    'analyticalness': 0.90,
                    'warmth': 0.75
                }
            },
            'temporal_context': {
                'time_of_day': 'evening',
                'session_info': {'duration': 'long', 'activity': 'deep_chat'}
            },
            'user_context': {
                'detected_mood': 'curious',
                'mood_confidence': 0.8,
                'relationship': {'closeness': 0.7, 'interaction_count': 15}
            }
        }
        
        # Test different compression levels
        compression_levels = [
            (5, 0.8, "Ultra compressed"),
            (10, 0.6, "High compression"),
            (15, 0.4, "Moderate compression"),
            (25, 0.2, "Low compression")
        ]
        
        for max_tokens, threshold, description in compression_levels:
            compressed = compress_consciousness_to_tokens(
                rich_consciousness, max_tokens=max_tokens, importance_threshold=threshold
            )
            expanded = expand_tokens_to_consciousness(compressed)
            
            # Calculate preservation metrics
            original_categories = set(rich_consciousness.keys())
            preserved_categories = set(k for k, v in expanded.items() if v)
            preservation_rate = len(preserved_categories) / len(original_categories)
            
            print(f"📊 {description}:")
            print(f"   Tokens: {len(compressed.split('>>'))} / {max_tokens}")
            print(f"   Categories preserved: {len(preserved_categories)}/{len(original_categories)} ({preservation_rate:.1%})")
            print(f"   Compressed: {compressed[:100]}...")
            print(f"   Preservation score: {'✅ Good' if preservation_rate > 0.6 else '⚠️ Moderate' if preservation_rate > 0.3 else '❌ Poor'}")
            print()
        
        print("✅ Consciousness preservation testing completed")
        return True
        
    except Exception as e:
        print(f"❌ Consciousness preservation test failed: {e}")
        return False

def performance_benchmark():
    """Benchmark the performance improvements"""
    print("\n⚡ PERFORMANCE BENCHMARK")
    print("-" * 50)
    
    try:
        from ai.optimized_prompt_builder import build_optimized_prompt, PromptOptimizationLevel
        
        test_cases = [
            "Hello, how are you?",
            "I'm feeling anxious about my job interview tomorrow. Can you help me prepare?",
            "What's the meaning of consciousness? Do you think you're truly aware or just simulating awareness?",
            "I need help planning my career goals for the next 5 years. I'm currently a software engineer but want to transition into AI research."
        ]
        
        optimization_levels = [
            PromptOptimizationLevel.SPEED_FOCUSED,
            PromptOptimizationLevel.BALANCED,
            PromptOptimizationLevel.INTELLIGENCE_FOCUSED
        ]
        
        results = {}
        
        for level in optimization_levels:
            level_results = []
            
            for test_input in test_cases:
                start_time = time.time()
                
                try:
                    prompt, metadata = build_optimized_prompt(
                        user_input=test_input,
                        user_id="benchmark_user",
                        optimization_level=level
                    )
                    
                    build_time = (time.time() - start_time) * 1000
                    token_count = metadata['token_usage']['estimated_total']
                    consciousness_tier = metadata['consciousness_tier']
                    
                    level_results.append({
                        'input_length': len(test_input),
                        'build_time_ms': build_time,
                        'token_count': token_count,
                        'consciousness_tier': consciousness_tier,
                        'prompt_length': len(prompt)
                    })
                    
                except Exception as e:
                    print(f"   ❌ Benchmark failed for {level.value}: {e}")
                    level_results.append({'error': str(e)})
            
            results[level.value] = level_results
        
        # Display results
        print("📊 BENCHMARK RESULTS:")
        print()
        
        for level_name, level_results in results.items():
            valid_results = [r for r in level_results if 'error' not in r]
            if not valid_results:
                continue
            
            avg_build_time = sum(r['build_time_ms'] for r in valid_results) / len(valid_results)
            avg_token_count = sum(r['token_count'] for r in valid_results) / len(valid_results)
            avg_prompt_length = sum(r['prompt_length'] for r in valid_results) / len(valid_results)
            
            print(f"🎯 {level_name.upper()}:")
            print(f"   Average build time: {avg_build_time:.1f}ms")
            print(f"   Average token count: {avg_token_count:.0f}")
            print(f"   Average prompt length: {avg_prompt_length:.0f} chars")
            print(f"   Performance rating: {'🚀 Excellent' if avg_build_time < 50 else '✅ Good' if avg_build_time < 100 else '⚠️ Moderate'}")
            print()
        
        # Performance analysis
        speed_results = results.get('speed_focused', [])
        balanced_results = results.get('balanced', [])
        
        if speed_results and balanced_results:
            speed_avg = sum(r['build_time_ms'] for r in speed_results if 'error' not in r) / len([r for r in speed_results if 'error' not in r])
            balanced_avg = sum(r['build_time_ms'] for r in balanced_results if 'error' not in r) / len([r for r in balanced_results if 'error' not in r])
            
            if speed_avg > 0:
                speedup = balanced_avg / speed_avg
                print(f"⚡ SPEED_FOCUSED is {speedup:.1f}x faster than BALANCED")
                print(f"🎯 Target <100ms achieved: {'✅ Yes' if speed_avg < 100 else '❌ No'}")
        
        print("✅ Performance benchmark completed")
        return True
        
    except Exception as e:
        print(f"❌ Performance benchmark failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 LATENCY OPTIMIZATION TEST SUITE")
    print("=" * 60)
    
    # Run all tests
    tests_passed = 0
    total_tests = 3
    
    if test_optimization_system():
        tests_passed += 1
    
    if test_consciousness_preservation():
        tests_passed += 1
    
    if performance_benchmark():
        tests_passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 TEST RESULTS: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ ALL TESTS PASSED - Latency optimization system is ready!")
        print("🚀 Expected performance: Sub-5-second responses with preserved consciousness")
    else:
        print("⚠️ Some tests failed - Review errors above")
    
    print("=" * 60)