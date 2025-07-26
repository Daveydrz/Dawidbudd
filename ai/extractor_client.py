"""
Gemma Extractor Client - Local Classification via Gemma-2-2B on CPU
Created: 2025-01-17
Purpose: Handle all classification tasks (memory, intent, emotion, name) using dedicated Gemma model
Features: Single API call for all classifications, JSON parsing, fallback handling
"""

import requests
import json
import time
from typing import Dict, Any, Optional

class ExtractorClient:
    def __init__(self, base_url: str = "http://localhost:5002"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/v1/generate"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
    def classify_message(self, user_text: str) -> Dict[str, Any]:
        """
        Classify user message using Gemma-2-2B Extractor
        Returns JSON with memory_type, intent, emotion, name_introduction
        """
        prompt = f"""You are a classifier. For the message below, return JSON:

{{
  "memory_type": "fact|preference|context",
  "intent": "question|command|statement",
  "emotion": "joy|sadness|anger|fear|surprise|neutral",
  "name_introduction": true|false
}}

Message: "{user_text}"
"""

        data = {
            "prompt": prompt,
            "max_context_length": 1024,
            "max_length": 150,
            "temperature": 0.0,
            "stop_sequence": "\n\n"
        }

        try:
            start_time = time.time()
            response = self.session.post(self.api_url, json=data, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            text = result.get("results", [{}])[0].get("text", "").strip()
            
            # Try to parse JSON response
            classification = json.loads(text)
            
            # Validate response structure
            required_keys = ["memory_type", "intent", "emotion", "name_introduction"]
            for key in required_keys:
                if key not in classification:
                    raise ValueError(f"Missing key: {key}")
            
            # Log performance
            inference_time = time.time() - start_time
            print(f"[ExtractorClient] ✅ Classification complete in {inference_time:.3f}s")
            
            return classification
            
        except requests.exceptions.RequestException as e:
            print(f"[ExtractorClient] ❌ Network error: {e}")
            return self._get_fallback_classification()
        except json.JSONDecodeError as e:
            print(f"[ExtractorClient] ❌ JSON parsing error: {e}")
            return self._get_fallback_classification()
        except Exception as e:
            print(f"[ExtractorClient] ❌ Unexpected error: {e}")
            return self._get_fallback_classification()
    
    def _get_fallback_classification(self) -> Dict[str, Any]:
        """
        Fallback classification when Gemma extractor is unavailable
        Uses simple rule-based classification
        """
        return {
            "memory_type": "context",
            "intent": "statement", 
            "emotion": "neutral",
            "name_introduction": False
        }
    
    def is_available(self) -> bool:
        """Check if Gemma extractor is available"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False

# Global instance
extractor_client = ExtractorClient()

def classify_message(user_text: str) -> Dict[str, Any]:
    """
    Main API function for message classification
    """
    return extractor_client.classify_message(user_text)

def get_extractor_status() -> Dict[str, Any]:
    """Get extractor status and performance info"""
    return {
        "available": extractor_client.is_available(),
        "base_url": extractor_client.base_url,
        "api_url": extractor_client.api_url
    }

if __name__ == "__main__":
    # Test the extractor client
    test_messages = [
        "I like pizza",
        "My name is David", 
        "I'm going to the shop",
        "What time is it?",
        "I'm feeling sad today"
    ]
    
    print("🧪 Testing Gemma Extractor Client:")
    for msg in test_messages:
        result = classify_message(msg)
        print(f"'{msg}' -> {result}")