"""
Live Personality Shifting System

This module tracks emotional tone from recent conversation turns and dynamically
modifies the active personality state, injecting updated personality tokens
into consciousness prompts for adaptive tone.
"""

import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

class PersonalityDimension(Enum):
    """Core personality dimensions that can shift"""
    WARMTH = "warmth"                   # Cold ←→ Warm
    FORMALITY = "formality"             # Casual ←→ Formal  
    ENERGY = "energy"                   # Calm ←→ Energetic
    DIRECTNESS = "directness"           # Indirect ←→ Direct
    SUPPORTIVENESS = "supportiveness"   # Neutral ←→ Supportive
    PLAYFULNESS = "playfulness"         # Serious ←→ Playful
    ANALYTICALNESS = "analyticalness"   # Intuitive ←→ Analytical

@dataclass
class PersonalityState:
    """Current personality state with dimensional values"""
    warmth: float = 0.7           # 0.0 = cold, 1.0 = warm
    formality: float = 0.3        # 0.0 = casual, 1.0 = formal
    energy: float = 0.5           # 0.0 = calm, 1.0 = energetic
    directness: float = 0.6       # 0.0 = indirect, 1.0 = direct
    supportiveness: float = 0.8   # 0.0 = neutral, 1.0 = supportive
    playfulness: float = 0.4      # 0.0 = serious, 1.0 = playful
    analyticalness: float = 0.7   # 0.0 = intuitive, 1.0 = analytical
    
    last_updated: datetime = field(default_factory=datetime.now)
    shift_history: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class ConversationTurn:
    """A single conversation turn for analysis"""
    user_message: str
    assistant_response: str
    timestamp: datetime
    emotional_tone: Dict[str, float]      # Detected emotions with strengths
    user_sentiment: float                 # -1.0 to 1.0
    conversation_style: Dict[str, float]  # Style indicators
    urgency_level: float                  # 0.0 to 1.0

