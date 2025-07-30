"""
Smart Audio Manager - Consolidated Audio Processing System
==========================================================

This module consolidates 7 audio processing components into a unified system:
1. input.py: Full duplex audio input with voice activity detection
2. output.py: Streaming audio output with Kokoro-FastAPI integration  
3. aec.py: Acoustic Echo Cancellation system
4. full_duplex_aec.py: Advanced full duplex AEC processing
5. full_duplex_manager.py: Full duplex audio management
6. processing.py: Audio processing utilities and filters
7. smart_streaming_output.py: Smart chunk accumulation for TTS

The unified system provides comprehensive audio processing capabilities with
real-time input/output, echo cancellation, and intelligent streaming.
"""

import threading
import time
import queue
import json
import logging
import os
import tempfile
import io
import random
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# Safe import handling
def safe_import(module_name, fallback=None):
    """Safely import modules with fallback"""
    try:
        return __import__(module_name)
    except ImportError as e:
        logging.warning(f"Could not import {module_name}: {e}")
        return fallback

# Try core audio imports with fallbacks
try:
    import sounddevice as sd
    SOUNDDEVICE_AVAILABLE = True
except ImportError:
    SOUNDDEVICE_AVAILABLE = False
    logging.warning("sounddevice not available - audio will be limited")

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    logging.warning("NumPy not available - audio processing will be limited")

try:
    from scipy.signal import resample_poly
    from scipy.io.wavfile import write
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    logging.warning("SciPy not available - using basic audio processing")

try:
    import simpleaudio as sa
    SIMPLEAUDIO_AVAILABLE = True
except ImportError:
    SIMPLEAUDIO_AVAILABLE = False
    logging.warning("simpleaudio not available - using fallback playback")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    logging.warning("requests not available - TTS will be limited")

try:
    from pyaec import PyAec
    PYAEC_AVAILABLE = True
except ImportError:
    PYAEC_AVAILABLE = False
    logging.warning("PyAEC not available - using mock echo cancellation")

try:
    from langdetect import detect as detect_language
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False
    logging.warning("langdetect not available - using fallback language detection")
    def detect_language(text):
        return 'en'

# Configuration imports with fallbacks
try:
    from config import (
        DEBUG, SAMPLE_RATE, MIC_SAMPLE_RATE, MIC_DEVICE_INDEX,
        FULL_DUPLEX_MODE, KOKORO_API_BASE_URL, KOKORO_DEFAULT_VOICE,
        KOKORO_TIMEOUT, BUDDY_INTERRUPT_THRESHOLD
    )
except ImportError:
    DEBUG = True
    SAMPLE_RATE = 16000
    MIC_SAMPLE_RATE = 16000
    MIC_DEVICE_INDEX = None
    FULL_DUPLEX_MODE = True
    KOKORO_API_BASE_URL = "http://127.0.0.1:8880"
    KOKORO_DEFAULT_VOICE = "af_heart"
    KOKORO_TIMEOUT = 10
    BUDDY_INTERRUPT_THRESHOLD = 2500

# ===== DATA CLASSES =====

@dataclass
class AudioConfig:
    """Audio configuration settings"""
    sample_rate: int = SAMPLE_RATE
    mic_sample_rate: int = MIC_SAMPLE_RATE
    blocksize: int = 320
    channels: int = 1
    dtype: str = 'int16'
    device_index: Optional[int] = MIC_DEVICE_INDEX
    full_duplex: bool = FULL_DUPLEX_MODE

@dataclass
class VADConfig:
    """Voice Activity Detection configuration"""
    speech_threshold_multiplier: float = 3.0
    min_speech_threshold: float = 600.0
    silence_timeout: float = 2.0
    min_speech_duration: float = 0.5
    max_recording_duration: float = 30.0

@dataclass
class AECConfig:
    """Acoustic Echo Cancellation configuration"""
    frame_size: int = 160
    sample_rate: int = 16000
    buffer_duration: float = 2.0
    active_timeout: float = 5.0

@dataclass
class TTSConfig:
    """Text-to-Speech configuration"""
    api_url: str = KOKORO_API_BASE_URL
    default_voice: str = KOKORO_DEFAULT_VOICE
    timeout: float = KOKORO_TIMEOUT
    chunk_threshold: float = 0.3
    min_speech_interval: float = 1.0
    max_retries: int = 3

