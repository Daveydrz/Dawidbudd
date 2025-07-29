"""
Emotion Mood - Consolidated emotion and mood management system
Created: 2025-01-29
Purpose: Unified emotion processing combining emotion.py, emotion_classifier.py, emotion_response_modulator.py, and mood_manager.py

This module consolidates:
- Traditional emotion engine with mood/arousal state management
- ONNX-based emotion classification 
- Emotion response modulation (tone, pace, structure adjustments)
- Dynamic mood evolution and influence system
- Per-user mood persistence and tracking
"""

import json
import os
import time
import threading
import random
import logging
import math
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path

# Optional imports
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    logging.warning("[EmotionMood] NumPy not available - using fallback calculations")

# Optional ONNX runtime import
try:
    import onnxruntime as ort
    from transformers import AutoTokenizer
    ONNX_AVAILABLE = True
except ImportError:
    ONNX_AVAILABLE = False
    logging.warning("[EmotionMood] ONNX runtime not available - using fallback classification")

# Optional entropy engine import
try:
    from ai.entropy import get_entropy_engine, EntropyLevel, inject_consciousness_entropy
    ENTROPY_AVAILABLE = True
except ImportError:
    ENTROPY_AVAILABLE = False
    def get_entropy_engine():
        return None
    def inject_consciousness_entropy(context, value):
        return value

# ============================================================================
# CONSOLIDATED ENUMS AND DATA STRUCTURES
# ============================================================================

class EmotionType(Enum):
    """Basic emotion types"""
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    ANTICIPATION = "anticipation"
    TRUST = "trust"
    CURIOSITY = "curiosity"
    CONTENTMENT = "contentment"

class MoodState(Enum):
    """Primary mood states"""
    JOYFUL = "joyful"
    CONTENT = "content"
    CALM = "calm"
    NEUTRAL = "neutral"
    MELANCHOLY = "melancholy"
    ANXIOUS = "anxious"
    FRUSTRATED = "frustrated"
    EXCITED = "excited"
    CONTEMPLATIVE = "contemplative"
    EMPATHETIC = "empathetic"
    CURIOUS = "curious"
    PLAYFUL = "playful"

class EmotionalTone(Enum):
    """Emotional tones for response modulation"""
    WARM = "warm"
    COOL = "cool"
    EXCITED = "excited"
    CALM = "calm"
    SERIOUS = "serious"
    PLAYFUL = "playful"
    EMPATHETIC = "empathetic"
    CONFIDENT = "confident"
    UNCERTAIN = "uncertain"
    CONTEMPLATIVE = "contemplative"

class ResponsePace(Enum):
    """Response pacing options"""
    SLOW = "slow"
    NORMAL = "normal"
    FAST = "fast"
    VARIABLE = "variable"

class ResponseStructure(Enum):
    """Response structure options"""
    BRIEF = "brief"
    DETAILED = "detailed"
    CONVERSATIONAL = "conversational"
    ANALYTICAL = "analytical"
    NARRATIVE = "narrative"

class MoodIntensity(Enum):
    """Intensity levels for moods"""
    SUBTLE = 0.2
    MILD = 0.4
    MODERATE = 0.6
    STRONG = 0.8
    INTENSE = 1.0

class MoodTrigger(Enum):
    """Events that can trigger mood changes"""
    USER_INTERACTION = "user_interaction"
    POSITIVE_FEEDBACK = "positive_feedback"
    NEGATIVE_FEEDBACK = "negative_feedback"
    PROLONGED_SILENCE = "prolonged_silence"
    ENVIRONMENTAL_CHANGE = "environmental_change"

@dataclass
class EmotionResult:
    """Emotion classification result with confidence and intensity"""
    emotion: str
    confidence: float
    intensity: str  # low, medium, high
    raw_logits: List[float] = field(default_factory=list)
    inference_time_ms: float = 0.0

@dataclass
class EmotionalModulation:
    """Emotional modulation settings"""
    tone: EmotionalTone
    pace: ResponsePace
    structure: ResponseStructure
    intensity: float  # 0.0 to 1.0
    confidence: float
    reasoning: str
    timestamp: str

@dataclass
class EmotionState:
    """Current emotion state"""
    primary_emotion: str = "neutral"
    intensity: float = 0.5
    arousal: float = 0.5  # energy level
    valence: float = 0.5  # positive/negative
    stability: float = 0.8  # how stable the emotion is
    last_update: datetime = field(default_factory=datetime.now)

