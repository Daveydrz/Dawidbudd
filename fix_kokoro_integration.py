#!/usr/bin/env python3
"""
Fix Kokoro Integration Script
This script provides instructions and diagnostics to fix the Kokoro voice issue.
"""

import os
import sys

def check_kokoro_installation():
    """Check if Kokoro and dependencies are installed"""
    print("🔍 Checking Kokoro Installation Status")
    print("=" * 50)
    
    # Check kokoro library
    try:
        import kokoro
        print("✅ kokoro library: INSTALLED")
        kokoro_available = True
    except ImportError:
        print("❌ kokoro library: NOT INSTALLED")
        kokoro_available = False
    
    # Check KPipeline specifically
    try:
        from kokoro import KPipeline
        print("✅ KPipeline class: AVAILABLE")
        kpipeline_available = True
    except ImportError:
        print("❌ KPipeline class: NOT AVAILABLE")
        kpipeline_available = False
    
    # Check soundfile
    try:
        import soundfile
        print("✅ soundfile: INSTALLED")
        soundfile_available = True
    except ImportError:
        print("❌ soundfile: NOT INSTALLED")
        soundfile_available = False
    
    # Check simpleaudio
    try:
        import simpleaudio
        print("✅ simpleaudio: INSTALLED")
        simpleaudio_available = True
    except ImportError:
        print("❌ simpleaudio: NOT INSTALLED")
        simpleaudio_available = False
    
    return kokoro_available, kpipeline_available, soundfile_available, simpleaudio_available

def check_model_files():
    """Check if the Kokoro model files exist"""
    print("\n🔍 Checking Kokoro Model Files")
    print("=" * 50)
    
    # Check the configured model path from config.py
    model_paths_to_check = [
        "C:/Users/drzew/kokoro/kokoro/voices/kokoro-v1_0.pth",
        "C:/Users/drzew/kokoro-onnx/kokoro-v1_0.pth",
        "./kokoro-v1_0.pth",
        "./models/kokoro-v1_0.pth"
    ]
    
    for path in model_paths_to_check:
        if os.path.exists(path):
            print(f"✅ Model file found: {path}")
            return True
        else:
            print(f"❌ Model file not found: {path}")
    
    return False

def show_installation_instructions():
    """Show step-by-step installation instructions"""
    print("\n📋 Installation Instructions")
    print("=" * 50)
    
    print("To fix the Kokoro voice issue, follow these steps:")
    print()
    
    print("1. Install required Python packages:")
    print("   pip install kokoro soundfile simpleaudio")
    print()
    
    print("2. If simpleaudio installation fails on Linux, install system dependencies:")
    print("   sudo apt-get update")
    print("   sudo apt-get install libasound2-dev")
    print("   pip install simpleaudio")
    print()
    
    print("3. For Windows, if you get compilation errors:")
    print("   pip install simpleaudio --only-binary=all")
    print()
    
    print("4. Alternative audio playback (if simpleaudio fails):")
    print("   pip install pygame")
    print("   pip install pydub")
    print()
    
    print("5. Verify installation:")
    print("   python -c \"from kokoro import KPipeline; print('Kokoro installed successfully')\"")
    print()

def show_working_test_example():
    """Show the working test example that should be replicated"""
    print("\n🧪 Working Test Example (Your Pattern)")
    print("=" * 50)
    
    working_code = '''
from kokoro import KPipeline
import soundfile as sf
import os
import simpleaudio as sa

pipeline = KPipeline(lang_code='a')

text = "This is a test of Kokoro TTS using the af_bella voice model running locally."
generator = pipeline(text, voice='af_bella')

for i, (gs, ps, audio) in enumerate(generator):
    print(f"Chunk {i}")
    print("Text:", gs)
    print("Phonemes:", ps)
    
    out_path = f"chunk_{i}.wav"
    sf.write(out_path, audio, 24000)

    # Play the audio automatically
    wave_obj = sa.WaveObject.from_wave_file(out_path)
    play_obj = wave_obj.play()
    play_obj.wait_done()
'''
    
    print("This is your working pattern that needs to be replicated:")
    print(working_code)

