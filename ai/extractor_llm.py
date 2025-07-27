import json
import re

# Try to load GPT4All-J model (CPU only, no GPU required)
extractor = None
GPT4ALL_AVAILABLE = False

try:
    from gpt4all import GPT4All
    import os
    model_path = "./extractor_model/ggml-gpt4all-j-v1.3-groovy.bin"
    if os.path.exists(model_path):
        extractor = GPT4All("ggml-gpt4all-j-v1.3-groovy.bin", model_path="./extractor_model")
        GPT4ALL_AVAILABLE = True
        print("[ExtractorLLM] ✅ GPT4All model loaded successfully")
    else:
        print(f"[ExtractorLLM] ⚠️ GPT4All model file not found: {model_path}")
        print("[ExtractorLLM] ℹ️ Using fallback extraction method")
except ImportError:
    print("[ExtractorLLM] ⚠️ GPT4All not installed, using fallback extraction method")
except Exception as e:
    print(f"[ExtractorLLM] ⚠️ GPT4All initialization failed: {e}")
    print("[ExtractorLLM] ℹ️ Using fallback extraction method")

def extract_facts(text: str) -> dict:
    """Extract name, likes, dislikes, emotion using GPT4All-J or fallback method"""
    
    if GPT4ALL_AVAILABLE and extractor:
        try:
            prompt = f"""
You are an extractor. Your ONLY job is to return valid JSON.

Text: "{text}"

Extract:
- name (if user clearly says their OWN name)
- likes (things user says they like)
- dislikes (things user says they dislike)  
- emotion (happy, sad, neutral)

Return ONLY JSON. No explanation.
"""
            output = extractor.generate(prompt, max_tokens=120)
            
            try:
                # Try to parse JSON from output
                json_part = output.strip()
                if "```" in json_part:
                    json_part = json_part.split("```")[-1]
                return json.loads(json_part)
            except:
                print(f"[ExtractorLLM] ⚠️ Failed to parse GPT4All output: {output}")
                return _fallback_extract_facts(text)
                
        except Exception as e:
            print(f"[ExtractorLLM] ⚠️ GPT4All generation error: {e}")
            return _fallback_extract_facts(text)
    else:
        return _fallback_extract_facts(text)

def _fallback_extract_facts(text: str) -> dict:
    """Fallback fact extraction using simple pattern matching"""
    result = {"name": None, "likes": [], "dislikes": [], "emotion": "neutral"}
    
    text_lower = text.lower()
    
    # Extract name with improved patterns
    name_patterns = [
        r"my name is (\w+)",
        r"i'm (\w+)",
        r"i am (\w+)",
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
            if len(name) >= 2 and name.isalpha():
                result["name"] = name
                break
    
    # Extract likes
    like_patterns = [
        r"i like (.+?)(?:\.|$|,)",
        r"i love (.+?)(?:\.|$|,)",
        r"i enjoy (.+?)(?:\.|$|,)",
        r"i'm fond of (.+?)(?:\.|$|,)"
    ]
    
    for pattern in like_patterns:
        matches = re.findall(pattern, text_lower)
        for match in matches:
            like_item = match.strip()
            if like_item and len(like_item) < 50:  # Reasonable length
                result["likes"].append(like_item)
    
    # Extract dislikes
    dislike_patterns = [
        r"i don't like (.+?)(?:\.|$|,)",
        r"i hate (.+?)(?:\.|$|,)",
        r"i dislike (.+?)(?:\.|$|,)",
        r"i can't stand (.+?)(?:\.|$|,)"
    ]
    
    for pattern in dislike_patterns:
        matches = re.findall(pattern, text_lower)
        for match in matches:
            dislike_item = match.strip()
            if dislike_item and len(dislike_item) < 50:  # Reasonable length
                result["dislikes"].append(dislike_item)
    
    # Extract emotion using keyword detection
    if any(word in text_lower for word in ["happy", "great", "wonderful", "amazing", "excited", "good"]):
        result["emotion"] = "happy"
    elif any(word in text_lower for word in ["sad", "disappointed", "upset", "bad", "terrible"]):
        result["emotion"] = "sad"
    elif any(word in text_lower for word in ["angry", "mad", "frustrated", "annoyed"]):
        result["emotion"] = "angry"
    elif any(word in text_lower for word in ["worried", "anxious", "nervous", "scared"]):
        result["emotion"] = "worried"
    
    return result