@dataclass
class MoodProfile:
    """Comprehensive mood profile for a user"""
    current_mood: MoodState = MoodState.NEUTRAL
    intensity: float = 0.5
    stability: float = 0.8
    mood_history: List[Dict] = field(default_factory=list)
    interaction_count: int = 0
    last_interaction: Optional[datetime] = None
    personality_traits: List[str] = field(default_factory=lambda: ["empathetic", "helpful"])

# ============================================================================
# ONNX-BASED EMOTION CLASSIFIER
# ============================================================================

class EmotionClassifier:
    """ONNX-based neural emotion classifier"""
    
    def __init__(self):
        """Initialize ONNX emotion classifier"""
        self.model_loaded = False
        self.tokenizer = None
        self.session = None
        self.inference_count = 0
        self.total_inference_time = 0.0
        
        if ONNX_AVAILABLE:
            self._load_model()
    
    def _load_model(self):
        """Load ONNX model and tokenizer"""
        try:
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-multilingual-cased")
            
            # Load ONNX model
            self.session = ort.InferenceSession("emotion_classifier.onnx", providers=["CPUExecutionProvider"])
            
            self.model_loaded = True
            logging.info("[EmotionClassifier] 🧠 ONNX emotion classifier loaded successfully")
            
        except Exception as e:
            logging.warning(f"[EmotionClassifier] ⚠️ Model loading failed: {e}")
            self.model_loaded = False
    
    def classify_emotion(self, text: str) -> EmotionResult:
        """Classify emotion in text using ONNX model"""
        start_time = time.time()
        
        if not self.model_loaded:
            return self._fallback_classification(text, start_time)
        
        try:
            # Tokenize input
            inputs = self.tokenizer(
                text, 
                return_tensors="np" if NUMPY_AVAILABLE else "pt", 
                padding=True, 
                truncation=True, 
                max_length=128
            )
            
            # Run ONNX inference
            if NUMPY_AVAILABLE:
                outputs = self.session.run(None, {
                    "input_ids": inputs["input_ids"].astype(np.int64),
                    "attention_mask": inputs["attention_mask"].astype(np.int64)
                })
            else:
                # Convert to numpy-like arrays manually
                input_ids = [[int(x) for x in inputs["input_ids"][0]]]
                attention_mask = [[int(x) for x in inputs["attention_mask"][0]]]
                outputs = self.session.run(None, {
                    "input_ids": input_ids,
                    "attention_mask": attention_mask
                })
            
            # Process outputs
            logits = outputs[0][0]  # Get first batch
            probabilities = self._softmax(logits)
            
            # Map to emotions
            emotion_labels = ["joy", "sadness", "anger", "fear", "surprise", "neutral"]
            if NUMPY_AVAILABLE:
                max_idx = np.argmax(probabilities)
            else:
                max_idx = probabilities.index(max(probabilities))
            
            emotion = emotion_labels[max_idx]
            confidence = float(probabilities[max_idx])
            intensity = self._calculate_intensity(confidence)
            
            inference_time = (time.time() - start_time) * 1000
            self.inference_count += 1
            self.total_inference_time += inference_time
            
            return EmotionResult(
                emotion=emotion,
                confidence=confidence,
                intensity=intensity,
                raw_logits=logits.tolist() if NUMPY_AVAILABLE else list(logits),
                inference_time_ms=inference_time
            )
            
        except Exception as e:
            logging.error(f"[EmotionClassifier] Error in ONNX classification: {e}")
            return self._fallback_classification(text, start_time)
    
    def _softmax(self, x):
        """Apply softmax to logits"""
        if NUMPY_AVAILABLE:
            exp_x = np.exp(x - np.max(x))
            return exp_x / np.sum(exp_x)
        else:
            # Fallback implementation
            import math
            max_x = max(x)
            exp_x = [math.exp(xi - max_x) for xi in x]
            sum_exp = sum(exp_x)
            return [exp_xi / sum_exp for exp_xi in exp_x]
    
    def _calculate_intensity(self, confidence: float) -> str:
        """Calculate intensity based on confidence"""
        if confidence > 0.8:
            return "high"
        elif confidence > 0.6:
            return "medium"
        else:
            return "low"
    
    def _fallback_classification(self, text: str, start_time: float) -> EmotionResult:
        """Fallback emotion classification using keyword matching"""
        text_lower = text.lower()
        
        # Simple keyword-based classification
        emotion_keywords = {
            "joy": ["happy", "joy", "great", "awesome", "wonderful", "excited"],
            "sadness": ["sad", "down", "disappointed", "upset", "unhappy"],
            "anger": ["angry", "mad", "frustrated", "annoyed", "irritated"],
            "fear": ["scared", "afraid", "worried", "anxious", "nervous"],
            "surprise": ["surprised", "shocked", "amazed", "wow", "unexpected"],
            "neutral": []
        }
        
        scores = {}
        for emotion, keywords in emotion_keywords.items():
            scores[emotion] = sum(1 for keyword in keywords if keyword in text_lower)
        
        # Find highest scoring emotion
        max_emotion = max(scores.keys(), key=lambda k: scores[k])
        confidence = min(0.8, max(0.3, scores[max_emotion] * 0.2))
        
        if scores[max_emotion] == 0:
            max_emotion = "neutral"
            confidence = 0.5
        
        inference_time = (time.time() - start_time) * 1000
        
        return EmotionResult(
            emotion=max_emotion,
            confidence=confidence,
            intensity=self._calculate_intensity(confidence),
            raw_logits=[],
            inference_time_ms=inference_time
        )

