"""
Mock simpleaudio module for testing purposes
"""
import numpy as np
import time

class MockWaveObject:
    """Mock wave object for testing"""
    
    def __init__(self, audio_data, sample_rate=44100, num_channels=1):
        self.audio_data = audio_data
        self.sample_rate = sample_rate
        self.num_channels = num_channels
        self.is_playing = False
    
    def play(self):
        """Mock play function"""
        self.is_playing = True
        return MockPlayObject(self)
    
    def wait_done(self):
        """Mock wait done function"""
        time.sleep(0.1)  # Simulate brief playback
        self.is_playing = False

class MockPlayObject:
    """Mock play object for testing"""
    
    def __init__(self, wave_object):
        self.wave_object = wave_object
        self._is_playing = True
    
    def wait_done(self):
        """Mock wait done function"""
        time.sleep(0.1)  # Simulate brief playback
        self._is_playing = False
        self.wave_object.is_playing = False
    
    def stop(self):
        """Mock stop function"""
        self._is_playing = False
        self.wave_object.is_playing = False
    
    def is_playing(self):
        """Mock is playing check"""
        return self._is_playing

def play_buffer(audio_data, num_channels=1, bytes_per_sample=2, sample_rate=44100):
    """Mock play buffer function"""
    wave_obj = MockWaveObject(audio_data, sample_rate, num_channels)
    return wave_obj.play()

# Mock the main functions
WaveObject = MockWaveObject