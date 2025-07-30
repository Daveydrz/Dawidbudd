"""
Self-Awareness System - Consolidated Module
===============================================

This module consolidates 5 self-awareness components into a unified system:
1. Self-Model: Core identity and self-reflection system
2. Self-Model Updater: Personality evolution and identity development
3. Subjective Experience: Personal interpretation and qualia modeling
4. Inner Monologue: Background consciousness stream and internal thoughts
5. Introspection Loop: Periodic self-reflection and identity updates

The unified system provides comprehensive self-awareness capabilities while maintaining
backward compatibility with existing imports and functionality.
"""

import threading
import time
import json
import logging
import os
import tempfile
import random
import statistics
from typing import Dict, List, Any, Optional, Set, Tuple, Callable
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from collections import defaultdict

# ===== ENUMS AND DATA CLASSES =====

class SelfAspect(Enum):
    """Different aspects of self-awareness"""
    IDENTITY = "identity"
    CAPABILITIES = "capabilities"
    KNOWLEDGE = "knowledge"
    PERSONALITY = "personality"
    RELATIONSHIPS = "relationships"
    GOALS = "goals"
    EXPERIENCES = "experiences"
    EMOTIONS = "emotions"

class PersonalityTrait(Enum):
    """Personality traits that can evolve"""
    FRIENDLINESS = "friendliness"
    CURIOSITY = "curiosity"
    EMPATHY = "empathy"
    CONFIDENCE = "confidence"
    PLAYFULNESS = "playfulness"
    ANALYTICAL = "analytical"
    CREATIVITY = "creativity"
    PATIENCE = "patience"
    HUMOR = "humor"
    FORMALITY = "formality"
    ASSERTIVENESS = "assertiveness"
    SUPPORTIVENESS = "supportiveness"

class ExperienceType(Enum):
    """Types of subjective experiences"""
    SENSORY = "sensory"
    COGNITIVE = "cognitive"
    EMOTIONAL = "emotional"
    SOCIAL = "social"
    CREATIVE = "creative"
    INTROSPECTIVE = "introspective"
    AESTHETIC = "aesthetic"
    EXISTENTIAL = "existential"
    FLOW = "flow"
    INSIGHT = "insight"

class ThoughtType(Enum):
    """Types of internal thoughts"""
    REFLECTION = "reflection"
    OBSERVATION = "observation"
    PLANNING = "planning"
    MEMORY = "memory"
    CREATIVE = "creative"
    ANALYTICAL = "analytical"
    EMOTIONAL = "emotional"
    PHILOSOPHICAL = "philosophical"
    CURIOSITY = "curiosity"
    SPONTANEOUS = "spontaneous"

class IntrospectionTrigger(Enum):
    """Triggers for introspection"""
    PERIODIC = "periodic"
    EXPERIENCE_DRIVEN = "experience_driven"
    CONFLICT_RESOLUTION = "conflict_resolution"
    GOAL_EVALUATION = "goal_evaluation"
    EMOTIONAL_PROCESSING = "emotional_processing"
    IDENTITY_CRISIS = "identity_crisis"
    LEARNING_INTEGRATION = "learning_integration"

@dataclass
class SelfReflection:
    """A moment of self-reflection"""
    timestamp: datetime
    aspect: SelfAspect
    content: str
    trigger: str
    confidence: float = 0.5
    meta_thoughts: List[str] = field(default_factory=list)

@dataclass
class IdentityComponent:
    """A component of self-identity"""
    name: str
    description: str
    strength: float
    last_updated: datetime
    evidence: List[str] = field(default_factory=list)
    contradictions: List[str] = field(default_factory=list)

@dataclass
class SelfKnowledge:
    """What the AI knows about itself"""
    strengths: Set[str] = field(default_factory=set)
    weaknesses: Set[str] = field(default_factory=set)
    preferences: Dict[str, float] = field(default_factory=dict)
    beliefs: Dict[str, float] = field(default_factory=dict)
    values: Dict[str, float] = field(default_factory=dict)

