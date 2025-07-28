"""
LLM Extractor - Dual-LLM HTTP Client System
Updated: 2025-07-28
Purpose: Replace GPT4All with HTTP-based extraction via port 5002
Uses: Lightweight extractor (LaMini-Flan-248M/783M) for name, memory, emotions, and intents
"""

import json
import re

# Import dual-LLM client system
try:
    from ai.dual_llm_client import dual_llm_client
    DUAL_LLM_AVAILABLE = True
    print("[ExtractorLLM] ✅ Dual-LLM client loaded successfully")
except ImportError as e:
    DUAL_LLM_AVAILABLE = False
    print(f"[ExtractorLLM] ❌ Dual-LLM client not available: {e}")
    print("[ExtractorLLM] ℹ️ Using fallback extraction method")

def extract_facts(text: str) -> dict:
    """Extract name, likes, dislikes, emotion using Dual-LLM port 5002 or fallback method"""
    
    if DUAL_LLM_AVAILABLE:
        try:
            return dual_llm_client.extract_facts(text)
        except Exception as e:
            print(f"[ExtractorLLM] ⚠️ Dual-LLM extraction failed: {e}, using fallback")
    
    # Fallback pattern matching when dual-LLM is unavailable
    return _fallback_extract_facts(text)

def extract_name(text: str) -> str:
    """Extract user's name using Dual-LLM port 5002 or fallback method"""
    
    if DUAL_LLM_AVAILABLE:
        try:
            return dual_llm_client.extract_name(text)
        except Exception as e:
            print(f"[ExtractorLLM] ⚠️ Dual-LLM name extraction failed: {e}, using fallback")
    
    # Fallback pattern matching when dual-LLM is unavailable  
    return _fallback_extract_name(text)

def _fallback_extract_name(text: str) -> str:
    """Fallback name extraction using pattern matching"""
    text_lower = text.lower()
    
    # Extract name with improved patterns - more specific to avoid false matches
    name_patterns = [
        r"my name is (\w+)",
        r"i'm (\w+)(?:\s|$|[,.])",  # Require word boundary after name
        r"i am (\w+)(?:\s|$|[,.])",  # Require word boundary after name  
        r"call me (\w+)",
        r"name's (\w+)",
        r"this is (\w+)",
        r"it's (\w+)",
        r"i am called (\w+)"
    ]
    
    for pattern in name_patterns:
        match = re.search(pattern, text_lower)
        if match:
            name = match.group(1).title()
            # Validate name (2-20 chars, only letters)
            if 2 <= len(name) <= 20 and name.isalpha():
                return name
    
    return "NONE"

def _fallback_extract_facts(text: str) -> dict:
    """Fallback fact extraction using pattern matching and keywords"""
    
    name = _fallback_extract_name(text)
    likes = []
    dislikes = []
    emotion = "neutral"
    
    text_lower = text.lower()
    
    # Extract likes
    like_patterns = [
        r"i like (.+?)(?:\.|$|,|and|but)",
        r"i love (.+?)(?:\.|$|,|and|but)",
        r"i enjoy (.+?)(?:\.|$|,|and|but)",
        r"my favorite (.+?)(?:\.|$|,|and|but)",
        r"(.+?) is good",
        r"(.+?) is great",
        r"(.+?) is amazing"
    ]
    
    for pattern in like_patterns:
        matches = re.findall(pattern, text_lower)
        for match in matches:
            if len(match.strip()) > 0 and len(match.strip()) < 50:
                likes.append(match.strip())
    
    # Extract dislikes
    dislike_patterns = [
        r"i hate (.+?)(?:\.|$|,|and|but)",
        r"i don't like (.+?)(?:\.|$|,|and|but)",
        r"i dislike (.+?)(?:\.|$|,|and|but)",
        r"(.+?) is bad",
        r"(.+?) is terrible",
        r"(.+?) sucks"
    ]
    
    for pattern in dislike_patterns:
        matches = re.findall(pattern, text_lower)
        for match in matches:
            if len(match.strip()) > 0 and len(match.strip()) < 50:
                dislikes.append(match.strip())
    
    # Detect emotion based on keywords and context
    emotion_keywords = {
        "happy": ["happy", "joy", "excited", "great", "wonderful", "amazing", "fantastic", "good", "pleased"],
        "sad": ["sad", "depressed", "down", "unhappy", "disappointed", "upset", "hurt"],
        "angry": ["angry", "mad", "furious", "irritated", "annoyed", "frustrated", "pissed"],
        "neutral": []
    }
    
    emotion_scores = {"happy": 0, "sad": 0, "angry": 0, "neutral": 0}
    
    for emotion_type, keywords in emotion_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                emotion_scores[emotion_type] += 1
    
    # Determine primary emotion
    max_score = max(emotion_scores.values())
    if max_score > 0:
        for emotion_type, score in emotion_scores.items():
            if score == max_score:
                emotion = emotion_type
                break
    
    return {
        "name": name,
        "likes": likes,
        "dislikes": dislikes,
        "emotion": emotion
    }