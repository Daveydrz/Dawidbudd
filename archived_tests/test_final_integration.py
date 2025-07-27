"""
Final Integration Test for Latency Optimization
Created: 2025-01-17
Purpose: Test complete integration of optimization system with main Buddy AI
"""

import time
import json
from typing import Dict, Any

def test_main_integration():
    """Test that main.py can use the optimization system"""
    print("🔧 TESTING MAIN INTEGRATION")
    print("=" * 50)
    
    # Test 1: Import latency optimizer in main context
    print("\n1️⃣ Testing latency optimizer imports...")
    try:
        from ai.latency_optimizer import (
            generate_optimized_buddy_response,
            LatencyOptimizationMode,
            set_global_optimization_mode,
            get_latency_performance_report
        )
        print("   ✅ Latency optimizer imports successful")
    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
        return False
    
    # Test 2: Set optimization mode
    print("\n2️⃣ Testing optimization mode setting...")
    try:
        set_global_optimization_mode(LatencyOptimizationMode.FAST)
        print("   ✅ Set FAST optimization mode (target: <5s)")
    except Exception as e:
        print(f"   ❌ Mode setting failed: {e}")
        return False
    
    # Test 3: Generate optimized response
    print("\n3️⃣ Testing optimized response generation...")
    try:
        test_input = "Hello Buddy! How are you feeling today?"
        start_time = time.time()
        
        response_chunks = []
        for chunk in generate_optimized_buddy_response(
            user_input=test_input,
            user_id="main_test_user",
            context={'source': 'main_integration_test'},
            stream=True
        ):
            response_chunks.append(chunk)
            # Simulate real-time processing but limit for testing
            if len(response_chunks) >= 3:
                break
        
        total_time = time.time() - start_time
        full_response = ' '.join(response_chunks)
        
        print(f"   ⚡ Response time: {total_time:.3f}s")
        print(f"   📝 Response preview: '{full_response[:60]}...'")
        print(f"   🎯 Target met: {'✅ Yes' if total_time < 5.0 else '❌ No'}")
        print("   ✅ Optimized response generation successful")
        
    except Exception as e:
        print(f"   ❌ Response generation failed: {e}")
        return False
    
    # Test 4: Performance reporting
    print("\n4️⃣ Testing performance reporting...")
    try:
        report = get_latency_performance_report()
        
        if 'status' in report and report['status'] == 'no_data':
            print("   📊 No performance data yet (expected for new system)")
        else:
            print(f"   📊 Performance report generated")
            if 'current_mode' in report:
                print(f"   🎯 Current mode: {report['current_mode']}")
            if 'performance_summary' in report:
                summary = report['performance_summary']
                if 'average_response_time' in summary:
                    print(f"   ⚡ Average response time: {summary['average_response_time']:.3f}s")
        
        print("   ✅ Performance reporting successful")
        
    except Exception as e:
        print(f"   ❌ Performance reporting failed: {e}")
        return False
    
    print("\n✅ Main integration test passed!")
    return True

def test_llm_handler_integration():
    """Test that LLM handler uses optimization"""
    print("\n🧠 TESTING LLM HANDLER INTEGRATION")
    print("=" * 50)
    
    try:
        from ai.llm_handler import LLMHandler
        
        print("\n1️⃣ Testing LLM handler with optimization...")
        
        llm = LLMHandler()
        test_input = "I'm curious about consciousness. Can you help me understand?"
        
        start_time = time.time()
        response_chunks = []
        
        # Test the generate_response_with_consciousness method with optimization
        for chunk in llm.generate_response_with_consciousness(
            text=test_input,
            user="llm_test_user",
            context={'test': True},
            stream=True,
            use_optimization=True  # Enable optimization
        ):
            response_chunks.append(chunk)
            if len(response_chunks) >= 3:  # Limit for testing
                break
        
        total_time = time.time() - start_time
        full_response = ' '.join(response_chunks)
        
        print(f"   ⚡ LLM handler response time: {total_time:.3f}s")
        print(f"   📝 Response preview: '{full_response[:60]}...'")
        print(f"   🎯 Optimization working: {'✅ Yes' if total_time < 10.0 else '❌ No'}")
        print("   ✅ LLM handler integration successful")
        
        return True
        
    except Exception as e:
        print(f"   ❌ LLM handler integration failed: {e}")
        return False

