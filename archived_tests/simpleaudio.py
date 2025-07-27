# Mock simpleaudio for testing
class MockPlayObject:
    def __init__(self):
        self._playing = True
    
    def is_playing(self):
        return self._playing
    
    def stop(self):
        self._playing = False

def play_buffer(audio_data, num_channels, bytes_per_sample, sample_rate):
    print(f"[MockAudio] Would play audio: {len(audio_data)} bytes, {sample_rate}Hz")
    return MockPlayObject()