"""
Live Personality Shifting System
Dynamically adapts personality based on conversation flow and emotional tone.
"""

import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import re

class PersonalityTrait(Enum):
    """Core personality traits that can shift dynamically"""
    FRIENDLY = "friendly"
    ANALYTICAL = "analytical"
    EMPATHETIC = "empathetic"
    CASUAL = "casual"
    ENTHUSIASTIC = "enthusiastic"
    SUPPORTIVE = "supportive"
    CURIOUS = "curious"
    CONFIDENT = "confident"
    CREATIVE = "creative"
    PROFESSIONAL = "professional"
    HUMOROUS = "humorous"
    PATIENT = "patient"

class EmotionalTone(Enum):
    """Emotional tones detected from conversation"""
    EXCITED = "excited"
    HAPPY = "happy"
    SAD = "sad"
    FRUSTRATED = "frustrated"
    ANXIOUS = "anxious"
    CONFUSED = "confused"
    CALM = "calm"
    ANGRY = "angry"
    NEUTRAL = "neutral"
    CURIOUS = "curious"
    DISAPPOINTED = "disappointed"
    ENTHUSIASTIC = "enthusiastic"

@dataclass
class PersonalityState:
    """Current personality state with trait intensities"""
    traits: Dict[PersonalityTrait, float]  # trait -> intensity (0.0 to 1.0)
    dominant_traits: List[PersonalityTrait]  # top 3 traits
    emotional_tone: EmotionalTone
    adaptation_reason: str
    timestamp: str
    confidence: float = 0.8

@dataclass
class ConversationTurn:
    """A single conversation turn for analysis"""
    user_input: str
    detected_emotion: EmotionalTone
    keywords: List[str]
    sentiment_score: float  # -1.0 (negative) to 1.0 (positive)
    urgency_level: float    # 0.0 (low) to 1.0 (high)
    complexity_level: float # 0.0 (simple) to 1.0 (complex)
    timestamp: str

