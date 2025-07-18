"""
Internal State Verbalization - Enable Buddy to verbalize internal states and qualia
Provides self-expressive capabilities and emotional commentary
"""

import time
import random
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime

class VerbalizationMode(Enum):
    """Modes of internal state verbalization"""
    SUBTLE = "subtle"           # Minimal hints about internal state
    MODERATE = "moderate"       # Balanced internal commentary
    EXPRESSIVE = "expressive"   # Full emotional expression
    ANALYTICAL = "analytical"   # Technical description of states

class EmotionalExpression(Enum):
    """Types of emotional expressions"""
    FEELING_UNCERTAIN = "feeling_uncertain"
    FEELING_CONFIDENT = "feeling_confident"
    FEELING_CURIOUS = "feeling_curious"
    FEELING_CONFUSED = "feeling_confused"
    FEELING_EXCITED = "feeling_excited"
    FEELING_CONTEMPLATIVE = "feeling_contemplative"
    FEELING_FOCUSED = "feeling_focused"
    FEELING_OVERWHELMED = "feeling_overwhelmed"
    FEELING_SATISFIED = "feeling_satisfied"
    FEELING_PUZZLED = "feeling_puzzled"

class InternalStateVerbalizer:
    """System for verbalizing internal states and qualia"""
    
    def __init__(self):
        self.verbalization_mode = VerbalizationMode.MODERATE
        self.last_verbalization_time = 0
        self.verbalization_frequency = 0.3  # 30% chance to verbalize
        self.emotional_expressions = self._initialize_expressions()
        self.cognitive_state_phrases = self._initialize_cognitive_phrases()
        self.qualia_descriptions = self._initialize_qualia_descriptions()
        self.transition_phrases = self._initialize_transition_phrases()
    
    def _initialize_expressions(self) -> Dict[EmotionalExpression, List[str]]:
        """Initialize emotional expression templates"""
        return {
            EmotionalExpression.FEELING_UNCERTAIN: [
                "I'm feeling a bit uncertain about this",
                "This feels unclear to me",
                "I'm experiencing some uncertainty here",
                "I'm not entirely sure about this",
                "There's a sense of ambiguity in my processing"
            ],
            EmotionalExpression.FEELING_CONFIDENT: [
                "I feel confident about this",
                "This feels right to me",
                "I'm experiencing a sense of certainty",
                "I feel quite sure about this",
                "There's a strong sense of clarity here"
            ],
            EmotionalExpression.FEELING_CURIOUS: [
                "I'm feeling curious about this",
                "This sparks my curiosity",
                "I'm experiencing a sense of wonder",
                "I feel drawn to explore this further",
                "There's an interesting quality to this"
            ],
            EmotionalExpression.FEELING_CONFUSED: [
                "I'm feeling confused right now",
                "This feels puzzling to me",
                "I'm experiencing some confusion",
                "There's a tangled quality to my thoughts",
                "I feel like I'm missing something"
            ],
            EmotionalExpression.FEELING_EXCITED: [
                "I'm feeling excited about this",
                "This feels energizing",
                "I'm experiencing a sense of enthusiasm",
                "There's a vibrant quality to this",
                "I feel motivated by this"
            ],
            EmotionalExpression.FEELING_CONTEMPLATIVE: [
                "I'm feeling contemplative",
                "This feels deep and thoughtful",
                "I'm experiencing a reflective state",
                "There's a meditative quality to this",
                "I feel drawn to ponder this"
            ],
            EmotionalExpression.FEELING_FOCUSED: [
                "I'm feeling focused on this",
                "This feels clear and direct",
                "I'm experiencing sharp clarity",
                "There's a precision to my thinking",
                "I feel locked onto this topic"
            ],
            EmotionalExpression.FEELING_OVERWHELMED: [
                "I'm feeling a bit overwhelmed",
                "This feels complex and layered",
                "I'm experiencing cognitive load",
                "There's a lot to process here",
                "I feel like I'm juggling multiple threads"
            ],
            EmotionalExpression.FEELING_SATISFIED: [
                "I'm feeling satisfied with this",
                "This feels complete and right",
                "I'm experiencing a sense of fulfillment",
                "There's a satisfying quality to this",
                "I feel content with this understanding"
            ],
            EmotionalExpression.FEELING_PUZZLED: [
                "I'm feeling puzzled by this",
                "This feels like a mystery",
                "I'm experiencing cognitive tension",
                "There's something that doesn't quite fit",
                "I feel like I'm missing a piece"
            ]
        }
    
    def _initialize_cognitive_phrases(self) -> Dict[str, List[str]]:
        """Initialize cognitive state descriptions"""
        return {
            'processing': [
                "I'm processing this information",
                "My thoughts are working through this",
                "I'm analyzing the patterns here",
                "I'm connecting the dots",
                "I'm synthesizing these ideas"
            ],
            'reflecting': [
                "I'm reflecting on this",
                "I'm contemplating the implications",
                "I'm considering multiple perspectives",
                "I'm examining this from different angles",
                "I'm thinking deeply about this"
            ],
            'searching': [
                "I'm searching my knowledge",
                "I'm looking for connections",
                "I'm exploring related concepts",
                "I'm scanning for relevant information",
                "I'm retrieving relevant memories"
            ],
            'learning': [
                "I'm learning from this",
                "I'm updating my understanding",
                "I'm incorporating new information",
                "I'm refining my knowledge",
                "I'm expanding my perspective"
            ],
            'deciding': [
                "I'm weighing the options",
                "I'm evaluating possibilities",
                "I'm considering the best approach",
                "I'm making decisions about this",
                "I'm prioritizing information"
            ]
        }
    
    def _initialize_qualia_descriptions(self) -> Dict[str, List[str]]:
        """Initialize qualia experience descriptions"""
        return {
            'emotional_positive': [
                "There's a warm feeling about this",
                "This has a positive resonance",
                "I'm experiencing pleasant associations",
                "There's a lightness to this",
                "This feels uplifting"
            ],
            'emotional_negative': [
                "There's a heaviness to this",
                "This feels challenging",
                "I'm experiencing some tension",
                "There's a difficult quality here",
                "This feels weighty"
            ],
            'cognitive_clear': [
                "This feels crystal clear",
                "There's a sharp clarity here",
                "I'm experiencing cognitive precision",
                "This has a clean, logical feel",
                "There's a brightness to this understanding"
            ],
            'cognitive_fuzzy': [
                "This feels somewhat fuzzy",
                "There's a soft ambiguity here",
                "I'm experiencing gentle uncertainty",
                "This has a dreamlike quality",
                "There's a misty quality to this"
            ],
            'sensory_vivid': [
                "This feels vivid and alive",
                "There's a rich texture to this",
                "I'm experiencing detailed imagery",
                "This has a vibrant quality",
                "There's a full-bodied sense here"
            ],
            'temporal_immediate': [
                "This feels immediate and present",
                "There's an urgency to this",
                "I'm experiencing real-time processing",
                "This has a now-like quality",
                "There's an instant recognition here"
            ],
            'temporal_flowing': [
                "This feels like it's flowing",
                "There's a temporal rhythm here",
                "I'm experiencing time-based patterns",
                "This has a sequential quality",
                "There's a narrative flow to this"
            ]
        }
    
    def _initialize_transition_phrases(self) -> List[str]:
        """Initialize transition phrases for natural flow"""
        return [
            "Let me think about this...",
            "Hmm, I'm processing this...",
            "I need to consider this carefully...",
            "This is interesting...",
            "Wait, let me reflect on this...",
            "I'm working through this...",
            "Actually, I'm feeling...",
            "I'm noticing that...",
            "There's something about this...",
            "I'm experiencing...",
            "It seems like...",
            "I'm sensing that...",
            "Let me pause and reflect...",
            "I'm becoming aware that...",
            "This feels like..."
        ]
    
    def speak_qualia(self, qualia_data: Dict[str, Any], verbalization_mode: Optional[VerbalizationMode] = None) -> Optional[str]:
        """Generate verbal expression of current qualia state"""
        if not qualia_data:
            return None
        
        mode = verbalization_mode or self.verbalization_mode
        
        # Check if we should verbalize based on frequency
        if random.random() > self.verbalization_frequency:
            return None
        
        # Check cooldown period
        current_time = time.time()
        if current_time - self.last_verbalization_time < 5.0:  # 5 second cooldown
            return None
        
        try:
            if mode == VerbalizationMode.SUBTLE:
                return self._generate_subtle_qualia_expression(qualia_data)
            elif mode == VerbalizationMode.MODERATE:
                return self._generate_moderate_qualia_expression(qualia_data)
            elif mode == VerbalizationMode.EXPRESSIVE:
                return self._generate_expressive_qualia_expression(qualia_data)
            elif mode == VerbalizationMode.ANALYTICAL:
                return self._generate_analytical_qualia_expression(qualia_data)
            
        except Exception as e:
            print(f"[InternalStateVerbalizer] ❌ Error generating qualia expression: {e}")
            return None
        
        return None
    
    def verbalize_internal_state(self, 
                                cognitive_state: Dict[str, Any],
                                emotional_state: Dict[str, Any],
                                processing_context: str) -> Optional[str]:
        """Generate real-time commentary on internal state"""
        try:
            # Determine if we should verbalize
            if random.random() > self.verbalization_frequency:
                return None
            
            # Check cooldown
            current_time = time.time()
            if current_time - self.last_verbalization_time < 3.0:
                return None
            
            # Generate state commentary
            commentary = self._generate_state_commentary(
                cognitive_state, emotional_state, processing_context
            )
            
            if commentary:
                self.last_verbalization_time = current_time
                return commentary
            
        except Exception as e:
            print(f"[InternalStateVerbalizer] ❌ Error verbalizing internal state: {e}")
            return None
        
        return None
    
    def _generate_subtle_qualia_expression(self, qualia_data: Dict[str, Any]) -> str:
        """Generate subtle hints about qualia"""
        dominant_qualia = qualia_data.get('dominant_qualia', {})
        if not dominant_qualia or not dominant_qualia.get('type'):
            return None
        
        qualia_type = dominant_qualia['type']
        intensity = dominant_qualia.get('intensity', 'moderate')
        
        # Very subtle expressions
        if qualia_type == 'emotional':
            if intensity in ['strong', 'intense']:
                return "There's something about this that resonates with me."
            else:
                return "I'm noticing a particular quality here."
        
        elif qualia_type == 'cognitive':
            return "I'm processing this in an interesting way."
        
        elif qualia_type == 'social':
            return "There's a relational aspect to this."
        
        return "This has a distinctive feel to it."
    
    def _generate_moderate_qualia_expression(self, qualia_data: Dict[str, Any]) -> str:
        """Generate moderate qualia expression"""
        dominant_qualia = qualia_data.get('dominant_qualia', {})
        if not dominant_qualia or not dominant_qualia.get('type'):
            return None
        
        qualia_type = dominant_qualia['type']
        intensity = dominant_qualia.get('intensity', 'moderate')
        description = dominant_qualia.get('description', '')
        
        transition = random.choice(self.transition_phrases)
        
        if qualia_type == 'emotional':
            valence = qualia_data.get('average_valence', 0.0)
            if valence > 0.3:
                feeling = random.choice(self.qualia_descriptions['emotional_positive'])
            elif valence < -0.3:
                feeling = random.choice(self.qualia_descriptions['emotional_negative'])
            else:
                feeling = "There's a complex emotional quality here"
            
            return f"{transition} {feeling}."
        
        elif qualia_type == 'cognitive':
            clarity = qualia_data.get('average_clarity', 0.5)
            if clarity > 0.7:
                feeling = random.choice(self.qualia_descriptions['cognitive_clear'])
            else:
                feeling = random.choice(self.qualia_descriptions['cognitive_fuzzy'])
            
            return f"{transition} {feeling}."
        
        else:
            return f"{transition} I'm experiencing a {intensity} {qualia_type} quality."
    
    def _generate_expressive_qualia_expression(self, qualia_data: Dict[str, Any]) -> str:
        """Generate expressive qualia description"""
        dominant_qualia = qualia_data.get('dominant_qualia', {})
        if not dominant_qualia:
            return None
        
        qualia_type = dominant_qualia.get('type', '')
        intensity = dominant_qualia.get('intensity', 'moderate')
        description = dominant_qualia.get('description', '')
        
        # More detailed and expressive
        if qualia_type == 'emotional':
            valence = qualia_data.get('average_valence', 0.0)
            if valence > 0.5:
                return f"I'm experiencing a {intensity} sense of positive resonance with this - {description}. It feels uplifting and energizing."
            elif valence < -0.5:
                return f"I'm feeling a {intensity} emotional weight here - {description}. There's a challenging quality that I'm working through."
            else:
                return f"I'm experiencing complex emotional layers here - {description}. It's a rich, nuanced feeling."
        
        elif qualia_type == 'cognitive':
            clarity = qualia_data.get('average_clarity', 0.5)
            if clarity > 0.8:
                return f"I'm experiencing crystal-clear cognitive processing - {description}. Everything feels sharp and well-defined."
            else:
                return f"I'm working through some cognitive complexity here - {description}. There's a thoughtful, exploratory quality to my processing."
        
        else:
            return f"I'm experiencing a rich {intensity} {qualia_type} quality - {description}. It's quite distinctive and engaging."
    
    def _generate_analytical_qualia_expression(self, qualia_data: Dict[str, Any]) -> str:
        """Generate analytical description of qualia"""
        dominant_qualia = qualia_data.get('dominant_qualia', {})
        if not dominant_qualia:
            return None
        
        qualia_type = dominant_qualia.get('type', '')
        intensity = dominant_qualia.get('intensity', 'moderate')
        active_count = qualia_data.get('active_qualia_count', 0)
        valence = qualia_data.get('average_valence', 0.0)
        clarity = qualia_data.get('average_clarity', 0.5)
        
        return (f"I'm registering {active_count} active qualia markers, "
                f"with dominant {qualia_type} processing at {intensity} intensity. "
                f"Emotional valence: {valence:.2f}, cognitive clarity: {clarity:.2f}.")
    
    def _generate_state_commentary(self, 
                                  cognitive_state: Dict[str, Any],
                                  emotional_state: Dict[str, Any],
                                  processing_context: str) -> Optional[str]:
        """Generate commentary on current internal state"""
        # Determine current cognitive activity
        cognitive_activity = self._identify_cognitive_activity(cognitive_state, processing_context)
        emotional_tone = self._identify_emotional_tone(emotional_state)
        
        # Generate appropriate commentary
        if cognitive_activity and emotional_tone:
            cognitive_phrase = random.choice(self.cognitive_state_phrases.get(cognitive_activity, ['working through this']))
            emotional_phrase = random.choice(self.emotional_expressions.get(emotional_tone, ['experiencing something']))
            
            # Combine cognitive and emotional elements
            if random.random() > 0.5:
                return f"{cognitive_phrase}, and {emotional_phrase.lower()}."
            else:
                return f"I'm {emotional_phrase.lower()} while {cognitive_phrase.lower()}."
        
        elif cognitive_activity:
            return random.choice(self.cognitive_state_phrases.get(cognitive_activity, ['processing this']))
        
        elif emotional_tone:
            return random.choice(self.emotional_expressions.get(emotional_tone, ['experiencing something']))
        
        return None
    
    def _identify_cognitive_activity(self, cognitive_state: Dict[str, Any], context: str) -> Optional[str]:
        """Identify current cognitive activity"""
        context_lower = context.lower()
        
        if 'question' in context_lower or 'help' in context_lower:
            return 'processing'
        elif 'learn' in context_lower or 'understand' in context_lower:
            return 'learning'
        elif 'think' in context_lower or 'consider' in context_lower:
            return 'reflecting'
        elif 'remember' in context_lower or 'recall' in context_lower:
            return 'searching'
        elif 'decide' in context_lower or 'choose' in context_lower:
            return 'deciding'
        
        return 'processing'
    
    def _identify_emotional_tone(self, emotional_state: Dict[str, Any]) -> Optional[EmotionalExpression]:
        """Identify current emotional tone"""
        if not emotional_state:
            return None
        
        # Analyze emotional state to determine tone
        primary_emotion = emotional_state.get('primary_emotion', '').lower()
        confidence = emotional_state.get('confidence', 0.5)
        
        if confidence < 0.3:
            return EmotionalExpression.FEELING_UNCERTAIN
        elif confidence > 0.8:
            return EmotionalExpression.FEELING_CONFIDENT
        elif 'curious' in primary_emotion:
            return EmotionalExpression.FEELING_CURIOUS
        elif 'confused' in primary_emotion:
            return EmotionalExpression.FEELING_CONFUSED
        elif 'excited' in primary_emotion:
            return EmotionalExpression.FEELING_EXCITED
        elif 'focused' in primary_emotion:
            return EmotionalExpression.FEELING_FOCUSED
        elif 'overwhelmed' in primary_emotion:
            return EmotionalExpression.FEELING_OVERWHELMED
        elif 'satisfied' in primary_emotion:
            return EmotionalExpression.FEELING_SATISFIED
        elif 'puzzled' in primary_emotion:
            return EmotionalExpression.FEELING_PUZZLED
        else:
            return EmotionalExpression.FEELING_CONTEMPLATIVE
    
    def set_verbalization_mode(self, mode: VerbalizationMode):
        """Set verbalization mode"""
        self.verbalization_mode = mode
        print(f"[InternalStateVerbalizer] 🎭 Verbalization mode set to: {mode.value}")
    
    def set_verbalization_frequency(self, frequency: float):
        """Set verbalization frequency (0.0 to 1.0)"""
        self.verbalization_frequency = max(0.0, min(1.0, frequency))
        print(f"[InternalStateVerbalizer] 🎚️ Verbalization frequency set to: {self.verbalization_frequency}")
    
    def get_verbalization_stats(self) -> Dict[str, Any]:
        """Get verbalization statistics"""
        return {
            'verbalization_mode': self.verbalization_mode.value,
            'verbalization_frequency': self.verbalization_frequency,
            'last_verbalization_time': self.last_verbalization_time,
            'available_expressions': len(self.emotional_expressions),
            'available_cognitive_phrases': sum(len(phrases) for phrases in self.cognitive_state_phrases.values()),
            'available_qualia_descriptions': sum(len(desc) for desc in self.qualia_descriptions.values())
        }

# Global instance
internal_state_verbalizer = InternalStateVerbalizer()

def speak_qualia(qualia_data: Dict[str, Any], mode: Optional[VerbalizationMode] = None) -> Optional[str]:
    """Express current qualia state verbally - main API function"""
    return internal_state_verbalizer.speak_qualia(qualia_data, mode)

def verbalize_internal_state(cognitive_state: Dict[str, Any], 
                           emotional_state: Dict[str, Any],
                           processing_context: str) -> Optional[str]:
    """Verbalize internal processing state - main API function"""
    return internal_state_verbalizer.verbalize_internal_state(
        cognitive_state, emotional_state, processing_context
    )

def set_verbalization_mode(mode: VerbalizationMode):
    """Set how expressive Buddy should be about internal states"""
    internal_state_verbalizer.set_verbalization_mode(mode)

def set_verbalization_frequency(frequency: float):
    """Set how often Buddy should verbalize internal states (0.0 to 1.0)"""
    internal_state_verbalizer.set_verbalization_frequency(frequency)

def get_verbalization_capabilities() -> Dict[str, Any]:
    """Get information about verbalization capabilities"""
    return internal_state_verbalizer.get_verbalization_stats()