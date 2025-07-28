"""
ONNX-based Memory Classifier - Real neural network memory type categorization
Created: 2025-01-17
Updated: 2025-01-17 - Real ONNX model integration
Purpose: Classify user text into fact, preference, or context using trained neural network
Features: Multi-language support, real AI classification, fast ONNX inference
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
    print("[MemoryClassifier] 🔤 DistilBERT tokenizer loaded successfully")
except Exception as e:
    TOKENIZER_LOADED = False
    print(f"[MemoryClassifier] ⚠️ Tokenizer loading failed: {e}")

# Load ONNX model (path updated if file is in same folder as main.py)
try:
    session = ort.InferenceSession("memory_classifier.onnx", providers=["CPUExecutionProvider"])
    MODEL_LOADED = True
    print("[MemoryClassifier] 🧠 ONNX memory classifier model loaded successfully")
except Exception as e:
    MODEL_LOADED = False
    session = None
    print(f"[MemoryClassifier] ⚠️ ONNX model loading failed: {e}")

@dataclass
class ClassificationResult:
    """Classification result with confidence"""
    memory_type: str
    confidence: float
    raw_logits: List[float]
    inference_time_ms: float
class MemoryClassifier:
    """ONNX-based neural memory classifier"""
    
    def __init__(self):
        """Initialize ONNX classifier"""
        self.model_loaded = MODEL_LOADED and TOKENIZER_LOADED
        self.inference_count = 0
        self.total_inference_time = 0.0
        
        # Label mapping (must match training order)
        self.label_mapping = ["preference", "fact", "context"]
        
        if self.model_loaded:
            print("[MemoryClassifier] ✅ ONNX neural classifier ready")
        else:
            print("[MemoryClassifier] ⚠️ Falling back to rule-based classification")
            # Initialize fallback rule-based classifier
            self._init_fallback_classifier()
    
    def _init_fallback_classifier(self):
        """Initialize rule-based fallback classifier"""
        # Simplified patterns for fallback
        self.preference_keywords = ["like", "love", "hate", "prefer", "enjoy", "dislike", "favorite", "favourite"]
        self.fact_keywords = ["name is", "years old", "birthday", "live in", "work as", "born", "my"]
        self.context_keywords = ["going to", "at", "just", "back", "currently", "how are", "what time"]
    
    def classify_memory_type(self, user_text: str) -> str:
        """
        Main API function - classify text into fact, preference, or context using ONNX
        Returns: "fact", "preference", or "context"
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
            
            return result.memory_type
            
        except Exception as e:
            print(f"[MemoryClassifier] ⚠️ Classification error: {e}")
            return "context"  # Safe fallback
    
    def _classify_with_onnx(self, user_text: str) -> ClassificationResult:
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
            memory_type = self.label_mapping[label_id]
            
            inference_time = (time.time() - start_time) * 1000  # Convert to ms
            
            return ClassificationResult(
                memory_type=memory_type,
                confidence=confidence,
                raw_logits=logits[0].tolist(),
                inference_time_ms=inference_time
            )
            
        except Exception as e:
            print(f"[MemoryClassifier] ⚠️ ONNX inference error: {e}")
            # Fall back to rule-based classification
            return self._classify_with_fallback(user_text)
    
    def _classify_with_fallback(self, user_text: str) -> ClassificationResult:
        """Rule-based fallback classification"""
        start_time = time.time()
        text_lower = user_text.lower().strip()
        
        # Simple keyword-based classification
        preference_score = sum(1 for keyword in self.preference_keywords if keyword in text_lower)
        fact_score = sum(1 for keyword in self.fact_keywords if keyword in text_lower)
        context_score = sum(1 for keyword in self.context_keywords if keyword in text_lower)
        
        # Determine best match
        scores = {"preference": preference_score, "fact": fact_score, "context": context_score}
        memory_type = max(scores, key=scores.get)
        confidence = min(0.5 + (scores[memory_type] * 0.2), 0.9)
        
        # Default to context if no clear match
        if scores[memory_type] == 0:
            memory_type = "context"
            confidence = 0.5
        
        inference_time = (time.time() - start_time) * 1000
        
        return ClassificationResult(
            memory_type=memory_type,
            confidence=confidence,
            raw_logits=[0.0, 0.0, 0.0],  # No logits for rule-based
            inference_time_ms=inference_time
        )
    
    def classify_with_confidence(self, user_text: str) -> ClassificationResult:
        """Classify text with detailed confidence information"""
        if self.model_loaded:
            return self._classify_with_onnx(user_text)
        else:
            return self._classify_with_fallback(user_text)
    
    def get_classification_stats(self) -> Dict[str, float]:
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
            "classification_method": "ONNX neural network" if self.model_loaded else "Rule-based fallback"
        }
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        if self.model_loaded:
            return ["en", "pl", "it", "multilingual"]  # ONNX model supports multilingual
        else:
            return ["en"]  # Fallback is primarily English

# Global classifier instance (lazy loading for ONNX model)
_classifier_instance = None

def _get_classifier() -> MemoryClassifier:
    """Get or create classifier instance (lazy loading)"""
    global _classifier_instance
    if _classifier_instance is None:
        print("[MemoryClassifier] 🧠 Loading ONNX neural memory classification model...")
        _classifier_instance = MemoryClassifier()
        if _classifier_instance.model_loaded:
            print("[MemoryClassifier] ✅ ONNX neural model loaded successfully")
            print(f"[MemoryClassifier] 🌍 Supported: {', '.join(_classifier_instance.get_supported_languages())}")
        else:
            print("[MemoryClassifier] ⚠️ Using rule-based fallback classifier")
    return _classifier_instance

def classify_memory_type(user_text: str) -> str:
    """
    Main API function for memory classification using ONNX neural network
    
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
    Classify memory type with confidence score using ONNX
    
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
    return {"model_loaded": False, "onnx_model_available": False}

# Test function for verification
def test_classifier():
    """Test ONNX classifier with example inputs"""
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
    
    print("[MemoryClassifier] 🧪 Running ONNX classifier tests...")
    correct = 0
    total = len(test_cases)
    total_inference_time = 0
    
    for text, expected in test_cases:
        start_time = time.time()
        result = classify_memory_type(text)
        inference_time = (time.time() - start_time) * 1000
        total_inference_time += inference_time
        
        status = "✅" if result == expected else "❌"
        print(f"  {status} '{text}' -> {result} (expected: {expected}) [{inference_time:.2f}ms]")
        if result == expected:
            correct += 1
    
    accuracy = (correct / total) * 100
    avg_inference = total_inference_time / total
    print(f"[MemoryClassifier] 📊 Test accuracy: {accuracy:.1f}% ({correct}/{total})")
    print(f"[MemoryClassifier] ⚡ Average inference: {avg_inference:.2f}ms")
    
    # Show performance stats
    stats = get_classifier_stats()
    print(f"[MemoryClassifier] 🔧 Method: {stats.get('classification_method', 'Unknown')}")
    print(f"[MemoryClassifier] 🎯 Target met: {stats.get('performance_target_met', False)}")
    
    return accuracy >= 80  # 80% accuracy threshold

if __name__ == "__main__":
    # Run tests when script is executed directly
    test_classifier()