@dataclass
class AudioQuality:
    """Audio quality metrics"""
    overall_score: float = 0.0
    volume_score: float = 0.0
    noise_score: float = 0.0
    duration_score: float = 0.0
    snr_db: float = 0.0

# ===== MOCK CLASSES FOR MISSING DEPENDENCIES =====

class MockAEC:
    """Mock AEC when PyAEC is not available"""
    def __init__(self, frame_size=160, sample_rate=16000):
        self.frame_size = frame_size
        self.sample_rate = sample_rate
    
    def process(self, captured_audio, reference_audio):
        # Just return the captured audio without processing
        return captured_audio if NUMPY_AVAILABLE else None

class MockAudioDevice:
    """Mock audio device when sounddevice is not available"""
    def __init__(self, *args, **kwargs):
        pass
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        pass
    
    def read(self, frames):
        if NUMPY_AVAILABLE:
            # Return mock audio data
            return np.random.randint(-1000, 1000, (frames, 1), dtype=np.int16), False
        return None, True

# ===== UNIFIED SMART AUDIO MANAGER SYSTEM =====

class SmartAudioManagerSystem:
    """
    Unified Smart Audio Manager combining all audio processing components.
    
    This system provides:
    - Full duplex audio input/output with voice activity detection
    - Advanced acoustic echo cancellation (AEC)
    - Smart streaming TTS output with chunk accumulation
    - Audio quality assessment and noise filtering
    - Real-time audio processing with minimal latency
    - Kokoro-FastAPI integration with connection management
    - Comprehensive error handling and fallbacks
    """
    
    def __init__(self,
                 audio_config: Optional[AudioConfig] = None,
                 vad_config: Optional[VADConfig] = None,
                 aec_config: Optional[AECConfig] = None,
                 tts_config: Optional[TTSConfig] = None):
        """Initialize the unified smart audio manager system"""
        
        # Configuration
        self.audio_config = audio_config or AudioConfig()
        self.vad_config = vad_config or VADConfig()
        self.aec_config = aec_config or AECConfig()
        self.tts_config = tts_config or TTSConfig()
        
        # === AUDIO INPUT COMPONENTS ===
        self.input_stream = None
        self.input_active = threading.Event()
        self.recording_active = threading.Event()
        self.vad_baseline = 200.0
        self.speech_threshold = 600.0
        
        # === AUDIO OUTPUT COMPONENTS ===
        self.output_queue = queue.Queue()
        self.output_active = threading.Event()
        self.buddy_talking = threading.Event()
        self.tts_session = None
        self.output_thread = None
        
        # === AEC COMPONENTS ===
        self.aec_instance = None
        self.ref_audio_buffer = None
        self.aec_active = threading.Event()
        self.last_buddy_speech_time = None
        
        # === STREAMING COMPONENTS ===
        self.chunk_buffer = []
        self.buffer_lock = threading.Lock()
        self.token_count = 0
        self.estimated_total_tokens = 0
        self.speech_started = False
        self.last_speech_time = 0
        
        # === PROCESSING COMPONENTS ===
        self.audio_filters = {}
        self.quality_assessor = None
        
        # Performance tracking
        self.performance_stats = {
            'total_recordings': 0,
            'successful_recordings': 0,
            'total_tts_requests': 0,
            'successful_tts_requests': 0,
            'average_quality': 0.0,
            'error_count': 0,
            'uptime': time.time()
        }
        
        # Threading
        self.lock = threading.Lock()
        self.running = False
        self.threads = {}
        
        # Initialize system
        self._initialize_audio_system()
        self._initialize_aec_system()
        self._initialize_tts_system()
        
        logging.info(f"[SmartAudio] 🎵 Smart audio manager system initialized")
        logging.info(f"[SmartAudio] 📊 Full Duplex: {self.audio_config.full_duplex}")
        logging.info(f"[SmartAudio] 🎤 Sample Rate: {self.audio_config.sample_rate}Hz")
    
    def start(self):
        """Start all audio processing components"""
        if self.running:
            return
        
        self.running = True
        
        # Start output processing thread
        self.output_thread = threading.Thread(target=self._output_processing_loop, daemon=True)
        self.output_thread.start()
        
        # Start AEC monitoring thread
        if self.aec_instance:
            aec_thread = threading.Thread(target=self._aec_monitoring_loop, daemon=True)
            aec_thread.start()
            self.threads['aec'] = aec_thread
        
        self.threads['output'] = self.output_thread
        
        logging.info("[SmartAudio] ✅ Smart audio manager started")
    
    def stop(self):
        """Stop all audio processing components"""
        self.running = False
        
        # Stop input stream
        if self.input_stream:
            try:
                self.input_stream.close()
            except:
                pass
        
        # Stop all events
        self.input_active.clear()
        self.recording_active.clear()
        self.output_active.clear()
        self.buddy_talking.clear()
        self.aec_active.clear()
        
        # Wait for threads to complete
        for thread_name, thread in self.threads.items():
            if thread and thread.is_alive():
                thread.join(timeout=2.0)
        
        logging.info("[SmartAudio] 🛑 Smart audio manager stopped")
    
    # ===== AUDIO INPUT METHODS =====
    
    def listen_for_speech(self, timeout: float = 30.0) -> Optional[np.ndarray]:
        """
        Listen for speech using voice activity detection
        
        Args:
            timeout: Maximum time to wait for speech
            
        Returns:
            Audio data as numpy array or None if no speech detected
        """
        if not SOUNDDEVICE_AVAILABLE or not NUMPY_AVAILABLE:
            logging.warning("[SmartAudio] Audio dependencies not available - using mock")
            return self._mock_listen()
        
        if self.audio_config.full_duplex:
            return self._full_duplex_listen(timeout)
        else:
            return self._half_duplex_listen(timeout)
    
    def _full_duplex_listen(self, timeout: float) -> Optional[np.ndarray]:
        """Full duplex listening with AEC"""
        try:
            blocksize = int(self.audio_config.mic_sample_rate * 0.02)  # 20ms blocks
            
            with sd.InputStream(
                device=self.audio_config.device_index,
                samplerate=self.audio_config.mic_sample_rate,
                channels=self.audio_config.channels,
                blocksize=blocksize,
                dtype=self.audio_config.dtype
            ) as stream:
                
                # Calculate baseline noise level
                baseline_samples = []
                for _ in range(5):
                    frame, _ = stream.read(blocksize)
                    if frame is not None:
                        audio = np.frombuffer(frame.tobytes(), dtype=np.int16)
                        baseline_samples.append(np.abs(audio).mean())
                
                baseline = np.mean(baseline_samples) if baseline_samples else self.vad_baseline
                speech_threshold = max(
                    baseline * self.vad_config.speech_threshold_multiplier,
                    self.vad_config.min_speech_threshold
                )
                
                logging.info(f"[SmartAudio] 👂 Full duplex ready (baseline: {baseline:.0f}, threshold: {speech_threshold:.0f})")
                
                # Main listening loop
                audio_buffer = []
                start_time = time.time()
                silence_frames = 0
                has_speech = False
                speech_frames = 0
                
                while time.time() - start_time < timeout:
                    if not self.running:
                        break
                    
                    frame, overflowed = stream.read(blocksize)
                    if frame is None or overflowed:
                        continue
                    
                    audio = np.frombuffer(frame.tobytes(), dtype=np.int16)
                    
                    # Apply AEC if available and Buddy is talking
                    if self.aec_instance and self.buddy_talking.is_set():
                        audio = self._apply_aec(audio)
                    
                    # Voice activity detection
                    energy = np.abs(audio).mean()
                    
                    if energy > speech_threshold:
                        speech_frames += 1
                        silence_frames = 0
                        has_speech = True
                        audio_buffer.extend(audio)
                    else:
                        silence_frames += 1
                        if has_speech:
                            audio_buffer.extend(audio)  # Include some silence
                        
                        # Check for end of speech
                        silence_duration = silence_frames * blocksize / self.audio_config.mic_sample_rate
                        if has_speech and silence_duration > self.vad_config.silence_timeout:
                            break
                
                # Validate recording
                if audio_buffer and has_speech:
                    audio_array = np.array(audio_buffer, dtype=np.int16)
                    duration = len(audio_array) / self.audio_config.mic_sample_rate
                    
                    if duration >= self.vad_config.min_speech_duration:
                        self.performance_stats['total_recordings'] += 1
                        self.performance_stats['successful_recordings'] += 1
                        return audio_array
                
                return None
                
        except Exception as e:
            logging.error(f"[SmartAudio] Full duplex listen error: {e}")
            self.performance_stats['error_count'] += 1
            return None
    
    def _half_duplex_listen(self, timeout: float) -> Optional[np.ndarray]:
        """Half duplex listening (simpler, no AEC)"""
        try:
            duration = min(timeout, self.vad_config.max_recording_duration)
            
            recording = sd.rec(
                int(duration * self.audio_config.mic_sample_rate),
                samplerate=self.audio_config.mic_sample_rate,
                channels=self.audio_config.channels,
                device=self.audio_config.device_index,
                dtype=self.audio_config.dtype
            )
            
            sd.wait()  # Wait for recording to complete
            
            if recording is not None and len(recording) > 0:
                audio_array = recording.flatten().astype(np.int16)
                self.performance_stats['total_recordings'] += 1
                self.performance_stats['successful_recordings'] += 1
                return audio_array
                
            return None
            
        except Exception as e:
            logging.error(f"[SmartAudio] Half duplex listen error: {e}")
            self.performance_stats['error_count'] += 1
            return None
    
    def _mock_listen(self) -> Optional[np.ndarray]:
        """Mock listening for testing when audio is not available"""
        if NUMPY_AVAILABLE:
            # Generate mock audio data
            duration = 3.0  # 3 seconds
            samples = int(duration * self.audio_config.sample_rate)
            audio = np.random.randint(-1000, 1000, samples, dtype=np.int16)
            
            logging.info("[SmartAudio] 🎭 Mock audio generated for testing")
            return audio
        return None
    
    # ===== AUDIO OUTPUT METHODS =====
    
    def speak_text(self, text: str, voice: Optional[str] = None, priority: int = 0) -> bool:
        """
        Convert text to speech using Kokoro-FastAPI
        
        Args:
            text: Text to speak
            voice: Voice to use (optional)
            priority: Priority level (higher = more urgent)
            
        Returns:
            True if speech request was queued successfully
        """
        try:
            if not text or not text.strip():
                return False
            
            # Clean and prepare text
            cleaned_text = self._clean_text_for_tts(text)
            if not cleaned_text:
                return False
            
            # Add to output queue
            speech_request = {
                'text': cleaned_text,
                'voice': voice or self.tts_config.default_voice,
                'priority': priority,
                'timestamp': time.time()
            }
            
            self.output_queue.put(speech_request)
            self.performance_stats['total_tts_requests'] += 1
            
            return True
            
        except Exception as e:
            logging.error(f"[SmartAudio] Speak text error: {e}")
            self.performance_stats['error_count'] += 1
            return False
    
    def speak_streaming(self, text_chunks: List[str], voice: Optional[str] = None) -> bool:
        """
        Stream text chunks to TTS with smart accumulation
        
        Args:
            text_chunks: List of text chunks to speak
            voice: Voice to use (optional)
            
        Returns:
            True if streaming started successfully
        """
        try:
            with self.buffer_lock:
                self.chunk_buffer = []
                self.token_count = 0
                self.estimated_total_tokens = sum(len(chunk.split()) for chunk in text_chunks)
                self.speech_started = False
            
            for i, chunk in enumerate(text_chunks):
                is_final = (i == len(text_chunks) - 1)
                self._add_streaming_chunk(chunk, is_final, voice)
            
            return True
            
        except Exception as e:
            logging.error(f"[SmartAudio] Streaming error: {e}")
            self.performance_stats['error_count'] += 1
            return False
    
    def _add_streaming_chunk(self, chunk: str, is_final: bool, voice: Optional[str] = None) -> bool:
        """Add chunk to streaming buffer with smart accumulation"""
        try:
            with self.buffer_lock:
                if not chunk.strip():
                    return False
                
                self.chunk_buffer.append(chunk)
                self.token_count += len(chunk.split())
                
                # Calculate completion percentage
                completion_ratio = (self.token_count / self.estimated_total_tokens 
                                 if self.estimated_total_tokens > 0 else 0)
                
                # Decide whether to trigger speech
                should_speak = (
                    is_final or
                    (completion_ratio >= self.tts_config.chunk_threshold and not self.speech_started) or
                    (time.time() - self.last_speech_time >= self.tts_config.min_speech_interval)
                )
                
                if should_speak and self.chunk_buffer:
                    combined_text = ' '.join(self.chunk_buffer)
                    self.chunk_buffer = []
                    self.speech_started = True
                    self.last_speech_time = time.time()
                    
                    # Queue for TTS
                    return self.speak_text(combined_text, voice, priority=1)
            
            return False
            
        except Exception as e:
            logging.error(f"[SmartAudio] Add streaming chunk error: {e}")
            return False
    
    def _output_processing_loop(self):
        """Main output processing loop"""
        while self.running:
            try:
                # Get next speech request
                try:
                    request = self.output_queue.get(timeout=1.0)
                except queue.Empty:
                    continue
                
                if not request:
                    continue
                
                # Process TTS request
                success = self._process_tts_request(request)
                if success:
                    self.performance_stats['successful_tts_requests'] += 1
                
                self.output_queue.task_done()
                
            except Exception as e:
                logging.error(f"[SmartAudio] Output processing error: {e}")
                time.sleep(1.0)
    
    def _process_tts_request(self, request: Dict[str, Any]) -> bool:
        """Process a single TTS request"""
        try:
            if not REQUESTS_AVAILABLE:
                logging.warning("[SmartAudio] Requests not available - mock TTS")
                return self._mock_tts(request['text'])
            
            # Mark Buddy as talking
            self.buddy_talking.set()
            
            # Prepare request data
            tts_data = {
                'text': request['text'],
                'voice': request['voice'],
                'speed': 1.0,
                'audioformat': 'wav'
            }
            
            # Make TTS request with retries
            for attempt in range(self.tts_config.max_retries):
                try:
                    response = self.tts_session.post(
                        f"{self.tts_config.api_url}/api/tts",
                        json=tts_data,
                        timeout=self.tts_config.timeout
                    )
                    
                    if response.status_code == 200:
                        # Play audio
                        success = self._play_audio_data(response.content)
                        if success:
                            return True
                    else:
                        logging.warning(f"[SmartAudio] TTS API error {response.status_code}")
                
                except requests.exceptions.RequestException as e:
                    logging.warning(f"[SmartAudio] TTS request error (attempt {attempt + 1}): {e}")
                    if attempt < self.tts_config.max_retries - 1:
                        time.sleep(random.uniform(0.5, 1.5))  # Jittered retry
                
            return False
            
        except Exception as e:
            logging.error(f"[SmartAudio] TTS processing error: {e}")
            return False
        finally:
            self.buddy_talking.clear()
    
    def _play_audio_data(self, audio_data: bytes) -> bool:
        """Play audio data through speakers"""
        try:
            if SIMPLEAUDIO_AVAILABLE:
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                    temp_file.write(audio_data)
                    temp_file.flush()
                    
                    wave_obj = sa.WaveObject.from_wave_file(temp_file.name)
                    play_obj = wave_obj.play()
                    play_obj.wait_done()
                    
                    os.unlink(temp_file.name)
                return True
            else:
                logging.warning("[SmartAudio] Audio playback not available")
                return False
                
        except Exception as e:
            logging.error(f"[SmartAudio] Audio playback error: {e}")
            return False
    
    def _mock_tts(self, text: str) -> bool:
        """Mock TTS for testing when requests is not available"""
        logging.info(f"[SmartAudio] 🎭 Mock TTS: {text[:50]}...")
        time.sleep(len(text) * 0.05)  # Simulate speech duration
        return True
    
    # ===== AEC METHODS =====
    
    def _apply_aec(self, captured_audio: np.ndarray) -> np.ndarray:
        """Apply acoustic echo cancellation"""
        try:
            if not self.aec_instance or not NUMPY_AVAILABLE:
                return captured_audio
            
            # Get reference audio from buffer
            if self.ref_audio_buffer is None:
                return captured_audio
            
            # Process audio in frame-sized chunks
            frame_size = self.aec_config.frame_size
            processed_audio = []
            
            for i in range(0, len(captured_audio), frame_size):
                captured_frame = captured_audio[i:i+frame_size]
                if len(captured_frame) < frame_size:
                    # Pad incomplete frame
                    captured_frame = np.pad(captured_frame, (0, frame_size - len(captured_frame)))
                
                # Get corresponding reference frame
                ref_frame = self.ref_audio_buffer[i:i+frame_size]
                if len(ref_frame) < frame_size:
                    ref_frame = np.pad(ref_frame, (0, frame_size - len(ref_frame)))
                
                # Apply AEC
                processed_frame = self.aec_instance.process(captured_frame, ref_frame)
                if processed_frame is not None:
                    processed_audio.extend(processed_frame)
                else:
                    processed_audio.extend(captured_frame)
            
            return np.array(processed_audio, dtype=np.int16)
            
        except Exception as e:
            logging.error(f"[SmartAudio] AEC processing error: {e}")
            return captured_audio
    
    def update_reference_audio(self, audio_data: np.ndarray):
        """Update AEC reference audio buffer"""
        try:
            if not self.buddy_talking.is_set() or not NUMPY_AVAILABLE:
                return
            
            self.last_buddy_speech_time = time.time()
            self.aec_active.set()
            
            # Update reference buffer
            if self.ref_audio_buffer is not None:
                buffer_size = len(self.ref_audio_buffer)
                audio_size = len(audio_data)
                
                if audio_size >= buffer_size:
                    # Replace entire buffer
                    self.ref_audio_buffer = audio_data[-buffer_size:].copy()
                else:
                    # Shift buffer and append new data
                    self.ref_audio_buffer[:-audio_size] = self.ref_audio_buffer[audio_size:]
                    self.ref_audio_buffer[-audio_size:] = audio_data
            
        except Exception as e:
            logging.error(f"[SmartAudio] Reference audio update error: {e}")
    
    def _aec_monitoring_loop(self):
        """Monitor AEC activity and clean up stale references"""
        while self.running:
            try:
                if (self.last_buddy_speech_time and 
                    time.time() - self.last_buddy_speech_time > self.aec_config.active_timeout):
                    self.aec_active.clear()
                
                time.sleep(1.0)
                
            except Exception as e:
                logging.error(f"[SmartAudio] AEC monitoring error: {e}")
                time.sleep(5.0)
    
    # ===== AUDIO PROCESSING METHODS =====
    
    def process_audio(self, audio: np.ndarray, 
                     target_sample_rate: Optional[int] = None,
                     apply_filters: bool = True) -> Optional[np.ndarray]:
        """
        Process audio with filtering and resampling
        
        Args:
            audio: Input audio data
            target_sample_rate: Target sample rate (optional)
            apply_filters: Whether to apply audio filters
            
        Returns:
            Processed audio data or None if processing failed
        """
        try:
            if not NUMPY_AVAILABLE or audio is None or len(audio) == 0:
                return None
            
            processed_audio = audio.copy()
            
            # Ensure mono audio
            if processed_audio.ndim > 1:
                processed_audio = processed_audio[:, 0]
            
            # Convert to float for processing
            if processed_audio.dtype == np.int16:
                processed_audio = processed_audio.astype(np.float32) / 32768.0
            
            # Apply noise filtering if requested
            if apply_filters:
                processed_audio = self._apply_noise_filters(processed_audio)
            
            # Resample if needed
            if target_sample_rate and target_sample_rate != self.audio_config.sample_rate:
                if SCIPY_AVAILABLE:
                    processed_audio = resample_poly(
                        processed_audio, 
                        target_sample_rate, 
                        self.audio_config.sample_rate
                    )
                else:
                    logging.warning("[SmartAudio] SciPy not available - skipping resampling")
            
            # Convert back to int16
            processed_audio = np.clip(processed_audio, -1.0, 1.0)
            return (processed_audio * 32767).astype(np.int16)
            
        except Exception as e:
            logging.error(f"[SmartAudio] Audio processing error: {e}")
            return None
    
    def assess_audio_quality(self, audio: np.ndarray) -> AudioQuality:
        """Assess audio quality metrics"""
        try:
            if not NUMPY_AVAILABLE or audio is None or len(audio) == 0:
                return AudioQuality()
            
            # Basic metrics
            duration = len(audio) / self.audio_config.sample_rate
            volume_level = np.sqrt(np.mean(audio.astype(np.float32)**2))
            
            # Duration score (prefer 2-10 seconds)
            duration_score = 1.0
            if duration < 1.0:
                duration_score = duration
            elif duration > 10.0:
                duration_score = max(0.1, 1.0 - (duration - 10.0) * 0.1)
            
            # Volume score (prefer moderate volumes)
            volume_score = min(1.0, volume_level * 10)
            
            # Simple SNR estimate
            signal_power = np.var(audio.astype(np.float32))
            noise_floor = np.percentile(np.abs(audio.astype(np.float32)), 10)
            snr_db = 10 * np.log10(signal_power / (noise_floor**2 + 1e-10))
            
            # Noise score based on SNR
            noise_score = min(1.0, max(0.0, (snr_db - 5) / 20))
            
            # Overall score
            overall_score = (duration_score + volume_score + noise_score) / 3
            
            return AudioQuality(
                overall_score=overall_score,
                volume_score=volume_score,
                noise_score=noise_score,
                duration_score=duration_score,
                snr_db=snr_db
            )
            
        except Exception as e:
            logging.error(f"[SmartAudio] Quality assessment error: {e}")
            return AudioQuality()
    
    def _apply_noise_filters(self, audio: np.ndarray) -> np.ndarray:
        """Apply basic noise filtering"""
        try:
            # Simple high-pass filter to remove low-frequency noise
            if len(audio) > 1:
                filtered = audio[1:] - 0.95 * audio[:-1]  # Simple high-pass
                return np.pad(filtered, (1, 0), mode='constant')
            return audio
            
        except Exception as e:
            logging.warning(f"[SmartAudio] Noise filtering error: {e}")
            return audio
    
    def is_speech_quality_acceptable(self, audio: np.ndarray, min_quality: float = 0.4) -> bool:
        """Check if audio quality is acceptable for processing"""
        quality = self.assess_audio_quality(audio)
        return quality.overall_score >= min_quality
    
    # ===== UTILITY METHODS =====
    
    def _clean_text_for_tts(self, text: str) -> str:
        """Clean text for TTS processing"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        cleaned = ' '.join(text.split())
        
        # Filter out very short or nonsensical text
        words = cleaned.split()
        if len(words) < 2:
            avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
            if avg_word_length < 3:
                return ""
        
        return cleaned
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get comprehensive system statistics"""
        uptime = time.time() - self.performance_stats['uptime']
        
        stats = {
            'uptime_seconds': uptime,
            'performance': self.performance_stats.copy(),
            'config': {
                'full_duplex': self.audio_config.full_duplex,
                'sample_rate': self.audio_config.sample_rate,
                'tts_api': self.tts_config.api_url
            },
            'dependencies': {
                'sounddevice': SOUNDDEVICE_AVAILABLE,
                'numpy': NUMPY_AVAILABLE,
                'scipy': SCIPY_AVAILABLE,
                'simpleaudio': SIMPLEAUDIO_AVAILABLE,
                'requests': REQUESTS_AVAILABLE,
                'pyaec': PYAEC_AVAILABLE,
                'langdetect': LANGDETECT_AVAILABLE
            },
            'status': {
                'running': self.running,
                'buddy_talking': self.buddy_talking.is_set(),
                'aec_active': self.aec_active.is_set(),
                'queue_size': self.output_queue.qsize()
            }
        }
        
        # Calculate success rates
        if stats['performance']['total_recordings'] > 0:
            stats['performance']['recording_success_rate'] = (
                stats['performance']['successful_recordings'] / 
                stats['performance']['total_recordings']
            )
        
        if stats['performance']['total_tts_requests'] > 0:
            stats['performance']['tts_success_rate'] = (
                stats['performance']['successful_tts_requests'] / 
                stats['performance']['total_tts_requests']
            )
        
        return stats
    
    # ===== PRIVATE INITIALIZATION METHODS =====
    
    def _initialize_audio_system(self):
        """Initialize audio input/output system"""
        try:
            if SOUNDDEVICE_AVAILABLE:
                # Test audio devices
                devices = sd.query_devices()
                logging.info(f"[SmartAudio] Found {len(devices)} audio devices")
                
                # Set default device if not specified
                if self.audio_config.device_index is None:
                    default_device = sd.default.device[0]  # Input device
                    self.audio_config.device_index = default_device
                    logging.info(f"[SmartAudio] Using default input device: {default_device}")
            else:
                logging.warning("[SmartAudio] SoundDevice not available - using mock audio")
            
        except Exception as e:
            logging.error(f"[SmartAudio] Audio system initialization error: {e}")
    
    def _initialize_aec_system(self):
        """Initialize acoustic echo cancellation system"""
        try:
            if PYAEC_AVAILABLE and NUMPY_AVAILABLE:
                self.aec_instance = PyAec(
                    frame_size=self.aec_config.frame_size,
                    sample_rate=self.aec_config.sample_rate
                )
                
                # Initialize reference audio buffer
                buffer_samples = int(self.aec_config.buffer_duration * self.aec_config.sample_rate)
                self.ref_audio_buffer = np.zeros(buffer_samples, dtype=np.int16)
                
                logging.info("[SmartAudio] ✅ AEC system initialized")
            else:
                self.aec_instance = MockAEC()
                logging.warning("[SmartAudio] Using mock AEC - PyAEC not available")
                
        except Exception as e:
            logging.error(f"[SmartAudio] AEC system initialization error: {e}")
            self.aec_instance = MockAEC()
    
    def _initialize_tts_system(self):
        """Initialize text-to-speech system"""
        try:
            if REQUESTS_AVAILABLE:
                self.tts_session = requests.Session()
                self.tts_session.headers.update({
                    'Connection': 'keep-alive',
                    'Keep-Alive': 'timeout=30, max=100',
                    'User-Agent': 'SmartAudio/1.0'
                })
                
                # Configure session adapter
                adapter = requests.adapters.HTTPAdapter(
                    pool_connections=1,
                    pool_maxsize=1,
                    max_retries=0,
                    pool_block=False
                )
                self.tts_session.mount('http://', adapter)
                self.tts_session.mount('https://', adapter)
                
                logging.info(f"[SmartAudio] ✅ TTS system initialized - {self.tts_config.api_url}")
            else:
                logging.warning("[SmartAudio] TTS system using mock - requests not available")
                
        except Exception as e:
            logging.error(f"[SmartAudio] TTS system initialization error: {e}")


