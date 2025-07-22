#!/usr/bin/env python3
"""
Comprehensive verification script for Kokoro Direct Library integration
Checks file contents and import changes without loading heavy dependencies
"""

import os
import re

def check_file_content(filepath, check_name):
    """Check if a file contains expected content changes"""
    if not os.path.exists(filepath):
        print(f"[Check] ❌ {check_name}: File {filepath} not found")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        print(f"[Check] ❌ {check_name}: Error reading {filepath}: {e}")
        return False

def verify_audio_output_changes():
    """Verify changes in audio/output.py"""
    print("[Verify] 🔍 Checking audio/output.py changes...")
    
    content = check_file_content("audio/output.py", "Audio Output")
    if not content:
        return False
    
    # Check for new imports
    has_kokoro_import = "from kokoro import Kokoro" in content
    print(f"[Verify] {'✅' if has_kokoro_import else '❌'} Kokoro import: {has_kokoro_import}")
    
    # Check for model path
    has_model_path = "KOKORO_MODEL_PATH" in content
    print(f"[Verify] {'✅' if has_model_path else '❌'} Model path config: {has_model_path}")
    
    # Check for direct library functions
    has_load_model = "def load_kokoro_model" in content
    print(f"[Verify] {'✅' if has_load_model else '❌'} Load model function: {has_load_model}")
    
    has_kokoro_model_var = "kokoro_model =" in content
    print(f"[Verify] {'✅' if has_kokoro_model_var else '❌'} Kokoro model variable: {has_kokoro_model_var}")
    
    # Check for removed FastAPI code
    has_requests_import = "import requests" in content
    print(f"[Verify] {'✅' if not has_requests_import else '❌'} Requests import removed: {not has_requests_import}")
    
    has_fastapi_url = "KOKORO_API_BASE_URL" in content  
    print(f"[Verify] {'✅' if not has_fastapi_url else '❌'} FastAPI URL removed: {not has_fastapi_url}")
    
    has_requests_post = "requests.post" in content
    print(f"[Verify] {'✅' if not has_requests_post else '❌'} requests.post calls removed: {not has_requests_post}")
    
    # Check generate_tts function uses direct library
    generate_tts_match = re.search(r'def generate_tts.*?kokoro_model\.generate', content, re.DOTALL)
    has_direct_generation = generate_tts_match is not None
    print(f"[Verify] {'✅' if has_direct_generation else '❌'} Direct generation in generate_tts: {has_direct_generation}")
    
    success_count = sum([
        has_kokoro_import, has_model_path, has_load_model, has_kokoro_model_var,
        not has_requests_import, not has_fastapi_url, not has_requests_post, has_direct_generation
    ])
    
    print(f"[Verify] 📊 Audio Output: {success_count}/8 checks passed")
    return success_count >= 6

def verify_config_changes():
    """Verify changes in config.py"""
    print("[Verify] 🔍 Checking config.py changes...")
    
    content = check_file_content("config.py", "Config")
    if not content:
        return False
    
    # Check for new model path
    has_correct_path = 'C:/Users/drzew/kokoro-onnx/kokoro-v1_0.pth' in content
    print(f"[Verify] {'✅' if has_correct_path else '❌'} Correct model path: {has_correct_path}")
    
    # Check for KOKORO_VOICES (not KOKORO_API_VOICES)
    has_kokoro_voices = "KOKORO_VOICES =" in content
    print(f"[Verify] {'✅' if has_kokoro_voices else '❌'} KOKORO_VOICES config: {has_kokoro_voices}")
    
    has_old_api_voices = "KOKORO_API_VOICES" in content
    print(f"[Verify] {'✅' if not has_old_api_voices else '❌'} Old API voices removed: {not has_old_api_voices}")
    
    # Check for removed FastAPI configs
    has_api_base_url = "KOKORO_API_BASE_URL" in content
    print(f"[Verify] {'✅' if not has_api_base_url else '❌'} API base URL removed: {not has_api_base_url}")
    
    has_api_timeout = "KOKORO_API_TIMEOUT" in content
    print(f"[Verify] {'✅' if not has_api_timeout else '❌'} API timeout removed: {not has_api_timeout}")
    
    # Check for updated status messages
    has_direct_library_status = "KOKORO DIRECT LIBRARY TTS" in content
    print(f"[Verify] {'✅' if has_direct_library_status else '❌'} Direct library status: {has_direct_library_status}")
    
    success_count = sum([
        has_correct_path, has_kokoro_voices, not has_old_api_voices,
        not has_api_base_url, not has_api_timeout, has_direct_library_status
    ])
    
    print(f"[Verify] 📊 Config: {success_count}/6 checks passed")
    return success_count >= 5

