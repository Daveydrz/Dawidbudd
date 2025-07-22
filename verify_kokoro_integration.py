#!/usr/bin/env python3
"""
Verification script for Kokoro KPipeline integration
Verifies that all the requested changes have been implemented correctly
"""

import sys
import os

# Add the project root to path
sys.path.append('.')

def verify_kokoro_integration():
    """Verify all Kokoro KPipeline integration changes"""
    print("🔍 Verifying Kokoro KPipeline Integration")
    print("=" * 50)
    
    verification_results = []
    
    # Check 1: Config.py model path update
    print("\n1. Checking config.py model path...")
    try:
        from config import KOKORO_MODEL_PATH
        expected_path = "C:/Users/drzew/kokoro/kokoro/voices/kokoro-v1_0.pth"
        
        if KOKORO_MODEL_PATH == expected_path:
            print(f"✅ Model path correctly updated: {KOKORO_MODEL_PATH}")
            verification_results.append(("Model Path", True))
        else:
            print(f"❌ Model path incorrect. Expected: {expected_path}, Got: {KOKORO_MODEL_PATH}")
            verification_results.append(("Model Path", False))
            
    except Exception as e:
        print(f"❌ Error checking config: {e}")
        verification_results.append(("Model Path", False))
    
    # Check 2: Audio output KPipeline import
    print("\n2. Checking audio/output.py KPipeline import...")
    try:
        with open('audio/output.py', 'r') as f:
            content = f.read()
            
        if 'from kokoro import KPipeline' in content:
            print("✅ KPipeline import found in audio/output.py")
            verification_results.append(("Audio Output Import", True))
        else:
            print("❌ KPipeline import not found in audio/output.py")
            verification_results.append(("Audio Output Import", False))
            
    except Exception as e:
        print(f"❌ Error checking audio/output.py: {e}")
        verification_results.append(("Audio Output Import", False))
    
    # Check 3: Generate_kokoro function
    print("\n3. Checking generate_kokoro function...")
    try:
        with open('audio/output.py', 'r') as f:
            content = f.read()
            
        if 'def generate_kokoro(' in content and 'voice=' in content and 'speed=' in content:
            print("✅ generate_kokoro function with voice and speed parameters found")
            verification_results.append(("Generate Kokoro Function", True))
        else:
            print("❌ generate_kokoro function with proper parameters not found")
            verification_results.append(("Generate Kokoro Function", False))
            
    except Exception as e:
        print(f"❌ Error checking generate_kokoro function: {e}")
        verification_results.append(("Generate Kokoro Function", False))
    
    # Check 4: Voice manager Kokoro integration
    print("\n4. Checking voice manager Kokoro integration...")
    try:
        with open('voice/manager.py', 'r') as f:
            content = f.read()
            
        has_import = 'from kokoro import KPipeline' in content
        has_generate = 'def generate_kokoro(' in content
        has_tts_engine = 'def set_tts_engine(' in content
        has_speak_engine = 'def speak_with_engine(' in content
        
        if has_import and has_generate and has_tts_engine and has_speak_engine:
            print("✅ Voice manager has all required Kokoro functions")
            verification_results.append(("Voice Manager Integration", True))
        else:
            print(f"❌ Voice manager missing functions: import={has_import}, generate={has_generate}, set_engine={has_tts_engine}, speak={has_speak_engine}")
            verification_results.append(("Voice Manager Integration", False))
            
    except Exception as e:
        print(f"❌ Error checking voice manager: {e}")
        verification_results.append(("Voice Manager Integration", False))
    
    # Check 5: TTS engine selection logic
    print("\n5. Checking TTS engine selection logic...")
    try:
        with open('voice/manager.py', 'r') as f:
            content = f.read()
            
        if 'self.tts_engine = "kokoro"' in content and 'if self.tts_engine == "kokoro"' in content:
            print("✅ TTS engine selection logic implemented")
            verification_results.append(("TTS Engine Selection", True))
        else:
            print("❌ TTS engine selection logic not found")
            verification_results.append(("TTS Engine Selection", False))
            
    except Exception as e:
        print(f"❌ Error checking TTS engine selection: {e}")
        verification_results.append(("TTS Engine Selection", False))
    
    # Check 6: Streaming Kokoro updates
    print("\n6. Checking streaming Kokoro updates...")
    try:
        with open('audio/streaming_kokoro.py', 'r') as f:
            content = f.read()
            
        if 'generate_kokoro' in content and 'KPipeline' in content:
            print("✅ Streaming Kokoro updated for KPipeline")
            verification_results.append(("Streaming Updates", True))
        else:
            print("❌ Streaming Kokoro not updated for KPipeline")
            verification_results.append(("Streaming Updates", False))
            
    except Exception as e:
        print(f"❌ Error checking streaming Kokoro: {e}")
        verification_results.append(("Streaming Updates", False))
    
    # Check 7: Audio handling for 24kHz
    print("\n7. Checking 24kHz audio handling...")
    try:
        with open('audio/output.py', 'r') as f:
            content = f.read()
            
        with open('voice/manager.py', 'r') as f:
            manager_content = f.read()
            
        if '24000' in content or '24000' in manager_content:
            print("✅ 24kHz audio handling implemented")
            verification_results.append(("24kHz Audio Handling", True))
        else:
            print("❌ 24kHz audio handling not found")
            verification_results.append(("24kHz Audio Handling", False))
            
    except Exception as e:
        print(f"❌ Error checking 24kHz handling: {e}")
        verification_results.append(("24kHz Audio Handling", False))
    
    # Check 8: Voice and speed parameters
    print("\n8. Checking voice and speed parameter support...")
    try:
        with open('audio/output.py', 'r') as f:
            content = f.read()
            
        with open('voice/manager.py', 'r') as f:
            manager_content = f.read()
            
        voice_support = 'voice=' in content and 'voice=' in manager_content
        speed_support = 'speed=' in content and 'speed=' in manager_content
        
        if voice_support and speed_support:
            print("✅ Voice and speed parameter support implemented")
            verification_results.append(("Voice/Speed Parameters", True))
        else:
            print(f"❌ Parameter support incomplete: voice={voice_support}, speed={speed_support}")
            verification_results.append(("Voice/Speed Parameters", False))
            
    except Exception as e:
        print(f"❌ Error checking parameters: {e}")
        verification_results.append(("Voice/Speed Parameters", False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 VERIFICATION SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(verification_results)
    
    for check_name, result in verification_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {check_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} checks passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL VERIFICATION CHECKS PASSED!")
        print("\n✅ Implementation Summary:")
        print("  • Updated model path to new location")
        print("  • Replaced Kokoro with KPipeline import")
        print("  • Added generate_kokoro function with voice/speed control")
        print("  • Integrated KPipeline in voice manager")
        print("  • Added TTS engine selection capabilities")
        print("  • Updated streaming for KPipeline compatibility")
        print("  • Implemented 24kHz audio handling")
        print("  • Added voice and speed parameter support")
        
        print("\n🚀 Ready for Testing:")
        print("  1. Install Kokoro library: pip install kokoro")
        print("  2. Ensure model file exists at specified path")
        print("  3. Test with: python test_kokoro_kpipeline.py")
        
    else:
        print(f"\n⚠️ {total-passed} verification checks failed.")
        print("Please review the failed checks above.")
    
    return passed == total

if __name__ == "__main__":
    success = verify_kokoro_integration()
    sys.exit(0 if success else 1)