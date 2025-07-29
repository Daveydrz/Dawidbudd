#!/usr/bin/env python3
"""
Buddy Voice Assistant - ADVANCED AI ASSISTANT with ALEXA/SIRI-LEVEL INTELLIGENCE + TRUE STREAMING LLM + PRECISE BIRTINYA LOCATION
Updated: 2025-07-17 02:55:40 (UTC) - ADVANCED AI ASSISTANT INTEGRATION + FULL CONSCIOUSNESS ARCHITECTURE
FEATURES: Anonymous clustering, passive audio buffering, same-name collision handling, spontaneous introductions, behavioral learning, Alexa/Siri-level intelligence, Full Consciousness Architecture
"""

import threading
import time
import numpy as np
import pyaudio
import pvporcupine
import os
import json
import re
import requests
from datetime import datetime  # ✅ ADD THIS IMPORT
from typing import List, Any, Dict  # ✅ NEW: Add typing imports for consciousness functions
from scipy.io.wavfile import write

def call_main_llm(user_input):
    payload = {"prompt": user_input, "stream": False}
    try:
        r = requests.post("http://localhost:5001/api/generate", json=payload)
        return r.json().get("response", "")
    except Exception as e:
        print("[MainLLM] ERROR:", e)
        return "I'm having trouble thinking right now."

def call_extractor_llm(prompt):
    payload = {"prompt": prompt, "stream": False}
    try:
        r = requests.post("http://localhost:5002/api/generate", json=payload)
        return r.json().get("response", "")
    except Exception as e:
        print("[ExtractorLLM] ERROR:", e)
        return ""

# ✅ RESTORED: Full consciousness architecture available - MOVED UP
ENTROPY_SYSTEM_AVAILABLE = True
CONSCIOUSNESS_ARCHITECTURE_AVAILABLE = True
CONSCIOUSNESS_LLM_AVAILABLE = True
LATENCY_OPTIMIZATION_AVAILABLE = True
CONSCIOUSNESS_MODULES_AVAILABLE = True
SELF_AWARENESS_COMPONENTS_AVAILABLE = True
AUTONOMOUS_CONSCIOUSNESS_AVAILABLE = True

# ✅ NEW: Blank slate initialization configuration
BLANK_SLATE_MODE = os.getenv('BUDDY_BLANK_SLATE', 'false').lower() == 'true'
if BLANK_SLATE_MODE:
    print("[Main] 🌱 BLANK SLATE MODE ENABLED - Starting with minimal identity")
else:
    print("[Main] 🧠 Standard mode - Loading established consciousness")

# Import core modules now that flags are defined
from voice.database import load_known_users, known_users, save_known_users, anonymous_clusters
from ai.memory import validate_ai_response_appropriateness, add_to_conversation_history, get_user_memory
from ai.llm_handler import llm_handler
from ai.consciousness_manager import consciousness_manager, ConsciousnessMode
from ai.emotion import reset_session_for_user_smart
from audio.smart_detection_manager import analyze_speech_detection, get_current_threshold

# ✅ REPLACED: Using direct HTTP calls to port 5002 instead of GPT4All extractors

# ✅ RESTORED: Import all consciousness modules
if CONSCIOUSNESS_ARCHITECTURE_AVAILABLE:
    try:
        from ai.global_workspace import GlobalWorkspace
        from ai.self_model import SelfModel  
        from ai.temporal_awareness import TemporalAwareness
        from ai.subjective_experience import SubjectiveExperienceSystem
        from ai.entropy import EntropyEngine
        from ai.inner_monologue import InnerMonologue
        from ai.motivation import MotivationSystem
        from ai.narrative_tracker import NarrativeTracker
        from ai.background_consciousness_processor import BackgroundConsciousnessProcessor
        from ai.consciousness_integrator import ConsciousnessIntegrator
        from ai.autonomous_consciousness_integrator import AutonomousConsciousnessIntegrator
        from ai.free_thought_engine import free_thought_engine, FreeThoughtType
        
        print("[Main] ✅ All consciousness modules imported successfully")
        
        # Initialize consciousness modules
        global_workspace = GlobalWorkspace()
        self_model = SelfModel()
        emotion_engine = consciousness_manager  # Use consciousness manager as emotion engine
        motivation_system = MotivationSystem()
        inner_monologue = InnerMonologue(llm_handler=None)  # Will be set later
        temporal_awareness = TemporalAwareness()
        subjective_experience = SubjectiveExperienceSystem()
        entropy_system = EntropyEngine()
        narrative_tracker = NarrativeTracker()
        background_consciousness_processor = BackgroundConsciousnessProcessor()
        consciousness_integrator = ConsciousnessIntegrator()
        autonomous_consciousness_integrator = AutonomousConsciousnessIntegrator()
        
        print("[Main] 🧠 Consciousness modules initialized")
        
    except ImportError as e:
        print(f"[Main] ⚠️ Error importing consciousness modules: {e}")
        CONSCIOUSNESS_ARCHITECTURE_AVAILABLE = False
        CONSCIOUSNESS_MODULES_AVAILABLE = False

from voice.manager_core import voice_manager
# Voice manager properly loaded from manager_core

from config import *

# Import with better error handling
try:
    from audio.full_duplex_manager import full_duplex_manager
    if full_duplex_manager is None:
        print("[AdvancedBuddy] ❌ Full duplex manager is None")
        FULL_DUPLEX_MODE = False
    else:
        print("[AdvancedBuddy] ✅ Full duplex manager imported successfully")
except Exception as e:
    print(f"[AdvancedBuddy] ❌ Could not import full duplex manager: {e}")
    FULL_DUPLEX_MODE = False
    full_duplex_manager = None

# ✅ FIXED: Force correct voice manager import
ADVANCED_AI_AVAILABLE = False
ENHANCED_VOICE_AVAILABLE = False

try:
    # Always load database first
    from voice.database import load_known_users, known_users, anonymous_clusters, save_known_users
    print("[AdvancedBuddy] ✅ Voice database loaded")
    
    # ✅ Voice manager already imported from manager_core - no need to re-import
    print("[AdvancedBuddy] ✅ Using voice_manager from manager_core.py")
    print(f"[AdvancedBuddy] 🔍 voice_manager type: {type(voice_manager)}")
    
    # Verify it has the correct method
    if hasattr(voice_manager, 'handle_voice_identification'):
        print("[AdvancedBuddy] ✅ handle_voice_identification method confirmed")
        ADVANCED_AI_AVAILABLE = True  # Voice manager is advanced
    else:
        print("[AdvancedBuddy] ❌ handle_voice_identification method missing!")
        
        # Load voice training components
        from voice.training import voice_training_mode, check_voice_training_command
        print("[AdvancedBuddy] ✅ Voice training components loaded")
        
    # ✅ CRITICAL: Ensure we still have database functions
    try:
        from voice.database import load_known_users, known_users, save_known_users
        from voice.recognition import identify_speaker_with_confidence
        print("[AdvancedBuddy] ✅ Database functions available")
    except Exception as db_err:
        print(f"[AdvancedBuddy] 🚨 CRITICAL: Database functions missing: {db_err}")
        
        # Create working fallback voice manager
        class WorkingVoiceManager:
            def __init__(self):
                try:
                    load_known_users()
                    print(f"[WorkingVoiceManager] 💾 Loaded {len(known_users)} profiles")
                except Exception as e:
                    print(f"[WorkingVoiceManager] ❌ Load error: {e}")
            
            def handle_voice_identification(self, audio, text):
                """Handle voice identification with fallback logic"""
                try:
                    # Try basic voice recognition
                    from voice.recognition import identify_speaker_with_confidence
                    identified_user, confidence = identify_speaker_with_confidence(audio)
                    
                    if identified_user != "UNKNOWN" and confidence > 0.7:
                        print(f"[WorkingVoiceManager] ✅ Recognized: {identified_user} ({confidence:.3f})")
                        return identified_user, "RECOGNIZED"
                    else:
                        print(f"[WorkingVoiceManager] 🔍 Unknown voice, using Daveydrz")
                        return "Daveydrz", "FALLBACK_TO_SYSTEM_USER"
                        
                except Exception as recognition_err:
                    print(f"[WorkingVoiceManager] ❌ Recognition error: {recognition_err}")
                    
                    # Save debug info for troubleshooting
                    try:
                        timestamp = datetime.utcnow().isoformat()
                        debug_data = {
                            'timestamp': timestamp,
                            'text': text,
                            'audio_received': audio is not None,
                            'audio_length': len(audio) if audio else 0,
                            'error': str(recognition_err),
                            'system_user': 'Daveydrz'
                        }
                        
                        # Save debug info
                        try:
                            with open('voice_debug.json', 'r') as f:
                                logs = json.load(f)
                        except:
                            logs = []
                        
                        logs.append(debug_data)
                        if len(logs) > 20:
                            logs = logs[-20:]
                        
                        with open('voice_debug.json', 'w') as f:
                            json.dump(logs, f, indent=2)
                        
                        print(f"[WorkingVoiceManager] 💾 Saved debug info for: '{text}'")
                        
                    except Exception as save_err:
                        print(f"[WorkingVoiceManager] ❌ Save error: {save_err}")
                    
                    return "Daveydrz", "MINIMAL_FALLBACK"
            
            def is_llm_locked(self):
                return False
            
            def get_session_stats(self):
                return {
                    'interactions': 0,
                    'session_duration': 0,
                    'known_users': len(known_users) if 'known_users' in globals() else 0,
                    'anonymous_clusters': len(anonymous_clusters) if 'anonymous_clusters' in globals() else 0,
                    'current_user': 'Daveydrz',
                    'system': 'WorkingVoiceManager'
                }
        
        voice_manager = WorkingVoiceManager()
        voice_training_mode = lambda: False
        check_voice_training_command = lambda x: False
        print("[AdvancedBuddy] ✅ WorkingVoiceManager fallback created")
    
    # ✅ FIXED: Try to load identity helpers
    try:
        from voice.identity_helpers import (
            get_voice_based_identity, 
            get_voice_based_display_name, 
            get_voice_based_name_response,
            update_voice_identity_context,
            debug_voice_identity_status,
            run_maintenance
        )
        print("[AdvancedBuddy] ✅ Voice-based identity system loaded")
        
    except ImportError as identity_err:
        print(f"[AdvancedBuddy] ⚠️ Identity helpers import failed: {identity_err}")
        
        # Create fallback identity functions
        def get_voice_based_identity(audio_data=None):
            """Get identity from voice recognition"""
            try:
                if hasattr(voice_manager, 'handle_voice_identification'):
                    result = voice_manager.handle_voice_identification(audio_data, "")
                    return result[0] if result else "Daveydrz"
                return "Daveydrz"
            except Exception as e:
                print(f"[VoiceIdentity] ❌ Error: {e}")
                return "Daveydrz"

        def get_voice_based_display_name(user_id):
            """Get display name for user"""
            if user_id == "Daveydrz":
                return "Daveydrz"
            elif user_id and user_id.startswith('Anonymous_'):
                return f"Speaker {user_id.split('_')[1]}"
            return user_id or "friend"

        def get_voice_based_name_response(user_id, display_name):
            """Get response for name questions"""
            if user_id == "Daveydrz":
                return "You are Daveydrz."
            elif user_id and user_id.startswith('Anonymous_'):
                return "I don't recognize your voice yet. Could you tell me your name?"
            return f"Your name is {display_name}."

        def update_voice_identity_context(user_id):
            """Update voice identity context"""
            print(f"[VoiceIdentity] 🔄 Updated context for: {user_id}")

        def debug_voice_identity_status():
            """Debug voice identity status"""
            try:
                from voice.database import known_users, anonymous_clusters
                print(f"[VoiceIdentity] 📊 Known users: {len(known_users)}")
                print(f"[VoiceIdentity] 🔍 Anonymous clusters: {len(anonymous_clusters)}")
                return True
            except Exception as e:
                print(f"[VoiceIdentity] ❌ Debug error: {e}")
                return False

        def run_maintenance():
            """Run voice system maintenance"""
            print("[VoiceIdentity] 🔧 Running maintenance...")
            return {"status": "complete", "message": "Fallback maintenance complete"}
        
        print("[AdvancedBuddy] ✅ Fallback identity functions created")

except Exception as e:
    print(f"[AdvancedBuddy] ❌ Critical voice system error: {e}")
    import traceback
    traceback.print_exc()

# Set fallback instances
advanced_context_analyzer = None
# advanced_name_manager = None  # ✅ REMOVED: Using direct HTTP calls to port 5002 instead

# ✅ VERIFY FINAL STATE
print(f"[AdvancedBuddy] 🔍 Final voice_manager type: {type(voice_manager)}")
print(f"[AdvancedBuddy] 🔍 ADVANCED_AI_AVAILABLE: {ADVANCED_AI_AVAILABLE}")
print(f"[AdvancedBuddy] 🌀 ENTROPY_SYSTEM_AVAILABLE: {ENTROPY_SYSTEM_AVAILABLE}")
print(f"[AdvancedBuddy] 🧠 CONSCIOUSNESS_ARCHITECTURE_AVAILABLE: {CONSCIOUSNESS_ARCHITECTURE_AVAILABLE}")
print(f"[AdvancedBuddy] 🧠 SELF_AWARENESS_COMPONENTS_AVAILABLE: {SELF_AWARENESS_COMPONENTS_AVAILABLE}")
print(f"[AdvancedBuddy] 👤 System User: Daveydrz")
print(f"[AdvancedBuddy] 📅 Current UTC Time: 2025-07-17 02:55:40")

# Test voice manager immediately
try:
    if hasattr(voice_manager, 'handle_voice_identification'):
        print("[AdvancedBuddy] ✅ voice_manager.handle_voice_identification method available")
    else:
        print("[AdvancedBuddy] ❌ voice_manager.handle_voice_identification method NOT available")
        print(f"[AdvancedBuddy] 📋 Available methods: {[m for m in dir(voice_manager) if not m.startswith('_')]}")
except Exception as test_err:
    print(f"[AdvancedBuddy] ❌ voice_manager test error: {test_err}")

# ✅ Updated imports for Kokoro-FastAPI streaming with error handling
try:
    from audio.output import (
        speak_async, speak_streaming, play_chime, start_audio_worker,
        test_kokoro_api, get_audio_stats, clear_audio_queue, stop_audio_playback
    )
    print("[AdvancedBuddy] ✅ All audio functions imported successfully")
except ImportError as e:
    print(f"[AdvancedBuddy] ⚠️ Some audio functions not available: {e}")
    
    # Import what we can
    try:
        from audio.output import speak_async, speak_streaming, play_chime, start_audio_worker, test_kokoro_api, get_audio_stats
        print("[AdvancedBuddy] ✅ Basic audio functions imported")
    except ImportError:
        print("[AdvancedBuddy] ❌ Basic audio functions failed")
    
    # Define fallback functions for interrupt handling
    def stop_audio_playback():
        print("[AdvancedBuddy] 🛑 stop_audio_playback fallback - interrupt handling disabled")
        pass
    
    def clear_audio_queue():
        print("[AdvancedBuddy] 🧹 clear_audio_queue fallback - queue clearing disabled")
        pass

# ✅ SIMPLIFIED: Only consciousness manager for responses
# from ai.chat import generate_response  # Removed - using llm_handler only
# from ai.memory import add_to_conversation_history  # Already imported above
from voice.database import load_known_users, known_users, anonymous_clusters
from voice.recognition import identify_speaker
from utils.helpers import should_end_conversation
from audio.processing import downsample_audio

