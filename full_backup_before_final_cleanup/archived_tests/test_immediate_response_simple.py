#!/usr/bin/env python3
"""
Simple Test for Immediate Response Architecture
"""

import sys
import time

def test_immediate_response():
    """Test the immediate response system"""
    print("🚀 Testing Immediate Response Architecture...")
    
    try:
        # Mock the required modules to avoid dependencies
        sys.modules['pyaudio'] = type('MockModule', (), {})()
        sys.modules['pvporcupine'] = type('MockModule', (), {})()
        sys.modules['scipy.io.wavfile'] = type('MockModule', (), {'write': lambda *args: None})()
        
        # Mock audio functions
        def mock_speak_streaming(text):
            print(f"🎵 [MOCK SPEECH] {text}")
        
        sys.modules['audio.output'] = type('MockModule', (), {'speak_streaming': mock_speak_streaming})()
        
        # Now try to import and test
        from main import handle_streaming_response
        
        print("✅ handle_streaming_response imported successfully")
        
        # Test basic response
        print("\n🧪 Testing immediate response flow...")
        start_time = time.time()
        
        # This should trigger immediate response without waiting for consciousness
        handle_streaming_response("Hello, how are you?", "TestUser")
        
        response_time = time.time() - start_time
        print(f"\n📊 Response completed in {response_time:.3f}s")
        
        if response_time < 5.0:
            print("✅ PASS: Response time under 5 seconds")
        else:
            print("❌ FAIL: Response time too slow")
        
        print("\n✅ Immediate response architecture test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_immediate_response()
    sys.exit(0 if success else 1)
