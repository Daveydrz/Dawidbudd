"""
semantic_tagger.py - Semantic tagging for enhanced conversation understanding

This module provides semantic analysis and tagging capabilities to enhance
prompt construction with contextual understanding, intent recognition,
and semantic relationship mapping.
"""

import re
import json
from typing import Dict, List, Tuple, Any, Optional, Set
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import math

class SemanticCategory(Enum):
    """Main semantic categories for tagging"""
    QUESTION = "question"
    STATEMENT = "statement"
    REQUEST = "request"
    EMOTIONAL = "emotional"
    FACTUAL = "factual"
    OPINION = "opinion"
    MEMORY = "memory"
    PLANNING = "planning"
    GREETING = "greeting"
    FAREWELL = "farewell"
    CLARIFICATION = "clarification"
    CORRECTION = "correction"

class IntentType(Enum):
    """User intent classification"""
    INFORMATION_SEEKING = "information_seeking"
    SOCIAL_INTERACTION = "social_interaction"
    TASK_REQUEST = "task_request"
    EMOTIONAL_SUPPORT = "emotional_support"
    CREATIVE_REQUEST = "creative_request"
    PROBLEM_SOLVING = "problem_solving"
    CASUAL_CHAT = "casual_chat"
    MEMORY_SHARING = "memory_sharing"
    PREFERENCE_EXPRESSION = "preference_expression"
    GOAL_SETTING = "goal_setting"

