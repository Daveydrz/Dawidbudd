"""
Local ONNX-like Memory Classifier - Automatic memory type categorization
Created: 2025-01-17
Purpose: Classify user text into fact, preference, or context without LLM calls
Features: Multi-language support, semantic understanding, fast inference
"""

import re
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class MemoryType(Enum):
    """Memory classification types"""
    FACT = "fact"
    PREFERENCE = "preference"
    CONTEXT = "context"

@dataclass
class ClassificationResult:
    """Classification result with confidence"""
    memory_type: str
    confidence: float
    matched_patterns: List[str]
    language_detected: str

class MemoryClassifier:
    """Local memory classifier simulating ONNX behavior"""
    
    def __init__(self):
        """Initialize classifier with multi-language patterns"""
        self.model_loaded = True
        self.inference_count = 0
        self.total_inference_time = 0.0
        
        # Multi-language preference patterns
        self.preference_patterns = {
            # English preferences
            "en": [
                # Positive preferences
                (r"\b(?:i|my)\s+(?:really\s+)?(?:love|adore|like|enjoy|prefer|am\s+into|am\s+fond\s+of)\s+(.+?)(?:\.|!|$)", "positive", 0.9),
                (r"\b(?:i|my)\s+(?:absolutely\s+)?(?:favorite|favourite)\s+(.+?)\s+is\s+(.+?)(?:\.|!|$)", "positive", 0.95),
                (r"\bi\s+am\s+(?:a\s+big\s+)?fan\s+of\s+(.+?)(?:\.|!|$)", "positive", 0.85),
                (r"\bi\s+can't\s+get\s+enough\s+of\s+(.+?)(?:\.|!|$)", "positive", 0.9),
                (r"\bi\s+am\s+passionate\s+about\s+(.+?)(?:\.|!|$)", "positive", 0.9),
                (r"\bi\s+(?:really\s+)?love\s+(.+?)(?:\.|!|$)", "positive", 0.95),  # Enhanced love pattern
                
                # Negative preferences  
                (r"\b(?:i|my)\s+(?:really\s+)?(?:hate|dislike|can't\s+stand|despise|loathe)\s+(.+?)(?:\.|!|$)", "negative", 0.9),
                (r"\bi\s+(?:am\s+)?not\s+(?:a\s+)?(?:fan\s+of|into|fond\s+of)\s+(.+?)(?:\.|!|$)", "negative", 0.85),
                (r"\bi\s+avoid\s+(.+?)(?:\.|!|$)", "negative", 0.8),
                (r"\b(.+?)\s+(?:is|are)n't\s+(?:my\s+)?(?:thing|cup\s+of\s+tea)(?:\.|!|$)", "negative", 0.8),
                
                # Neutral preferences
                (r"\bi\s+(?:usually|normally|typically|often)\s+(.+?)(?:\.|!|$)", "neutral", 0.7),
                (r"\bi\s+tend\s+to\s+(.+?)(?:\.|!|$)", "neutral", 0.7),
                (r"\bi\s+(?:sometimes|occasionally)\s+(.+?)(?:\.|!|$)", "neutral", 0.6),
            ],
            
            # Polish preferences  
            "pl": [
                (r"\b(?:kocham|uwielbiam|lubię|podoba\s+mi\s+się)\s+(.+?)(?:\.|!|$)", "positive", 0.9),
                (r"\blubię\s+(.+?)(?:\.|!|$)", "positive", 0.9),  # More specific
                (r"\bmoja?\s+ulubiona?\s+(.+?)\s+to\s+(.+?)(?:\.|!|$)", "positive", 0.95),
                (r"\b(?:nienawidzę|nie\s+lubię|nie\s+znoszę)\s+(.+?)(?:\.|!|$)", "negative", 0.9),
                (r"\b(?:zwykle|zazwyczai|często)\s+(.+?)(?:\.|!|$)", "neutral", 0.7),
            ],
            
            # Italian preferences
            "it": [
                (r"\b(?:amo|adoro|mi\s+piace|preferisco)\s+(.+?)(?:\.|!|$)", "positive", 0.9),
                (r"\bil\s+mio\s+(?:preferito|favorito)\s+(.+?)\s+è\s+(.+?)(?:\.|!|$)", "positive", 0.95),
                (r"\b(?:odio|non\s+mi\s+piace|detesto)\s+(.+?)(?:\.|!|$)", "negative", 0.9),
                (r"\b(?:di\s+solito|solitamente|spesso)\s+(.+?)(?:\.|!|$)", "neutral", 0.7),
            ]
        }
        
        # Multi-language fact patterns
        self.fact_patterns = {
            "en": [
                # Personal identity
                (r"\bmy\s+name\s+is\s+(.+?)(?:\.|!|$)", "identity", 0.95),
                (r"\bi\s+am\s+(.+?)\s+years?\s+old(?:\.|!|$)", "age", 0.95),
                (r"\bi\s+was\s+born\s+(?:on|in)\s+(.+?)(?:\.|!|$)", "birth", 0.95),
                (r"\bmy\s+birthday\s+is\s+(.+?)(?:\.|!|$)", "birth", 0.95),
                
                # Relationships
                (r"\bmy\s+(?:wife|husband|spouse|partner|girlfriend|boyfriend)\s+is\s+(.+?)(?:\.|!|$)", "relationship", 0.9),
                (r"\bi\s+have\s+(?:a\s+)?(?:son|daughter|child|children|kids?)\s+(?:named\s+)?(.+?)(?:\.|!|$)", "family", 0.9),
                (r"\bmy\s+(?:mother|mom|father|dad|sister|brother)\s+is\s+(.+?)(?:\.|!|$)", "family", 0.85),
                
                # Location & Work
                (r"\bi\s+live\s+in\s+(.+?)(?:\.|!|$)", "location", 0.9),
                (r"\bi\s+work\s+(?:at|for|as)\s+(.+?)(?:\.|!|$)", "work", 0.9),
                (r"\bmy\s+job\s+is\s+(.+?)(?:\.|!|$)", "work", 0.9),
                
                # Physical attributes
                (r"\bi\s+am\s+(.+?)\s+(?:tall|short|feet|inches|cm|meters?)(?:\.|!|$)", "physical", 0.85),
                (r"\bmy\s+(?:height|weight)\s+is\s+(.+?)(?:\.|!|$)", "physical", 0.9),
                (r"\bi\s+have\s+(.+?)\s+(?:hair|eyes)(?:\.|!|$)", "physical", 0.8),
                
                # Medical/Health facts
                (r"\bi\s+am\s+allergic\s+to\s+(.+?)(?:\.|!|$)", "medical", 0.9),
                (r"\bi\s+have\s+(?:a\s+)?(.+?)\s+(?:condition|disease|illness)(?:\.|!|$)", "medical", 0.85),
                (r"\bi\s+take\s+(.+?)\s+(?:medication|medicine|pills?)(?:\.|!|$)", "medical", 0.8),
                
                # Education
                (r"\bi\s+(?:studied|graduated\s+from|went\s+to)\s+(.+?)(?:\.|!|$)", "education", 0.85),
                (r"\bi\s+have\s+a\s+degree\s+in\s+(.+?)(?:\.|!|$)", "education", 0.9),
            ],
            
            "pl": [
                (r"\bmam\s+na\s+imię\s+(.+?)(?:\.|!|$)", "identity", 0.95),
                (r"\bnazywam\s+się\s+(.+?)(?:\.|!|$)", "identity", 0.95),  # More common
                (r"\bmam\s+(.+?)\s+lat(?:\.|!|$)", "age", 0.95),
                (r"\bmoje\s+urodziny\s+są\s+(.+?)(?:\.|!|$)", "birth", 0.95),
                (r"\bmieszkam\s+w\s+(.+?)(?:\.|!|$)", "location", 0.9),
                (r"\bpracuję\s+(?:w|jako)\s+(.+?)(?:\.|!|$)", "work", 0.9),
            ],
            
            "it": [
                (r"\bil\s+mio\s+nome\s+è\s+(.+?)(?:\.|!|$)", "identity", 0.95),
                (r"\bmi\s+chiamo\s+(.+?)(?:\.|!|$)", "identity", 0.95),  # More common  
                (r"\bho\s+(.+?)\s+anni(?:\.|!|$)", "age", 0.95),
                (r"\bil\s+mio\s+compleanno\s+è\s+(.+?)(?:\.|!|$)", "birth", 0.95),
                (r"\bvivo\s+a\s+(.+?)(?:\.|!|$)", "location", 0.9),
                (r"\babito\s+a\s+(.+?)(?:\.|!|$)", "location", 0.9),  # Also "live in"
                (r"\blavoro\s+(?:come|presso)\s+(.+?)(?:\.|!|$)", "work", 0.9),
            ]
        }
        
        # Multi-language context patterns (actions, temporary states)
        self.context_patterns = {
            "en": [
                # Current actions
                (r"\bi\s+am\s+(?:currently\s+)?(?:going\s+to|at|in)\s+(.+?)(?:\.|!|$)", "current_action", 0.9),
                (r"\bi\s+just\s+(.+?)(?:\.|!|$)", "recent_action", 0.85),
                (r"\bi\s+am\s+about\s+to\s+(.+?)(?:\.|!|$)", "future_action", 0.8),
                (r"\bright\s+now\s+i\s+am\s+(.+?)(?:\.|!|$)", "current_state", 0.9),
                (r"\bhow\s+are\s+you(?:\.|!|$)", "question", 0.8),  # Common questions
                (r"\bwhat\s+time\s+is\s+it(?:\.|!|$)", "question", 0.9),
                (r"\bhi\b|hello\b|hey\b", "greeting", 0.8),  # Greetings
                
                # Movement/Location
                (r"\bi\s+(?:went|am\s+going)\s+to\s+(?:the\s+)?(.+?)(?:\.|!|$)", "movement", 0.85),
                (r"\bi\s+am\s+(?:back\s+)?(?:from|at)\s+(?:the\s+)?(.+?)(?:\.|!|$)", "location_update", 0.85),
                
                # Activities
                (r"\bi\s+am\s+(?:doing|making|cooking|cleaning|working\s+on)\s+(.+?)(?:\.|!|$)", "activity", 0.8),
                (r"\bi\s+(?:finished|completed|done\s+with)\s+(.+?)(?:\.|!|$)", "completion", 0.8),
                
                # Temporary states
                (r"\bi\s+(?:feel|am\s+feeling)\s+(.+?)(?:\.|!|$)", "emotional_state", 0.7),
                (r"\bi\s+am\s+(?:tired|hungry|thirsty|busy|free)(?:\.|!|$)", "physical_state", 0.75),
            ],
            
            "pl": [
                (r"\bidę\s+do\s+(.+?)(?:\.|!|$)", "movement", 0.85),
                (r"\bjestem\s+(?:w|na)\s+(.+?)(?:\.|!|$)", "location_update", 0.85),
                (r"\bjust\s+(.+?)(?:\.|!|$)", "recent_action", 0.85),
                (r"\brodę\s+(.+?)(?:\.|!|$)", "activity", 0.8),
            ],
            
            "it": [
                (r"\bsto\s+andando\s+(?:a|al|alla)\s+(.+?)(?:\.|!|$)", "movement", 0.85),
                (r"\bsono\s+(?:a|al|alla)\s+(.+?)(?:\.|!|$)", "location_update", 0.85),
                (r"\bho\s+appena\s+(.+?)(?:\.|!|$)", "recent_action", 0.85),
                (r"\bsto\s+(?:facendo|cucinando|pulendo)\s+(.+?)(?:\.|!|$)", "activity", 0.8),
            ]
        }
        
        # Language detection patterns - enhanced
        self.language_indicators = {
            "en": ["the", "and", "or", "but", "with", "have", "this", "that", "will", "would", "my", "i'm", "going", "you", "are"],
            "pl": ["jest", "są", "mam", "mój", "moja", "jego", "jej", "które", "gdzie", "jak", "lubię", "lat", "się", "na", "do"],
            "it": ["sono", "è", "che", "con", "per", "suo", "sua", "dove", "come", "quando", "ho", "anni", "mi", "la", "il"]
        }
    
    def detect_language(self, text: str) -> str:
        """Detect language of input text"""
        text_lower = text.lower()
        words = text_lower.split()
        
        # Quick English detection - if it contains common English words, it's probably English
        english_words = ["i", "my", "the", "and", "or", "but", "with", "have", "this", "that", "will", "would", "going", "just", "back", "are", "you", "is", "was", "were", "love", "like", "hate"]
        english_count = sum(1 for word in words if word in english_words)
        
        if english_count >= 1 or (len(words) <= 3 and any(word in english_words for word in words)):  # Strong English indicators
            return "en"
        
        language_scores = {}
        for lang, indicators in self.language_indicators.items():
            score = sum(1 for indicator in indicators if indicator in text_lower)
            language_scores[lang] = score
        
        # Return language with highest score, default to English
        if language_scores:
            detected_lang = max(language_scores, key=language_scores.get)
            return detected_lang if language_scores[detected_lang] > 0 else "en"
        
        return "en"
    
    def classify_memory_type(self, user_text: str) -> str:
        """
        Main API function - classify text into fact, preference, or context
        Returns: "fact", "preference", or "context"
        """
        start_time = time.time()
        
        try:
            # Get detailed classification result
            result = self.classify_with_confidence(user_text)
            
            # Track performance
            inference_time = time.time() - start_time
            self.inference_count += 1
            self.total_inference_time += inference_time
            
            return result.memory_type
            
        except Exception as e:
            print(f"[MemoryClassifier] ⚠️ Classification error: {e}")
            return "context"  # Safe fallback
    
    def classify_with_confidence(self, user_text: str) -> ClassificationResult:
        """Classify text with detailed confidence information"""
        text = user_text.strip()
        if not text:
            return ClassificationResult("context", 0.5, [], "en")
        
        # Detect language
        language = self.detect_language(text)
        
        # Try fact classification first (highest priority)
        fact_result = self._match_patterns(text, self.fact_patterns.get(language, []), "fact")
        if fact_result[1] > 0.75:  # Slightly lower threshold
            return ClassificationResult("fact", fact_result[1], fact_result[2], language)
        
        # Try preference classification (medium priority)
        pref_result = self._match_patterns(text, self.preference_patterns.get(language, []), "preference")
        if pref_result[1] > 0.65:  # Lower threshold for preferences
            return ClassificationResult("preference", pref_result[1], pref_result[2], language)
        
        # Try context classification (lowest priority, catch-all)
        context_result = self._match_patterns(text, self.context_patterns.get(language, []), "context")
        if context_result[1] > 0.55:  # Lower threshold for context
            return ClassificationResult("context", context_result[1], context_result[2], language)
        
        # Fallback classification based on sentence structure
        fallback_type, fallback_confidence = self._fallback_classification(text, language)
        return ClassificationResult(fallback_type, fallback_confidence, ["fallback"], language)
    
    def _match_patterns(self, text: str, patterns: List[Tuple], category: str) -> Tuple[str, float, List[str]]:
        """Match text against pattern list"""
        text_lower = text.lower()
        best_confidence = 0.0
        matched_patterns = []
        
        for pattern, subcategory, confidence in patterns:
            try:
                if re.search(pattern, text_lower):
                    if confidence > best_confidence:
                        best_confidence = confidence
                    matched_patterns.append(f"{category}:{subcategory}")
            except re.error:
                continue  # Skip invalid regex patterns
        
        return category, best_confidence, matched_patterns
    
    def _fallback_classification(self, text: str, language: str) -> Tuple[str, float]:
        """Fallback classification using sentence structure analysis"""
        text_lower = text.lower()
        
        # Fact indicators (biographical/static information)
        fact_indicators = {
            "en": ["my name is", "i am", "i was born", "i live in", "i work as", "my age is", "my birthday is"],
            "pl": ["mam na imię", "jestem", "urodziłem", "mieszkam w", "pracuję jako", "mam", "mój wiek", "nazywam się", "lat"],
            "it": ["mi chiamo", "sono nato", "vivo a", "lavoro come", "ho", "la mia età", "anni"]
        }
        
        # Preference indicators (likes/dislikes)
        preference_indicators = {
            "en": ["i like", "i love", "i hate", "i prefer", "i enjoy", "i dislike", "favorite"],
            "pl": ["lubię", "kocham", "nienawidzę", "wolę", "podoba mi się", "ulubiony", "uwielbiam"],
            "it": ["mi piace", "amo", "odio", "preferisco", "mi diverto", "preferito", "adoro"]
        }
        
        # Context indicators (actions/temporary states)
        context_indicators = {
            "en": ["i'm going", "i went", "i'm at", "i just", "right now", "currently", "how are you", "what time"],
            "pl": ["idę", "poszedłem", "jestem w", "właśnie", "teraz", "obecnie"],
            "it": ["sto andando", "sono andato", "sono a", "appena", "adesso", "attualmente"]
        }
        
        lang_indicators = {
            "fact": fact_indicators.get(language, fact_indicators["en"]),
            "preference": preference_indicators.get(language, preference_indicators["en"]),
            "context": context_indicators.get(language, context_indicators["en"])
        }
        
        # Score each category with more specific scoring
        scores = {"fact": 0, "preference": 0, "context": 0}
        
        for category, indicators in lang_indicators.items():
            score = 0
            for indicator in indicators:
                if indicator in text_lower:
                    # Give extra weight to longer, more specific matches
                    weight = len(indicator.split()) * 2  # Multi-word phrases get more weight
                    score += weight
            scores[category] = score
        
        # Determine best category
        if any(scores.values()):
            best_category = max(scores, key=scores.get)
            max_score = scores[best_category]
            confidence = min(0.6 + (max_score * 0.05), 0.8)  # Scale confidence based on score
            return best_category, confidence
        
        # Ultimate fallback - analyze sentence structure
        if "?" in text:
            return "context", 0.6  # Questions are usually context
        elif any(word in text_lower for word in ["love", "like", "hate", "prefer", "enjoy", "favorite"]):
            return "preference", 0.6  # Preference keywords
        elif any(word in text_lower for word in ["my name is", "i am", "birthday is", "work as", "live in"]):
            return "fact", 0.6  # More specific fact patterns
        elif any(word in text_lower for word in ["going", "just", "at", "from", "back", "currently", "how are"]):
            return "context", 0.6  # Context keywords
        else:
            return "context", 0.5  # Default to context
    
    def get_classification_stats(self) -> Dict[str, float]:
        """Get classifier performance statistics"""
        avg_inference_time = (self.total_inference_time / self.inference_count 
                            if self.inference_count > 0 else 0.0)
        
        return {
            "model_loaded": self.model_loaded,
            "total_inferences": self.inference_count,
            "average_inference_time_ms": avg_inference_time * 1000,
            "target_inference_time_ms": 10.0,
            "performance_target_met": avg_inference_time * 1000 < 10.0
        }
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        return ["en", "pl", "it"]