# ===== BACKWARD COMPATIBILITY ALIASES =====

# Allow existing imports to continue working
def simple_vad_listen():
    """Backward compatibility function for VAD listening"""
    global _default_audio_manager
    if _default_audio_manager is None:
        _default_audio_manager = SmartAudioManagerSystem()
    return _default_audio_manager.listen_for_speech()

def speak_streaming(text, voice=None):
    """Backward compatibility function for streaming TTS"""
    global _default_audio_manager
    if _default_audio_manager is None:
        _default_audio_manager = SmartAudioManagerSystem()
    return _default_audio_manager.speak_text(text, voice)

def aec_training_listen():
    """Backward compatibility function for training audio"""
    global _default_audio_manager
    if _default_audio_manager is None:
        _default_audio_manager = SmartAudioManagerSystem()
    return _default_audio_manager.listen_for_speech(timeout=10.0)

def downsample_audio(audio, orig_sr, target_sr):
    """Backward compatibility function for audio downsampling"""
    global _default_audio_manager
    if _default_audio_manager is None:
        _default_audio_manager = SmartAudioManagerSystem()
    return _default_audio_manager.process_audio(audio, target_sr)

def is_noise_or_gibberish(text):
    """Check if text is noise or gibberish"""
    if not text or len(text.strip()) < 2:
        return True
    words = text.strip().split()
    avg_len = sum(len(w) for w in words) / len(words) if words else 0
    if len(words) < 2 and avg_len < 4:
        return True
    return False

