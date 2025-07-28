"""
Intent Extractor - Simple GPT4All-based intent detection
Created: 2025-01-27
Purpose: Extract user intent using GPT4All with fool-proof prompts and JSON fallback
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
        print("[IntentExtractor] ✅ GPT4All model loaded successfully")
    else:
        print(f"[IntentExtractor] ⚠️ GPT4All model file not found: {model_path}")
except ImportError:
    print("[IntentExtractor] ⚠️ GPT4All not installed, using fallback method")
except Exception as e:
    print(f"[IntentExtractor] ⚠️ GPT4All initialization failed: {e}")

def extract_intent(text: str) -> str:
    """Extract user intent using GPT4All-J or fallback method"""
    
    if GPT4ALL_AVAILABLE and extractor:
        try:
            prompt = f"""
TASK: What is the user's intent?

Message: "{text}"

Return ONLY one word: question, request, information, greeting, goodbye, complaint, compliment, help, or casual.
"""
            output = extractor.generate(prompt, max_tokens=10).strip()
            
            # Clean and validate output
            intent = output.strip().lower().strip('"').strip("'")
            valid_intents = ["question", "request", "information", "greeting", "goodbye", 
                           "complaint", "compliment", "help", "casual"]
            
            if intent in valid_intents:
                return intent
            else:
                return _fallback_extract_intent(text)
                
        except Exception as e:
            print(f"[IntentExtractor] ⚠️ GPT4All failed, using fallback: {e}")
            return _fallback_extract_intent(text)
    else:
        return _fallback_extract_intent(text)

def _fallback_extract_intent(text: str) -> str:
    """Fallback intent extraction using simple pattern matching"""
    text_lower = text.lower().strip()
    
    # Intent patterns
    if any(word in text_lower for word in ["what", "how", "when", "where", "who", "why", "?"]):
        return "question"
    elif any(word in text_lower for word in ["please", "can you", "could you", "would you", "help me"]):
        return "request"
    elif any(word in text_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon"]):
        return "greeting"
    elif any(word in text_lower for word in ["bye", "goodbye", "see you", "take care"]):
        return "goodbye"
    elif any(word in text_lower for word in ["terrible", "awful", "hate", "frustrated", "angry"]):
        return "complaint"
    elif any(word in text_lower for word in ["great", "awesome", "amazing", "wonderful", "love"]):
        return "compliment"
    elif any(word in text_lower for word in ["help", "assist", "confused", "don't understand"]):
        return "help"
    elif any(word in text_lower for word in ["i am", "my", "i have", "i like", "i don't like"]):
        return "information"
    else:
        return "casual"