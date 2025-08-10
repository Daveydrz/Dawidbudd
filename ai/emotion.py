"""
Unified Emotion System - Facade preserving original public API.

This facade maintains backward compatibility by importing key components
from the original emotion file and providing a clean interface.
"""

# Import the original comprehensive emotion system temporarily
# In a full refactoring, this would import from separated modules
from ai.emotion_modules.state import (
    EmotionType, MoodType, EmotionalState, EmotionalMemory, EmotionalPattern,
    create_basic_emotional_state
)

# Import from original file for full functionality preservation
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Import the complete emotion system from the original file
try:
    from ai.emotion_original import (
        EmotionEngine, EmotionalEntropySystem, 
        get_emotional_system, process_emotional_context,
        get_current_emotional_state, inject_emotional_surprise
    )
    
    # Create global instances exactly as in the original
    emotion_engine = EmotionEngine()
    
    print("[Emotion] ✅ Emotion system loaded with full functionality")
    
except ImportError as e:
    print(f"[Emotion] ⚠️ Using simplified emotion system: {e}")
    
    # Fallback minimal implementation
    class EmotionEngine:
        def __init__(self, save_path: str = "ai_emotions.json"):
            self.current_emotion = create_basic_emotional_state()
            
        def start(self):
            pass
            
        def stop(self):
            pass
            
        def process_emotional_trigger(self, trigger: str, context: dict = None):
            return self.current_emotion
            
        def get_current_state(self):
            return {"primary_emotion": "contentment", "intensity": 0.5}
    
    class EmotionalEntropySystem:
        def process_emotional_input(self, text: str, context: str = ""):
            return {"primary_emotion": "contentment", "intensity": 0.5}
            
        def get_emotional_state_summary(self):
            return {"emotion": "contentment", "intensity": 0.5}
    
    def get_emotional_system():
        return EmotionalEntropySystem()
    
    def process_emotional_context(text: str, context: str = ""):
        return {"primary_emotion": "contentment"}
    
    def get_current_emotional_state():
        return {"emotion": "contentment"}
    
    def inject_emotional_surprise(context: str = ""):
        pass
    
    emotion_engine = EmotionEngine()

# Preserve all original exports for backward compatibility
__all__ = [
    # Original emotion types and classes
    'EmotionType', 'MoodType', 'EmotionalState', 'EmotionalMemory', 'EmotionalPattern',
    'EmotionEngine',
    
    # Global instances (preserved for compatibility)
    'emotion_engine',
    
    # Entropy-based system API
    'EmotionalEntropySystem', 'get_emotional_system', 'process_emotional_context',
    'get_current_emotional_state', 'inject_emotional_surprise',
    
    # Helper functions
    'create_basic_emotional_state'
]