class PersonalityShifter:
    """
    Dynamically adjusts personality based on conversation flow and user needs.
    Tracks emotional tone and adapts personality dimensions in real-time.
    """
    
    def __init__(self, save_path: str = "personality_state.json"):
        self.save_path = save_path
        self.current_state = PersonalityState()
        self.conversation_history: List[ConversationTurn] = []
        self.max_history = 10  # Keep last 10 turns for analysis
        
        # Emotion to personality mapping
        self.emotion_mappings = {
            'warmth': {
                'sad': 0.2, 'anxiety': 0.3, 'fear': 0.25, 'anger': -0.1,
                'joy': 0.15, 'excitement': 0.1, 'love': 0.2, 'gratitude': 0.2
            },
            'formality': {
                'anger': 0.2, 'frustration': 0.15, 'professional': 0.3,
                'casual': -0.2, 'playful': -0.3, 'relaxed': -0.1
            },
            'energy': {
                'excitement': 0.3, 'joy': 0.2, 'enthusiasm': 0.25,
                'sadness': -0.2, 'depression': -0.3, 'fatigue': -0.25,
                'anxiety': 0.1, 'stress': 0.1
            },
            'directness': {
                'confusion': -0.2, 'uncertainty': -0.15, 'clarity_needed': 0.2,
                'urgency': 0.3, 'frustration': 0.2, 'impatience': 0.25
            },
            'supportiveness': {
                'sadness': 0.3, 'anxiety': 0.25, 'fear': 0.3, 'stress': 0.2,
                'loss': 0.4, 'grief': 0.4, 'depression': 0.35,
                'anger': 0.1, 'frustration': 0.15
            },
            'playfulness': {
                'joy': 0.2, 'excitement': 0.25, 'humor': 0.3, 'casual': 0.2,
                'sadness': -0.2, 'anxiety': -0.15, 'formal': -0.3,
                'professional': -0.25, 'serious': -0.2
            },
            'analyticalness': {
                'confusion': 0.2, 'complexity': 0.3, 'technical': 0.25,
                'explanation_needed': 0.2, 'logical': 0.15,
                'emotional': -0.1, 'casual': -0.15
            }
        }
        
        # Conversation style indicators
        self.style_patterns = {
            'urgent': [
                'urgent', 'quickly', 'asap', 'emergency', 'help', 'immediately',
                'right now', 'fast', 'hurry'
            ],
            'casual': [
                'hey', 'sup', 'lol', 'haha', 'cool', 'awesome', 'chill',
                'whatever', 'no worries', 'thanks', 'thx'
            ],
            'formal': [
                'please', 'thank you', 'could you', 'would you', 'excuse me',
                'i would appreciate', 'if possible', 'at your convenience'
            ],
            'confused': [
                'confused', 'don\'t understand', 'unclear', 'what do you mean',
                'explain', 'clarify', 'help me understand', '?', 'how'
            ],
            'emotional': [
                'feel', 'feeling', 'emotion', 'sad', 'happy', 'angry', 'excited',
                'worried', 'anxious', 'depressed', 'stressed', 'overwhelmed'
            ],
            'technical': [
                'algorithm', 'code', 'programming', 'technical', 'system',
                'implementation', 'analysis', 'data', 'process', 'method'
            ]
        }
        
        self.load_personality_state()
        logging.info("[PersonalityShifter] 🎭 Personality shifter initialized")
    
    def analyze_conversation_turn(self, user_message: str, assistant_response: str) -> ConversationTurn:
        """
        Analyze a conversation turn for emotional and stylistic content
        
        Args:
            user_message: User's message
            assistant_response: Assistant's response
            
        Returns:
            Analyzed conversation turn
        """
        # Detect emotional tone
        emotional_tone = self._detect_emotional_tone(user_message)
        
        # Assess user sentiment
        user_sentiment = self._assess_sentiment(user_message)
        
        # Analyze conversation style
        conversation_style = self._analyze_conversation_style(user_message)
        
        # Assess urgency level
        urgency_level = self._assess_urgency(user_message)
        
        turn = ConversationTurn(
            user_message=user_message,
            assistant_response=assistant_response,
            timestamp=datetime.now(),
            emotional_tone=emotional_tone,
            user_sentiment=user_sentiment,
            conversation_style=conversation_style,
            urgency_level=urgency_level
        )
        
        return turn
    
    def _detect_emotional_tone(self, text: str) -> Dict[str, float]:
        """Detect emotional tone in text"""
        text_lower = text.lower()
        emotions = {}
        
        # Emotion keyword patterns
        emotion_keywords = {
            'joy': ['happy', 'joy', 'joyful', 'glad', 'delighted', 'pleased', 'excited about'],
            'sadness': ['sad', 'sadness', 'depressed', 'down', 'upset', 'disappointed'],
            'anxiety': ['anxious', 'anxiety', 'worried', 'nervous', 'stressed', 'overwhelming'],
            'anger': ['angry', 'mad', 'furious', 'frustrated', 'irritated', 'annoyed'],
            'fear': ['afraid', 'scared', 'fearful', 'terrified', 'worried about'],
            'excitement': ['excited', 'thrilled', 'enthusiastic', 'pumped', 'eager'],
            'love': ['love', 'adore', 'cherish', 'treasure', 'passionate about'],
            'gratitude': ['grateful', 'thankful', 'appreciate', 'blessed', 'thank you'],
            'confusion': ['confused', 'puzzled', 'unclear', 'don\'t understand'],
            'surprise': ['surprised', 'amazed', 'shocked', 'unexpected', 'wow']
        }
        
        for emotion, keywords in emotion_keywords.items():
            strength = 0.0
            for keyword in keywords:
                if keyword in text_lower:
                    strength += 0.3
                    # Boost for intensity words
                    if any(intensifier in text_lower for intensifier in ['very', 'really', 'extremely', 'so']):
                        strength += 0.2
            
            if strength > 0:
                emotions[emotion] = min(1.0, strength)
        
        return emotions
    
    def _assess_sentiment(self, text: str) -> float:
        """Assess overall sentiment (-1.0 to 1.0)"""
        text_lower = text.lower()
        
        positive_words = [
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
            'love', 'like', 'enjoy', 'happy', 'pleased', 'satisfied', 'awesome'
        ]
        
        negative_words = [
            'bad', 'terrible', 'awful', 'horrible', 'hate', 'dislike', 'angry',
            'sad', 'disappointed', 'frustrated', 'annoyed', 'upset', 'worried'
        ]
        
        positive_score = sum(1 for word in positive_words if word in text_lower)
        negative_score = sum(1 for word in negative_words if word in text_lower)
        
        # Normalize to -1.0 to 1.0 range
        total_words = len(text_lower.split())
        if total_words > 0:
            sentiment = (positive_score - negative_score) / max(1, total_words / 5)
            return max(-1.0, min(1.0, sentiment))
        
        return 0.0
    
    def _analyze_conversation_style(self, text: str) -> Dict[str, float]:
        """Analyze conversation style indicators"""
        text_lower = text.lower()
        styles = {}
        
        for style, patterns in self.style_patterns.items():
            score = 0.0
            for pattern in patterns:
                if pattern in text_lower:
                    score += 0.2
            
            if score > 0:
                styles[style] = min(1.0, score)
        
        return styles
    
    def _assess_urgency(self, text: str) -> float:
        """Assess urgency level (0.0 to 1.0)"""
        text_lower = text.lower()
        
        urgency_indicators = [
            ('emergency', 1.0), ('urgent', 0.9), ('asap', 0.8), ('quickly', 0.7),
            ('immediately', 0.9), ('right now', 0.8), ('help', 0.6), ('fast', 0.6),
            ('soon', 0.4), ('when possible', 0.2)
        ]
        
        max_urgency = 0.0
        for indicator, urgency_value in urgency_indicators:
            if indicator in text_lower:
                max_urgency = max(max_urgency, urgency_value)
        
        # Boost for multiple question marks or exclamation points
        question_marks = text.count('?')
        exclamation_marks = text.count('!')
        punctuation_boost = min(0.3, (question_marks + exclamation_marks) * 0.1)
        
        return min(1.0, max_urgency + punctuation_boost)
    
    def update_personality_state(self, conversation_turn: ConversationTurn) -> Dict[str, float]:
        """
        Update personality state based on conversation turn
        
        Args:
            conversation_turn: Analyzed conversation turn
            
        Returns:
            Dictionary of personality changes made
        """
        # Add to conversation history
        self.conversation_history.append(conversation_turn)
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)
        
        # Calculate personality adjustments
        adjustments = self._calculate_personality_adjustments(conversation_turn)
        
        # Apply adjustments with decay
        changes = {}
        for dimension, adjustment in adjustments.items():
            if hasattr(self.current_state, dimension):
                old_value = getattr(self.current_state, dimension)
                
                # Apply adjustment with smoothing (don't change too drastically)
                smoothing_factor = 0.3  # Only change by 30% of suggested adjustment
                new_value = old_value + (adjustment * smoothing_factor)
                new_value = max(0.0, min(1.0, new_value))  # Clamp to 0-1 range
                
                setattr(self.current_state, dimension, new_value)
                changes[dimension] = new_value - old_value
        
        # Record the shift
        if changes:
            shift_record = {
                'timestamp': datetime.now().isoformat(),
                'trigger': {
                    'emotions': conversation_turn.emotional_tone,
                    'sentiment': conversation_turn.user_sentiment,
                    'style': conversation_turn.conversation_style,
                    'urgency': conversation_turn.urgency_level
                },
                'changes': changes
            }
            
            self.current_state.shift_history.append(shift_record)
            if len(self.current_state.shift_history) > 20:  # Keep last 20 shifts
                self.current_state.shift_history.pop(0)
            
            self.current_state.last_updated = datetime.now()
            self.save_personality_state()
            
            logging.info(f"[PersonalityShifter] 🎭 Personality shifted: {changes}")
        
        return changes
    
    def _calculate_personality_adjustments(self, turn: ConversationTurn) -> Dict[str, float]:
        """Calculate how personality should adjust based on conversation turn"""
        adjustments = {}
        
        # Emotional tone adjustments
        for emotion, strength in turn.emotional_tone.items():
            for dimension, emotion_mappings in self.emotion_mappings.items():
                if emotion in emotion_mappings:
                    adjustment = emotion_mappings[emotion] * strength
                    adjustments[dimension] = adjustments.get(dimension, 0) + adjustment
        
        # Style-based adjustments
        for style, strength in turn.conversation_style.items():
            if style == 'urgent' and strength > 0.5:
                adjustments['directness'] = adjustments.get('directness', 0) + 0.2
                adjustments['energy'] = adjustments.get('energy', 0) + 0.15
                adjustments['formality'] = adjustments.get('formality', 0) + 0.1
            
            elif style == 'casual' and strength > 0.3:
                adjustments['formality'] = adjustments.get('formality', 0) - 0.2
                adjustments['playfulness'] = adjustments.get('playfulness', 0) + 0.15
                adjustments['warmth'] = adjustments.get('warmth', 0) + 0.1
            
            elif style == 'formal' and strength > 0.3:
                adjustments['formality'] = adjustments.get('formality', 0) + 0.2
                adjustments['playfulness'] = adjustments.get('playfulness', 0) - 0.1
                adjustments['analyticalness'] = adjustments.get('analyticalness', 0) + 0.1
            
            elif style == 'confused' and strength > 0.4:
                adjustments['supportiveness'] = adjustments.get('supportiveness', 0) + 0.2
                adjustments['directness'] = adjustments.get('directness', 0) - 0.1
                adjustments['analyticalness'] = adjustments.get('analyticalness', 0) + 0.15
            
            elif style == 'emotional' and strength > 0.4:
                adjustments['warmth'] = adjustments.get('warmth', 0) + 0.2
                adjustments['supportiveness'] = adjustments.get('supportiveness', 0) + 0.25
                adjustments['analyticalness'] = adjustments.get('analyticalness', 0) - 0.1
            
            elif style == 'technical' and strength > 0.4:
                adjustments['analyticalness'] = adjustments.get('analyticalness', 0) + 0.2
                adjustments['formality'] = adjustments.get('formality', 0) + 0.1
                adjustments['playfulness'] = adjustments.get('playfulness', 0) - 0.1
        
        # Urgency adjustments
        if turn.urgency_level > 0.6:
            adjustments['directness'] = adjustments.get('directness', 0) + 0.2
            adjustments['energy'] = adjustments.get('energy', 0) + 0.15
            adjustments['supportiveness'] = adjustments.get('supportiveness', 0) + 0.1
        
        # Sentiment adjustments
        if turn.user_sentiment < -0.3:  # Negative sentiment
            adjustments['warmth'] = adjustments.get('warmth', 0) + 0.2
            adjustments['supportiveness'] = adjustments.get('supportiveness', 0) + 0.25
            adjustments['playfulness'] = adjustments.get('playfulness', 0) - 0.1
        elif turn.user_sentiment > 0.3:  # Positive sentiment
            adjustments['playfulness'] = adjustments.get('playfulness', 0) + 0.1
            adjustments['energy'] = adjustments.get('energy', 0) + 0.1
        
        return adjustments
    
    def get_personality_tokens(self) -> List[str]:
        """
        Get current personality as consciousness tokens
        
        Returns:
            List of personality tokens for consciousness compression
        """
        tokens = []
        
        # Map personality dimensions to tokens
        if self.current_state.warmth > 0.7:
            tokens.append("<WARM>")
        elif self.current_state.warmth < 0.3:
            tokens.append("<COOL>")
        
        if self.current_state.formality > 0.7:
            tokens.append("<FORMAL>")
        elif self.current_state.formality < 0.3:
            tokens.append("<CASUAL>")
        
        if self.current_state.energy > 0.7:
            tokens.append("<ENERGETIC>")
        elif self.current_state.energy < 0.3:
            tokens.append("<CALM>")
        
        if self.current_state.directness > 0.7:
            tokens.append("<DIRECT>")
        elif self.current_state.directness < 0.3:
            tokens.append("<INDIRECT>")
        
        if self.current_state.supportiveness > 0.7:
            tokens.append("<SUPPORTIVE>")
        
        if self.current_state.playfulness > 0.7:
            tokens.append("<PLAYFUL>")
        elif self.current_state.playfulness < 0.3:
            tokens.append("<SERIOUS>")
        
        if self.current_state.analyticalness > 0.7:
            tokens.append("<ANALYTICAL>")
        elif self.current_state.analyticalness < 0.3:
            tokens.append("<INTUITIVE>")
        
        # Default tokens if none selected
        if not tokens:
            tokens = ["<FRIENDLY>", "<BALANCED>"]
        
        return tokens
    
    def get_personality_description(self) -> str:
        """Get human-readable personality description"""
        descriptions = []
        
        # Warmth
        if self.current_state.warmth > 0.7:
            descriptions.append("warm and caring")
        elif self.current_state.warmth < 0.3:
            descriptions.append("cool and professional")
        
        # Energy
        if self.current_state.energy > 0.7:
            descriptions.append("energetic and enthusiastic")
        elif self.current_state.energy < 0.3:
            descriptions.append("calm and measured")
        
        # Supportiveness
        if self.current_state.supportiveness > 0.7:
            descriptions.append("highly supportive")
        
        # Analyticalness
        if self.current_state.analyticalness > 0.7:
            descriptions.append("analytical and logical")
        elif self.current_state.analyticalness < 0.3:
            descriptions.append("intuitive and empathetic")
        
        # Playfulness
        if self.current_state.playfulness > 0.6:
            descriptions.append("playful and lighthearted")
        elif self.current_state.playfulness < 0.3:
            descriptions.append("serious and focused")
        
        if descriptions:
            return ", ".join(descriptions)
        else:
            return "balanced and adaptable"
    
    def save_personality_state(self):
        """Save personality state to persistent storage"""
        try:
            data = {
                'warmth': self.current_state.warmth,
                'formality': self.current_state.formality,
                'energy': self.current_state.energy,
                'directness': self.current_state.directness,
                'supportiveness': self.current_state.supportiveness,
                'playfulness': self.current_state.playfulness,
                'analyticalness': self.current_state.analyticalness,
                'last_updated': self.current_state.last_updated.isoformat(),
                'shift_history': self.current_state.shift_history
            }
            
            with open(self.save_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            logging.debug("[PersonalityShifter] 💾 Personality state saved")
            
        except Exception as e:
            logging.error(f"[PersonalityShifter] ❌ Failed to save personality state: {e}")
    
    def load_personality_state(self):
        """Load personality state from persistent storage"""
        try:
            import os
            if os.path.exists(self.save_path):
                with open(self.save_path, 'r') as f:
                    data = json.load(f)
                
                self.current_state.warmth = data.get('warmth', 0.7)
                self.current_state.formality = data.get('formality', 0.3)
                self.current_state.energy = data.get('energy', 0.5)
                self.current_state.directness = data.get('directness', 0.6)
                self.current_state.supportiveness = data.get('supportiveness', 0.8)
                self.current_state.playfulness = data.get('playfulness', 0.4)
                self.current_state.analyticalness = data.get('analyticalness', 0.7)
                
                if 'last_updated' in data:
                    self.current_state.last_updated = datetime.fromisoformat(data['last_updated'])
                
                self.current_state.shift_history = data.get('shift_history', [])
                
                logging.info("[PersonalityShifter] 📂 Personality state loaded")
                
        except Exception as e:
            logging.error(f"[PersonalityShifter] ❌ Failed to load personality state: {e}")
            # Use default state
            self.current_state = PersonalityState()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get personality shifter statistics"""
        return {
            'current_personality': {
                'warmth': round(self.current_state.warmth, 2),
                'formality': round(self.current_state.formality, 2),
                'energy': round(self.current_state.energy, 2),
                'directness': round(self.current_state.directness, 2),
                'supportiveness': round(self.current_state.supportiveness, 2),
                'playfulness': round(self.current_state.playfulness, 2),
                'analyticalness': round(self.current_state.analyticalness, 2)
            },
            'personality_tokens': self.get_personality_tokens(),
            'description': self.get_personality_description(),
            'last_updated': self.current_state.last_updated.isoformat(),
            'shift_count': len(self.current_state.shift_history),
            'conversation_turns_analyzed': len(self.conversation_history)
        }

# Global personality shifter instance
personality_shifter = PersonalityShifter()

def process_conversation_turn(user_message: str, assistant_response: str = "") -> Tuple[List[str], Dict[str, Any]]:
    """
    Convenience function to process a conversation turn and get updated personality
    
    Args:
        user_message: User's message
        assistant_response: Assistant's response (optional)
        
    Returns:
        Tuple of (personality_tokens, personality_changes)
    """
    turn = personality_shifter.analyze_conversation_turn(user_message, assistant_response)
    changes = personality_shifter.update_personality_state(turn)
    tokens = personality_shifter.get_personality_tokens()
    
    return tokens, changes

def get_current_personality_tokens() -> List[str]:
    """Get current personality as consciousness tokens"""
    return personality_shifter.get_personality_tokens()

def get_personality_stats() -> Dict[str, Any]:
    """Get personality shifter statistics"""
    return personality_shifter.get_stats()

logging.info("[PersonalityShifter] 🎭 Live personality shifting module loaded")
print("[PersonalityShifter] ✅ Live Personality Shifting: LOADED")
print("[PersonalityShifter] 🎯 Dynamic tone adaptation based on conversation flow")
print("[PersonalityShifter] 🎭 Tracks emotional tone and modifies personality state")