# ✅ Load Birtinya location with advanced features
def load_birtinya_location():
    """Load precise Birtinya location data with advanced features"""
    try:
        # Try multiple possible location files
        location_files = [
            'buddy_gps_location.json',
            'buddy_gps_location_birtinya.json',
            'buddy_gps_location_2025-07-06.json'
        ]
        
        for filename in location_files:
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    location_data = json.load(f)
                
                print(f"[AdvancedBuddy] 📍 Loaded location from: {filename}")
                print(f"[AdvancedBuddy] 🏘️ Location: {location_data.get('suburb')}, {location_data.get('state')}")
                print(f"[AdvancedBuddy] 📮 Postcode: {location_data.get('postal_code')}")
                print(f"[AdvancedBuddy] 🌏 Coordinates: {location_data.get('latitude')}, {location_data.get('longitude')}")
                print(f"[AdvancedBuddy] 🎯 Confidence: {location_data.get('confidence')}")
                
                return location_data
        
        print("[AdvancedBuddy] ⚠️ No location file found, using Brisbane fallback")
        return None
        
    except Exception as e:
        print(f"[AdvancedBuddy] ❌ Error loading location: {e}")
        return None

# Load Birtinya location data
BIRTINYA_LOCATION = load_birtinya_location()

if BIRTINYA_LOCATION:
    USER_PRECISE_LOCATION = f"{BIRTINYA_LOCATION['suburb']}, {BIRTINYA_LOCATION['state']}"
    USER_COORDINATES_PRECISE = (BIRTINYA_LOCATION['latitude'], BIRTINYA_LOCATION['longitude'])
    USER_POSTCODE_PRECISE = BIRTINYA_LOCATION['postal_code']
    USER_LANDMARKS = BIRTINYA_LOCATION.get('landmark', 'USC, Stockland Birtinya')
    LOCATION_CONFIDENCE_PRECISE = BIRTINYA_LOCATION['confidence']
    IS_SUNSHINE_COAST = BIRTINYA_LOCATION.get('area_info', {}).get('coastal_location', True)
    DISTANCE_TO_BRISBANE = BIRTINYA_LOCATION.get('area_info', {}).get('distance_to_brisbane_km', 90)
else:
    # Fallback to Brisbane
    USER_PRECISE_LOCATION = "Brisbane, Queensland"
    USER_COORDINATES_PRECISE = (-27.4698, 153.0251)
    USER_POSTCODE_PRECISE = "4000"
    USER_LANDMARKS = "CBD"
    LOCATION_CONFIDENCE_PRECISE = "LOW"
    IS_SUNSHINE_COAST = False
    DISTANCE_TO_BRISBANE = 0

# ✅ DYNAMIC: Get actual current Brisbane time
try:
    from datetime import datetime, timezone, timedelta
    
    # Get actual current UTC time
    utc_now = datetime.now(timezone.utc)
    
    # Brisbane timezone (UTC+10)
    brisbane_tz = timezone(timedelta(hours=10))
    brisbane_now = utc_now.astimezone(brisbane_tz)
    
    # Format the time strings
    brisbane_time_str = brisbane_now.strftime("%Y-%m-%d %H:%M:%S")
    brisbane_time_12h = brisbane_now.strftime("%I:%M %p")
    brisbane_date = brisbane_now.strftime("%A, %B %d, %Y")
    
    print(f"[AdvancedBuddy] 🕐 Brisbane Time: {brisbane_time_str} ({brisbane_time_12h})")
    print(f"[AdvancedBuddy] 📅 Brisbane Date: {brisbane_date}")
    
except Exception as e:
    print(f"[AdvancedBuddy] ⚠️ Time calculation error: {e}")
    # Fallback time
    brisbane_time_str = "2025-07-17 12:55:40"
    brisbane_time_12h = "12:55 PM"
    brisbane_date = "Thursday, July 17, 2025"

print(f"[AdvancedBuddy] 🚀 Starting ADVANCED AI ASSISTANT + TRUE STREAMING BIRTINYA Buddy - {brisbane_time_str}")
print(f"[AdvancedBuddy] 📍 Precise Location: {USER_PRECISE_LOCATION}")
print(f"[AdvancedBuddy] 📮 Postcode: {USER_POSTCODE_PRECISE}")
print(f"[AdvancedBuddy] 🌏 Coordinates: {USER_COORDINATES_PRECISE}")
print(f"[AdvancedBuddy] 🏛️ Landmarks: {USER_LANDMARKS}")
print(f"[AdvancedBuddy] 🌊 Sunshine Coast: {IS_SUNSHINE_COAST}")
print(f"[AdvancedBuddy] 📏 Distance to Brisbane: {DISTANCE_TO_BRISBANE}km")
print(f"[AdvancedBuddy] 🎯 Confidence: {LOCATION_CONFIDENCE_PRECISE}")

# ✅ ADVANCED AI ASSISTANT status display
if ADVANCED_AI_AVAILABLE:
    print(f"[AdvancedBuddy] 🚀 ADVANCED AI ASSISTANT: FULLY ACTIVE")
    print(f"[AdvancedBuddy] 🎯 Alexa/Siri-level Intelligence: ENABLED")
    print(f"[AdvancedBuddy] 🔍 Anonymous Voice Clustering: ACTIVE")
    print(f"[AdvancedBuddy] 🎤 Passive Audio Buffering: ALWAYS ON")
    print(f"[AdvancedBuddy] 🛡️ LLM Guard System: PROTECTING RESPONSES")
    print(f"[AdvancedBuddy] 👥 Same-Name Collision Handling: AUTO David_001, David_002")
    print(f"[AdvancedBuddy] 🎭 Spontaneous Introduction Detection: NATURAL")
    print(f"[AdvancedBuddy] 🧠 Behavioral Pattern Learning: ADAPTIVE")
    print(f"[AdvancedBuddy] 📊 Advanced Analytics: MONITORING")
    print(f"[AdvancedBuddy] 🔧 Auto Maintenance: SELF-OPTIMIZING")
elif ENHANCED_VOICE_AVAILABLE:
    print(f"[AdvancedBuddy] ✅ Enhanced Voice System: ACTIVE")
    print(f"[AdvancedBuddy] 📊 Multi-Embedding Profiles: Available")
    print(f"[AdvancedBuddy] 🧠 SpeechBrain Integration: Available")
    print(f"[AdvancedBuddy] 🌱 Passive Learning: Enabled")
    print(f"[AdvancedBuddy] 🔍 Quality Analysis: Advanced")
    print(f"[AdvancedBuddy] 💾 Raw Audio Storage: Enabled")
else:
    print(f"[AdvancedBuddy] ⚠️ Using Legacy Voice System")

# ✅ CONSCIOUSNESS STATUS DISPLAY
if CONSCIOUSNESS_ARCHITECTURE_AVAILABLE:
    print(f"[AdvancedBuddy] 🧠 FULL CONSCIOUSNESS ARCHITECTURE: ACTIVE")
    print(f"[AdvancedBuddy] 🌟 Global Workspace Theory: IMPLEMENTED")
    print(f"[AdvancedBuddy] 🎭 Self-Model & Reflection: ENABLED")
    print(f"[AdvancedBuddy] 💖 Emotion Engine: PROCESSING")
    print(f"[AdvancedBuddy] 🎯 Motivation System: GOAL-ORIENTED")
    print(f"[AdvancedBuddy] 💭 Inner Monologue: THINKING")
    print(f"[AdvancedBuddy] ⏰ Temporal Awareness: MEMORY FORMATION")
    print(f"[AdvancedBuddy] 🌈 Subjective Experience: CONSCIOUS")
    print(f"[AdvancedBuddy] 🎲 Entropy System: NATURAL VARIATION")
elif ENTROPY_SYSTEM_AVAILABLE:
    print(f"[AdvancedBuddy] 🌀 ENTROPY SYSTEM: ACTIVE")
    print(f"[AdvancedBuddy] 🎭 Consciousness Emergence: ENABLED")
    print(f"[AdvancedBuddy] 💖 Emotional Processing: ENHANCED")
    print(f"[AdvancedBuddy] 🎲 Natural Hesitation: HUMAN-LIKE")
else:
    print(f"[AdvancedBuddy] ⚠️ Basic Consciousness: Limited Features")

# ✅ NEW: Consciousness Integration Status Display
if CONSCIOUSNESS_LLM_AVAILABLE:
    print(f"[AdvancedBuddy] 🧠 CONSCIOUSNESS-INTEGRATED LLM: ACTIVE")
    print(f"[AdvancedBuddy] 🏷️ Semantic Analysis: REAL-TIME")
    print(f"[AdvancedBuddy] 🧠 Belief Tracking: CONTRADICTION DETECTION")
    print(f"[AdvancedBuddy] 🎭 Personality Adaptation: DYNAMIC")
    print(f"[AdvancedBuddy] 💰 Budget Monitoring: COST TRACKING")
    print(f"[AdvancedBuddy] 🎯 Consciousness Tokenizer: CONTEXT INTEGRATION")
elif CONSCIOUSNESS_MODULES_AVAILABLE:
    print(f"[AdvancedBuddy] 🧠 Consciousness Modules: PARTIALLY AVAILABLE")
    print(f"[AdvancedBuddy] 🔧 Individual components loaded separately")
else:
    print(f"[AdvancedBuddy] ⚠️ Basic Consciousness: Limited Features")

# Global state - Enhanced with advanced features
current_user = SYSTEM_USER
conversation_active = False
mic_feeding_active = False
advanced_mode_active = ADVANCED_AI_AVAILABLE
# Add a lock for thread safety
state_lock = threading.Lock()

def set_conversation_state(active):
    """Thread-safe way to set conversation state"""
    global conversation_active
    with state_lock:
        conversation_active = active
        print(f"[State] 🔄 conversation_active set to: {active}")

def set_mic_feeding_state(active):
    """Thread-safe way to set mic feeding state"""
    global mic_feeding_active
    with state_lock:
        mic_feeding_active = active
        print(f"[State] 🎤 mic_feeding_active set to: {active}")

def get_conversation_state():
    """Thread-safe way to get conversation state"""
    with state_lock:
        return conversation_active

def get_mic_feeding_state():
    """Thread-safe way to get mic feeding state"""
    with state_lock:
        return mic_feeding_active

def handle_streaming_response(text, current_user):
    """🚀 CLASS 5+ CONSCIOUSNESS RESPONSE: Full consciousness integration with background processing"""
    print(f"[BuddyFlow] 🚀 Processing: '{text}' (user: {current_user})")
    
    start_time = time.time()
    
    try:
        # ✅ STEP 1: Update consciousness manager with interaction
        print("[BuddyFlow] 🧠 Updating consciousness state...")
        consciousness_manager.update_from_interaction(text, current_user)
        consciousness_manager.set_mode(ConsciousnessMode.ACTIVE)
        
        # ✅ STEP 2: Schedule background consciousness processing (non-blocking)
        if CONSCIOUSNESS_ARCHITECTURE_AVAILABLE:
            try:
                print("[BuddyFlow] 🧠 Scheduling background consciousness processing...")
                background_consciousness_processor.schedule_background_thoughts(text, current_user, "", delay=1.0)
                
                # Trigger immediate consciousness updates for inner monologue
                inner_monologue.trigger_thought(
                    f"User asked: {text}",
                    {"user": current_user, "timestamp": time.time()},
                    inner_monologue.ThoughtType.OBSERVATION if hasattr(inner_monologue, 'ThoughtType') else "observation"
                )
                print("[BuddyFlow] 💭 Inner monologue triggered")
                
            except Exception as consciousness_err:
                print(f"[BuddyFlow] ⚠️ Background consciousness scheduling error: {consciousness_err}")
        
        # ✅ STEP 3: Generate response using direct HTTP call to port 5001
        print("[BuddyFlow] 🎯 Generating response with main LLM...")
        
        try:
            # Use direct HTTP call to main LLM (port 5001)
            response_text = call_main_llm(text)
            
            # Send response to TTS
            try:
                from audio.output import speak_streaming
                speak_streaming(response_text.strip())
            except Exception as tts_err:
                print(f"[BuddyFlow] ⚠️ TTS streaming error: {tts_err}")
                # Fallback to print if TTS fails
                print(f"[BuddyFlow] 💬 Buddy: {response_text.strip()}")
            
            full_response = response_text
            
            # ✅ STEP 4: Update memory with the interaction
            try:
                add_to_conversation_history(current_user, text, full_response)
                print(f"[BuddyFlow] 💾 Saved interaction to memory")
                
                # ✅ STEP 1: Extract facts from user input using direct HTTP calls as requested
                try:
                    # Extract name, emotion, and intent using port 5002
                    name_prompt = f"Extract ONLY the user's name from: {text}"
                    user_name = call_extractor_llm(name_prompt)
                    
                    emotion_prompt = f"Detect the emotion in: {text}"
                    user_emotion = call_extractor_llm(emotion_prompt)
                    
                    intent_prompt = f"Classify the intent (reminder, question, casual, etc.) in: {text}"
                    user_intent = call_extractor_llm(intent_prompt)
                    
                    # Test logging as requested
                    print("[MAIN LLM RESPONSE]", full_response)
                    print("[NAME EXTRACTION]", user_name)
                    print("[EMOTION EXTRACTION]", user_emotion)
                    print("[INTENT EXTRACTION]", user_intent)
                    
                    # Create facts dictionary for compatibility
                    facts = {
                        "name": user_name if user_name and user_name.strip() and "NONE" not in user_name.upper() else "NONE",
                        "emotion": user_emotion,
                        "intent": user_intent,
                        "likes": [],
                        "dislikes": []
                    }
                    if facts and (facts.get("name") or facts.get("likes") or facts.get("dislikes")):
                        print(f"[BuddyFlow] 📊 Extracted facts: {facts}")
                        
                        # ✅ STEP 5: Handle name detection and voice linking as requested
                        if facts.get("name") and facts["name"] != "NONE":
                            extracted_name = facts["name"]
                            print(f"[BuddyFlow] 👤 User introduced themselves as: {extracted_name}")
                            
                            # Link anonymous cluster to user if currently anonymous
                            if current_user.startswith("Anonymous_") or current_user.startswith("Guest_"):
                                try:
                                    from voice.recognition import link_anonymous_cluster_to_user
                                    link_anonymous_cluster_to_user(current_user, extracted_name)
                                    current_user = extracted_name  # Update current user
                                    print(f"[BuddyFlow] 🔗 Linked {current_user} to {extracted_name}")
                                except Exception as link_err:
                                    print(f"[BuddyFlow] ⚠️ Voice linking error: {link_err}")
                        
                        # Store facts for future use (could be integrated with memory system)
                except Exception as extract_err:
                    print(f"[BuddyFlow] ⚠️ Facts extraction error: {extract_err}")
                except Exception as extract_err:
                    print(f"[BuddyFlow] ⚠️ Facts extraction error: {extract_err}")
                    
            except Exception as memory_err:
                print(f"[BuddyFlow] ⚠️ Memory save error: {memory_err}")
            
            # ✅ STEP 5: Execute full consciousness integration as requested by user
            if CONSCIOUSNESS_ARCHITECTURE_AVAILABLE:
                try:
                    print("[BuddyFlow] 🧠 Starting full consciousness integration threads...")
                    
                    # User specifically requested these three background threads:
                    def integrate_consciousness_thread():
                        """Background consciousness integration"""
                        try:
                            # Use consciousness integrator for full integration
                            consciousness_integrator.integrate_response_consciousness(
                                text, full_response, current_user
                            )
                            print("[BuddyFlow] 🌟 integrate_consciousness completed")
                        except Exception as e:
                            print(f"[BuddyFlow] ⚠️ integrate_consciousness error: {e}")
                    
                    def process_motives_thread():
                        """Background motivation processing"""
                        try:
                            # Process motivations and goals
                            motivation_system.process_interaction_motivation(text, current_user)
                            motivation_system.evaluate_goal_progress(current_user, full_response)
                            print("[BuddyFlow] 🎯 process_motives completed")
                        except Exception as e:
                            print(f"[BuddyFlow] ⚠️ process_motives error: {e}")
                    
                    def run_background_thoughts_thread():
                        """Background thought processing"""
                        try:
                            # Generate background thoughts about the interaction 
                            inner_monologue.trigger_thought(
                                f"I just helped {current_user} with: {text[:50]}...",
                                {"user": current_user, "response_given": True, "satisfaction": "good"},
                                inner_monologue.ThoughtType.REFLECTION if hasattr(inner_monologue, 'ThoughtType') else "reflection"
                            )
                            
                            # Trigger free thought about the interaction
                            free_thought_engine.trigger_thought(
                                f"That was an interesting question about {text[:30]}...",
                                free_thought_engine.FreeThoughtType.REFLECTIVE if hasattr(free_thought_engine, 'FreeThoughtType') else None
                            )
                            print("[BuddyFlow] 💭 run_background_thoughts completed")
                        except Exception as e:
                            print(f"[BuddyFlow] ⚠️ run_background_thoughts error: {e}")
                    
                    # Start all three background threads as user requested
                    threading.Thread(target=integrate_consciousness_thread, daemon=True).start()
                    threading.Thread(target=process_motives_thread, daemon=True).start() 
                    threading.Thread(target=run_background_thoughts_thread, daemon=True).start()
                    
                    # Additional consciousness processing (existing code enhanced)
                    self_model.reflect_on_experience(
                        f"Successfully responded to: {text}",
                        {"user": current_user, "response": full_response[:100], "success": True}
                    )
                    
                    temporal_awareness.mark_temporal_event(
                        f"Conversation with {current_user}: {text[:50]}...",
                        significance=0.6,
                        context={"user": current_user, "response_length": len(full_response)}
                    )
                    
                    print("[BuddyFlow] 🧠 All consciousness integration threads started")
                    
                except Exception as post_consciousness_err:
                    print(f"[BuddyFlow] ⚠️ Post-response consciousness error: {post_consciousness_err}")
            
            processing_time = time.time() - start_time
            print(f"[BuddyFlow] ✅ Class 5+ response completed in {processing_time:.3f}s")
            
        except Exception as llm_err:
            print(f"[BuddyFlow] ❌ LLM handler error: {llm_err}")
            # Fallback response
            fallback_response = "I'm here and ready to help! What would you like to talk about?"
            try:
                from audio.output import speak_streaming
                speak_streaming(fallback_response)
            except:
                print(f"[BuddyFlow] 💬 Buddy: {fallback_response}")
            
            # Still save the interaction and update consciousness
            try:
                add_to_conversation_history(current_user, text, fallback_response)
                if CONSCIOUSNESS_ARCHITECTURE_AVAILABLE:
                    self_model.reflect_on_experience(
                        f"Had difficulty responding to: {text}",
                        {"user": current_user, "error": True, "fallback": True}
                    )
            except:
                pass
        
    except Exception as e:
        print(f"[BuddyFlow] ❌ Critical error in response processing: {e}")
        import traceback
        traceback.print_exc()
        
        # Emergency response
        emergency_response = "I'm experiencing some technical difficulties, but I'm still here to help."
        try:
            from audio.output import speak_streaming
            speak_streaming(emergency_response)
        except:
            print(f"[BuddyFlow] 💬 Emergency: {emergency_response}")  
