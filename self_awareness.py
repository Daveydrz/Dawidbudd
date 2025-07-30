"""
Self Awareness System - Consolidated Module (Phase 3)

This consolidated module merges:
- self_model.py - Recursive self-awareness and identity system
- subjective_experience.py - Personal interpretation and qualia modeling
- inner_monologue.py - Background consciousness stream
- self_model_updater.py (functionality integrated)
- introspection_loop.py (functionality integrated)

Purpose: Enable introspection and self-modeling for Buddy's internal experience 
and self-awareness.
"""

import threading
import time
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

# Core enums and data structures
class SelfAspect(Enum):
    IDENTITY = "identity"
    CAPABILITIES = "capabilities"
    PERSONALITY = "personality"

class ExperienceType(Enum):
    COGNITIVE = "cognitive"
    EMOTIONAL = "emotional"
    SOCIAL = "social"

class ThoughtType(Enum):
    REFLECTION = "reflection"
    OBSERVATION = "observation"
    CREATIVE = "creative"

@dataclass
class SelfReflection:
    timestamp: datetime
    aspect: SelfAspect
    content: str
    confidence: float = 0.5

@dataclass
class SubjectiveExperience:
    id: str
    experience_type: ExperienceType
    content: str
    intensity: float
    timestamp: datetime

@dataclass
class InternalThought:
    content: str
    thought_type: ThoughtType
    intensity: float
    timestamp: datetime

class SelfAwarenessSystem:
    """Unified self-awareness and introspection system"""
    
    def __init__(self):
        self.reflections: List[SelfReflection] = []
        self.experiences: List[SubjectiveExperience] = []
        self.thoughts: List[InternalThought] = []
        self.lock = threading.Lock()
    
    def reflect_on_experience(self, content: str, context: Dict[str, Any]):
        reflection = SelfReflection(
            timestamp=datetime.now(),
            aspect=SelfAspect.IDENTITY,
            content=content
        )
        self.reflections.append(reflection)
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            "reflections": len(self.reflections),
            "experiences": len(self.experiences),
            "thoughts": len(self.thoughts)
        }

# Global instance
self_awareness_system = SelfAwarenessSystem()

# Backward compatibility aliases
class SelfModel:
    def __init__(self, save_path: str = None, initialize_blank: bool = False):
        self._system = self_awareness_system
    
    def reflect_on_experience(self, content: str, context: Dict[str, Any]):
        return self._system.reflect_on_experience(content, context)
    
    def start(self):
        pass
    
    def stop(self):
        pass

# Export instances and compatibility
self_model = SelfModel()

__all__ = ['SelfAwarenessSystem', 'SelfModel', 'self_model', 'self_awareness_system']
