"""
ONNX-based Name Classifier - Local neural network name introduction detection
Created: 2025-01-17
Purpose: Detect when users introduce names without LLM calls using ONNX neural network
Features: Multi-language support, fast local inference, name extraction capabilities
"""

import onnxruntime as ort
import numpy as np
from transformers import AutoTokenizer
import time
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# Load tokenizer (same one used during training)
try:
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-multilingual-cased")
    TOKENIZER_LOADED = True
    print("[NameClassifier] 🔤 DistilBERT tokenizer loaded successfully")
except Exception as e:
    TOKENIZER_LOADED = False
    print(f"[NameClassifier] ⚠️ Tokenizer loading failed: {e}")

# Load ONNX model (path updated if file is in same folder as main.py)
try:
    session = ort.InferenceSession("name_classifier.onnx", providers=["CPUExecutionProvider"])
    MODEL_LOADED = True
    print("[NameClassifier] 🧠 ONNX name classifier model loaded successfully")
except Exception as e:
    MODEL_LOADED = False
    session = None
    print(f"[NameClassifier] ⚠️ ONNX model loading failed: {e}")

@dataclass
class NameResult:
    """Name classification result with extracted names"""
    contains_name: bool
    confidence: float
    extracted_names: List[str]
    name_type: str  # self_introduction, other_person, pet_name, place_name, general
    raw_logits: List[float]
    inference_time_ms: float

