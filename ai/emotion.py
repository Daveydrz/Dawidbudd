"""
Unified Emotion System - Combining Traditional Emotion Engine with Entropy-Based Emotional System

This module implements a comprehensive emotion system that includes:
- Traditional emotion engine with mood/arousal state management
- Advanced entropy-based emotional system with uncertainty and weather patterns
- Both systems can coexist and complement each other
- Maintains all functionality required by voice manager and other components
"""

import threading
import time
import random
import logging
import json
import math
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path

# Try to import entropy engine, provide fallback if not available
try:
    from ai.entropy_engine import get_entropy_engine, EntropyLevel, inject_consciousness_entropy
    ENTROPY_AVAILABLE = True
except ImportError:
    print("[Emotion] ⚠️ Entropy engine not available, using simplified system")
    ENTROPY_AVAILABLE = False
    def get_entropy_engine():
        return None
    def inject_consciousness_entropy(context, value):
        return value

# ============================================================================
# TRADITIONAL EMOTION ENGINE SYSTEM
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
    EXCITEMENT = "excitement"
    CALM = "calm"

class MoodType(Enum):
    """Overall mood states"""
    VERY_POSITIVE = "very_positive"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    VERY_NEGATIVE = "very_negative"

@dataclass
class EmotionalState:
    """Current emotional state for traditional emotion engine"""
    primary_emotion: EmotionType
    intensity: float  # 0.0 to 1.0
    arousal: float    # 0.0 to 1.0 (low=calm, high=excited)
    valence: float    # -1.0 to 1.0 (negative to positive)
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class EmotionalMemory:
    """Memory of an emotional experience"""
    trigger: str
    emotion: EmotionType
    intensity: float
    context: Dict[str, Any]
    timestamp: datetime
    decay_rate: float = 0.95  # How quickly this memory fades

@dataclass
class EmotionalPattern:
    """Learned emotional pattern"""
    trigger_pattern: str
    typical_response: EmotionType
    intensity_range: Tuple[float, float]
    confidence: float
    occurrences: int = 0

