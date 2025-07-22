# audio/output.py - UPDATED for Direct Kokoro Library Integration
# Date: 2025-01-18 (Brisbane Time)
# CHANGES: Switch from Kokoro FastAPI to direct Kokoro library from hexgrad/kokoro

import threading
import time
import queue
import numpy as np
import simpleaudio as sa
import tempfile
import os
from langdetect import detect
from config import *

# Import Kokoro library directly
try:
    from kokoro import Kokoro
    KOKORO_AVAILABLE = True
    print("[Kokoro] ✅ Direct Kokoro library imported successfully")
except ImportError as e:
    print(f"[Kokoro] ❌ Could not import Kokoro library: {e}")
    KOKORO_AVAILABLE = False

# Global audio state
audio_queue = queue.Queue()
current_audio_playback = None
audio_lock = threading.Lock()
buddy_talking = threading.Event()
playback_start_time = None

# ✅ NEW: Direct Kokoro library configuration
KOKORO_MODEL_PATH = "C:/Users/drzew/kokoro-onnx/kokoro-v1_0.pth"
KOKORO_DEFAULT_VOICE = getattr(globals(), 'KOKORO_DEFAULT_VOICE', "af_heart")

# Voice mapping for different languages
KOKORO_VOICES = {
    "en": "af_heart",      # Australian female
    "en-us": "am_adam",    # American male  
    "en-gb": "bf_emma",    # British female
    "es": "es_maria",      # Spanish female
    "fr": "fr_pierre",     # French male
    "de": "de_anna",       # German female
    "it": "it_marco",      # Italian male
    "pt": "pt_sofia",      # Portuguese female
    "ja": "ja_yuki",       # Japanese female
    "ko": "ko_minho",      # Korean male
    "zh": "zh_mei",        # Chinese female
}

# Initialize Kokoro model
kokoro_model = None

def load_kokoro_model():
    """Load the Kokoro model once globally"""
    global kokoro_model
    try:
        if KOKORO_AVAILABLE and kokoro_model is None:
            print(f"[Kokoro] 🔄 Loading model from {KOKORO_MODEL_PATH}")
            kokoro_model = Kokoro(KOKORO_MODEL_PATH)
            print(f"[Kokoro] ✅ Model loaded successfully")
            return True
    except Exception as e:
        print(f"[Kokoro] ❌ Failed to load model: {e}")
        kokoro_model = None
    return False

def test_kokoro_api():
    """Test if Kokoro model is available and loaded"""
    global kokoro_model
    if kokoro_model is not None:
        print(f"[Kokoro] ✅ Direct Kokoro model ready")
        return True
    
    # Try to load the model
    if load_kokoro_model():
        return True
    
    print(f"[Kokoro] ❌ Kokoro model not available")
    print(f"[Kokoro] 💡 Make sure the model file exists at {KOKORO_MODEL_PATH}")
    return False

def generate_tts(text, lang=DEFAULT_LANG):
    """Generate TTS audio using direct Kokoro library"""
    try:
        if not text.strip():
            return None, None
        
        # Ensure model is loaded
        if kokoro_model is None:
            if not load_kokoro_model():
                return None, None
            
        # Detect language and select voice (simplified for direct library)
        detected_lang = lang or detect(text)
        voice = KOKORO_VOICES.get(detected_lang, KOKORO_DEFAULT_VOICE)
        
        # Generate audio directly using Kokoro model
        try:
            audio_np = kokoro_model.generate(text.strip())
        except Exception as e:
            print(f"[Kokoro] ❌ First generation failed: {e}, retrying...")
            time.sleep(1)
            try:
                audio_np = kokoro_model.generate(text.strip())
            except Exception as retry_e:
                print(f"[Kokoro] ❌ Retry also failed: {retry_e}")
                return None, None
        
        # Normalize and ensure correct dtype
        if audio_np is not None:
            audio_np = (audio_np * 32767).astype(np.int16)
            
            if DEBUG:
                print(f"[Kokoro] 🗣️ Generated TTS: {len(audio_np)} samples, voice: {voice}")
            
            return audio_np, 16000
        else:
            print(f"[Kokoro] ❌ No audio generated")
            return None, None
            
    except Exception as e:
        print(f"[Kokoro] TTS error: {e}")
        return None, None