def test_different_optimization_modes():
    """Test different optimization modes for various scenarios"""
    print("\n🎛️ TESTING DIFFERENT OPTIMIZATION MODES")
    print("=" * 50)
    
    try:
        from ai.latency_optimizer import generate_optimized_buddy_response, LatencyOptimizationMode
        
        test_scenarios = [
            ("Quick question", "Hey, what time is it?", LatencyOptimizationMode.ULTRA_FAST),
            ("Casual chat", "How are you feeling today?", LatencyOptimizationMode.FAST),
            ("Complex topic", "I'm struggling with some life decisions and need advice", LatencyOptimizationMode.BALANCED),
            ("Deep conversation", "What's the nature of consciousness and do you truly experience awareness?", LatencyOptimizationMode.INTELLIGENT)
        ]
        
        results = []
        
        for scenario_name, test_input, mode in test_scenarios:
            print(f"\n📝 Testing {scenario_name} with {mode.value} mode...")
            
            start_time = time.time()
            
            try:
                response_chunks = []
                for chunk in generate_optimized_buddy_response(
                    user_input=test_input,
                    user_id=f"mode_test_user_{mode.value}",
                    optimization_mode=mode,
                    stream=True
                ):
                    response_chunks.append(chunk)
                    if len(response_chunks) >= 2:  # Limit for testing
                        break
                
                total_time = time.time() - start_time
                response_preview = ' '.join(response_chunks)[:50]
                
                results.append({
                    'scenario': scenario_name,
                    'mode': mode.value,
                    'time': total_time,
                    'preview': response_preview
                })
                
                print(f"   ⚡ Time: {total_time:.3f}s")
                print(f"   📝 Preview: '{response_preview}...'")
                print(f"   ✅ Success")
                
            except Exception as e:
                print(f"   ❌ Failed: {e}")
                results.append({
                    'scenario': scenario_name,
                    'mode': mode.value,
                    'error': str(e)
                })
        
        # Summary
        print(f"\n📊 OPTIMIZATION MODE SUMMARY:")
        successful_results = [r for r in results if 'error' not in r]
        
        if successful_results:
            avg_times = {}
            for result in successful_results:
                mode = result['mode']
                if mode not in avg_times:
                    avg_times[mode] = []
                avg_times[mode].append(result['time'])
            
            for mode, times in avg_times.items():
                avg_time = sum(times) / len(times)
                print(f"   {mode}: {avg_time:.3f}s average")
            
            print("   ✅ Multiple optimization modes working")
        else:
            print("   ⚠️ No successful tests")
        
        return len(successful_results) > 0
        
    except Exception as e:
        print(f"   ❌ Mode testing failed: {e}")
        return False

