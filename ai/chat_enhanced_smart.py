# ai/chat_enhanced_smart.py - FACADE: Smart LLM-based chat integration (delegates to ai.chat.core)
"""
This is a facade that maintains the original API while delegating to ai.chat.core.
All existing imports and function signatures are preserved for backward compatibility.
The smart memory functionality is now integrated into the core.
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
    from ai.human_memory_smart import SmartHumanLikeMemory
    SMART_MEMORY_AVAILABLE = True
except ImportError:
    SMART_MEMORY_AVAILABLE = False
    # Create a stub class for compatibility
    class SmartHumanLikeMemory:
        def __init__(self, username):
            self.username = username
        def reset_session_context(self):
            pass

# Global chat core instance
_chat_core = get_chat_core()

# Global smart memory instances (maintained for compatibility)
smart_memories = {}

def get_smart_memory(username: str) -> SmartHumanLikeMemory:
    """Get or create smart memory for user - delegates to core where possible"""
    if SMART_MEMORY_AVAILABLE:
        if username not in smart_memories:
            smart_memories[username] = SmartHumanLikeMemory(username)
        return smart_memories[username]
    else:
        # Return stub memory
        if username not in smart_memories:
            smart_memories[username] = SmartHumanLikeMemory(username)
        return smart_memories[username]

def reset_session_for_user_smart(username: str):
    """Reset session when conversation starts - delegates to core"""
    # Reset core memory
    _chat_core.reset_session_for_user(username)
    
    # Also reset local memory for compatibility
    if username in smart_memories:
        smart_memories[username].reset_session_context()

def generate_response_streaming_with_smart_memory(question: str, username: str, lang: str = "en") -> Iterator[str]:
    """Streaming version with smart LLM-based memory - delegates to core"""
    print(f"[SmartChat] 🧠 Starting smart LLM-based streaming for '{question}' from {username}")
    
    # The core now handles smart memory integration automatically
    for chunk in _chat_core.generate_response_streaming(question, username, lang):
        yield chunk

# ============================================================================
# Legacy compatibility - these functions now delegate to core seamlessly
# ============================================================================

print("[SmartChat] ✅ Smart chat facade initialized - smart memory integration handled by ai.chat.core")