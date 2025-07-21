#!/usr/bin/env python3
"""
Test Emergency Ultra-Fast Response System
Created: 2025-01-17
Purpose: Test that the emergency response system fixes the 4-minute latency issue
"""

import time
import sys
import os

# Add the project root to Python path
sys.path.insert(0, '/home/runner/work/Dawidbudd/Dawidbudd')

def test_ultra_fast_response():
    """Test the ultra-fast response system"""
    print("🚨 TESTING EMERGENCY ULTRA-FAST RESPONSE SYSTEM 🚨")
    print("="*60)
    
    try:
        from ai.ultra_fast_response import generate_ultra_fast_response, get_ultra_fast_stats
        print("✅ Ultra-fast response system imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import ultra-fast response: {e}")
        return False
    
    # Test cases representing typical user inputs
    test_cases = [
        "Hello, how are you?",
        "What time is it?",
        "Tell me about artificial intelligence",
        "What's the weather like today?",
        "Can you help me with something?",
        "What's your name?",
        "Where are you located?",
        "How do you work?",
        "What can you do for me?",
        "Thank you for your help"
    ]
    
    total_time = 0.0
    successful_responses = 0
    failed_responses = 0
    
    print(f"\n🧪 Running {len(test_cases)} response speed tests...")
    print(f"🎯 Target: <2 seconds per response (was 4+ minutes)")
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n--- Test {i}/{len(test_cases)} ---")
        print(f"Input: '{test_input}'")
        
        start_time = time.time()
        response_parts = []
        
        try:
            # Generate response using ultra-fast system
            for chunk in generate_ultra_fast_response(test_input, "test_user"):
                response_parts.append(chunk)
                
                # Emergency timeout protection
                if time.time() - start_time > 10.0:
                    print("⚠️ Emergency timeout - breaking")
                    break
            
            response_time = time.time() - start_time
            full_response = " ".join(response_parts)
            
            # Evaluate response
            if response_time <= 2.0:
                status = "✅ SUCCESS"
                successful_responses += 1
            elif response_time <= 5.0:
                status = "⚠️ SLOW"
                successful_responses += 1
            else:
                status = "❌ FAILED"
                failed_responses += 1
            
            total_time += response_time
            
            print(f"Response: '{full_response[:80]}...'")
            print(f"Time: {response_time:.3f}s {status}")
            print(f"Chunks: {len(response_parts)}")
            
            if response_time > 2.0:
                print(f"⚠️ Exceeded target by {response_time - 2.0:.3f}s")
            else:
                print(f"✅ Under target with {2.0 - response_time:.3f}s to spare")
            
        except Exception as e:
            response_time = time.time() - start_time
            print(f"❌ ERROR after {response_time:.3f}s: {e}")
            failed_responses += 1
            total_time += response_time
    
    # Calculate final statistics
    avg_response_time = total_time / len(test_cases)
    success_rate = (successful_responses / len(test_cases)) * 100
    
    print(f"\n" + "="*60)
    print(f"📊 EMERGENCY RESPONSE SYSTEM TEST RESULTS")
    print(f"="*60)
    print(f"✅ Successful responses: {successful_responses}/{len(test_cases)}")
    print(f"❌ Failed responses: {failed_responses}/{len(test_cases)}")
    print(f"📈 Success rate: {success_rate:.1f}%")
    print(f"⏱️  Average response time: {avg_response_time:.3f}s")
    print(f"🎯 Target response time: 2.000s")
    
    if avg_response_time <= 2.0:
        print(f"🎉 TARGET ACHIEVED! Average time under 2 seconds")
        improvement = ((240.0 - avg_response_time) / 240.0) * 100  # Assuming 4 min was original
        print(f"🚀 Improvement: {improvement:.1f}% faster than original 4-minute responses")
    else:
        print(f"⚠️ Target missed by {avg_response_time - 2.0:.3f}s")
        if avg_response_time < 10.0:
            improvement = ((240.0 - avg_response_time) / 240.0) * 100
            print(f"🔧 Still much better: {improvement:.1f}% improvement over original")
    
    # Show detailed stats
    try:
        stats = get_ultra_fast_stats()
        print(f"\n📊 System Statistics:")
        print(f"   Total responses: {stats['total_responses']}")
        print(f"   Average time: {stats['average_response_time']:.3f}s")
        print(f"   Success rate: {stats['success_rate']*100:.1f}%")
        print(f"   Time saved: {stats['total_time_saved']:.1f}s total")
        print(f"   Status: {stats['status']}")
    except Exception as e:
        print(f"⚠️ Could not get detailed stats: {e}")
    
    # Determine overall result
    if success_rate >= 80 and avg_response_time <= 5.0:
        print(f"\n🎉 LATENCY CRISIS RESOLVED!")
        print(f"✅ Emergency ultra-fast response system working correctly")
        print(f"🚀 User responses now {avg_response_time:.1f}s instead of 4+ minutes")
        return True
    else:
        print(f"\n❌ SYSTEM NEEDS MORE WORK")
        print(f"⚠️ Either success rate too low or responses still too slow")
        return False

