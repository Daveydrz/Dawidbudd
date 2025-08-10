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