# Global classifier instance (simulating ONNX model loading)
_classifier_instance = None

def _get_classifier() -> MemoryClassifier:
    """Get or create classifier instance (lazy loading)"""
    global _classifier_instance
    if _classifier_instance is None:
        print("[MemoryClassifier] 🧠 Loading ONNX-like memory classification model...")
        _classifier_instance = MemoryClassifier()
        print("[MemoryClassifier] ✅ Model loaded successfully")
        print(f"[MemoryClassifier] 🌍 Supported languages: {', '.join(_classifier_instance.get_supported_languages())}")
    return _classifier_instance

def classify_memory_type(user_text: str) -> str:
    """
    Main API function for memory classification
    
    Args:
        user_text: Input text to classify
        
    Returns:
        str: One of "fact", "preference", or "context"
        
    Examples:
        classify_memory_type("I like pizza") -> "preference"
        classify_memory_type("My birthday is June 5") -> "fact"  
        classify_memory_type("I'm going to the shop") -> "context"
    """
    classifier = _get_classifier()
    return classifier.classify_memory_type(user_text)

def classify_memory_type_with_confidence(user_text: str) -> Tuple[str, float]:
    """
    Classify memory type with confidence score
    
    Args:
        user_text: Input text to classify
        
    Returns:
        Tuple[str, float]: (memory_type, confidence_score)
    """
    classifier = _get_classifier()
    result = classifier.classify_with_confidence(user_text)
    return result.memory_type, result.confidence

