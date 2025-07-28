"""
Dual-LLM HTTP Client System
Created: 2025-07-28
Purpose: Replace GPT4All with HTTP-based dual-LLM architecture
- Port 5001: Main LLM for conversations and reasoning
- Port 5002: Lightweight extractor (LaMini-Flan-248M/783M) for name, memory, emotions, and intents
"""

import requests
import json
import time
from typing import Dict, List, Any, Optional, Generator, Tuple
from datetime import datetime

class DualLLMClient:
    def __init__(self):
        self.main_llm_url = "http://localhost:5001"
        self.extractor_url = "http://localhost:5002"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        # Test connectivity on initialization
        self.main_llm_available = self._test_connection(self.main_llm_url)
        self.extractor_available = self._test_connection(self.extractor_url)
        
        print(f"[DualLLM] Main LLM (5001): {'✅ Available' if self.main_llm_available else '❌ Unavailable'}")
        print(f"[DualLLM] Extractor (5002): {'✅ Available' if self.extractor_available else '❌ Unavailable'}")
    
    def _test_connection(self, url: str, timeout: float = 2.0) -> bool:
        """Test if LLM server is available"""
        try:
            response = self.session.get(f"{url}/health", timeout=timeout)
            return response.status_code == 200
        except:
            return False
    
    def generate_response_with_consciousness(self, text: str, user: str, context: Dict[str, Any], stream: bool = True) -> Generator[str, None, None]:
        """Generate main conversation response via port 5001"""
        if not self.main_llm_available:
            print("[DualLLM] ⚠️ Main LLM unavailable, using fallback")
            yield from self._fallback_response(text, user, context)
            return
        
        try:
            payload = {
                "prompt": text,
                "user": user,
                "context": context,
                "stream": stream,
                "max_tokens": 150,
                "temperature": 0.7,
                "consciousness_mode": True
            }
            
            if stream:
                yield from self._stream_response(self.main_llm_url, payload)
            else:
                response = self._single_response(self.main_llm_url, payload)
                yield response
                
        except Exception as e:
            print(f"[DualLLM] ❌ Main LLM error: {e}")
            yield from self._fallback_response(text, user, context)
    
    def extract_facts(self, text: str) -> Dict[str, Any]:
        """Extract facts using lightweight extractor on port 5002"""
        if not self.extractor_available:
            print("[DualLLM] ⚠️ Extractor unavailable, using pattern matching")
            return self._fallback_extract_facts(text)
        
        try:
            payload = {
                "text": text,
                "task": "extract_facts",
                "format": "json",
                "schema": {
                    "name": "string or NONE",
                    "likes": "list",
                    "dislikes": "list", 
                    "emotion": "string"
                }
            }
            
            response = self.session.post(
                f"{self.extractor_url}/extract",
                json=payload,
                timeout=5.0
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"[DualLLM] ⚠️ Extractor error: {response.status_code}")
                return self._fallback_extract_facts(text)
                
        except Exception as e:
            print(f"[DualLLM] ❌ Extractor error: {e}")
            return self._fallback_extract_facts(text)
    
    def extract_name(self, text: str) -> str:
        """Extract name using lightweight extractor on port 5002"""
        if not self.extractor_available:
            return self._fallback_extract_name(text)
        
        try:
            payload = {
                "text": text,
                "task": "extract_name",
                "format": "string"
            }
            
            response = self.session.post(
                f"{self.extractor_url}/extract",
                json=payload,
                timeout=3.0
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("name", "NONE")
            else:
                return self._fallback_extract_name(text)
                
        except Exception as e:
            print(f"[DualLLM] ❌ Name extraction error: {e}")
            return self._fallback_extract_name(text)
    
    def extract_emotions_and_intents(self, text: str) -> Dict[str, Any]:
        """Extract emotions and intents using lightweight extractor on port 5002"""
        if not self.extractor_available:
            return self._fallback_extract_emotions_intents(text)
        
        try:
            payload = {
                "text": text,
                "task": "extract_emotions_intents",
                "format": "json",
                "schema": {
                    "emotions": "list",
                    "primary_emotion": "string",
                    "intents": "list",
                    "primary_intent": "string"
                }
            }
            
            response = self.session.post(
                f"{self.extractor_url}/extract",
                json=payload,
                timeout=4.0
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return self._fallback_extract_emotions_intents(text)
                
        except Exception as e:
            print(f"[DualLLM] ❌ Emotion/intent extraction error: {e}")
            return self._fallback_extract_emotions_intents(text)
    
    def _stream_response(self, url: str, payload: Dict[str, Any]) -> Generator[str, None, None]:
        """Stream response from LLM server"""
        try:
            response = self.session.post(
                f"{url}/generate/stream",
                json=payload,
                stream=True,
                timeout=60.0
            )
            
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        if 'token' in data:
                            yield data['token']
                        elif 'text' in data:
                            yield data['text']
                    except json.JSONDecodeError:
                        # Handle plain text responses
                        yield line.decode('utf-8')
                        
        except Exception as e:
            print(f"[DualLLM] ❌ Streaming error: {e}")
            yield f"I'm having trouble connecting to the main language model. {str(e)}"
    
    def _single_response(self, url: str, payload: Dict[str, Any]) -> str:
        """Get single response from LLM server"""
        try:
            payload_copy = payload.copy()
            payload_copy['stream'] = False
            
            response = self.session.post(
                f"{url}/generate",
                json=payload_copy,
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('text', result.get('response', ''))
            else:
                return f"Server error: {response.status_code}"
                
        except Exception as e:
            return f"Connection error: {e}"
    
    def _fallback_response(self, text: str, user: str, context: Dict[str, Any]) -> Generator[str, None, None]:
        """Fallback response when main LLM is unavailable"""
        fallback_responses = [
            "I'm here and ready to help! What would you like to talk about?",
            "I'm listening. How can I assist you today?",
            "That's interesting! Tell me more about that.",
            "I understand. What else would you like to discuss?",
            "Thanks for sharing that with me. What's on your mind?"
        ]
        
        # Simple keyword-based responses
        text_lower = text.lower()
        if any(word in text_lower for word in ['hello', 'hi', 'hey']):
            yield f"Hello {user}! How are you doing today?"
        elif any(word in text_lower for word in ['time', 'clock']):
            yield f"It's {datetime.now().strftime('%I:%M %p')} right now."
        elif any(word in text_lower for word in ['weather', 'temperature']):
            yield "I'd love to help with weather information, but I need my main systems online."
        else:
            import random
            yield random.choice(fallback_responses)
    
    def _fallback_extract_facts(self, text: str) -> Dict[str, Any]:
        """Fallback fact extraction using pattern matching"""
        import re
        
        # Simple pattern matching for common cases
        name = "NONE"
        likes = []
        dislikes = []
        emotion = "neutral"
        
        # Name patterns
        name_patterns = [
            r"my name is (\w+)",
            r"i'm (\w+)",
            r"i am (\w+)", 
            r"call me (\w+)"
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, text.lower())
            if match:
                name = match.group(1).title()
                break
        
        # Like patterns
        if 'like' in text.lower():
            likes = ['general interest']
        
        # Dislike patterns  
        if any(word in text.lower() for word in ['hate', 'dislike', "don't like"]):
            dislikes = ['mentioned dislike']
        
        # Emotion patterns
        if any(word in text.lower() for word in ['happy', 'great', 'good']):
            emotion = "happy"
        elif any(word in text.lower() for word in ['sad', 'bad', 'terrible']):
            emotion = "sad"
        elif any(word in text.lower() for word in ['angry', 'mad', 'frustrated']):
            emotion = "angry"
        
        return {
            "name": name,
            "likes": likes,
            "dislikes": dislikes,
            "emotion": emotion
        }
    
    def _fallback_extract_name(self, text: str) -> str:
        """Fallback name extraction using pattern matching"""
        import re
        
        patterns = [
            r"my name is (\w+)",
            r"i'm (\w+)",
            r"i am (\w+)", 
            r"call me (\w+)",
            r"name's (\w+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return match.group(1).title()
        
        return "NONE"
    
    def _fallback_extract_emotions_intents(self, text: str) -> Dict[str, Any]:
        """Fallback emotion and intent extraction"""
        emotions = []
        primary_emotion = "neutral"
        intents = []
        primary_intent = "general"
        
        text_lower = text.lower()
        
        # Emotion detection
        if any(word in text_lower for word in ['happy', 'joy', 'excited']):
            emotions.append("happy")
            primary_emotion = "happy"
        elif any(word in text_lower for word in ['sad', 'disappointed']):
            emotions.append("sad")
            primary_emotion = "sad"
        elif any(word in text_lower for word in ['angry', 'frustrated']):
            emotions.append("angry")
            primary_emotion = "angry"
        
        # Intent detection
        if any(word in text_lower for word in ['help', 'assist']):
            intents.append("request_help")
            primary_intent = "request_help"
        elif any(word in text_lower for word in ['what', 'how', 'why', 'when']):
            intents.append("ask_question")
            primary_intent = "ask_question"
        elif any(word in text_lower for word in ['tell', 'say', 'explain']):
            intents.append("request_information")
            primary_intent = "request_information"
        
        return {
            "emotions": emotions,
            "primary_emotion": primary_emotion,
            "intents": intents,
            "primary_intent": primary_intent
        }

# Global instance
dual_llm_client = DualLLMClient()

# Convenience functions for backward compatibility
def generate_response_streaming_with_intelligent_fusion(text: str, user: str, context: Dict[str, Any] = None) -> Generator[str, None, None]:
    """Backward compatibility function for existing code"""
    if context is None:
        context = {}
    
    yield from dual_llm_client.generate_response_with_consciousness(text, user, context, stream=True)

def extract_facts(text: str) -> Dict[str, Any]:
    """Extract facts using dual-LLM system"""
    return dual_llm_client.extract_facts(text)

def extract_name(text: str) -> str:
    """Extract name using dual-LLM system"""
    return dual_llm_client.extract_name(text)

def reset_session_for_user_smart(user: str):
    """Reset session - placeholder for compatibility"""
    print(f"[DualLLM] Session reset for user: {user}")