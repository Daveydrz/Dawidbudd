# Mock audio system for testing
import time
import threading

class MockAudioSystem:
    def __init__(self):
        self.is_speaking = False
        
    def speak_streaming(self, text):
        """Mock speak_streaming function"""
        print(f"[MockAudio] 🎵 Speaking: '{text}'")
        self.is_speaking = True
        
        # Simulate speaking time
        def simulate_speech():
            time.sleep(len(text) * 0.05)  # Simulate speech duration
            self.is_speaking = False
            print(f"[MockAudio] ✅ Finished speaking")
        
        threading.Thread(target=simulate_speech, daemon=True).start()
        return True
    
    def test_kokoro_api(self):
        """Mock Kokoro API test"""
        print("[MockAudio] ⚠️ Using mock Kokoro (no real audio server)")
        return False
    
    def start_audio_worker(self):
        """Mock audio worker start"""
        print("[MockAudio] 🚀 Mock audio worker started")
        
    def is_buddy_talking(self):
        return self.is_speaking

# Global mock instance
mock_audio = MockAudioSystem()

# Mock functions to replace the real ones
def speak_streaming(text):
    return mock_audio.speak_streaming(text)

def test_kokoro_api():
    return mock_audio.test_kokoro_api()

def start_audio_worker():
    return mock_audio.start_audio_worker()

def is_buddy_talking():
    return mock_audio.is_buddy_talking()

print("[MockAudio] 🎭 Mock audio system loaded")
