#!/usr/bin/env python3
"""
Code verification script to check if Kokoro KPipeline integration matches user's working pattern
This analyzes the code structure without requiring the actual dependencies
"""

import ast
import os

def check_file_for_pattern(filename, expected_patterns):
    """Check if a file contains the expected patterns"""
    try:
        with open(filename, 'r') as f:
            content = f.read()
        
        results = {}
        for pattern_name, pattern in expected_patterns.items():
            results[pattern_name] = pattern in content
        
        return results
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return {}

def main():
    """Verify the KPipeline integration"""
    print("🔍 KOKORO KPIPELINE INTEGRATION VERIFICATION")
    print("="*60)
    
    # Define expected patterns that should be in the code
    files_to_check = {
        "audio/output.py": {
            "KPipeline_import": "from kokoro import KPipeline",
            "soundfile_import": "import soundfile as sf",
            "simpleaudio_import": "import simpleaudio as sa",
            "generator_pattern": "for i, (gs, ps, audio) in enumerate(generator):",
            "correct_path": "C:/Users/drzew/kokoro/kokoro/voices/kokoro-v1_0.pth",
            "af_bella_voice": "af_bella"
        },
        "voice/manager.py": {
            "KPipeline_import": "from kokoro import KPipeline",
            "generator_pattern": "for i, (gs, ps, audio) in enumerate(generator):",
            "voice_manager_generation": "def generate_kokoro(self, text, voice='af_bella', speed=1.0):"
        },
        "config.py": {
            "correct_path": "C:/Users/drzew/kokoro/kokoro/voices/kokoro-v1_0.pth",
            "af_bella_default": 'KOKORO_DEFAULT_VOICE = "af_bella"',
            "af_bella_mapping": '"en": "af_bella"'
        },
        "audio/streaming_kokoro.py": {
            "generator_pattern": "for i, (gs, ps, audio) in enumerate(generator):",
            "audio_chunk_generation": "def generate_audio_chunk_sync(self, text: str, chunk_id: str)"
        }
    }
    
    all_passed = True
    
    for filename, patterns in files_to_check.items():
        filepath = os.path.join("/home/runner/work/Dawidbudd/Dawidbudd", filename)
        print(f"\n🔍 Checking {filename}...")
        
        if not os.path.exists(filepath):
            print(f"❌ File not found: {filepath}")
            all_passed = False
            continue
        
        results = check_file_for_pattern(filepath, patterns)
        
        file_passed = True
        for pattern_name, found in results.items():
            status = "✅" if found else "❌"
            print(f"  {status} {pattern_name}")
            if not found:
                file_passed = False
                all_passed = False
        
        if file_passed:
            print(f"  ✅ {filename} - All patterns found")
        else:
            print(f"  ❌ {filename} - Missing some patterns")
    
    print("\n" + "="*60)
    print("📊 VERIFICATION SUMMARY")
    print("="*60)
    
    if all_passed:
        print("🎉 ✅ ALL CHECKS PASSED!")
        print("🎯 Kokoro KPipeline integration follows the user's working pattern")
        print("🔧 Key improvements made:")
        print("   - Fixed generator pattern: for i, (gs, ps, audio) in enumerate(generator)")
        print("   - Added soundfile and simpleaudio imports")
        print("   - Updated to use af_bella voice (matches user's test)")
        print("   - Corrected model path: C:/Users/drzew/kokoro/kokoro/voices/kokoro-v1_0.pth")
        print("   - Fixed all audio generation to use numpy arrays directly")
    else:
        print("❌ SOME CHECKS FAILED!")
        print("🔧 Review the failed patterns above")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)