def speak_async(text, lang=DEFAULT_LANG):
    """Queue text for speech synthesis"""
    if not text or len(text.strip()) < 2:
        return
    
    # Split long text before TTS
    if len(text.strip()) > 500:
        print("[TTS] ⚠️ Text too long. Splitting into chunks.")
        import re
        for chunk in re.split(r'[.!?]', text):
            if chunk.strip():
                speak_async(chunk.strip(), lang)
        return
        
    def tts_worker():
        pcm, sr = generate_tts(text.strip(), lang)
        if pcm is None:
            print("[TTS] ⚠️ No audio generated. Using fallback message.")
            fallback_pcm, sr = generate_tts("Sorry, something went wrong.", lang)
            if fallback_pcm is not None:
                audio_queue.put((fallback_pcm, sr))
        else:
            audio_queue.put((pcm, sr))
    
    threading.Thread(target=tts_worker, daemon=True).start()

def speak_streaming(text, voice=None, lang=DEFAULT_LANG):
    """✅ FIXED: Queue text chunk for immediate streaming TTS using direct Kokoro"""
    if not text or len(text.strip()) < 2:
        return False
    
    # Split long text before streaming TTS
    if len(text.strip()) > 500:
        print("[StreamingTTS] ⚠️ Text too long. Splitting into chunks.")
        import re
        success = True
        for chunk in re.split(r'[.!?]', text):
            if chunk.strip():
                chunk_success = speak_streaming(chunk.strip(), voice, lang)
                success = success and chunk_success
        return success
        
    def streaming_tts_worker():
        try:
            # Ensure model is loaded
            if kokoro_model is None:
                if not load_kokoro_model():
                    return False
            
            # ✅ FIX: Properly handle voice parameter
            selected_voice = voice  # Use provided voice
            if selected_voice is None:
                # Detect voice from language if none provided
                detected_lang = lang or detect(text)
                selected_voice = KOKORO_VOICES.get(detected_lang, KOKORO_DEFAULT_VOICE)
            
            # Generate audio directly using Kokoro model
            try:
                audio_data = kokoro_model.generate(text.strip())
            except Exception as e:
                print(f"[StreamingTTS] ❌ First generation failed: {e}, retrying...")
                time.sleep(0.5)
                try:
                    audio_data = kokoro_model.generate(text.strip())
                except Exception as retry_e:
                    print(f"[StreamingTTS] ❌ Retry also failed: {retry_e}")
                    return False
            
            if audio_data is not None:
                # Normalize and convert to int16
                audio_data = (audio_data * 32767).astype(np.int16)
                
                # Queue immediately
                audio_queue.put((audio_data, 16000))
                
                if DEBUG:
                    print(f"[StreamingTTS] ✅ Queued chunk: '{text[:50]}...' with voice: {selected_voice}")
                
                return True
            else:
                print(f"[StreamingTTS] ❌ No audio generated")
                
        except Exception as e:
            print(f"[StreamingTTS] ❌ Error: {e}")
        
        return False
    
    threading.Thread(target=streaming_tts_worker, daemon=True).start()
    return True

def play_chime():
    """Play notification chime"""
    try:
        from pydub import AudioSegment
        from audio.processing import downsample_audio
        
        audio = AudioSegment.from_wav(CHIME_PATH)
        samples = np.array(audio.get_array_of_samples(), dtype=np.int16)
        
        if audio.channels == 2:
            samples = samples.reshape((-1, 2))
            samples = samples[:, 0]
        
        if audio.frame_rate != SAMPLE_RATE:
            samples = downsample_audio(samples, audio.frame_rate, SAMPLE_RATE)
        
        audio_queue.put((samples, SAMPLE_RATE))
    except Exception as e:
        if DEBUG:
            print(f"[Buddy V2] Chime error: {e}")

def notify_full_duplex_manager_speaking(audio_data):
    """✅ SIMPLE: Notify for audio chunk"""
    try:
        if FULL_DUPLEX_MODE:
            from audio.full_duplex_manager import full_duplex_manager
            if full_duplex_manager and hasattr(full_duplex_manager, 'notify_buddy_speaking'):
                full_duplex_manager.notify_buddy_speaking(audio_data)
                print("[Audio] 🤖 ✅ NOTIFIED: Buddy speaking")
    except Exception as e:
        print(f"[Audio] ❌ Error notifying speaking start: {e}")