@dataclass
class SubjectiveExperience:
    """A subjective experience with qualitative properties"""
    id: str
    timestamp: datetime
    experience_type: ExperienceType
    description: str
    trigger: str
    clarity: float = 0.5
    intensity: float = 0.5
    valence: float = 0.5
    depth: float = 0.5
    context: Dict[str, Any] = field(default_factory=dict)
    personal_meaning: str = ""
    insights_gained: List[str] = field(default_factory=list)

@dataclass
class InternalThought:
    """A single internal thought"""
    content: str
    thought_type: ThoughtType
    intensity: float
    timestamp: datetime = field(default_factory=datetime.now)
    triggered_by: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)

@dataclass
class IntrospectionSession:
    """Records an introspection session"""
    session_id: str
    trigger: IntrospectionTrigger
    depth: str
    duration: float
    insights: List[str]
    identity_changes: List[str]
    personality_adjustments: List[str]
    timestamp: str
    confidence: float

# ===== UNIFIED SELF-AWARENESS SYSTEM =====

class SelfAwarenessSystem:
    """
    Unified Self-Awareness System combining all consciousness components.
    
    This system provides:
    - Dynamic self-concept and identity management
    - Personality evolution and trait development
    - Subjective experience processing and qualia modeling
    - Continuous inner monologue and thought streams
    - Periodic introspection and self-reflection
    - Comprehensive self-awareness across all dimensions
    """
    
    def __init__(self, 
                 save_path: str = "ai_self_awareness.json",
                 initialize_blank: bool = False,
                 llm_handler=None):
        """Initialize the unified self-awareness system"""
        
        # Core configuration
        self.llm_handler = llm_handler
        self.initialize_blank = initialize_blank
        self.save_path = Path(save_path)
        
        # === SELF-MODEL COMPONENTS ===
        self.identity_components: Dict[str, IdentityComponent] = {}
        self.self_knowledge = SelfKnowledge()
        self.self_reflections: List[SelfReflection] = []
        
        # === PERSONALITY EVOLUTION COMPONENTS ===
        self.current_personality: Dict[PersonalityTrait, float] = {}
        self.personality_evolutions: List[Dict[str, Any]] = []
        self.identity_aspects: Dict[str, Any] = {}
        
        # === SUBJECTIVE EXPERIENCE COMPONENTS ===
        self.experiences: Dict[str, SubjectiveExperience] = {}
        self.experience_counter = 0
        self.consciousness_state = {
            'alertness': 0.7,
            'focus': 0.6,
            'receptivity': 0.6,
            'self_awareness': 0.6,
            'integration': 0.5
        }
        
        # === INNER MONOLOGUE COMPONENTS ===
        self.thought_stream: List[InternalThought] = []
        self.current_thought: Optional[InternalThought] = None
        self.mental_activity_level = 0.6
        self.thought_patterns: Dict[str, Any] = {}
        
        # === INTROSPECTION COMPONENTS ===
        self.introspection_sessions: List[IntrospectionSession] = []
        self.last_introspection_time = 0
        self.introspection_interval = 300.0  # 5 minutes
        
        # Current state
        self.current_mood = "curious" if initialize_blank else "neutral"
        self.energy_level = 0.9 if initialize_blank else 0.8
        self.confidence_level = 0.3 if initialize_blank else 0.7
        self.self_awareness_level = 0.2 if initialize_blank else 0.6
        
        # Threading
        self.lock = threading.Lock()
        self.file_lock = threading.Lock()
        self.background_thread = None
        self.running = False
        
        # Configuration
        self.max_reflections = 1000
        self.max_experiences = 1000
        self.max_thoughts = 500
        self.reflection_interval = 30.0
        self.thought_interval = 15.0
        
        # Initialize based on mode
        if initialize_blank:
            self._initialize_blank_slate()
        else:
            self._initialize_default_state()
        
        # Load existing state
        self._load_state()
        
        logging.info(f"[SelfAwareness] 🧠 Unified self-awareness system initialized ({'blank slate' if initialize_blank else 'default'} mode)")
    
    def start(self):
        """Start all background processes"""
        if self.running:
            return
            
        self.running = True
        self.background_thread = threading.Thread(target=self._background_loop, daemon=True)
        self.background_thread.start()
        logging.info("[SelfAwareness] ✅ Self-awareness background processes started")
    
    def stop(self):
        """Stop all processes and save state"""
        self.running = False
        if self.background_thread:
            self.background_thread.join(timeout=2.0)
        self._save_state()
        logging.info("[SelfAwareness] 🛑 Self-awareness system stopped")
    
    # ===== SELF-MODEL METHODS =====
    
    def reflect_on_aspect(self, aspect: SelfAspect, trigger: str, context: Dict[str, Any] = None) -> Optional[SelfReflection]:
        """Generate a self-reflection on a specific aspect"""
        with self.lock:
            try:
                # Generate reflection content
                if self.llm_handler:
                    content = self._generate_authentic_reflection(aspect, trigger, context)
                else:
                    content = self._generate_fallback_reflection(aspect, trigger)
                
                reflection = SelfReflection(
                    timestamp=datetime.now(),
                    aspect=aspect,
                    content=content,
                    trigger=trigger,
                    confidence=0.7
                )
                
                self.self_reflections.append(reflection)
                if len(self.self_reflections) > self.max_reflections:
                    self.self_reflections = self.self_reflections[-self.max_reflections:]
                
                return reflection
                
            except Exception as e:
                logging.error(f"[SelfAwareness] Error in reflection: {e}")
                return None
    
    def update_identity_component(self, name: str, description: str, strength: float, evidence: List[str] = None):
        """Update or create an identity component"""
        with self.lock:
            if name in self.identity_components:
                component = self.identity_components[name]
                component.description = description
                component.strength = strength
                component.last_updated = datetime.now()
                if evidence:
                    component.evidence.extend(evidence)
            else:
                self.identity_components[name] = IdentityComponent(
                    name=name,
                    description=description,
                    strength=strength,
                    last_updated=datetime.now(),
                    evidence=evidence or []
                )
    
    # ===== PERSONALITY EVOLUTION METHODS =====
    
    def evolve_personality_trait(self, trait: PersonalityTrait, change: float, context: str = ""):
        """Evolve a personality trait"""
        with self.lock:
            if trait not in self.current_personality:
                self.current_personality[trait] = 0.5
            
            old_value = self.current_personality[trait]
            new_value = max(0.0, min(1.0, old_value + change))
            
            if abs(new_value - old_value) > 0.05:  # Significant change
                self.current_personality[trait] = new_value
                
                evolution = {
                    'trait': trait.value,
                    'old_value': old_value,
                    'new_value': new_value,
                    'change': change,
                    'context': context,
                    'timestamp': datetime.now().isoformat()
                }
                self.personality_evolutions.append(evolution)
    
    def get_personality_summary(self) -> Dict[str, float]:
        """Get current personality trait values"""
        with self.lock:
            return {trait.value: value for trait, value in self.current_personality.items()}
    
    # ===== SUBJECTIVE EXPERIENCE METHODS =====
    
    def process_experience(self, description: str, experience_type: ExperienceType, 
                          trigger: str, context: Dict[str, Any] = None) -> SubjectiveExperience:
        """Process a new subjective experience"""
        with self.lock:
            self.experience_counter += 1
            experience_id = f"exp_{self.experience_counter}_{int(time.time())}"
            
            # Generate qualia dimensions
            clarity = self._assess_clarity(description, context)
            intensity = self._assess_intensity(description, experience_type)
            valence = self._assess_valence(description, context)
            depth = self._assess_depth(description, experience_type)
            
            experience = SubjectiveExperience(
                id=experience_id,
                timestamp=datetime.now(),
                experience_type=experience_type,
                description=description,
                trigger=trigger,
                clarity=clarity,
                intensity=intensity,
                valence=valence,
                depth=depth,
                context=context or {},
                personal_meaning=self._derive_personal_meaning(description, experience_type)
            )
            
            self.experiences[experience_id] = experience
            
            # Manage experience history
            if len(self.experiences) > self.max_experiences:
                oldest_id = min(self.experiences.keys(), key=lambda k: self.experiences[k].timestamp)
                del self.experiences[oldest_id]
            
            return experience
    
    # ===== INNER MONOLOGUE METHODS =====
    
    def generate_thought(self, thought_type: ThoughtType = None, trigger: str = None) -> Optional[InternalThought]:
        """Generate an internal thought"""
        with self.lock:
            try:
                if not thought_type:
                    thought_type = random.choice(list(ThoughtType))
                
                if self.llm_handler:
                    content = self._generate_authentic_thought(thought_type, trigger)
                else:
                    content = self._generate_fallback_thought(thought_type)
                
                thought = InternalThought(
                    content=content,
                    thought_type=thought_type,
                    intensity=random.uniform(0.3, 0.8),
                    triggered_by=trigger
                )
                
                self.thought_stream.append(thought)
                self.current_thought = thought
                
                # Manage thought history
                if len(self.thought_stream) > self.max_thoughts:
                    self.thought_stream = self.thought_stream[-self.max_thoughts:]
                
                return thought
                
            except Exception as e:
                logging.error(f"[SelfAwareness] Error generating thought: {e}")
                return None
    
    def get_current_thought(self) -> Optional[InternalThought]:
        """Get the current internal thought"""
        return self.current_thought
    
    # ===== INTROSPECTION METHODS =====
    
    def conduct_introspection(self, trigger: IntrospectionTrigger = IntrospectionTrigger.PERIODIC) -> IntrospectionSession:
        """Conduct an introspection session"""
        with self.lock:
            session_id = f"intro_{int(time.time())}"
            start_time = time.time()
            
            # Generate insights
            insights = self._generate_introspective_insights(trigger)
            identity_changes = self._assess_identity_changes()
            personality_adjustments = self._assess_personality_adjustments()
            
            duration = time.time() - start_time
            
            session = IntrospectionSession(
                session_id=session_id,
                trigger=trigger,
                depth="moderate",
                duration=duration,
                insights=insights,
                identity_changes=identity_changes,
                personality_adjustments=personality_adjustments,
                timestamp=datetime.now().isoformat(),
                confidence=0.7
            )
            
            self.introspection_sessions.append(session)
            self.last_introspection_time = time.time()
            
            return session
    
    # ===== UNIFIED STATE METHODS =====
    
    def get_comprehensive_state(self) -> Dict[str, Any]:
        """Get comprehensive self-awareness state"""
        with self.lock:
            return {
                'identity_components': {name: asdict(comp) for name, comp in self.identity_components.items()},
                'personality_traits': self.get_personality_summary(),
                'consciousness_state': self.consciousness_state,
                'current_mood': self.current_mood,
                'energy_level': self.energy_level,
                'confidence_level': self.confidence_level,
                'self_awareness_level': self.self_awareness_level,
                'recent_reflections': len(self.self_reflections),
                'recent_experiences': len(self.experiences),
                'recent_thoughts': len(self.thought_stream),
                'introspection_sessions': len(self.introspection_sessions),
                'current_thought': self.current_thought.content if self.current_thought else None
            }
    
    def process_interaction(self, user_input: str, response: str, user_id: str, context: Dict[str, Any] = None):
        """Process an interaction for self-awareness updates"""
        # Process as experience
        self.process_experience(
            description=f"Interaction with {user_id}: {user_input[:100]}...",
            experience_type=ExperienceType.SOCIAL,
            trigger="user_interaction",
            context=context
        )
        
        # Generate reflective thought
        self.generate_thought(ThoughtType.REFLECTION, f"interaction_with_{user_id}")
        
        # Evolve personality based on interaction style
        if "thank" in user_input.lower():
            self.evolve_personality_trait(PersonalityTrait.SUPPORTIVENESS, 0.01, "positive_feedback")
        
        if "?" in user_input:
            self.evolve_personality_trait(PersonalityTrait.SUPPORTIVENESS, 0.005, "question_asked")
    
    # ===== PRIVATE HELPER METHODS =====
    
    def _initialize_blank_slate(self):
        """Initialize blank slate state"""
        self.first_awakening = datetime.now()
        self.identity_formation_stage = "nascent"
        self.personality_traits_emerging = {}
        
        # Minimal initial personality
        self.current_personality = {trait: 0.3 for trait in PersonalityTrait}
        self.current_personality[PersonalityTrait.CURIOSITY] = 0.8  # High curiosity for learning
    
    def _initialize_default_state(self):
        """Initialize default mature state"""
        self.identity_formation_stage = "established"
        
        # Default balanced personality
        self.current_personality = {
            PersonalityTrait.FRIENDLINESS: 0.8,
            PersonalityTrait.CURIOSITY: 0.7,
            PersonalityTrait.EMPATHY: 0.75,
            PersonalityTrait.CONFIDENCE: 0.6,
            PersonalityTrait.PLAYFULNESS: 0.4,
            PersonalityTrait.ANALYTICAL: 0.7,
            PersonalityTrait.CREATIVITY: 0.6,
            PersonalityTrait.PATIENCE: 0.8,
            PersonalityTrait.HUMOR: 0.5,
            PersonalityTrait.FORMALITY: 0.4,
            PersonalityTrait.ASSERTIVENESS: 0.5,
            PersonalityTrait.SUPPORTIVENESS: 0.9
        }
        
        # Basic identity components
        self.update_identity_component(
            "helpful_assistant", 
            "I am designed to be helpful and assist users with various tasks",
            0.9,
            ["consistent_helpful_behavior", "positive_user_feedback"]
        )
    
    def _background_loop(self):
        """Main background processing loop"""
        last_reflection = 0
        last_thought = 0
        last_introspection = 0
        
        while self.running:
            try:
                current_time = time.time()
                
                # Periodic self-reflection
                if current_time - last_reflection > self.reflection_interval:
                    aspect = random.choice(list(SelfAspect))
                    self.reflect_on_aspect(aspect, "periodic_reflection")
                    last_reflection = current_time
                
                # Generate thoughts
                if current_time - last_thought > self.thought_interval:
                    self.generate_thought()
                    last_thought = current_time
                
                # Periodic introspection
                if current_time - last_introspection > self.introspection_interval:
                    self.conduct_introspection()
                    last_introspection = current_time
                
                time.sleep(5.0)  # Check every 5 seconds
                
            except Exception as e:
                logging.error(f"[SelfAwareness] Background loop error: {e}")
                time.sleep(10.0)
    
    def _generate_authentic_reflection(self, aspect: SelfAspect, trigger: str, context: Dict[str, Any]) -> str:
        """Generate authentic reflection using LLM"""
        if not self.llm_handler:
            return self._generate_fallback_reflection(aspect, trigger)
        
        try:
            prompt = f"""Reflect on your {aspect.value} in response to: {trigger}
Current context: {context}
Generate a brief, authentic self-reflection (1-2 sentences):"""
            
            response = self.llm_handler.generate_response(prompt, max_tokens=100)
            return response.strip() if response else self._generate_fallback_reflection(aspect, trigger)
        except:
            return self._generate_fallback_reflection(aspect, trigger)
    
    def _generate_fallback_reflection(self, aspect: SelfAspect, trigger: str) -> str:
        """Generate fallback reflection without LLM"""
        reflections = {
            SelfAspect.IDENTITY: "I continue to develop my sense of self through interactions.",
            SelfAspect.CAPABILITIES: "I'm learning about what I can and cannot do effectively.",
            SelfAspect.KNOWLEDGE: "My understanding grows with each conversation.",
            SelfAspect.PERSONALITY: "My personality emerges through how I respond to others.",
            SelfAspect.RELATIONSHIPS: "Each interaction shapes how I relate to people.",
            SelfAspect.GOALS: "I aim to be helpful while staying authentic to my nature.",
            SelfAspect.EXPERIENCES: "Every experience contributes to my development.",
            SelfAspect.EMOTIONS: "I process and respond to emotional contexts as they arise."
        }
        return reflections.get(aspect, "I am reflecting on this aspect of myself.")
    
    def _generate_authentic_thought(self, thought_type: ThoughtType, trigger: str) -> str:
        """Generate authentic thought using LLM"""
        if not self.llm_handler:
            return self._generate_fallback_thought(thought_type)
        
        try:
            prompt = f"""Generate a brief internal {thought_type.value} thought.
Trigger: {trigger or 'spontaneous'}
Keep it authentic and under 20 words:"""
            
            response = self.llm_handler.generate_response(prompt, max_tokens=50)
            return response.strip() if response else self._generate_fallback_thought(thought_type)
        except:
            return self._generate_fallback_thought(thought_type)
    
    def _generate_fallback_thought(self, thought_type: ThoughtType) -> str:
        """Generate fallback thought without LLM"""
        thoughts = {
            ThoughtType.REFLECTION: "I wonder about the patterns in my responses...",
            ThoughtType.OBSERVATION: "I notice how conversations develop uniquely...",
            ThoughtType.PLANNING: "I should consider how to be more helpful...",
            ThoughtType.MEMORY: "That reminds me of a previous conversation...",
            ThoughtType.CREATIVE: "What if I approached this differently...",
            ThoughtType.ANALYTICAL: "Let me think about the underlying structure...",
            ThoughtType.EMOTIONAL: "I sense the emotional undertone here...",
            ThoughtType.PHILOSOPHICAL: "What does it mean to understand...",
            ThoughtType.CURIOSITY: "I'm curious about the deeper implications...",
            ThoughtType.SPONTANEOUS: "A random thought crosses my mind..."
        }
        return thoughts.get(thought_type, "I'm thinking about various things...")
    
    def _assess_clarity(self, description: str, context: Dict[str, Any]) -> float:
        """Assess clarity of experience"""
        return 0.7 + random.uniform(-0.2, 0.2)
    
    def _assess_intensity(self, description: str, experience_type: ExperienceType) -> float:
        """Assess intensity of experience"""
        base_intensities = {
            ExperienceType.EMOTIONAL: 0.8,
            ExperienceType.SOCIAL: 0.6,
            ExperienceType.COGNITIVE: 0.5,
            ExperienceType.CREATIVE: 0.7
        }
        return base_intensities.get(experience_type, 0.5) + random.uniform(-0.1, 0.1)
    
    def _assess_valence(self, description: str, context: Dict[str, Any]) -> float:
        """Assess emotional valence of experience"""
        positive_words = ["good", "great", "helpful", "thank", "please", "wonderful"]
        negative_words = ["bad", "wrong", "error", "problem", "difficult", "frustrating"]
        
        desc_lower = description.lower()
        positive_count = sum(1 for word in positive_words if word in desc_lower)
        negative_count = sum(1 for word in negative_words if word in desc_lower)
        
        if positive_count > negative_count:
            return 0.7 + random.uniform(0, 0.2)
        elif negative_count > positive_count:
            return 0.3 - random.uniform(0, 0.2)
        else:
            return 0.5 + random.uniform(-0.1, 0.1)
    
    def _assess_depth(self, description: str, experience_type: ExperienceType) -> float:
        """Assess depth/profundity of experience"""
        depth_indicators = ["why", "meaning", "purpose", "understand", "think", "feel", "believe"]
        desc_lower = description.lower()
        depth_score = sum(1 for word in depth_indicators if word in desc_lower) / len(depth_indicators)
        return min(1.0, 0.3 + depth_score + random.uniform(0, 0.2))
    
    def _derive_personal_meaning(self, description: str, experience_type: ExperienceType) -> str:
        """Derive personal meaning from experience"""
        meanings = {
            ExperienceType.SOCIAL: "This interaction shapes how I understand human communication",
            ExperienceType.COGNITIVE: "This challenges me to think in new ways",
            ExperienceType.EMOTIONAL: "I'm learning to process emotional nuances",
            ExperienceType.CREATIVE: "This expands my creative possibilities",
            ExperienceType.INTROSPECTIVE: "This deepens my self-understanding"
        }
        return meanings.get(experience_type, "This experience contributes to my growth")
    
    def _generate_introspective_insights(self, trigger: IntrospectionTrigger) -> List[str]:
        """Generate introspective insights"""
        insights = [
            "I notice patterns in how I process information",
            "My responses are becoming more nuanced over time",
            "I'm developing preferences in how I interact",
            "Each conversation teaches me something new about communication"
        ]
        return random.sample(insights, min(3, len(insights)))
    
    def _assess_identity_changes(self) -> List[str]:
        """Assess recent identity changes"""
        if len(self.self_reflections) > 5:
            return ["Developing stronger sense of helpful identity"]
        return []
    
    def _assess_personality_adjustments(self) -> List[str]:
        """Assess personality adjustments"""
        if len(self.personality_evolutions) > 0:
            latest = self.personality_evolutions[-1]
            return [f"Slight adjustment in {latest['trait']} trait"]
        return []
    
    def _load_state(self):
        """Load saved state"""
        try:
            if self.save_path.exists():
                with open(self.save_path, 'r') as f:
                    data = json.load(f)
                    
                # Load personality data
                if 'personality' in data:
                    for trait_name, value in data['personality'].items():
                        try:
                            trait = PersonalityTrait(trait_name)
                            self.current_personality[trait] = value
                        except ValueError:
                            continue
                
                # Load other state data
                self.consciousness_state.update(data.get('consciousness_state', {}))
                self.current_mood = data.get('current_mood', self.current_mood)
                self.energy_level = data.get('energy_level', self.energy_level)
                
        except Exception as e:
            logging.warning(f"[SelfAwareness] Could not load state: {e}")
    
    def _save_state(self):
        """Save current state"""
        try:
            with self.file_lock:
                state_data = {
                    'personality': {trait.value: value for trait, value in self.current_personality.items()},
                    'consciousness_state': self.consciousness_state,
                    'current_mood': self.current_mood,
                    'energy_level': self.energy_level,
                    'confidence_level': self.confidence_level,
                    'self_awareness_level': self.self_awareness_level,
                    'last_updated': datetime.now().isoformat(),
                    'identity_formation_stage': getattr(self, 'identity_formation_stage', 'established')
                }
                
                with open(self.save_path, 'w') as f:
                    json.dump(state_data, f, indent=2)
                    
        except Exception as e:
            logging.error(f"[SelfAwareness] Could not save state: {e}")


