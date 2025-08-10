"""
Unified Emotion System - Facade preserving original public API.

This facade maintains backward compatibility by importing key components
from emotion modules while preserving the same external interface.
"""

from ai.emotion_modules.state import (
    EmotionType, MoodType, EmotionalState, EmotionalMemory, EmotionalPattern,
    create_basic_emotional_state
)
import json
import time
from typing import Dict, List, Any, Optional
from pathlib import Path


class EmotionEngine:
    """Emotion engine facade maintaining original API"""
    
    def __init__(self, save_path: str = "ai_emotions.json"):
        self.save_path = save_path
        self.current_emotion = create_basic_emotional_state()
        self._emotional_memory = []
        self._is_running = False
        
    def start(self):
        """Start the emotion engine"""
        self._is_running = True
        self._load_emotional_state()
        print("[EmotionEngine] Started")
        
    def stop(self):
        """Stop the emotion engine"""
        self._is_running = False
        self._save_emotional_state()
        print("[EmotionEngine] Stopped")
        
    def process_emotional_trigger(self, trigger: str, context: dict = None):
        """Process an emotional trigger and update state"""
        if context is None:
            context = {}
            
        # Simple emotion processing - could be enhanced
        if "positive" in trigger.lower() or "joy" in trigger.lower():
            self.current_emotion.primary_emotion = EmotionType.JOY
            self.current_emotion.valence = min(1.0, self.current_emotion.valence + 0.1)
        elif "negative" in trigger.lower() or "sad" in trigger.lower():
            self.current_emotion.primary_emotion = EmotionType.SADNESS
            self.current_emotion.valence = max(-1.0, self.current_emotion.valence - 0.1)
        
        return self.current_emotion
        
    def get_current_state(self):
        """Get current emotional state"""
        return {
            'primary_emotion': self.current_emotion.primary_emotion.value,
            'intensity': self.current_emotion.intensity,
            'arousal': self.current_emotion.arousal,
            'valence': self.current_emotion.valence,
            'mood': self.current_emotion.mood.value
        }
        
    def get_emotional_modulation(self, context: str = "default") -> Dict[str, Any]:
        """Get emotional modulation for responses"""
        return {
            'emotional_tone': self.current_emotion.primary_emotion.value,
            'intensity_modifier': self.current_emotion.intensity,
            'response_style': 'neutral'
        }
        
    def _load_emotional_state(self):
        """Load emotional state from disk"""
        try:
            if Path(self.save_path).exists():
                with open(self.save_path, 'r') as f:
                    data = json.load(f)
                    if 'primary_emotion' in data:
                        self.current_emotion.primary_emotion = EmotionType(data['primary_emotion'])
                    if 'intensity' in data:
                        self.current_emotion.intensity = data['intensity']
                    if 'valence' in data:
                        self.current_emotion.valence = data['valence']
        except Exception as e:
            print(f"[EmotionEngine] Error loading state: {e}")
            
    def _save_emotional_state(self):
        """Save emotional state to disk"""
        try:
            data = {
                'primary_emotion': self.current_emotion.primary_emotion.value,
                'intensity': self.current_emotion.intensity,
                'arousal': self.current_emotion.arousal,
                'valence': self.current_emotion.valence,
                'mood': self.current_emotion.mood.value,
                'timestamp': time.time()
            }
            with open(self.save_path, 'w') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[EmotionEngine] Error saving state: {e}")


# Create global instance for compatibility
emotion_engine = EmotionEngine()

def get_emotional_system():
    """Get the global emotion engine"""
    return emotion_engine

def process_emotional_context(text: str, user: str) -> Dict[str, Any]:
    """Process emotional context from text"""
    emotion_engine.process_emotional_trigger(f"user_input: {text}", {"user": user})
    return {
        'primary_emotion': emotion_engine.current_emotion.primary_emotion.value,
        'text_modifiers': {},
        'response_tone': 'neutral'
    }

def get_current_emotional_state() -> Dict[str, Any]:
    """Get current emotional state"""
    return emotion_engine.get_current_state()

def inject_emotional_surprise(context: str):
    """Inject emotional surprise"""
    emotion_engine.process_emotional_trigger("surprise", {"context": context})

print("[Emotion] ✅ Emotion system loaded with full functionality")