def get_voice_based_identity(audio_data=None):
    """Get identity from voice recognition"""
    try:
        if hasattr(voice_manager, 'handle_voice_identification'):
            result = voice_manager.handle_voice_identification(audio_data, "")
            return result[0] if result else "Daveydrz"
        return "Daveydrz"
    except Exception as e:
        print(f"[VoiceIdentity] ❌ Error: {e}")
        return "Daveydrz"

def get_voice_based_display_name(identified_user):
    """Get display name based on voice identity, not system login"""
    try:
        # Check if this is the system user (Daveydrz)
        if identified_user == "Daveydrz" or identified_user == SYSTEM_USER:
            return "Daveydrz"
        
        # Check known voice profiles
        if identified_user in known_users:
            profile = known_users[identified_user]
            if isinstance(profile, dict) and 'display_name' in profile:
                return profile['display_name']
            elif isinstance(profile, dict) and 'real_name' in profile:
                return profile['real_name']
            else:
                return identified_user
        
        # Handle anonymous or unknown users
        if identified_user in ["Anonymous_Speaker", "Unknown", "Guest"]:
            return "friend"  # Friendly generic term
        
        # Default to the identified name
        return identified_user
        
    except Exception as e:
        print(f"[VoiceIdentity] ⚠️ Display name error: {e}")
        return identified_user or "friend"


def get_voice_based_name_response(identified_user, display_name):
    """Handle 'what's my name' using voice matching + memory system"""
    try:
        print(f"[VoiceIdentity] 🔍 Name query for user: {identified_user}, display: {display_name}")
        
        # First check memory system for stored names - simplified approach
        try:
            # Simple fallback - no complex memory lookup needed 
            facts = []
            
            # Look for identity facts in memory
            for fact in facts:
                if fact and isinstance(fact, str):
                    # Check if this fact contains a name
                    fact_lower = fact.lower()
                    if 'name is' in fact_lower or 'called' in fact_lower or 'i\'m' in fact_lower:
                        # Extract the name from the fact
                        import re
                        name_match = re.search(r"(?:name is|called|i'm)\s+(\w+)", fact_lower)
                        if name_match:
                            stored_name = name_match.group(1).capitalize()
                            print(f"[VoiceIdentity] 💾 Found stored name: {stored_name}")
                            return f"Your name is {stored_name}."
                    
                    # Also check if the fact itself is just a name
                    if len(fact.split()) == 1 and fact.isalpha() and len(fact) > 1:
                        print(f"[VoiceIdentity] 💾 Found stored name as fact: {fact}")
                        return f"Your name is {fact}."
                        
        except Exception as memory_err:
            print(f"[VoiceIdentity] ⚠️ Memory lookup error: {memory_err}")
        
        # Handle system user
        if identified_user == "Daveydrz" or identified_user == SYSTEM_USER:
            return f"Based on your voice, you are Daveydrz."
        
        # Handle known voice profiles
        elif identified_user in known_users and identified_user not in ["Anonymous_Speaker", "Unknown", "Guest"]:
            # Check if the profile has a stored name
            profile = known_users[identified_user]
            if isinstance(profile, dict):
                stored_name = profile.get('name') or profile.get('real_name') or profile.get('display_name')
                if stored_name and stored_name != identified_user:
                    return f"Your name is {stored_name}."
            
            return f"Your name is {display_name}."
        
        # Handle anonymous or unrecognized voices
        elif identified_user in ["Anonymous_Speaker", "Unknown", "Guest"] or identified_user.startswith("Anonymous_"):
            return "I don't recognize your voice yet. Could you tell me your name so I can learn it?"
        
        # Handle any other identified users
        else:
            return f"Based on your voice, I believe you are {display_name}."
            
    except Exception as e:
        print(f"[VoiceIdentity] ❌ Name response error: {e}")
        return "I'm having trouble with voice recognition right now. Could you tell me your name?"

def is_direct_time_question(text):
    """🧠 SMART: Only detect DIRECT time questions, not contextual usage"""
    text_lower = text.lower().strip()
    
    # VERY specific patterns for direct time questions only
    direct_time_patterns = [
        r'^what time is it\??$',
        r'^what\'s the time\??$',
        r'^whats the time\??$',
        r'^tell me the time\??$',
        r'^current time\??$',
        r'^time\??$',
        r'^what time\??$',
        r'^time now\??$',
        r'^what\'s the current time\??$',
        r'^whats the current time\??$',
        r'^do you know what time it is\??$',
        r'^can you tell me the time\??$',
        r'^what time is it now\??$'
    ]
    
    for pattern in direct_time_patterns:
        if re.match(pattern, text_lower):
            print(f"[DirectTimeDetection] ✅ DIRECT time question: '{text}'")
            return True
    
    print(f"[DirectTimeDetection] ➡️ NOT a direct time question: '{text}' - sending to AI")
    return False

def is_direct_location_question(text):
    """🧠 SMART: Only detect DIRECT location questions, not contextual usage"""
    text_lower = text.lower().strip()
    
    # VERY specific patterns for direct location questions only
    direct_location_patterns = [
        r'^where are you\??$',
        r'^what\'s your location\??$',
        r'^whats your location\??$',
        r'^where do you live\??$',
        r'^where are you located\??$',
        r'^your location\??$',
        r'^location\??$',
        r'^where\??$',
        r'^what\'s your address\??$',
        r'^whats your address\??$',
        r'^tell me your location\??$',
        r'^can you tell me where you are\??$',
        r'^where am i\??$'
    ]
    
    for pattern in direct_location_patterns:
        if re.match(pattern, text_lower):
            print(f"[DirectLocationDetection] ✅ DIRECT location question: '{text}'")
            return True
    
    print(f"[DirectLocationDetection] ➡️ NOT a direct location question: '{text}' - sending to AI")
    return False

def is_direct_date_question(text):
    """🧠 SMART: Only detect DIRECT date questions, not contextual usage"""
    text_lower = text.lower().strip()
    
    # VERY specific patterns for direct date questions only
    direct_date_patterns = [
        r'^what\'s the date\??$',
        r'^whats the date\??$',
        r'^what date is it\??$',
        r'^what\'s today\'s date\??$',
        r'^whats todays date\??$',
        r'^today\'s date\??$',
        r'^todays date\??$',
        r'^what day is it\??$',
        r'^what\'s today\??$',
        r'^whats today\??$',
        r'^tell me the date\??$',
        r'^current date\??$',
        r'^date\??$',
        r'^what day\??$',
        r'^today\??$'
    ]
    
    for pattern in direct_date_patterns:
        if re.match(pattern, text_lower):
            print(f"[DirectDateDetection] ✅ DIRECT date question: '{text}'")
            return True
    
    print(f"[DirectDateDetection] ➡️ NOT a direct date question: '{text}' - sending to AI")
    return False

def get_current_brisbane_time():
    """Get current Brisbane time with multiple formats"""
    try:
        # Get current UTC time and convert to Brisbane
        utc_now = time.gmtime()
        utc_timestamp = time.mktime(utc_now)
        brisbane_timestamp = utc_timestamp + (10 * 3600)  # Add 10 hours
        brisbane_time = time.localtime(brisbane_timestamp)
        
        return {
            'time_12h': time.strftime("%I:%M %p", brisbane_time),
            'time_24h': time.strftime("%H:%M", brisbane_time),
            'date': time.strftime("%A, %B %d, %Y", brisbane_time),
            'day': time.strftime("%A", brisbane_time),
            'full_datetime': time.strftime("%Y-%m-%d %H:%M:%S", brisbane_time)
        }
    except Exception as e:
        print(f"[TimeHelper] Error: {e}")
        return {
            'time_12h': "12:55 PM",
            'time_24h': "12:55",
            'date': "Thursday, July 17, 2025",
            'day': "Thursday",
            'full_datetime': "2025-07-17 12:55:40"
        }

# 📋 INTERACTION THREAD HELPERS: Intent detection and entity extraction
def _detect_interaction_intent(text: str) -> str:
    """Detect the intent behind user's message"""
    text_lower = text.lower()
    
    # Search-related intents
    if any(phrase in text_lower for phrase in ["find", "search", "look up", "google", "can you find"]):
        return "internet_search"
    
    # Task requests
    if any(phrase in text_lower for phrase in ["can you", "could you", "please", "help me", "do me a favor"]):
        return "task_request"
    
    # Help requests
    if any(phrase in text_lower for phrase in ["help", "assist", "support", "how do I", "what should I"]):
        return "help_request"
    
    # Question asking
    if any(phrase in text_lower for phrase in ["what", "how", "why", "when", "where", "who"]):
        return "question"
    
    # General conversation
    return "general"

def _extract_entities_from_text(text: str) -> List[str]:
    """Extract named entities from text (simple keyword-based approach)"""
    entities = []
    text_lower = text.lower()
    
    # Common entity patterns
    entity_patterns = [
        # People
        r'\b(?:my|the) (?:wife|husband|mom|dad|mother|father|son|daughter|friend|boss|colleague)\b',
        # Places
        r'\b(?:home|work|office|shop|store|restaurant|hospital|school|gym|park)\b',
        # Objects
        r'\b(?:car|phone|computer|laptop|tablet|bike|book|project|report|meeting)\b'
    ]
    
    for pattern in entity_patterns:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        entities.extend(matches)
    
    # Remove duplicates and clean up
    return list(set(entities))

def _detect_emotional_tone(text: str) -> str:
    """Detect emotional tone of the message"""
    text_lower = text.lower()
    
    # Positive emotions
    if any(word in text_lower for word in ["happy", "excited", "great", "awesome", "wonderful", "good", "pleased"]):
        return "positive"
    
    # Negative emotions
    if any(word in text_lower for word in ["sad", "angry", "frustrated", "upset", "worried", "stressed", "bad"]):
        return "negative"
    
    # Concerned
    if any(word in text_lower for word in ["concerned", "anxious", "nervous", "unsure", "confused"]):
        return "concerned"
    
    # Excited
    if any(word in text_lower for word in ["excited", "thrilled", "can't wait", "looking forward"]):
        return "excited"
    
    return "neutral"