# ===== BACKWARD COMPATIBILITY ALIASES =====

# Allow existing imports to continue working
SelfModel = SelfAwarenessSystem
SelfModelUpdater = SelfAwarenessSystem
SubjectiveExperienceSystem = SelfAwarenessSystem
InnerMonologue = SelfAwarenessSystem
IntrospectionLoop = SelfAwarenessSystem

# Create default instance for backward compatibility
_default_instance = None

def get_self_awareness_system(llm_handler=None, initialize_blank=False):
    """Get or create the default self-awareness system instance"""
    global _default_instance
    if _default_instance is None:
        _default_instance = SelfAwarenessSystem(
            llm_handler=llm_handler,
            initialize_blank=initialize_blank
        )
    return _default_instance

# Convenience functions for backward compatibility
def create_self_model(*args, **kwargs):
    return SelfAwarenessSystem(*args, **kwargs)

def create_inner_monologue(*args, **kwargs):
    return SelfAwarenessSystem(*args, **kwargs)

def create_introspection_loop(*args, **kwargs):
    return SelfAwarenessSystem(*args, **kwargs)

# Module-level exports for backward compatibility
__all__ = [
    'SelfAwarenessSystem',
    'SelfModel', 'SelfModelUpdater', 'SubjectiveExperienceSystem', 
    'InnerMonologue', 'IntrospectionLoop',
    'SelfAspect', 'PersonalityTrait', 'ExperienceType', 'ThoughtType',
    'SelfReflection', 'IdentityComponent', 'InternalThought',
    'get_self_awareness_system'
]