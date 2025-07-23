#!/usr/bin/env python3
"""
Test script to verify Kokoro KPipeline integration matches the working pattern
This script mimics the user's working test file
"""

import sys
import os
import numpy as np

def test_direct_kokoro():
    """Test the exact same pattern as the user's working test file"""
    print("[TEST] 🧪 Testing direct Kokoro KPipeline (user's working pattern)...")
    
    try:
        from kokoro import KPipeline
        import soundfile as sf
        import simpleaudio as sa
        
        print("[TEST] ✅ Successfully imported kokoro, soundfile, and simpleaudio")
        
        # Initialize KPipeline like user's working test
        pipeline = KPipeline(lang_code='a')
        print("[TEST] ✅ KPipeline initialized with lang_code='a'")
        
        text = "This is a test of Kokoro TTS using the af_bella voice model running locally."
        generator = pipeline(text, voice='af_bella')
        
        print(f"[TEST] 🎭 Generating text: '{text}'")
        
        # Use the exact same pattern as user's working test
        for i, (gs, ps, audio) in enumerate(generator):
            print(f"[TEST] Chunk {i}")
            print(f"[TEST] Text:", gs[:50] + "..." if len(gs) > 50 else gs)
            print(f"[TEST] Phonemes:", ps[:50] + "..." if len(ps) > 50 else ps)
            print(f"[TEST] Audio shape:", audio.shape)
            print(f"[TEST] Audio dtype:", audio.dtype)
            
            # Save as WAV file like user's test (but skip actual file creation in test)
            print(f"[TEST] ✅ Would save chunk_{i}.wav with {len(audio)} samples at 24kHz")
        
        print("[TEST] ✅ Direct Kokoro test completed successfully")
        return True
        
    except ImportError as e:
        print(f"[TEST] ❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"[TEST] ❌ Error: {e}")
        return False

def test_buddy_integration():
    """Test Buddy's integration with Kokoro"""
    print("\n[TEST] 🧪 Testing Buddy's Kokoro integration...")
    
    try:
        # Test audio/output.py integration
        from audio.output import generate_kokoro, load_kokoro_model
        
        print("[TEST] ✅ Successfully imported Buddy's Kokoro functions")
        
        # Load model
        success = load_kokoro_model()
        print(f"[TEST] Model loading: {'✅ SUCCESS' if success else '❌ FAILED'}")
        
        if success:
            # Test generation
            result = generate_kokoro("Hello from Buddy", voice='af_bella', speed=1.0)
            
            if result:
                audio_data, sample_rate = result
                print(f"[TEST] ✅ Generated audio: {len(audio_data)} samples at {sample_rate}Hz")
                print(f"[TEST] ✅ Audio dtype: {audio_data.dtype}")
                return True
            else:
                print("[TEST] ❌ No audio generated")
                return False
        else:
            print("[TEST] ❌ Model loading failed")
            return False
            
    except ImportError as e:
        print(f"[TEST] ❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"[TEST] ❌ Error: {e}")
        return False

def test_voice_manager_integration():
    """Test voice manager integration"""
    print("\n[TEST] 🧪 Testing Voice Manager integration...")
    
    try:
        from voice.manager import voice_manager
        
        print("[TEST] ✅ Successfully imported voice_manager")
        
        # Test TTS generation
        audio_data = voice_manager.generate_kokoro("Test from voice manager", voice='af_bella', speed=1.0)
        
        if audio_data:
            print(f"[TEST] ✅ Voice manager generated audio: {len(audio_data)} bytes")
            return True
        else:
            print("[TEST] ❌ Voice manager returned no audio")
            return False
            
    except ImportError as e:
        print(f"[TEST] ❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"[TEST] ❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("🧪 KOKORO KPIPELINE INTEGRATION TEST")
    print("="*60)
    
    tests = [
        ("Direct Kokoro Test", test_direct_kokoro),
        ("Buddy Integration Test", test_buddy_integration),
        ("Voice Manager Test", test_voice_manager_integration)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"[TEST] ❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    print("\n" + "="*60)
    print("📊 TEST RESULTS")
    print("="*60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 SUMMARY: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 ALL TESTS PASSED - Kokoro integration is working correctly!")
    else:
        print("⚠️ SOME TESTS FAILED - Check the error messages above")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)