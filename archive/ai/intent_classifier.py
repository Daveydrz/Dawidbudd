"""
ONNX-based Intent Classifier - Local neural network intent classification
Created: 2025-01-17
Purpose: Classify user intents without LLM calls using ONNX neural network
Features: Multi-language support, fast local inference, context-aware classification
"""

import onnxruntime as ort
import numpy as np
from transformers import AutoTokenizer
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# Load tokenizer (same one used during training)
try:
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-multilingual-cased")
    TOKENIZER_LOADED = True
    print("[IntentClassifier] 🔤 DistilBERT tokenizer loaded successfully")
except Exception as e:
    TOKENIZER_LOADED = False
    print(f"[IntentClassifier] ⚠️ Tokenizer loading failed: {e}")

# Load ONNX model (path updated if file is in same folder as main.py)
try:
    session = ort.InferenceSession("intent_classifier.onnx", providers=["CPUExecutionProvider"])
    MODEL_LOADED = True
    print("[IntentClassifier] 🧠 ONNX intent classifier model loaded successfully")
except Exception as e:
    MODEL_LOADED = False
    session = None
    print(f"[IntentClassifier] ⚠️ ONNX model loading failed: {e}")

@dataclass
class IntentResult:
    """Intent classification result with confidence"""
    intent: str
    confidence: float
    raw_logits: List[float]
    inference_time_ms: float

