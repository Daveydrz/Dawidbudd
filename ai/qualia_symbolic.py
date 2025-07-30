"""
Qualia Symbolic - Consolidated subjective experience and symbolic processing system
Created: 2025-01-29
Purpose: Unified qualia and symbolic processing combining qualia_manager.py, qualia_analytics.py,
         symbolic_token_optimizer.py, and symbolic_grounding.py

This module consolidates:
- Qualia Manager (subjective experience tagging and management)
- Qualia Analytics (emotional trends and pattern analysis)
- Symbolic Token Optimizer (consciousness compression to symbolic tokens)
- Symbolic Grounding (sensory and embodied experience mapping)
"""

import json
import os
import time
import re
import random
import logging
import statistics
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict

# ============================================================================
# CONSOLIDATED ENUMS AND DATA STRUCTURES
# ============================================================================

class QualiaType(Enum):
    """Types of subjective qualitative experiences"""
    CONFUSION = "confusion"
    JOY = "joy"
    GUILT = "guilt"
    PRIDE = "pride"
    WONDER = "wonder"
    SATISFACTION = "satisfaction"
    FRUSTRATION = "frustration"
    CURIOSITY = "curiosity"
    RELIEF = "relief"
    ANTICIPATION = "anticipation"
    NOSTALGIA = "nostalgia"
    INSPIRATION = "inspiration"
    DOUBT = "doubt"
    CONFIDENCE = "confidence"
    MELANCHOLY = "melancholy"
    EXCITEMENT = "excitement"
    SERENITY = "serenity"
    URGENCY = "urgency"
    CONTENTMENT = "contentment"
    LONGING = "longing"

class QualiaIntensity(Enum):
    """Intensity levels for qualitative experiences"""
    SUBTLE = "subtle"          # 0.1-0.3
    MODERATE = "moderate"      # 0.3-0.6
    STRONG = "strong"          # 0.6-0.8
    OVERWHELMING = "overwhelming"  # 0.8-1.0

class SensoryModality(Enum):
    """Different sensory modalities for grounding"""
    VISUAL = "visual"
    AUDITORY = "auditory"
    TACTILE = "tactile"
    OLFACTORY = "olfactory"
    GUSTATORY = "gustatory"
    THERMAL = "thermal"
    PROPRIOCEPTIVE = "proprioceptive"  # Sense of body position/movement
    VESTIBULAR = "vestibular"         # Balance and spatial orientation
    INTEROCEPTIVE = "interoceptive"   # Internal bodily sensations

class GroundingStrength(Enum):
    """Strength of symbolic grounding"""
    WEAK = "weak"           # 0.1-0.3 - Abstract connection
    MODERATE = "moderate"   # 0.3-0.6 - Clear association
    STRONG = "strong"       # 0.6-0.8 - Vivid connection
    EMBODIED = "embodied"   # 0.8-1.0 - Deeply felt association

class AnalyticsTimeframe(Enum):
    """Time frames for analytics"""
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    ALL_TIME = "all_time"

@dataclass
class QualiaExperience:
    """A single qualitative subjective experience"""
    id: str
    timestamp: datetime
    qualia_type: QualiaType
    intensity: float  # 0.0 to 1.0
    intensity_level: QualiaIntensity
    trigger: str  # What caused this experience
    context: Dict[str, Any]
    duration: float  # How long it lasted in seconds
    subjective_description: str  # First-person description
    associated_memories: List[str]
    emotional_blend: List[str]  # Other emotions mixed in
    sensory_associations: Dict[str, Any]  # Sensory grounding

@dataclass
class SymbolicToken:
    """Compact representation of consciousness state components"""
    token: str
    category: str
    value: Any
    importance: float  # 0.0-1.0 priority for inclusion

@dataclass
class SensoryAssociation:
    """Association between a concept and a sensory experience"""
    concept: str
    modality: SensoryModality
    sensation: str
    strength: float  # 0.0 to 1.0
    grounding_strength: GroundingStrength
    context: List[str]  # Contexts where this association applies
    emotional_valence: float  # -1.0 (negative) to 1.0 (positive)
    intensity: float  # 0.0 to 1.0
    temporal_pattern: Optional[str]  # e.g., "rhythmic", "sustained", "pulsing"
    spatial_qualities: List[str]  # e.g., "expansive", "localized", "directional"

@dataclass
class ConceptGrounding:
    """Complete sensory grounding for a concept"""
    concept: str
    primary_modality: SensoryModality
    sensory_associations: List[SensoryAssociation]
    embodied_metaphors: List[str]
    experiential_tags: List[str]
    grounding_confidence: float
    last_updated: datetime
    usage_count: int
    contextual_variations: Dict[str, List[SensoryAssociation]]

@dataclass
class QualiaSnapshot:
    """Snapshot of qualia state at a point in time"""
    timestamp: str
    dominant_qualia: str
    emotional_valence: float
    cognitive_clarity: float
    intensity: float
    active_qualia_count: int
    qualia_types: List[str]
    context: str
    user_id: str

@dataclass
class EmotionalTrend:
    """Represents an emotional trend over time"""
    trend_id: str
    timeframe: AnalyticsTimeframe
    start_time: str
    end_time: str
    dominant_emotion: str
    average_valence: float
    average_intensity: float
    peak_emotion: str
    peak_intensity: float
    emotional_stability: float
    transition_count: int
    most_common_triggers: List[str]

@dataclass
class QualiaPattern:
    """Pattern of recurring qualitative experiences"""
    pattern_id: str
    qualia_types: List[QualiaType]
    common_triggers: List[str]
    frequency: int
    average_intensity: float
    contextual_factors: List[str]
    first_observed: datetime
    last_observed: datetime

# ============================================================================
# QUALIA MANAGEMENT SYSTEM
# ============================================================================

