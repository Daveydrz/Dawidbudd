"""
Smart Streaming Audio Output - Fixed Kokoro timing to prevent shutdown
Created: 2025-01-17
Purpose: Implement smart chunk accumulation to prevent overwhelming Kokoro
Features: 30-50% token threshold, batch processing, anti-overwhelm protection
"""

import threading
import time
import queue
import requests
from typing import List, Optional

# Try to import config, fallback to defaults
try:
    from config import KOKORO_API_BASE_URL, KOKORO_DEFAULT_VOICE
except ImportError:
    KOKORO_API_BASE_URL = "http://127.0.0.1:8880"
    KOKORO_DEFAULT_VOICE = "af_heart"

class SmartStreamingOutput:
    """Smart streaming output that accumulates chunks before sending to Kokoro"""
    
    def __init__(self):
        self.chunk_buffer = []
        self.buffer_lock = threading.Lock()
        self.token_count = 0
        self.estimated_total_tokens = 0
        self.speech_started = False
        self.last_speech_time = 0
        self.min_speech_interval = 1.0  # Minimum 1 second between Kokoro calls
        
        # Kokoro session
        self.session = requests.Session()
        
        print("[SmartStreaming] 🎵 Smart streaming output initialized")
    
    def reset_for_new_response(self):
        """Reset state for new response generation"""
        with self.buffer_lock:
            self.chunk_buffer = []
            self.token_count = 0
            self.estimated_total_tokens = 0
            self.speech_started = False
        print("[SmartStreaming] 🔄 Reset for new response")
    
    def add_chunk(self, chunk: str, is_final: bool = False) -> bool:
        """
        Add chunk to buffer and decide when to send to Kokoro
        Returns True if speech was triggered
        """
        with self.buffer_lock:
            if not chunk or not chunk.strip():
                return False
            
            self.chunk_buffer.append(chunk.strip())
            self.token_count += len(chunk.split())
            
            # Estimate total tokens on first few chunks
            if len(self.chunk_buffer) <= 3:
                self.estimated_total_tokens = max(self.estimated_total_tokens, self.token_count * 6)
            
            print(f"[SmartStreaming] 📝 Added chunk (tokens: {self.token_count}/{self.estimated_total_tokens})")
            
            # Decide when to start speaking
            should_speak = self._should_start_speaking(is_final)
            
            if should_speak:
                # Send accumulated chunks to Kokoro
                accumulated_text = " ".join(self.chunk_buffer)
                self.chunk_buffer = []  # Clear buffer after sending
                
                # Speak in background thread to avoid blocking
                threading.Thread(
                    target=self._speak_text_smart,
                    args=(accumulated_text,),
                    daemon=True
                ).start()
                
                self.speech_started = True
                return True
                
            return False
    
    def _should_start_speaking(self, is_final: bool) -> bool:
        """Determine if we should start speaking based on smart criteria"""
        
        # Always speak if it's the final chunk and we haven't started yet
        if is_final and not self.speech_started:
            print("[SmartStreaming] 🎵 Final chunk - forcing speech")
            return True
        
        # Don't overwhelm Kokoro - respect minimum interval
        time_since_last = time.time() - self.last_speech_time
        if time_since_last < self.min_speech_interval:
            print(f"[SmartStreaming] ⏸️ Too soon since last speech ({time_since_last:.1f}s)")
            return False
        
        # If we haven't started speaking yet, wait for 30-50% of estimated tokens
        if not self.speech_started:
            if self.estimated_total_tokens > 0:
                token_percentage = self.token_count / self.estimated_total_tokens
                print(f"[SmartStreaming] 📊 Token progress: {token_percentage:.1%}")
                
                if token_percentage >= 0.3:  # 30% threshold
                    print("[SmartStreaming] 🎵 Reached 30% token threshold - starting speech")
                    return True
            else:
                # Fallback: start after 10 tokens if no estimate
                if self.token_count >= 10:
                    print("[SmartStreaming] 🎵 Reached 10 token fallback - starting speech")
                    return True
        
        # If speech has already started, send chunks in batches
        if self.speech_started:
            # Send every 15-20 tokens to maintain flow without overwhelming
            if self.token_count >= 15:
                print("[SmartStreaming] 🎵 Continuing speech - batch ready")
                return True
        
        return False
    
    def _speak_text_smart(self, text: str):
        """Send text to Kokoro with anti-overwhelm protection"""
        try:
            self.last_speech_time = time.time()
            
            print(f"[SmartStreaming] 🎵 Sending to Kokoro: '{text[:50]}...' ({len(text)} chars)")
            
            # Call Kokoro API
            payload = {
                "input": text,
                "voice": KOKORO_DEFAULT_VOICE,
                "response_format": "wav"
            }
            
            response = self.session.post(
                f"{KOKORO_API_BASE_URL}/v1/audio/speech",
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                # Play the audio (simplified - you'd integrate with your audio system)
                print(f"[SmartStreaming] ✅ Kokoro speech generated successfully")
                # Here you would integrate with your actual audio playback system
                self._play_audio_data(response.content)
            else:
                print(f"[SmartStreaming] ❌ Kokoro error: {response.status_code}")
                
        except Exception as e:
            print(f"[SmartStreaming] ❌ Error sending to Kokoro: {e}")
    
    def _play_audio_data(self, audio_data: bytes):
        """Play audio data (placeholder - integrate with your audio system)"""
        # This would integrate with your existing audio playback system
        print(f"[SmartStreaming] 🔊 Playing audio ({len(audio_data)} bytes)")
        
    def finalize_response(self):
        """Send any remaining chunks to Kokoro"""
        with self.buffer_lock:
            if self.chunk_buffer:
                remaining_text = " ".join(self.chunk_buffer)
                print(f"[SmartStreaming] 🎵 Finalizing with remaining chunks: '{remaining_text[:50]}...'")
                
                threading.Thread(
                    target=self._speak_text_smart,
                    args=(remaining_text,),
                    daemon=True
                ).start()
                
                self.chunk_buffer = []

# Global instance
smart_streaming_output = SmartStreamingOutput()

def speak_streaming_smart(chunk: str, is_final: bool = False) -> bool:
    """
    Smart streaming speech that prevents Kokoro overwhelm
    """
    return smart_streaming_output.add_chunk(chunk, is_final)

def reset_streaming_output():
    """Reset streaming output for new response"""
    smart_streaming_output.reset_for_new_response()

def finalize_streaming_output():
    """Finalize streaming output"""
    smart_streaming_output.finalize_response()

if __name__ == "__main__":
    # Test the smart streaming output
    print("🧪 Testing Smart Streaming Output:")
    
    # Simulate streaming chunks
    test_chunks = [
        "Hello there,",
        "I'm Buddy",
        "and I'm here",
        "to help you",
        "with whatever",
        "you need today.",
        "How can I",
        "assist you?"
    ]
    
    reset_streaming_output()
    
    for i, chunk in enumerate(test_chunks):
        is_final = (i == len(test_chunks) - 1)
        spoke = speak_streaming_smart(chunk, is_final)
        print(f"Chunk '{chunk}' -> Spoke: {spoke}")
        time.sleep(0.1)  # Simulate streaming delay
    
    finalize_streaming_output()
    time.sleep(2)  # Allow audio to finish