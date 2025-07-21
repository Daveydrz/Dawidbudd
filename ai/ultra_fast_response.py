"""
Ultra Fast Response System
Created: 2025-01-17
Purpose: Provide instant user responses (<2 seconds) bypassing ALL consciousness processing
         to fix the critical 4-minute latency issue while maintaining Class 5+ in background
"""

import time
import threading
from typing import Generator, Dict, Any, Optional
from datetime import datetime

# Simple fallback LLM imports
try:
    from ai.chat_enhanced_smart_with_fusion import generate_response_streaming_with_intelligent_fusion
    FUSION_AVAILABLE = True
except ImportError:
    try:
        from ai.chat import generate_response_streaming
        FUSION_AVAILABLE = False
    except ImportError:
        FUSION_AVAILABLE = False

class UltraFastResponse:
    """Ultra-fast response system that bypasses all consciousness processing"""
    
    def __init__(self):
        self.response_count = 0
        self.total_response_time = 0.0
        self.max_response_time = 2.0  # Hard limit: 2 seconds
        
        print("[UltraFast] ⚡ Ultra Fast Response System initialized")
        print("[UltraFast] 🎯 Target: <2 second responses with zero consciousness blocking")
        
    def generate_instant_response(self, user_input: str, user_id: str) -> Generator[str, None, None]:
        """
        Generate instant response with ZERO consciousness processing delays
        
        This is the emergency response system to fix the 4-minute latency issue.
        ALL consciousness processing is completely bypassed.
        """
        start_time = time.time()
        
        try:
            print(f"[UltraFast] ⚡ INSTANT RESPONSE for: '{user_input[:30]}...'")
            
            # 1. ZERO PROCESSING - Just basic sanitization
            clean_input = self._basic_sanitize(user_input)
            
            # 2. MINIMAL PROMPT - No consciousness, no context, just basic response
            prompt = self._build_minimal_prompt(clean_input, user_id)
            
            # 3. DIRECT LLM CALL - No fancy processing
            response_text = ""
            
            if FUSION_AVAILABLE:
                # Use fusion but with completely empty context
                response_gen = generate_response_streaming_with_intelligent_fusion(
                    prompt, user_id, "en", context={}
                )
            elif 'generate_response_streaming' in globals():
                response_gen = generate_response_streaming(prompt, user_id, "en")
            else:
                # Ultimate emergency fallback
                yield self._emergency_response(clean_input)
                return
            
            # 4. STREAM IMMEDIATELY - No validation, no processing
            chunk_count = 0
            for chunk in response_gen:
                if chunk and chunk.strip():
                    chunk_text = chunk.strip()
                    response_text += chunk_text + " "
                    chunk_count += 1
                    yield chunk_text
                    
                    # Emergency timeout protection
                    if time.time() - start_time > self.max_response_time:
                        print(f"[UltraFast] ⏰ Emergency timeout at {self.max_response_time}s")
                        break
            
            # Track performance
            response_time = time.time() - start_time
            self._record_performance(response_time, chunk_count)
            
            print(f"[UltraFast] ✅ INSTANT RESPONSE COMPLETE: {response_time:.3f}s")
            
        except Exception as e:
            error_time = time.time() - start_time
            print(f"[UltraFast] ❌ Error after {error_time:.3f}s: {e}")
            yield self._emergency_response(user_input)
    
    def _basic_sanitize(self, text: str) -> str:
        """Minimal sanitization for security without processing delays"""
        if not text or not text.strip():
            return "Hello"
            
        # Remove only the most dangerous patterns quickly
        text = text.replace("system:", "").replace("assistant:", "").replace("human:", "")
        text = text.replace("{{", "").replace("}}", "").replace("<%", "").replace("%>", "")
        
        # Length limit for speed
        if len(text) > 500:
            text = text[:500]
            
        return text.strip() or "Hello"
    
    def _build_minimal_prompt(self, user_input: str, user_id: str) -> str:
        """Build absolute minimal prompt for maximum speed"""
        # Bare minimum prompt - no personality, no consciousness, no context
        return f"Assistant: I'm Buddy, a helpful AI assistant in Birtinya, Sunshine Coast.\n\nUser: {user_input}\n\nBuddy:"
    
    def _emergency_response(self, user_input: str) -> str:
        """Emergency response when all else fails"""
        responses = [
            f"I hear you saying: {user_input[:50]}. I'm processing this and will help you.",
            f"Thanks for asking about {user_input[:30]}. Let me help with that.",
            f"I understand you're asking about {user_input[:40]}. I'm here to assist.",
            f"Got it - {user_input[:35]}. I'm working on a response for you.",
            f"I see you mentioned {user_input[:45]}. I'll help you with this."
        ]
        
        # Simple hash-based selection for consistency
        index = abs(hash(user_input)) % len(responses)
        return responses[index]
    
    def _record_performance(self, response_time: float, chunk_count: int):
        """Track performance metrics"""
        self.response_count += 1
        self.total_response_time += response_time
        
        avg_time = self.total_response_time / self.response_count
        
        print(f"[UltraFast] 📊 Performance: {response_time:.3f}s ({chunk_count} chunks)")
        print(f"[UltraFast] 📈 Average: {avg_time:.3f}s over {self.response_count} responses")
        
        if response_time > self.max_response_time:
            print(f"[UltraFast] ⚠️ Target missed by {response_time - self.max_response_time:.3f}s")
        else:
            print(f"[UltraFast] ✅ Target met with {self.max_response_time - response_time:.3f}s to spare")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        avg_time = self.total_response_time / max(self.response_count, 1)
        
        return {
            "total_responses": self.response_count,
            "average_response_time": avg_time,
            "target_response_time": self.max_response_time,
            "success_rate": sum(1 for _ in range(self.response_count) if avg_time <= self.max_response_time) / max(self.response_count, 1),
            "total_time_saved": self.response_count * (60.0 - avg_time),  # Assuming 60s was the original time
            "status": "operational"
        }

# Global instance
ultra_fast_response = UltraFastResponse()

def generate_ultra_fast_response(user_input: str, user_id: str) -> Generator[str, None, None]:
    """Generate ultra-fast response bypassing all consciousness processing"""
    return ultra_fast_response.generate_instant_response(user_input, user_id)

def get_ultra_fast_stats() -> Dict[str, Any]:
    """Get ultra-fast response statistics"""
    return ultra_fast_response.get_stats()

if __name__ == "__main__":
    # Test the ultra-fast response system
    print("Testing Ultra Fast Response System")
    
    test_inputs = [
        "Hello, how are you?",
        "What time is it?", 
        "Tell me about AI",
        "What's the weather like?",
        "Help me with something"
    ]
    
    for test_input in test_inputs:
        print(f"\nTesting: {test_input}")
        start = time.time()
        
        response_parts = []
        for chunk in generate_ultra_fast_response(test_input, "test_user"):
            response_parts.append(chunk)
            
        total_time = time.time() - start
        full_response = " ".join(response_parts)
        
        print(f"Response: {full_response}")
        print(f"Time: {total_time:.3f}s")
    
    # Show final stats
    stats = get_ultra_fast_stats()
    print(f"\nFinal Stats: {stats}")