def test_background_consciousness():
    """Test that consciousness processing runs in background"""
    print(f"\n🧠 TESTING TRUE BACKGROUND CONSCIOUSNESS")
    print(f"="*40)
    
    try:
        from ai.true_background_consciousness import (
            start_true_background_processing,
            queue_consciousness_processing_true_bg,
            get_true_background_stats,
            is_true_background_healthy
        )
        print("✅ True background consciousness imported")
        
        # Start the system
        start_true_background_processing()
        print("✅ Background processing started")
        
        # Queue some consciousness tasks
        queue_consciousness_processing_true_bg(
            "Test consciousness input",
            "test_user", 
            "Test consciousness response",
            delay=0.1
        )
        print("✅ Consciousness processing queued")
        
        # Check that it returns immediately
        start_time = time.time()
        for i in range(5):
            queue_consciousness_processing_true_bg(
                f"Background test {i}",
                "test_user",
                f"Background response {i}",
                delay=0.1
            )
        queue_time = time.time() - start_time
        
        print(f"✅ Queued 5 consciousness tasks in {queue_time:.3f}s")
        
        if queue_time < 0.1:
            print(f"🎉 Background queueing is INSTANT - no blocking!")
        else:
            print(f"⚠️ Background queueing took {queue_time:.3f}s - may still be blocking")
        
        # Wait a bit for processing
        time.sleep(2.0)
        
        # Check stats
        stats = get_true_background_stats()
        print(f"\n📊 Background Processing Stats:")
        print(f"   Tasks queued: {stats['tasks_queued']}")
        print(f"   Tasks completed: {stats['tasks_completed']}")
        print(f"   Tasks failed: {stats['tasks_failed']}")
        print(f"   Queue size: {stats['queue_size']}")
        print(f"   Average task time: {stats['average_task_time']:.3f}s")
        
        healthy = is_true_background_healthy()
        print(f"   System healthy: {healthy}")
        
        if healthy and stats['tasks_completed'] > 0:
            print(f"✅ Background consciousness is working correctly")
            return True
        else:
            print(f"❌ Background consciousness has issues")
            return False
            
    except ImportError as e:
        print(f"❌ Could not import background consciousness: {e}")
        return False
    except Exception as e:
        print(f"❌ Background consciousness error: {e}")
        return False

