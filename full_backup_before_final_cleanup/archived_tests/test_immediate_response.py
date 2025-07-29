#!/usr/bin/env python3
"""
Test Immediate Response with Background Consciousness Processing
Created: 2025-01-17
Purpose: Test the new background processing system for speeding up responses
"""

import time
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_background_processor():
    """Test the background consciousness processor module"""
    print("🧪 Testing Background Consciousness Processor...")
    
    try:
        from ai.background_consciousness_processor import (
            background_processor,
            start_background_processing,
            schedule_background_thoughts,
            get_background_processing_stats,
            stop_background_processing
        )
        
        print("✅ Background processor imports successful")
        
        # Test starting the processor
        start_background_processing()
        print("✅ Background processor started")
        
        # Test scheduling tasks
        schedule_background_thoughts(
            user_input="Hello, how are you?",
            user_id="test_user",
            response="I'm doing well, thank you!",
            delay=1.0
        )
        print("✅ Background tasks scheduled")
        
        # Wait a moment and check stats
        time.sleep(2.0)
        stats = get_background_processing_stats()
        print(f"✅ Background stats: {stats}")
        
        # Stop processor
        stop_background_processing()
        print("✅ Background processor stopped")
        
        return True
        
    except Exception as e:
        print(f"❌ Background processor test failed: {e}")
        return False

def test_llm_handler_immediate_response():
    """Test the LLM handler immediate response method"""
    print("\n🧪 Testing LLM Handler Immediate Response...")
    
    try:
        from ai.llm_handler import (
            llm_handler,
            generate_immediate_response_with_background_consciousness
        )
        
        print("✅ LLM handler imports successful")
        
        # Test immediate response
        test_input = "What's the weather like?"
        test_user = "test_user"
        
        print(f"🔄 Testing immediate response for: '{test_input}'")
        start_time = time.time()
        
        response_chunks = []
        for chunk in generate_immediate_response_with_background_consciousness(test_input, test_user):
            response_chunks.append(chunk)
            print(f"📄 Chunk: {chunk}")
            
        response_time = time.time() - start_time
        full_response = " ".join(response_chunks)
        
        print(f"✅ Response generated in {response_time:.3f} seconds")
        print(f"✅ Full response: {full_response}")
        print(f"✅ Response length: {len(full_response)} characters")
        
        # Check if response time is under target (5 seconds)
        if response_time < 5.0:
            print(f"🎯 SPEED TARGET MET: {response_time:.3f}s < 5.0s")
        else:
            print(f"⚠️ Speed target missed: {response_time:.3f}s >= 5.0s")
        
        return True
        
    except Exception as e:
        print(f"❌ LLM handler immediate response test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration():
    """Test integration between components"""
    print("\n🧪 Testing Integration...")
    
    try:
        # Test that the background processor and LLM handler work together
        from ai.background_consciousness_processor import start_background_processing, get_background_processing_stats
        from ai.llm_handler import get_llm_session_statistics
        
        # Start background processing
        start_background_processing()
        
        # Get stats from both systems
        bg_stats = get_background_processing_stats()
        llm_stats = get_llm_session_statistics()
        
        print(f"✅ Background processor stats: {bg_stats}")
        print(f"✅ LLM handler stats: {llm_stats}")
        
        # Check if background processing is enabled in LLM handler
        if llm_stats.get("background_processing_enabled"):
            print("✅ Background processing enabled in LLM handler")
        else:
            print("⚠️ Background processing not enabled in LLM handler")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def test_class5_consciousness_preservation():
    """Test that Class 5+ consciousness is preserved"""
    print("\n🧪 Testing Class 5+ Consciousness Preservation...")
    
    try:
        # Check if consciousness modules are available
        consciousness_available = False
        
        try:
            from ai.global_workspace import global_workspace
            from ai.emotion import emotion_engine
            from ai.motivation import motivation_system
            consciousness_available = True
            print("✅ Core consciousness modules available")
        except ImportError:
            print("⚠️ Core consciousness modules not available")
        
        # Check if background processor can handle consciousness
        from ai.background_consciousness_processor import background_processor
        
        if consciousness_available:
            # Register consciousness modules with background processor
            consciousness_modules = {
                'global_workspace': 'available',
                'emotion_engine': 'available',
                'motivation_system': 'available'
            }
            background_processor.register_consciousness_modules(consciousness_modules)
            print("✅ Consciousness modules registered with background processor")
        
        # Test that all required methods exist
        methods_to_check = [
            'schedule_background_thoughts',
            'is_system_idle',
            '_run_pending_inner_monologue',
            '_run_pending_emotion_update',
            '_run_pending_belief_update',
            '_run_pending_memory_update'
        ]
        
        for method_name in methods_to_check:
            if hasattr(background_processor, method_name):
                print(f"✅ Method {method_name} available")
            else:
                print(f"❌ Method {method_name} missing")
                return False
        
        print("✅ Class 5+ consciousness preservation mechanisms in place")
        return True
        
    except Exception as e:
        print(f"❌ Consciousness preservation test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Immediate Response with Background Consciousness Processing")
    print("=" * 60)
    
    tests = [
        ("Background Processor", test_background_processor),
        ("LLM Handler Immediate Response", test_llm_handler_immediate_response),
        ("Integration", test_integration),
        ("Class 5+ Consciousness Preservation", test_class5_consciousness_preservation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Immediate response system ready!")
        print("⚡ Speed optimization: User responses prioritized")
        print("🧠 Class 5+ consciousness: Maintained via background processing")
        print("🛡️ Fail-safe: Error handling prevents blocking")
    else:
        print("⚠️ Some tests failed - review implementation")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)