"""
Auto-Generated Semantic Tags System

This module extracts intent, emotion, and topic from each message and stores
them as semantic tags in memory entries for smarter conversation categorization
and enhanced consciousness awareness.
"""

import re
import json
import logging
from typing import Dict, List, Any, Set, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

class IntentType(Enum):
    """Common conversation intents"""
    QUESTION = "question"
    REQUEST = "request"
    INFORMATION = "information"
    EMOTION_SHARING = "emotion_sharing"
    GREETING = "greeting"
    GOODBYE = "goodbye"
    THANKS = "thanks"
    COMPLAINT = "complaint"
    PRAISE = "praise"
    INSTRUCTION = "instruction"
    STORY = "story"
    OPINION = "opinion"
    CONFIRMATION = "confirmation"
    DENIAL = "denial"

class EmotionTag(Enum):
    """Emotional semantic tags"""
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    LOVE = "love"
    EXCITEMENT = "excitement"
    ANXIETY = "anxiety"
    FRUSTRATION = "frustration"
    CONTENTMENT = "contentment"
    CONFUSION = "confusion"
    CURIOSITY = "curiosity"
    GRATITUDE = "gratitude"
    DISAPPOINTMENT = "disappointment"
    RELIEF = "relief"

class TopicCategory(Enum):
    """Topic categories for conversation"""
    PERSONAL = "personal"
    WORK = "work"
    FAMILY = "family"
    HEALTH = "health"
    TECHNOLOGY = "technology"
    ENTERTAINMENT = "entertainment"
    EDUCATION = "education"
    TRAVEL = "travel"
    FOOD = "food"
    RELATIONSHIPS = "relationships"
    HOBBIES = "hobbies"
    NEWS = "news"
    WEATHER = "weather"
    EMOTIONS = "emotions"
    GOALS = "goals"
    MEMORIES = "memories"
    ADVICE = "advice"
    GENERAL = "general"

@dataclass
class SemanticTags:
    """Complete semantic analysis of a message"""
    intent: IntentType
    emotions: List[EmotionTag]
    topics: List[TopicCategory]
    keywords: List[str]
    sentiment_score: float  # -1.0 to 1.0
    urgency_level: float    # 0.0 to 1.0
    complexity_level: float # 0.0 to 1.0
    confidence_scores: Dict[str, float] = field(default_factory=dict)
    