def notify_full_duplex_manager_stopped():
    """✅ SIMPLE: Notify when audio stops"""
    try:
        if FULL_DUPLEX_MODE:
            from audio.full_duplex_manager import full_duplex_manager
            if full_duplex_manager and hasattr(full_duplex_manager, 'notify_buddy_stopped_speaking'):
                full_duplex_manager.notify_buddy_stopped_speaking()
                print("[Audio] 🤖 ✅ NOTIFIED: Buddy stopped")
                
                # Clear AEC reference
                from audio.smart_aec import smart_aec
                smart_aec.clear_reference()
                print("[Audio] 🧹 Cleared AEC reference")
    except Exception as e:
        print(f"[Audio] ❌ Error notifying speaking stop: {e}")

def audio_worker():
    """✅ SIMPLE FIX: Audio worker that STOPS IMMEDIATELY on interrupt"""
    global current_audio_playback, playback_start_time
    
    print(f"[Buddy V2] 🎵 Simple Audio Worker started")
    
    while True:
        try:
            item = audio_queue.get(timeout=0.1)
            if item is None:
                break
                
            pcm, sr = item
            
            # ✅ SIMPLE: Check interrupt before playing
            if FULL_DUPLEX_MODE:
                from audio.full_duplex_manager import full_duplex_manager
                if full_duplex_manager and getattr(full_duplex_manager, 'speech_interrupted', False):
                    print("[Audio] 🛑 INTERRUPT - Skipping chunk")
                    audio_queue.task_done()
                    continue
            
            with audio_lock:
                # Notify once when starting
                if FULL_DUPLEX_MODE:
                    notify_full_duplex_manager_speaking(pcm)
                
                if not FULL_DUPLEX_MODE:
                    buddy_talking.set()
                
                playback_start_time = time.time()
                
                try:
                    print(f"[Audio] 🎵 Playing chunk: {len(pcm)} samples")
                    current_audio_playback = sa.play_buffer(pcm.tobytes(), 1, 2, sr)
                    
                    # ✅ CRITICAL: Check for interrupt every 1ms during playback
                    while current_audio_playback and current_audio_playback.is_playing():
                        if FULL_DUPLEX_MODE:
                            try:
                                from audio.full_duplex_manager import full_duplex_manager
                                if full_duplex_manager and getattr(full_duplex_manager, 'speech_interrupted', False):
                                    print("[Audio] ⚡ IMMEDIATE STOP - Interrupt detected!")
                                    current_audio_playback.stop()
                                    
                                    # Clear ALL remaining chunks
                                    cleared = 0
                                    while not audio_queue.empty():
                                        try:
                                            audio_queue.get_nowait()
                                            audio_queue.task_done()
                                            cleared += 1
                                        except queue.Empty:
                                            break
                                    
                                    print(f"[Audio] 🗑️ Cleared {cleared} remaining chunks")
                                    break
                            except Exception:
                                pass
                        
                        time.sleep(0.001)  # Check every 1 millisecond
                    
                    if current_audio_playback and not current_audio_playback.is_playing():
                        print(f"[Audio] ✅ Chunk completed")
                    
                except Exception as playback_err:
                    print(f"[Audio] ❌ Playback error: {playback_err}")
                
                finally:
                    # Clean up
                    try:
                        if current_audio_playback:
                            if current_audio_playback.is_playing():
                                current_audio_playback.stop()
                            current_audio_playback = None
                    except:
                        pass
                    
                    # Check if interrupted after chunk
                    if FULL_DUPLEX_MODE:
                        from audio.full_duplex_manager import full_duplex_manager
                        if full_duplex_manager and getattr(full_duplex_manager, 'speech_interrupted', False):
                            print("[Audio] 🛑 Post-chunk interrupt detected")
                            
                            # Clear remaining queue
                            while not audio_queue.empty():
                                try:
                                    audio_queue.get_nowait()
                                    audio_queue.task_done()
                                except queue.Empty:
                                    break
                            
                            notify_full_duplex_manager_stopped()
                            audio_queue.task_done()
                            continue
                    
                    # Normal completion - notify stopped only if queue empty
                    if FULL_DUPLEX_MODE and audio_queue.empty():
                        from audio.full_duplex_manager import full_duplex_manager
                        is_interrupted = full_duplex_manager and getattr(full_duplex_manager, 'speech_interrupted', False)
                        
                        if not is_interrupted:
                            print("[Audio] 🏁 All chunks completed normally")
                            notify_full_duplex_manager_stopped()
                    
                    if not FULL_DUPLEX_MODE and audio_queue.empty():
                        buddy_talking.clear()
                    
                    playback_start_time = None
                
            audio_queue.task_done()
            
        except queue.Empty:
            continue
            
        except Exception as e:
            print(f"[Audio] ❌ Worker error: {e}")
            try:
                if current_audio_playback:
                    current_audio_playback.stop()
                    current_audio_playback = None
                if FULL_DUPLEX_MODE:
                    notify_full_duplex_manager_stopped()
                else:
                    buddy_talking.clear()
            except:
                pass