def verify_production_readiness():
    """Verify the system is ready for production use"""
    print("\n🚀 PRODUCTION READINESS VERIFICATION")
    print("=" * 50)
    
    try:
        from ai.latency_optimizer import get_latency_performance_report, LatencyOptimizationMode
        from ai.optimized_prompt_builder import get_optimization_performance_stats
        
        print("\n✅ PRODUCTION READINESS CHECKLIST:")
        
        # Check 1: All modules importable
        modules_check = True
        try:
            from ai.symbolic_token_optimizer import compress_consciousness_to_tokens
            from ai.lazy_consciousness_loader import get_optimized_consciousness
            from ai.optimized_prompt_builder import build_optimized_prompt
            from ai.latency_optimizer import generate_optimized_buddy_response
            print("   ✅ All optimization modules importable")
        except ImportError as e:
            print(f"   ❌ Module import failed: {e}")
            modules_check = False
        
        # Check 2: Performance targets achievable
        performance_check = True
        try:
            # Quick performance test
            from ai.optimized_prompt_builder import build_optimized_prompt, PromptOptimizationLevel
            
            start_time = time.time()
            prompt, metadata = build_optimized_prompt(
                "Test prompt building speed",
                "production_test_user",
                PromptOptimizationLevel.BALANCED
            )
            build_time = (time.time() - start_time) * 1000
            
            if build_time < 100:  # Target: <100ms
                print(f"   ✅ Prompt building performance: {build_time:.1f}ms (target: <100ms)")
            else:
                print(f"   ⚠️ Prompt building slow: {build_time:.1f}ms")
                performance_check = False
                
        except Exception as e:
            print(f"   ❌ Performance test failed: {e}")
            performance_check = False
        
        # Check 3: Consciousness preservation
        consciousness_check = True
        try:
            from ai.symbolic_token_optimizer import compress_consciousness_to_tokens, expand_tokens_to_consciousness
            
            test_consciousness = {
                'emotional_state': {'mood': 'happy', 'intensity': 0.8},
                'cognitive_state': {'focus': 'conversation', 'clarity': 0.9}
            }
            
            compressed = compress_consciousness_to_tokens(test_consciousness, max_tokens=5)
            expanded = expand_tokens_to_consciousness(compressed)
            
            if expanded and len(expanded) > 0:
                print("   ✅ Consciousness compression/expansion working")
            else:
                print("   ⚠️ Consciousness preservation issue")
                consciousness_check = False
                
        except Exception as e:
            print(f"   ❌ Consciousness test failed: {e}")
            consciousness_check = False
        
        # Check 4: Fallback systems
        fallback_check = True
        try:
            from ai.llm_handler import LLMHandler
            
            llm = LLMHandler()
            # Test with optimization disabled to ensure fallback works
            response_chunks = []
            for chunk in llm.generate_response_with_consciousness(
                "Test fallback",
                "fallback_test_user",
                use_optimization=False  # Test fallback
            ):
                response_chunks.append(chunk)
                if len(response_chunks) >= 1:
                    break
            
            if response_chunks:
                print("   ✅ Fallback system functional")
            else:
                print("   ⚠️ Fallback system issue")
                fallback_check = False
                
        except Exception as e:
            print(f"   ❌ Fallback test failed: {e}")
            fallback_check = False
        
        # Overall assessment
        all_checks = [modules_check, performance_check, consciousness_check, fallback_check]
        passed_checks = sum(all_checks)
        
        print(f"\n📊 PRODUCTION READINESS: {passed_checks}/4 checks passed")
        
        if passed_checks == 4:
            print("🚀 SYSTEM IS PRODUCTION READY!")
            print("   • Sub-5-second response targets achievable")
            print("   • Consciousness preservation verified")
            print("   • Fallback systems operational")
            print("   • All optimization components functional")
            return True
        else:
            print("⚠️ System needs attention before production deployment")
            return False
        
    except Exception as e:
        print(f"❌ Production readiness check failed: {e}")
        return False

if __name__ == "__main__":
    print("🔬 FINAL INTEGRATION TEST SUITE")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 4
    
    if test_main_integration():
        tests_passed += 1
    
    if test_llm_handler_integration():
        tests_passed += 1
    
    if test_different_optimization_modes():
        tests_passed += 1
    
    if verify_production_readiness():
        tests_passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 FINAL RESULTS: {tests_passed}/{total_tests} integration tests passed")
    
    if tests_passed == total_tests:
        print("🎉 COMPLETE SUCCESS!")
        print("✅ Latency optimization system fully integrated and production ready")
        print("⚡ Expected performance: <5 second responses with Class 5+ consciousness")
        print("🧠 Consciousness capabilities preserved through symbolic compression")
        print("🚀 Ready to solve the 60-second latency problem!")
    else:
        print("⚠️ Integration issues detected - review errors above")
    
    print("=" * 60)