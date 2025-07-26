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
from datetime import datetime  # ✅ ADD THIS IMPORT
from typing import List, Any, Dict  # ✅ NEW: Add typing imports for consciousness functions
from scipy.io.wavfile import write
from voice.database import load_known_users, known_users, save_known_users, anonymous_clusters
from ai.memory import validate_ai_response_appropriateness, add_to_conversation_history
from ai.chat_enhanced_smart import generate_response_streaming_with_smart_memory, reset_session_for_user_smart
from ai.chat_enhanced_smart_with_fusion import generate_response_streaming_with_intelligent_fusion
from audio.smart_detection_manager import analyze_speech_detection, get_current_threshold

# ✅ NEW: Blank slate initialization configuration
BLANK_SLATE_MODE = os.getenv('BUDDY_BLANK_SLATE', 'false').lower() == 'true'
if BLANK_SLATE_MODE:
    print("[Main] 🌱 BLANK SLATE MODE ENABLED - Starting with minimal identity")
else:
    print("[Main] 🧠 Standard mode - Loading established consciousness")

# ✅ ENTROPY SYSTEM: Import consciousness emergence components (from main (2).py)
try:
    from ai.entropy_engine import get_entropy_engine, inject_consciousness_entropy, should_surprise, get_random_hesitation
    from ai.emotion import get_emotional_system, process_emotional_context, inject_emotional_surprise
    print("[Main] 🌀 Entropy and consciousness systems loaded")
    ENTROPY_SYSTEM_AVAILABLE = True
except ImportError as e:
    print(f"[Main] ⚠️ Entropy system not available: {e}")
    ENTROPY_SYSTEM_AVAILABLE = False

# ✅ NEW: Import full consciousness architecture modules with blank slate support
try:
    from ai.global_workspace import global_workspace, AttentionPriority, ProcessingMode
    
    # Import SelfModel class and create instance with appropriate mode
    from ai.self_model import SelfModel, SelfAspect
    if BLANK_SLATE_MODE:
        self_model = SelfModel(save_path="ai_self_model_blank.json", initialize_blank=True)
        print("[Main] 🌱 Blank slate self-model initialized")
    else:
        from ai.self_model import self_model
        print("[Main] 🧠 Standard self-model loaded")
    
    from ai.emotion import emotion_engine, EmotionType, MoodType
    from ai.motivation import motivation_system, MotivationType, GoalType
    from ai.inner_monologue import inner_monologue, ThoughtType
    from ai.temporal_awareness import temporal_awareness, TemporalScale
    from ai.subjective_experience import subjective_experience, ExperienceType
    from ai.entropy import entropy_system, EntropyType
    
    # Import new autonomous consciousness components
    from ai.free_thought_engine import free_thought_engine, FreeThoughtType
    from ai.narrative_tracker import narrative_tracker, NarrativeEvent, NarrativeSignificance
    
    print("[Main] 🧠 Full consciousness architecture loaded")
    print("[Main] 💭 Autonomous consciousness components: Free Thought Engine, Narrative Tracker")
    CONSCIOUSNESS_ARCHITECTURE_AVAILABLE = True
except ImportError as e:
    print(f"[Main] ⚠️ Full consciousness architecture not available: {e}")
    CONSCIOUSNESS_ARCHITECTURE_AVAILABLE = False

# ✅ NEW: Import consciousness-integrated modules with latency optimization
try:
    from ai.llm_handler import (
        llm_handler,
        process_user_input_with_consciousness,
        generate_consciousness_integrated_response,
        get_llm_session_statistics
    )
    print("[Main] 🧠 Consciousness-integrated LLM handler loaded")
    CONSCIOUSNESS_LLM_AVAILABLE = True
except ImportError as e:
    print(f"[Main] ⚠️ Consciousness LLM handler not available: {e}")
    CONSCIOUSNESS_LLM_AVAILABLE = False

# ✅ NEW: Import latency optimization system for sub-5-second responses
try:
    from ai.latency_optimizer import (
        set_global_optimization_mode,
        LatencyOptimizationMode,
        get_latency_performance_report
    )
    # Set default optimization mode for production
    set_global_optimization_mode(LatencyOptimizationMode.FAST)
    print("[Main] ⚡ Latency optimization system loaded - Target: <5 second responses")
    LATENCY_OPTIMIZATION_AVAILABLE = True
except ImportError as e:
    print(f"[Main] ⚠️ Latency optimization not available: {e}")
    LATENCY_OPTIMIZATION_AVAILABLE = False

try:
    from ai.consciousness_tokenizer import tokenize_consciousness_for_llm
    from ai.llm_budget_monitor import get_budget_status
    from ai.belief_analyzer import get_active_belief_contradictions
    from ai.personality_state import get_personality_summary_for_user
    from ai.semantic_tagging import analyze_content_semantics
    print("[Main] 🧠 Individual consciousness modules loaded")
    CONSCIOUSNESS_MODULES_AVAILABLE = True
except ImportError as e:
    print(f"[Main] ⚠️ Individual consciousness modules not available: {e}")
    CONSCIOUSNESS_MODULES_AVAILABLE = False

# ✅ NEW: Import all self-awareness components as requested by @Daveydrz
try:
    from ai.memory_context_corrector import MemoryContextCorrector
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
    from ai.cognitive_debug_logger import cognitive_debug_logger
    
    # ✅ NEW: Import persistent cognitive modules
    from cognitive_modules.integration import cognitive_integrator
    print("[Main] 🧠 All self-awareness components loaded")
    print("[Main] 🚀 Persistent cognitive integrator loaded")
    print("[Main] 📊 Cognitive debug logger loaded")
    SELF_AWARENESS_COMPONENTS_AVAILABLE = True
