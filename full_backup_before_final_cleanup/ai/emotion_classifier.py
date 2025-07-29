"""
ONNX-based Emotion Classifier - Local neural network emotion detection
Created: 2025-01-17
Purpose: Classify user emotions without LLM calls using ONNX neural network
Features: Multi-language support, fast local inference, emotional intensity detection
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
    print("[EmotionClassifier] 🔤 DistilBERT tokenizer loaded successfully")
except Exception as e:
    TOKENIZER_LOADED = False
    print(f"[EmotionClassifier] ⚠️ Tokenizer loading failed: {e}")

# Load ONNX model (path updated if file is in same folder as main.py)
try:
    session = ort.InferenceSession("emotion_classifier.onnx", providers=["CPUExecutionProvider"])
    MODEL_LOADED = True
    print("[EmotionClassifier] 🧠 ONNX emotion classifier model loaded successfully")
except Exception as e:
    MODEL_LOADED = False
    session = None
    print(f"[EmotionClassifier] ⚠️ ONNX model loading failed: {e}")

@dataclass
class EmotionResult:
    """Emotion classification result with confidence and intensity"""
    emotion: str
    confidence: float
    intensity: str  # low, medium, high
    raw_logits: List[float]
    inference_time_ms: float

class EmotionClassifier:
    """ONNX-based neural emotion classifier"""
    
    def __init__(self):
        """Initialize ONNX emotion classifier"""
        self.model_loaded = MODEL_LOADED and TOKENIZER_LOADED
        self.inference_count = 0
        self.total_inference_time = 0.0
        
        # Emotion label mapping (must match training order)
        self.label_mapping = [
            "joy",          # Happy, excited, positive
            "sadness",      # Sad, melancholy, down
            "anger",        # Angry, frustrated, irritated
            "fear",         # Afraid, anxious, worried
            "surprise",     # Surprised, shocked, amazed
            "disgust",      # Disgusted, repulsed, disturbed
            "neutral",      # Calm, balanced, no strong emotion
            "love",         # Loving, affectionate, caring
            "excitement",   # Thrilled, enthusiastic, energetic
            "confusion"     # Confused, puzzled, uncertain
        ]
        
        if self.model_loaded:
            print("[EmotionClassifier] ✅ ONNX neural emotion classifier ready")
        else:
            print("[EmotionClassifier] ⚠️ Falling back to rule-based classification")
            # Initialize fallback rule-based classifier
            self._init_fallback_classifier()
    
    def _init_fallback_classifier(self):
        """Initialize rule-based fallback classifier"""
        # Emotion keywords with intensity markers
        self.emotion_patterns = {
            "joy": {
                "high": ["ecstatic", "thrilled", "overjoyed", "elated", "euphoric"],
                "medium": ["happy", "glad", "pleased", "cheerful", "delighted", "joyful"],
                "low": ["content", "satisfied", "okay", "fine", "good"]
            },
            "sadness": {
                "high": ["devastated", "heartbroken", "depressed", "miserable", "despair"],
                "medium": ["sad", "unhappy", "disappointed", "down", "blue", "melancholy"],
                "low": ["a bit sad", "somewhat down", "not great", "meh"]
            },
            "anger": {
                "high": ["furious", "enraged", "livid", "outraged", "infuriated"],
                "medium": ["angry", "mad", "frustrated", "irritated", "annoyed"],
                "low": ["bothered", "slightly annoyed", "mildly frustrated"]
            },
            "fear": {
                "high": ["terrified", "petrified", "panicked", "horrified"],
                "medium": ["afraid", "scared", "worried", "anxious", "nervous"],
                "low": ["concerned", "uneasy", "slightly worried"]
            },
            "surprise": {
                "high": ["shocked", "stunned", "amazed", "astounded"],
                "medium": ["surprised", "taken aback", "unexpected"],
                "low": ["oh", "really", "interesting"]
            },
            "disgust": {
                "high": ["revolted", "repulsed", "sickened"],
                "medium": ["disgusted", "gross", "yuck", "ew"],
                "low": ["not pleasant", "don't like"]
            },
            "love": {
                "high": ["adore", "love deeply", "cherish", "treasure"],
                "medium": ["love", "care about", "fond of"],
                "low": ["like", "appreciate"]
            },
            "excitement": {
                "high": ["thrilled", "pumped", "stoked", "fired up"],
                "medium": ["excited", "enthusiastic", "eager"],
                "low": ["interested", "looking forward"]
            },
            "confusion": {
                "high": ["totally confused", "completely lost", "bewildered"],
                "medium": ["confused", "puzzled", "don't understand"],
                "low": ["not sure", "unclear", "maybe"]
            }
        }
    
    def classify_emotion(self, user_text: str) -> str:
        """
        Main API function - classify user emotion using ONNX
        Returns: One of the emotion labels
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
            
            return result.emotion
            
        except Exception as e:
            print(f"[EmotionClassifier] ⚠️ Classification error: {e}")
            return "neutral"  # Safe fallback
    
    def _classify_with_onnx(self, user_text: str) -> EmotionResult:
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
            emotion = self.label_mapping[label_id]
            
            # Determine intensity based on confidence
            if confidence > 0.8:
                intensity = "high"
            elif confidence > 0.6:
                intensity = "medium"
            else:
                intensity = "low"
            
            inference_time = (time.time() - start_time) * 1000  # Convert to ms
            
            return EmotionResult(
                emotion=emotion,
                confidence=confidence,
                intensity=intensity,
                raw_logits=logits[0].tolist(),
                inference_time_ms=inference_time
            )
            
        except Exception as e:
            print(f"[EmotionClassifier] ⚠️ ONNX inference error: {e}")
            # Fall back to rule-based classification
            return self._classify_with_fallback(user_text)
    
    def _classify_with_fallback(self, user_text: str) -> EmotionResult:
        """Rule-based fallback classification"""
        start_time = time.time()
        text_lower = user_text.lower().strip()
        
        # Score each emotion and intensity
        best_emotion = "neutral"
        best_intensity = "low"
        best_score = 0
        
        for emotion, intensity_levels in self.emotion_patterns.items():
            for intensity, keywords in intensity_levels.items():
                score = sum(1 for keyword in keywords if keyword in text_lower)
                if score > best_score:
                    best_score = score
                    best_emotion = emotion
                    best_intensity = intensity
        
        # Calculate confidence based on matches
        confidence = min(0.4 + (best_score * 0.2), 0.9) if best_score > 0 else 0.5
        
        # Default to neutral if no clear emotional indicators
        if best_score == 0:
            best_emotion = "neutral"
            best_intensity = "low"
            confidence = 0.5
        
        inference_time = (time.time() - start_time) * 1000
        
        return EmotionResult(
            emotion=best_emotion,
            confidence=confidence,
            intensity=best_intensity,
            raw_logits=[0.0] * len(self.label_mapping),  # No logits for rule-based
            inference_time_ms=inference_time
        )
    
    def classify_with_confidence(self, user_text: str) -> EmotionResult:
        """Classify emotion with detailed confidence and intensity information"""
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
            "supported_emotions": len(self.label_mapping)
        }
    
    def get_supported_emotions(self) -> List[str]:
        """Get list of supported emotion labels"""
        return self.label_mapping.copy()
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        if self.model_loaded:
            return ["en", "pl", "it", "multilingual"]  # ONNX model supports multilingual
        else:
            return ["en"]  # Fallback is primarily English