class SemanticTagger:
    """
    Automatically generates semantic tags for conversation messages.
    Extracts intent, emotion, topic, and other semantic information.
    """
    
    def __init__(self):
        # Intent detection patterns
        self.intent_patterns = {
            IntentType.QUESTION: [
                r'\?', r'what', r'how', r'when', r'where', r'why', r'who',
                r'can you', r'could you', r'do you know', r'tell me'
            ],
            IntentType.REQUEST: [
                r'please', r'can you', r'could you', r'would you',
                r'help me', r'i need', r'i want you to'
            ],
            IntentType.GREETING: [
                r'\bhello\b', r'\bhi\b', r'\bhey\b', r'good morning',
                r'good afternoon', r'good evening', r'how are you'
            ],
            IntentType.GOODBYE: [
                r'\bbye\b', r'goodbye', r'see you', r'talk later',
                r'good night', r'farewell', r'take care'
            ],
            IntentType.THANKS: [
                r'thank you', r'thanks', r'grateful', r'appreciate',
                r'thx', r'ty'
            ],
            IntentType.COMPLAINT: [
                r'hate', r'terrible', r'awful', r'frustrated',
                r'annoyed', r'disappointed', r'problem with'
            ],
            IntentType.PRAISE: [
                r'great', r'amazing', r'wonderful', r'excellent',
                r'love it', r'fantastic', r'awesome'
            ],
            IntentType.EMOTION_SHARING: [
                r'i feel', r'i\'m feeling', r'i am', r'feeling',
                r'emotion', r'mood'
            ],
            IntentType.STORY: [
                r'yesterday', r'today', r'last week', r'happened',
                r'story', r'experience', r'remember when'
            ],
            IntentType.OPINION: [
                r'i think', r'in my opinion', r'i believe',
                r'my view', r'personally'
            ]
        }
        
        # Emotion detection patterns
        self.emotion_patterns = {
            EmotionTag.JOY: [
                'happy', 'joy', 'joyful', 'cheerful', 'delighted',
                'elated', 'glad', 'pleased', 'upbeat'
            ],
            EmotionTag.SADNESS: [
                'sad', 'sadness', 'down', 'depressed', 'melancholy',
                'blue', 'upset', 'disappointed', 'gloomy'
            ],
            EmotionTag.ANGER: [
                'angry', 'mad', 'furious', 'irritated', 'annoyed',
                'rage', 'frustrated', 'outraged'
            ],
            EmotionTag.FEAR: [
                'afraid', 'scared', 'fearful', 'terrified',
                'worried', 'anxious', 'nervous', 'frightened'
            ],
            EmotionTag.EXCITEMENT: [
                'excited', 'thrilled', 'enthusiastic', 'pumped',
                'energized', 'hyped', 'eager'
            ],
            EmotionTag.LOVE: [
                'love', 'adore', 'cherish', 'treasure',
                'passionate', 'devoted', 'affection'
            ],
            EmotionTag.ANXIETY: [
                'anxious', 'anxiety', 'stressed', 'tense',
                'overwhelmed', 'panicked', 'restless'
            ],
            EmotionTag.CURIOSITY: [
                'curious', 'wonder', 'interested', 'intrigued',
                'fascinated', 'questioning'
            ],
            EmotionTag.GRATITUDE: [
                'grateful', 'thankful', 'appreciate', 'blessed',
                'indebted', 'obliged'
            ],
            EmotionTag.CONFUSION: [
                'confused', 'puzzled', 'unclear', 'bewildered',
                'lost', 'perplexed'
            ]
        }
        
        # Topic detection patterns
        self.topic_patterns = {
            TopicCategory.WORK: [
                'job', 'work', 'office', 'boss', 'colleague', 'career',
                'profession', 'business', 'meeting', 'project'
            ],
            TopicCategory.FAMILY: [
                'family', 'mother', 'father', 'parent', 'child',
                'sibling', 'brother', 'sister', 'spouse', 'relative'
            ],
            TopicCategory.HEALTH: [
                'health', 'doctor', 'medical', 'medicine', 'sick',
                'illness', 'hospital', 'treatment', 'pain', 'wellness'
            ],
            TopicCategory.TECHNOLOGY: [
                'computer', 'technology', 'software', 'programming',
                'internet', 'app', 'digital', 'tech', 'AI'
            ],
            TopicCategory.ENTERTAINMENT: [
                'movie', 'music', 'game', 'book', 'show', 'film',
                'entertainment', 'fun', 'hobby', 'art'
            ],
            TopicCategory.FOOD: [
                'food', 'eat', 'restaurant', 'cooking', 'recipe',
                'meal', 'dinner', 'lunch', 'breakfast', 'cuisine'
            ],
            TopicCategory.TRAVEL: [
                'travel', 'trip', 'vacation', 'journey', 'visit',
                'destination', 'flight', 'hotel', 'adventure'
            ],
            TopicCategory.RELATIONSHIPS: [
                'relationship', 'dating', 'marriage', 'friendship',
                'partner', 'girlfriend', 'boyfriend', 'love'
            ],
            TopicCategory.EDUCATION: [
                'school', 'education', 'learning', 'study', 'class',
                'teacher', 'student', 'university', 'knowledge'
            ],
            TopicCategory.EMOTIONS: [
                'emotion', 'feeling', 'mood', 'sentiment', 'heart',
                'soul', 'mind', 'psychological'
            ],
            TopicCategory.GOALS: [
                'goal', 'dream', 'ambition', 'plan', 'future',
                'aspiration', 'objective', 'target'
            ],
            TopicCategory.MEMORIES: [
                'memory', 'remember', 'past', 'childhood', 'history',
                'nostalgia', 'reminisce', 'recall'
            ]
        }
        
        # Sentiment analysis words
        self.positive_words = [
            'good', 'great', 'excellent', 'amazing', 'wonderful',
            'fantastic', 'awesome', 'love', 'like', 'enjoy',
            'happy', 'pleased', 'satisfied', 'perfect'
        ]
        
        self.negative_words = [
            'bad', 'terrible', 'awful', 'horrible', 'hate',
            'dislike', 'angry', 'sad', 'disappointed', 'frustrated',
            'annoyed', 'upset', 'worried', 'anxious'
        ]
        
        # Urgency indicators
        self.urgency_indicators = [
            ('urgent', 1.0), ('emergency', 1.0), ('asap', 0.9),
            ('immediately', 0.9), ('quickly', 0.8), ('soon', 0.6),
            ('help', 0.7), ('problem', 0.6), ('issue', 0.5)
        ]
        
        logging.info("[SemanticTagger] 🏷️ Semantic tagger initialized")
    
    def analyze_message(self, text: str, context: str = "") -> SemanticTags:
        """
        Perform complete semantic analysis of a message
        
        Args:
            text: Message text to analyze
            context: Additional context information
            
        Returns:
            Complete semantic tags
        """
        text_lower = text.lower().strip()
        
        # Detect intent
        intent = self._detect_intent(text_lower)
        
        # Detect emotions
        emotions = self._detect_emotions(text_lower)
        
        # Detect topics
        topics = self._detect_topics(text_lower)
        
        # Extract keywords
        keywords = self._extract_keywords(text)
        
        # Calculate sentiment score
        sentiment_score = self._calculate_sentiment(text_lower)
        
        # Assess urgency level
        urgency_level = self._assess_urgency(text_lower)
        
        # Assess complexity
        complexity_level = self._assess_complexity(text)
        
        # Calculate confidence scores
        confidence_scores = {
            'intent': self._calculate_intent_confidence(intent, text_lower),
            'emotions': self._calculate_emotion_confidence(emotions, text_lower),
            'topics': self._calculate_topic_confidence(topics, text_lower)
        }
        
        return SemanticTags(
            intent=intent,
            emotions=emotions,
            topics=topics,
            keywords=keywords,
            sentiment_score=sentiment_score,
            urgency_level=urgency_level,
            complexity_level=complexity_level,
            confidence_scores=confidence_scores
        )
    
    def _detect_intent(self, text: str) -> IntentType:
        """Detect the primary intent of the message"""
        intent_scores = {}
        
        for intent, patterns in self.intent_patterns.items():
            score = 0.0
            for pattern in patterns:
                if re.search(pattern, text):
                    score += 1.0
                    # Boost for exact matches
                    if pattern in text:
                        score += 0.5
            
            if score > 0:
                intent_scores[intent] = score
        
        if intent_scores:
            # Return intent with highest score
            return max(intent_scores.items(), key=lambda x: x[1])[0]
        else:
            # Default intent based on structure
            if '?' in text:
                return IntentType.QUESTION
            elif any(word in text for word in ['i', 'my', 'me']):
                return IntentType.INFORMATION
            else:
                return IntentType.INFORMATION
    
    def _detect_emotions(self, text: str) -> List[EmotionTag]:
        """Detect emotions present in the message"""
        detected_emotions = []
        
        for emotion, patterns in self.emotion_patterns.items():
            for pattern in patterns:
                if pattern in text:
                    detected_emotions.append(emotion)
                    break  # One match per emotion type
        
        # If no specific emotions detected, try to infer from sentiment
        if not detected_emotions:
            if any(word in text for word in self.positive_words):
                detected_emotions.append(EmotionTag.JOY)
            elif any(word in text for word in self.negative_words):
                detected_emotions.append(EmotionTag.SADNESS)
        
        return detected_emotions
    
    def _detect_topics(self, text: str) -> List[TopicCategory]:
        """Detect topics discussed in the message"""
        detected_topics = []
        
        for topic, patterns in self.topic_patterns.items():
            for pattern in patterns:
                if pattern in text:
                    detected_topics.append(topic)
                    break  # One match per topic type
        
        # Default to general if no specific topics detected
        if not detected_topics:
            detected_topics.append(TopicCategory.GENERAL)
        
        return detected_topics
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text"""
        # Simple keyword extraction - could be enhanced with NLP
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Remove common stop words
        stop_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all',
            'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day',
            'get', 'has', 'him', 'his', 'how', 'its', 'may', 'new',
            'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did',
            'she', 'use', 'her', 'now', 'air', 'put', 'say', 'she',
            'too', 'any', 'man', 'new', 'now', 'old', 'see', 'two'
        }
        
        keywords = [word for word in words if word not in stop_words]
        
        # Return top keywords (by frequency if text is long enough)
        if len(keywords) > 10:
            # Count frequencies
            word_freq = {}
            for word in keywords:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            # Sort by frequency and return top 10
            sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
            return [word for word, freq in sorted_words[:10]]
        
        return keywords[:10]  # Limit to 10 keywords
    
    def _calculate_sentiment(self, text: str) -> float:
        """Calculate sentiment score (-1.0 to 1.0)"""
        positive_score = sum(1 for word in self.positive_words if word in text)
        negative_score = sum(1 for word in self.negative_words if word in text)
        
        # Factor in intensifiers
        intensifiers = ['very', 'really', 'extremely', 'so', 'quite', 'rather']
        intensifier_count = sum(1 for word in intensifiers if word in text)
        
        # Calculate base sentiment
        if positive_score > 0 or negative_score > 0:
            base_sentiment = (positive_score - negative_score) / (positive_score + negative_score + 1)
        else:
            base_sentiment = 0.0
        
        # Apply intensifier boost
        if intensifier_count > 0:
            base_sentiment *= (1 + intensifier_count * 0.2)
        
        # Clamp to [-1, 1] range
        return max(-1.0, min(1.0, base_sentiment))
    
    def _assess_urgency(self, text: str) -> float:
        """Assess urgency level (0.0 to 1.0)"""
        max_urgency = 0.0
        
        for indicator, urgency_value in self.urgency_indicators:
            if indicator in text:
                max_urgency = max(max_urgency, urgency_value)
        
        # Boost for punctuation
        question_marks = text.count('?')
        exclamation_marks = text.count('!')
        punctuation_boost = min(0.3, (question_marks + exclamation_marks) * 0.1)
        
        # Boost for capital letters (shouting)
        caps_ratio = sum(1 for c in text if c.isupper()) / max(1, len(text))
        caps_boost = min(0.2, caps_ratio * 0.5)
        
        total_urgency = max_urgency + punctuation_boost + caps_boost
        return min(1.0, total_urgency)
    
    def _assess_complexity(self, text: str) -> float:
        """Assess complexity level (0.0 to 1.0)"""
        words = text.split()
        
        if not words:
            return 0.0
        
        # Factors contributing to complexity
        avg_word_length = sum(len(word) for word in words) / len(words)
        sentence_count = len(re.findall(r'[.!?]', text)) or 1
        words_per_sentence = len(words) / sentence_count
        
        # Technical/complex words
        complex_words = [
            word for word in words 
            if len(word) > 7 and word.lower() not in self.positive_words + self.negative_words
        ]
        complex_word_ratio = len(complex_words) / len(words)
        
        # Normalize and combine factors
        complexity = (
            min(avg_word_length / 8, 1.0) * 0.3 +      # Word length factor
            min(words_per_sentence / 20, 1.0) * 0.3 +   # Sentence length factor
            complex_word_ratio * 0.4                     # Complex words factor
        )
        
        return min(1.0, complexity)
    
    def _calculate_intent_confidence(self, intent: IntentType, text: str) -> float:
        """Calculate confidence in intent detection"""
        if intent in self.intent_patterns:
            patterns = self.intent_patterns[intent]
            matches = sum(1 for pattern in patterns if re.search(pattern, text))
            return min(1.0, matches / len(patterns) * 2)  # Scale to 0-1
        return 0.5  # Default confidence
    
    def _calculate_emotion_confidence(self, emotions: List[EmotionTag], text: str) -> float:
        """Calculate confidence in emotion detection"""
        if not emotions:
            return 0.3  # Low confidence when no emotions detected
        
        total_confidence = 0.0
        for emotion in emotions:
            if emotion in self.emotion_patterns:
                patterns = self.emotion_patterns[emotion]
                matches = sum(1 for pattern in patterns if pattern in text)
                confidence = min(1.0, matches / len(patterns) * 3)
                total_confidence += confidence
        
        return min(1.0, total_confidence / len(emotions))
    
    def _calculate_topic_confidence(self, topics: List[TopicCategory], text: str) -> float:
        """Calculate confidence in topic detection"""
        if not topics or topics == [TopicCategory.GENERAL]:
            return 0.4  # Lower confidence for general topics
        
        total_confidence = 0.0
        for topic in topics:
            if topic in self.topic_patterns:
                patterns = self.topic_patterns[topic]
                matches = sum(1 for pattern in patterns if pattern in text)
                confidence = min(1.0, matches / len(patterns) * 2)
                total_confidence += confidence
        
        return min(1.0, total_confidence / len(topics))
    
    def get_tag_summary(self, tags: SemanticTags) -> str:
        """Get human-readable summary of semantic tags"""
        parts = []
        
        # Intent
        parts.append(f"Intent: {tags.intent.value}")
        
        # Emotions
        if tags.emotions:
            emotion_names = [e.value for e in tags.emotions]
            parts.append(f"Emotions: {', '.join(emotion_names)}")
        
        # Topics
        if tags.topics:
            topic_names = [t.value for t in tags.topics]
            parts.append(f"Topics: {', '.join(topic_names)}")
        
        # Sentiment
        if tags.sentiment_score != 0:
            sentiment_desc = "positive" if tags.sentiment_score > 0 else "negative"
            parts.append(f"Sentiment: {sentiment_desc} ({tags.sentiment_score:.2f})")
        
        # Urgency
        if tags.urgency_level > 0.5:
            parts.append(f"Urgency: {tags.urgency_level:.1f}")
        
        return "; ".join(parts)

# Global semantic tagger instance
semantic_tagger = SemanticTagger()

def tag_message(text: str, context: str = "") -> Tuple[SemanticTags, str]:
    """
    Convenience function to tag a message with semantic information
    
    Args:
        text: Message text to analyze
        context: Additional context
        
    Returns:
        Tuple of (semantic_tags, summary_string)
    """
    tags = semantic_tagger.analyze_message(text, context)
    summary = semantic_tagger.get_tag_summary(tags)
    
    return tags, summary

def get_consciousness_tags(tags: SemanticTags) -> List[str]:
    """
    Convert semantic tags to consciousness tokens for compression
    
    Args:
        tags: Semantic tags to convert
        
    Returns:
        List of consciousness tokens
    """
    consciousness_tokens = []
    
    # Intent tokens
    intent_mapping = {
        IntentType.QUESTION: "<INQUIRING>",
        IntentType.EMOTION_SHARING: "<EMOTIONAL>",
        IntentType.REQUEST: "<REQUESTING>",
        IntentType.COMPLAINT: "<VENTING>",
        IntentType.PRAISE: "<APPRECIATIVE>",
        IntentType.STORY: "<STORYTELLING>"
    }
    
    if tags.intent in intent_mapping:
        consciousness_tokens.append(intent_mapping[tags.intent])
    
    # Emotion tokens
    emotion_mapping = {
        EmotionTag.JOY: "<HAPPY>",
        EmotionTag.SADNESS: "<SAD>",
        EmotionTag.ANXIETY: "<ANXIOUS>",
        EmotionTag.EXCITEMENT: "<EXCITED>",
        EmotionTag.ANGER: "<ANGRY>",
        EmotionTag.CONFUSION: "<CONFUSED>",
        EmotionTag.GRATITUDE: "<GRATEFUL>"
    }
    
    for emotion in tags.emotions:
        if emotion in emotion_mapping:
            consciousness_tokens.append(emotion_mapping[emotion])
    
    # Topic tokens
    topic_mapping = {
        TopicCategory.WORK: "<WORK_TOPIC>",
        TopicCategory.FAMILY: "<FAMILY_TOPIC>",
        TopicCategory.EMOTIONS: "<EMOTIONAL_TOPIC>",
        TopicCategory.HEALTH: "<HEALTH_TOPIC>",
        TopicCategory.RELATIONSHIPS: "<RELATIONSHIP_TOPIC>"
    }
    
    for topic in tags.topics:
        if topic in topic_mapping:
            consciousness_tokens.append(topic_mapping[topic])
    
    # Urgency and complexity
    if tags.urgency_level > 0.7:
        consciousness_tokens.append("<URGENT>")
    if tags.complexity_level > 0.6:
        consciousness_tokens.append("<COMPLEX>")
    
    return consciousness_tokens

logging.info("[SemanticTagger] 🏷️ Auto-generated semantic tags module loaded")
print("[SemanticTagger] ✅ Auto-Generated Semantic Tags: LOADED")
print("[SemanticTagger] 🎯 Extract intent, emotion, topic from each message")
print("[SemanticTagger] 🏷️ Smarter conversation categorization for consciousness awareness")