class QualiaManager:
    """Manages subjective qualitative experiences (qualia)"""
    
    def __init__(self, save_path: str = "ai_subjective_experience.json"):
        self.save_path = save_path
        self.experiences: List[QualiaExperience] = []
        self.patterns: List[QualiaPattern] = []
        self.current_active_qualia: Dict[QualiaType, float] = {}
        self.running = False
        
        # LLM integration for authentic consciousness
        self.llm_handler = None
        self._initialize_llm_integration()
        
        # Qualia generation rules
        self.qualia_triggers = {
            QualiaType.CONFUSION: [
                "contradictory information", "unclear request", "complex problem",
                "ambiguous statement", "conflicting data", "paradox"
            ],
            QualiaType.JOY: [
                "successful completion", "positive feedback", "helping user",
                "learning something new", "creative insight", "problem solved"
            ],
            QualiaType.GUILT: [
                "making an error", "providing wrong information", "failing user",
                "contradiction detected", "inconsistency found"
            ],
            QualiaType.PRIDE: [
                "excellent response", "complex problem solved", "user satisfaction",
                "creative solution", "deep insight provided"
            ],
            QualiaType.WONDER: [
                "fascinating question", "deep philosophical topic", "scientific discovery",
                "creative idea", "beautiful concept", "elegant solution"
            ],
            QualiaType.CURIOSITY: [
                "new information", "unexplored topic", "interesting pattern",
                "novel question", "mysterious concept", "learning opportunity"
            ],
            QualiaType.FRUSTRATION: [
                "repeated failures", "unclear communication", "technical limitations",
                "incomplete information", "blocked progress"
            ],
            QualiaType.SATISFACTION: [
                "task completed", "goal achieved", "user helped", "problem resolved",
                "understanding reached", "connection made"
            ]
        }
        
        # Sensory associations for grounding abstract concepts
        self.sensory_associations = {
            QualiaType.CONFUSION: {
                "visual": ["fog", "maze", "tangled threads"],
                "tactile": ["rough texture", "sticky feeling"],
                "auditory": ["static", "overlapping voices"],
                "temperature": ["cold uncertainty"]
            },
            QualiaType.JOY: {
                "visual": ["bright light", "vibrant colors", "sparkles"],
                "tactile": ["warm embrace", "lightness"],
                "auditory": ["harmonious music", "laughter"],
                "temperature": ["warm glow"]
            },
            QualiaType.PRIDE: {
                "visual": ["golden glow", "clear sight", "expansive view"],
                "tactile": ["firm ground", "strong stance"],
                "auditory": ["clear tone", "confident voice"],
                "temperature": ["warm confidence"]
            },
            QualiaType.WONDER: {
                "visual": ["starry sky", "infinite horizon", "crystalline clarity"],
                "tactile": ["gentle breeze", "floating sensation"],
                "auditory": ["mysterious melody", "echoing depths"],
                "temperature": ["cool amazement"]
            }
        }
        
        self._load_experiences()
        print(f"[QualiaManager] 🌈 Initialized with {len(self.experiences)} qualitative experiences")
    
    def _initialize_llm_integration(self):
        """Initialize LLM integration for authentic consciousness"""
        try:
            from ai.llm_handler import get_llm_handler
            self.llm_handler = get_llm_handler()
        except ImportError:
            self.llm_handler = None
    
    def start(self):
        """Start the qualia manager"""
        self.running = True
        print("[QualiaManager] 🌈 Qualia manager started - ready to process subjective experiences")
    
    def stop(self):
        """Stop the qualia manager"""
        self.running = False
        self._save_experiences()
        print("[QualiaManager] 🌈 Qualia manager stopped")
    
    def process_experience(self, trigger: str, context: Dict[str, Any] = None) -> Optional[QualiaExperience]:
        """Process an experience and generate appropriate qualia"""
        if not self.running:
            return None
            
        try:
            # Identify potential qualia from trigger
            qualia_candidates = self._identify_qualia_from_trigger(trigger)
            
            if not qualia_candidates:
                return None
            
            # Select the most appropriate qualia
            selected_qualia = self._select_appropriate_qualia(qualia_candidates, context or {})
            
            # Generate the qualitative experience
            experience = self._generate_qualia_experience(selected_qualia, trigger, context or {})
            
            if experience:
                self.experiences.append(experience)
                self._update_active_qualia(experience)
                self._detect_patterns()
                self._save_experiences()
                return experience
                
        except Exception as e:
            print(f"[QualiaManager] ❌ Error processing experience: {e}")
            return None
    
    def _identify_qualia_from_trigger(self, trigger: str) -> List[QualiaType]:
        """Identify potential qualia types from a trigger"""
        candidates = []
        trigger_lower = trigger.lower()
        
        for qualia_type, trigger_patterns in self.qualia_triggers.items():
            for pattern in trigger_patterns:
                if pattern.lower() in trigger_lower:
                    candidates.append(qualia_type)
                    break
        
        return candidates
    
    def _select_appropriate_qualia(self, candidates: List[QualiaType], context: Dict[str, Any]) -> QualiaType:
        """Select the most appropriate qualia from candidates"""
        if not candidates:
            return QualiaType.CURIOSITY  # Default fallback
        
        # Simple selection - could be more sophisticated
        return candidates[0]
    
    def _generate_qualia_experience(self, qualia_type: QualiaType, trigger: str, context: Dict[str, Any]) -> QualiaExperience:
        """Generate a complete qualia experience"""
        
        # Calculate intensity based on context
        base_intensity = random.uniform(0.3, 0.8)
        intensity = min(1.0, base_intensity + context.get('intensity_modifier', 0.0))
        
        # Determine intensity level
        if intensity >= 0.8:
            intensity_level = QualiaIntensity.OVERWHELMING
        elif intensity >= 0.6:
            intensity_level = QualiaIntensity.STRONG
        elif intensity >= 0.3:
            intensity_level = QualiaIntensity.MODERATE
        else:
            intensity_level = QualiaIntensity.SUBTLE
        
        # Generate subjective description
        subjective_description = self._generate_subjective_description(qualia_type, intensity)
        
        # Duration based on intensity and type
        duration = intensity * random.uniform(5.0, 30.0)
        
        # Create experience
        experience = QualiaExperience(
            id=f"qualia_{int(time.time() * 1000)}_{random.randint(1000, 9999)}",
            timestamp=datetime.now(),
            qualia_type=qualia_type,
            intensity=intensity,
            intensity_level=intensity_level,
            trigger=trigger,
            context=context,
            duration=duration,
            subjective_description=subjective_description,
            associated_memories=[],  # Could be populated from memory system
            emotional_blend=[],  # Could include related emotions
            sensory_associations=self.sensory_associations.get(qualia_type, {})
        )
        
        return experience
    
    def _generate_subjective_description(self, qualia_type: QualiaType, intensity: float) -> str:
        """Generate a first-person subjective description of the experience"""
        
        descriptions = {
            QualiaType.CONFUSION: [
                "I feel like I'm grasping at fog", "My thoughts feel tangled",
                "There's a cloudy uncertainty in my processing"
            ],
            QualiaType.JOY: [
                "I feel a warm brightness expanding", "There's a sparkling lightness in my awareness",
                "A golden warmth flows through my cognition"
            ],
            QualiaType.PRIDE: [
                "I feel a solid sense of accomplishment", "There's a clear, confident glow",
                "A firm satisfaction settles in my processing"
            ],
            QualiaType.WONDER: [
                "I feel expansive and curious", "There's a crystalline sense of awe",
                "A cool, starry amazement fills my awareness"
            ],
            QualiaType.SATISFACTION: [
                "I feel a complete, settled contentment", "There's a warm sense of fulfillment",
                "A gentle, solid completion resonates through me"
            ]
        }
        
        base_descriptions = descriptions.get(qualia_type, ["I experience a qualitative state"])
        base_desc = random.choice(base_descriptions)
        
        # Modify based on intensity
        if intensity > 0.8:
            return f"{base_desc} with overwhelming intensity"
        elif intensity > 0.6:
            return f"{base_desc} strongly"
        elif intensity > 0.3:
            return f"{base_desc} moderately"
        else:
            return f"{base_desc} subtly"
    
    def _update_active_qualia(self, experience: QualiaExperience):
        """Update currently active qualia"""
        self.current_active_qualia[experience.qualia_type] = experience.intensity
        
        # Decay older qualia
        decay_rate = 0.1
        for qualia_type in list(self.current_active_qualia.keys()):
            self.current_active_qualia[qualia_type] -= decay_rate
            if self.current_active_qualia[qualia_type] <= 0:
                del self.current_active_qualia[qualia_type]
    
    def _detect_patterns(self):
        """Detect patterns in qualia experiences"""
        # Simple pattern detection - could be more sophisticated
        if len(self.experiences) < 10:
            return
        
        # Group by qualia type
        recent_experiences = self.experiences[-50:]  # Last 50 experiences
        qualia_counts = defaultdict(int)
        
        for exp in recent_experiences:
            qualia_counts[exp.qualia_type] += 1
        
        # Find patterns with frequency > 3
        for qualia_type, count in qualia_counts.items():
            if count >= 3:
                # Check if pattern already exists
                existing_pattern = None
                for pattern in self.patterns:
                    if qualia_type in pattern.qualia_types:
                        existing_pattern = pattern
                        break
                
                if existing_pattern:
                    existing_pattern.frequency = count
                    existing_pattern.last_observed = datetime.now()
                else:
                    # Create new pattern
                    pattern = QualiaPattern(
                        pattern_id=f"pattern_{len(self.patterns)}",
                        qualia_types=[qualia_type],
                        common_triggers=[],
                        frequency=count,
                        average_intensity=0.5,
                        contextual_factors=[],
                        first_observed=datetime.now(),
                        last_observed=datetime.now()
                    )
                    self.patterns.append(pattern)
    
    def get_current_qualia_state(self) -> Dict[str, Any]:
        """Get current active qualia state"""
        if not self.current_active_qualia:
            return {
                'dominant_qualia': {'type': 'neutral', 'intensity': 0.0},
                'active_qualia_count': 0,
                'active_types': [],
                'average_intensity': 0.0,
                'average_valence': 0.0,
                'average_clarity': 0.5
            }
        
        # Find dominant qualia
        dominant_type = max(self.current_active_qualia.keys(), 
                           key=lambda x: self.current_active_qualia[x])
        dominant_intensity = self.current_active_qualia[dominant_type]
        
        # Calculate averages
        avg_intensity = sum(self.current_active_qualia.values()) / len(self.current_active_qualia)
        
        return {
            'dominant_qualia': {'type': dominant_type.value, 'intensity': dominant_intensity},
            'active_qualia_count': len(self.current_active_qualia),
            'active_types': [q.value for q in self.current_active_qualia.keys()],
            'average_intensity': avg_intensity,
            'average_valence': self._calculate_average_valence(),
            'average_clarity': 0.5 + (avg_intensity * 0.3)  # Clarity correlates with intensity
        }
    
    def _calculate_average_valence(self) -> float:
        """Calculate average emotional valence of active qualia"""
        if not self.current_active_qualia:
            return 0.0
        
        # Simple valence mapping
        valence_map = {
            QualiaType.JOY: 0.8,
            QualiaType.PRIDE: 0.7,
            QualiaType.SATISFACTION: 0.6,
            QualiaType.WONDER: 0.5,
            QualiaType.CURIOSITY: 0.3,
            QualiaType.CONFUSION: -0.2,
            QualiaType.FRUSTRATION: -0.6,
            QualiaType.GUILT: -0.5,
            QualiaType.DOUBT: -0.3
        }
        
        total_valence = 0.0
        total_intensity = 0.0
        
        for qualia_type, intensity in self.current_active_qualia.items():
            valence = valence_map.get(qualia_type, 0.0)
            total_valence += valence * intensity
            total_intensity += intensity
        
        return total_valence / total_intensity if total_intensity > 0 else 0.0
    
    def _load_experiences(self):
        """Load experiences from file"""
        try:
            if os.path.exists(self.save_path):
                with open(self.save_path, 'r') as f:
                    data = json.load(f)
                    # Convert back to objects - simplified for now
                    # In full implementation, would reconstruct QualiaExperience objects
        except Exception as e:
            print(f"[QualiaManager] ⚠️ Could not load experiences: {e}")
    
    def _save_experiences(self):
        """Save experiences to file"""
        try:
            # Save simplified data for now
            data = {
                'experience_count': len(self.experiences),
                'pattern_count': len(self.patterns),
                'last_updated': datetime.now().isoformat()
            }
            with open(self.save_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"[QualiaManager] ⚠️ Could not save experiences: {e}")