# Global classifier instance (lazy loading for ONNX model)
_emotion_classifier_instance = None

def _get_emotion_classifier() -> EmotionClassifier:
    """Get or create emotion classifier instance (lazy loading)"""
    global _emotion_classifier_instance
    if _emotion_classifier_instance is None:
        print("[EmotionClassifier] 🧠 Loading ONNX neural emotion classification model...")
        _emotion_classifier_instance = EmotionClassifier()
        if _emotion_classifier_instance.model_loaded:
            print("[EmotionClassifier] ✅ ONNX neural model loaded successfully")
            print(f"[EmotionClassifier] 🌍 Supported: {', '.join(_emotion_classifier_instance.get_supported_languages())}")
        else:
            print("[EmotionClassifier] ⚠️ Using rule-based fallback classifier")
    return _emotion_classifier_instance

def classify_emotion(user_text: str) -> str:
    """
    Main API function for emotion classification using ONNX neural network
    
    Args:
        user_text: Input text to classify
        
    Returns:
        str: One of the emotion labels (joy, sadness, anger, etc.)
        
    Examples:
        classify_emotion("I'm so happy today!") -> "joy"
        classify_emotion("This is terrible") -> "anger"
        classify_emotion("I'm feeling okay") -> "neutral"
    """
    classifier = _get_emotion_classifier()
    return classifier.classify_emotion(user_text)