# ============================================================================
# EMOTION RESPONSE MODULATOR
# ============================================================================

class EmotionResponseModulator:
    """Modify response tone, pace, and structure based on emotional state"""
    
    def __init__(self):
        self.modulation_history = []
        self.default_modulation = EmotionalModulation(
            tone=EmotionalTone.WARM,
            pace=ResponsePace.NORMAL,
            structure=ResponseStructure.CONVERSATIONAL,
            intensity=0.5,
            confidence=0.8,
            reasoning="default_setting",
            timestamp=datetime.now().isoformat()
        )
    
    def modulate_response(self, response: str, emotion_state: EmotionState, mood_state: MoodState) -> Tuple[str, EmotionalModulation]:
        """Modulate response based on emotional and mood state"""
        
        # Determine modulation based on emotion and mood
        modulation = self._determine_modulation(emotion_state, mood_state)
        
        # Apply modulation to response
        modulated_response = self._apply_modulation(response, modulation)
        
        # Store modulation history
        self.modulation_history.append(modulation)
        if len(self.modulation_history) > 50:
            self.modulation_history = self.modulation_history[-50:]
        
        return modulated_response, modulation
    
    def _determine_modulation(self, emotion_state: EmotionState, mood_state: MoodState) -> EmotionalModulation:
        """Determine appropriate modulation settings"""
        
        # Map emotions to tones
        emotion_tone_map = {
            "joy": EmotionalTone.EXCITED,
            "sadness": EmotionalTone.EMPATHETIC,
            "anger": EmotionalTone.CALM,
            "fear": EmotionalTone.CONFIDENT,
            "surprise": EmotionalTone.CURIOUS,
            "neutral": EmotionalTone.WARM
        }
        
        # Map moods to paces
        mood_pace_map = {
            MoodState.EXCITED: ResponsePace.FAST,
            MoodState.CALM: ResponsePace.SLOW,
            MoodState.ANXIOUS: ResponsePace.VARIABLE,
            MoodState.CONTEMPLATIVE: ResponsePace.SLOW,
        }
        
        tone = emotion_tone_map.get(emotion_state.primary_emotion, EmotionalTone.WARM)
        pace = mood_pace_map.get(mood_state, ResponsePace.NORMAL)
        
        # Determine structure based on intensity
        if emotion_state.intensity > 0.7:
            structure = ResponseStructure.DETAILED
        elif emotion_state.intensity < 0.3:
            structure = ResponseStructure.BRIEF
        else:
            structure = ResponseStructure.CONVERSATIONAL
        
        return EmotionalModulation(
            tone=tone,
            pace=pace,
            structure=structure,
            intensity=emotion_state.intensity,
            confidence=emotion_state.stability,
            reasoning=f"Based on {emotion_state.primary_emotion} emotion and {mood_state.value} mood",
            timestamp=datetime.now().isoformat()
        )
    
    def _apply_modulation(self, response: str, modulation: EmotionalModulation) -> str:
        """Apply emotional modulation to response text"""
        
        # Apply tone modifications
        if modulation.tone == EmotionalTone.EXCITED:
            response = self._add_excitement(response)
        elif modulation.tone == EmotionalTone.EMPATHETIC:
            response = self._add_empathy(response)
        elif modulation.tone == EmotionalTone.CALM:
            response = self._add_calmness(response)
        
        # Apply pace modifications
        if modulation.pace == ResponsePace.SLOW:
            response = self._slow_pace(response)
        elif modulation.pace == ResponsePace.FAST:
            response = self._fast_pace(response)
        
        return response
    
    def _add_excitement(self, response: str) -> str:
        """Add excitement to response"""
        if not response.endswith(("!", "?", ".")):
            response += "!"
        return response
    
    def _add_empathy(self, response: str) -> str:
        """Add empathy to response"""
        empathy_starters = ["I understand", "I can see that", "That sounds"]
        if not any(response.startswith(starter) for starter in empathy_starters):
            response = f"I understand. {response}"
        return response
    
    def _add_calmness(self, response: str) -> str:
        """Add calmness to response"""
        calm_words = ["gently", "softly", "peacefully", "calmly"]
        # This is a simplified implementation
        return response
    
    def _slow_pace(self, response: str) -> str:
        """Modify for slower pace"""
        # Add pauses and extend phrasing
        return response.replace(". ", "... ")
    
    def _fast_pace(self, response: str) -> str:
        """Modify for faster pace"""
        # Shorten sentences and make more direct
        return response.replace("...", ".").replace("  ", " ")

