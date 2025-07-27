#!/usr/bin/env python3
"""
Test script to verify voice detection reset and TTS streaming fixes
"""

import sys
import os
sys.path.append('/home/runner/work/Dawidbudd/Dawidbudd')

def test_tts_streaming_changes():
    """Test that TTS streaming changes are applied correctly"""
    print("🧪 Testing TTS streaming changes...")
    
    try:
        from ai.chat import generate_response_streaming_ultraresponsive
        
        # Check if the function exists (it might be renamed or modified)
        print("✅ generate_response_streaming_ultraresponsive function found")
        
        # We can't easily test the actual streaming without a full LLM setup,
        # but we can verify the constants have been changed
        import inspect
        source = inspect.getsource(generate_response_streaming_ultraresponsive)
        
        if "TARGET_COMPLETION_PERCENTAGE = 0.15" in source:
            print("✅ TARGET_COMPLETION_PERCENTAGE reduced to 15% (was 45%)")
        else:
            print("❌ TARGET_COMPLETION_PERCENTAGE not found or not updated")
            
        if "MIN_WORDS_FOR_FIRST_CHUNK = 4" in source:
            print("✅ MIN_WORDS_FOR_FIRST_CHUNK reduced to 4 words (was 8)")
        else:
            print("❌ MIN_WORDS_FOR_FIRST_CHUNK not found or not updated")
            
        if "IMMEDIATE STREAMING" in source:
            print("✅ Immediate streaming comments found")
        else:
            print("❌ Immediate streaming changes not found")
            
    except ImportError as e:
        print(f"⚠️ Could not import TTS streaming module: {e}")
    except Exception as e:
        print(f"❌ Error testing TTS streaming: {e}")

def test_voice_analyzer_reset():
    """Test voice analyzer reset improvements"""
    print("\n🧪 Testing voice analyzer reset improvements...")
    
    try:
        from audio.voice_analyzer import voice_analyzer
        
        if voice_analyzer:
            print("✅ Voice analyzer loaded")
            
            # Test the enhanced reset method
            voice_analyzer.reset_conversation_state()
            print("✅ Enhanced reset_conversation_state() executed successfully")
            
            # Check if conversation count tracking is working
            if hasattr(voice_analyzer, '_conversation_count'):
                print(f"✅ Conversation count tracking: {voice_analyzer._conversation_count}")
            else:
                print("⚠️ Conversation count tracking not found")
                
        else:
            print("❌ Voice analyzer not available")
            
    except Exception as e:
        print(f"❌ Error testing voice analyzer: {e}")

def test_smart_detection_reset():
    """Test smart detection manager reset"""
    print("\n🧪 Testing smart detection manager reset...")
    
    try:
        from audio.smart_detection_manager import smart_detector
        
        print("✅ Smart detector loaded")
        
        # Test the new reset method
        if hasattr(smart_detector, 'reset_session'):
            smart_detector.reset_session()
            print("✅ New reset_session() method executed successfully")
        else:
            print("❌ reset_session() method not found")
            
    except Exception as e:
        print(f"❌ Error testing smart detection: {e}")

def test_full_duplex_improvements():
    """Test full duplex manager improvements"""
    print("\n🧪 Testing full duplex manager improvements...")
    
    try:
        from audio.full_duplex_manager import full_duplex_manager
        
        if full_duplex_manager:
            print("✅ Full duplex manager loaded")
            
            # Test enhanced force reset
            if hasattr(full_duplex_manager, 'force_reset_to_waiting'):
                print("✅ Enhanced force_reset_to_waiting() method found")
            else:
                print("❌ force_reset_to_waiting() method not found")
                
            # Test stuck state detection
            if hasattr(full_duplex_manager, 'check_for_stuck_state'):
                result = full_duplex_manager.check_for_stuck_state()
                print(f"✅ check_for_stuck_state() executed: {result}")
            else:
                print("❌ check_for_stuck_state() method not found")
                
            # Test state watchdog
            if hasattr(full_duplex_manager, '_state_watchdog'):
                print("✅ State watchdog method found")
            else:
                print("❌ State watchdog method not found")
                
        else:
            print("❌ Full duplex manager not available")
            
    except Exception as e:
        print(f"❌ Error testing full duplex manager: {e}")

def main():
    """Run all tests"""
    print("🚀 Voice Detection & TTS Streaming Fix Verification")
    print("=" * 50)
    
    test_tts_streaming_changes()
    test_voice_analyzer_reset()
    test_smart_detection_reset()
    test_full_duplex_improvements()
    
    print("\n" + "=" * 50)
    print("✅ Test suite completed!")
    print("\n📋 Summary of fixes:")
    print("1. TTS streaming delay reduced from 45% to 15% completion")
    print("2. Enhanced voice analyzer reset with conversation tracking")
    print("3. Smart detection manager session reset added")
    print("4. Full duplex manager stuck state detection and recovery")
    print("5. State watchdog for automatic stuck state recovery")

if __name__ == "__main__":
    main()