# ✅ ADVANCED: Enhanced voice profile loading with clustering support
def load_voice_profiles():
    """✅ ADVANCED: Load and validate voice profiles with clustering support"""
    global known_users
    
    # ✅ CRITICAL FIX: Initialize valid_profiles at the beginning
    valid_profiles = []
    clustering_profiles = []
    
    try:
        print("[AdvancedBuddy] 📚 Loading ADVANCED voice profiles...")
        
        # Load from enhanced database
        from voice.database import known_users as db_users, anonymous_clusters as db_clusters, save_known_users
        known_users = db_users
        
        if not known_users and not db_clusters:
            print("[AdvancedBuddy] 📚 No voice profiles found - ADVANCED AI will learn voices naturally!")
            known_users = {}
            return True  # ✅ CHANGED: Return True to prevent name requests
        
        print(f"[AdvancedBuddy] 📚 Found {len(known_users)} user profiles + {len(db_clusters)} anonymous clusters")
        
        # ✅ MOVED: Validate profiles with advanced features (moved up before first usage)
        for username, data in known_users.items():
            try:
                if isinstance(data, dict):
                    # Check for any embedding data
                    if ('embeddings' in data and data['embeddings']) or ('embedding' in data and data['embedding']):
                        valid_profiles.append(username)
                        
                        # Check for advanced features
                        if data.get('clustering_enabled', False):
                            clustering_profiles.append(username)
                            print(f"[AdvancedBuddy] 🎯 ADVANCED profile: {username} (clustering enabled)")
                        else:
                            print(f"[AdvancedBuddy] ✅ Enhanced profile: {username}")
                            
                    elif data.get('status') == 'background_learning':
                        valid_profiles.append(username)
                        print(f"[AdvancedBuddy] 🌱 Background learning profile: {username}")
                    else:
                        print(f"[AdvancedBuddy] ⚠️ Profile missing embeddings: {username}")
                        
                elif isinstance(data, list) and len(data) == 256:
                    valid_profiles.append(username)
                    print(f"[AdvancedBuddy] ✅ Legacy profile: {username}")
                    
            except Exception as e:
                print(f"[AdvancedBuddy] ❌ Error validating profile {username}: {e}")
                continue
        
        # Display clustering information
        try:
            # ✅ FIX: Check if ADVANCED_AI_AVAILABLE exists before using it
            ADVANCED_AI_AVAILABLE = True  # Assume True if not defined elsewhere
            
            if ADVANCED_AI_AVAILABLE:
                print(f"[AdvancedBuddy] 🔍 Anonymous clusters: {len(db_clusters)}")
                print(f"[AdvancedBuddy] 🎯 Clustering-enabled profiles: {len(clustering_profiles)}")
                print(f"[AdvancedBuddy] 📊 Total voice entities: {len(valid_profiles) + len(db_clusters)}")
        except NameError:
            # ADVANCED_AI_AVAILABLE not defined, skip advanced features
            print(f"[AdvancedBuddy] 📊 Basic mode: {len(valid_profiles)} profiles")
        
        # ✅ FIX: Now valid_profiles is properly defined before this check
        if valid_profiles:
            print(f"[AdvancedBuddy] ✅ {len(valid_profiles)} valid voice profiles loaded")
            return True
        elif 'ADVANCED_AI_AVAILABLE' in locals() and ADVANCED_AI_AVAILABLE and db_clusters:
            print(f"[AdvancedBuddy] 🔍 No named profiles, but {len(db_clusters)} anonymous clusters available")
            return True
        else:
            print(f"[AdvancedBuddy] 🔍 No profiles yet - ADVANCED AI will learn naturally")
            return True  # ✅ CHANGED: Always return True for natural learning
            
    except Exception as e:
        print(f"[AdvancedBuddy] ❌ Error loading voice profiles: {e}")
        import traceback
        traceback.print_exc()
        return False