def show_current_status():
    """Show what's been fixed in the current implementation"""
    print("\n✅ What's Already Fixed")
    print("=" * 50)
    
    print("1. ✅ Updated audio/output.py to handle missing dependencies gracefully")
    print("2. ✅ Updated voice/manager.py to handle missing dependencies gracefully")
    print("3. ✅ Added proper error messages with installation instructions")
    print("4. ✅ Implemented fallback behavior when Kokoro is not available")
    print("5. ✅ Updated code to match your working test pattern exactly")
    print()
    
    print("📝 Key Changes Made:")
    print("- Separated import checks for kokoro, soundfile, and simpleaudio")
    print("- Added graceful fallbacks when libraries are missing")
    print("- Updated generator pattern to match your working test")
    print("- Added proper error messages with installation instructions")
    print("- Fixed audio chunk handling to match working pattern")

def create_test_script():
    """Create a simple test script to verify the fix"""
    test_script = '''#!/usr/bin/env python3
"""
Simple test to verify Kokoro integration after installation
"""

def test_kokoro_basic():
    print("🧪 Testing Basic Kokoro Functionality")
    print("=" * 40)
    
    try:
        from kokoro import KPipeline
        print("✅ KPipeline imported successfully")
    except ImportError as e:
        print(f"❌ KPipeline import failed: {e}")
        return False
    
    try:
        pipeline = KPipeline(lang_code='a')
        print("✅ KPipeline initialized")
    except Exception as e:
        print(f"❌ KPipeline initialization failed: {e}")
        return False
    
    try:
        text = "Hello, this is a test."
        generator = pipeline(text, voice='af_bella')
        
        audio_chunks = []
        for i, (gs, ps, audio) in enumerate(generator):
            print(f"✅ Generated chunk {i}: {len(audio)} samples")
            audio_chunks.append(audio)
        
        if audio_chunks:
            print(f"✅ Total chunks generated: {len(audio_chunks)}")
            return True
        else:
            print("❌ No audio chunks generated")
            return False
            
    except Exception as e:
        print(f"❌ Audio generation failed: {e}")
        return False

if __name__ == "__main__":
    success = test_kokoro_basic()
    if success:
        print("🎉 Kokoro integration test passed!")
    else:
        print("💡 Run: pip install kokoro soundfile simpleaudio")
'''
    
    with open("test_kokoro_simple.py", "w") as f:
        f.write(test_script)
    
    print(f"\n📄 Created test script: test_kokoro_simple.py")
    print("Run this after installing dependencies: python test_kokoro_simple.py")

def main():
    print("🔧 Kokoro Integration Fix Diagnostics")
    print("=" * 60)
    
    # Check current installation status
    kokoro_ok, kpipeline_ok, soundfile_ok, simpleaudio_ok = check_kokoro_installation()
    
    # Check model files
    model_ok = check_model_files()
    
    # Show what needs to be done
    if not kokoro_ok:
        show_installation_instructions()
    
    # Show the working pattern
    show_working_test_example()
    
    # Show what's already been fixed
    show_current_status()
    
    # Create test script
    create_test_script()
    
    print("\n🎯 Next Steps:")
    print("=" * 20)
    
    if not kokoro_ok:
        print("1. Install missing dependencies using the commands above")
        print("2. Run the test script: python test_kokoro_simple.py")
        print("3. Test Buddy's voice response")
    else:
        print("1. Run the test script: python test_kokoro_simple.py")
        print("2. Check if model files exist at the configured path")
        print("3. Test Buddy's voice response")
    
    print("\n💡 The code has been updated to handle missing dependencies gracefully.")
    print("💡 Once you install the kokoro library, voice should work automatically!")

if __name__ == "__main__":
    main()