class EmotionalTone(Enum):
    """Emotional tone of input"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    EXCITED = "excited"
    FRUSTRATED = "frustrated"
    CURIOUS = "curious"
    ANXIOUS = "anxious"
    CONFIDENT = "confident"
    UNCERTAIN = "uncertain"
    PLAYFUL = "playful"

class TopicDomain(Enum):
    """Topic domains for semantic understanding"""
    PERSONAL = "personal"
    TECHNOLOGY = "technology"
    RELATIONSHIPS = "relationships"
    WORK = "work"
    ENTERTAINMENT = "entertainment"
    HEALTH = "health"
    EDUCATION = "education"
    TRAVEL = "travel"
    FOOD = "food"
    FINANCE = "finance"
    NEWS = "news"
    SCIENCE = "science"
    ARTS = "arts"
    SPORTS = "sports"
    HOME = "home"
    TIME = "time"
    LOCATION = "location"

@dataclass
class SemanticTag:
    """Represents a semantic tag with confidence"""
    tag: str
    category: SemanticCategory
    confidence: float
    context: Dict[str, Any]

@dataclass
class SemanticAnalysis:
    """Complete semantic analysis of text"""
    text: str
    tags: List[SemanticTag]
    intent: IntentType
    intent_confidence: float
    emotional_tone: EmotionalTone
    tone_confidence: float
    topic_domains: List[TopicDomain]
    complexity_score: float  # 0.0 to 1.0
    urgency_score: float     # 0.0 to 1.0
    context_requirements: List[str]  # What context is needed for best response
    semantic_entities: Dict[str, Any]  # Extracted entities (names, places, etc.)

class SemanticTagger:
    """Main semantic analysis and tagging system"""
    
    def __init__(self):
        self.cached_analyses: Dict[str, SemanticAnalysis] = {}
        self._initialize_patterns()
    
    def _initialize_patterns(self):
        """Initialize regex patterns for semantic recognition"""
        
        # Question patterns
        self.question_patterns = [
            r'^(what|how|why|when|where|who|which|whose|can|could|would|should|do|does|did|is|are|was|were|will|have|has|had)\b',
            r'\?$',
            r'\b(tell me|explain|help me understand)\b',
        ]
        
        # Request patterns
        self.request_patterns = [
            r'^(please|could you|can you|would you|help me|i need)\b',
            r'\b(show me|give me|find|search|look up)\b',
            r'\b(remind me|set a reminder|schedule)\b',
        ]
        
        # Emotional patterns
        self.emotional_patterns = {
            EmotionalTone.POSITIVE: [
                r'\b(happy|great|awesome|fantastic|wonderful|amazing|love|excited|thrilled|delighted|glad|pleased)\b',
                r'\b(yes!|yay|woohoo|brilliant|excellent|perfect)\b',
            ],
            EmotionalTone.NEGATIVE: [
                r'\b(sad|angry|frustrated|annoyed|disappointed|upset|terrible|awful|hate|worried|stressed)\b',
                r'\b(no!|damn|crap|ugh|argh)\b',
            ],
            EmotionalTone.EXCITED: [
                r'\b(excited|thrilled|can\'t wait|so cool|amazing|incredible)\b',
                r'!{2,}',  # Multiple exclamation marks
            ],
            EmotionalTone.FRUSTRATED: [
                r'\b(frustrated|annoyed|irritated|fed up|sick of|tired of)\b',
                r'\b(why won\'t|doesn\'t work|broken|stupid)\b',
            ],
            EmotionalTone.CURIOUS: [
                r'\b(curious|wondering|interested|fascinating|intriguing)\b',
                r'\b(how does|what if|i wonder)\b',
            ],
            EmotionalTone.UNCERTAIN: [
                r'\b(not sure|maybe|perhaps|i think|possibly|might be|could be)\b',
                r'\b(uncertain|confused|don\'t know|unclear)\b',
            ],
        }
        
        # Topic domain patterns
        self.topic_patterns = {
            TopicDomain.TECHNOLOGY: [
                r'\b(computer|software|app|website|internet|phone|device|tech|AI|robot|code|program|digital)\b',
                r'\b(google|facebook|apple|microsoft|amazon|netflix|youtube|instagram|twitter)\b',
            ],
            TopicDomain.RELATIONSHIPS: [
                r'\b(family|friend|partner|husband|wife|boyfriend|girlfriend|relationship|marriage|dating)\b',
                r'\b(love|romantic|couple|wedding|divorce|breakup)\b',
            ],
            TopicDomain.WORK: [
                r'\b(job|work|career|office|boss|colleague|employee|meeting|project|deadline|salary)\b',
                r'\b(business|company|corporation|startup|interview|resume)\b',
            ],
            TopicDomain.HEALTH: [
                r'\b(health|doctor|hospital|medicine|sick|illness|pain|treatment|therapy|exercise|diet)\b',
                r'\b(mental health|stress|anxiety|depression|wellness)\b',
            ],
            TopicDomain.ENTERTAINMENT: [
                r'\b(movie|film|tv|show|music|song|game|book|novel|concert|theater)\b',
                r'\b(actor|actress|musician|artist|director|author)\b',
            ],
            TopicDomain.FOOD: [
                r'\b(food|eat|cooking|recipe|restaurant|meal|breakfast|lunch|dinner|snack)\b',
                r'\b(taste|flavor|delicious|hungry|diet|nutrition)\b',
            ],
            TopicDomain.TRAVEL: [
                r'\b(travel|trip|vacation|holiday|flight|hotel|destination|country|city|visit)\b',
                r'\b(passport|visa|luggage|tourist|explore)\b',
            ],
            TopicDomain.TIME: [
                r'\b(time|clock|hour|minute|second|today|tomorrow|yesterday|week|month|year)\b',
                r'\b(schedule|calendar|appointment|meeting|deadline|when)\b',
            ],
            TopicDomain.LOCATION: [
                r'\b(where|location|place|address|here|there|near|far|distance|map|gps)\b',
                r'\b(city|town|country|state|street|building|home|office)\b',
            ],
        }
        
        # Intent patterns
        self.intent_patterns = {
            IntentType.INFORMATION_SEEKING: [
                r'^(what|how|why|when|where|who|tell me|explain|i want to know)\b',
                r'\b(information|details|facts|learn|understand)\b',
            ],
            IntentType.TASK_REQUEST: [
                r'^(can you|could you|please|help me|i need you to)\b',
                r'\b(do|make|create|find|search|calculate|convert)\b',
            ],
            IntentType.EMOTIONAL_SUPPORT: [
                r'\b(feeling|upset|sad|worried|anxious|stressed|need to talk)\b',
                r'\b(support|comfort|advice|help|listen)\b',
            ],
            IntentType.SOCIAL_INTERACTION: [
                r'^(hi|hello|hey|good morning|good afternoon|good evening|how are you)\b',
                r'\b(chat|talk|conversation|tell me about yourself)\b',
            ],
            IntentType.MEMORY_SHARING: [
                r'\b(remember|recall|i told you|last time|before|previously)\b',
                r'\b(my|mine|personal|experience|story|happened)\b',
            ],
        }
    
    def analyze_text(self, text: str, user_id: str = None, context: Dict[str, Any] = None) -> SemanticAnalysis:
        """Perform complete semantic analysis of text"""
        
        # Check cache first
        cache_key = f"{text}:{user_id}"
        if cache_key in self.cached_analyses:
            return self.cached_analyses[cache_key]
        
        # Clean and prepare text
        text_clean = text.strip().lower()
        
        # Extract semantic tags
        tags = self._extract_semantic_tags(text_clean)
        
        # Determine intent
        intent, intent_confidence = self._classify_intent(text_clean)
        
        # Analyze emotional tone
        emotional_tone, tone_confidence = self._analyze_emotional_tone(text_clean)
        
        # Identify topic domains
        topic_domains = self._identify_topic_domains(text_clean)
        
        # Calculate complexity score
        complexity_score = self._calculate_complexity(text_clean)
        
        # Calculate urgency score
        urgency_score = self._calculate_urgency(text_clean)
        
        # Determine context requirements
        context_requirements = self._determine_context_requirements(text_clean, intent, topic_domains)
        
        # Extract semantic entities
        semantic_entities = self._extract_entities(text_clean)
        
        # Create analysis
        analysis = SemanticAnalysis(
            text=text,
            tags=tags,
            intent=intent,
            intent_confidence=intent_confidence,
            emotional_tone=emotional_tone,
            tone_confidence=tone_confidence,
            topic_domains=topic_domains,
            complexity_score=complexity_score,
            urgency_score=urgency_score,
            context_requirements=context_requirements,
            semantic_entities=semantic_entities
        )
        
        # Cache the analysis
        self.cached_analyses[cache_key] = analysis
        
        return analysis
    
    def _extract_semantic_tags(self, text: str) -> List[SemanticTag]:
        """Extract semantic tags from text"""
        tags = []
        
        # Check for questions
        for pattern in self.question_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                tags.append(SemanticTag(
                    tag="question",
                    category=SemanticCategory.QUESTION,
                    confidence=0.9,
                    context={"pattern": pattern}
                ))
                break
        
        # Check for requests
        for pattern in self.request_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                tags.append(SemanticTag(
                    tag="request",
                    category=SemanticCategory.REQUEST,
                    confidence=0.8,
                    context={"pattern": pattern}
                ))
                break
        
        # Check for statements vs questions
        if not any(tag.category == SemanticCategory.QUESTION for tag in tags):
            if '?' not in text:
                tags.append(SemanticTag(
                    tag="statement",
                    category=SemanticCategory.STATEMENT,
                    confidence=0.7,
                    context={}
                ))
        
        # Check for greetings
        greeting_patterns = [
            r'^(hi|hello|hey|good morning|good afternoon|good evening)\b',
            r'\b(how are you|how\'s it going|what\'s up)\b'
        ]
        for pattern in greeting_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                tags.append(SemanticTag(
                    tag="greeting",
                    category=SemanticCategory.GREETING,
                    confidence=0.9,
                    context={"pattern": pattern}
                ))
                break
        
        # Check for farewells
        farewell_patterns = [
            r'\b(bye|goodbye|see you|talk to you later|gotta go|farewell)\b',
            r'^(thanks|thank you).*(bye|goodbye|later)?\b'
        ]
        for pattern in farewell_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                tags.append(SemanticTag(
                    tag="farewell",
                    category=SemanticCategory.FAREWELL,
                    confidence=0.8,
                    context={"pattern": pattern}
                ))
                break
        
        # Check for emotional content
        emotional_indicators = [
            r'\b(feel|feeling|emotion|mood|happy|sad|angry|excited|worried)\b',
            r'[!]{2,}',  # Multiple exclamation marks
            r'[.]{3,}',  # Ellipsis indicating hesitation
        ]
        for pattern in emotional_indicators:
            if re.search(pattern, text, re.IGNORECASE):
                tags.append(SemanticTag(
                    tag="emotional",
                    category=SemanticCategory.EMOTIONAL,
                    confidence=0.6,
                    context={"pattern": pattern}
                ))
                break
        
        # Check for memory references
        memory_patterns = [
            r'\b(remember|recall|told you|mentioned|last time|before|previously|earlier)\b',
            r'\b(my|mine|i|me).*(story|experience|happened|did|was|were)\b'
        ]
        for pattern in memory_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                tags.append(SemanticTag(
                    tag="memory_reference",
                    category=SemanticCategory.MEMORY,
                    confidence=0.7,
                    context={"pattern": pattern}
                ))
                break
        
        # Check for planning/future content
        planning_patterns = [
            r'\b(plan|planning|will|going to|want to|hope to|schedule|appointment)\b',
            r'\b(tomorrow|next week|next month|future|later|soon)\b'
        ]
        for pattern in planning_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                tags.append(SemanticTag(
                    tag="future_planning",
                    category=SemanticCategory.PLANNING,
                    confidence=0.6,
                    context={"pattern": pattern}
                ))
                break
        
        return tags
    
    def _classify_intent(self, text: str) -> Tuple[IntentType, float]:
        """Classify the user's intent"""
        intent_scores = {}
        
        for intent_type, patterns in self.intent_patterns.items():
            score = 0.0
            matches = 0
            
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    score += 1.0
                    matches += 1
            
            if matches > 0:
                # Normalize score by number of patterns
                intent_scores[intent_type] = score / len(patterns)
        
        # Default to casual chat if no specific intent detected
        if not intent_scores:
            return IntentType.CASUAL_CHAT, 0.5
        
        # Return intent with highest score
        best_intent = max(intent_scores.items(), key=lambda x: x[1])
        return best_intent[0], min(best_intent[1], 1.0)
    
    def _analyze_emotional_tone(self, text: str) -> Tuple[EmotionalTone, float]:
        """Analyze emotional tone of the text"""
        tone_scores = {}
        
        for tone, patterns in self.emotional_patterns.items():
            score = 0.0
            matches = 0
            
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    score += 1.0
                    matches += 1
            
            if matches > 0:
                tone_scores[tone] = score / len(patterns)
        
        # Default to neutral if no emotional indicators
        if not tone_scores:
            return EmotionalTone.NEUTRAL, 0.8
        
        # Return tone with highest score
        best_tone = max(tone_scores.items(), key=lambda x: x[1])
        return best_tone[0], min(best_tone[1], 1.0)
    
    def _identify_topic_domains(self, text: str) -> List[TopicDomain]:
        """Identify relevant topic domains"""
        domain_scores = {}
        
        for domain, patterns in self.topic_patterns.items():
            score = 0.0
            
            for pattern in patterns:
                matches = len(re.findall(pattern, text, re.IGNORECASE))
                score += matches
            
            if score > 0:
                domain_scores[domain] = score
        
        # Return domains with score > 0, sorted by relevance
        relevant_domains = [
            domain for domain, score in 
            sorted(domain_scores.items(), key=lambda x: x[1], reverse=True)
        ]
        
        # Return top 3 domains or all if fewer than 3
        return relevant_domains[:3] if len(relevant_domains) > 3 else relevant_domains
    
    def _calculate_complexity(self, text: str) -> float:
        """Calculate complexity score based on various factors"""
        factors = []
        
        # Length factor
        word_count = len(text.split())
        length_score = min(word_count / 50.0, 1.0)  # Normalize to 50 words = 1.0
        factors.append(length_score)
        
        # Sentence structure complexity
        sentence_count = len(re.split(r'[.!?]+', text))
        avg_sentence_length = word_count / max(sentence_count, 1)
        structure_score = min(avg_sentence_length / 20.0, 1.0)  # 20 words/sentence = 1.0
        factors.append(structure_score)
        
        # Vocabulary complexity (simple heuristic)
        complex_words = len(re.findall(r'\b\w{8,}\b', text))  # Words with 8+ letters
        vocab_score = min(complex_words / max(word_count, 1), 0.5)  # Cap at 0.5
        factors.append(vocab_score)
        
        # Multiple topics increase complexity
        topic_count = len(self._identify_topic_domains(text))
        topic_score = min(topic_count / 3.0, 0.3)  # Cap at 0.3
        factors.append(topic_score)
        
        # Average all factors
        return sum(factors) / len(factors)
    
    def _calculate_urgency(self, text: str) -> float:
        """Calculate urgency score"""
        urgency_indicators = [
            (r'\b(urgent|emergency|asap|immediately|right now|help)\b', 1.0),
            (r'\b(soon|quickly|fast|hurry|rush)\b', 0.7),
            (r'\b(today|tonight|this morning|this afternoon)\b', 0.5),
            (r'[!]{2,}', 0.4),  # Multiple exclamation marks
            (r'\b(please|need|important)\b', 0.3),
        ]
        
        max_urgency = 0.0
        
        for pattern, score in urgency_indicators:
            if re.search(pattern, text, re.IGNORECASE):
                max_urgency = max(max_urgency, score)
        
        return max_urgency
    
    def _determine_context_requirements(self, text: str, intent: IntentType, 
                                      domains: List[TopicDomain]) -> List[str]:
        """Determine what context is needed for optimal response"""
        requirements = []
        
        # Intent-based requirements
        if intent == IntentType.MEMORY_SHARING:
            requirements.append("user_memory")
            requirements.append("conversation_history")
        elif intent == IntentType.INFORMATION_SEEKING:
            requirements.append("knowledge_base")
            if TopicDomain.TIME in domains:
                requirements.append("current_time")
            if TopicDomain.LOCATION in domains:
                requirements.append("location_info")
        elif intent == IntentType.EMOTIONAL_SUPPORT:
            requirements.append("emotional_context")
            requirements.append("user_personality")
        elif intent == IntentType.SOCIAL_INTERACTION:
            requirements.append("user_personality")
            requirements.append("relationship_context")
        elif intent == IntentType.TASK_REQUEST:
            requirements.append("capability_awareness")
            requirements.append("user_preferences")
        
        # Domain-based requirements
        if TopicDomain.PERSONAL in domains:
            requirements.append("user_profile")
        if TopicDomain.RELATIONSHIPS in domains:
            requirements.append("relationship_context")
        if TopicDomain.WORK in domains:
            requirements.append("professional_context")
        if TopicDomain.TIME in domains:
            requirements.append("temporal_context")
        if TopicDomain.LOCATION in domains:
            requirements.append("spatial_context")
        
        # Memory reference patterns
        if re.search(r'\b(remember|recall|told you|mentioned|last time)\b', text, re.IGNORECASE):
            requirements.append("conversation_history")
            requirements.append("user_memory")
        
        # Remove duplicates
        return list(set(requirements))
    
    def _extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract semantic entities from text"""
        entities = {
            "names": [],
            "places": [],
            "times": [],
            "numbers": [],
            "organizations": [],
        }
        
        # Names (simple pattern - capitalized words that aren't common words)
        common_words = {'I', 'The', 'This', 'That', 'When', 'Where', 'What', 'How', 'Why', 'Who'}
        name_candidates = re.findall(r'\b[A-Z][a-z]+\b', text)
        entities["names"] = [name for name in name_candidates if name not in common_words]
        
        # Places (capitalized phrases, common place indicators)
        place_patterns = [
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+(?:Street|Road|Avenue|Drive|Lane|Boulevard|City|State|Country))\b',
            r'\bin\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b',
            r'\bat\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b'
        ]
        for pattern in place_patterns:
            entities["places"].extend(re.findall(pattern, text))
        
        # Times
        time_patterns = [
            r'\b\d{1,2}:\d{2}(?:\s*(?:AM|PM))?\b',
            r'\b(?:today|tomorrow|yesterday|tonight|morning|afternoon|evening)\b',
            r'\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b',
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b'
        ]
        for pattern in time_patterns:
            entities["times"].extend(re.findall(pattern, text, re.IGNORECASE))
        
        # Numbers
        entities["numbers"] = re.findall(r'\b\d+(?:\.\d+)?\b', text)
        
        # Organizations (simple heuristic - words ending in common org suffixes)
        org_patterns = [
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+(?:Inc|Corp|LLC|Ltd|Company|Corporation|Organization))\b'
        ]
        for pattern in org_patterns:
            entities["organizations"].extend(re.findall(pattern, text))
        
        return entities
    
    def generate_semantic_tokens(self, analysis: SemanticAnalysis) -> Dict[str, str]:
        """Generate semantic tokens for prompt injection"""
        tokens = {}
        
        # Intent tokens
        tokens['<sem_intent>'] = analysis.intent.value
        tokens['<sem_intent_conf>'] = f"{analysis.intent_confidence:.2f}"
        
        # Emotional tone tokens
        tokens['<sem_tone>'] = analysis.emotional_tone.value
        tokens['<sem_tone_conf>'] = f"{analysis.tone_confidence:.2f}"
        
        # Topic domains
        if analysis.topic_domains:
            tokens['<sem_topics>'] = ", ".join([domain.value for domain in analysis.topic_domains])
        else:
            tokens['<sem_topics>'] = "general"
        
        # Complexity and urgency
        tokens['<sem_complexity>'] = "high" if analysis.complexity_score > 0.7 else "medium" if analysis.complexity_score > 0.3 else "low"
        tokens['<sem_urgency>'] = "high" if analysis.urgency_score > 0.7 else "medium" if analysis.urgency_score > 0.3 else "low"
        
        # Context requirements
        if analysis.context_requirements:
            tokens['<sem_context_needs>'] = ", ".join(analysis.context_requirements[:3])  # Top 3
        else:
            tokens['<sem_context_needs>'] = "minimal"
        
        # Key semantic tags
        main_tags = [tag.tag for tag in analysis.tags if tag.confidence > 0.7]
        if main_tags:
            tokens['<sem_tags>'] = ", ".join(main_tags[:3])  # Top 3 high-confidence tags
        else:
            tokens['<sem_tags>'] = "general"
        
        # Entity information
        entities_found = []
        for entity_type, entities in analysis.semantic_entities.items():
            if entities:
                entities_found.append(f"{entity_type}: {len(entities)}")
        
        if entities_found:
            tokens['<sem_entities>'] = "; ".join(entities_found[:3])
        else:
            tokens['<sem_entities>'] = "none"
        
        return tokens
    
    def should_trigger_memory_search(self, analysis: SemanticAnalysis) -> bool:
        """Determine if semantic analysis suggests memory search is needed"""
        # Check for memory-related intent
        if analysis.intent == IntentType.MEMORY_SHARING:
            return True
        
        # Check for memory-related tags
        memory_tags = [tag for tag in analysis.tags if tag.category == SemanticCategory.MEMORY]
        if memory_tags and any(tag.confidence > 0.6 for tag in memory_tags):
            return True
        
        # Check for context requirements
        if "user_memory" in analysis.context_requirements or "conversation_history" in analysis.context_requirements:
            return True
        
        return False
    
    def get_response_style_guidance(self, analysis: SemanticAnalysis) -> Dict[str, str]:
        """Get guidance for response style based on semantic analysis"""
        guidance = {}
        
        # Tone guidance
        if analysis.emotional_tone == EmotionalTone.FRUSTRATED:
            guidance['tone'] = "empathetic, patient, solution-focused"
        elif analysis.emotional_tone == EmotionalTone.EXCITED:
            guidance['tone'] = "enthusiastic, matching energy"
        elif analysis.emotional_tone == EmotionalTone.ANXIOUS:
            guidance['tone'] = "reassuring, calm, supportive"
        elif analysis.emotional_tone == EmotionalTone.CURIOUS:
            guidance['tone'] = "informative, engaging, encouraging"
        else:
            guidance['tone'] = "natural, conversational"
        
        # Complexity guidance
        if analysis.complexity_score > 0.7:
            guidance['complexity'] = "detailed, comprehensive, structured"
        elif analysis.complexity_score < 0.3:
            guidance['complexity'] = "simple, direct, concise"
        else:
            guidance['complexity'] = "balanced, clear"
        
        # Urgency guidance
        if analysis.urgency_score > 0.7:
            guidance['urgency'] = "immediate, prioritized, focused"
        elif analysis.urgency_score < 0.3:
            guidance['urgency'] = "relaxed, thorough"
        else:
            guidance['urgency'] = "timely, appropriate"
        
        # Intent-based guidance
        if analysis.intent == IntentType.EMOTIONAL_SUPPORT:
            guidance['approach'] = "supportive, validating, helpful"
        elif analysis.intent == IntentType.INFORMATION_SEEKING:
            guidance['approach'] = "informative, accurate, comprehensive"
        elif analysis.intent == IntentType.SOCIAL_INTERACTION:
            guidance['approach'] = "friendly, engaging, personal"
        elif analysis.intent == IntentType.TASK_REQUEST:
            guidance['approach'] = "practical, action-oriented, clear"
        else:
            guidance['approach'] = "adaptive, natural"
        
        return guidance

# Global semantic tagger instance
semantic_tagger = SemanticTagger()

# Convenience functions for integration
def analyze_user_text(text: str, user_id: str = None, context: Dict[str, Any] = None) -> SemanticAnalysis:
    """Analyze user text and return semantic analysis"""
    return semantic_tagger.analyze_text(text, user_id, context)

def get_semantic_tokens(text: str, user_id: str = None) -> Dict[str, str]:
    """Get semantic tokens for a text"""
    analysis = semantic_tagger.analyze_text(text, user_id)
    return semantic_tagger.generate_semantic_tokens(analysis)

def get_response_guidance(text: str, user_id: str = None) -> Dict[str, str]:
    """Get response style guidance based on semantic analysis"""
    analysis = semantic_tagger.analyze_text(text, user_id)
    return semantic_tagger.get_response_style_guidance(analysis)

def requires_memory_search(text: str, user_id: str = None) -> bool:
    """Check if text requires memory search based on semantic analysis"""
    analysis = semantic_tagger.analyze_text(text, user_id)
    return semantic_tagger.should_trigger_memory_search(analysis)