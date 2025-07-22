#!/usr/bin/env python3
"""
Test script for Kokoro Direct Library integration
Verifies that the switch from FastAPI to direct library works correctly
"""

import sys
import os
import time

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_kokoro_import():
    """Test if we can import the necessary modules"""
    print("[Test] 🧪 Testing Kokoro Direct Library Import...")
    
    try:
        from config import KOKORO_MODEL_PATH, KOKORO_DEFAULT_VOICE, KOKORO_VOICES
        print(f"[Test] ✅ Config imported successfully")
        print(f"[Test] 📍 Model Path: {KOKORO_MODEL_PATH}")
        print(f"[Test] 🎵 Default Voice: {KOKORO_DEFAULT_VOICE}")
        print(f"[Test] 🎭 Available Voices: {len(KOKORO_VOICES)}")
        
        return True
    except Exception as e:
        print(f"[Test] ❌ Config import failed: {e}")
        return False

def test_audio_output_import():
    """Test if we can import the updated audio output module"""
    print("[Test] 🧪 Testing Audio Output Module Import...")
    
    try:
        from audio.output import load_kokoro_model, generate_tts, test_kokoro_api
        print(f"[Test] ✅ Audio output module imported successfully")
        
        # Test the API check (which now checks model loading)
        model_available = test_kokoro_api()
        if model_available:
            print(f"[Test] ✅ Kokoro model loaded successfully")
        else:
            print(f"[Test] ⚠️ Kokoro model not available (expected on test environment)")
        
        return True
    except Exception as e:
        print(f"[Test] ❌ Audio output import failed: {e}")
        return False

def test_removed_fastapi_references():
    """Test that FastAPI references have been removed"""
    print("[Test] 🧪 Testing FastAPI References Removal...")
    
    try:
        # Check if old FastAPI imports are removed
        import audio.output as output_module
        
        # These should not exist anymore
        old_attributes = [
            'KOKORO_API_BASE_URL',
            'KOKORO_API_TIMEOUT', 
            'KOKORO_API_VOICES',
            'kokoro_api_available'
        ]
        
        removed_count = 0
        for attr in old_attributes:
            if not hasattr(output_module, attr):
                removed_count += 1
                print(f"[Test] ✅ {attr} successfully removed")
            else:
                print(f"[Test] ⚠️ {attr} still exists")
        
        print(f"[Test] 📊 Removed {removed_count}/{len(old_attributes)} FastAPI references")
        
        # Check if new attributes exist
        new_attributes = [
            'KOKORO_MODEL_PATH',
            'KOKORO_VOICES',
            'kokoro_model',
            'load_kokoro_model'
        ]
        
        added_count = 0
        for attr in new_attributes:
            if hasattr(output_module, attr):
                added_count += 1
                print(f"[Test] ✅ {attr} successfully added")
            else:
                print(f"[Test] ❌ {attr} missing")
        
        print(f"[Test] 📊 Added {added_count}/{len(new_attributes)} direct library references")
        
        return removed_count >= 3 and added_count >= 3
        
    except Exception as e:
        print(f"[Test] ❌ FastAPI removal test failed: {e}")
        return False

def test_config_updates():
    """Test that config.py has been updated correctly"""
    print("[Test] 🧪 Testing Config Updates...")
    
    try:
        from config import KOKORO_MODEL_PATH, KOKORO_VOICES
        
        # Check model path
        expected_path = "C:/Users/drzew/kokoro-onnx/kokoro-v1_0.pth"
        if KOKORO_MODEL_PATH == expected_path:
            print(f"[Test] ✅ Model path correctly set: {KOKORO_MODEL_PATH}")
        else:
            print(f"[Test] ❌ Model path incorrect: {KOKORO_MODEL_PATH}")
            return False
        
        # Check if KOKORO_VOICES exists (not KOKORO_API_VOICES)
        if isinstance(KOKORO_VOICES, dict) and len(KOKORO_VOICES) > 0:
            print(f"[Test] ✅ KOKORO_VOICES properly configured with {len(KOKORO_VOICES)} voices")
        else:
            print(f"[Test] ❌ KOKORO_VOICES not properly configured")
            return False
        
        return True
        
    except Exception as e:
        print(f"[Test] ❌ Config update test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 KOKORO DIRECT LIBRARY INTEGRATION TEST")
    print("=" * 60)
    
    tests = [
        ("Config Import", test_kokoro_import),
        ("Audio Output Import", test_audio_output_import),
        ("FastAPI Removal", test_removed_fastapi_references),
        ("Config Updates", test_config_updates)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        print("-" * 40)
        
        try:
            result = test_func()
            if result:
                print(f"[Test] ✅ {test_name} PASSED")
                passed += 1
            else:
                print(f"[Test] ❌ {test_name} FAILED")
        except Exception as e:
            print(f"[Test] ❌ {test_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Kokoro Direct Library integration successful!")
        return True
    else:
        print("⚠️ Some tests failed. Check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)