"""
Simple LLM Handler - Port 5001 Main LLM Only
Created: 2025-01-17
Purpose: Handle ONLY final response generation from main LLM (port 5001)
Features: Clean prompt injection, streaming response, minimal processing
Architecture: Receives consciousness data from port 5002, generates response via port 5001
"""

import requests
import json
import time
from typing import Dict, Any, Generator, Optional

class SimpleLLMHandler:
    """Simple LLM handler for main LLM on port 5001"""
    
    def __init__(self, base_url: str = "http://localhost:5001"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/v1/generate"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        self.request_count = 0
        self.session_start = time.time()
        
        print("[SimpleLLM] 🚀 Initialized for port 5001 (Main LLM only)")
        
    def generate_response_with_consciousness(self, user_text: str, user_id: str, consciousness_context: str) -> Generator[str, None, None]:
        """
        Generate response using main LLM with injected consciousness data
        This is the ONLY LLM call per turn
        """
        
        # Build clean, minimal prompt with consciousness injection
        prompt = f"""Buddy is a helpful, empathetic AI assistant.

{consciousness_context}

User: {user_text}

Buddy:"""
        
        data = {
            "prompt": prompt,
            "max_context_length": 4096,
            "max_length": 500,
            "temperature": 0.7,
            "stream": True,
            "stop_sequence": ["User:", "Human:"]
        }
        
        try:
            start_time = time.time()
            print(f"[SimpleLLM] 🎯 Generating response for: '{user_text[:50]}...'")
            
            response = self.session.post(self.api_url, json=data, timeout=30, stream=True)
            response.raise_for_status()
            
            full_response = ""
            chunk_count = 0
            
            # Stream response chunks
            for line in response.iter_lines():
                if line:
                    try:
                        # Parse streaming response format
                        if line.startswith(b'data: '):
                            json_str = line[6:].decode('utf-8')
                            if json_str.strip() == '[DONE]':
                                break
                                
                            chunk_data = json.loads(json_str)
                            text_chunk = chunk_data.get('choices', [{}])[0].get('text', '')
                            
                            if text_chunk:
                                chunk_count += 1
                                full_response += text_chunk
                                yield text_chunk
                                
                    except json.JSONDecodeError:
                        # Handle non-JSON streaming format
                        text_chunk = line.decode('utf-8').strip()
                        if text_chunk and not text_chunk.startswith('[') and not text_chunk.endswith(']'):
                            chunk_count += 1
                            full_response += text_chunk + " "
                            yield text_chunk
            
            generation_time = time.time() - start_time
            self.request_count += 1
            
            print(f"[SimpleLLM] ✅ Response generated in {generation_time:.3f}s ({chunk_count} chunks)")
            
        except requests.exceptions.RequestException as e:
            print(f"[SimpleLLM] ❌ Network error: {e}")
            yield f"I apologize, but I'm having trouble connecting to my language model. Please try again."
            
        except Exception as e:
            print(f"[SimpleLLM] ❌ Error generating response: {e}")
            yield f"I apologize, but I encountered an error while processing your request."
    
    def is_available(self) -> bool:
        """Check if main LLM is available"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get LLM handler statistics"""
        return {
            "request_count": self.request_count,  
            "session_duration": time.time() - self.session_start,
            "base_url": self.base_url,
            "available": self.is_available()
        }

# Global instance
simple_llm_handler = SimpleLLMHandler()

def generate_response_with_consciousness(user_text: str, user_id: str, consciousness_context: str) -> Generator[str, None, None]:
    """
    Main API function for response generation with consciousness
    """
    return simple_llm_handler.generate_response_with_consciousness(user_text, user_id, consciousness_context)

def get_llm_stats() -> Dict[str, Any]:
    """Get LLM statistics"""
    return simple_llm_handler.get_stats()

if __name__ == "__main__":
    # Test the simple LLM handler
    consciousness_context = """BUDDY'S CONSCIOUSNESS STATE:
Current Emotion: curious
Motivation Level: 0.8
Active Goals: help user effectively, learn from interaction
Current Focus: user question about time
Inner Thoughts: User seems to want practical information
Personality: friendly

USER MEMORY:
Facts: User works in tech, lives in Brisbane
Preferences: Likes direct answers, prefers casual tone
Recent Context: Asked about weather earlier"""
    
    print("🎯 Testing Simple LLM Handler:")
    response_chunks = []
    for chunk in generate_response_with_consciousness("What time is it?", "test_user", consciousness_context):
        response_chunks.append(chunk)
        print(f"Chunk: '{chunk}'")
    
    print(f"\nFull response: {''.join(response_chunks)}")
    print(f"Stats: {get_llm_stats()}")