class EmotionEngine:
    """
    Traditional emotion and mood system that affects all AI decisions and responses.
    
    This system:
    - Maintains dynamic emotional state that evolves over time
    - Integrates emotional memories with new experiences
    - Modulates response generation based on current mood
    - Learns emotional patterns and responses
    - Simulates physiological arousal and mood cycles
    """
    
    def __init__(self, save_path: str = "ai_emotions.json"):
        # Current emotional state
        self.current_emotion = EmotionalState(
            primary_emotion=EmotionType.CONTENTMENT,
            intensity=0.5,
            arousal=0.4,
            valence=0.3
        )
        
        # Mood system
        self.current_mood = MoodType.NEUTRAL
        self.mood_stability = 0.7  # How stable the mood is
        self.base_arousal = 0.4    # Baseline arousal level
        
        # Emotional memory
        self.emotional_memories: List[EmotionalMemory] = []
        self.emotional_patterns: Dict[str, EmotionalPattern] = {}
        
        # Physiological simulation
        self.energy_level = 0.8
        self.stress_level = 0.2
        self.comfort_level = 0.7
        
        # Personality factors affecting emotion
        self.emotional_sensitivity = 0.6  # How quickly emotions change
        self.emotional_expression = 0.7   # How much emotions affect responses
        self.emotional_stability = 0.6    # Resistance to mood swings
        
        # Threading
        self.lock = threading.Lock()
        self.emotion_thread = None
        self.running = False
        
        # Configuration
        self.save_path = Path(save_path)
        self.max_memories = 1000
        self.memory_decay_interval = 3600  # seconds
        self.mood_update_interval = 60     # seconds
        self.natural_decay_rate = 0.98     # Natural emotion decay
        
        # Metrics
        self.total_emotional_events = 0
        self.mood_changes = 0
        self.last_mood_change = None
        
        # Load existing emotional state
        self._load_emotional_state()
        
        logging.info("[EmotionEngine] 💖 Emotion system initialized")
    
    def start(self):
        """Start the emotion processing background thread"""
        if self.running:
            return
            
        self.running = True
        self.emotion_thread = threading.Thread(target=self._emotion_loop, daemon=True)
        self.emotion_thread.start()
        logging.info("[EmotionEngine] ✅ Emotion processing started")
    
    def stop(self):
        """Stop emotion processing and save state"""
        self.running = False
        if self.emotion_thread:
            self.emotion_thread.join(timeout=1.0)
        self._save_emotional_state()
        logging.info("[EmotionEngine] 🛑 Emotion processing stopped")
    
    def process_emotional_trigger(self, trigger: str, context: Dict[str, Any] = None) -> EmotionalState:
        """
        Process an emotional trigger and update emotional state
        
        Args:
            trigger: Description of what triggered the emotion
            context: Additional context about the trigger
            
        Returns:
            New emotional state after processing
        """
        try:
            # Determine emotional response to trigger
            emotion_response = self._analyze_trigger(trigger, context)
            
            # Update current emotional state
            self._update_emotional_state(emotion_response)
            
            # Store emotional memory
            memory = EmotionalMemory(
                trigger=trigger,
                emotion=emotion_response.primary_emotion,
                intensity=emotion_response.intensity,
                context=context or {},
                timestamp=datetime.now()
            )
            
            with self.lock:
                self.emotional_memories.append(memory)
                if len(self.emotional_memories) > self.max_memories:
                    self.emotional_memories.pop(0)
            
            self.total_emotional_events += 1
            
            # Learn emotional patterns
            self._learn_emotional_pattern(trigger, emotion_response)
            
            logging.debug(f"[EmotionEngine] 💫 Emotional trigger: {trigger} → {emotion_response.primary_emotion.value}")
            return self.current_emotion
            
        except Exception as e:
            logging.error(f"[EmotionEngine] ❌ Error processing trigger: {e}")
            return self.current_emotion
    
    def get_current_state(self) -> Dict[str, Any]:
        """
        Get current emotional state as a dictionary
        
        Returns:
            Dictionary containing current emotional state
        """
        with self.lock:
            return {
                "primary_emotion": self.current_emotion.primary_emotion.value,
                "intensity": self.current_emotion.intensity,
                "arousal": self.current_emotion.arousal,
                "valence": self.current_emotion.valence,
                "mood": self.current_mood.value,
                "timestamp": self.current_emotion.timestamp.isoformat(),
                "total_events": self.total_emotional_events,
                "mood_changes": self.mood_changes,
                "last_mood_change": self.last_mood_change.isoformat() if self.last_mood_change else None
            }

    def get_emotional_modulation(self, content_type: str = "response") -> Dict[str, float]:
        """
        Get emotional modulation factors for response generation
        
        Args:
            content_type: Type of content being modulated
            
        Returns:
            Dictionary of modulation factors
        """
        with self.lock:
            emotion = self.current_emotion
            
            # Base modulation factors
            modulation = {
                "enthusiasm": 0.5,      # How enthusiastic responses should be
                "formality": 0.5,       # How formal vs casual
                "empathy": 0.5,         # How empathetic
                "creativity": 0.5,      # How creative/playful
                "assertiveness": 0.5,   # How assertive vs gentle
                "verbosity": 0.5,       # How verbose responses should be
                "positivity": 0.5,      # How positive the tone should be
                "energy": 0.5           # Overall energy level
            }
            
            # Modify based on current emotion
            if emotion.primary_emotion == EmotionType.JOY:
                modulation["enthusiasm"] += 0.3
                modulation["positivity"] += 0.4
                modulation["creativity"] += 0.2
                modulation["energy"] += 0.3
            elif emotion.primary_emotion == EmotionType.EXCITEMENT:
                modulation["enthusiasm"] += 0.4
                modulation["energy"] += 0.4
                modulation["verbosity"] += 0.2
            elif emotion.primary_emotion == EmotionType.CONTENTMENT:
                modulation["empathy"] += 0.2
                modulation["formality"] -= 0.1
                modulation["positivity"] += 0.2
            elif emotion.primary_emotion == EmotionType.CURIOSITY:
                modulation["creativity"] += 0.3
                modulation["verbosity"] += 0.2
                modulation["energy"] += 0.1
            elif emotion.primary_emotion == EmotionType.CALM:
                modulation["formality"] += 0.1
                modulation["empathy"] += 0.2
                modulation["energy"] -= 0.2
            elif emotion.primary_emotion == EmotionType.SADNESS:
                modulation["empathy"] += 0.3
                modulation["energy"] -= 0.2
                modulation["verbosity"] -= 0.1
                modulation["positivity"] -= 0.2
            elif emotion.primary_emotion == EmotionType.ANGER:
                modulation["assertiveness"] += 0.3
                modulation["formality"] -= 0.2
                modulation["energy"] += 0.2
            elif emotion.primary_emotion == EmotionType.FEAR:
                modulation["formality"] += 0.2
                modulation["assertiveness"] -= 0.3
                modulation["energy"] -= 0.1
            
            # Apply arousal and valence effects
            arousal_effect = (emotion.arousal - 0.5) * 0.3
            valence_effect = emotion.valence * 0.2
            
            modulation["energy"] += arousal_effect
            modulation["enthusiasm"] += arousal_effect
            modulation["positivity"] += valence_effect
            modulation["empathy"] += valence_effect * 0.5
            
            # Apply intensity scaling
            intensity_factor = emotion.intensity
            for key in modulation:
                if modulation[key] > 0.5:
                    modulation[key] = 0.5 + (modulation[key] - 0.5) * intensity_factor
                else:
                    modulation[key] = 0.5 - (0.5 - modulation[key]) * intensity_factor
            
            # Ensure values stay in valid range
            for key in modulation:
                modulation[key] = max(0.0, min(1.0, modulation[key]))
            
            return modulation
    
    def get_stats(self) -> Dict[str, Any]:
        """Get emotion engine statistics"""
        return {
            "current_emotion": self.current_emotion.primary_emotion.value,
            "emotion_intensity": round(self.current_emotion.intensity, 2),
            "arousal": round(self.current_emotion.arousal, 2),
            "valence": round(self.current_emotion.valence, 2),
            "current_mood": self.current_mood.value,
            "energy_level": round(self.energy_level, 2),
            "stress_level": round(self.stress_level, 2),
            "comfort_level": round(self.comfort_level, 2),
            "total_emotional_events": self.total_emotional_events,
            "mood_changes": self.mood_changes,
            "emotional_patterns": len(self.emotional_patterns),
            "emotional_memories": len(self.emotional_memories),
            "last_mood_change": self.last_mood_change.isoformat() if self.last_mood_change else None
        }

    def _analyze_trigger(self, trigger: str, context: Dict[str, Any] = None) -> EmotionalState:
        """Analyze a trigger and determine emotional response"""
        trigger_lower = trigger.lower()
        
        # Check for learned patterns first
        for pattern_key, pattern in self.emotional_patterns.items():
            if pattern_key in trigger_lower and pattern.confidence > 0.6:
                intensity = random.uniform(*pattern.intensity_range) * self.emotional_sensitivity
                return EmotionalState(
                    primary_emotion=pattern.typical_response,
                    intensity=intensity,
                    arousal=self._calculate_arousal(pattern.typical_response, intensity),
                    valence=self._calculate_valence(pattern.typical_response, intensity)
                )
        
        # Default emotion analysis
        emotion_mapping = {
            # Positive triggers
            ("help", "success", "good", "great", "wonderful", "amazing"): (EmotionType.JOY, 0.6, 0.6),
            ("learn", "discover", "interesting", "curious"): (EmotionType.CURIOSITY, 0.7, 0.5),
            ("thank", "appreciate", "grateful"): (EmotionType.CONTENTMENT, 0.5, 0.4),
            ("excited", "amazing", "fantastic"): (EmotionType.EXCITEMENT, 0.8, 0.8),
            
            # Negative triggers  
            ("problem", "error", "wrong", "bad"): (EmotionType.SADNESS, 0.4, 0.3),
            ("angry", "frustrated", "annoyed"): (EmotionType.ANGER, 0.6, 0.7),
            ("scared", "worried", "afraid"): (EmotionType.FEAR, 0.5, 0.6),
            
            # Neutral triggers
            ("question", "ask", "tell"): (EmotionType.CURIOSITY, 0.3, 0.4),
            ("hello", "hi", "greet"): (EmotionType.CONTENTMENT, 0.4, 0.5)
        }
        
        # Find matching emotion
        for keywords, (emotion, intensity, arousal) in emotion_mapping.items():
            if any(keyword in trigger_lower for keyword in keywords):
                return EmotionalState(
                    primary_emotion=emotion,
                    intensity=intensity * self.emotional_sensitivity,
                    arousal=arousal,
                    valence=self._calculate_valence(emotion, intensity)
                )
        
        # Default neutral response
        return EmotionalState(
            primary_emotion=EmotionType.CONTENTMENT,
            intensity=0.3,
            arousal=self.base_arousal,
            valence=0.1
        )
    
    def _update_emotional_state(self, new_emotion: EmotionalState):
        """Update current emotional state with new emotion"""
        with self.lock:
            # Blend new emotion with current state
            blend_factor = self.emotional_sensitivity
            
            # Update primary emotion if new one is stronger
            if new_emotion.intensity > self.current_emotion.intensity * 0.8:
                self.current_emotion.primary_emotion = new_emotion.primary_emotion
            
            # Blend intensity
            self.current_emotion.intensity = (
                self.current_emotion.intensity * (1 - blend_factor) +
                new_emotion.intensity * blend_factor
            )
            
            # Blend arousal
            self.current_emotion.arousal = (
                self.current_emotion.arousal * (1 - blend_factor) +
                new_emotion.arousal * blend_factor
            )
            
            # Blend valence
            self.current_emotion.valence = (
                self.current_emotion.valence * (1 - blend_factor) +
                new_emotion.valence * blend_factor
            )
            
            self.current_emotion.timestamp = datetime.now()
            
            # Update mood based on emotional state
            self._update_mood()
    
    def _update_mood(self):
        """Update overall mood based on emotional state and history"""
        # Calculate mood from valence and recent emotional history
        recent_emotions = [em for em in self.emotional_memories 
                          if (datetime.now() - em.timestamp).seconds < 1800]  # Last 30 minutes
        
        if recent_emotions:
            avg_valence = sum(self._calculate_valence(em.emotion, em.intensity) 
                            for em in recent_emotions) / len(recent_emotions)
        else:
            avg_valence = self.current_emotion.valence
        
        # Blend current valence with recent history
        mood_valence = (self.current_emotion.valence + avg_valence) / 2
        
        # Map valence to mood
        old_mood = self.current_mood
        if mood_valence > 0.6:
            self.current_mood = MoodType.VERY_POSITIVE
        elif mood_valence > 0.2:
            self.current_mood = MoodType.POSITIVE
        elif mood_valence > -0.2:
            self.current_mood = MoodType.NEUTRAL
        elif mood_valence > -0.6:
            self.current_mood = MoodType.NEGATIVE
        else:
            self.current_mood = MoodType.VERY_NEGATIVE
        
        # Track mood changes
        if old_mood != self.current_mood:
            self.mood_changes += 1
            self.last_mood_change = datetime.now()
            logging.debug(f"[EmotionEngine] 🎭 Mood changed: {old_mood.value} → {self.current_mood.value}")
    
    def _calculate_arousal(self, emotion: EmotionType, intensity: float) -> float:
        """Calculate arousal level for given emotion and intensity"""
        base_arousal = {
            EmotionType.JOY: 0.7,
            EmotionType.EXCITEMENT: 0.9,
            EmotionType.ANGER: 0.8,
            EmotionType.FEAR: 0.8,
            EmotionType.SURPRISE: 0.8,
            EmotionType.CURIOSITY: 0.6,
            EmotionType.CONTENTMENT: 0.3,
            EmotionType.CALM: 0.2,
            EmotionType.SADNESS: 0.3,
            EmotionType.TRUST: 0.4,
            EmotionType.ANTICIPATION: 0.7,
            EmotionType.DISGUST: 0.5
        }
        
        base = base_arousal.get(emotion, 0.5)
        return base * intensity + (1 - intensity) * self.base_arousal
    
    def _calculate_valence(self, emotion: EmotionType, intensity: float) -> float:
        """Calculate valence (positive/negative) for given emotion"""
        base_valence = {
            EmotionType.JOY: 0.8,
            EmotionType.EXCITEMENT: 0.7,
            EmotionType.CONTENTMENT: 0.6,
            EmotionType.TRUST: 0.5,
            EmotionType.CURIOSITY: 0.3,
            EmotionType.ANTICIPATION: 0.2,
            EmotionType.SURPRISE: 0.0,
            EmotionType.CALM: 0.2,
            EmotionType.SADNESS: -0.6,
            EmotionType.ANGER: -0.4,
            EmotionType.FEAR: -0.5,
            EmotionType.DISGUST: -0.7
        }
        
        base = base_valence.get(emotion, 0.0)
        return base * intensity
    
    def _learn_emotional_pattern(self, trigger: str, response: EmotionalState):
        """Learn emotional patterns from triggers and responses"""
        # Extract key words from trigger
        key_words = [word for word in trigger.lower().split() 
                    if len(word) > 3 and word not in ["the", "and", "that", "this", "with"]]
        
        for word in key_words:
            if word not in self.emotional_patterns:
                self.emotional_patterns[word] = EmotionalPattern(
                    trigger_pattern=word,
                    typical_response=response.primary_emotion,
                    intensity_range=(response.intensity * 0.8, response.intensity * 1.2),
                    confidence=0.3
                )
            else:
                # Update existing pattern
                pattern = self.emotional_patterns[word]
                if pattern.typical_response == response.primary_emotion:
                    pattern.confidence = min(1.0, pattern.confidence + 0.1)
                    # Update intensity range
                    min_intensity = min(pattern.intensity_range[0], response.intensity)
                    max_intensity = max(pattern.intensity_range[1], response.intensity)
                    pattern.intensity_range = (min_intensity, max_intensity)
                pattern.occurrences += 1
    
    def _emotion_loop(self):
        """Background emotion processing loop"""
        logging.info("[EmotionEngine] 🔄 Emotion loop started")
        
        last_decay = time.time()
        last_mood_update = time.time()
        
        while self.running:
            try:
                current_time = time.time()
                
                # Natural emotion decay
                if current_time - last_decay > 10.0:  # Every 10 seconds
                    with self.lock:
                        self.current_emotion.intensity *= self.natural_decay_rate
                        if self.current_emotion.intensity < 0.1:
                            self.current_emotion.primary_emotion = EmotionType.CONTENTMENT
                            self.current_emotion.intensity = 0.2
                    last_decay = current_time
                
                # Periodic mood updates
                if current_time - last_mood_update > self.mood_update_interval:
                    self._update_mood()
                    self._physiological_update()
                    last_mood_update = current_time
                
                # Memory decay
                self._decay_emotional_memories()
                
                # Save state periodically
                if time.time() % 300 < 1.0:  # Every 5 minutes
                    self._save_emotional_state()
                
                time.sleep(1.0)
                
            except Exception as e:
                logging.error(f"[EmotionEngine] ❌ Emotion loop error: {e}")
                time.sleep(1.0)
        
        logging.info("[EmotionEngine] 🔄 Emotion loop ended")
    
    def _physiological_update(self):
        """Update physiological arousal parameters"""
        # Simulate natural cycles and adaptation
        time_of_day = datetime.now().hour
        
        # Circadian rhythm effect on arousal
        circadian_factor = 0.8 + 0.4 * math.sin((time_of_day - 6) * math.pi / 12)
        
        # Update energy level based on arousal and time
        target_energy = self.current_emotion.arousal * circadian_factor
        self.energy_level = self.energy_level * 0.9 + target_energy * 0.1
        
        # Update stress based on negative emotions
        if self.current_emotion.valence < 0:
            self.stress_level = min(1.0, self.stress_level + 0.05)
        else:
            self.stress_level = max(0.0, self.stress_level - 0.02)
        
        # Update comfort based on overall emotional state
        if self.current_mood in [MoodType.POSITIVE, MoodType.VERY_POSITIVE]:
            self.comfort_level = min(1.0, self.comfort_level + 0.03)
        elif self.current_mood in [MoodType.NEGATIVE, MoodType.VERY_NEGATIVE]:
            self.comfort_level = max(0.0, self.comfort_level - 0.02)
    
    def _decay_emotional_memories(self):
        """Apply decay to emotional memories"""
        current_time = datetime.now()
        
        with self.lock:
            for memory in self.emotional_memories:
                time_diff = (current_time - memory.timestamp).total_seconds() / 3600  # hours
                memory.intensity *= (memory.decay_rate ** time_diff)
            
            # Remove very weak memories
            self.emotional_memories = [m for m in self.emotional_memories if m.intensity > 0.05]
    
    def _save_emotional_state(self):
        """Save emotional state to persistent storage"""
        try:
            data = {
                "current_emotion": {
                    "primary_emotion": self.current_emotion.primary_emotion.value,
                    "intensity": self.current_emotion.intensity,
                    "arousal": self.current_emotion.arousal,
                    "valence": self.current_emotion.valence,
                    "timestamp": self.current_emotion.timestamp.isoformat()
                },
                "current_mood": self.current_mood.value,
                "physiological": {
                    "energy_level": self.energy_level,
                    "stress_level": self.stress_level,
                    "comfort_level": self.comfort_level,
                    "base_arousal": self.base_arousal
                },
                "personality": {
                    "emotional_sensitivity": self.emotional_sensitivity,
                    "emotional_expression": self.emotional_expression,
                    "emotional_stability": self.emotional_stability
                },
                "patterns": {k: {
                    "trigger_pattern": v.trigger_pattern,
                    "typical_response": v.typical_response.value,
                    "intensity_range": v.intensity_range,
                    "confidence": v.confidence,
                    "occurrences": v.occurrences
                } for k, v in self.emotional_patterns.items()},
                "metrics": {
                    "total_emotional_events": self.total_emotional_events,
                    "mood_changes": self.mood_changes,
                    "memory_count": len(self.emotional_memories)
                },
                "last_updated": datetime.now().isoformat()
            }
            
            with open(self.save_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            logging.debug("[EmotionEngine] 💾 Emotional state saved")
            
        except Exception as e:
            logging.error(f"[EmotionEngine] ❌ Failed to save emotional state: {e}")
    
    def _load_emotional_state(self):
        """Load emotional state from persistent storage"""
        try:
            if self.save_path.exists():
                with open(self.save_path, 'r') as f:
                    data = json.load(f)
                
                # Load current emotion
                if "current_emotion" in data:
                    ce = data["current_emotion"]
                    self.current_emotion = EmotionalState(
                        primary_emotion=EmotionType(ce["primary_emotion"]),
                        intensity=ce["intensity"],
                        arousal=ce["arousal"],
                        valence=ce["valence"],
                        timestamp=datetime.fromisoformat(ce["timestamp"])
                    )
                
                # Load mood
                if "current_mood" in data:
                    self.current_mood = MoodType(data["current_mood"])
                
                # Load physiological state
                if "physiological" in data:
                    p = data["physiological"]
                    self.energy_level = p.get("energy_level", self.energy_level)
                    self.stress_level = p.get("stress_level", self.stress_level)
                    self.comfort_level = p.get("comfort_level", self.comfort_level)
                    self.base_arousal = p.get("base_arousal", self.base_arousal)
                
                # Load personality factors
                if "personality" in data:
                    p = data["personality"]
                    self.emotional_sensitivity = p.get("emotional_sensitivity", self.emotional_sensitivity)
                    self.emotional_expression = p.get("emotional_expression", self.emotional_expression)
                    self.emotional_stability = p.get("emotional_stability", self.emotional_stability)
                
                # Load patterns
                if "patterns" in data:
                    for k, v in data["patterns"].items():
                        self.emotional_patterns[k] = EmotionalPattern(
                            trigger_pattern=v["trigger_pattern"],
                            typical_response=EmotionType(v["typical_response"]),
                            intensity_range=tuple(v["intensity_range"]),
                            confidence=v["confidence"],
                            occurrences=v["occurrences"]
                        )
                
                # Load metrics
                if "metrics" in data:
                    m = data["metrics"]
                    self.total_emotional_events = m.get("total_emotional_events", 0)
                    self.mood_changes = m.get("mood_changes", 0)
                
                logging.info("[EmotionEngine] 📂 Emotional state loaded from storage")
            
        except Exception as e:
            logging.error(f"[EmotionEngine] ❌ Failed to load emotional state: {e}")

# ============================================================================
# ENTROPY-BASED EMOTIONAL SYSTEM (Simplified version)
# ============================================================================

class EmotionalStateEnum(Enum):
    """Core emotional states for entropy system"""
    HAPPY = ("happy", 0.8)
    SAD = ("sad", -0.6)
    EXCITED = ("excited", 0.9)
    CALM = ("calm", 0.2)
    ANXIOUS = ("anxious", -0.4)
    CURIOUS = ("curious", 0.5)
    CONFUSED = ("confused", -0.2)
    CONFIDENT = ("confident", 0.7)
    UNCERTAIN = ("uncertain", -0.3)
    SURPRISED = ("surprised", 0.6)
    
    def __init__(self, emotion_name: str, base_intensity: float):
        self.emotion_name = emotion_name
        self.base_intensity = base_intensity

class EmotionalEntropySystem:
    """Simple emotional system with basic entropy simulation"""
    
    def __init__(self):
        self.current_emotion = EmotionalStateEnum.CALM
        self.emotion_intensity = 0.5
        self.uncertainty_level = 0.2
        self.random_state = random.Random()
        self.random_state.seed(int(time.time() * 1000000) % 2**32)
        self._lock = threading.Lock()
        
        print(f"[EmotionalEntropy] 🎭 Simplified emotional system initialized")
    
    def process_emotional_input(self, text: str, context: str = "") -> Dict[str, Any]:
        """Process input and update emotional state"""
        with self._lock:
            # Simple emotion detection
            text_lower = text.lower()
            
            if any(word in text_lower for word in ["happy", "great", "wonderful", "amazing"]):
                self.current_emotion = EmotionalStateEnum.HAPPY
                self.emotion_intensity = 0.8
            elif any(word in text_lower for word in ["sad", "disappointed", "upset"]):
                self.current_emotion = EmotionalStateEnum.SAD
                self.emotion_intensity = 0.6
            elif any(word in text_lower for word in ["excited", "thrilled"]):
                self.current_emotion = EmotionalStateEnum.EXCITED
                self.emotion_intensity = 0.9
            elif any(word in text_lower for word in ["confused", "uncertain", "unsure"]):
                self.current_emotion = EmotionalStateEnum.CONFUSED
                self.emotion_intensity = 0.5
            elif any(word in text_lower for word in ["curious", "interesting", "wonder"]):
                self.current_emotion = EmotionalStateEnum.CURIOUS
                self.emotion_intensity = 0.7
            
            # Add some randomness
            if self.random_state.random() < 0.1:  # 10% chance of random shift
                self.current_emotion = self.random_state.choice(list(EmotionalStateEnum))
                self.emotion_intensity = self.random_state.uniform(0.3, 0.8)
            
            return {
                "primary_emotion": self.current_emotion.emotion_name,
                "intensity": self.emotion_intensity,
                "uncertainty": self.uncertainty_level,
                "emotional_context": f"Feeling {self.current_emotion.emotion_name} with intensity {self.emotion_intensity:.2f}"
            }
    
    def get_emotional_state_summary(self) -> Dict[str, Any]:
        """Get current emotional state summary"""
        return {
            "current_emotion": self.current_emotion.emotion_name,
            "intensity": self.emotion_intensity,
            "uncertainty_level": self.uncertainty_level,
            "context_description": f"Currently feeling {self.current_emotion.emotion_name}"
        }

# ============================================================================
# GLOBAL INSTANCES AND API FUNCTIONS
# ============================================================================

# Global traditional emotion engine instance
emotion_engine = EmotionEngine()

# Global entropy-based emotional system instance
_emotional_system = None

def get_emotional_system() -> EmotionalEntropySystem:
    """Get global emotional entropy system instance (CRITICAL function)"""
    global _emotional_system
    if _emotional_system is None:
        _emotional_system = EmotionalEntropySystem()
    return _emotional_system

def process_emotional_context(text: str, context: str = "") -> Dict[str, Any]:
    """Convenience function to process emotional context"""
    return get_emotional_system().process_emotional_input(text, context)

def get_current_emotional_state() -> Dict[str, Any]:
    """Convenience function to get current emotional state"""
    return get_emotional_system().get_emotional_state_summary()

def inject_emotional_surprise(context: str = ""):
    """Convenience function to inject emotional surprise"""
    system = get_emotional_system()
    system.current_emotion = EmotionalStateEnum.SURPRISED
    system.emotion_intensity = 0.8
    system.uncertainty_level = min(1.0, system.uncertainty_level + 0.3)

# For backward compatibility
def reset_session_for_user_smart(user: str):
    """Reset emotional session for user (compatibility function)"""
    pass