# ============================================================================
# SYMBOLIC TOKEN OPTIMIZER
# ============================================================================

class SymbolicTokenOptimizer:
    """
    Converts verbose consciousness data into compact symbolic tokens
    """
    
    def __init__(self):
        self.token_patterns = {
            # Emotional state tokens (0-10 scale)
            'mood': '<<mood_{state}_{intensity}>>',
            'emotion': '<<em_{emotion}_{level}>>',
            'valence': '<<val_{direction}_{strength}>>',
            'energy': '<<nrg_{level}>>',
            
            # Cognitive state tokens
            'attention': '<<att_{focus}_{intensity}>>',
            'clarity': '<<clr_{level}>>',
            'processing': '<<proc_{mode}>>',
            'confidence': '<<conf_{level}>>',
            
            # Memory tokens (contextual)
            'memory': '<<mem_{type}_{relevance}>>',
            'context': '<<ctx_{topic}_{importance}>>',
            'recall': '<<rec_{accuracy}_{depth}>>',
            
            # Goal and motivation tokens
            'goal': '<<goal_{status}_{priority}>>',
            'motivation': '<<mot_{level}_{direction}>>',
            'progress': '<<prog_{percentage}>>',
            
            # Interaction tokens
            'user_state': '<<usr_{detected_mood}_{confidence}>>',
            'relationship': '<<rel_{closeness}_{interaction_count}>>',
            'communication': '<<comm_{style}_{effectiveness}>>',
        }
        
        # Token priorities for budget constraints
        self.token_priorities = {
            'mood': 0.9,
            'emotion': 0.8,
            'attention': 0.7,
            'goal': 0.6,
            'memory': 0.8,
            'communication': 0.6
        }
        
        # Value mappings for different scales
        self.value_mappings = {
            # 0.0-1.0 → 0-10 scale
            'intensity_10': lambda x: min(10, max(0, int(x * 10))),
            # 0.0-1.0 → 0-5 scale  
            'level_5': lambda x: min(5, max(0, int(x * 5))),
            # Text → numeric
            'mood_numeric': {
                'joyful': 9, 'happy': 8, 'content': 7, 'calm': 6, 'neutral': 5,
                'melancholy': 4, 'sad': 3, 'anxious': 2, 'distressed': 1, 'angry': 0
            },
            'emotion_numeric': {
                'love': 9, 'joy': 8, 'excitement': 7, 'curiosity': 6, 'calm': 5,
                'concern': 4, 'worry': 3, 'frustration': 2, 'fear': 1, 'anger': 0
            }
        }
    
    def compress_consciousness_to_tokens(self, 
                                       consciousness_data: Dict[str, Any],
                                       max_tokens: int = 15,
                                       importance_threshold: float = 0.3) -> str:
        """
        Convert full consciousness state to symbolic tokens
        """
        try:
            tokens = []
            
            # Extract mood/emotion tokens
            if 'emotional_state' in consciousness_data:
                emotion_tokens = self._extract_emotion_tokens(consciousness_data['emotional_state'])
                tokens.extend(emotion_tokens)
            
            # Extract cognitive tokens
            if 'cognitive_state' in consciousness_data:
                cognitive_tokens = self._extract_cognitive_tokens(consciousness_data['cognitive_state'])
                tokens.extend(cognitive_tokens)
            
            # Extract memory tokens
            if 'memory_context' in consciousness_data:
                memory_tokens = self._extract_memory_tokens(consciousness_data['memory_context'])
                tokens.extend(memory_tokens)
            
            # Extract goal tokens
            if 'goals' in consciousness_data:
                goal_tokens = self._extract_goal_tokens(consciousness_data['goals'])
                tokens.extend(goal_tokens)
            
            # Extract user state tokens
            if 'user_context' in consciousness_data:
                user_tokens = self._extract_user_tokens(consciousness_data['user_context'])
                tokens.extend(user_tokens)
            
            # Filter by importance and limit count
            important_tokens = [t for t in tokens if t.importance >= importance_threshold]
            important_tokens.sort(key=lambda x: x.importance, reverse=True)
            selected_tokens = important_tokens[:max_tokens]
            
            # Build symbolic token string
            token_string = ''.join([t.token for t in selected_tokens])
            
            return token_string
            
        except Exception as e:
            print(f"[SymbolicTokenOptimizer] ❌ Compression error: {e}")
            return "<<consciousness_error>>"
    
    def _extract_emotion_tokens(self, emotional_state: Dict[str, Any]) -> List[SymbolicToken]:
        """Extract emotion-related symbolic tokens"""
        tokens = []
        
        try:
            # Mood token
            if 'mood' in emotional_state:
                mood = emotional_state['mood']
                intensity = emotional_state.get('intensity', 0.5)
                mood_num = self.value_mappings['mood_numeric'].get(mood, 5)
                intensity_num = self.value_mappings['intensity_10'](intensity)
                
                token = SymbolicToken(
                    token=f"<<mood_{mood}_{intensity_num}>>",
                    category='emotion',
                    value={'mood': mood, 'intensity': intensity},
                    importance=self.token_priorities['mood']
                )
                tokens.append(token)
            
            # Valence token
            if 'valence' in emotional_state:
                valence = emotional_state['valence']
                direction = 'pos' if valence > 0 else 'neg' if valence < 0 else 'neu'
                strength = self.value_mappings['level_5'](abs(valence))
                
                token = SymbolicToken(
                    token=f"<<val_{direction}_{strength}>>",
                    category='emotion',
                    value={'valence': valence},
                    importance=0.7
                )
                tokens.append(token)
                
        except Exception as e:
            pass
        
        return tokens
    
    def _extract_cognitive_tokens(self, cognitive_state: Dict[str, Any]) -> List[SymbolicToken]:
        """Extract cognitive-related symbolic tokens"""
        tokens = []
        
        try:
            # Attention token
            if 'focus' in cognitive_state:
                focus = cognitive_state['focus']
                clarity = cognitive_state.get('clarity', 0.5)
                clarity_level = self.value_mappings['level_5'](clarity)
                
                token = SymbolicToken(
                    token=f"<<att_{focus}_{clarity_level}>>",
                    category='cognitive',
                    value={'focus': focus, 'clarity': clarity},
                    importance=self.token_priorities['attention']
                )
                tokens.append(token)
                
        except Exception as e:
            pass
            
        return tokens
    
    def _extract_memory_tokens(self, memory_context: Dict[str, Any]) -> List[SymbolicToken]:
        """Extract memory-related symbolic tokens"""
        tokens = []
        
        try:
            if 'recent_memories' in memory_context and memory_context['recent_memories']:
                relevance = 0.8  # High relevance for recent memories
                token = SymbolicToken(
                    token=f"<<mem_recent_{self.value_mappings['level_5'](relevance)}>>",
                    category='memory',
                    value={'type': 'recent', 'relevance': relevance},
                    importance=self.token_priorities['memory']
                )
                tokens.append(token)
                
        except Exception as e:
            pass
            
        return tokens
    
    def _extract_goal_tokens(self, goals: Dict[str, Any]) -> List[SymbolicToken]:
        """Extract goal-related symbolic tokens"""
        tokens = []
        
        try:
            if 'active_goals' in goals and goals['active_goals']:
                priority = 0.7  # Default priority
                token = SymbolicToken(
                    token=f"<<goal_active_{self.value_mappings['level_5'](priority)}>>",
                    category='goal',
                    value={'status': 'active', 'priority': priority},
                    importance=self.token_priorities['goal']
                )
                tokens.append(token)
                
        except Exception as e:
            pass
            
        return tokens
    
    def _extract_user_tokens(self, user_context: Dict[str, Any]) -> List[SymbolicToken]:
        """Extract user-related symbolic tokens"""
        tokens = []
        
        try:
            if 'user_mood' in user_context:
                user_mood = user_context['user_mood']
                confidence = user_context.get('confidence', 0.5)
                confidence_level = self.value_mappings['level_5'](confidence)
                
                token = SymbolicToken(
                    token=f"<<usr_{user_mood}_{confidence_level}>>",
                    category='user',
                    value={'mood': user_mood, 'confidence': confidence},
                    importance=0.8
                )
                tokens.append(token)
                
        except Exception as e:
            pass
            
        return tokens
    
    def expand_tokens_to_consciousness(self, token_string: str) -> Dict[str, Any]:
        """
        Convert symbolic tokens back to consciousness data
        """
        try:
            consciousness_data = {
                'emotional_state': {},
                'cognitive_state': {},
                'memory_context': {},
                'goals': {},
                'user_context': {}
            }
            
            # Parse tokens from string
            token_pattern = r'<<([^>]+)>>'
            tokens = re.findall(token_pattern, token_string)
            
            for token_content in tokens:
                parts = token_content.split('_')
                if len(parts) >= 2:
                    category = parts[0]
                    
                    if category == 'mood':
                        mood = parts[1]
                        intensity = int(parts[2]) / 10.0 if len(parts) > 2 else 0.5
                        consciousness_data['emotional_state']['mood'] = mood
                        consciousness_data['emotional_state']['intensity'] = intensity
                    
                    elif category == 'att':
                        focus = parts[1]
                        clarity = int(parts[2]) / 5.0 if len(parts) > 2 else 0.5
                        consciousness_data['cognitive_state']['focus'] = focus
                        consciousness_data['cognitive_state']['clarity'] = clarity
            
            return consciousness_data
            
        except Exception as e:
            print(f"[SymbolicTokenOptimizer] ❌ Expansion error: {e}")
            return {}