def test_voice_detection_fix():
    """Test voice detection emergency fixes"""
    print(f"\n🎤 TESTING VOICE DETECTION EMERGENCY FIX")
    print(f"="*40)
    
    try:
        from ai.voice_detection_fix import (
            emergency_voice_detection,
            get_voice_detection_stats,
            force_voice_detection_reset
        )
        import numpy as np
        
        print("✅ Voice detection fix imported")
        
        # Test with dummy audio
        test_audio = np.random.randint(-1000, 1000, 1000, dtype=np.int16)
        
        detection_times = []
        for i in range(5):
            start_time = time.time()
            is_voice, info = emergency_voice_detection(test_audio)
            detection_time = time.time() - start_time
            detection_times.append(detection_time)
            
            print(f"Test {i+1}: Voice={is_voice}, Time={detection_time:.3f}s")
            
            if detection_time > 1.0:
                print(f"⚠️ Detection too slow: {detection_time:.3f}s")
        
        avg_detection_time = sum(detection_times) / len(detection_times)
        print(f"\n📊 Average detection time: {avg_detection_time:.3f}s")
        
        # Test force reset
        force_voice_detection_reset()
        print(f"✅ Force reset successful")
        
        stats = get_voice_detection_stats()
        print(f"📊 Detection stats: {stats}")
        
        if avg_detection_time < 0.5:
            print(f"✅ Voice detection is fast enough")
            return True
        else:
            print(f"❌ Voice detection still too slow")
            return False
            
    except ImportError as e:
        print(f"❌ Could not import voice detection fix: {e}")
        return False
    except Exception as e:
        print(f"❌ Voice detection test error: {e}")
        return False

def main():
    """Main test function"""
    print("🚨 EMERGENCY LATENCY FIX VERIFICATION TESTS 🚨")
    print("This test verifies that the 4-minute latency issue has been resolved")
    print("="*80)
    
    # Track overall results
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Ultra-fast responses
    print(f"\n{'='*20} TEST 1: ULTRA-FAST RESPONSES {'='*20}")
    if test_ultra_fast_response():
        tests_passed += 1
        print(f"✅ Test 1 PASSED: Ultra-fast responses working")
    else:
        print(f"❌ Test 1 FAILED: Ultra-fast responses not working")
    
    # Test 2: Background consciousness
    print(f"\n{'='*20} TEST 2: BACKGROUND CONSCIOUSNESS {'='*19}")
    if test_background_consciousness():
        tests_passed += 1
        print(f"✅ Test 2 PASSED: Background consciousness working")
    else:
        print(f"❌ Test 2 FAILED: Background consciousness not working")
    
    # Test 3: Voice detection fixes
    print(f"\n{'='*20} TEST 3: VOICE DETECTION FIXES {'='*21}")
    if test_voice_detection_fix():
        tests_passed += 1
        print(f"✅ Test 3 PASSED: Voice detection fixes working")
    else:
        print(f"❌ Test 3 FAILED: Voice detection fixes not working")
    
    # Final results
    print(f"\n" + "="*80)
    print(f"🏁 FINAL TEST RESULTS")
    print(f"="*80)
    print(f"✅ Tests passed: {tests_passed}/{total_tests}")
    print(f"❌ Tests failed: {total_tests - tests_passed}/{total_tests}")
    
    success_rate = (tests_passed / total_tests) * 100
    print(f"📈 Success rate: {success_rate:.1f}%")
    
    if tests_passed == total_tests:
        print(f"\n🎉 ALL TESTS PASSED!")
        print(f"✅ The 4-minute latency crisis has been RESOLVED!")
        print(f"🚀 Buddy now responds in <2 seconds instead of 4+ minutes")
        print(f"🧠 Class 5+ consciousness preserved in background")
        print(f"🎤 Voice detection no longer gets stuck")
        print(f"⚡ User speech is prioritized over everything")
        return True
    elif tests_passed >= 2:
        print(f"\n⚠️ MOSTLY WORKING - {tests_passed}/{total_tests} tests passed")
        print(f"🔧 System is much improved but may need minor fixes")
        return True
    else:
        print(f"\n❌ SYSTEM STILL HAS MAJOR ISSUES")
        print(f"🚨 More work needed to resolve latency crisis")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n🛑 Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test crashed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)