def classify_emotion_with_confidence(user_text: str) -> Tuple[str, float, str]:
    """
    Classify emotion with confidence score and intensity using ONNX
    
    Args:
        user_text: Input text to classify
        
    Returns:
        Tuple[str, float, str]: (emotion, confidence_score, intensity)
    """
    classifier = _get_emotion_classifier()
    result = classifier.classify_with_confidence(user_text)
    return result.emotion, result.confidence, result.intensity

def get_emotion_classifier_stats() -> Dict[str, any]:
    """Get emotion classifier performance statistics"""
    if _emotion_classifier_instance:
        return _emotion_classifier_instance.get_classification_stats()
    return {"model_loaded": False, "onnx_model_available": False}

# Test function for verification
def test_emotion_classifier():
    """Test ONNX emotion classifier with example inputs"""
    test_cases = [
        # Joy/Happiness
        ("I'm so happy today!", "joy"),
        ("This is amazing!", "joy"),
        ("I feel great!", "joy"),
        
        # Sadness
        ("I'm feeling really sad", "sadness"),
        ("This is terrible news", "sadness"),
        ("I'm so disappointed", "sadness"),
        
        # Anger
        ("This is so frustrating!", "anger"),
        ("I'm really angry about this", "anger"),
        ("This makes me furious", "anger"),
        
        # Fear/Anxiety
        ("I'm really worried about this", "fear"),
        ("This makes me nervous", "fear"),
        ("I'm scared", "fear"),
        
        # Surprise
        ("Wow, that's unexpected!", "surprise"),
        ("I can't believe it!", "surprise"),
        ("What a shock!", "surprise"),
        
        # Disgust
        ("That's disgusting", "disgust"),
        ("Ew, gross!", "disgust"),
        ("I find this repulsive", "disgust"),
        
        # Neutral
        ("It's okay", "neutral"),
        ("Just another day", "neutral"),
        ("The weather is fine", "neutral"),
        
        # Love/Affection
        ("I love this so much", "love"),
        ("This is wonderful", "love"),
        ("I adore this", "love"),
        
        # Excitement
        ("I'm so excited!", "excitement"),
        ("This is thrilling!", "excitement"),
        ("I can't wait!", "excitement"),
        
        # Confusion
        ("I don't understand", "confusion"),
        ("This is confusing", "confusion"),
        ("I'm puzzled", "confusion"),
        
        # Multi-language tests
        ("Jestem bardzo szczęśliwy", "joy"),     # Polish: I'm very happy
        ("To jest straszne", "sadness"),         # Polish: This is terrible
        ("Sono molto felice", "joy"),            # Italian: I'm very happy
        ("Questo è terribile", "sadness"),       # Italian: This is terrible
    ]
    
    print("[EmotionClassifier] 🧪 Running ONNX emotion classifier tests...")
    correct = 0
    total = len(test_cases)
    total_inference_time = 0
    
    for text, expected in test_cases:
        start_time = time.time()
        result = classify_emotion(text)
        inference_time = (time.time() - start_time) * 1000
        total_inference_time += inference_time
        
        status = "✅" if result == expected else "❌"
        print(f"  {status} '{text}' -> {result} (expected: {expected}) [{inference_time:.2f}ms]")
        if result == expected:
            correct += 1
    
    accuracy = (correct / total) * 100
    avg_inference = total_inference_time / total
    print(f"[EmotionClassifier] 📊 Test accuracy: {accuracy:.1f}% ({correct}/{total})")
    print(f"[EmotionClassifier] ⚡ Average inference: {avg_inference:.2f}ms")
    
    # Show performance stats
    stats = get_emotion_classifier_stats()
    print(f"[EmotionClassifier] 🔧 Method: {stats.get('classification_method', 'Unknown')}")
    print(f"[EmotionClassifier] 🎯 Target met: {stats.get('performance_target_met', False)}")
    
    return accuracy >= 70  # 70% accuracy threshold

if __name__ == "__main__":
    # Run tests when script is executed directly
    test_emotion_classifier()