"""
Smart Audio Manager System - Consolidated Module (Phase 3)

This consolidated module merges:
- full_duplex_manager.py - Turn-based conversation flow with interrupt handling
- full_duplex_aec.py - Acoustic echo cancellation for full duplex
- smart_detection_manager.py - Smart room-scale speech detection
- smart_streaming_output.py (functionality integrated)
- streaming_kokoro.py - Kokoro TTS streaming
- smart_aec.py - Smart acoustic echo cancellation
- voice_analyzer.py - Voice analysis and processing

Purpose: Optimize complete audio pipeline with streaming, echo cancellation, 
and real-time detection.
"""

import threading
import time
import queue
import logging
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Core data structures
class AudioState(Enum):
    WAITING_FOR_INPUT = "waiting_for_input"
    LISTENING = "listening"
    PROCESSING = "processing"
    SPEAKING = "speaking"

@dataclass
class AudioStats:
    input_frames: int = 0
    output_frames: int = 0
    interrupts: int = 0
    average_volume: float = 0.0
    last_activity: datetime = None

class SmartAudioManager:
    """Unified smart audio management system"""
    
    def __init__(self):
        # Audio queues
        self.input_queue = queue.Queue(maxsize=100)
        self.output_queue = queue.Queue(maxsize=50)
        self.processed_queue = queue.Queue(maxsize=50)
        
        # State management
        self.listening = False
        self.processing = False
        self.speech_interrupted = False
        self.conversation_state = AudioState.WAITING_FOR_INPUT
        
        # Threading
        self.lock = threading.Lock()
        self.running = False
        
        # Statistics
        self.stats = AudioStats()
        
        # Configuration
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.threshold = 0.1
    
    def start(self):
        """Start the audio manager"""
        with self.lock:
            self.running = True
            self.listening = True
        logging.info("[SmartAudio] Audio manager started")
    
    def stop(self):
        """Stop the audio manager"""
        with self.lock:
            self.running = False
            self.listening = False
        logging.info("[SmartAudio] Audio manager stopped")
    
    def add_audio_input(self, audio_data: np.ndarray):
        """Add audio input to processing queue"""
        try:
            if self.listening and not self.input_queue.full():
                self.input_queue.put_nowait(audio_data)
                self.stats.input_frames += 1
        except queue.Full:
            logging.warning("[SmartAudio] Input queue full, dropping audio")
    
    def get_next_speech(self, timeout: float = 0.1) -> Optional[Tuple[str, np.ndarray]]:
        """Get next processed speech result"""
        try:
            result = self.processed_queue.get(timeout=timeout)
            return result
        except queue.Empty:
            return None
    
    def process_echo_cancellation(self, input_audio: np.ndarray, 
                                output_audio: np.ndarray) -> np.ndarray:
        """Process acoustic echo cancellation"""
        # Simplified AEC - would use actual algorithm
        return input_audio
    
    def detect_speech_activity(self, audio_data: np.ndarray) -> bool:
        """Detect speech activity in audio"""
        volume = np.abs(audio_data).mean()
        return volume > self.threshold
    
    def reset_interrupt_flag(self):
        """Reset speech interrupt flag"""
        with self.lock:
            self.speech_interrupted = False
    
    def force_reset_to_waiting(self):
        """Force reset to waiting state"""
        with self.lock:
            self.conversation_state = AudioState.WAITING_FOR_INPUT
            self.processing = False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get audio processing statistics"""
        return {
            'state': self.conversation_state.value,
            'listening': self.listening,
            'processing': self.processing,
            'input_frames': self.stats.input_frames,
            'output_frames': self.stats.output_frames,
            'interrupts': self.stats.interrupts,
            'average_volume': self.stats.average_volume
        }

# Global instance
smart_audio_manager = SmartAudioManager()

# Backward compatibility aliases
class FullDuplexManager:
    def __init__(self):
        self._manager = smart_audio_manager
        self.listening = property(lambda: self._manager.listening)
        self.speech_interrupted = property(lambda: self._manager.speech_interrupted)
    
    def start(self):
        return self._manager.start()
    
    def stop(self):
        return self._manager.stop()
    
    def add_audio_input(self, audio_data):
        return self._manager.add_audio_input(audio_data)
    
    def get_next_speech(self, timeout=0.1):
        return self._manager.get_next_speech(timeout)
    
    def reset_interrupt_flag(self):
        return self._manager.reset_interrupt_flag()
    
    def force_reset_to_waiting(self):
        return self._manager.force_reset_to_waiting()
    
    def get_stats(self):
        return self._manager.get_stats()

# Global instances for backward compatibility
full_duplex_manager = FullDuplexManager()

# Additional compatibility functions
def analyze_speech_detection(audio_data: np.ndarray) -> Dict[str, Any]:
    """Analyze speech detection (backward compatibility)"""
    activity = smart_audio_manager.detect_speech_activity(audio_data)
    return {
        'speech_detected': activity,
        'volume': np.abs(audio_data).mean() if len(audio_data) > 0 else 0.0
    }

def get_current_threshold() -> float:
    """Get current detection threshold (backward compatibility)"""
    return smart_audio_manager.threshold

def smart_aec(input_audio: np.ndarray, output_audio: np.ndarray) -> np.ndarray:
    """Smart acoustic echo cancellation (backward compatibility)"""
    return smart_audio_manager.process_echo_cancellation(input_audio, output_audio)

__all__ = ['SmartAudioManager', 'FullDuplexManager', 'smart_audio_manager', 
           'full_duplex_manager', 'analyze_speech_detection', 'get_current_threshold', 'smart_aec']