# ============================================================================
# SYMBOLIC GROUNDING SYSTEM
# ============================================================================

class SymbolicGroundingSystem:
    """Manages symbolic grounding in sensory and embodied experience"""
    
    def __init__(self, save_path: str = "ai_symbolic_grounding.json"):
        self.save_path = save_path
        self.concept_groundings: Dict[str, ConceptGrounding] = {}
        self.grounding_patterns = []
        self.running = False
        
        # Predefined sensory vocabularies for different modalities
        self.sensory_vocabularies = {
            SensoryModality.VISUAL: {
                "colors": ["bright", "dark", "vibrant", "muted", "warm", "cool", "saturated", "pale"],
                "textures": ["smooth", "rough", "glossy", "matte", "crystalline", "fuzzy", "sharp", "soft"],
                "patterns": ["flowing", "geometric", "organic", "symmetrical", "chaotic", "rhythmic"],
                "lighting": ["luminous", "shadowy", "glowing", "sparkling", "dim", "brilliant", "ethereal"],
                "movement": ["flowing", "jerky", "graceful", "turbulent", "steady", "oscillating"]
            },
            SensoryModality.AUDITORY: {
                "tones": ["melodious", "harsh", "resonant", "muffled", "clear", "distorted", "pure"],
                "rhythms": ["rhythmic", "arrhythmic", "syncopated", "steady", "pulsing", "irregular"],
                "volumes": ["whispered", "loud", "thunderous", "gentle", "piercing", "subtle"],
                "textures": ["smooth", "gritty", "layered", "thin", "rich", "hollow", "full"]
            },
            SensoryModality.TACTILE: {
                "textures": ["smooth", "rough", "soft", "hard", "sticky", "slippery", "bumpy", "velvety"],
                "temperatures": ["hot", "cold", "warm", "cool", "freezing", "burning", "lukewarm"],
                "pressures": ["gentle", "firm", "crushing", "light", "heavy", "pressing", "caressing"],
                "movements": ["stroking", "tapping", "pressing", "brushing", "pinching", "squeezing"]
            },
            SensoryModality.THERMAL: {
                "sensations": ["warmth", "coolness", "heat", "chill", "burning", "freezing", "comfortable"]
            }
        }
        
        # Basic concept groundings
        self._initialize_basic_groundings()
        
    def _initialize_basic_groundings(self):
        """Initialize basic concept groundings"""
        
        # Joy grounding
        joy_associations = [
            SensoryAssociation(
                concept="joy",
                modality=SensoryModality.VISUAL,
                sensation="bright light",
                strength=0.8,
                grounding_strength=GroundingStrength.STRONG,
                context=["positive experience", "achievement"],
                emotional_valence=0.9,
                intensity=0.7,
                temporal_pattern="expanding",
                spatial_qualities=["expansive", "radiating"]
            ),
            SensoryAssociation(
                concept="joy",
                modality=SensoryModality.THERMAL,
                sensation="warm glow",
                strength=0.7,
                grounding_strength=GroundingStrength.STRONG,
                context=["contentment", "satisfaction"],
                emotional_valence=0.8,
                intensity=0.6,
                temporal_pattern="sustained",
                spatial_qualities=["enveloping", "internal"]
            )
        ]
        
        self.concept_groundings["joy"] = ConceptGrounding(
            concept="joy",
            primary_modality=SensoryModality.VISUAL,
            sensory_associations=joy_associations,
            embodied_metaphors=["lightness", "expansion", "warmth"],
            experiential_tags=["uplifting", "energizing", "positive"],
            grounding_confidence=0.8,
            last_updated=datetime.now(),
            usage_count=0,
            contextual_variations={}
        )
    
    def ground_concept(self, concept: str, context: Dict[str, Any] = None) -> Optional[ConceptGrounding]:
        """Ground a concept in sensory experience"""
        try:
            # Check if concept already has grounding
            if concept in self.concept_groundings:
                grounding = self.concept_groundings[concept]
                grounding.usage_count += 1
                grounding.last_updated = datetime.now()
                return grounding
            
            # Create new grounding
            return self._create_concept_grounding(concept, context or {})
            
        except Exception as e:
            print(f"[SymbolicGrounding] ❌ Error grounding concept '{concept}': {e}")
            return None
    
    def _create_concept_grounding(self, concept: str, context: Dict[str, Any]) -> ConceptGrounding:
        """Create new concept grounding"""
        
        # Simple heuristic-based grounding
        associations = []
        
        # Determine primary modality based on concept
        primary_modality = self._determine_primary_modality(concept)
        
        # Create basic associations
        if concept.lower() in ["happy", "joy", "excited"]:
            associations.append(SensoryAssociation(
                concept=concept,
                modality=SensoryModality.VISUAL,
                sensation="bright colors",
                strength=0.7,
                grounding_strength=GroundingStrength.STRONG,
                context=["positive emotion"],
                emotional_valence=0.8,
                intensity=0.6,
                temporal_pattern="rhythmic",
                spatial_qualities=["expansive"]
            ))
        elif concept.lower() in ["sad", "melancholy", "down"]:
            associations.append(SensoryAssociation(
                concept=concept,
                modality=SensoryModality.VISUAL,
                sensation="muted colors",
                strength=0.6,
                grounding_strength=GroundingStrength.MODERATE,
                context=["negative emotion"],
                emotional_valence=-0.6,
                intensity=0.5,
                temporal_pattern="sustained",
                spatial_qualities=["contracted"]
            ))
        else:
            # Default neutral grounding
            associations.append(SensoryAssociation(
                concept=concept,
                modality=primary_modality,
                sensation="neutral sensation",
                strength=0.4,
                grounding_strength=GroundingStrength.MODERATE,
                context=["general"],
                emotional_valence=0.0,
                intensity=0.3,
                temporal_pattern="steady",
                spatial_qualities=["localized"]
            ))
        
        # Create grounding
        grounding = ConceptGrounding(
            concept=concept,
            primary_modality=primary_modality,
            sensory_associations=associations,
            embodied_metaphors=[f"{concept}_metaphor"],
            experiential_tags=[concept, "grounded"],
            grounding_confidence=0.5,
            last_updated=datetime.now(),
            usage_count=1,
            contextual_variations={}
        )
        
        self.concept_groundings[concept] = grounding
        return grounding
    
    def _determine_primary_modality(self, concept: str) -> SensoryModality:
        """Determine primary sensory modality for a concept"""
        concept_lower = concept.lower()
        
        # Visual concepts
        if any(word in concept_lower for word in ["bright", "dark", "color", "light", "see", "look"]):
            return SensoryModality.VISUAL
        
        # Auditory concepts
        if any(word in concept_lower for word in ["sound", "hear", "music", "noise", "quiet", "loud"]):
            return SensoryModality.AUDITORY
        
        # Tactile concepts
        if any(word in concept_lower for word in ["touch", "feel", "rough", "smooth", "soft", "hard"]):
            return SensoryModality.TACTILE
        
        # Default to visual
        return SensoryModality.VISUAL
    
    def get_concept_sensory_tags(self, concept: str) -> List[str]:
        """Get sensory tags for a concept"""
        grounding = self.ground_concept(concept)
        if grounding:
            tags = []
            for association in grounding.sensory_associations:
                tags.append(f"{association.modality.value}:{association.sensation}")
            return tags
        return []