def emergency_stop_all_audio():
    """✅ EMERGENCY: Stop ALL audio immediately"""
    global current_audio_playback
    
    try:
        print("[Audio] 🚨 EMERGENCY STOP")
        
        with audio_lock:
            if current_audio_playback:
                if current_audio_playback.is_playing():
                    current_audio_playback.stop()
                    print("[Audio] ⚡ Current chunk STOPPED")
                current_audio_playback = None
        
        cleared = clear_audio_queue()
        
        if not FULL_DUPLEX_MODE:
            buddy_talking.clear()
        
        print(f"[Audio] ⚡ EMERGENCY COMPLETE - Cleared {cleared} chunks")
        
    except Exception as e:
        print(f"[Audio] Emergency stop error: {e}")

def start_audio_worker():
    """Start the audio worker thread"""
    load_kokoro_model()  # Load the model on startup
    threading.Thread(target=audio_worker, daemon=True).start()
    if DEBUG:
        print("[Audio] 🚀 Audio worker thread started")

def is_buddy_talking():
    """Check if Buddy is currently talking"""
    if FULL_DUPLEX_MODE:
        return current_audio_playback is not None and current_audio_playback.is_playing()
    else:
        return buddy_talking.is_set()

def stop_audio_playback():
    """✅ Emergency stop"""
    global current_audio_playback
    
    try:
        with audio_lock:
            if current_audio_playback and current_audio_playback.is_playing():
                current_audio_playback.stop()
                print("[Audio] 🛑 Emergency stop")
                
            current_audio_playback = None
            playback_start_time = None
            
            if FULL_DUPLEX_MODE:
                notify_full_duplex_manager_stopped()
            else:
                buddy_talking.clear()
                
    except Exception as e:
        if DEBUG:
            print(f"[Audio] Emergency stop error: {e}")

def clear_audio_queue():
    """Clear pending audio queue"""
    cleared = 0
    while not audio_queue.empty():
        try:
            audio_queue.get_nowait()
            audio_queue.task_done()
            cleared += 1
        except queue.Empty:
            break
    
    if cleared > 0 and DEBUG:
        print(f"[Audio] 🗑️ Cleared {cleared} pending audio items")
    
    return cleared

def force_buddy_stop_notification():
    """Force notify that Buddy stopped"""
    print("[Audio] 🚨 FORCE notifying Buddy stopped")
    notify_full_duplex_manager_stopped()

def get_audio_stats():
    """Get audio system statistics"""
    return {
        "queue_size": audio_queue.qsize(),
        "is_playing": current_audio_playback is not None and current_audio_playback.is_playing() if current_audio_playback else False,
        "buddy_talking": buddy_talking.is_set(),
        "playback_start_time": playback_start_time,
        "current_time": time.time(),
        "mode": "FULL_DUPLEX" if FULL_DUPLEX_MODE else "HALF_DUPLEX",
        "kokoro_available": kokoro_model is not None,
        "model_path": KOKORO_MODEL_PATH
    }

def start_streaming_response(user_input, current_user, language):
    """Start a streaming response with immediate TTS"""
    pass

def queue_text_chunk(text_chunk, voice=None):
    """Queue a text chunk for immediate TTS processing with fallback"""
    success = speak_streaming(text_chunk, voice)
    if not success:
        print("[TTS] ⚠️ Streaming failed, trying fallback...")
        speak_async("Sorry, there was an audio issue.")
    return success

# Initialize Kokoro model on module load
load_kokoro_model()