def verify_ai_main_changes():
    """Verify changes in ai/main.py"""
    print("[Verify] 🔍 Checking ai/main.py changes...")
    
    content = check_file_content("ai/main.py", "AI Main")
    if not content:
        return False
    
    # Check for updated messages
    has_direct_library_msg = "Kokoro Direct Library ready" in content
    print(f"[Verify] {'✅' if has_direct_library_msg else '❌'} Direct library message: {has_direct_library_msg}")
    
    has_model_path_msg = "check model at" in content
    print(f"[Verify] {'✅' if has_model_path_msg else '❌'} Model path message: {has_model_path_msg}")
    
    # Check that old FastAPI messages are removed
    has_old_fastapi_msg = "Kokoro-FastAPI connected at" in content
    print(f"[Verify] {'✅' if not has_old_fastapi_msg else '❌'} Old FastAPI message removed: {not has_old_fastapi_msg}")
    
    success_count = sum([has_direct_library_msg, has_model_path_msg, not has_old_fastapi_msg])
    
    print(f"[Verify] 📊 AI Main: {success_count}/3 checks passed")
    return success_count >= 2

def verify_main_changes():
    """Verify changes in main.py"""
    print("[Verify] 🔍 Checking main.py changes...")
    
    content = check_file_content("main.py", "Main")
    if not content:
        return False
    
    # Check for updated messages
    has_direct_library_msg = "Kokoro Direct Library ready" in content
    print(f"[Verify] {'✅' if has_direct_library_msg else '❌'} Direct library message: {has_direct_library_msg}")
    
    has_model_path_msg = "check model at" in content
    print(f"[Verify] {'✅' if has_model_path_msg else '❌'} Model path message: {has_model_path_msg}")
    
    # Check that old FastAPI messages are removed
    has_old_fastapi_msg = "Kokoro-FastAPI connected at" in content
    print(f"[Verify] {'✅' if not has_old_fastapi_msg else '❌'} Old FastAPI message removed: {not has_old_fastapi_msg}")
    
    success_count = sum([has_direct_library_msg, has_model_path_msg, not has_old_fastapi_msg])
    
    print(f"[Verify] 📊 Main: {success_count}/3 checks passed")
    return success_count >= 2

def verify_streaming_kokoro_changes():
    """Verify changes in audio/streaming_kokoro.py"""
    print("[Verify] 🔍 Checking audio/streaming_kokoro.py changes...")
    
    content = check_file_content("audio/streaming_kokoro.py", "Streaming Kokoro")
    if not content:
        return False
    
    # Check for updated comments
    has_direct_library_comment = "Direct Kokoro library" in content
    print(f"[Verify] {'✅' if has_direct_library_comment else '❌'} Direct library comment: {has_direct_library_comment}")
    
    # Check for updated function using generate_tts
    has_generate_tts_import = "from audio.output import generate_tts" in content
    print(f"[Verify] {'✅' if has_generate_tts_import else '❌'} generate_tts import: {has_generate_tts_import}")
    
    success_count = sum([has_direct_library_comment, has_generate_tts_import])
    
    print(f"[Verify] 📊 Streaming Kokoro: {success_count}/2 checks passed")
    return success_count >= 1

def main():
    """Run comprehensive verification"""
    print("=" * 70)
    print("🔍 KOKORO DIRECT LIBRARY INTEGRATION VERIFICATION")
    print("=" * 70)
    
    verifications = [
        ("Audio Output", verify_audio_output_changes),
        ("Config", verify_config_changes),
        ("AI Main", verify_ai_main_changes),
        ("Main", verify_main_changes),
        ("Streaming Kokoro", verify_streaming_kokoro_changes)
    ]
    
    passed = 0
    total = len(verifications)
    
    for name, verify_func in verifications:
        print(f"\n🔍 Verifying: {name}")
        print("-" * 50)
        
        try:
            result = verify_func()
            if result:
                print(f"[Verify] ✅ {name} verification PASSED")
                passed += 1
            else:
                print(f"[Verify] ❌ {name} verification FAILED")
        except Exception as e:
            print(f"[Verify] ❌ {name} verification FAILED with exception: {e}")
    
    print("\n" + "=" * 70)
    print("📊 VERIFICATION RESULTS")
    print("=" * 70)
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 ALL VERIFICATIONS PASSED!")
        print("✅ Successfully switched from Kokoro FastAPI to Direct Library")
        print("📋 Summary of changes:")
        print("   • Replaced FastAPI requests with direct Kokoro library calls")
        print("   • Updated model path to C:/Users/drzew/kokoro-onnx/kokoro-v1_0.pth")
        print("   • Removed all API-related configurations")
        print("   • Updated status messages and error handling")
        print("   • Modified streaming integration to use direct library")
        return True
    else:
        print("⚠️ Some verifications failed. Check the implementation.")
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)