except ImportError as e:
    print(f"[Main] ⚠️ Self-awareness components not available: {e}")
    # Fallback to old cognitive integration if available
    try:
        from ai.cognitive_integration import cognitive_integrator
        print("[Main] 🔄 Using fallback cognitive integrator")
        SELF_AWARENESS_COMPONENTS_AVAILABLE = True
    except ImportError as e2:
        print(f"[Main] ❌ No cognitive integrator available: {e2}")
        SELF_AWARENESS_COMPONENTS_AVAILABLE = False

# ✅ NEW: Import autonomous consciousness systems
try:
    from ai.autonomous_consciousness_integrator import autonomous_consciousness_integrator, AutonomousMode
    print("[Main] 🚀 Autonomous consciousness integrator loaded")
    print("[Main] 💭 Autonomous systems: Proactive thinking, Calendar monitoring, Self-motivation, Dream simulation")
    print("[Main] 🌍 Environmental awareness and Autonomous communication loaded")
    AUTONOMOUS_CONSCIOUSNESS_AVAILABLE = True
except ImportError as e:
    print(f"[Main] ⚠️ Autonomous consciousness systems not available: {e}")
    AUTONOMOUS_CONSCIOUSNESS_AVAILABLE = False

from voice.voice_manager_instance import voice_manager
from voice.manager_names import UltraIntelligentNameManager

voice_manager.ultra_name_manager = UltraIntelligentNameManager(voice_manager)
print("[Main] ✅ UltraIntelligentNameManager assigned to voice_manager")

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
    
    # ✅ FORCE CORRECT VOICE MANAGER IMPORT - Always use IntelligentVoiceManager
    try:
        from voice.manager import voice_manager as intelligent_voice_manager
        voice_manager = intelligent_voice_manager
        
        print("[AdvancedBuddy] ✅ Using IntelligentVoiceManager from manager.py")
        print(f"[AdvancedBuddy] 🔍 voice_manager type: {type(voice_manager)}")
        
        # Verify it has the correct method
        if hasattr(voice_manager, 'handle_voice_identification'):
            print("[AdvancedBuddy] ✅ handle_voice_identification method confirmed")
            ADVANCED_AI_AVAILABLE = True  # Your IntelligentVoiceManager IS advanced
        else:
            print("[AdvancedBuddy] ❌ handle_voice_identification method missing!")
        
        # Load voice training components
        from voice.training import voice_training_mode, check_voice_training_command
        print("[AdvancedBuddy] ✅ Voice training components loaded")
        
    except ImportError as manager_err:
        print(f"[AdvancedBuddy] ❌ IntelligentVoiceManager import failed: {manager_err}")
        
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
advanced_name_manager = None

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