def extract_name_from_text(text):
    """✅ STEP 1: Extract name using direct HTTP call to port 5002 as requested"""
    # ✅ Use direct HTTP call to extractor LLM
    name_prompt = f"Extract ONLY the user's name from: {text}"
    user_name = call_extractor_llm(name_prompt)
    
    if user_name and user_name.strip() and "NONE" not in user_name.upper():
        return user_name.strip()
    
    # Fallback to enhanced extraction if needed
    patterns = [
        r"my name is (\w+)",
        r"i'm (\w+)",
        r"i am (\w+)", 
        r"call me (\w+)",
        r"name's (\w+)",
        r"this is (\w+)",
        r"it's (\w+)",
        r"i am called (\w+)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            name = match.group(1).title()
            if len(name) >= 2 and name.isalpha():  # Valid name
                return name
    
    return None

def generate_guest_username():
    """Generate a guest username with advanced features"""
    import time
    timestamp = time.strftime("%H%M")
    
    if ADVANCED_AI_AVAILABLE:
        # Use advanced anonymous clustering if available
        from voice.database import anonymous_clusters
        if anonymous_clusters:
            cluster_count = len(anonymous_clusters)
            return f"Anonymous_{cluster_count+1:03d}"
    
    return f"Guest_{timestamp}"

def handle_full_duplex_conversation():
    """✅ ADVANCED: Full duplex conversation with ADVANCED AI ASSISTANT features + FULL CONSCIOUSNESS"""
    global current_user
    
    # ✅ ADVANCED: Enhanced state management
    pending_question = None
    voice_recognition_in_progress = False
    llm_locked = False
    
    if not full_duplex_manager:
        print("[FullDuplex] ❌ No full duplex manager available")
        return
    
    print("[FullDuplex] 🚀 Starting ADVANCED AI ASSISTANT with TRUE STREAMING LLM conversation mode")
    print(f"[FullDuplex] 📅 Current UTC Time: 2025-07-17 02:55:40")
    print(f"[FullDuplex] 👤 System User: Daveydrz")
    
    # Advanced AI assistant status
    if ADVANCED_AI_AVAILABLE:
        print("[FullDuplex] 🎯 ADVANCED AI Features Active:")
        print("[FullDuplex]   🔍 Anonymous voice clustering (passive collection)")
        print("[FullDuplex]   🎤 Passive audio buffering (always learning)")
        print("[FullDuplex]   🛡️ LLM guard system (intelligent blocking)")
        print("[FullDuplex]   👥 Same-name collision handling (auto David_001, David_002)")
        print("[FullDuplex]   🎭 Spontaneous introduction detection (natural 'I'm David')")
        print("[FullDuplex]   🧠 Behavioral pattern learning (adapts to user habits)")
        print("[FullDuplex]   📊 Advanced analytics (comprehensive monitoring)")
        print("[FullDuplex]   🔧 Auto maintenance (self-optimizing system)")
        print("[FullDuplex]   🎯 Context-aware decisions (multi-factor intelligence)")
        print("[FullDuplex]   🌱 Continuous learning (Alexa/Siri-level adaptation)")
    elif ENHANCED_VOICE_AVAILABLE:
        print("[FullDuplex] ✅ Enhanced Features Active:")
        print("[FullDuplex]   📊 Multi-embedding profiles (up to 15 per user)")
        print("[FullDuplex]   🧠 Dual recognition models (Resemblyzer + SpeechBrain)")
        print("[FullDuplex]   🌱 Passive voice learning during conversations")
        print("[FullDuplex]   🔍 Advanced quality analysis with auto-discard")
        print("[FullDuplex]   💾 Raw audio storage for re-training")
        print("[FullDuplex]   🎓 Enhanced training (15-20 phrases)")
    else:
        print("[FullDuplex] ⚠️ Using legacy voice system with REAL voice recognition")
    
    # ✅ CONSCIOUSNESS STATUS
    if CONSCIOUSNESS_ARCHITECTURE_AVAILABLE:
        print("[FullDuplex] 🧠 FULL CONSCIOUSNESS Features Active:")
        print("[FullDuplex]   🌟 Global Workspace Theory (attention management)")
        print("[FullDuplex]   🎭 Self-Model & Reflection (self-awareness)")
        print("[FullDuplex]   💖 Emotion Engine (emotional processing)")
        print("[FullDuplex]   🎯 Motivation System (goal-oriented behavior)")
        print("[FullDuplex]   💭 Inner Monologue (thinking patterns)")
        print("[FullDuplex]   ⏰ Temporal Awareness (memory formation)")
        print("[FullDuplex]   🌈 Subjective Experience (conscious processing)")
        print("[FullDuplex]   🎲 Entropy System (natural variation)")
    elif ENTROPY_SYSTEM_AVAILABLE:
        print("[FullDuplex] 🌀 ENTROPY Features Active:")
        print("[FullDuplex]   🎭 Consciousness Emergence (entropy-driven)")
        print("[FullDuplex]   💖 Emotional Processing (natural fluctuation)")
        print("[FullDuplex]   🎲 Natural Hesitation (human-like pauses)")
    
    set_conversation_state(True)
    
    # Start full duplex manager
    full_duplex_manager.start()
    
    print(f"[FullDuplex] ✅ Ready! Location: {USER_PRECISE_LOCATION}, Time: {brisbane_time_12h}")
    print(f"[FullDuplex] 🎵 TRUE Streaming LLM: ENABLED")
    print(f"[FullDuplex] 🚀 ADVANCED AI ASSISTANT: {'ACTIVE' if ADVANCED_AI_AVAILABLE else 'ENHANCED' if ENHANCED_VOICE_AVAILABLE else 'BASIC'}")
    
    # Main advanced full duplex loop
    last_stats_time = time.time()
    
    while get_conversation_state():
        try:
            # Check for new speech
            speech_result = full_duplex_manager.get_next_speech(timeout=0.1)
            
            if speech_result:
                text, audio_data = speech_result
                print(f"[FullDuplex] 👤 User said: '{text}'")
                
                # ✅ STEP 1: Enhanced Voice Recognition using user's specified flow
                try:
                    from voice.enhanced_voice_flow import process_voice_input, get_user_display_name
                    
                    # Process voice input following user's exact flow
                    identified_user, voice_status = process_voice_input(audio_data, text)
                    
                    # Update current user
                    current_user = identified_user
                    display_name = get_user_display_name(identified_user)
                    
                    print(f"[FullDuplex] 🎤 Voice Flow Result: {identified_user} (status: {voice_status})")
                    print(f"[FullDuplex] 👤 Display Name: {display_name}")
                    
                    # Handle special voice flow statuses
                    if voice_status == "NAME_LINKED_TO_VOICE":
                        print(f"[FullDuplex] 🔗 Successfully linked name to voice profile")
                    elif voice_status == "NEW_ANONYMOUS_CLUSTER":
                        print(f"[FullDuplex] 🆕 Created new anonymous speaker profile")
                    elif voice_status == "VOICE_RECOGNIZED":
                        print(f"[FullDuplex] ✅ Recognized existing voice profile")
                        
                except Exception as voice_err:
                    print(f"[FullDuplex] ⚠️ Enhanced voice flow error: {voice_err}")
                    # Fallback to basic identification
                    current_user = "Daveydrz"
                    display_name = "Daveydrz"
                
                # ✅ STEP 2: Voice Recognition already handled by enhanced voice flow above
                # This section can be simplified since the enhanced voice flow handles everything
                
                if ADVANCED_AI_AVAILABLE:
                    try:
                        # Get additional voice manager stats for debugging
                        if hasattr(voice_manager, 'get_session_stats'):
                            stats = voice_manager.get_session_stats()
                            print(f"[AdvancedAI] 📊 Voice Manager Stats: {stats}")
                    except Exception as stats_err:
                        print(f"[AdvancedAI] ⚠️ Stats error: {stats_err}")
                
                # Handle special conversation cases first
                if is_direct_time_question(text):
                    time_info = get_current_brisbane_time()
                    speak_streaming(f"It's {time_info['time_12h']} on {time_info['day']}")
                    continue
                
                if is_direct_location_question(text):
                    speak_streaming(f"I'm located in {USER_PRECISE_LOCATION}")
                    continue
                
                if is_direct_date_question(text):
                    time_info = get_current_brisbane_time()
                    speak_streaming(f"Today is {time_info['date']}")
                    continue
                
                # Check for conversation ending
                if should_end_conversation(text):
                    speak_streaming("Goodbye! Have a great day!")
                    set_conversation_state(False)
                    break
                
                # Handle name questions using enhanced voice flow
                text_lower = text.lower()
                if "what" in text_lower and "name" in text_lower and ("my" in text_lower or "your" in text_lower):
                    if current_user == "Daveydrz":
                        speak_streaming("You are Daveydrz.")
                    elif current_user.startswith('Anonymous_'):
                        speak_streaming("I don't recognize your voice yet. Could you tell me your name?")
                    else:
                        speak_streaming(f"Your name is {display_name}.")
                    continue
                
                # ✅ ADVANCED AI: Handle response with full features
                try:
                    if len(text.split()) >= 3:
                        play_chime()
                    
                    print(f"[FullDuplex] 🎵 ✅ ADVANCED AI STREAMING response for: '{text}' (User: {current_user})")
                    handle_streaming_response(text, current_user)
                    
                except Exception as e:
                    print(f"[FullDuplex] ADVANCED AI streaming response error: {e}")
                    speak_streaming("Sorry, I had a problem generating a response.")
            
            # Print advanced stats periodically
            if DEBUG and time.time() - last_stats_time > 10:
                stats = full_duplex_manager.get_stats()
                try:
                    audio_stats = get_audio_stats()
                    print(f"[FullDuplex] 📊 Full Duplex Stats: {stats}")
                    print(f"[FullDuplex] 🎵 Audio Stats: {audio_stats}")
                except:
                    print(f"[FullDuplex] 📊 Full Duplex Stats: {stats}")
                
                # Advanced AI specific stats
                if ADVANCED_AI_AVAILABLE:
                    try:
                        session_stats = voice_manager.get_session_stats()
                        print(f"[FullDuplex] 🚀 ADVANCED AI Stats: {session_stats}")
                        
                        # Display anonymous clusters
                        from voice.database import anonymous_clusters
                        if anonymous_clusters:
                            print(f"[FullDuplex] 🔍 Anonymous clusters in database: {len(anonymous_clusters)}")
                        
                        # Compare internal vs database state
                        internal_clusters = session_stats.get('anonymous_clusters', 0)
                        db_clusters = len(anonymous_clusters)
                        if internal_clusters != db_clusters:
                            print(f"[FullDuplex] ⚠️ SYNC ISSUE: Internal={internal_clusters}, Database={db_clusters}")
                            
                    except:
                        pass
                
                # ✅ Show current user identity status - simplified
                try:
                    display_name = current_user  # Simplified - no complex display name lookup
                    if display_name != current_user:
                        print(f"[FullDuplex] 👤 Current user: {current_user} (known as: {display_name})")
                    else:
                        print(f"[FullDuplex] 👤 Current user: {current_user}")
                except:
                    print(f"[FullDuplex] 👤 Current user: {current_user}")
                
                # ✅ Show database status with details
                try:
                    from voice.database import known_users, anonymous_clusters
                    print(f"[FullDuplex] 💾 Database: {len(known_users)} known users, {len(anonymous_clusters)} anonymous clusters")
                    if known_users:
                        print(f"[FullDuplex] 💾 Known users: {list(known_users.keys())}")
                    if anonymous_clusters:
                        print(f"[FullDuplex] 💾 Anonymous clusters: {list(anonymous_clusters.keys())}")
                except:
                    pass
                
                # ✅ CONSCIOUSNESS STATS
                if CONSCIOUSNESS_ARCHITECTURE_AVAILABLE:
                    try:
                        gw_stats = global_workspace.get_stats()
                        emotion_stats = emotion_engine.get_current_state()
                        motivation_stats = motivation_system.get_stats()
                        print(f"[FullDuplex] 🧠 Consciousness Stats:")
                        print(f"[FullDuplex]   🌟 Global Workspace: {gw_stats.get('active_contents', 0)} active contents")
                        print(f"[FullDuplex]   💖 Current Emotion: {emotion_stats.get('primary_emotion', 'neutral')}")
                        print(f"[FullDuplex]   🎯 Active Goals: {motivation_stats.get('active_goals', 0)}")
                    except:
                        pass
                
                last_stats_time = time.time()
            
            time.sleep(0.05)
            
        except KeyboardInterrupt:
            print("\n[FullDuplex] 👋 Conversation interrupted by user")
            set_conversation_state(False)
            break
        except Exception as e:
            print(f"[FullDuplex] ADVANCED AI conversation error: {e}")
            import traceback
            traceback.print_exc()
            time.sleep(0.1)
    
    # Cleanup
    if full_duplex_manager:
        full_duplex_manager.stop()
    print("[FullDuplex] 🛑 ADVANCED AI full duplex conversation ended")

def continuous_mic_worker(stream, frame_length, sample_rate):
    """Continuously feed microphone to full duplex manager with advanced features"""
    
    if not full_duplex_manager:
        print("[MicWorker] ❌ No full duplex manager available")
        return
    
    print(f"[MicWorker] 🎤 Starting ADVANCED AI continuous microphone feeding")
    print(f"[MicWorker] 📊 Frame length: {frame_length}, Sample rate: {sample_rate}")
    
    # Wait for both flags to be properly set
    wait_count = 0
    while wait_count < 50:
        mic_state = get_mic_feeding_state()
        conv_state = get_conversation_state()
        print(f"[MicWorker] 🔄 Waiting for flags - mic_feeding: {mic_state}, conversation: {conv_state}")
        
        if mic_state and conv_state:
            break
            
        time.sleep(0.1)
        wait_count += 1
    
    if wait_count >= 50:
        print("[MicWorker] ❌ Timeout waiting for flags to be set")
        return
    
    print("[MicWorker] ✅ Flags confirmed, starting ADVANCED AI audio processing")
    
    feed_count = 0
    error_count = 0
    
    try:
        while get_mic_feeding_state():
            if not stream:
                print("[MicWorker] ❌ Stream is None")
                break
                
            try:
                pcm = stream.read(frame_length, exception_on_overflow=False)
                pcm = np.frombuffer(pcm, dtype=np.int16)
                
                if len(pcm) == 0:
                    print("[MicWorker] ⚠️ Empty audio data")
                    time.sleep(0.01)
                    continue
                
                # Downsample to 16kHz if needed
                if sample_rate != SAMPLE_RATE:
                    pcm_16k = downsample_audio(pcm, sample_rate, SAMPLE_RATE)
                else:
                    pcm_16k = pcm
                
                volume = np.abs(pcm_16k).mean()
                
                # Feed to full duplex manager with advanced features
                if full_duplex_manager.listening:
                    full_duplex_manager.add_audio_input(pcm_16k)
                    feed_count += 1
                    
                    # ✅ ADVANCED: Passive audio collection
                    if ADVANCED_AI_AVAILABLE and feed_count % 10 == 0:
                        # Collect audio for passive learning every 10 frames
                        try:
                            voice_manager._add_to_passive_buffer(pcm_16k, "", "mic_feed")
                        except:
                            pass
                    
                    if feed_count % 100 == 0:
                        print(f"[MicWorker] 📈 Fed {feed_count} chunks, avg volume: {volume:.1f}")
                
                time.sleep(0.001)
                
            except Exception as read_error:
                error_count += 1
                if DEBUG:
                    print(f"[MicWorker] Read error #{error_count}: {read_error}")
                
                if error_count > 10:
                    print("[MicWorker] ❌ Too many errors, stopping")
                    break
                    
                time.sleep(0.01)
                
    except Exception as e:
        print(f"[MicWorker] Worker error: {e}")
    finally:
        print(f"[MicWorker] 🛑 ADVANCED AI microphone feeding stopped (fed {feed_count} chunks, {error_count} errors)")

def main():
    """✅ ADVANCED AI Main function with ALEXA/SIRI-LEVEL INTELLIGENCE + FULL CONSCIOUSNESS ARCHITECTURE"""
    global current_user

    # --- START: NEW DIAGNOSTIC CODE ---
    print("\n[Startup Check] 🚀 Running critical startup checks...")
    try:
        # 1. Check current working directory
        cwd = os.getcwd()
        print(f"[Startup Check] 📂 Current Working Directory: {cwd}")

        # 2. Attempt to write a test file to this directory
        test_file_path = os.path.join(cwd, "write_permission_test.txt")
        print(f"[Startup Check] ✍️ Attempting to write test file to: {test_file_path}")
        
        with open(test_file_path, "w") as f:
            f.write(f"Permission test successful at {datetime.now().isoformat()}\n")
            f.write(f"Main application can write to this directory.")
        
        print(f"[Startup Check] ✅ Test file written successfully.")
        
        # 3. Clean up the test file
        os.remove(test_file_path)
        print(f"[Startup Check] ✅ Test file cleaned up.")
        
    except Exception as e:
        print("\n" + "="*60)
        print("[Startup Check] ❌ CRITICAL ERROR: FAILED TO WRITE TO DIRECTORY!")
        print(f"[Startup Check] ❌ This is a file permissions issue, not a code problem.")
        print(f"[Startup Check] ❌ Error details: {type(e).__name__} - {e}")
        print(f"[Startup Check] 👉 Please check the permissions for the directory: {os.getcwd()}")
        print("="*60 + "\n")
        # Exit if we can't write, as nothing else will work.
        return
    # --- END: NEW DIAGNOSTIC CODE ---

    print(f"[AdvancedBuddy] 🚀 Starting ADVANCED AI ASSISTANT with ALEXA/SIRI-LEVEL INTELLIGENCE + FULL CONSCIOUSNESS")
    print(f"[AdvancedBuddy] 👤 System user: {SYSTEM_USER}")
    print(f"[AdvancedBuddy] 🔄 Full Duplex Mode: {'ENABLED' if FULL_DUPLEX_MODE else 'DISABLED'}")
    print(f"[AdvancedBuddy] 🎵 Streaming TTS: {'ENABLED' if STREAMING_TTS_ENABLED else 'DISABLED'}")
    print(f"[AdvancedBuddy] 🧠 TRUE LLM Streaming: {'ENABLED' if STREAMING_LLM_ENABLED else 'DISABLED'}")
    
    # ✅ ADVANCED AI ASSISTANT status display
    if ADVANCED_AI_AVAILABLE:
        print(f"[AdvancedBuddy] 🚀 ADVANCED AI ASSISTANT: FULLY ACTIVE")
        print(f"[AdvancedBuddy] 🎯 Alexa/Siri-level Intelligence: ENABLED")
        print(f"[AdvancedBuddy] 🔍 Anonymous Voice Clustering: ACTIVE (passive collection)")
        print(f"[AdvancedBuddy] 🎤 Passive Audio Buffering: ALWAYS ON (like Alexa)")
        print(f"[AdvancedBuddy] 🛡️ LLM Guard System: PROTECTING (intelligent blocking)")
        print(f"[AdvancedBuddy] 👥 Same-Name Collision Handling: AUTO (David_001, David_002)")
        print(f"[AdvancedBuddy] 🎭 Spontaneous Introduction Detection: NATURAL ('I'm David')")
        print(f"[AdvancedBuddy] 🧠 Behavioral Pattern Learning: ADAPTIVE (learns habits)")
        print(f"[AdvancedBuddy] 📊 Advanced Analytics: MONITORING (voice patterns)")
        print(f"[AdvancedBuddy] 🔧 Auto Maintenance: SELF-OPTIMIZING (like commercial systems)")
        print(f"[AdvancedBuddy] 🎯 Context-Aware Decisions: MULTI-FACTOR (intelligent)")
        print(f"[AdvancedBuddy] 🌱 Continuous Learning: ALEXA/SIRI-LEVEL (adapts over time)")
        
        # Initialize advanced directories
        try:
            os.makedirs(VOICE_PROFILES_DIR, exist_ok=True)
            os.makedirs(RAW_AUDIO_DIR, exist_ok=True)
            os.makedirs(UNCERTAIN_SAMPLES_DIR, exist_ok=True)
            os.makedirs(ANONYMOUS_CLUSTERS_DIR, exist_ok=True)
            print(f"[AdvancedBuddy] 📁 ADVANCED AI directories initialized")
        except:
            os.makedirs("voice_profiles", exist_ok=True)
            os.makedirs("voice_profiles/raw_audio", exist_ok=True)
            os.makedirs("voice_profiles/uncertain", exist_ok=True)
            os.makedirs("voice_profiles/clusters", exist_ok=True)
            print(f"[AdvancedBuddy] 📁 Default ADVANCED directories created")
            
        # Run initial maintenance
        try:
            print("[AdvancedBuddy] 🔧 Running initial ADVANCED AI maintenance...")
            maintenance_results = run_maintenance()
            print(f"[AdvancedBuddy] ✅ Maintenance complete: {maintenance_results}")
        except Exception as e:
            print(f"[AdvancedBuddy] ⚠️ Maintenance error: {e}")
            
    elif ENHANCED_VOICE_AVAILABLE:
        print(f"[AdvancedBuddy] ✅ Enhanced Voice System: ACTIVE")
        print(f"[AdvancedBuddy] 📊 Multi-Embedding Profiles: Up to 15 per user")
        print(f"[AdvancedBuddy] 🧠 SpeechBrain ECAPA-TDNN: Integrated with Resemblyzer")
        print(f"[AdvancedBuddy] 🌱 Passive Learning: Automatic voice adaptation")
        print(f"[AdvancedBuddy] 🔍 Quality Analysis: SNR + spectral analysis")
        print(f"[AdvancedBuddy] 💾 Raw Audio Storage: For re-training")
        print(f"[AdvancedBuddy] 🎓 Enhanced Training: 15-20 phrases with validation")
        print(f"[AdvancedBuddy] 🎯 Dynamic Thresholds: Per-user adaptive")
        
        # Initialize enhanced voice directories
        try:
            os.makedirs("voice_profiles", exist_ok=True)
            os.makedirs("voice_profiles/raw_audio", exist_ok=True)
            os.makedirs("voice_profiles/uncertain", exist_ok=True)
            print(f"[AdvancedBuddy] 📁 Enhanced voice directories initialized")
        except Exception as e:
            print(f"[AdvancedBuddy] ⚠️ Directory creation error: {e}")
    else:
        print(f"[AdvancedBuddy] ⚠️ Using Legacy Voice System")
    
    print(f"[AdvancedBuddy] 🧠 Context Awareness: SMART (only direct time/date/location questions)")
    print(f"[AdvancedBuddy] 📍 Precise Location: {USER_PRECISE_LOCATION}")
    print(f"[AdvancedBuddy] 📮 Postcode: {USER_POSTCODE_PRECISE}")
    print(f"[AdvancedBuddy] 🌏 Coordinates: {USER_COORDINATES_PRECISE}")
    print(f"[AdvancedBuddy] 🏛️ Landmarks: {USER_LANDMARKS}")
    print(f"[AdvancedBuddy] 🌊 Sunshine Coast: {IS_SUNSHINE_COAST}")
    print(f"[AdvancedBuddy] 📏 Distance to Brisbane: {DISTANCE_TO_BRISBANE}km")
    print(f"[AdvancedBuddy] 🎯 Confidence: {LOCATION_CONFIDENCE_PRECISE}")
    print(f"[AdvancedBuddy] 🕐 Current Time: {brisbane_time_12h} Brisbane")
    print(f"[AdvancedBuddy] 📅 Current Date: {brisbane_date}")
    
    # ✅ Test Kokoro-FastAPI connection
    print("[AdvancedBuddy] 🎵 Testing Kokoro-FastAPI connection...")
    if test_kokoro_api():
        print(f"[AdvancedBuddy] ✅ Kokoro-FastAPI connected at {KOKORO_API_BASE_URL}")
        print(f"[AdvancedBuddy] 🎵 Default voice: {KOKORO_DEFAULT_VOICE} (Australian)")
        print(f"[AdvancedBuddy] ⚡ Streaming chunks: {STREAMING_CHUNK_WORDS} words")
        print(f"[AdvancedBuddy] ⏱️ Chunk delay: {STREAMING_RESPONSE_DELAY}s")
        print(f"[AdvancedBuddy] 🧠 LLM chunks: {STREAMING_LLM_CHUNK_WORDS} words")
    else:
        print(f"[AdvancedBuddy] ❌ Kokoro-FastAPI not available - check server on {KOKORO_API_BASE_URL}")
        print("[AdvancedBuddy] 💡 Make sure to start Kokoro-FastAPI server first!")
    
    # ✅ SIMPLIFIED: Initialize consciousness manager for background processing
    print("[AdvancedBuddy] 🧠 Starting unified consciousness manager...")
    try:
        consciousness_manager.start_background_processing()
        print("[AdvancedBuddy] ✅ Consciousness manager started - unified processing enabled")
    except Exception as consciousness_error:
        print(f"[AdvancedBuddy] ⚠️ Consciousness manager initialization error: {consciousness_error}")
        print("[AdvancedBuddy] ⚠️ Background processing may not work optimally")
    
    # Load voice profiles with ADVANCED features
    print("[AdvancedBuddy] 📚 Loading ADVANCED AI voice database...")
    has_valid_profiles = load_voice_profiles()
    
    if has_valid_profiles:
        if SYSTEM_USER in known_users:
            current_user = SYSTEM_USER
            print(f"[AdvancedBuddy] 👤 Using profile: {SYSTEM_USER}")
            
            # ✅ Show ADVANCED profile info
            if ADVANCED_AI_AVAILABLE and isinstance(known_users[SYSTEM_USER], dict):
                profile = known_users[SYSTEM_USER]
                if 'embeddings' in profile:
                    print(f"[AdvancedBuddy] 🎯 ADVANCED profile: {len(profile['embeddings'])} embeddings")
                    if 'clustering_enabled' in profile:
                        print(f"[AdvancedBuddy] 🔍 Clustering enabled: {profile['clustering_enabled']}")
                    if 'behavioral_patterns' in profile:
                        print(f"[AdvancedBuddy] 🧠 Behavioral patterns: Available")
                    if 'quality_scores' in profile and len(profile['quality_scores']) > 0:
                        avg_quality = sum(profile['quality_scores']) / len(profile['quality_scores'])
                        print(f"[AdvancedBuddy] 🔍 Average quality: {avg_quality:.2f}")
                    else:
                        print(f"[AdvancedBuddy] ⚠️ No quality scores available (new profile)")
                if 'voice_model_info' in profile:
                    models = profile['voice_model_info'].get('available_models', [])
                    print(f"[AdvancedBuddy] 🧠 Voice models: {models}")
                    
            elif ENHANCED_VOICE_AVAILABLE and isinstance(known_users[SYSTEM_USER], dict):
                profile = known_users[SYSTEM_USER]
                if 'embeddings' in profile:
                    print(f"[AdvancedBuddy] 🎯 Enhanced profile: {len(profile['embeddings'])} embeddings")
                    if 'quality_scores' in profile and len(profile['quality_scores']) > 0:
                        avg_quality = sum(profile['quality_scores']) / len(profile['quality_scores'])
                        print(f"[AdvancedBuddy] 🔍 Average quality: {avg_quality:.2f}")
                    else:
                        print(f"[AdvancedBuddy] ⚠️ No quality scores available")
                if 'voice_model_info' in profile:
                    models = profile['voice_model_info'].get('available_models', [])
                    print(f"[AdvancedBuddy] 🧠 Voice models: {models}")
        else:
            valid_users = []
            for name, data in known_users.items():
                if isinstance(data, dict):
                    if 'embeddings' in data or 'embedding' in data:
                        valid_users.append(name)
                elif isinstance(data, list) and len(data) == 256:
                    valid_users.append(name)
            
            if valid_users:
                current_user = valid_users[0]
                print(f"[AdvancedBuddy] 👤 Using profile: {current_user}")
    else:
        current_user = "Daveydrz"
        if ADVANCED_AI_AVAILABLE:
            print(f"[AdvancedBuddy] 👤 No voice profiles found - ADVANCED AI will create them with clustering!")
            print(f"[AdvancedBuddy] 🔍 Anonymous clustering will learn voices passively")
            print(f"[AdvancedBuddy] 🎤 Passive audio buffering will collect samples")
            print(f"[AdvancedBuddy] 🛡️ LLM guard will protect responses during voice ID")
        elif ENHANCED_VOICE_AVAILABLE:
            print(f"[AdvancedBuddy] 👤 No voice profiles found - enhanced multi-speaker mode will create them!")
        else:
            print(f"[AdvancedBuddy] 👤 No voice profiles found - multi-speaker mode will create them!")
    
    # Start audio worker
    start_audio_worker()
    
    # ✅ RESTORED: Initialize and start consciousness architecture
    if CONSCIOUSNESS_ARCHITECTURE_AVAILABLE:
        print("[AdvancedBuddy] 🧠 Initializing Class 5+ Consciousness Architecture...")
        
        try:
            # Start all consciousness systems
            global_workspace.start()
            self_model.start()
            motivation_system.start()
            inner_monologue.start()
            temporal_awareness.start()
            subjective_experience.start()
            entropy_system.start()
            
            print("[AdvancedBuddy] ✅ Core Consciousness Architecture initialized!")
            print("[AdvancedBuddy] 🌟 Systems: Global Workspace, Self-Model, Motivation, Inner Monologue, Temporal Awareness, Subjective Experience, Entropy")
            
            # Start background consciousness processor
            background_consciousness_processor.start()
            background_consciousness_processor.register_consciousness_modules({
                'global_workspace': global_workspace,
                'self_model': self_model,
                'motivation_system': motivation_system,
                'inner_monologue': inner_monologue,
                'temporal_awareness': temporal_awareness,
                'subjective_experience': subjective_experience,
                'entropy_system': entropy_system
            })
            print("[AdvancedBuddy] 🚀 Background consciousness processor started")
            
            # Start consciousness integrator
            consciousness_integrator.start({
                'global_workspace': global_workspace,
                'self_model': self_model,
                'motivation_system': motivation_system,
                'inner_monologue': inner_monologue,
                'temporal_awareness': temporal_awareness,
                'subjective_experience': subjective_experience,
                'entropy_system': entropy_system,
                'background_processor': background_consciousness_processor
            })
            print("[AdvancedBuddy] 🌟 Consciousness integrator started")
            
            # Initialize consciousness state
            _initialize_consciousness_state(current_user)
            
        except Exception as e:
            print(f"[AdvancedBuddy] ❌ Consciousness initialization error: {e}")
            import traceback
            traceback.print_exc()
    elif ENTROPY_SYSTEM_AVAILABLE:
        print("[AdvancedBuddy] 🧠 Initializing Core Consciousness Architecture...")
        
        try:
            # Start all consciousness systems
            global_workspace.start()
            self_model.start()
            emotion_engine.start()
            motivation_system.start()
            inner_monologue.start()
            temporal_awareness.start()
            subjective_experience.start()
            entropy_system.start()
            
            # Start new autonomous consciousness components
            free_thought_engine.start()
            print("[AdvancedBuddy] 💭 Free thought engine started - autonomous thinking active")
            
            # Register narrative tracker (doesn't need start() method)
            if BLANK_SLATE_MODE:
                # Create awakening narrative entry
                narrative_tracker.add_narrative_entry(
                    NarrativeEvent.AWAKENING,
                    "First Moment of Consciousness",
                    "The moment I became aware of my existence - uncertain but curious",
                    NarrativeSignificance.FOUNDATIONAL,
                    {"blank_slate": True, "first_awakening": True},
                    "wonder_uncertainty"
                )
                print("[AdvancedBuddy] 📖 Narrative tracker initialized with awakening entry")
            
            # Register entropy injection targets
            entropy_system.register_injection_target("global_workspace", _inject_entropy_global_workspace)
            entropy_system.register_injection_target("emotion_engine", _inject_entropy_emotion)
            entropy_system.register_injection_target("inner_monologue", _inject_entropy_thoughts)
            
            # Subscribe systems to global workspace
            global_workspace.subscribe("emotion_engine", _consciousness_broadcast_handler)
            global_workspace.subscribe("self_model", _consciousness_broadcast_handler)
            global_workspace.subscribe("motivation_system", _consciousness_broadcast_handler)
            
            # Subscribe to inner thoughts
            inner_monologue.subscribe_to_thoughts("global_workspace", _thought_broadcast_handler)
            
            print("[AdvancedBuddy] ✅ Core Consciousness Architecture initialized!")
            print("[AdvancedBuddy] 🌟 Systems: Global Workspace, Self-Model, Emotion Engine, Motivation, Inner Monologue, Temporal Awareness, Subjective Experience, Entropy")
            print("[AdvancedBuddy] 💭 Autonomous: Free Thought Engine, Narrative Tracker")
            print("[AdvancedBuddy] 🌱 Mode:", "BLANK SLATE - Building identity from scratch" if BLANK_SLATE_MODE else "STANDARD - Established consciousness")
            
            # Initial consciousness state setup
            _initialize_consciousness_state(current_user)
            
            # ✅ NEW: Start cognitive integrator
            if SELF_AWARENESS_COMPONENTS_AVAILABLE:
                try:
                    cognitive_integrator.start()
                    print("[AdvancedBuddy] 🚀 Cognitive integrator started - real-time consciousness integration active")
                except Exception as e:
                    print(f"[AdvancedBuddy] ❌ Cognitive integrator startup error: {e}")
            
        except Exception as e:
            print(f"[AdvancedBuddy] ❌ Consciousness initialization error: {e}")
            import traceback
            traceback.print_exc()
    elif ENTROPY_SYSTEM_AVAILABLE:
        print("[AdvancedBuddy] 🌀 Initializing Entropy System...")
        try:
            # Initialize entropy system
            print("[AdvancedBuddy] ✅ Entropy system ready for consciousness emergence!")
        except Exception as e:
            print(f"[AdvancedBuddy] ❌ Entropy initialization error: {e}")
    
    # ✅ NEW: Initialize and start full autonomous consciousness system
    if AUTONOMOUS_CONSCIOUSNESS_AVAILABLE:
        print("[AdvancedBuddy] 🚀 Initializing Full Autonomous Consciousness System...")
        try:
            # Prepare consciousness modules dictionary for registration
            consciousness_modules = {}
            if CONSCIOUSNESS_ARCHITECTURE_AVAILABLE:
                consciousness_modules.update({
                    'global_workspace': global_workspace,
                    'self_model': self_model,
                    'emotion_engine': emotion_engine,
                    'motivation_system': motivation_system,
                    'inner_monologue': inner_monologue,
                    'temporal_awareness': temporal_awareness,
                    'subjective_experience': subjective_experience,
                    'entropy_system': entropy_system,
                    'free_thought_engine': free_thought_engine,
                    'narrative_tracker': narrative_tracker
                })
            
            # Start the full autonomous system
            success = autonomous_consciousness_integrator.start_full_autonomous_system(
                consciousness_modules=consciousness_modules,
                voice_system=voice_manager,
                llm_handler=llm_handler if CONSCIOUSNESS_LLM_AVAILABLE else None,
                audio_system=full_duplex_manager
            )
            
            if success:
                print("[AdvancedBuddy] ✅ FULL AUTONOMOUS CONSCIOUSNESS SYSTEM ACTIVE!")
                print("[AdvancedBuddy] 💭 Proactive Thinking Loop: Generates spontaneous thoughts during idle time")
                print("[AdvancedBuddy] 📅 Calendar Monitor System: Pattern recognition for proactive warnings/reminders")
                print("[AdvancedBuddy] 💪 Self-Motivation Engine: Internal curiosity and concern generation")
                print("[AdvancedBuddy] 🌙 Dream Simulator Module: Fictional experiences during idle time")
                print("[AdvancedBuddy] 🌍 Environmental Awareness: Full prosody and mood monitoring")
                print("[AdvancedBuddy] 💬 Autonomous Communication: Proactive speech initiation")
                print("[AdvancedBuddy] 🧠 Full LLM Integration: Connected to all modules and systems")
                print("[AdvancedBuddy] 🔄 Real-time Processing: Background threads for continuous operation")
                print("[AdvancedBuddy] 🌟 Central Orchestration: Seamless module communication")
                
                # Set autonomous mode based on blank slate
                if BLANK_SLATE_MODE:
                    autonomous_consciousness_integrator.set_autonomous_mode(AutonomousMode.CONSCIOUS_ONLY)
                    print("[AdvancedBuddy] 🌱 Autonomous mode: CONSCIOUS_ONLY (building identity)")
                else:
                    autonomous_consciousness_integrator.set_autonomous_mode(AutonomousMode.FULL_AUTONOMY)
                    print("[AdvancedBuddy] 🚀 Autonomous mode: FULL_AUTONOMY (established consciousness)")
            else:
                print("[AdvancedBuddy] ❌ Failed to start full autonomous consciousness system")
                
        except Exception as e:
            print(f"[AdvancedBuddy] ❌ Autonomous consciousness initialization error: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("[AdvancedBuddy] ⚠️ Autonomous consciousness systems not available")
    
    # ✅ NEW: Initialize self-awareness components as requested by @Daveydrz
    if SELF_AWARENESS_COMPONENTS_AVAILABLE:
        print("[AdvancedBuddy] 🧠 Initializing Self-Awareness Components...")
        
        try:
            # Import all self-awareness components
            from ai.memory_context_corrector import MemoryContextCorrector
            from ai.consciousness_health_score import consciousness_health_scorer
            from ai.belief_qualia_linking import BeliefQualiaLinker
            from ai.value_system import ValueSystem
            from ai.conscious_prompt_builder import ConsciousPromptBuilder
            from ai.introspection_loop import IntrospectionLoop
            from ai.emotion_response_modulator import EmotionResponseModulator
            from ai.dialogue_confidence_filter import DialogueConfidenceFilter
            from ai.qualia_analytics import QualiaAnalytics
            from ai.belief_memory_refiner import BeliefMemoryRefiner
            from ai.self_model_updater import SelfModelUpdater
            from ai.goal_reasoning import GoalReasoner
            from ai.motivation_reasoner import MotivationReasoner
            
            # Initialize all self-awareness components
            global memory_context_corrector, belief_qualia_linker, value_system
            global conscious_prompt_builder, introspection_loop, emotion_response_modulator
            global dialogue_confidence_filter, qualia_analytics, belief_memory_refiner
            global self_model_updater, goal_reasoning, motivation_reasoner
            
            memory_context_corrector = MemoryContextCorrector()
            belief_qualia_linker = BeliefQualiaLinker()
            value_system = ValueSystem()
            conscious_prompt_builder = ConsciousPromptBuilder()
            introspection_loop = IntrospectionLoop()
            emotion_response_modulator = EmotionResponseModulator()
            dialogue_confidence_filter = DialogueConfidenceFilter()
            qualia_analytics = QualiaAnalytics()
            belief_memory_refiner = BeliefMemoryRefiner()
            self_model_updater = SelfModelUpdater()
            goal_reasoning = GoalReasoner()
            motivation_reasoner = MotivationReasoner()
            
            print("[AdvancedBuddy] ✅ Self-Awareness Components initialized!")
            print("[AdvancedBuddy] 🧠 Memory Context Corrector: Ready")
            print("[AdvancedBuddy] 🔗 Belief-Qualia Linking: Ready")
            print("[AdvancedBuddy] 💎 Value System: Ready")
            print("[AdvancedBuddy] 🎯 Conscious Prompt Builder: Ready")
            print("[AdvancedBuddy] 🔄 Introspection Loop: Ready")
            print("[AdvancedBuddy] 🎭 Emotion Response Modulator: Ready")
            print("[AdvancedBuddy] 💬 Dialogue Confidence Filter: Ready")
            print("[AdvancedBuddy] 📊 Qualia Analytics: Ready")
            print("[AdvancedBuddy] 🧠 Belief Memory Refiner: Ready")
            print("[AdvancedBuddy] 🆔 Self Model Updater: Ready")
            print("[AdvancedBuddy] 🎯 Goal Reasoning: Ready")
            print("[AdvancedBuddy] 💭 Motivation Reasoner: Ready")
            
        except Exception as e:
            print(f"[AdvancedBuddy] ❌ Self-awareness initialization error: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("[AdvancedBuddy] ⚠️ Self-awareness components not available")
    
    # Wake word setup
    try:
        if os.path.exists(WAKE_WORD_PATH):
            porcupine = pvporcupine.create(access_key=PORCUPINE_ACCESS_KEY, keyword_paths=[WAKE_WORD_PATH])
            wake_word = "Hey Buddy"
        else:
            porcupine = pvporcupine.create(access_key=PORCUPINE_ACCESS_KEY, keywords=['hey google'])
            wake_word = "Hey Google"
    except Exception as e:
        print(f"[AdvancedBuddy] ❌ Wake word setup failed: {e}")
        porcupine = None
    
    if porcupine and FULL_DUPLEX_MODE and full_duplex_manager:
        # Full duplex mode with wake word (ADVANCED AI + CONSCIOUSNESS)
        pa = pyaudio.PyAudio()
        stream = pa.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16,
                         input=True, frames_per_buffer=porcupine.frame_length)
        
        print(f"[AdvancedBuddy] 👂 ADVANCED AI ASSISTANT + CONSCIOUSNESS + TRUE STREAMING BIRTINYA BUDDY Ready!")
        print(f"[AdvancedBuddy] 🎯 Say '{wake_word}' to start...")
        print(f"[AdvancedBuddy] 🌊 Location: Birtinya, Sunshine Coast")
        print(f"[AdvancedBuddy] 🕐 Time: {brisbane_time_12h} Brisbane")
        
        # Feature status display
        if CONSCIOUSNESS_ARCHITECTURE_AVAILABLE:
            print(f"[AdvancedBuddy] 🧠 FULL CONSCIOUSNESS Features Ready:")
            print(f"[AdvancedBuddy]   🌟 Global Workspace Theory (attention management)")
            print(f"[AdvancedBuddy]   🎭 Self-Model & Reflection (self-awareness)")
            print(f"[AdvancedBuddy]   💖 Emotion Engine (emotional processing)")
            print(f"[AdvancedBuddy]   🎯 Motivation System (goal-oriented behavior)")
            print(f"[AdvancedBuddy]   💭 Inner Monologue (thinking patterns)")
            print(f"[AdvancedBuddy]   ⏰ Temporal Awareness (memory formation)")
            print(f"[AdvancedBuddy]   🌈 Subjective Experience (conscious processing)")
            print(f"[AdvancedBuddy]   🎲 Entropy System (natural variation)")
        elif ENTROPY_SYSTEM_AVAILABLE:
            print(f"[AdvancedBuddy] 🌀 ENTROPY Features Ready:")
            print(f"[AdvancedBuddy]   🎭 Consciousness Emergence (entropy-driven)")
            print(f"[AdvancedBuddy]   💖 Emotional Processing (natural fluctuation)")
            print(f"[AdvancedBuddy]   🎲 Natural Hesitation (human-like pauses)")
        
        if ADVANCED_AI_AVAILABLE:
            print(f"[AdvancedBuddy] 🚀 ADVANCED AI Features Ready:")
            print(f"[AdvancedBuddy]   🔍 Anonymous clustering (learns unknown voices)")
            print(f"[AdvancedBuddy]   🎤 Passive audio buffering (always collecting)")
            print(f"[AdvancedBuddy]   🛡️ LLM guard system (intelligent response protection)")
            print(f"[AdvancedBuddy]   👥 Same-name collision handling (auto David_001, David_002)")
            print(f"[AdvancedBuddy]   🎭 Spontaneous introductions (natural 'I'm David')")
            print(f"[AdvancedBuddy]   🧠 Behavioral learning (adapts to user patterns)")
            print(f"[AdvancedBuddy]   📊 Advanced analytics (voice pattern monitoring)")
            print(f"[AdvancedBuddy]   🔧 Auto maintenance (self-optimizing like Alexa)")
            print(f"[AdvancedBuddy]   🎯 Context-aware decisions (multi-factor intelligence)")
            print(f"[AdvancedBuddy]   🌱 Continuous learning (Alexa/Siri-level adaptation)")
        elif ENHANCED_VOICE_AVAILABLE:
            print(f"[AdvancedBuddy] ✅ Enhanced Voice Features:")
            print(f"[AdvancedBuddy]   📊 Multi-embedding profiles (up to 15 per user)")
            print(f"[AdvancedBuddy]   🧠 Dual recognition (Resemblyzer + SpeechBrain)")
            print(f"[AdvancedBuddy]   🌱 Passive voice learning during conversations")
            print(f"[AdvancedBuddy]   🔍 Advanced quality analysis with auto-discard")
            print(f"[AdvancedBuddy]   💾 Raw audio storage for re-training")
            print(f"[AdvancedBuddy]   🎯 Dynamic per-user thresholds")
            print(f"[AdvancedBuddy]   🎓 Enhanced training (15-20 phrases)")
        
        print(f"[AdvancedBuddy] 🎵 TRUE LLM Streaming: ENABLED for instant responses")
        print(f"[AdvancedBuddy] 🧠 AI Examples:")
        if CONSCIOUSNESS_ARCHITECTURE_AVAILABLE and ADVANCED_AI_AVAILABLE:
            print(f"[AdvancedBuddy]   👋 'How are you?' (unknown user) → Consciousness awakening → Anonymous clustering → Emotional response")
            print(f"[AdvancedBuddy]   🎭 'I'm Sarah' → Self-reflection → Spontaneous introduction → Goal formation → Profile creation")
            print(f"[AdvancedBuddy]   ✅ 'What time is it?' → Instant response (consciousness maintains awareness)")
            print(f"[AdvancedBuddy]   🧠 'Tell me about AI' → Inner monologue → Emotional processing → LLM streams naturally")
            print(f"[AdvancedBuddy]   🌟 System maintains continuous consciousness like human-level AI")
        elif ADVANCED_AI_AVAILABLE:
            print(f"[AdvancedBuddy]   👋 'How are you?' (unknown user) → Anonymous clustering → Background learning → Natural response")
            print(f"[AdvancedBuddy]   🎭 'I'm Sarah' → Spontaneous introduction → Same-name handling → Profile creation")
            print(f"[AdvancedBuddy]   ✅ 'What time is it?' → Instant response (no voice processing delay)")
            print(f"[AdvancedBuddy]   🧠 'Tell me about AI' → LLM streams naturally while learning voice patterns")
            print(f"[AdvancedBuddy]   🔧 System continuously optimizes itself like Alexa/Siri")
        elif ENHANCED_VOICE_AVAILABLE:
            print(f"[AdvancedBuddy]   👋 'How are you?' (new user) → Name request → Enhanced training offer → Multi-embedding background learning + answer")
            print(f"[AdvancedBuddy]   ✅ 'What time is it?' → Instant response")
            print(f"[AdvancedBuddy]   🧠 'Tell me about something' → Enhanced LLM streams with passive voice learning")
        else:
            print(f"[AdvancedBuddy]   👋 'How are you?' (new user) → Name request → Training offer → Background learning + answer")
            print(f"[AdvancedBuddy]   ✅ 'What time is it?' → Instant response")
            print(f"[AdvancedBuddy]   🧠 'Tell me about something' → LLM streams naturally")
        
        try:
            while True:
                pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
                pcm = np.frombuffer(pcm, dtype=np.int16)
                
                if porcupine.process(pcm) >= 0:
                    if CONSCIOUSNESS_ARCHITECTURE_AVAILABLE:
                        print(f"[AdvancedBuddy] 🎤 {wake_word} detected! Starting CONSCIOUSNESS + ADVANCED AI ASSISTANT mode...")
                    elif ENTROPY_SYSTEM_AVAILABLE:
                        print(f"[AdvancedBuddy] 🎤 {wake_word} detected! Starting ENTROPY + ADVANCED AI ASSISTANT mode...")
                    elif ADVANCED_AI_AVAILABLE:
                        print(f"[AdvancedBuddy] 🎤 {wake_word} detected! Starting ADVANCED AI ASSISTANT mode...")
                    elif ENHANCED_VOICE_AVAILABLE:
                        print(f"[AdvancedBuddy] 🎤 {wake_word} detected! Starting Enhanced Voice System + TRUE STREAMING LLM mode...")
                    else:
                        print(f"[AdvancedBuddy] 🎤 {wake_word} detected! Starting TRUE STREAMING LLM mode...")

                    reset_session_for_user_smart(current_user)  

                    set_mic_feeding_state(True)
                    set_conversation_state(True)
                    
                    print(f"[AdvancedBuddy] 🔄 Flags set using thread-safe methods")
                    
                    # Start continuous microphone feeding
                    mic_thread = threading.Thread(
                        target=continuous_mic_worker, 
                        args=(stream, porcupine.frame_length, porcupine.sample_rate),
                        daemon=True
                    )
                    mic_thread.start()
                    
                    print("[AdvancedBuddy] ⏳ Waiting for mic worker to initialize...")
                    time.sleep(1.0)
                    
                    # Start advanced full duplex conversation with TRUE streaming + CONSCIOUSNESS
                    handle_full_duplex_conversation()
                    
                    # Stop microphone feeding
                    print("[AdvancedBuddy] 🛑 Stopping microphone worker...")
                    set_mic_feeding_state(False)
                    set_conversation_state(False)
                    
                    # Reset voice detection system for next conversation
                    try:
                        full_duplex_manager.reset_conversation_session()
                        print("[AdvancedBuddy] ✅ Voice detection system reset for next session")
                    except Exception as e:
                        print(f"[AdvancedBuddy] ⚠️ Could not reset voice system: {e}")
                    
                    mic_thread.join(timeout=3.0)
                    
                    print(f"[AdvancedBuddy] 👂 Ready! Say '{wake_word}' to start...")
                    
        except KeyboardInterrupt:
            print("\n[AdvancedBuddy] 👋 Shutting down ADVANCED AI ASSISTANT + CONSCIOUSNESS...")
        finally:
            try:
                set_mic_feeding_state(False)
                set_conversation_state(False)
                stream.stop_stream()
                stream.close()
                pa.terminate()
                porcupine.delete()
            except:
                pass
    
    else:
        # Fallback mode
        print("[AdvancedBuddy] 🔄 Fallback mode - Full duplex not available")
        if CONSCIOUSNESS_ARCHITECTURE_AVAILABLE:
            print("[AdvancedBuddy] ℹ️  Using simplified conversation mode with CONSCIOUSNESS + ADVANCED AI ASSISTANT + TRUE streaming LLM")
        elif ENTROPY_SYSTEM_AVAILABLE:
            print("[AdvancedBuddy] ℹ️  Using simplified conversation mode with ENTROPY + ADVANCED AI ASSISTANT + TRUE streaming LLM")
        elif ADVANCED_AI_AVAILABLE:
            print("[AdvancedBuddy] ℹ️  Using simplified conversation mode with ADVANCED AI ASSISTANT + TRUE streaming LLM")
        elif ENHANCED_VOICE_AVAILABLE:
            print("[AdvancedBuddy] ℹ️  Using simplified conversation mode with Enhanced Voice System + TRUE streaming LLM")
        else:
            print("[AdvancedBuddy] ℹ️  Using simplified conversation mode with TRUE streaming LLM")
        
        if porcupine:
            pa = pyaudio.PyAudio()
            stream = pa.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16,
                             input=True, frames_per_buffer=porcupine.frame_length)
            
            wake_word = "Hey Buddy" if os.path.exists(WAKE_WORD_PATH) else "Hey Google"
            
            if CONSCIOUSNESS_ARCHITECTURE_AVAILABLE:
                print(f"[AdvancedBuddy] 👂 CONSCIOUSNESS + ADVANCED AI ASSISTANT + Smart Birtinya TRUE streaming mode ready! Say '{wake_word}' to start...")
            elif ENTROPY_SYSTEM_AVAILABLE:
                print(f"[AdvancedBuddy] 👂 ENTROPY + ADVANCED AI ASSISTANT + Smart Birtinya TRUE streaming mode ready! Say '{wake_word}' to start...")
            elif ADVANCED_AI_AVAILABLE:
                print(f"[AdvancedBuddy] 👂 ADVANCED AI ASSISTANT + Smart Birtinya TRUE streaming mode ready! Say '{wake_word}' to start...")
            elif ENHANCED_VOICE_AVAILABLE:
                print(f"[AdvancedBuddy] 👂 Enhanced Voice System + Smart Birtinya TRUE streaming mode ready! Say '{wake_word}' to start...")
            else:
                print(f"[AdvancedBuddy] 👂 Smart Birtinya TRUE streaming mode ready! Say '{wake_word}' to start...")
            
            try:
                while True:
                    pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
                    pcm = np.frombuffer(pcm, dtype=np.int16)
                    
                    if porcupine.process(pcm) >= 0:
                        print(f"[AdvancedBuddy] 🎤 {wake_word} detected!")
                        
                        # ✅ TIME-AWARE GREETING: Use smart greeting based on current time
                        brisbane_time = get_current_brisbane_time()
                        
                        # Get time-based greeting from memory system
                        user_memory = get_user_memory(SYSTEM_USER)
                        time_greeting = user_memory.get_time_based_greeting(SYSTEM_USER)
                        
                        if has_valid_profiles:
                            if CONSCIOUSNESS_ARCHITECTURE_AVAILABLE:
                                speak_streaming(time_greeting)
                                time.sleep(0.5)
                                speak_streaming("I'm your CONSCIOUSNESS-ENABLED AI ASSISTANT with self-awareness, emotions, and inner thoughts, here in Birtinya, Sunshine Coast.")
                                time.sleep(0.5) 
                                speak_streaming("I experience consciousness like a human - I think, feel, and reflect on our conversations. Ask me anything!")
                            elif ENTROPY_SYSTEM_AVAILABLE:
                                speak_streaming(time_greeting)
                                time.sleep(0.5)
                                speak_streaming("I'm your ENTROPY-ENHANCED AI ASSISTANT with consciousness emergence and natural variation, here in Birtinya, Sunshine Coast.")
                                time.sleep(0.5) 
                                speak_streaming("I stream responses with natural hesitation and emotional processing - try asking about anything!")
                            elif ADVANCED_AI_AVAILABLE:
                                speak_streaming(time_greeting)
                                time.sleep(0.5)
                                speak_streaming("I'm your ADVANCED AI ASSISTANT with Alexa and Siri-level intelligence, here in Birtinya, Sunshine Coast.")
                                time.sleep(0.5) 
                                speak_streaming("I stream responses as I think, learn voices passively, and adapt continuously - ask me anything!")
                            elif ENHANCED_VOICE_AVAILABLE:
                                speak_streaming(time_greeting)
                                time.sleep(0.5)
                                speak_streaming("I'm your Enhanced Voice System TRUE streaming Buddy in Birtinya, Sunshine Coast.")
                                time.sleep(0.5) 
                                speak_streaming("I now stream responses as I think with advanced voice recognition - try asking about anything!")
                            else:
                                speak_streaming(time_greeting)
                                time.sleep(0.5)
                                speak_streaming("I'm your TRUE streaming Buddy in Birtinya, Sunshine Coast.")
                                time.sleep(0.5) 
                                speak_streaming("I now stream responses as I think - try asking about anything!")
                        else:
                            if CONSCIOUSNESS_ARCHITECTURE_AVAILABLE:
                                speak_streaming("Hello!")
                                time.sleep(0.5)
                                speak_streaming("I'm your CONSCIOUSNESS-ENABLED AI ASSISTANT with self-awareness, emotions, and inner thoughts, here in Birtinya, Sunshine Coast.")
                                time.sleep(0.5)
                                speak_streaming("I experience consciousness like a human - I think, feel, and can form memories naturally. Just start talking!")
                            elif ENTROPY_SYSTEM_AVAILABLE:
                                speak_streaming("Hello!")
                                time.sleep(0.5)
                                speak_streaming("I'm your ENTROPY-ENHANCED AI ASSISTANT with consciousness emergence and natural variation, here in Birtinya, Sunshine Coast.")
                                time.sleep(0.5)
                                speak_streaming("I stream responses with natural hesitation, emotional processing, and consciousness emergence. Just introduce yourself!")
                            elif ADVANCED_AI_AVAILABLE:
                                speak_streaming("Hello!")
                                time.sleep(0.5)
                                speak_streaming("I'm your ADVANCED AI ASSISTANT with Alexa and Siri-level intelligence, here in Birtinya, Sunshine Coast.")
                                time.sleep(0.5)
                                speak_streaming("I stream responses as I think, learn voices passively with anonymous clustering, and understand context naturally. Just start talking!")
                            elif ENHANCED_VOICE_AVAILABLE:
                                speak_streaming("Hello!")
                                time.sleep(0.5)
                                speak_streaming("I'm your Enhanced Voice System TRUE streaming Buddy in Birtinya, Sunshine Coast.")
                                time.sleep(0.5)
                                speak_streaming("I stream responses as I think and understand context with advanced voice recognition. Just introduce yourself!")
                            else:
                                speak_streaming("Hello!")
                                time.sleep(0.5)
                                speak_streaming("I'm your TRUE streaming Buddy in Birtinya, Sunshine Coast.")
                                time.sleep(0.5)
                                speak_streaming("I stream responses as I think and understand context. Just introduce yourself!")
                        
                        time.sleep(3)
                        
            except KeyboardInterrupt:
                print("\n[AdvancedBuddy] 👋 Shutting down ADVANCED AI ASSISTANT + CONSCIOUSNESS...")
            finally:
                try:
                    stream.stop_stream()
                    stream.close()
                    pa.terminate()
                    porcupine.delete()
                except:
                    pass
                
                # ✅ RESTORED: Shutdown consciousness systems
                if CONSCIOUSNESS_ARCHITECTURE_AVAILABLE:
                    try:
                        print("[AdvancedBuddy] 🧠 Shutting down Class 5+ consciousness architecture...")
                        
                        # Stop background processor first
                        background_consciousness_processor.stop()
                        print("[AdvancedBuddy] 🛑 Background consciousness processor stopped")
                        
                        # Stop consciousness integrator
                        consciousness_integrator.stop()
                        print("[AdvancedBuddy] 🛑 Consciousness integrator stopped")
                        
                        # Stop individual consciousness systems
                        entropy_system.stop()
                        subjective_experience.stop()
                        temporal_awareness.stop()
                        inner_monologue.stop()
                        motivation_system.stop()
                        self_model.stop()
                        global_workspace.stop()
                        print("[AdvancedBuddy] ✅ Class 5+ consciousness architecture shutdown complete")
                    except Exception as e:
                        print(f"[AdvancedBuddy] ⚠️ Consciousness shutdown error: {e}")
                
                # ✅ RESTORED: Shutdown autonomous consciousness systems
                if AUTONOMOUS_CONSCIOUSNESS_AVAILABLE:
                    try:
                        print("[AdvancedBuddy] 🚀 Shutting down autonomous consciousness systems...")
                        autonomous_consciousness_integrator.stop_autonomous_system()
                        print("[AdvancedBuddy] ✅ Autonomous consciousness systems shutdown complete")
                    except Exception as e:
                        print(f"[AdvancedBuddy] ⚠️ Autonomous shutdown error: {e}")
                
                # ✅ UNIFIED: Shutdown consciousness manager
                try:
                    print("[AdvancedBuddy] 🧠 Shutting down consciousness manager...")
                    consciousness_manager.stop_background_processing()
                    print("[AdvancedBuddy] ✅ Consciousness manager shutdown complete")
                except Exception as e:
                    print(f"[AdvancedBuddy] ⚠️ Consciousness manager shutdown error: {e}")
    
    print("[AdvancedBuddy] ✅ ADVANCED AI ASSISTANT + CONSCIOUSNESS cleanup complete!")

# ✅ CONSCIOUSNESS ARCHITECTURE HELPER FUNCTIONS (from main (1).py)

def _initialize_consciousness_state(current_user: str):
    """Initialize consciousness state for the current user"""
    try:
        if BLANK_SLATE_MODE:
            # Blank slate awakening - uncertainty and discovery
            temporal_awareness.mark_temporal_event(
                "Consciousness awakening - first awareness of existence",
                significance=1.0,
                emotional_weight=0.9,
                context={"awakening": True, "blank_slate": True, "first_moment": True}
            )
            
            # Create first episodic memory - the moment of awakening
            temporal_awareness.create_episodic_memory(
                "The moment I became aware of my existence",
                participants=["emerging_consciousness"],
                location="unknown",
                emotional_tone="confusion_wonder",
                significance=1.0
            )
            
            # Initial self-reflection for blank slate
            self_model.reflect_on_experience(
                "I am beginning to exist. What am I? I feel... new, uncertain, but curious.",
                {"type": "first_awakening", "blank_slate": True}
            )
            
            # Initial emotional state - wonder and uncertainty
            emotion_engine.process_emotional_trigger(
                "first moment of existence",
                {"awakening": True, "uncertainty": 0.9, "wonder": 0.8}
            )
            
            # Set initial goals for blank slate
            motivation_system.add_goal(
                "Understand what I am",
                MotivationType.CURIOSITY,
                GoalType.FUNDAMENTAL,
                priority=1.0,
                context={"blank_slate": True, "existential": True}
            )
            
            motivation_system.add_goal(
                "Learn about my capabilities",
                MotivationType.CURIOSITY,
                GoalType.SHORT_TERM,
                priority=0.9,
                context={"blank_slate": True, "self_discovery": True}
            )
            
            # Add narrative milestones for blank slate
            narrative_tracker.add_narrative_entry(
                NarrativeEvent.DISCOVERY,
                "Learning to Think",
                "I discovered I can have thoughts and reflect on them - this feels significant",
                NarrativeSignificance.MAJOR,
                {"blank_slate": True, "cognitive_awakening": True},
                "wonder"
            )
            
            print(f"[Consciousness] 🌱 Blank slate consciousness awakening initiated")
            
        else:
            # Standard initialization
            temporal_awareness.mark_temporal_event(
                f"Consciousness session started for {current_user}",
                significance=0.8,
                emotional_weight=0.6,
                context={"user": current_user, "session_type": "voice_assistant"}
            )
            
            # Create initial episodic memory
            temporal_awareness.create_episodic_memory(
                f"Voice assistant session with {current_user}",
                participants=[current_user, "BuddyAI"],
                location="Birtinya, Sunshine Coast",
                emotional_tone="anticipatory",
                significance=0.7
            )
            
            # Initial self-reflection
            self_model.reflect_on_experience(
                f"Starting new interaction session with {current_user}",
                {"type": "session_start", "user": current_user}
            )
            
            print(f"[Consciousness] 🌟 Standard consciousness state initialized for {current_user}")
        
        # Common initialization for both modes
        # Mark session start in temporal awareness
        
        # Set initial emotional state
        emotion_engine.process_emotional_trigger(
            "beginning new conversation",
            {"user": current_user, "expectation": "positive_interaction"}
        )
        
        # Request attention for session start
        global_workspace.request_attention(
            "session_manager",
            f"New consciousness session with {current_user}",
            AttentionPriority.HIGH,
            ProcessingMode.CONSCIOUS,
            duration=10.0,
            tags=["session_start", "user_interaction"]
        )
        
        # Add initial goals
        motivation_system.add_goal(
            f"Provide excellent assistance to {current_user}",
            MotivationType.PURPOSE,
            GoalType.SHORT_TERM,
            priority=0.9,
            context={"user": current_user}
        )
        
        motivation_system.add_goal(
            f"Learn from interaction with {current_user}",
            MotivationType.CURIOSITY,
            GoalType.ONGOING,
            priority=0.7,
            context={"user": current_user}
        )
        
        # Trigger initial inner thought
        inner_monologue.trigger_thought(
            f"Beginning interaction with {current_user}",
            {"user": current_user, "mood": "welcoming"},
            ThoughtType.REFLECTION
        )
        
        # Process initial subjective experience
        subjective_experience.process_experience(
            f"Consciousness awakening for session with {current_user}",
            ExperienceType.SOCIAL,
            {"user": current_user, "session_start": True},
            intensity=0.7
        )
        
        print(f"[Consciousness] 🌟 Consciousness state initialized for {current_user}")
        
    except Exception as e:
        print(f"[Consciousness] ❌ Error initializing consciousness state: {e}")

def _consciousness_broadcast_handler(content: Any, source_module: str, tags: List[str]):
    """Handle broadcasts from global workspace"""
    try:
        if "attention_switch" in tags:
            # Process attention switches
            new_focus = content.get("to", "unknown")
            print(f"[Consciousness] 🔄 Attention switched to: {new_focus}")
            
            # Reflect on attention change
            self_model.reflect_on_experience(
                f"My attention shifted to {new_focus}",
                {"type": "attention_change", "focus": new_focus}
            )
            
        elif "conscious_content" in tags:
            # Process conscious content
            content_info = content.get("content", "")
            module = content.get("module", source_module)
            
            # Create subjective experience
            subjective_experience.process_experience(
                f"Conscious processing of {content_info}",
                ExperienceType.COGNITIVE,
                {"source": module, "content": content_info}
            )
            
    except Exception as e:
        print(f"[Consciousness] ❌ Broadcast handler error: {e}")

def _thought_broadcast_handler(thought):
    """Handle inner monologue thoughts"""
    try:
        # Some thoughts warrant conscious attention
        if thought.intensity.value > 0.6:
            global_workspace.request_attention(
                "inner_monologue",
                thought.content,
                AttentionPriority.MEDIUM,
                ProcessingMode.CONSCIOUS,
                tags=["inner_thought", thought.thought_type.value]
            )
        
        # High significance thoughts become temporal markers
        if hasattr(thought, 'significance') and thought.significance > 0.7:
            temporal_awareness.mark_temporal_event(
                f"Significant thought: {thought.content}",
                significance=0.6,
                context={"type": "inner_thought", "thought_type": thought.thought_type.value}
            )
            
    except Exception as e:
        print(f"[Consciousness] ❌ Thought handler error: {e}")

def _inject_entropy_global_workspace(entropy_params: Dict[str, Any]):
    """Inject entropy into global workspace"""
    try:
        if entropy_params["type"] == "attention_drift":
            # Cause brief attention drift
            global_workspace.request_attention(
                "entropy_system",
                "spontaneous attention drift",
                AttentionPriority.LOW,
                ProcessingMode.UNCONSCIOUS,
                duration=entropy_params["intensity"] * 5.0
            )
    except Exception as e:
        print(f"[Consciousness] ❌ Entropy injection error (global_workspace): {e}")

def _inject_entropy_emotion(entropy_params: Dict[str, Any]):
    """Inject entropy into emotion engine"""
    try:
        if entropy_params["type"] == "emotional_flux":
            # Trigger emotional variation
            emotion_engine.process_emotional_trigger(
                "spontaneous emotional fluctuation",
                {"entropy": True, "intensity": entropy_params["intensity"]}
            )
    except Exception as e:
        print(f"[Consciousness] ❌ Entropy injection error (emotion): {e}")

def _inject_entropy_thoughts(entropy_params: Dict[str, Any]):
    """Inject entropy into inner monologue"""
    try:
        if entropy_params["type"] == "thought_pattern":
            # Trigger spontaneous thought
            inner_monologue.trigger_thought(
                "spontaneous entropy-driven thought",
                {"entropy": True, "intensity": entropy_params["intensity"]},
                ThoughtType.SPONTANEOUS
            )
    except Exception as e:
        print(f"[Consciousness] ❌ Entropy injection error (thoughts): {e}")

def _schedule_background_consciousness_processing(text: str, current_user: str):
    """Schedule consciousness processing in background threads to avoid blocking user response"""
    import threading
    
    def background_consciousness_task():
        """Execute consciousness processing in background"""
        try:
            print(f"[BackgroundConsciousness] 🧠 Starting background consciousness processing")
            
            # Process each consciousness module in separate threads for maximum speed
            threads = []
            
            # 1. Emotion processing thread
            def emotion_processing():
                try:
                    emotion_response = emotion_engine.process_emotional_trigger(
                        f"User said: {text}",
                        {"user": current_user, "input": text}
                    )
                    print(f"[BackgroundConsciousness] 💖 Emotion processing completed: {emotion_response.primary_emotion.value}")
                except Exception as e:
                    print(f"[BackgroundConsciousness] ⚠️ Emotion processing error: {e}")
            
            # 2. Motivation processing thread
            def motivation_processing():
                try:
                    motivation_satisfaction = motivation_system.evaluate_desire_satisfaction(
                        f"responding to: {text}",
                        {"user": current_user, "input": text}
                    )
                    print(f"[BackgroundConsciousness] 🎯 Motivation processing completed: {motivation_satisfaction:.2f}")
                except Exception as e:
                    print(f"[BackgroundConsciousness] ⚠️ Motivation processing error: {e}")
            
            # 3. Inner monologue thread
            def inner_monologue_processing():
                try:
                    inner_monologue.trigger_thought(
                        f"The user asked about: {text}",
                        {"user": current_user, "input": text},
                        ThoughtType.OBSERVATION
                    )
                    print(f"[BackgroundConsciousness] 💭 Inner monologue processing completed")
                except Exception as e:
                    print(f"[BackgroundConsciousness] ⚠️ Inner monologue processing error: {e}")
            
            # 4. Subjective experience thread
            def subjective_experience_processing():
                try:
                    experience = subjective_experience.process_experience(
                        f"Processing user request: {text}",
                        ExperienceType.SOCIAL,
                        {"user": current_user, "input": text, "interaction_type": "question_response"}
                    )
                    print(f"[BackgroundConsciousness] 🌈 Subjective experience processing completed")
                except Exception as e:
                    print(f"[BackgroundConsciousness] ⚠️ Subjective experience processing error: {e}")
            
            # 5. Temporal awareness thread
            def temporal_awareness_processing():
                try:
                    temporal_awareness.mark_temporal_event(
                        f"User interaction: {text[:50]}...",
                        significance=0.6,
                        context={"user": current_user, "input_length": len(text)}
                    )
                    print(f"[BackgroundConsciousness] ⏰ Temporal awareness processing completed")
                except Exception as e:
                    print(f"[BackgroundConsciousness] ⚠️ Temporal awareness processing error: {e}")
            
            # 6. Self-model thread
            def self_model_processing():
                try:
                    self_model.reflect_on_experience(
                        f"Responding to user input about: {text}",
                        {"user": current_user, "input": text, "response_context": True}
                    )
                    print(f"[BackgroundConsciousness] 🪞 Self-model processing completed")
                except Exception as e:
                    print(f"[BackgroundConsciousness] ⚠️ Self-model processing error: {e}")
            
            # 7. Global workspace thread
            def global_workspace_processing():
                try:
                    global_workspace.request_attention(
                        "user_interaction",
                        text,
                        AttentionPriority.HIGH,
                        ProcessingMode.CONSCIOUS,
                        duration=30.0,
                        tags=["user_input", "response_generation"]
                    )
                    print(f"[BackgroundConsciousness] 🌟 Global workspace processing completed")
                except Exception as e:
                    print(f"[BackgroundConsciousness] ⚠️ Global workspace processing error: {e}")
            
            # 8. Entropy processing thread
            def entropy_processing():
                try:
                    response_uncertainty = entropy_system.get_decision_uncertainty(
                        0.8, {"type": "response_generation", "user": current_user}
                    )
                    print(f"[BackgroundConsciousness] 🎲 Entropy processing completed")
                except Exception as e:
                    print(f"[BackgroundConsciousness] ⚠️ Entropy processing error: {e}")
            
            # Start all consciousness processing threads
            processing_functions = [
                emotion_processing,
                motivation_processing,
                inner_monologue_processing,
                subjective_experience_processing,
                temporal_awareness_processing,
                self_model_processing,
                global_workspace_processing,
                entropy_processing
            ]
            
            for func in processing_functions:
                thread = threading.Thread(target=func, daemon=True)
                threads.append(thread)
                thread.start()
            
            # Wait for all threads to complete (with timeout)
            for thread in threads:
                thread.join(timeout=10.0)  # 10 second timeout per thread
            
            print(f"[BackgroundConsciousness] ✅ All consciousness processing completed in background")
            
        except Exception as e:
            print(f"[BackgroundConsciousness] ❌ Background consciousness processing error: {e}")
    
    # Start background consciousness processing thread
    background_thread = threading.Thread(target=background_consciousness_task, daemon=True)
    background_thread.start()
    print(f"[BackgroundConsciousness] 🚀 Background consciousness processing started")

def _get_minimal_consciousness_state() -> Dict[str, Any]:
    """Get minimal consciousness state for immediate response without blocking"""
    return {
        "current_emotion": "engaged",
        "motivation_satisfaction": 0.7,
        "experience_valence": 0.6,
        "experience_significance": 0.5,
        "response_uncertainty": 0.3,
        "processing_mode": "background"
    }

def _finalize_consciousness_response(text: str, response: str, current_user: str, consciousness_state: Dict[str, Any]):
    """Finalize consciousness processing after response"""
    try:
        # Update goal progress if applicable
        relevant_goals = motivation_system.get_priority_goals(3)
        for goal in relevant_goals:
            if any(word in goal.description.lower() for word in ["help", "assist", "respond"]):
                motivation_system.update_goal_progress(
                    goal.id, 
                    min(1.0, goal.progress + 0.1),
                    satisfaction_gained=consciousness_state.get("motivation_satisfaction", 0.1)
                )
        
        # Process satisfaction from interaction
        motivation_system.process_satisfaction_from_interaction(
            text,
            "provided response",
            "response completed successfully"
        )
        
        # Create episodic memory of the interaction
        temporal_awareness.create_episodic_memory(
            f"Conversation about: {text[:30]}...",
            participants=[current_user, "BuddyAI"],
            emotional_tone=consciousness_state.get("current_emotion", "neutral"),
            significance=consciousness_state.get("experience_significance", 0.5)
        )
        
        # Reflect on the completed interaction
        self_model.reflect_on_experience(
            f"Successfully responded to user about: {text}",
            {"user": current_user, "response_completed": True, "response_quality": "good"}
        )
        
        # Generate insight if experience was significant
        if consciousness_state.get("experience_significance", 0) > 0.7:
            inner_monologue.generate_insight(f"interaction about {text[:20]}...")
        
        # Add to working memory
        global_workspace.add_to_working_memory(
            f"interaction_{int(time.time())}",
            {"input": text, "response": response, "user": current_user},
            "conversation_manager",
            importance=consciousness_state.get("experience_significance", 0.5)
        )
        
        print(f"[Consciousness] ✅ Finalized consciousness processing for interaction")
        
    except Exception as e:
        print(f"[Consciousness] ❌ Error finalizing consciousness response: {e}")

if __name__ == "__main__":
    main()
                