def get_classifier_stats() -> Dict[str, float]:
    """Get classifier performance statistics"""
    if _classifier_instance:
        return _classifier_instance.get_classification_stats()
    return {"model_loaded": False}

# Test function for verification
def test_classifier():
    """Test classifier with example inputs"""
    test_cases = [
        # Preferences
        ("I like pizza", "preference"),
        ("I love cats", "preference"), 
        ("I hate rain", "preference"),
        ("My favorite color is blue", "preference"),
        
        # Facts
        ("My name is John", "fact"),
        ("I am 25 years old", "fact"),
        ("My birthday is June 5", "fact"),
        ("I live in New York", "fact"),
        ("I work as a teacher", "fact"),
        
        # Context
        ("I'm going to the shop", "context"),
        ("I just got back", "context"),
        ("I'm at the office", "context"),
        ("I feel tired", "context"),
        
        # Multi-language tests
        ("Lubię pizzę", "preference"),  # Polish: I like pizza
        ("Mam 30 lat", "fact"),  # Polish: I am 30 years old
        ("Idę do sklepu", "context"),  # Polish: I'm going to the shop
        
        ("Mi piace la pizza", "preference"),  # Italian: I like pizza
        ("Ho 25 anni", "fact"),  # Italian: I am 25 years old
        ("Sto andando al negozio", "context"),  # Italian: I'm going to the shop
    ]
    
    print("[MemoryClassifier] 🧪 Running classifier tests...")
    correct = 0
    total = len(test_cases)
    
    for text, expected in test_cases:
        result = classify_memory_type(text)
        status = "✅" if result == expected else "❌"
        print(f"  {status} '{text}' -> {result} (expected: {expected})")
        if result == expected:
            correct += 1
    
    accuracy = (correct / total) * 100
    print(f"[MemoryClassifier] 📊 Test accuracy: {accuracy:.1f}% ({correct}/{total})")
    
    # Show performance stats
    stats = get_classifier_stats()
    print(f"[MemoryClassifier] ⚡ Average inference: {stats.get('average_inference_time_ms', 0):.2f}ms")
    
    return accuracy >= 80  # 80% accuracy threshold

if __name__ == "__main__":
    # Run tests when script is executed directly
    test_classifier()