from ai.chat import generate_response  # Keep for fallback
from ai.memory import add_to_conversation_history
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
    """🚀 IMMEDIATE RESPONSE: Proper memory integration + Fast response generation"""
    print(f"[IMMEDIATE] 🚀 Starting IMMEDIATE response for: '{text}' (user: {current_user})")
    
    start_time = time.time()
    
    try:
        # ✅ STEP 1: IMMEDIATE memory processing (fast local + background Gemma)
        print("[IMMEDIATE] 💾 Processing memory immediately...")
        
        # Fast local memory extraction for names/facts
        from ai.local_memory_manager import local_memory_manager
        
        # Check for name introduction first (critical for remembering names)
        name_detected = False
        extracted_name = None
        text_lower = text.lower().strip()
        
        # Name patterns - check immediately
        name_patterns = [
            r"my name is (\w+)",
            r"i'?m (\w+)",
            r"call me (\w+)",
            r"i'?m called (\w+)",
            r"this is (\w+)"
        ]
        
        for pattern in name_patterns:
            import re
            match = re.search(pattern, text_lower)
            if match:
                extracted_name = match.group(1).capitalize()
                name_detected = True
                print(f"[IMMEDIATE] 👤 NAME DETECTED: {extracted_name}")
                
                # Store name immediately as a fact
                from ai.local_memory_manager import MemoryEntry
                from datetime import datetime
                
                name_memory = MemoryEntry(
                    timestamp=datetime.now().isoformat(),
                    user_id=current_user,
                    text=f"User's name is {extracted_name}",
                    memory_type="fact",
                    extracted_info={
                        "fact_category": "identity",
                        "fact_value": extracted_name,
                        "name_introduction": True,
                        "confidence": 0.95,
                        "source": "immediate_extraction"
                    },
                    confidence=0.95
                )
                local_memory_manager.store_memories([name_memory])
                print(f"[IMMEDIATE] ✅ Name '{extracted_name}' stored immediately")
                break
        
        # ✅ STEP 2: Get current memory context for response (updated with new name if detected)
        print("[IMMEDIATE] 📋 Loading current memory context...")
        existing_context = local_memory_manager.get_user_context(current_user)
        
        # Build consciousness context with latest memory
        consciousness_context = f"""BUDDY'S CONSCIOUSNESS STATE:
Current Emotion: helpful
Motivation Level: 0.8
Active Goals: help user effectively, remember user information
Current Focus: user interaction
Personality: friendly, empathetic, good memory

USER MEMORY:
Facts: {', '.join(existing_context.get('facts', [])[:5])}
Preferences: {', '.join(existing_context.get('preferences', [])[:5])}
Recent Context: {', '.join(existing_context.get('context', [])[-3:])}"""

        if name_detected and extracted_name:
            consciousness_context += f"\nIMPORTANT: User just introduced themselves as {extracted_name}. Remember this name!"
        
        print("[IMMEDIATE] 📝 Memory context prepared for immediate response")
        
        # ✅ STEP 3: Start background consciousness processing (port 5002) - NON-BLOCKING
        def background_consciousness_processing():
            """Process full consciousness in background via port 5002"""
            try:
                from ai.extractor_client import process_full_consciousness
                print(f"[IMMEDIATE] 🧠 Background: Processing consciousness via port 5002...")
                
                # Process ALL consciousness via Gemma on port 5002
                consciousness_data = process_full_consciousness(text, current_user)
                
                # Update local memory with full consciousness data
                local_memory_manager.update_memory(current_user, text, consciousness_data)
                
                print(f"[IMMEDIATE] ✅ Background consciousness processing complete")
                
            except Exception as e:
                print(f"[IMMEDIATE] ⚠️ Background consciousness error (non-critical): {e}")
        
        # Start consciousness processing in background thread (don't wait)
        import threading
        threading.Thread(target=background_consciousness_processing, daemon=True).start()
        
        # ✅ STEP 4: Generate response immediately using port 5001 ONLY
        print("[IMMEDIATE] ⚡ Starting IMMEDIATE response generation (port 5001)...")
        
        try:
            from ai.simple_llm_handler import generate_response_with_consciousness
            print("[IMMEDIATE] 🎯 Using simple LLM handler for port 5001 ONLY")
            
            full_response = ""
            chunk_count = 0
            response_interrupted = False
            first_chunk = True
            
            # Import audio functions with better error handling
            audio_available = False
            try:
                from audio.output import speak_streaming
                audio_available = True
                print("[IMMEDIATE] 🎵 Audio system available - Kokoro ready")
            except ImportError as audio_err:
                print(f"[IMMEDIATE] ⚠️ Audio system not available: {audio_err}")
                audio_available = False
            
            # Generate response using ONLY port 5001 with consciousness injection
            response_chunks = []
            for chunk in generate_response_with_consciousness(text, current_user, consciousness_context):
                # Check for interrupt
                if full_duplex_manager and hasattr(full_duplex_manager, 'speech_interrupted') and full_duplex_manager.speech_interrupted:
                    print("[IMMEDIATE] ⚡ INTERRUPT DETECTED - STOPPING")
                    response_interrupted = True
                    break
                
                if chunk and chunk.strip():
                    chunk_text = chunk.strip()
                    chunk_count += 1
                    response_chunks.append(chunk_text)
                    
                    if first_chunk:
                        print("[IMMEDIATE] 🎵 First chunk ready - starting speech IMMEDIATELY!")
                        first_chunk = False
                    
                    print(f"[IMMEDIATE] 🗣️ Speaking chunk {chunk_count}: '{chunk_text[:50]}...'")
                    
                    # Start speaking immediately (fixed audio output)
                    if audio_available:
                        try:
                            success = speak_streaming(chunk_text)
                            if not success:
                                print(f"[IMMEDIATE] ⚠️ speak_streaming returned False - audio may not be playing")
                        except Exception as audio_err:
                            print(f"[IMMEDIATE] ❌ Audio error: {audio_err}")
                            print(f"[IMMEDIATE] 💬 Would speak: {chunk_text}")
                    else:
                        print(f"[IMMEDIATE] 💬 Would speak: {chunk_text}")
                    
                    full_response += chunk_text + " "
                    
                    # Check for interrupt after speaking
                    if full_duplex_manager and hasattr(full_duplex_manager, 'speech_interrupted') and full_duplex_manager.speech_interrupted:
                        print("[IMMEDIATE] ⚡ INTERRUPT AFTER SPEAKING")
                        response_interrupted = True
                        break
                    
                    # Brief pause for natural flow (minimal)
                    time.sleep(0.05)  # Slightly longer for stability
            
            total_time = time.time() - start_time
            
            if not response_interrupted and full_response.strip():
                # Add to conversation history IMMEDIATELY
                local_memory_manager.add_interaction(current_user, text, full_response.strip())
                
                print(f"[IMMEDIATE] ✅ IMMEDIATE response complete:")
                print(f"[IMMEDIATE] ⚡ Total time: {total_time:.3f}s (TARGET: <3s)")
                print(f"[IMMEDIATE] 📊 Chunks processed: {chunk_count}")
                print(f"[IMMEDIATE] 🧠 Background consciousness processing for enhanced memory")
                print(f"[IMMEDIATE] 💾 Interaction stored immediately")
                
            return
            
        except ImportError as e:
            print(f"[IMMEDIATE] ❌ Simple LLM handler not available: {e}")
            
        # ✅ FALLBACK: Direct HTTP call to port 5001 if simple handler fails
        print("[IMMEDIATE] 🔄 Using direct HTTP fallback to port 5001...")
        
        try:
            import requests
            
            # Build minimal prompt
            prompt = f"""Buddy is a helpful, empathetic AI assistant with excellent memory.

{consciousness_context}

User: {text}

Buddy:"""
            
            # Different payload formats to try
            payload_formats = [
                # Format 1: Messages format
                {
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 500,
                    "temperature": 0.7,
                    "stream": True
                },
                # Format 2: Simple prompt format  
                {
                    "prompt": prompt,
                    "max_length": 500,
                    "temperature": 0.7,
                    "stream": True
                },
                # Format 3: Text-generation-webui format
                {
                    "text": prompt,
                    "max_new_tokens": 500,
                    "temperature": 0.7,
                    "stream": True
                }
            ]
            
            urls_to_try = [
                "http://localhost:5001/api/v1/generate",
                "http://localhost:5001/v1/chat/completions", 
                "http://localhost:5001/api/v1/stream",
                "http://localhost:5001/generate"
            ]
            
            response_generated = False
            
            for url in urls_to_try:
                if response_generated:
                    break
                    
                for payload in payload_formats:
                    try:
                        print(f"[IMMEDIATE] 🎯 Trying {url} with payload type: {list(payload.keys())}")
                        
                        response = requests.post(url, json=payload, stream=True, timeout=10)
                        
                        if response.status_code == 200:
                            print(f"[IMMEDIATE] ✅ Connected to {url}")
                            
                            full_response = ""
                            chunk_count = 0
                            
                            # Process streaming response
                            for line in response.iter_lines():
                                if line:
                                    try:
                                        # Try different parsing methods
                                        line_text = line.decode('utf-8')
                                        
                                        # SSE format
                                        if line_text.startswith('data: '):
                                            json_str = line_text[6:]
                                            if json_str.strip() == '[DONE]':
                                                break
                                            
                                            try:
                                                chunk_data = json.loads(json_str)
                                                # Try different response formats
                                                text_chunk = (
                                                    chunk_data.get('choices', [{}])[0].get('delta', {}).get('content', '') or
                                                    chunk_data.get('choices', [{}])[0].get('text', '') or
                                                    chunk_data.get('results', [{}])[0].get('text', '') or
                                                    chunk_data.get('text', '')
                                                )
                                                
                                                if text_chunk:
                                                    chunk_count += 1
                                                    full_response += text_chunk
                                                    
                                                    if chunk_count == 1:
                                                        print("[IMMEDIATE] 🎵 First chunk from direct call - speaking immediately!")
                                                    
                                                    print(f"[IMMEDIATE] 🗣️ Direct chunk {chunk_count}: '{text_chunk[:50]}...'")
                                                    
                                                    if audio_available:
                                                        try:
                                                            speak_streaming(text_chunk)
                                                        except Exception as audio_err:
                                                            print(f"[IMMEDIATE] ❌ Audio error: {audio_err}")
                                                            print(f"[IMMEDIATE] 💬 Would speak: {text_chunk}")
                                                    else:
                                                        print(f"[IMMEDIATE] 💬 Would speak: {text_chunk}")
                                                    
                                            except json.JSONDecodeError:
                                                # Raw text chunk
                                                if json_str and not json_str.startswith('['):
                                                    chunk_count += 1
                                                    full_response += json_str + " "
                                                    
                                                    if audio_available:
                                                        try:
                                                            speak_streaming(json_str)
                                                        except Exception as audio_err:
                                                            print(f"[IMMEDIATE] ❌ Audio error: {audio_err}")
                                                            print(f"[IMMEDIATE] 💬 Would speak: {json_str}")
                                                    else:
                                                        print(f"[IMMEDIATE] 💬 Would speak: {json_str}")
                                        
                                        # Raw line format
                                        elif line_text and not line_text.startswith('[') and len(line_text) > 1:
                                            chunk_count += 1
                                            full_response += line_text + " "
                                            
                                            if audio_available:
                                                try:
                                                    speak_streaming(line_text)
                                                except Exception as audio_err:
                                                    print(f"[IMMEDIATE] ❌ Audio error: {audio_err}")
                                                    print(f"[IMMEDIATE] 💬 Would speak: {line_text}")
                                            else:
                                                print(f"[IMMEDIATE] 💬 Would speak: {line_text}")
                                        
                                    except Exception as parse_error:
                                        print(f"[IMMEDIATE] ⚠️ Parse error: {parse_error} - line: {line}")
                            
                            if full_response.strip():
                                # Success! Add to conversation history
                                local_memory_manager.add_interaction(current_user, text, full_response.strip())
                                
                                total_time = time.time() - start_time
                                print(f"[IMMEDIATE] ✅ Direct response complete:")
                                print(f"[IMMEDIATE] ⚡ Total time: {total_time:.3f}s")
                                print(f"[IMMEDIATE] 📊 Chunks: {chunk_count}")
                                print(f"[IMMEDIATE] 💾 Interaction stored")
                                
                                response_generated = True
                                break
                        
                    except Exception as e:
                        print(f"[IMMEDIATE] ⚠️ Failed {url}: {e}")
                        continue
            
            if response_generated:
                return
            else:
                print("[IMMEDIATE] ❌ All direct HTTP attempts failed")
        
        except Exception as e:
            print(f"[IMMEDIATE] ❌ Direct HTTP fallback error: {e}")
        
        # ✅ FINAL FALLBACK: Use existing chat system if everything else fails
        print("[IMMEDIATE] 🔄 Using existing chat system as final fallback...")
        
        try:
            from ai.chat import generate_response
            response = generate_response(text, current_user)
            
            if response and response.strip():
                print(f"[IMMEDIATE] 🗣️ Fallback response: {response[:100]}...")
                
                if audio_available:
                    try:
                        speak_streaming(response)
                    except Exception as audio_err:
                        print(f"[IMMEDIATE] ❌ Audio error: {audio_err}")
                        print(f"[IMMEDIATE] 💬 Would speak: {response}")
                else:
                    print(f"[IMMEDIATE] 💬 Would speak: {response}")
                
                # Add to conversation history
                local_memory_manager.add_interaction(current_user, text, response.strip())
                
                total_time = time.time() - start_time
                print(f"[IMMEDIATE] ✅ Fallback response complete in {total_time:.3f}s")
                
                return
            
        except Exception as e:
            print(f"[IMMEDIATE] ❌ Fallback chat system error: {e}")
        
        # If we get here, something is seriously wrong
        print("[IMMEDIATE] 🚨 CRITICAL: All response generation methods failed!")
        emergency_response = "I apologize, but I'm having technical difficulties. Please try again."
        
        if audio_available:
            try:
                speak_streaming(emergency_response)
            except Exception as audio_err:
                print(f"[IMMEDIATE] ❌ Emergency audio error: {audio_err}")
                print(f"[IMMEDIATE] 💬 Emergency response: {emergency_response}")
        else:
            print(f"[IMMEDIATE] 💬 Emergency response: {emergency_response}")
        
        return
        
    except Exception as e:
        print(f"[IMMEDIATE] ❌ Critical error in immediate response: {e}")
        
        # Emergency fallback
        emergency_response = f"I apologize, but I encountered an error. Let me try to help you with: {text}"
        try:
            from audio.output import speak_streaming
            speak_streaming(emergency_response)
        except:
            print(f"[IMMEDIATE] 💬 Emergency: {emergency_response}")
        
        # Try to add to history even in error case
        try:
            local_memory_manager.add_interaction(current_user, text, emergency_response)
        except:
            pass
        
        return

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
    """Handle 'what's my name' using voice matching, not system login"""
    try:
        # Handle system user
        if identified_user == "Daveydrz" or identified_user == SYSTEM_USER:
            return f"Based on your voice, you are Daveydrz."
        
        # Handle known voice profiles
        elif identified_user in known_users and identified_user not in ["Anonymous_Speaker", "Unknown", "Guest"]:
            return f"Your name is {display_name}."
        
        # Handle anonymous or unrecognized voices
        elif identified_user in ["Anonymous_Speaker", "Unknown", "Guest"]:
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
    """✅ ADVANCED: Extract name with enhanced AI processing"""
    if ADVANCED_AI_AVAILABLE:
        try:
            # Use advanced name manager
            return advanced_name_manager.extract_name_ultra_smart(text, {})
        except:
            pass
    
    # Fallback to enhanced extraction
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
                if ADVANCED_AI_AVAILABLE:
                    # Use advanced name validation
                    try:
                        if advanced_name_manager.is_valid_name_enhanced(name):
                            return name
                    except:
                        pass
                elif ENHANCED_VOICE_AVAILABLE:
                    # Use enhanced name validation
                    try:
                        from voice.manager_names import name_manager
                        if name_manager.is_valid_name_enhanced(name):
                            return name
                    except:
                        pass
                
                # Fallback validation
                if hasattr(voice_manager, 'is_valid_name') and voice_manager.is_valid_name(name):
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
                
                # ✅ STEP 1: Process user identification from text FIRST
                try:
                    from ai.speech import identify_user, get_display_name
                    
                    # Check if user is introducing themselves (always process this)
                    identify_user(text, current_user)
                    
                    # Get current display name
                    display_name = get_display_name(current_user)
                    print(f"[FullDuplex] 👤 Text User: {current_user} (display: {display_name})")
                    
                except Exception as id_error:
                    print(f"[FullDuplex] ⚠️ User identification error: {id_error}")
                
                # ✅ STEP 2: VOICE RECOGNITION PROCESSING (CRITICAL!)
                if ADVANCED_AI_AVAILABLE:
                    # Use advanced voice manager
                    try:
                        identified_user, status = voice_manager.handle_voice_identification(audio_data, text)
                        
                        print(f"[AdvancedAI] 🔍 Status: '{status}', User: '{identified_user}'")
                        print(f"[AdvancedAI] 🛡️ LLM locked: {voice_manager.is_llm_locked() if hasattr(voice_manager, 'is_llm_locked') else False}")
                        
                        # ✅ CRITICAL DATABASE SYNC FIX (NON-DESTRUCTIVE)
                        try:
                            print("[AdvancedAI] 🔄 Syncing voice manager to database...")
                            from voice.database import known_users, anonymous_clusters, save_known_users
                            from datetime import datetime
                            
                            # Get voice manager stats to check internal state
                            if hasattr(voice_manager, 'get_session_stats'):
                                stats = voice_manager.get_session_stats()
                                print(f"[AdvancedAI] 📊 Internal stats: {stats}")
                                
                                # Check if voice manager has anonymous clusters
                                if stats.get('anonymous_clusters', 0) > 0:
                                    # 🔥 CRITICAL: Only sync if the cluster DOESN'T EXIST or has NO EMBEDDINGS
                                    if identified_user and identified_user.startswith('Anonymous_'):
                                        
                                        # Check if cluster already exists with embeddings
                                        existing_cluster = anonymous_clusters.get(identified_user)
                                        existing_embeddings = existing_cluster.get('embeddings', []) if existing_cluster else []
                                        
                                        if not existing_cluster:
                                            # ✅ NEW CLUSTER: Only create if it doesn't exist
                                            print(f"[AdvancedAI] 🆕 Creating new database entry for {identified_user}")
                                            
                                            anonymous_clusters[identified_user] = {
                                                'cluster_id': identified_user,
                                                'embeddings': [],  # Start empty, embeddings will be added by voice manager
                                                'created_at': datetime.utcnow().isoformat(),
                                                'last_updated': datetime.utcnow().isoformat(),
                                                'status': 'anonymous',
                                                'sample_count': 1,
                                                'quality_scores': [0.8],
                                                'audio_contexts': ['voice_manager_sync'],
                                                'confidence_threshold': 0.6
                                            }
                                            
                                            known_users[identified_user] = {
                                                'username': identified_user,
                                                'status': 'anonymous',
                                                'voice_embeddings': [],  # Start empty, embeddings will be added by voice manager
                                                'created_at': datetime.utcnow().isoformat(),
                                                'last_updated': datetime.utcnow().isoformat(),
                                                'is_anonymous': True,
                                                'cluster_id': identified_user,
                                                'training_type': 'advanced_ai_sync',
                                                'confidence_threshold': 0.6,
                                                'recognition_count': 1,
                                                'recognition_successes': 1,
                                                'recognition_failures': 0,
                                                'embedding_count': 0  # Will be updated when embeddings are added
                                            }
                                            
                                        elif len(existing_embeddings) == 0:
                                            # ✅ EMPTY CLUSTER: Update metadata only, don't touch embeddings
                                            print(f"[AdvancedAI] 🔄 Updating metadata for existing empty cluster {identified_user}")
                                            
                                            if existing_cluster:
                                                existing_cluster['last_updated'] = datetime.utcnow().isoformat()
                                                existing_cluster['recognition_count'] = existing_cluster.get('recognition_count', 0) + 1
                                            
                                            if identified_user in known_users:
                                                known_users[identified_user]['last_updated'] = datetime.utcnow().isoformat()
                                                known_users[identified_user]['recognition_count'] = known_users[identified_user].get('recognition_count', 0) + 1
                                                
                                        else:
                                            # ✅ CLUSTER WITH EMBEDDINGS: DON'T TOUCH IT!
                                            print(f"[AdvancedAI] 🛡️ PRESERVING existing cluster {identified_user} with {len(existing_embeddings)} embeddings")
                                            # Just update timestamp
                                            existing_cluster['last_updated'] = datetime.utcnow().isoformat()
                                            if identified_user in known_users:
                                                known_users[identified_user]['last_updated'] = datetime.utcnow().isoformat()
                                        
                                        # Save only if we made changes and no embeddings exist
                                        if not existing_cluster or len(existing_embeddings) == 0:
                                            if save_known_users():
                                                print(f"[AdvancedAI] ✅ Successfully synced {identified_user} to database")
                                            else:
                                                print(f"[AdvancedAI] ❌ Failed to sync {identified_user} to database")
                            
                        except Exception as sync_error:
                            print(f"[AdvancedAI] ⚠️ Database sync error: {sync_error}")
                        
                        # Handle LLM locking/unlocking
                        if hasattr(voice_manager, 'is_llm_locked'):
                            if voice_manager.is_llm_locked():
                                if not llm_locked:
                                    pending_question = text
                                    llm_locked = True
                                    print(f"[AdvancedAI] 🛡️ LLM LOCKED - Question queued: '{text}'")
                                continue
                            else:
                                if llm_locked:
                                    llm_locked = False
                                    print(f"[AdvancedAI] 🔓 LLM UNLOCKED")
                                    
                                    # Update current user
                                    if identified_user and identified_user != current_user:
                                        current_user = identified_user
                                        print(f"[AdvancedAI] 🔄 User updated to: {current_user}")
                                    
                                    # Process pending question
                                    if pending_question:
                                        print(f"[AdvancedAI] ✅ Processing queued question: '{pending_question}'")
                                        handle_streaming_response(pending_question, current_user)
                                        pending_question = None
                                        continue
                        
                        # Update current user
                        if identified_user and identified_user != current_user:
                            current_user = identified_user
                            print(f"[AdvancedAI] 🔄 User switched to: {current_user}")
                        
                    except Exception as e:
                        print(f"[AdvancedAI] ❌ Advanced voice processing error: {e}")
                        import traceback
                        traceback.print_exc()
                        # Fallback to basic processing
                        voice_recognition_in_progress = False
                
                elif ENHANCED_VOICE_AVAILABLE:
                    # Enhanced voice processing
                    try:
                        identified_user, status = voice_manager.handle_voice_identification(audio_data, text)
                        
                        print(f"[Enhanced] 🔍 Status: '{status}', User: '{identified_user}'")
                        
                        # Handle voice processing states
                        if status in ["NEEDS_NAME", "WAITING_FOR_NAME", "CONFIRMING_NAME", "NEEDS_TRAINING", "UNRECOGNIZED"]:
                            if not voice_recognition_in_progress:
                                pending_question = text
                                voice_recognition_in_progress = True
                                print(f"[Enhanced] 📝 Stored pending question: '{text}'")
                            continue
                        
                        if status in ["RECOGNIZED", "LIKELY", "CONFIRMED", "GUEST_CREATED", "NAME_CONFIRMED"]:
                            if identified_user and identified_user != current_user:
                                current_user = identified_user
                                print(f"[Enhanced] 🔄 Switched to: {current_user}")
                            
                            voice_recognition_in_progress = False
                            
                            # Add passive sample if available
                            if ENHANCED_VOICE_AVAILABLE and current_user != "Guest":
                                try:
                                    enhanced_speaker_profiles.add_passive_sample(current_user, audio_data, 0.9)
                                    enhanced_speaker_profiles.tune_threshold_for_user(current_user)
                                except:
                                    pass
                            
                            # Process pending question
                            if pending_question:
                                print(f"[Enhanced] ✅ Processing pending: '{pending_question}'")
                                time.sleep(1)
                                handle_streaming_response(pending_question, current_user)
                                pending_question = None
                            continue
                        
                    except Exception as e:
                        print(f"[Enhanced] ❌ Enhanced voice processing error: {e}")
                        import traceback
                        traceback.print_exc()
                        voice_recognition_in_progress = False
                
                else:
                    # ✅ BASIC VOICE RECOGNITION - ACTUALLY PROCESS VOICE! (FIXED!)
                    print(f"[FullDuplex] 🔄 Using basic voice system with ACTUAL voice recognition")
                    
                    try:
                        # ✅ CRITICAL: Process voice recognition to create Anonymous_001
                        from voice.recognition import identify_speaker_with_confidence
                        identified_user, confidence = identify_speaker_with_confidence(audio_data)
                        
                        print(f"[BasicVoice] 🔍 Voice recognition result: '{identified_user}' (confidence: {confidence:.3f})")
                        
                        # Handle voice recognition results
                        if identified_user != "UNKNOWN" and identified_user != "Unknown":
                            # Known user or anonymous cluster was created/matched
                            if confidence > 0.7 or identified_user.startswith("Anonymous_"):
                                if identified_user != current_user:
                                    current_user = identified_user
                                    print(f"[BasicVoice] 🔄 User switched to: {current_user}")
                                    
                                    # ✅ Update voice identity context
                                    try:
                                        update_voice_identity_context(current_user)
                                    except:
                                        pass
                                        
                        else:
                            # Unknown user - check if anonymous cluster was created
                            print(f"[BasicVoice] 👤 Unknown user result - checking for new anonymous clusters")
                            
                            from voice.database import anonymous_clusters, known_users
                            print(f"[BasicVoice] 📊 Current anonymous clusters: {list(anonymous_clusters.keys())}")
                            print(f"[BasicVoice] 📊 Current known users: {list(known_users.keys())}")
                            
                            # Check if a new anonymous cluster was created
                            if anonymous_clusters:
                                # Get the latest anonymous cluster
                                anonymous_ids = [k for k in anonymous_clusters.keys() if k.startswith("Anonymous_")]
                                if anonymous_ids:
                                    latest_cluster = max(anonymous_ids)
                                    current_user = latest_cluster
                                    print(f"[BasicVoice] 🆕 Using anonymous cluster: {current_user}")
                                    
                                    # ✅ Update voice identity context
                                    try:
                                        update_voice_identity_context(current_user)
                                    except:
                                        pass
                        
                        # ✅ VERIFY: Check if user was saved to database
                        from voice.database import known_users, anonymous_clusters
                        total_entities = len(known_users) + len(anonymous_clusters)
                        print(f"[BasicVoice] 📊 Total voice entities after processing: {total_entities}")
                        print(f"[BasicVoice] 📊 Current user: {current_user}")
                        
                    except Exception as basic_voice_error:
                        print(f"[BasicVoice] ❌ Basic voice recognition error: {basic_voice_error}")
                        import traceback
                        traceback.print_exc()
                        
                        # ✅ EMERGENCY: Force create anonymous cluster
                        try:
                            print(f"[BasicVoice] 🚨 Emergency: Forcing anonymous cluster creation...")
                            from voice.database import create_anonymous_cluster
                            from voice.voice_models import dual_voice_model_manager
                            
                            embedding = dual_voice_model_manager.generate_dual_embedding(audio_data)
                            if embedding:
                                cluster_id = create_anonymous_cluster(embedding)
                                if cluster_id:
                                    current_user = cluster_id
                                    print(f"[BasicVoice] ✅ Emergency cluster created: {current_user}")
                                    
                                    # Update voice identity context
                                    try:
                                        update_voice_identity_context(current_user)
                                    except:
                                        pass
                                else:
                                    print(f"[BasicVoice] ❌ Emergency cluster creation failed")
                            else:
                                print(f"[BasicVoice] ❌ Emergency embedding generation failed")
                                
                        except Exception as emergency_error:
                            print(f"[BasicVoice] ❌ Emergency creation failed: {emergency_error}")
                            # Last resort - just continue with existing user
                            print(f"[BasicVoice] 🆘 Continuing with existing user: {current_user}")
                
                # ✅ CRITICAL: Manual sync check for Advanced AI (NON-DESTRUCTIVE)
                if ADVANCED_AI_AVAILABLE:
                    try:
                        # Check if voice manager internal state differs from database
                        stats = voice_manager.get_session_stats() if hasattr(voice_manager, 'get_session_stats') else {}
                        internal_clusters = stats.get('anonymous_clusters', 0)
                        
                        from voice.database import anonymous_clusters, known_users
                        db_clusters = len(anonymous_clusters)
                        db_users = len(known_users)
                        
                        if internal_clusters > 0 and db_clusters == 0 and db_users == 0:
                            print(f"[FullDuplex] 🚨 CRITICAL: Voice manager has {internal_clusters} clusters but database is empty!")
                            print(f"[FullDuplex] 🔧 Performing emergency database sync...")
                            
                            # ✅ EMERGENCY SYNC: Create placeholder only, don't overwrite existing data
                            from datetime import datetime
                            cluster_id = "Anonymous_001"
                            
                            # Only create if it doesn't exist
                            if cluster_id not in anonymous_clusters:
                                anonymous_clusters[cluster_id] = {
                                    'cluster_id': cluster_id,
                                    'embeddings': [],  # Start empty, voice manager will populate
                                    'created_at': datetime.utcnow().isoformat(),
                                    'last_updated': datetime.utcnow().isoformat(),
                                    'status': 'anonymous',
                                    'sample_count': 0,  # Will be updated when embeddings are added
                                    'quality_scores': [],
                                    'audio_contexts': ['emergency_sync_placeholder'],
                                    'confidence_threshold': 0.6
                                }
                            
                            # Only create if it doesn't exist
                            if cluster_id not in known_users:
                                known_users[cluster_id] = {
                                    'username': cluster_id,
                                    'status': 'anonymous',
                                    'voice_embeddings': [],  # Start empty, voice manager will populate
                                    'created_at': datetime.utcnow().isoformat(),
                                    'last_updated': datetime.utcnow().isoformat(),
                                    'is_anonymous': True,
                                    'cluster_id': cluster_id,
                                    'training_type': 'emergency_sync_placeholder',
                                    'confidence_threshold': 0.6,
                                    'recognition_count': 0,
                                    'embedding_count': 0  # Will be updated when embeddings are added
                                }
                            
                            # Save placeholders
                            from voice.database import save_known_users
                            if save_known_users():
                                print(f"[FullDuplex] ✅ Emergency sync placeholder created!")
                                current_user = cluster_id
                            else:
                                print(f"[FullDuplex] ❌ Emergency sync failed!")
                                
                    except Exception as emergency_sync_error:
                        print(f"[FullDuplex] ❌ Emergency sync error: {emergency_sync_error}")
                
                # ✅ Handle training commands
                if "train" in text.lower() and ("voice" in text.lower() or "my" in text.lower()):
                    print(f"[FullDuplex] 🎓 Training command detected: '{text}'")
                    
                    # Clear any pending states
                    voice_recognition_in_progress = False
                    llm_locked = False
                    pending_question = None
                    
                    if ADVANCED_AI_AVAILABLE:
                        print("[FullDuplex] 🎓 ADVANCED AI voice training requested")
                        full_duplex_manager.stop()
                        
                        speak_streaming("Starting advanced AI voice training with clustering optimization and quality validation.")
                        time.sleep(2)
                        
                        success = voice_training_mode()
                        if success:
                            load_voice_profiles()
                            current_user = "Daveydrz"
                            speak_streaming("Advanced AI voice training complete! I now have multiple voice embeddings with clustering support for superior recognition.")
                        else:
                            speak_streaming("Training failed.")
                        
                        time.sleep(2)
                        full_duplex_manager.start()
                        continue
                    elif ENHANCED_VOICE_AVAILABLE:
                        print("[FullDuplex] 🎓 Enhanced voice training requested")
                        full_duplex_manager.stop()
                        
                        speak_streaming("Starting enhanced voice training with quality validation and multiple embeddings.")
                        time.sleep(2)
                        
                        success = voice_training_mode()
                        if success:
                            load_voice_profiles()
                            current_user = "Daveydrz"
                            speak_streaming("Enhanced voice training complete! I now have multiple voice embeddings for better recognition.")
                        else:
                            speak_streaming("Training failed.")
                        
                        time.sleep(2)
                        full_duplex_manager.start()
                        continue
                    else:
                        print("[FullDuplex] 🎓 Legacy voice training requested")
                        full_duplex_manager.stop()
                        
                        speak_streaming("Starting voice training.")
                        time.sleep(2)
                        
                        success = voice_training_mode()
                        if success:
                            load_voice_profiles()
                            current_user = "Daveydrz"
                            speak_streaming("Voice training complete!")
                        else:
                            speak_streaming("Training failed.")
                        
                        time.sleep(2)
                        full_duplex_manager.start()
                        continue
                
                # Check for conversation end
                if should_end_conversation(text):
                    try:
                        from ai.speech import get_display_name
                        display_name = get_display_name(current_user)
                        speak_streaming(f"Goodbye {display_name}! See you later from Birtinya!")
                    except:
                        speak_streaming("Goodbye from Birtinya!")
                    set_conversation_state(False)
                    break
                
                # ✅ FINAL CHECK: Block LLM if any voice states are active
                if voice_recognition_in_progress or llm_locked:
                    print(f"[FullDuplex] 🛡️ Voice processing active - LLM blocked for: '{text}'")
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
                
                # ✅ Show current user identity status
                try:
                    from ai.speech import get_display_name
                    display_name = get_display_name(current_user)
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
    
    # ✅ PERFORMANCE: Initialize async consciousness processor for background processing
    print("[AdvancedBuddy] ⚡ Initializing async consciousness processor for performance...")
    try:
        from ai.async_consciousness_processor import async_consciousness_processor
        async_consciousness_processor.start()
        print("[AdvancedBuddy] ✅ Async consciousness processor started - background processing enabled")
    except Exception as async_error:
        print(f"[AdvancedBuddy] ⚠️ Async consciousness processor initialization error: {async_error}")
        print("[AdvancedBuddy] ⚠️ Performance mode may not work optimally")
    
    # ✅ OPTIMIZED: Initialize new optimized background consciousness processor
    print("[AdvancedBuddy] 🚀 Initializing optimized background consciousness processor...")
    try:
        from ai.background_consciousness_processor_optimized import background_consciousness_processor
        background_consciousness_processor.start()
        print("[AdvancedBuddy] ✅ Optimized background consciousness processor started")
        print(f"[AdvancedBuddy] 🧠 Inner thoughts: {'ENABLED' if ENABLE_INNER_THOUGHTS else 'DISABLED'}")
        print(f"[AdvancedBuddy] 🔄 Self reflection: {'ENABLED' if ENABLE_SELF_REFLECTION else 'DISABLED'}")
        print(f"[AdvancedBuddy] ⚡ Single LLM call mode: {'ENABLED' if SINGLE_LLM_CALL_MODE else 'DISABLED'}")
    except Exception as optimized_bg_error:
        print(f"[AdvancedBuddy] ⚠️ Optimized background processor initialization error: {optimized_bg_error}")
        print("[AdvancedBuddy] ⚠️ Will use existing background processing")
    
    # ✅ EMERGENCY: Initialize background consciousness processor for fast responses
    print("[AdvancedBuddy] 🚨 Initializing emergency background consciousness processor...")
    try:
        from ai.background_consciousness_processor import get_background_processor
        background_processor = get_background_processor()
        background_processor.start()
        print("[AdvancedBuddy] ✅ Background consciousness processor started - fast responses enabled")
    except Exception as bg_error:
        print(f"[AdvancedBuddy] ⚠️ Background processor initialization error: {bg_error}")
        print("[AdvancedBuddy] ⚠️ Fast response mode may not work optimally")
    
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
    
    # ✅ NEW: Initialize and start consciousness architecture
    if CONSCIOUSNESS_ARCHITECTURE_AVAILABLE:
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
                        from ai.memory import get_user_memory
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
                
                # ✅ CONSCIOUSNESS: Shutdown consciousness systems
                if CONSCIOUSNESS_ARCHITECTURE_AVAILABLE:
                    try:
                        print("[AdvancedBuddy] 🧠 Shutting down consciousness architecture...")
                        
                        # Stop new autonomous components
                        free_thought_engine.stop()
                        print("[AdvancedBuddy] 💭 Free thought engine stopped")
                        
                        # Stop core consciousness systems
                        entropy_system.stop()
                        subjective_experience.stop()
                        temporal_awareness.stop()
                        inner_monologue.stop()
                        motivation_system.stop()
                        emotion_engine.stop()
                        self_model.stop()
                        global_workspace.stop()
                        print("[AdvancedBuddy] ✅ Consciousness architecture shutdown complete")
                    except Exception as e:
                        print(f"[AdvancedBuddy] ⚠️ Consciousness shutdown error: {e}")
                
                # ✅ NEW: Shutdown autonomous consciousness systems
                if AUTONOMOUS_CONSCIOUSNESS_AVAILABLE:
                    try:
                        print("[AdvancedBuddy] 🚀 Shutting down autonomous consciousness systems...")
                        autonomous_consciousness_integrator.stop_autonomous_system()
                        print("[AdvancedBuddy] ✅ Autonomous consciousness systems shutdown complete")
                    except Exception as e:
                        print(f"[AdvancedBuddy] ⚠️ Autonomous shutdown error: {e}")
                
                # ✅ OPTIMIZED: Shutdown optimized background consciousness processor
                try:
                    print("[AdvancedBuddy] 🚀 Shutting down optimized background consciousness processor...")
                    from ai.background_consciousness_processor_optimized import background_consciousness_processor
                    background_consciousness_processor.stop()
                    print("[AdvancedBuddy] ✅ Optimized background processor shutdown complete")
                except Exception as e:
                    print(f"[AdvancedBuddy] ⚠️ Optimized background processor shutdown error: {e}")
    
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
                