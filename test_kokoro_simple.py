#!/usr/bin/env python3
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
