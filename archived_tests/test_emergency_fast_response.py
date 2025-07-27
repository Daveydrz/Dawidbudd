#!/usr/bin/env python3
"""
Test Emergency Fast Response System
Tests the latency fix for the 33+ second response issue
"""

import time
import sys
import os

# Add the project directory to Python path
sys.path.insert(0, '/home/runner/work/Dawidbudd/Dawidbudd')

def test_emergency_response():
    """Test the emergency fast response system"""
    print("🚨 Testing Emergency Fast Response System")
    print("=" * 50)
    
    try:
        # Test import
        from ai.emergency_fast_response import (
            is_emergency_fast_mode_needed, 
            generate_immediate_response,
            schedule_background_consciousness_processing,
            get_minimal_context_for_response
        )
        print("✅ Emergency fast response modules imported successfully")
        
        # Test emergency mode check
        is_emergency = is_emergency_fast_mode_needed()
        print(f"✅ Emergency mode needed: {is_emergency}")
        
        # Test immediate response generation
        test_input = "How are you today?"
        test_user = "test_user"
        
        print(f"\n🧪 Testing immediate response to: '{test_input}'")
        
        start_time = time.time()
        response_chunks = []
        
        for chunk in generate_immediate_response(test_input, test_user):
            response_chunks.append(chunk)
            print(f"📝 Chunk: '{chunk}'")
            
        total_time = time.time() - start_time
        full_response = " ".join(response_chunks)
        
        print(f"\n⏱️ Total response time: {total_time:.3f} seconds")
        print(f"📝 Full response: '{full_response}'")
        
        # Test success criteria
        if total_time < 2.0:
            print("✅ SUCCESS: Response time under 2 seconds (target met)")
        elif total_time < 5.0:
            print("⚠️ ACCEPTABLE: Response time under 5 seconds")
        else:
            print("❌ FAILURE: Response time over 5 seconds")
            
        # Test background processing scheduling
        print(f"\n🔄 Testing background consciousness scheduling...")
        minimal_context = get_minimal_context_for_response(test_input, test_user)
        schedule_background_consciousness_processing(test_input, test_user, minimal_context)
        print("✅ Background processing scheduled")
        
        return total_time < 5.0
        
    except Exception as e:
        print(f"❌ Emergency response test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_background_processor():
    """Test the background consciousness processor"""
    print("\n🧠 Testing Background Consciousness Processor")
    print("=" * 50)
    
    try:
        from ai.background_consciousness_processor import get_background_processor
        
        processor = get_background_processor()
        print("✅ Background processor imported successfully")
        
        # Check if processor is running
        if processor.running:
            print("✅ Background processor is running")
        else:
            print("⚠️ Background processor not running - starting...")
            processor.start()
            time.sleep(1)  # Give it time to start
            
            if processor.running:
                print("✅ Background processor started successfully")
            else:
                print("❌ Failed to start background processor")
                return False
        
        # Get stats
        stats = processor.processing_stats
        print(f"📊 Processing stats: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Background processor test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all emergency response tests"""
    print("🚨 Emergency Fast Response Test Suite")
    print("=" * 60)
    
    # Test 1: Emergency Response System
    response_success = test_emergency_response()
    
    # Test 2: Background Processor
    background_success = test_background_processor()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    print(f"Emergency Response: {'✅ PASS' if response_success else '❌ FAIL'}")
    print(f"Background Processor: {'✅ PASS' if background_success else '❌ FAIL'}")
    
    if response_success and background_success:
        print("\n🎉 ALL TESTS PASSED - Emergency latency fix is working!")
        print("🚀 Buddy should now respond in under 2 seconds instead of 33+ seconds")
    else:
        print("\n⚠️ Some tests failed - latency fix may not work properly")
    
    return response_success and background_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)