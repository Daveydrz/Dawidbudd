"""
Voice Detection Emergency Fix
Created: 2025-01-17
Purpose: Fix VAD, voice analyzer, and smart detection getting stuck after questions
         ensuring user speech is always prioritized
"""

import time
import threading
import numpy as np
from typing import Dict, Any, Optional, Tuple
from collections import deque

class VoiceDetectionFix:
    """Emergency fix for voice detection getting stuck"""
    
    def __init__(self):
        self.detection_active = False
        self.last_detection_time = 0.0
        self.detection_timeout = 10.0  # Max 10 seconds for any detection
        self.stuck_detection_count = 0
        self.emergency_resets = 0
        
        # Simple volume-based detection as fallback
        self.volume_threshold = 500
        self.volume_history = deque(maxlen=10)
        
        # Thread safety
        self.detection_lock = threading.Lock()
        
        print("[VoiceDetectionFix] 🚨 Voice Detection Emergency Fix initialized")
        print("[VoiceDetectionFix] 🎯 Goal: Prevent voice detection from getting stuck")
        
    def emergency_voice_detection(self, audio_data: np.ndarray) -> Tuple[bool, Dict[str, Any]]:
        """
        Emergency voice detection that never gets stuck
        
        Returns: (is_voice_detected, detection_info)
        """
        with self.detection_lock:
            start_time = time.time()
            
            try:
                # Check for stuck detection
                if self.detection_active and (start_time - self.last_detection_time) > self.detection_timeout:
                    print(f"[VoiceDetectionFix] 🚨 STUCK DETECTION DETECTED - Emergency reset!")
                    self._emergency_reset()
                
                self.detection_active = True
                self.last_detection_time = start_time
                
                # Ultra-simple voice detection
                is_voice, detection_info = self._simple_voice_detection(audio_data)
                
                # Immediate completion
                self.detection_active = False
                detection_time = time.time() - start_time
                
                detection_info.update({
                    "detection_method": "emergency_fast",
                    "detection_time": detection_time,
                    "emergency_mode": True,
                    "stuck_resets": self.emergency_resets
                })
                
                if detection_time > 1.0:
                    print(f"[VoiceDetectionFix] ⚠️ Slow detection: {detection_time:.3f}s")
                
                return is_voice, detection_info
                
            except Exception as e:
                self.detection_active = False
                print(f"[VoiceDetectionFix] ❌ Detection error: {e}")
                return False, {
                    "error": str(e),
                    "detection_method": "emergency_fallback",
                    "emergency_mode": True
                }
    
    def _simple_voice_detection(self, audio_data: np.ndarray) -> Tuple[bool, Dict[str, Any]]:
        """Ultra-simple voice detection that can't get stuck"""
        try:
            # Basic validation
            if audio_data is None or len(audio_data) == 0:
                return False, {"reason": "empty_audio"}
            
            # Ensure numpy array
            if not isinstance(audio_data, np.ndarray):
                audio_data = np.array(audio_data, dtype=np.int16)
            
            # Calculate volume quickly
            volume = float(np.abs(audio_data).mean())
            peak = float(np.max(np.abs(audio_data)))
            
            # Add to history
            self.volume_history.append(volume)
            
            # Simple volume threshold
            volume_detected = volume > self.volume_threshold
            
            # Basic frequency analysis (fast)
            voice_frequency_detected = self._quick_frequency_check(audio_data)
            
            # Simple decision
            is_voice = volume_detected and voice_frequency_detected
            
            detection_info = {
                "volume": volume,
                "peak": peak,
                "threshold": self.volume_threshold,
                "volume_detected": volume_detected,
                "frequency_detected": voice_frequency_detected,
                "recent_volumes": list(self.volume_history)[-3:],  # Last 3 for context
                "decision": "voice" if is_voice else "noise"
            }
            
            return is_voice, detection_info
            
        except Exception as e:
            return False, {"error": f"simple_detection_error: {e}"}
    
    def _quick_frequency_check(self, audio_data: np.ndarray) -> bool:
        """Quick frequency analysis to detect voice-like content"""
        try:
            # Only analyze small chunk for speed
            chunk_size = min(1024, len(audio_data))
            chunk = audio_data[:chunk_size]
            
            # Simple FFT
            fft_data = np.fft.fft(chunk)
            freqs = np.fft.fftfreq(chunk_size, 1/16000)
            magnitude = np.abs(fft_data)
            
            # Voice frequency range (simplified)
            voice_mask = (freqs >= 100) & (freqs <= 4000)
            voice_energy = np.sum(magnitude[voice_mask])
            total_energy = np.sum(magnitude)
            
            # Simple ratio check
            voice_ratio = voice_energy / max(total_energy, 1)
            return voice_ratio > 0.1  # Very lenient threshold
            
        except:
            # If frequency analysis fails, default to True
            return True
    
    def _emergency_reset(self):
        """Emergency reset when detection gets stuck"""
        self.emergency_resets += 1
        self.stuck_detection_count += 1
        self.detection_active = False
        self.last_detection_time = 0.0
        
        print(f"[VoiceDetectionFix] 🔄 Emergency reset #{self.emergency_resets}")
        print(f"[VoiceDetectionFix] 📊 Total stuck detections: {self.stuck_detection_count}")
    
    def is_detection_stuck(self) -> bool:
        """Check if voice detection appears to be stuck"""
        if not self.detection_active:
            return False
            
        time_elapsed = time.time() - self.last_detection_time
        return time_elapsed > self.detection_timeout
    
    def force_reset(self):
        """Force reset of voice detection system"""
        with self.detection_lock:
            print("[VoiceDetectionFix] 🚨 FORCE RESET requested")
            self._emergency_reset()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get voice detection fix statistics"""
        return {
            "detection_active": self.detection_active,
            "last_detection_time": self.last_detection_time,
            "stuck_detections": self.stuck_detection_count,
            "emergency_resets": self.emergency_resets,
            "volume_threshold": self.volume_threshold,
            "recent_volumes": list(self.volume_history)[-5:],
            "status": "stuck" if self.is_detection_stuck() else "operational"
        }

# Global instance
voice_detection_fix = VoiceDetectionFix()

def emergency_voice_detection(audio_data: np.ndarray) -> Tuple[bool, Dict[str, Any]]:
    """Emergency voice detection that never gets stuck"""
    return voice_detection_fix.emergency_voice_detection(audio_data)

def is_voice_detection_stuck() -> bool:
    """Check if voice detection is stuck"""
    return voice_detection_fix.is_detection_stuck()

def force_voice_detection_reset():
    """Force reset voice detection if stuck"""
    voice_detection_fix.force_reset()

def get_voice_detection_stats() -> Dict[str, Any]:
    """Get voice detection statistics"""
    return voice_detection_fix.get_stats()

# Smart Detection Manager Override
class SmartDetectionManagerFix:
    """Fixed version of smart detection manager that doesn't get stuck"""
    
    def __init__(self):
        self.original_available = False
        try:
            from audio.smart_detection_manager import SmartDetectionManager
            self.original_manager = SmartDetectionManager()
            self.original_available = True
            print("[SmartDetectionFix] ✅ Original manager available, adding safeguards")
        except:
            self.original_manager = None
            print("[SmartDetectionFix] ⚠️ Original manager not available, using emergency mode")
    
    def analyze_speech_detection(self, audio_data: np.ndarray, volume: float) -> Tuple[bool, Dict[str, Any]]:
        """Analyze speech with timeout protection"""
        start_time = time.time()
        
        try:
            # Use emergency detection if original is not available
            if not self.original_available:
                return emergency_voice_detection(audio_data)
            
            # Try original with timeout
            try:
                # Set a timeout for the original detection
                import signal
                
                def timeout_handler(signum, frame):
                    raise TimeoutError("Smart detection timeout")
                
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(3)  # 3 second timeout
                
                # Try original method
                result = self.original_manager.should_trigger_detection(audio_data, volume)
                signal.alarm(0)  # Cancel timeout
                
                detection_time = time.time() - start_time
                
                if isinstance(result, tuple) and len(result) >= 2:
                    should_trigger, info = result
                    info["detection_time"] = detection_time
                    info["detection_method"] = "original_with_timeout"
                    return should_trigger, info
                else:
                    # Fallback if unexpected format
                    return emergency_voice_detection(audio_data)
                    
            except (TimeoutError, Exception) as e:
                signal.alarm(0)  # Cancel timeout
                print(f"[SmartDetectionFix] ⚠️ Original detection failed/timeout: {e}")
                return emergency_voice_detection(audio_data)
                
        except Exception as e:
            print(f"[SmartDetectionFix] ❌ Analysis error: {e}")
            return emergency_voice_detection(audio_data)
    
    def get_current_threshold(self) -> float:
        """Get current detection threshold"""
        if self.original_available:
            try:
                return getattr(self.original_manager, 'volume_threshold', 500)
            except:
                pass
        return 500  # Default fallback

# Global fixed manager
smart_detection_fix = SmartDetectionManagerFix()

def analyze_speech_detection(audio_data: np.ndarray, volume: float) -> Tuple[bool, Dict[str, Any]]:
    """Fixed speech detection that doesn't get stuck"""
    return smart_detection_fix.analyze_speech_detection(audio_data, volume)

def get_current_threshold() -> float:
    """Get current detection threshold"""
    return smart_detection_fix.get_current_threshold()

if __name__ == "__main__":
    # Test voice detection fix
    print("Testing Voice Detection Emergency Fix")
    
    # Test with dummy audio data
    test_audio = np.random.randint(-1000, 1000, 1000, dtype=np.int16)
    
    for i in range(5):
        print(f"\nTest {i+1}:")
        start_time = time.time()
        
        is_voice, info = emergency_voice_detection(test_audio)
        
        detection_time = time.time() - start_time
        print(f"Voice detected: {is_voice}")
        print(f"Detection time: {detection_time:.3f}s")
        print(f"Info: {info}")
        
        if detection_time > 1.0:
            print("⚠️ Detection too slow!")
    
    # Show stats
    stats = get_voice_detection_stats()
    print(f"\nStats: {stats}")