class IntentClassifier:
    """ONNX-based neural intent classifier"""
    
    def __init__(self):
        """Initialize ONNX intent classifier"""
        self.model_loaded = MODEL_LOADED and TOKENIZER_LOADED
        self.inference_count = 0
        self.total_inference_time = 0.0
        
        # Intent label mapping (must match training order)
        self.label_mapping = [
            "question",        # User asking questions
            "request",         # User requesting actions
            "information",     # User sharing information
            "greeting",        # User greeting/social
            "goodbye",         # User ending conversation
            "complaint",       # User expressing dissatisfaction
            "compliment",      # User expressing praise
            "casual_chat",     # General conversation
            "help",           # User needs assistance
            "confirmation"     # User confirming/agreeing
        ]
        
        if self.model_loaded:
            print("[IntentClassifier] ✅ ONNX neural intent classifier ready")
        else:
            print("[IntentClassifier] ⚠️ Falling back to rule-based classification")
            # Initialize fallback rule-based classifier
            self._init_fallback_classifier()
    
    def _init_fallback_classifier(self):
        """Initialize rule-based fallback classifier"""
        # Simplified patterns for fallback
        self.intent_patterns = {
            "question": ["what", "how", "when", "where", "who", "why", "?", "can you", "do you know"],
            "request": ["please", "can you", "could you", "would you", "help me", "i need"],
            "information": ["i am", "my", "i have", "i was", "i will", "i like", "i don't like"],
            "greeting": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"],
            "goodbye": ["bye", "goodbye", "see you", "take care", "farewell", "talk later"],
            "complaint": ["terrible", "awful", "hate", "annoying", "frustrated", "angry"],
            "compliment": ["great", "awesome", "amazing", "wonderful", "perfect", "love it"],
            "casual_chat": ["how are you", "what's up", "how's it going", "nice weather"],
            "help": ["help", "assist", "support", "i'm confused", "i don't understand"],
            "confirmation": ["yes", "ok", "okay", "sure", "right", "exactly", "correct"]
        }
    
    def classify_intent(self, user_text: str) -> str:
        """
        Main API function - classify user intent using ONNX
        Returns: One of the intent labels
        """
        start_time = time.time()
        
        try:
            if self.model_loaded:
                # Use ONNX neural network classification
                result = self._classify_with_onnx(user_text)
            else:
                # Use rule-based fallback
                result = self._classify_with_fallback(user_text)
            
            # Track performance
            inference_time = time.time() - start_time
            self.inference_count += 1
            self.total_inference_time += inference_time
            
            return result.intent
            
        except Exception as e:
            print(f"[IntentClassifier] ⚠️ Classification error: {e}")
            return "casual_chat"  # Safe fallback
    
    def _classify_with_onnx(self, user_text: str) -> IntentResult:
        """Classify using ONNX neural network"""
        start_time = time.time()
        
        try:
            # Tokenize input 
            inputs = tokenizer(user_text, return_tensors="np", padding="max_length", truncation=True, max_length=32)
            
            # Prepare ONNX inputs
            ort_inputs = {
                "input_ids": inputs["input_ids"].astype(np.int64),
                "attention_mask": inputs["attention_mask"].astype(np.int64)
            }
            
            # Run inference
            logits = session.run(None, ort_inputs)[0]
            
            # Get prediction
            label_id = int(np.argmax(logits, axis=1)[0])
            confidence = float(np.max(np.softmax(logits[0])))
            
            # Map to label
            intent = self.label_mapping[label_id]
            
            inference_time = (time.time() - start_time) * 1000  # Convert to ms
            
            return IntentResult(
                intent=intent,
                confidence=confidence,
                raw_logits=logits[0].tolist(),
                inference_time_ms=inference_time
            )
            
        except Exception as e:
            print(f"[IntentClassifier] ⚠️ ONNX inference error: {e}")
            # Fall back to rule-based classification
            return self._classify_with_fallback(user_text)
    
    def _classify_with_fallback(self, user_text: str) -> IntentResult:
        """Rule-based fallback classification"""
        start_time = time.time()
        text_lower = user_text.lower().strip()
        
        # Score each intent based on keyword matches
        intent_scores = {}
        for intent, keywords in self.intent_patterns.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            intent_scores[intent] = score
        
        # Determine best match
        best_intent = max(intent_scores, key=intent_scores.get)
        best_score = intent_scores[best_intent]
        confidence = min(0.5 + (best_score * 0.15), 0.9)
        
        # Default to casual_chat if no clear match
        if best_score == 0:
            best_intent = "casual_chat"
            confidence = 0.5
        
        inference_time = (time.time() - start_time) * 1000
        
        return IntentResult(
            intent=best_intent,
            confidence=confidence,
            raw_logits=[0.0] * len(self.label_mapping),  # No logits for rule-based
            inference_time_ms=inference_time
        )
    
    def classify_with_confidence(self, user_text: str) -> IntentResult:
        """Classify intent with detailed confidence information"""
        if self.model_loaded:
            return self._classify_with_onnx(user_text)
        else:
            return self._classify_with_fallback(user_text)
    
    def get_classification_stats(self) -> Dict[str, any]:
        """Get classifier performance statistics"""
        avg_inference_time = (self.total_inference_time / self.inference_count 
                            if self.inference_count > 0 else 0.0)
        
        return {
            "model_loaded": self.model_loaded,
            "onnx_model_available": MODEL_LOADED,
            "tokenizer_available": TOKENIZER_LOADED,
            "total_inferences": self.inference_count,
            "average_inference_time_ms": avg_inference_time * 1000,
            "target_inference_time_ms": 10.0,
            "performance_target_met": avg_inference_time * 1000 < 10.0,
            "classification_method": "ONNX neural network" if self.model_loaded else "Rule-based fallback",
            "supported_intents": len(self.label_mapping)
        }
    
    def get_supported_intents(self) -> List[str]:
        """Get list of supported intent labels"""
        return self.label_mapping.copy()
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        if self.model_loaded:
            return ["en", "pl", "it", "multilingual"]  # ONNX model supports multilingual
        else:
            return ["en"]  # Fallback is primarily English

# Global classifier instance (lazy loading for ONNX model)
_intent_classifier_instance = None

def _get_intent_classifier() -> IntentClassifier:
    """Get or create intent classifier instance (lazy loading)"""
    global _intent_classifier_instance
    if _intent_classifier_instance is None:
        print("[IntentClassifier] 🧠 Loading ONNX neural intent classification model...")
        _intent_classifier_instance = IntentClassifier()
        if _intent_classifier_instance.model_loaded:
            print("[IntentClassifier] ✅ ONNX neural model loaded successfully")
            print(f"[IntentClassifier] 🌍 Supported: {', '.join(_intent_classifier_instance.get_supported_languages())}")
        else:
            print("[IntentClassifier] ⚠️ Using rule-based fallback classifier")
    return _intent_classifier_instance