class LivePersonalityShifter:
    """
    Live Personality Shifting System
    
    Analyzes conversation flow and emotional tone to dynamically adapt
    personality traits for more natural and contextually appropriate responses.
    """
    
    def __init__(self, base_personality: Optional[Dict[PersonalityTrait, float]] = None):
        # Default base personality
        self.base_personality = base_personality or {
            PersonalityTrait.FRIENDLY: 0.8,
            PersonalityTrait.CASUAL: 0.7,
            PersonalityTrait.SUPPORTIVE: 0.6,
            PersonalityTrait.CURIOUS: 0.5,
            PersonalityTrait.EMPATHETIC: 0.6
        }
        
        self.current_personality = PersonalityState(
            traits=self.base_personality.copy(),
            dominant_traits=self._get_dominant_traits(self.base_personality),
            emotional_tone=EmotionalTone.NEUTRAL,
            adaptation_reason="base_personality",
            timestamp=datetime.now().isoformat()
        )
        
        self.conversation_history: List[ConversationTurn] = []
        self.personality_history: List[PersonalityState] = []
        
        # Emotional keywords for tone detection
        self.emotion_keywords = self._initialize_emotion_keywords()
        
        logging.info("[PersonalityShifter] 🎭 Live personality shifting initialized")
    
    def _initialize_emotion_keywords(self) -> Dict[EmotionalTone, List[str]]:
        """Initialize emotional keyword mappings"""
        return {
            EmotionalTone.EXCITED: ["amazing", "awesome", "fantastic", "incredible", "wow", "exciting", "thrilled", "pumped"],
            EmotionalTone.HAPPY: ["happy", "great", "good", "wonderful", "nice", "pleasant", "lovely", "cheerful"],
            EmotionalTone.SAD: ["sad", "down", "depressed", "upset", "disappointed", "hurt", "gloomy", "terrible"],
            EmotionalTone.FRUSTRATED: ["frustrated", "annoying", "irritating", "stuck", "difficult", "confusing", "ugh"],
            EmotionalTone.ANXIOUS: ["worried", "nervous", "anxious", "stressed", "concerned", "afraid", "scared"],
            EmotionalTone.CONFUSED: ["confused", "lost", "unclear", "don't understand", "what", "how", "puzzled"],
            EmotionalTone.CALM: ["calm", "peaceful", "relaxed", "fine", "okay", "steady", "chill"],
            EmotionalTone.ANGRY: ["angry", "mad", "furious", "hate", "stupid", "ridiculous", "outrageous"],
            EmotionalTone.CURIOUS: ["interesting", "wonder", "curious", "how does", "why", "what if", "tell me"],
            EmotionalTone.ENTHUSIASTIC: ["love", "passionate", "interested", "keen", "eager", "motivated"]
        }
    
    def analyze_conversation_turn(self, user_input: str) -> ConversationTurn:
        """
        Analyze a conversation turn for emotional tone and characteristics
        
        Args:
            user_input: User's input text
            
        Returns:
            ConversationTurn object with analysis
        """
        user_input_lower = user_input.lower()
        
        # Detect emotional tone
        detected_emotion = self._detect_emotional_tone(user_input_lower)
        
        # Extract keywords
        keywords = self._extract_keywords(user_input_lower)
        
        # Calculate sentiment score
        sentiment_score = self._calculate_sentiment_score(user_input_lower)
        
        # Calculate urgency level
        urgency_level = self._calculate_urgency_level(user_input_lower)
        
        # Calculate complexity level
        complexity_level = self._calculate_complexity_level(user_input)
        
        turn = ConversationTurn(
            user_input=user_input,
            detected_emotion=detected_emotion,
            keywords=keywords,
            sentiment_score=sentiment_score,
            urgency_level=urgency_level,
            complexity_level=complexity_level,
            timestamp=datetime.now().isoformat()
        )
        
        self.conversation_history.append(turn)
        
        # Keep only last 10 turns for analysis
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
        
        return turn
    
    def _detect_emotional_tone(self, text: str) -> EmotionalTone:
        """Detect emotional tone from text"""
        emotion_scores = {}
        
        for emotion, keywords in self.emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                emotion_scores[emotion] = score
        
        if not emotion_scores:
            return EmotionalTone.NEUTRAL
        
        # Return emotion with highest score
        return max(emotion_scores, key=emotion_scores.get)
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text"""
        # Simple keyword extraction - can be enhanced
        words = re.findall(r'\b\w+\b', text)
        
        # Filter out common words
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "are", "was", "were", "been", "be", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should", "can", "may", "might", "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them"}
        
        keywords = [word for word in words if len(word) > 3 and word not in stop_words]
        return keywords[:10]  # Return top 10 keywords
    
    def _calculate_sentiment_score(self, text: str) -> float:
        """Calculate sentiment score (-1.0 to 1.0)"""
        positive_words = ["good", "great", "awesome", "amazing", "love", "like", "enjoy", "happy", "excellent", "wonderful", "fantastic", "perfect", "brilliant"]
        negative_words = ["bad", "terrible", "awful", "hate", "dislike", "horrible", "worst", "stupid", "annoying", "frustrated", "disappointed", "sad"]
        
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        
        total_count = positive_count + negative_count
        if total_count == 0:
            return 0.0
        
        return (positive_count - negative_count) / total_count
    
    def _calculate_urgency_level(self, text: str) -> float:
        """Calculate urgency level (0.0 to 1.0)"""
        urgency_indicators = ["urgent", "asap", "immediately", "now", "quick", "fast", "help", "emergency", "please", "!"]
        
        urgency_score = sum(1 for indicator in urgency_indicators if indicator in text)
        urgency_score += text.count("!") * 0.2  # Multiple exclamations increase urgency
        
        return min(1.0, urgency_score / 3.0)  # Normalize to 0-1
    
    def _calculate_complexity_level(self, text: str) -> float:
        """Calculate complexity level (0.0 to 1.0)"""
        # Simple complexity based on length and question words
        word_count = len(text.split())
        question_words = ["how", "why", "what", "when", "where", "which", "explain", "analyze", "complex"]
        
        complexity_score = 0.0
        
        # Length component
        if word_count > 50:
            complexity_score += 0.5
        elif word_count > 20:
            complexity_score += 0.3
        
        # Question complexity
        question_count = sum(1 for word in question_words if word in text.lower())
        complexity_score += min(0.5, question_count * 0.2)
        
        return min(1.0, complexity_score)
    
    def adapt_personality(self, conversation_turn: ConversationTurn) -> PersonalityState:
        """
        Adapt personality based on conversation turn and recent history
        
        Args:
            conversation_turn: Current conversation turn
            
        Returns:
            New personality state
        """
        # Start with base personality
        new_traits = self.base_personality.copy()
        adaptation_reason = "base_personality"
        
        # Get recent conversation context (last 3 turns)
        recent_turns = self.conversation_history[-3:]
        current_emotion = conversation_turn.detected_emotion
        
        # Adapt based on emotional tone
        emotion_adaptations = self._get_emotion_adaptations(current_emotion)
        for trait, adjustment in emotion_adaptations.items():
            new_traits[trait] = min(1.0, max(0.0, new_traits.get(trait, 0.5) + adjustment))
        
        adaptation_reason = f"emotion_{current_emotion.value}"
        
        # Adapt based on conversation flow
        if len(recent_turns) >= 2:
            flow_adaptations = self._analyze_conversation_flow(recent_turns)
            for trait, adjustment in flow_adaptations.items():
                new_traits[trait] = min(1.0, max(0.0, new_traits.get(trait, 0.5) + adjustment))
            
            if flow_adaptations:
                adaptation_reason += "_flow_adaptation"
        
        # Adapt based on complexity and urgency
        if conversation_turn.complexity_level > 0.6:
            new_traits[PersonalityTrait.ANALYTICAL] = min(1.0, new_traits.get(PersonalityTrait.ANALYTICAL, 0.5) + 0.2)
            new_traits[PersonalityTrait.PATIENT] = min(1.0, new_traits.get(PersonalityTrait.PATIENT, 0.5) + 0.2)
            adaptation_reason += "_complex"
        
        if conversation_turn.urgency_level > 0.6:
            new_traits[PersonalityTrait.CONFIDENT] = min(1.0, new_traits.get(PersonalityTrait.CONFIDENT, 0.5) + 0.2)
            new_traits[PersonalityTrait.PROFESSIONAL] = min(1.0, new_traits.get(PersonalityTrait.PROFESSIONAL, 0.5) + 0.2)
            adaptation_reason += "_urgent"
        
        # Create new personality state
        new_personality = PersonalityState(
            traits=new_traits,
            dominant_traits=self._get_dominant_traits(new_traits),
            emotional_tone=current_emotion,
            adaptation_reason=adaptation_reason,
            timestamp=datetime.now().isoformat(),
            confidence=0.8
        )
        
        self.current_personality = new_personality
        self.personality_history.append(new_personality)
        
        # Keep only last 5 personality states
        if len(self.personality_history) > 5:
            self.personality_history = self.personality_history[-5:]
        
        logging.debug(f"[PersonalityShifter] 🎭 Adapted personality: {adaptation_reason}, dominant traits: {[t.value for t in new_personality.dominant_traits]}")
        
        return new_personality
    
    def _get_emotion_adaptations(self, emotion: EmotionalTone) -> Dict[PersonalityTrait, float]:
        """Get personality trait adjustments for emotional tone"""
        adaptations = {
            EmotionalTone.EXCITED: {
                PersonalityTrait.ENTHUSIASTIC: 0.3,
                PersonalityTrait.FRIENDLY: 0.2,
                PersonalityTrait.CASUAL: 0.2
            },
            EmotionalTone.HAPPY: {
                PersonalityTrait.FRIENDLY: 0.2,
                PersonalityTrait.HUMOROUS: 0.2,
                PersonalityTrait.CASUAL: 0.1
            },
            EmotionalTone.SAD: {
                PersonalityTrait.EMPATHETIC: 0.4,
                PersonalityTrait.SUPPORTIVE: 0.3,
                PersonalityTrait.PATIENT: 0.2,
                PersonalityTrait.CASUAL: -0.2
            },
            EmotionalTone.FRUSTRATED: {
                PersonalityTrait.PATIENT: 0.3,
                PersonalityTrait.SUPPORTIVE: 0.3,
                PersonalityTrait.ANALYTICAL: 0.2,
                PersonalityTrait.HUMOROUS: -0.2
            },
            EmotionalTone.ANXIOUS: {
                PersonalityTrait.SUPPORTIVE: 0.4,
                PersonalityTrait.EMPATHETIC: 0.3,
                PersonalityTrait.PATIENT: 0.2,
                PersonalityTrait.CASUAL: -0.2
            },
            EmotionalTone.CONFUSED: {
                PersonalityTrait.PATIENT: 0.3,
                PersonalityTrait.ANALYTICAL: 0.2,
                PersonalityTrait.SUPPORTIVE: 0.2,
                PersonalityTrait.PROFESSIONAL: 0.1
            },
            EmotionalTone.ANGRY: {
                PersonalityTrait.PATIENT: 0.4,
                PersonalityTrait.EMPATHETIC: 0.2,
                PersonalityTrait.PROFESSIONAL: 0.2,
                PersonalityTrait.CASUAL: -0.3,
                PersonalityTrait.HUMOROUS: -0.3
            },
            EmotionalTone.CURIOUS: {
                PersonalityTrait.CURIOUS: 0.3,
                PersonalityTrait.ANALYTICAL: 0.2,
                PersonalityTrait.ENTHUSIASTIC: 0.2
            },
            EmotionalTone.ENTHUSIASTIC: {
                PersonalityTrait.ENTHUSIASTIC: 0.3,
                PersonalityTrait.CREATIVE: 0.2,
                PersonalityTrait.FRIENDLY: 0.2
            }
        }
        
        return adaptations.get(emotion, {})
    
    def _analyze_conversation_flow(self, recent_turns: List[ConversationTurn]) -> Dict[PersonalityTrait, float]:
        """Analyze conversation flow for personality adaptations"""
        adaptations = {}
        
        # Check for emotional consistency
        emotions = [turn.detected_emotion for turn in recent_turns]
        if len(set(emotions)) == 1:  # Consistent emotion
            emotion = emotions[0]
            if emotion in [EmotionalTone.SAD, EmotionalTone.FRUSTRATED, EmotionalTone.ANXIOUS]:
                adaptations[PersonalityTrait.EMPATHETIC] = 0.2
                adaptations[PersonalityTrait.SUPPORTIVE] = 0.2
        
        # Check for increasing complexity
        complexities = [turn.complexity_level for turn in recent_turns]
        if len(complexities) >= 2 and complexities[-1] > complexities[-2]:
            adaptations[PersonalityTrait.ANALYTICAL] = 0.1
            adaptations[PersonalityTrait.PATIENT] = 0.1
        
        # Check for increasing urgency
        urgencies = [turn.urgency_level for turn in recent_turns]
        if len(urgencies) >= 2 and urgencies[-1] > urgencies[-2]:
            adaptations[PersonalityTrait.CONFIDENT] = 0.1
            adaptations[PersonalityTrait.PROFESSIONAL] = 0.1
        
        return adaptations
    
    def _get_dominant_traits(self, traits: Dict[PersonalityTrait, float]) -> List[PersonalityTrait]:
        """Get top 3 dominant personality traits"""
        sorted_traits = sorted(traits.items(), key=lambda x: x[1], reverse=True)
        return [trait for trait, intensity in sorted_traits[:3] if intensity > 0.3]
    
    def get_personality_tokens(self) -> List[str]:
        """Get consciousness tokens for current personality state"""
        tokens = []
        
        # Map personality traits to consciousness tokens
        trait_token_mapping = {
            PersonalityTrait.FRIENDLY: "<FRIENDLY>",
            PersonalityTrait.ANALYTICAL: "<ANALYTICAL_P>",
            PersonalityTrait.EMPATHETIC: "<EMPATHETIC_P>",
            PersonalityTrait.CASUAL: "<CASUAL>",
            PersonalityTrait.ENTHUSIASTIC: "<EXCITED>",
            PersonalityTrait.SUPPORTIVE: "<HELPFUL_P>",
            PersonalityTrait.CURIOUS: "<CURIOUS_P>",
            PersonalityTrait.CONFIDENT: "<CONFIDENT>",
            PersonalityTrait.CREATIVE: "<CREATIVE_P>"
        }
        
        # Add tokens for dominant traits
        for trait in self.current_personality.dominant_traits:
            token = trait_token_mapping.get(trait)
            if token:
                tokens.append(token)
        
        return tokens
    
    def get_personality_description(self) -> str:
        """Get natural language description of current personality"""
        dominant_traits = self.current_personality.dominant_traits
        if not dominant_traits:
            return "balanced and adaptable personality"
        
        trait_descriptions = {
            PersonalityTrait.FRIENDLY: "warm and welcoming",
            PersonalityTrait.ANALYTICAL: "logical and systematic", 
            PersonalityTrait.EMPATHETIC: "understanding and compassionate",
            PersonalityTrait.CASUAL: "relaxed and informal",
            PersonalityTrait.ENTHUSIASTIC: "energetic and excited",
            PersonalityTrait.SUPPORTIVE: "helpful and encouraging",
            PersonalityTrait.CURIOUS: "inquisitive and interested",
            PersonalityTrait.CONFIDENT: "assured and decisive",
            PersonalityTrait.CREATIVE: "imaginative and innovative",
            PersonalityTrait.PROFESSIONAL: "formal and business-like",
            PersonalityTrait.HUMOROUS: "funny and light-hearted",
            PersonalityTrait.PATIENT: "calm and understanding"
        }
        
        descriptions = [trait_descriptions.get(trait, trait.value) for trait in dominant_traits[:2]]
        return " and ".join(descriptions) + " personality"
    
    def process_conversation_turn(self, user_input: str) -> Tuple[PersonalityState, List[str], str]:
        """
        Process a conversation turn and adapt personality
        
        Args:
            user_input: User's input text
            
        Returns:
            Tuple of (new_personality_state, personality_tokens, personality_description)
        """
        # Analyze the conversation turn
        turn = self.analyze_conversation_turn(user_input)
        
        # Adapt personality based on the turn
        new_personality = self.adapt_personality(turn)
        
        # Get tokens and description
        tokens = self.get_personality_tokens()
        description = self.get_personality_description()
        
        return new_personality, tokens, description
    
    def get_personality_summary(self) -> Dict[str, Any]:
        """Get summary of current personality state"""
        return {
            'dominant_traits': [trait.value for trait in self.current_personality.dominant_traits],
            'emotional_tone': self.current_personality.emotional_tone.value,
            'adaptation_reason': self.current_personality.adaptation_reason,
            'confidence': self.current_personality.confidence,
            'timestamp': self.current_personality.timestamp,
            'recent_adaptations': len(self.personality_history)
        }

# Global personality shifter instance
personality_shifter = LivePersonalityShifter()

def adapt_personality_for_conversation(user_input: str) -> Tuple[List[str], str]:
    """
    Adapt personality for conversation turn
    
    Args:
        user_input: User's input text
        
    Returns:
        Tuple of (personality_tokens, personality_description)
    """
    _, tokens, description = personality_shifter.process_conversation_turn(user_input)
    return tokens, description