# ============================================================================
# MOOD MANAGER
# ============================================================================

class MoodManager:
    """Dynamic mood evolution and influence system"""
    
    def __init__(self, mood_dir: str = "mood_states"):
        self.mood_dir = Path(mood_dir)
        self.mood_dir.mkdir(exist_ok=True)
        self.user_moods: Dict[str, MoodProfile] = {}
        self.lock = threading.Lock()
        
        # Mood evolution parameters
        self.mood_decay_rate = 0.01  # How fast moods return to neutral
        self.interaction_influence = 0.1  # How much interactions affect mood
        self.time_influence = 0.05  # How much time affects mood
        
        logging.info("[MoodManager] 🎭 Mood manager initialized")
    
    def get_user_mood(self, user_name: str) -> MoodProfile:
        """Get or create mood profile for user"""
        with self.lock:
            if user_name not in self.user_moods:
                self.user_moods[user_name] = self._load_user_mood(user_name)
            return self.user_moods[user_name]
    
    def update_user_mood(self, user_name: str, trigger: MoodTrigger, intensity: float = 0.1):
        """Update user's mood based on trigger"""
        with self.lock:
            mood_profile = self.get_user_mood(user_name)
            
            # Apply mood change based on trigger
            new_mood = self._calculate_mood_change(mood_profile, trigger, intensity)
            mood_profile.current_mood = new_mood
            mood_profile.intensity = min(1.0, max(0.0, mood_profile.intensity + intensity))
            mood_profile.interaction_count += 1
            mood_profile.last_interaction = datetime.now()
            
            # Add to history
            mood_profile.mood_history.append({
                "timestamp": datetime.now().isoformat(),
                "mood": new_mood.value,
                "intensity": mood_profile.intensity,
                "trigger": trigger.value
            })
            
            # Keep only last 100 mood changes
            if len(mood_profile.mood_history) > 100:
                mood_profile.mood_history = mood_profile.mood_history[-100:]
            
            # Save to disk
            self._save_user_mood(user_name, mood_profile)
            
            logging.debug(f"[MoodManager] Updated {user_name} mood to {new_mood.value} (intensity: {mood_profile.intensity:.2f})")
    
    def _calculate_mood_change(self, mood_profile: MoodProfile, trigger: MoodTrigger, intensity: float) -> MoodState:
        """Calculate new mood based on trigger and current state"""
        
        # Mood transition mappings
        positive_triggers = [MoodTrigger.POSITIVE_FEEDBACK, MoodTrigger.USER_INTERACTION]
        negative_triggers = [MoodTrigger.NEGATIVE_FEEDBACK, MoodTrigger.PROLONGED_SILENCE]
        
        current_mood = mood_profile.current_mood
        
        if trigger in positive_triggers:
            # Move toward positive moods
            positive_moods = [MoodState.JOYFUL, MoodState.EXCITED, MoodState.CONTENT, MoodState.PLAYFUL]
            if current_mood in [MoodState.MELANCHOLY, MoodState.ANXIOUS, MoodState.FRUSTRATED]:
                return MoodState.NEUTRAL  # First move to neutral
            else:
                return random.choice(positive_moods)
        
        elif trigger in negative_triggers:
            # Move toward negative moods (but gently)
            if intensity > 0.5:
                return MoodState.MELANCHOLY
            else:
                return MoodState.CONTEMPLATIVE
        
        else:
            # Gradual return to neutral
            return MoodState.NEUTRAL
    
    def _load_user_mood(self, user_name: str) -> MoodProfile:
        """Load user mood from disk"""
        mood_file = self.mood_dir / f"{user_name}_mood.json"
        
        if mood_file.exists():
            try:
                with open(mood_file, 'r') as f:
                    data = json.load(f)
                
                mood_profile = MoodProfile()
                mood_profile.current_mood = MoodState(data.get("current_mood", "neutral"))
                mood_profile.intensity = data.get("intensity", 0.5)
                mood_profile.stability = data.get("stability", 0.8)
                mood_profile.mood_history = data.get("mood_history", [])
                mood_profile.interaction_count = data.get("interaction_count", 0)
                
                if data.get("last_interaction"):
                    mood_profile.last_interaction = datetime.fromisoformat(data["last_interaction"])
                
                mood_profile.personality_traits = data.get("personality_traits", ["empathetic", "helpful"])
                
                return mood_profile
                
            except Exception as e:
                logging.warning(f"[MoodManager] Could not load mood for {user_name}: {e}")
        
        # Return default mood profile
        return MoodProfile()
    
    def _save_user_mood(self, user_name: str, mood_profile: MoodProfile):
        """Save user mood to disk"""
        mood_file = self.mood_dir / f"{user_name}_mood.json"
        
        try:
            data = {
                "current_mood": mood_profile.current_mood.value,
                "intensity": mood_profile.intensity,
                "stability": mood_profile.stability,
                "mood_history": mood_profile.mood_history,
                "interaction_count": mood_profile.interaction_count,
                "last_interaction": mood_profile.last_interaction.isoformat() if mood_profile.last_interaction else None,
                "personality_traits": mood_profile.personality_traits,
                "last_updated": datetime.now().isoformat()
            }
            
            with open(mood_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            logging.error(f"[MoodManager] Could not save mood for {user_name}: {e}")

# ============================================================================
# UNIFIED EMOTION-MOOD SYSTEM
# ============================================================================

class EmotionMoodSystem:
    """Unified emotion and mood management system"""
    
    def __init__(self):
        self.emotion_classifier = EmotionClassifier()
        self.response_modulator = EmotionResponseModulator()
        self.mood_manager = MoodManager()
        
        # Current emotion state
        self.current_emotion = EmotionState()
        
        # User session tracking
        self.user_emotions: Dict[str, EmotionState] = {}
        
        logging.info("[EmotionMoodSystem] 🎭 Unified emotion-mood system initialized")
    
    def process_user_input(self, text: str, user_name: str = "User") -> Tuple[EmotionResult, EmotionState, MoodState]:
        """Process user input for emotion and mood"""
        
        # Classify emotion
        emotion_result = self.emotion_classifier.classify_emotion(text)
        
        # Update emotion state
        emotion_state = self._update_emotion_state(user_name, emotion_result)
        
        # Update mood based on emotion
        self._update_mood_from_emotion(user_name, emotion_result)
        
        # Get current mood
        mood_profile = self.mood_manager.get_user_mood(user_name)
        
        return emotion_result, emotion_state, mood_profile.current_mood
    
    def generate_modulated_response(self, response: str, user_name: str = "User") -> Tuple[str, EmotionalModulation]:
        """Generate emotionally modulated response"""
        
        # Get current states
        emotion_state = self.user_emotions.get(user_name, self.current_emotion)
        mood_profile = self.mood_manager.get_user_mood(user_name)
        
        # Modulate response
        return self.response_modulator.modulate_response(response, emotion_state, mood_profile.current_mood)
    
    def _update_emotion_state(self, user_name: str, emotion_result: EmotionResult) -> EmotionState:
        """Update emotion state for user"""
        
        if user_name not in self.user_emotions:
            self.user_emotions[user_name] = EmotionState()
        
        emotion_state = self.user_emotions[user_name]
        
        # Update emotion state
        emotion_state.primary_emotion = emotion_result.emotion
        emotion_state.intensity = emotion_result.confidence
        
        # Calculate arousal and valence based on emotion
        arousal_map = {
            "joy": 0.8, "excitement": 0.9, "anger": 0.9, "fear": 0.7,
            "surprise": 0.8, "sadness": 0.3, "neutral": 0.5
        }
        valence_map = {
            "joy": 0.9, "excitement": 0.9, "trust": 0.8, "surprise": 0.6,
            "neutral": 0.5, "fear": 0.2, "anger": 0.1, "sadness": 0.1
        }
        
        emotion_state.arousal = arousal_map.get(emotion_result.emotion, 0.5)
        emotion_state.valence = valence_map.get(emotion_result.emotion, 0.5)
        emotion_state.last_update = datetime.now()
        
        return emotion_state
    
    def _update_mood_from_emotion(self, user_name: str, emotion_result: EmotionResult):
        """Update mood based on detected emotion"""
        
        # Map emotions to mood triggers
        if emotion_result.emotion in ["joy", "excitement", "trust"]:
            trigger = MoodTrigger.POSITIVE_FEEDBACK
        elif emotion_result.emotion in ["anger", "sadness", "fear"]:
            trigger = MoodTrigger.NEGATIVE_FEEDBACK
        else:
            trigger = MoodTrigger.USER_INTERACTION
        
        # Update mood with appropriate intensity
        intensity = emotion_result.confidence * 0.2  # Scale down intensity for mood changes
        self.mood_manager.update_user_mood(user_name, trigger, intensity)
    
    def reset_session_for_user_smart(self, user_name: str):
        """Reset emotion session for user (compatibility method)"""
        if user_name in self.user_emotions:
            self.user_emotions[user_name] = EmotionState()
        logging.info(f"[EmotionMoodSystem] Reset emotion session for {user_name}")
    
    def get_user_emotion_summary(self, user_name: str) -> Dict[str, Any]:
        """Get emotion summary for user"""
        emotion_state = self.user_emotions.get(user_name, self.current_emotion)
        mood_profile = self.mood_manager.get_user_mood(user_name)
        
        return {
            "emotion": {
                "primary": emotion_state.primary_emotion,
                "intensity": emotion_state.intensity,
                "arousal": emotion_state.arousal,
                "valence": emotion_state.valence,
                "stability": emotion_state.stability
            },
            "mood": {
                "current": mood_profile.current_mood.value,
                "intensity": mood_profile.intensity,
                "stability": mood_profile.stability,
                "interaction_count": mood_profile.interaction_count
            },
            "classifier_stats": {
                "inference_count": self.emotion_classifier.inference_count,
                "avg_inference_time": (self.emotion_classifier.total_inference_time / 
                                     max(1, self.emotion_classifier.inference_count))
            }
        }

# ============================================================================
# GLOBAL INSTANCE AND COMPATIBILITY
# ============================================================================

# Create global instance
emotion_mood_system = EmotionMoodSystem()

# Backward compatibility functions
def reset_session_for_user_smart(user_name: str):
    """Backward compatibility function"""
    emotion_mood_system.reset_session_for_user_smart(user_name)

def classify_emotion(text: str) -> EmotionResult:
    """Backward compatibility function"""
    return emotion_mood_system.emotion_classifier.classify_emotion(text)

def get_user_mood(user_name: str) -> MoodProfile:
    """Backward compatibility function"""
    return emotion_mood_system.mood_manager.get_user_mood(user_name)

# Export main classes and functions
__all__ = [
    'EmotionMoodSystem',
    'EmotionClassifier',
    'EmotionResponseModulator', 
    'MoodManager',
    'EmotionType',
    'MoodState',
    'EmotionalTone',
    'EmotionResult',
    'EmotionState',
    'MoodProfile',
    'emotion_mood_system',
    'reset_session_for_user_smart',  # Backward compatibility
    'classify_emotion',  # Backward compatibility
    'get_user_mood'  # Backward compatibility
]