def buddy_talking():
    """Get buddy talking event"""
    global _default_audio_manager
    if _default_audio_manager is None:
        _default_audio_manager = SmartAudioManagerSystem()
    return _default_audio_manager.buddy_talking

def is_buddy_talking():
    """Check if buddy is currently talking"""
    global _default_audio_manager
    if _default_audio_manager is None:
        _default_audio_manager = SmartAudioManagerSystem()
    return _default_audio_manager.buddy_talking.is_set()

def play_chime():
    """Play notification chime"""
    global _default_audio_manager
    if _default_audio_manager is None:
        _default_audio_manager = SmartAudioManagerSystem()
    return _default_audio_manager.speak_text("*chime*")  # Mock chime

# Create default instance for backward compatibility
_default_audio_manager = None

def get_audio_manager():
    """Get or create the default audio manager instance"""
    global _default_audio_manager
    if _default_audio_manager is None:
        _default_audio_manager = SmartAudioManagerSystem()
    return _default_audio_manager

# Module-level exports for backward compatibility
__all__ = [
    'SmartAudioManagerSystem',
    'AudioConfig', 'VADConfig', 'AECConfig', 'TTSConfig', 'AudioQuality',
    'simple_vad_listen', 'speak_streaming', 'aec_training_listen',
    'downsample_audio', 'is_noise_or_gibberish', 'buddy_talking', 
    'is_buddy_talking', 'play_chime', 'get_audio_manager'
]