def classify_intent(user_text: str) -> str:
    """
    Main API function for intent classification using ONNX neural network
    
    Args:
        user_text: Input text to classify
        
    Returns:
        str: One of the intent labels (question, request, information, etc.)
        
    Examples:
        classify_intent("What time is it?") -> "question"
        classify_intent("Can you help me?") -> "request"
        classify_intent("I like pizza") -> "information"
    """
    classifier = _get_intent_classifier()
    return classifier.classify_intent(user_text)

def classify_intent_with_confidence(user_text: str) -> Tuple[str, float]:
    """
    Classify intent with confidence score using ONNX
    
    Args:
        user_text: Input text to classify
        
    Returns:
        Tuple[str, float]: (intent, confidence_score)
    """
    classifier = _get_intent_classifier()
    result = classifier.classify_with_confidence(user_text)
    return result.intent, result.confidence

def get_intent_classifier_stats() -> Dict[str, any]:
    """Get intent classifier performance statistics"""
    if _intent_classifier_instance:
        return _intent_classifier_instance.get_classification_stats()
    return {"model_loaded": False, "onnx_model_available": False}

# Test function for verification
def test_intent_classifier():
    """Test ONNX intent classifier with example inputs"""
    test_cases = [
        # Questions
        ("What time is it?", "question"),
        ("How are you doing?", "question"),
        ("When will this be finished?", "question"),
        
        # Requests
        ("Can you help me?", "request"),
        ("Please turn on the lights", "request"),
        ("Could you explain this?", "request"),
        
        # Information sharing
        ("I live in New York", "information"),
        ("My name is John", "information"),
        ("I'm going to the store", "information"),
        
        # Greetings
        ("Hello there!", "greeting"),
        ("Good morning", "greeting"),
        ("Hi buddy", "greeting"),
        
        # Goodbyes
        ("See you later", "goodbye"),
        ("Goodbye for now", "goodbye"),
        ("Take care", "goodbye"),
        
        # Complaints
        ("This is terrible", "complaint"),
        ("I hate this weather", "complaint"),
        ("So frustrating", "complaint"),
        
        # Compliments
        ("This is amazing!", "compliment"),
        ("Great job", "compliment"),
        ("Perfect solution", "compliment"),
        
        # Casual chat
        ("How's it going?", "casual_chat"),
        ("Nice weather today", "casual_chat"),
        ("What's up?", "casual_chat"),
        
        # Help requests
        ("I need help", "help"),
        ("I'm confused", "help"),
        ("Can you assist me?", "help"),
        
        # Confirmations
        ("Yes, that's right", "confirmation"),
        ("Okay, sounds good", "confirmation"),
        ("Exactly!", "confirmation"),
        
        # Multi-language tests
        ("Jak się masz?", "question"),  # Polish: How are you?
        ("Pomóż mi proszę", "request"),  # Polish: Please help me
        ("Come stai?", "question"),     # Italian: How are you?
        ("Aiutami per favore", "request"), # Italian: Please help me
    ]
    
    print("[IntentClassifier] 🧪 Running ONNX intent classifier tests...")
    correct = 0
    total = len(test_cases)
    total_inference_time = 0
    
    for text, expected in test_cases:
        start_time = time.time()
        result = classify_intent(text)
        inference_time = (time.time() - start_time) * 1000
        total_inference_time += inference_time
        
        status = "✅" if result == expected else "❌"
        print(f"  {status} '{text}' -> {result} (expected: {expected}) [{inference_time:.2f}ms]")
        if result == expected:
            correct += 1
    
    accuracy = (correct / total) * 100
    avg_inference = total_inference_time / total
    print(f"[IntentClassifier] 📊 Test accuracy: {accuracy:.1f}% ({correct}/{total})")
    print(f"[IntentClassifier] ⚡ Average inference: {avg_inference:.2f}ms")
    
    # Show performance stats
    stats = get_intent_classifier_stats()
    print(f"[IntentClassifier] 🔧 Method: {stats.get('classification_method', 'Unknown')}")
    print(f"[IntentClassifier] 🎯 Target met: {stats.get('performance_target_met', False)}")
    
    return accuracy >= 70  # 70% accuracy threshold

if __name__ == "__main__":
    # Run tests when script is executed directly
    test_intent_classifier()