# ai/chat.py - FACADE: Enhanced LLM chat integration (delegates to ai.chat.core)
"""
This is a facade that maintains the original API while delegating to ai.chat.core.
All existing imports and function signatures are preserved for backward compatibility.
"""

import re
import requests
import json
from datetime import datetime
import pytz
from typing import Iterator, Dict, Any

# Import from new core
from ai.chat.core import get_chat_core
from ai.core.types import UserContext

# Maintain existing imports for compatibility
from ai.memory import get_conversation_context, get_user_memory
from config import *

# Import time and location helpers (preserved from original)
try:
    from utils.time_helper import get_time_info_for_buddy, get_buddy_current_time, get_buddy_location
    LOCATION_HELPERS_AVAILABLE = True
except ImportError:
    LOCATION_HELPERS_AVAILABLE = False
    print("[Chat] ⚠️ Location helpers not available, using fallback")

# Global chat core instance
_chat_core = get_chat_core()

# ============================================================================
# Public API Functions (delegating to core)
# ============================================================================

def set_user_context_provider(provider):
    """Set the user context provider for dependency injection"""
    _chat_core.set_user_context_provider(provider)

def get_current_brisbane_time():
    """Get current Brisbane time - delegates to core"""
    return _chat_core.get_current_brisbane_time()

def generate_response_streaming(question: str, username: str, lang: str = DEFAULT_LANG) -> Iterator[str]:
    """Generate streaming response - delegates to core with full integration"""
    for chunk in _chat_core.generate_response_streaming(question, username, lang):
        yield chunk

def generate_response(question: str, username: str, lang: str = DEFAULT_LANG) -> str:
    """Generate simple response - delegates to core"""
    return _chat_core.generate_response_simple(question, username, lang)

def generate_streaming_response(question: str, username: str, lang: str = DEFAULT_LANG) -> Iterator[str]:
    """Alternative streaming interface - delegates to core"""
    for chunk in _chat_core.generate_response_streaming(question, username, lang):
        yield chunk

# ============================================================================
# Legacy API Functions (preserved for compatibility)
# ============================================================================

def ask_kobold_streaming(messages, max_tokens=MAX_TOKENS):
    """Legacy Kobold streaming interface - preserved for compatibility"""
    # This maintains the original direct Kobold interface for any code that uses it
    try:
        payload = {
            "model": "llama3",
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": TEMPERATURE,
            "stream": True
        }
        
        response = requests.post(
            KOBOLD_URL,
            json=payload,
            timeout=KOBOLD_TIMEOUT,
            stream=True
        )
        
        if response.status_code != 200:
            print(f"[Chat] ❌ Kobold API error: {response.status_code}")
            return
        
        buffer = ""
        
        for line in response.iter_lines(decode_unicode=True):
            if not line or not line.startswith("data: "):
                continue
            
            try:
                data = json.loads(line[6:])  # Remove "data: " prefix
                
                if 'choices' in data and len(data['choices']) > 0:
                    delta = data['choices'][0].get('delta', {})
                    content = delta.get('content', '')
                    
                    if content:
                        buffer += content
                        
                        # Yield complete sentences or when buffer gets long
                        words = buffer.split()
                        if len(words) >= 8 or any(p in buffer for p in '.!?'):
                            yield buffer.strip()
                            buffer = ""
            
            except json.JSONDecodeError:
                continue
        
        # Yield any remaining content
        if buffer.strip():
            yield buffer.strip()
            
    except Exception as e:
        print(f"[Chat] ❌ Kobold streaming error: {e}")
        yield "Sorry, I encountered an error with the language model."

def ask_kobold(messages, max_tokens=MAX_TOKENS):
    """Legacy Kobold interface - preserved for compatibility"""
    try:
        payload = {
            "model": "llama3",  
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": TEMPERATURE,
            "stream": False
        }
        
        response = requests.post(KOBOLD_URL, json=payload, timeout=KOBOLD_TIMEOUT)
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content'].strip()
        else:
            print(f"[Chat] ❌ Kobold API error: {response.status_code}")
            
    except Exception as e:
        print(f"[Chat] ❌ Kobold error: {e}")
    
    return "Sorry, I'm having trouble connecting to my language processing system."

def get_response_with_context_stats(question: str, username: str, lang: str = DEFAULT_LANG) -> Dict[str, Any]:
    """Get response with context statistics"""
    # Generate response using core
    response = _chat_core.generate_response_simple(question, username, lang)
    
    # Get context stats (simplified)
    try:
        context = get_conversation_context(username, include_emotions=True, include_reminders=True)
        return {
            'response': response,
            'context_length': len(context),
            'context_tokens': len(context.split()),
            'question_length': len(question),
            'username': username
        }
    except Exception as e:
        print(f"[Chat] ⚠️ Context stats error: {e}")
        return {
            'response': response,
            'context_length': 0,
            'context_tokens': 0,
            'question_length': len(question),
            'username': username
        }

def optimize_context_for_token_limit(context: str, max_tokens: int = 1500) -> str:
    """Optimize context to fit within token limit"""
    if not context:
        return context
    
    words = context.split()
    if len(words) <= max_tokens:
        return context
    
    # Keep the most recent parts of the context
    truncated = words[-max_tokens:]
    return " ".join(truncated)

def get_response_mode():
    """Get current response mode"""
    return "enhanced_streaming"

# ============================================================================
# Internal Helper Functions (preserved for any direct usage)
# ============================================================================

def _get_user_display_name(username: str) -> str:
    """Get user display name - delegates to core"""
    return _chat_core.get_user_display_name(username)

# ============================================================================
# Module Initialization
# ============================================================================

# Configure the chat core with current settings
try:
    _chat_core.config.update({
        'max_tokens': MAX_TOKENS,
        'temperature': TEMPERATURE,
        'kobold_url': KOBOLD_URL,
        'kobold_timeout': KOBOLD_TIMEOUT,
        'chunk_words': 8,
        'response_delay': 0.5,
    })
except NameError:
    # Handle case where config constants are not defined
    print("[Chat] ⚠️ Some config constants not available, using defaults")

print("[Chat] ✅ Chat facade initialized - delegating to ai.chat.core")