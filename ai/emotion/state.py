"""
Emotion state definitions - EmotionType, MoodType, and data structures.

This module contains all the emotional state dataclasses, enums, and lightweight 
data structures used across the emotion system modules.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


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
    NEUTRAL = "neutral"


class MoodType(Enum):
    """Overall mood states"""
    VERY_POSITIVE = "very_positive"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    VERY_NEGATIVE = "very_negative"


@dataclass
class EmotionalState:
    """Current emotional state for emotion engine"""
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


@dataclass
class EmotionalResponse:
    """Response from emotional processing"""
    primary_emotion: EmotionType
    intensity: float
    arousal_change: float
    valence_change: float
    suggested_modulations: Dict[str, float]
    timestamp: datetime = field(default_factory=datetime.now)


# Advanced emotional state structures (from entropy system)

class AdvancedEmotionType(Enum):
    """Extended emotion types for entropy-based system"""
    # Basic emotions
    CONTENTMENT = "contentment"
    CURIOSITY = "curiosity"
    UNCERTAINTY = "uncertainty"
    CONFUSION = "confusion"
    
    # Weather-influenced emotions
    MELANCHOLY = "melancholy"
    COZY = "cozy"
    RESTLESS = "restless"
    ENERGETIC = "energetic"
    CONTEMPLATIVE = "contemplative"
    
    # Complex emotional states
    NOSTALGIC = "nostalgic"
    WHIMSICAL = "whimsical"
    REFLECTIVE = "reflective"
    ANTICIPATORY = "anticipatory"
    BITTERSWEET = "bittersweet"


class WeatherMood(Enum):
    """Weather-influenced mood patterns"""
    SUNNY_OPTIMISTIC = "sunny_optimistic"
    RAINY_MELANCHOLY = "rainy_melancholy" 
    CLOUDY_CONTEMPLATIVE = "cloudy_contemplative"
    STORMY_INTENSE = "stormy_intense"
    FOGGY_MYSTERIOUS = "foggy_mysterious"
    CLEAR_FOCUSED = "clear_focused"


@dataclass
class AdvancedEmotionalState:
    """Advanced emotional state with entropy and weather awareness"""
    primary_emotion: AdvancedEmotionType
    secondary_emotions: List[AdvancedEmotionType] = field(default_factory=list)
    intensity: float = 0.5
    uncertainty_level: float = 0.0
    weather_influence: Optional[WeatherMood] = None
    consciousness_level: float = 0.8
    temporal_context: Dict[str, Any] = field(default_factory=dict)
    entropy_state: Dict[str, float] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class WeatherEmotionalInfluence:
    """How weather affects emotional state"""
    weather_condition: str
    temperature: float
    humidity: float
    pressure: float
    emotional_modifier: Dict[str, float]  # emotion -> intensity modifier
    mood_tendency: WeatherMood
    consciousness_effect: float  # -1.0 to 1.0
    

# Helper functions for emotion compatibility

def convert_to_basic_emotion(advanced_emotion: AdvancedEmotionType) -> EmotionType:
    """Convert advanced emotion type to basic emotion type"""
    mapping = {
        AdvancedEmotionType.CONTENTMENT: EmotionType.CONTENTMENT,
        AdvancedEmotionType.CURIOSITY: EmotionType.CURIOSITY,
        AdvancedEmotionType.UNCERTAINTY: EmotionType.FEAR,  
        AdvancedEmotionType.CONFUSION: EmotionType.SURPRISE,
        AdvancedEmotionType.MELANCHOLY: EmotionType.SADNESS,
        AdvancedEmotionType.COZY: EmotionType.CALM,
        AdvancedEmotionType.RESTLESS: EmotionType.ANTICIPATION,
        AdvancedEmotionType.ENERGETIC: EmotionType.EXCITEMENT,
        AdvancedEmotionType.CONTEMPLATIVE: EmotionType.CALM,
        AdvancedEmotionType.NOSTALGIC: EmotionType.SADNESS,
        AdvancedEmotionType.WHIMSICAL: EmotionType.JOY,
        AdvancedEmotionType.REFLECTIVE: EmotionType.CALM,
        AdvancedEmotionType.ANTICIPATORY: EmotionType.ANTICIPATION,
        AdvancedEmotionType.BITTERSWEET: EmotionType.SADNESS,
    }
    return mapping.get(advanced_emotion, EmotionType.NEUTRAL)


def create_basic_emotional_state(
    emotion: str = "contentment",
    intensity: float = 0.5,
    arousal: float = 0.5,
    valence: float = 0.3
) -> EmotionalState:
    """Create a basic emotional state with enum conversion"""
    emotion_enum = EmotionType(emotion.lower()) if emotion.lower() in [e.value for e in EmotionType] else EmotionType.NEUTRAL
    
    return EmotionalState(
        primary_emotion=emotion_enum,
        intensity=max(0.0, min(1.0, intensity)),
        arousal=max(0.0, min(1.0, arousal)),
        valence=max(-1.0, min(1.0, valence))
    )


def create_advanced_emotional_state(
    emotion: str = "contentment",
    intensity: float = 0.5,
    uncertainty: float = 0.0
) -> AdvancedEmotionalState:
    """Create an advanced emotional state with enum conversion"""
    emotion_enum = (AdvancedEmotionType(emotion.lower()) 
                   if emotion.lower() in [e.value for e in AdvancedEmotionType]
                   else AdvancedEmotionType.CONTENTMENT)
    
    return AdvancedEmotionalState(
        primary_emotion=emotion_enum,
        intensity=max(0.0, min(1.0, intensity)),
        uncertainty_level=max(0.0, min(1.0, uncertainty))
    )