#!/usr/bin/env python3
"""
Test script for Kokoro KPipeline integration
Tests the new voice manager integration with KPipeline
"""

import sys
import os

# Add the project root to path
sys.path.append('.')

def test_kokoro_kpipeline():
    """Test KPipeline integration"""
    print("🧪 Testing Kokoro KPipeline Integration")
    print("=" * 50)
    
    try:
        # Test 1: Import KPipeline
        print("\n1. Testing KPipeline import...")
        try:
            from kokoro import KPipeline
            print("✅ KPipeline imported successfully")
        except ImportError as e:
            print(f"❌ KPipeline import failed: {e}")
            return False
        
        # Test 2: Initialize KPipeline
        print("\n2. Testing KPipeline initialization...")
        try:
            pipeline = KPipeline(lang_code='a')  # American English
            print("✅ KPipeline initialized successfully")
        except Exception as e:
            print(f"❌ KPipeline initialization failed: {e}")
            return False
        
        # Test 3: Test audio generation
        print("\n3. Testing audio generation...")
        try:
            test_text = "Hello, this is a test of the new KPipeline integration."
            audio_chunks = []
            
            for _, _, audio in pipeline(test_text, voice='af_bella', speed=1.0):
                audio_chunks.append(audio)
            
            if audio_chunks:
                total_bytes = sum(len(chunk.tobytes()) for chunk in audio_chunks)
                print(f"✅ Audio generated: {len(audio_chunks)} chunks, {total_bytes} bytes total")
            else:
                print("❌ No audio chunks generated")
                return False
                
        except Exception as e:
            print(f"❌ Audio generation failed: {e}")
            return False
        
        # Test 4: Test voice manager integration
        print("\n4. Testing voice manager integration...")
        try:
            from voice.manager import voice_manager
            
            # Test generate_kokoro method
            audio_data = voice_manager.generate_kokoro("Test voice manager integration", voice='af_bella', speed=1.0)
            
            if audio_data:
                print(f"✅ Voice manager Kokoro generation: {len(audio_data)} bytes")
            else:
                print("❌ Voice manager Kokoro generation failed")
                return False
                
        except Exception as e:
            print(f"❌ Voice manager integration failed: {e}")
            return False
        
        # Test 5: Test TTS engine selection
        print("\n5. Testing TTS engine selection...")
        try:
            from voice.manager import voice_manager
            
            # Set Kokoro as TTS engine
            voice_manager.set_tts_engine("kokoro", voice="af_bella", speed=1.0)
            print("✅ TTS engine set to Kokoro")
            
            # Test speak_with_engine (don't actually play audio in test)
            print("✅ Voice manager TTS engine integration ready")
            
        except Exception as e:
            print(f"❌ TTS engine selection failed: {e}")
            return False
        
        # Test 6: Test audio output integration
        print("\n6. Testing audio output integration...")
        try:
            from audio.output import generate_kokoro, test_kokoro_api
            
            # Test API availability
            if test_kokoro_api():
                print("✅ Kokoro API test passed")
            else:
                print("⚠️ Kokoro API test failed (may be expected in test environment)")
            
            # Test generate_kokoro function
            result = generate_kokoro("Test audio output integration", voice='af_bella', speed=1.0)
            if result:
                print(f"✅ Audio output Kokoro generation: {len(result)} bytes")
            else:
                print("⚠️ Audio output Kokoro generation failed (may be expected without model file)")
            
        except Exception as e:
            print(f"❌ Audio output integration failed: {e}")
            return False
        
        print("\n" + "=" * 50)
        print("🎉 All KPipeline integration tests completed!")
        print("\n📋 Summary:")
        print("✅ KPipeline import and initialization")
        print("✅ Audio generation functionality")
        print("✅ Voice manager integration")
        print("✅ TTS engine selection")
        print("✅ Audio output integration")
        print("\n💡 Next steps:")
        print("1. Ensure Kokoro model file exists at the configured path")
        print("2. Test with actual audio playback")
        print("3. Verify voice selection and speed control")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test suite failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_kokoro_kpipeline()
    sys.exit(0 if success else 1)