class NameClassifier:
    """ONNX-based neural name classifier"""
    
    def __init__(self):
        """Initialize ONNX name classifier"""
        self.model_loaded = MODEL_LOADED and TOKENIZER_LOADED
        self.inference_count = 0
        self.total_inference_time = 0.0
        
        # Name classification labels (must match training order)
        self.label_mapping = [
            "no_name",          # No names mentioned
            "self_introduction", # User introducing their own name
            "other_person",     # Mentioning someone else's name
            "pet_name",         # Pet or animal names
            "place_name",       # Location/place names
            "general_name"      # Other types of names
        ]
        
        if self.model_loaded:
            print("[NameClassifier] ✅ ONNX neural name classifier ready")
        else:
            print("[NameClassifier] ⚠️ Falling back to rule-based classification")
            # Initialize fallback rule-based classifier
            self._init_fallback_classifier()
    
    def _init_fallback_classifier(self):
        """Initialize rule-based fallback classifier"""
        # Name introduction patterns
        self.name_patterns = {
            "self_introduction": [
                r"my name is ([A-Z][a-zA-Z]+)",
                r"i'?m ([A-Z][a-zA-Z]+)",
                r"i am ([A-Z][a-zA-Z]+)",
                r"call me ([A-Z][a-zA-Z]+)",
                r"i'?m called ([A-Z][a-zA-Z]+)",
                r"they call me ([A-Z][a-zA-Z]+)",
                r"everyone calls me ([A-Z][a-zA-Z]+)"
            ],
            "other_person": [
                r"my friend ([A-Z][a-zA-Z]+)",
                r"my brother ([A-Z][a-zA-Z]+)",
                r"my sister ([A-Z][a-zA-Z]+)",
                r"my mom ([A-Z][a-zA-Z]+)",
                r"my dad ([A-Z][a-zA-Z]+)",
                r"my wife ([A-Z][a-zA-Z]+)",
                r"my husband ([A-Z][a-zA-Z]+)",
                r"([A-Z][a-zA-Z]+) said",
                r"([A-Z][a-zA-Z]+) told me",
                r"with ([A-Z][a-zA-Z]+)",
                r"([A-Z][a-zA-Z]+) is my"
            ],
            "pet_name": [
                r"my dog ([A-Z][a-zA-Z]+)",
                r"my cat ([A-Z][a-zA-Z]+)",
                r"my pet ([A-Z][a-zA-Z]+)",
                r"([A-Z][a-zA-Z]+) is my dog",
                r"([A-Z][a-zA-Z]+) is my cat",
                r"([A-Z][a-zA-Z]+) is my pet"
            ],
            "place_name": [
                r"in ([A-Z][a-zA-Z]+)",
                r"from ([A-Z][a-zA-Z]+)",
                r"to ([A-Z][a-zA-Z]+)",
                r"live in ([A-Z][a-zA-Z]+)",
                r"went to ([A-Z][a-zA-Z]+)",
                r"visiting ([A-Z][a-zA-Z]+)"
            ]
        }
        
        # Common names for better detection (basic list)
        self.common_names = {
            "male": ["John", "James", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Christopher"],
            "female": ["Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen"],
            "unisex": ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Jamie", "Avery", "Quinn", "Blake"]
        }
        
        # Common place names
        self.common_places = ["London", "Paris", "Tokyo", "New York", "Berlin", "Madrid", "Rome", "Warsaw", "Milan", "Chicago"]
    
    def classify_name(self, user_text: str) -> str:
        """
        Main API function - classify if text contains names using ONNX
        Returns: One of the name classification labels
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
            
            return result.name_type
            
        except Exception as e:
            print(f"[NameClassifier] ⚠️ Classification error: {e}")
            return "no_name"  # Safe fallback
    
    def _classify_with_onnx(self, user_text: str) -> NameResult:
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
            name_type = self.label_mapping[label_id]
            contains_name = name_type != "no_name"
            
            # Extract names using pattern matching (even with ONNX)
            extracted_names = self._extract_names_from_text(user_text, name_type)
            
            inference_time = (time.time() - start_time) * 1000  # Convert to ms
            
            return NameResult(
                contains_name=contains_name,
                confidence=confidence,
                extracted_names=extracted_names,
                name_type=name_type,
                raw_logits=logits[0].tolist(),
                inference_time_ms=inference_time
            )
            
        except Exception as e:
            print(f"[NameClassifier] ⚠️ ONNX inference error: {e}")
            # Fall back to rule-based classification
            return self._classify_with_fallback(user_text)
    
    def _classify_with_fallback(self, user_text: str) -> NameResult:
        """Rule-based fallback classification"""
        start_time = time.time()
        text_normalized = user_text.strip()
        
        # Try to match patterns and extract names
        best_type = "no_name"
        extracted_names = []
        best_confidence = 0.5
        
        for name_type, patterns in self.name_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text_normalized, re.IGNORECASE)
                if matches:
                    extracted_names.extend(matches)
                    best_type = name_type
                    best_confidence = 0.8  # Higher confidence for pattern matches
                    break
            if extracted_names:
                break
        
        # Additional heuristic checks
        if not extracted_names:
            # Look for capitalized words that might be names
            words = text_normalized.split()
            potential_names = []
            
            for word in words:
                # Check if word looks like a name (capitalized, alphabetic)
                if (word[0].isupper() and word.isalpha() and len(word) > 2 and 
                    word not in ["I", "The", "A", "An", "This", "That", "What", "How", "When", "Where"]):
                    potential_names.append(word)
            
            if potential_names:
                extracted_names = potential_names
                # Try to classify the type based on context
                text_lower = text_normalized.lower()
                if any(phrase in text_lower for phrase in ["my name", "i'm", "i am", "call me"]):
                    best_type = "self_introduction"
                    best_confidence = 0.7
                elif any(phrase in text_lower for phrase in ["my friend", "my brother", "my sister", "with", "told me"]):
                    best_type = "other_person"
                    best_confidence = 0.6
                elif any(phrase in text_lower for phrase in ["my dog", "my cat", "my pet"]):
                    best_type = "pet_name"
                    best_confidence = 0.6
                elif any(phrase in text_lower for phrase in ["in", "from", "to", "live", "went", "visiting"]):
                    best_type = "place_name"
                    best_confidence = 0.6
                else:
                    best_type = "general_name"
                    best_confidence = 0.5
        
        # Clean up extracted names (remove duplicates, common words)
        cleaned_names = []
        for name in extracted_names:
            if (name not in cleaned_names and 
                len(name) > 1 and 
                name not in ["Me", "My", "The", "And", "But", "Or", "So"]):
                cleaned_names.append(name)
        
        contains_name = len(cleaned_names) > 0
        if not contains_name:
            best_type = "no_name"
            best_confidence = 0.8  # High confidence when no names found
        
        inference_time = (time.time() - start_time) * 1000
        
        return NameResult(
            contains_name=contains_name,
            confidence=best_confidence,
            extracted_names=cleaned_names,
            name_type=best_type,
            raw_logits=[0.0] * len(self.label_mapping),  # No logits for rule-based
            inference_time_ms=inference_time
        )
    
    def _extract_names_from_text(self, text: str, predicted_type: str) -> List[str]:
        """Extract names from text based on predicted type"""
        names = []
        
        # Use the appropriate patterns based on predicted type
        if predicted_type in self.name_patterns:
            patterns = self.name_patterns[predicted_type]
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                names.extend(matches)
        
        # Also do general name extraction
        words = text.split()
        for word in words:
            if (word[0].isupper() and word.isalpha() and len(word) > 2 and 
                word not in ["I", "The", "A", "An", "This", "That", "What", "How", "When", "Where"]):
                names.append(word)
        
        # Remove duplicates and clean up
        return list(set(names))
    
    def classify_with_confidence(self, user_text: str) -> NameResult:
        """Classify names with detailed confidence and extraction information"""
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
            "supported_name_types": len(self.label_mapping)
        }
    
    def get_supported_name_types(self) -> List[str]:
        """Get list of supported name classification labels"""
        return self.label_mapping.copy()
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        if self.model_loaded:
            return ["en", "pl", "it", "multilingual"]  # ONNX model supports multilingual
        else:
            return ["en"]  # Fallback is primarily English

# Global classifier instance (lazy loading for ONNX model)
_name_classifier_instance = None

def _get_name_classifier() -> NameClassifier:
    """Get or create name classifier instance (lazy loading)"""
    global _name_classifier_instance
    if _name_classifier_instance is None:
        print("[NameClassifier] 🧠 Loading ONNX neural name classification model...")
        _name_classifier_instance = NameClassifier()
        if _name_classifier_instance.model_loaded:
            print("[NameClassifier] ✅ ONNX neural model loaded successfully")
            print(f"[NameClassifier] 🌍 Supported: {', '.join(_name_classifier_instance.get_supported_languages())}")
        else:
            print("[NameClassifier] ⚠️ Using rule-based fallback classifier")
    return _name_classifier_instance

def classify_name(user_text: str) -> str:
    """
    Main API function for name classification using ONNX neural network
    
    Args:
        user_text: Input text to classify
        
    Returns:
        str: One of the name classification labels (no_name, self_introduction, etc.)
        
    Examples:
        classify_name("My name is John") -> "self_introduction"
        classify_name("I went with Sarah") -> "other_person"  
        classify_name("My dog Rex is cute") -> "pet_name"
    """
    classifier = _get_name_classifier()
    return classifier.classify_name(user_text)

def classify_name_with_confidence(user_text: str) -> Tuple[str, float, List[str]]:
    """
    Classify names with confidence score and extracted names using ONNX
    
    Args:
        user_text: Input text to classify
        
    Returns:
        Tuple[str, float, List[str]]: (name_type, confidence_score, extracted_names)
    """
    classifier = _get_name_classifier()
    result = classifier.classify_with_confidence(user_text)
    return result.name_type, result.confidence, result.extracted_names

def extract_names_from_text(user_text: str) -> List[str]:
    """
    Extract names from text regardless of classification
    
    Args:
        user_text: Input text to analyze
        
    Returns:
        List[str]: List of extracted names
    """
    classifier = _get_name_classifier()
    result = classifier.classify_with_confidence(user_text)
    return result.extracted_names

def get_name_classifier_stats() -> Dict[str, any]:
    """Get name classifier performance statistics"""
    if _name_classifier_instance:
        return _name_classifier_instance.get_classification_stats()
    return {"model_loaded": False, "onnx_model_available": False}

# Test function for verification
def test_name_classifier():
    """Test ONNX name classifier with example inputs"""
    test_cases = [
        # Self introductions
        ("My name is John", "self_introduction"),
        ("I'm Sarah", "self_introduction"),
        ("Call me Mike", "self_introduction"),
        ("I am called David", "self_introduction"),
        
        # Other people
        ("My friend Alice said", "other_person"),
        ("I went with Bob", "other_person"),
        ("My brother Tom is coming", "other_person"),
        ("Lisa told me about it", "other_person"),
        
        # Pet names
        ("My dog Max is playing", "pet_name"),
        ("My cat Fluffy is sleeping", "pet_name"),
        ("Rex is my dog", "pet_name"),
        
        # Place names
        ("I live in London", "place_name"),
        ("Going to Paris", "place_name"),
        ("From New York", "place_name"),
        ("Visiting Tokyo", "place_name"),
        
        # No names
        ("How are you today?", "no_name"),
        ("The weather is nice", "no_name"),
        ("I like pizza", "no_name"),
        ("What time is it?", "no_name"),
        
        # General names
        ("Microsoft announced something", "general_name"),
        ("Apple released a new product", "general_name"),
        
        # Multi-language tests
        ("Nazywam się Jan", "self_introduction"),    # Polish: My name is Jan
        ("Mój przyjaciel Piotr", "other_person"),     # Polish: My friend Piotr  
        ("Mi chiamo Marco", "self_introduction"),     # Italian: My name is Marco
        ("Il mio amico Luca", "other_person"),        # Italian: My friend Luca
    ]
    
    print("[NameClassifier] 🧪 Running ONNX name classifier tests...")
    correct = 0
    total = len(test_cases)
    total_inference_time = 0
    
    for text, expected in test_cases:
        start_time = time.time()
        result = classify_name(text)
        inference_time = (time.time() - start_time) * 1000
        total_inference_time += inference_time
        
        # Also test name extraction
        names = extract_names_from_text(text)
        
        status = "✅" if result == expected else "❌"
        names_str = f" [Names: {', '.join(names)}]" if names else " [No names]"
        print(f"  {status} '{text}' -> {result} (expected: {expected}){names_str} [{inference_time:.2f}ms]")
        if result == expected:
            correct += 1
    
    accuracy = (correct / total) * 100
    avg_inference = total_inference_time / total
    print(f"[NameClassifier] 📊 Test accuracy: {accuracy:.1f}% ({correct}/{total})")
    print(f"[NameClassifier] ⚡ Average inference: {avg_inference:.2f}ms")
    
    # Show performance stats
    stats = get_name_classifier_stats()
    print(f"[NameClassifier] 🔧 Method: {stats.get('classification_method', 'Unknown')}")
    print(f"[NameClassifier] 🎯 Target met: {stats.get('performance_target_met', False)}")
    
    return accuracy >= 70  # 70% accuracy threshold

if __name__ == "__main__":
    # Run tests when script is executed directly
    test_name_classifier()