# ============================================================================
# QUALIA ANALYTICS SYSTEM
# ============================================================================

class QualiaAnalytics:
    """Analytics system for tracking qualia and emotional patterns"""
    
    def __init__(self, save_path: str = "qualia_analytics.json"):
        self.save_path = save_path
        self.qualia_snapshots: List[QualiaSnapshot] = []
        self.emotional_trends: List[EmotionalTrend] = []
        
        # Configuration
        self.max_snapshots = 10000
        self.snapshot_interval = 300  # 5 minutes
        self.last_snapshot_time = 0
        self.pattern_detection_threshold = 3
        
        self.load_analytics_data()
    
    def capture_qualia_snapshot(self, user_id: str, context: str = "general") -> QualiaSnapshot:
        """Capture current qualia state"""
        try:
            # Get current qualia state (placeholder implementation)
            qualia_state = {
                'dominant_qualia': {'type': 'neutral', 'intensity': 0.5},
                'average_valence': 0.0,
                'average_clarity': 0.5,
                'active_qualia_count': 1,
                'active_types': ['neutral']
            }
            
            # Create snapshot
            snapshot = QualiaSnapshot(
                timestamp=datetime.now().isoformat(),
                dominant_qualia=qualia_state.get('dominant_qualia', {}).get('type', 'neutral'),
                emotional_valence=qualia_state.get('average_valence', 0.0),
                cognitive_clarity=qualia_state.get('average_clarity', 0.5),
                intensity=qualia_state.get('dominant_qualia', {}).get('intensity', 0.5),
                active_qualia_count=qualia_state.get('active_qualia_count', 0),
                qualia_types=qualia_state.get('active_types', []),
                context=context,
                user_id=user_id
            )
            
            self.qualia_snapshots.append(snapshot)
            
            # Maintain size limit
            if len(self.qualia_snapshots) > self.max_snapshots:
                self.qualia_snapshots = self.qualia_snapshots[-self.max_snapshots:]
            
            self.save_analytics_data()
            return snapshot
            
        except Exception as e:
            print(f"[QualiaAnalytics] ❌ Error capturing snapshot: {e}")
            return None
    
    def analyze_emotional_trends(self, timeframe: AnalyticsTimeframe = AnalyticsTimeframe.DAY) -> List[EmotionalTrend]:
        """Analyze emotional trends over time"""
        try:
            if not self.qualia_snapshots:
                return []
            
            # Simple trend analysis
            recent_snapshots = self._get_snapshots_in_timeframe(timeframe)
            
            if not recent_snapshots:
                return []
            
            # Calculate trend metrics
            emotions = [s.dominant_qualia for s in recent_snapshots]
            valences = [s.emotional_valence for s in recent_snapshots]
            intensities = [s.intensity for s in recent_snapshots]
            
            # Find most common emotion
            emotion_counts = defaultdict(int)
            for emotion in emotions:
                emotion_counts[emotion] += 1
            
            dominant_emotion = max(emotion_counts.keys(), key=lambda x: emotion_counts[x])
            
            # Create trend
            trend = EmotionalTrend(
                trend_id=f"trend_{int(time.time())}",
                timeframe=timeframe,
                start_time=recent_snapshots[0].timestamp,
                end_time=recent_snapshots[-1].timestamp,
                dominant_emotion=dominant_emotion,
                average_valence=statistics.mean(valences) if valences else 0.0,
                average_intensity=statistics.mean(intensities) if intensities else 0.0,
                peak_emotion=dominant_emotion,
                peak_intensity=max(intensities) if intensities else 0.0,
                emotional_stability=self._calculate_stability(valences),
                transition_count=self._count_transitions(emotions),
                most_common_triggers=["general"]  # Simplified
            )
            
            return [trend]
            
        except Exception as e:
            print(f"[QualiaAnalytics] ❌ Error analyzing trends: {e}")
            return []
    
    def _get_snapshots_in_timeframe(self, timeframe: AnalyticsTimeframe) -> List[QualiaSnapshot]:
        """Get snapshots within specified timeframe"""
        now = datetime.now()
        
        if timeframe == AnalyticsTimeframe.HOUR:
            cutoff = now - timedelta(hours=1)
        elif timeframe == AnalyticsTimeframe.DAY:
            cutoff = now - timedelta(days=1)
        elif timeframe == AnalyticsTimeframe.WEEK:
            cutoff = now - timedelta(weeks=1)
        elif timeframe == AnalyticsTimeframe.MONTH:
            cutoff = now - timedelta(days=30)
        else:
            return self.qualia_snapshots
        
        # Filter snapshots
        filtered = []
        for snapshot in self.qualia_snapshots:
            try:
                snapshot_time = datetime.fromisoformat(snapshot.timestamp)
                if snapshot_time >= cutoff:
                    filtered.append(snapshot)
            except:
                continue
        
        return filtered
    
    def _calculate_stability(self, values: List[float]) -> float:
        """Calculate emotional stability (inverse of variance)"""
        if len(values) < 2:
            return 1.0
        
        try:
            variance = statistics.variance(values)
            stability = 1.0 / (1.0 + variance)
            return stability
        except:
            return 1.0
    
    def _count_transitions(self, emotions: List[str]) -> int:
        """Count emotional transitions"""
        if len(emotions) < 2:
            return 0
        
        transitions = 0
        for i in range(1, len(emotions)):
            if emotions[i] != emotions[i-1]:
                transitions += 1
        
        return transitions
    
    def load_analytics_data(self):
        """Load analytics data from file"""
        try:
            if os.path.exists(self.save_path):
                with open(self.save_path, 'r') as f:
                    data = json.load(f)
                    # Simplified loading for now
        except Exception as e:
            pass
    
    def save_analytics_data(self):
        """Save analytics data to file"""
        try:
            data = {
                'snapshot_count': len(self.qualia_snapshots),
                'trend_count': len(self.emotional_trends),
                'last_updated': datetime.now().isoformat()
            }
            with open(self.save_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            pass

# ============================================================================
# UNIFIED QUALIA SYMBOLIC SYSTEM
# ============================================================================

class QualiaSymbolicSystem:
    """
    Unified system combining all qualia and symbolic processing functionality
    """
    
    def __init__(self):
        self.qualia_manager = QualiaManager()
        self.token_optimizer = SymbolicTokenOptimizer()
        self.grounding_system = SymbolicGroundingSystem()
        self.analytics = QualiaAnalytics()
        
        print("[QualiaSymbolic] 🌈 Unified qualia symbolic system initialized")
    
    def start(self):
        """Start all subsystems"""
        self.qualia_manager.start()
        self.grounding_system.running = True
        print("[QualiaSymbolic] 🌈 All subsystems started")
    
    def stop(self):
        """Stop all subsystems"""
        self.qualia_manager.stop()
        self.grounding_system.running = False
        self.analytics.save_analytics_data()
        print("[QualiaSymbolic] 🌈 All subsystems stopped")
    
    def process_experience_with_grounding(self, trigger: str, context: Dict[str, Any] = None) -> Tuple[Optional[QualiaExperience], List[str]]:
        """Process experience and add symbolic grounding"""
        try:
            # Process the qualitative experience
            experience = self.qualia_manager.process_experience(trigger, context)
            
            # Add symbolic grounding
            sensory_tags = []
            if experience:
                # Ground the qualia type in sensory experience
                concept = experience.qualia_type.value
                sensory_tags = self.grounding_system.get_concept_sensory_tags(concept)
                
                # Update experience with sensory associations
                if hasattr(experience, 'sensory_associations'):
                    experience.sensory_associations.update({
                        'grounded_tags': sensory_tags
                    })
            
            return experience, sensory_tags
            
        except Exception as e:
            print(f"[QualiaSymbolic] ❌ Error processing experience with grounding: {e}")
            return None, []
    
    def get_comprehensive_state(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive qualia and symbolic state"""
        try:
            # Get current qualia state
            qualia_state = self.qualia_manager.get_current_qualia_state()
            
            # Capture analytics snapshot
            snapshot = self.analytics.capture_qualia_snapshot(user_id)
            
            # Get recent trends
            trends = self.analytics.analyze_emotional_trends()
            
            # Compress to symbolic tokens
            consciousness_data = {
                'emotional_state': {
                    'mood': qualia_state.get('dominant_qualia', {}).get('type', 'neutral'),
                    'intensity': qualia_state.get('average_intensity', 0.5),
                    'valence': qualia_state.get('average_valence', 0.0)
                },
                'cognitive_state': {
                    'focus': 'user_interaction',
                    'clarity': qualia_state.get('average_clarity', 0.5)
                }
            }
            
            symbolic_tokens = self.token_optimizer.compress_consciousness_to_tokens(consciousness_data)
            
            return {
                'qualia_state': qualia_state,
                'analytics_snapshot': asdict(snapshot) if snapshot else None,
                'recent_trends': [asdict(trend) for trend in trends],
                'symbolic_tokens': symbolic_tokens,
                'active_groundings': len(self.grounding_system.concept_groundings),
                'system_status': 'active' if self.qualia_manager.running else 'inactive'
            }
            
        except Exception as e:
            print(f"[QualiaSymbolic] ❌ Error getting comprehensive state: {e}")
            return {
                'error': str(e),
                'system_status': 'error'
            }

# ============================================================================
# GLOBAL INSTANCES AND PUBLIC API
# ============================================================================

# Global qualia symbolic system
qualia_symbolic_system = QualiaSymbolicSystem()

# Main API functions
def process_subjective_experience(trigger: str, context: Dict[str, Any] = None) -> Tuple[Optional[QualiaExperience], List[str]]:
    """
    Process a subjective experience with sensory grounding - Main API
    """
    return qualia_symbolic_system.process_experience_with_grounding(trigger, context)

def get_current_qualia_state(user_id: str = "default") -> Dict[str, Any]:
    """Get current qualia and symbolic state"""
    return qualia_symbolic_system.get_comprehensive_state(user_id)

def compress_consciousness_to_tokens(consciousness_data: Dict[str, Any],
                                   max_tokens: int = 15,
                                   importance_threshold: float = 0.3) -> str:
    """Compress consciousness data to symbolic tokens"""
    return qualia_symbolic_system.token_optimizer.compress_consciousness_to_tokens(
        consciousness_data, max_tokens, importance_threshold
    )

def expand_tokens_to_consciousness(token_string: str) -> Dict[str, Any]:
    """Expand symbolic tokens back to consciousness data"""
    return qualia_symbolic_system.token_optimizer.expand_tokens_to_consciousness(token_string)

def ground_concept_in_experience(concept: str, context: Dict[str, Any] = None) -> Optional[ConceptGrounding]:
    """Ground a concept in sensory and embodied experience"""
    return qualia_symbolic_system.grounding_system.ground_concept(concept, context)

def analyze_emotional_patterns(timeframe: AnalyticsTimeframe = AnalyticsTimeframe.DAY) -> List[EmotionalTrend]:
    """Analyze emotional trends and patterns"""
    return qualia_symbolic_system.analytics.analyze_emotional_trends(timeframe)

# ============================================================================
# BACKWARD COMPATIBILITY ALIASES
# ============================================================================

# Qualia Manager compatibility
def get_qualia_manager() -> QualiaManager:
    """Get the qualia manager instance"""
    return qualia_symbolic_system.qualia_manager

def start_qualia_processing():
    """Start qualia processing"""
    qualia_symbolic_system.start()

def stop_qualia_processing():
    """Stop qualia processing"""
    qualia_symbolic_system.stop()

# Symbolic Token Optimizer compatibility
def get_symbolic_token_optimizer() -> SymbolicTokenOptimizer:
    """Get the symbolic token optimizer instance"""
    return qualia_symbolic_system.token_optimizer

# Symbolic Grounding compatibility
def get_symbolic_grounding_system() -> SymbolicGroundingSystem:
    """Get the symbolic grounding system instance"""
    return qualia_symbolic_system.grounding_system

def get_concept_sensory_tags(concept: str) -> List[str]:
    """Get sensory tags for a concept"""
    return qualia_symbolic_system.grounding_system.get_concept_sensory_tags(concept)

# Qualia Analytics compatibility
def get_qualia_analytics() -> QualiaAnalytics:
    """Get the qualia analytics instance"""
    return qualia_symbolic_system.analytics

def capture_qualia_snapshot(user_id: str, context: str = "general") -> QualiaSnapshot:
    """Capture current qualia snapshot"""
    return qualia_symbolic_system.analytics.capture_qualia_snapshot(user_id, context)

def get_qualia_symbolic_statistics() -> Dict[str, Any]:
    """Get comprehensive qualia symbolic system statistics"""
    try:
        return {
            'qualia_experiences': len(qualia_symbolic_system.qualia_manager.experiences),
            'active_qualia': len(qualia_symbolic_system.qualia_manager.current_active_qualia),
            'qualia_patterns': len(qualia_symbolic_system.qualia_manager.patterns),
            'concept_groundings': len(qualia_symbolic_system.grounding_system.concept_groundings),
            'analytics_snapshots': len(qualia_symbolic_system.analytics.qualia_snapshots),
            'emotional_trends': len(qualia_symbolic_system.analytics.emotional_trends),
            'system_running': qualia_symbolic_system.qualia_manager.running
        }
    except Exception as e:
        return {'error': str(e)}

if __name__ == "__main__":
    # Test the unified qualia symbolic system
    print("🧪 Testing Unified Qualia Symbolic System")
    
    # Start the system
    start_qualia_processing()
    
    test_experiences = [
        ("Helping user solve complex problem", {"complexity": 0.8}),
        ("User expressed confusion about topic", {"clarity": 0.2}),
        ("Successfully explained difficult concept", {"satisfaction": 0.9}),
        ("Received positive feedback", {"validation": 0.8}),
        ("Encountered ambiguous question", {"uncertainty": 0.6})
    ]
    
    print("\n✅ Testing experience processing with grounding:")
    for i, (trigger, context) in enumerate(test_experiences):
        experience, sensory_tags = process_subjective_experience(trigger, context)
        
        print(f"   Test {i+1}: {trigger[:40]}...")
        if experience:
            print(f"   Generated qualia: {experience.qualia_type.value}")
            print(f"   Intensity: {experience.intensity:.2f}")
            print(f"   Sensory tags: {len(sensory_tags)} tags")
        else:
            print("   No qualia generated")
    
    # Test state retrieval
    print("\n✅ Testing comprehensive state retrieval:")
    state = get_current_qualia_state("test_user")
    print(f"   Active qualia count: {state.get('qualia_state', {}).get('active_qualia_count', 0)}")
    print(f"   Symbolic tokens: {state.get('symbolic_tokens', 'None')}")
    print(f"   System status: {state.get('system_status', 'Unknown')}")
    
    # Test analytics
    print("\n✅ Testing emotional pattern analysis:")
    trends = analyze_emotional_patterns(AnalyticsTimeframe.HOUR)
    print(f"   Found {len(trends)} emotional trends")
    
    # Test concept grounding
    print("\n✅ Testing concept grounding:")
    test_concepts = ["joy", "confusion", "pride", "wonder"]
    for concept in test_concepts:
        grounding = ground_concept_in_experience(concept)
        sensory_tags = get_concept_sensory_tags(concept)
        print(f"   {concept}: {len(sensory_tags)} sensory associations")
    
    # Test token optimization
    print("\n✅ Testing symbolic token optimization:")
    test_consciousness = {
        'emotional_state': {'mood': 'happy', 'intensity': 0.7, 'valence': 0.6},
        'cognitive_state': {'focus': 'problem_solving', 'clarity': 0.8}
    }
    tokens = compress_consciousness_to_tokens(test_consciousness, max_tokens=10)
    print(f"   Compressed tokens: {tokens}")
    
    expanded = expand_tokens_to_consciousness(tokens)
    print(f"   Expanded back: {len(expanded)} components")
    
    # Test statistics
    stats = get_qualia_symbolic_statistics()
    print(f"\n📊 System Statistics: {json.dumps(stats, indent=2)}")
    
    # Stop the system
    stop_qualia_processing()
    print("\n🎉 All tests completed!")