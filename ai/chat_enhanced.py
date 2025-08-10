# ai/chat_enhanced.py - FACADE: Enhanced chat with human-like memory (delegates to ai.chat.core)
"""
This is a facade that maintains the original API while delegating to ai.chat.core.
All existing imports and function signatures are preserved for backward compatibility.
The human-like memory functionality is now integrated into the core.
"""

import random
from typing import Iterator

# Import from new core 
from ai.chat.core import get_chat_core

# Maintain existing imports for compatibility
from ai.chat import generate_response_streaming, ask_kobold_streaming, get_current_brisbane_time
from ai.memory import add_to_conversation_history

# Try to import original memory class for compatibility
try:
    from ai.human_memory import HumanLikeMemory
    HUMAN_MEMORY_AVAILABLE = True
except ImportError:
    HUMAN_MEMORY_AVAILABLE = False
    # Create a stub class for compatibility
    class HumanLikeMemory:
        def __init__(self, username):
            self.username = username
        def reset_session_context(self):
            pass

# Global chat core instance
_chat_core = get_chat_core()

# Global human memory instances (maintained for compatibility)
human_memories = {}

def get_human_memory(username: str) -> HumanLikeMemory:
    """Get or create human memory for user - delegates to core where possible"""
    if HUMAN_MEMORY_AVAILABLE:
        if username not in human_memories:
            human_memories[username] = HumanLikeMemory(username)
        return human_memories[username]
    else:
        # Return stub memory
        if username not in human_memories:
            human_memories[username] = HumanLikeMemory(username)
        return human_memories[username]

def reset_session_for_user(username: str):
    """Reset session when conversation starts - delegates to core"""
    # Reset core memory
    _chat_core.reset_session_for_user(username)
    
    # Also reset local memory for compatibility
    if username in human_memories:
        human_memories[username].reset_session_context()

def generate_response_with_human_memory(question: str, username: str, lang: str = "en") -> str:
    """Generate response with human-like memory integration - delegates to core"""
    # The core now handles memory integration automatically
    return _chat_core.generate_response_simple(question, username, lang)

def generate_response_streaming_with_human_memory(question: str, username: str, lang: str = "en") -> Iterator[str]:
    """Generate streaming response with human-like memory integration - delegates to core"""
    print(f"[ChatEnhanced] 🧠 Starting human-like streaming for '{question}' from {username}")
    
    # The core now handles memory integration automatically, including context responses
    for chunk in _chat_core.generate_response_streaming(question, username, lang):
        yield chunk

# ============================================================================
# Legacy compatibility - these functions now delegate to core seamlessly
# ============================================================================

print("[ChatEnhanced] ✅ Chat enhanced facade initialized - memory integration handled by ai.chat.core")