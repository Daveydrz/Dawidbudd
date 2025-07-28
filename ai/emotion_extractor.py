"""
Emotion Extractor - Simple GPT4All-based emotion detection
Created: 2025-01-27
Purpose: Extract user emotion using GPT4All with fool-proof prompts and JSON fallback
"""

import json
import re

# Try to load GPT4All-J model
extractor = None
GPT4ALL_AVAILABLE = False

try:
    from gpt4all import GPT4All
    import os
    model_path = "./extractor_model/ggml-gpt4all-j-v1.3-groovy.bin"
    if os.path.exists(model_path):
        extractor = GPT4All("ggml-gpt4all-j-v1.3-groovy.bin", model_path="./extractor_model")
        GPT4ALL_AVAILABLE = True
        print("[EmotionExtractor] ✅ GPT4All model loaded successfully")
    else:
        print(f"[EmotionExtractor] ⚠️ GPT4All model file not found: {model_path}")
except ImportError:
    print("[EmotionExtractor] ⚠️ GPT4All not installed, using fallback method")
except Exception as e:
    print(f"[EmotionExtractor] ⚠️ GPT4All initialization failed: {e}")

def extract_emotion(text: str) -> str:
    """Extract user emotion using GPT4All-J or fallback method"""
    
    if GPT4ALL_AVAILABLE and extractor:
        try:
            prompt = f"""
TASK: What emotion is the user expressing?

Message: "{text}"

Return ONLY one word: happy, sad, angry, worried, excited, neutral, or confused.
"""
            output = extractor.generate(prompt, max_tokens=10).strip()
            
            # Clean and validate output
            emotion = output.strip().lower().strip('"').strip("'")
            valid_emotions = ["happy", "sad", "angry", "worried", "excited", "neutral", "confused"]
            
            if emotion in valid_emotions:
                return emotion
            else:
                return _fallback_extract_emotion(text)
                
        except Exception as e:
            print(f"[EmotionExtractor] ⚠️ GPT4All failed, using fallback: {e}")
            return _fallback_extract_emotion(text)
    else:
        return _fallback_extract_emotion(text)

def _fallback_extract_emotion(text: str) -> str:
    """Fallback emotion extraction using keyword detection"""
    text_lower = text.lower().strip()
    
    # Emotion patterns
    if any(word in text_lower for word in ["happy", "great", "wonderful", "amazing", "excited", "good"]):
        return "happy"
    elif any(word in text_lower for word in ["sad", "disappointed", "upset", "bad", "terrible"]):
        return "sad"
    elif any(word in text_lower for word in ["angry", "mad", "frustrated", "annoyed"]):
        return "angry"
    elif any(word in text_lower for word in ["worried", "anxious", "nervous", "scared"]):
        return "worried"
    elif any(word in text_lower for word in ["excited", "thrilled", "pumped", "stoked"]):
        return "excited"
    elif any(word in text_lower for word in ["confused", "puzzled", "don't understand", "unclear"]):
        return "confused"
    else:
        return "neutral"