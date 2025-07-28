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
TASK: Extract facts from the user message below.

Message: "{text}"

Return ONLY valid JSON with these keys:
{{
  "name": "if user says their own name, else NONE",
  "likes": ["list of things user likes"],
  "dislikes": ["list of things user dislikes"],
  "emotion": "happy, sad, angry, or neutral"
}}
"""
            output = extractor.generate(prompt, max_tokens=60).strip()

            json_start = output.find("{")
            json_end = output.rfind("}")
            if json_start != -1 and json_end != -1:
                json_part = output[json_start:json_end+1]
                try:
                    return json.loads(json_part)
                except json.JSONDecodeError:
                    raise ValueError("Invalid JSON format")
            else:
                raise ValueError("No valid JSON found")

        except Exception as e:
            print(f"[ExtractorLLM] ⚠️ GPT4All failed, using fallback: {e}")
            return _fallback_extract_facts(text)
    else:
        return _fallback_extract_facts(text)

def extract_name(text: str) -> str:
    """Extract user's name using GPT4All-J or fallback method"""
    
    if GPT4ALL_AVAILABLE and extractor:
        try:
            prompt = f"""
TASK: If the user introduced themselves, extract their name.

Message: "{text}"

Return ONLY a name (e.g. "David"). 
If no name, reply with "NONE".
"""
            output = extractor.generate(prompt, max_tokens=10).strip()
            
            # Clean the output
            name = output.strip().strip('"').strip("'")
            if name and name.upper() != "NONE" and len(name) <= 20 and name.replace(" ", "").isalpha():
                return name
            else:
                return "NONE"
                
        except Exception as e:
            print(f"[ExtractorLLM] ⚠️ GPT4All name extraction failed: {e}")
            return _fallback_extract_name(text)
    else:
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
        r"this is (\w+)(?:\s|$|[,.])",  # Be specific about introductions
        r"you can call me (\w+)",
        r"i am called (\w+)"
    ]
    
    for pattern in name_patterns:
        match = re.search(pattern, text_lower)
        if match:
            name = match.group(1).title()
            # More strict validation - exclude common words that aren't names
            common_words = ["feeling", "having", "going", "doing", "getting", "saying", "thinking", 
                          "working", "living", "coming", "looking", "trying", "being", "making",
                          "happy", "sad", "angry", "confused", "excited", "worried", "fine", "okay",
                          "good", "bad", "great", "terrible", "amazing", "awful", "so", "very",
                          "really", "quite", "just", "now", "here", "there", "then", "when",
                          "what", "where", "why", "how", "who", "which", "absolutely", "definitely"]
            
            if len(name) >= 2 and name.isalpha() and name.lower() not in common_words:
                return name
    
    return "NONE"

def _fallback_extract_facts(text: str) -> dict:
    """Fallback fact extraction using simple pattern matching"""
    result = {"name": None, "likes": [], "dislikes": [], "emotion": "neutral"}
    
    text_lower = text.lower()
    
    # Extract name using the same improved logic as _fallback_extract_name
    name = _fallback_extract_name(text)
    if name != "NONE":
        result["name"] = name
    
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