# ai/chat_enhanced_smart_with_fusion.py - FACADE: Enhanced chat with intelligent memory fusion (delegates to ai.chat.core)
"""
This is a facade that maintains the original API while delegating to ai.chat.core.
All existing imports and function signatures are preserved for backward compatibility.
The fusion and consciousness functionality is now integrated into the core.
"""

import random
from typing import Iterator

# Import from new core 
from ai.chat.core import get_chat_core

# Maintain existing imports for compatibility
from ai.chat import generate_response_streaming
from ai.memory_fusion_intelligent import get_intelligent_unified_username

# Try to import smart memory and entropy systems
try:
    from ai.human_memory_smart import SmartHumanLikeMemory
    SMART_MEMORY_AVAILABLE = True
except ImportError:
    SMART_MEMORY_AVAILABLE = False
    class SmartHumanLikeMemory:
        def __init__(self, username):
            self.username = username

try:
    from ai.entropy_engine import get_entropy_engine, probabilistic_select, inject_consciousness_entropy, EntropyLevel
    from ai.emotion import get_emotional_system, process_emotional_context
    print("[ChatFusion] 🌀 Entropy system integrated for consciousness emergence")
    ENTROPY_AVAILABLE = True
except ImportError as e:
    print(f"[ChatFusion] ⚠️ Entropy system not available: {e}")
    ENTROPY_AVAILABLE = False

# Global chat core instance
_chat_core = get_chat_core()

# Global memory instances (maintained for compatibility)
smart_memories = {}

def get_smart_memory(username: str) -> SmartHumanLikeMemory:
    """Get or create smart memory for user - delegates to core where possible"""
    if SMART_MEMORY_AVAILABLE:
        if username not in smart_memories:
            smart_memories[username] = SmartHumanLikeMemory(username)
        return smart_memories[username]
    else:
        if username not in smart_memories:
            smart_memories[username] = SmartHumanLikeMemory(username)
        return smart_memories[username]

def generate_response_streaming_with_intelligent_fusion(question: str, username: str, lang: str = "en") -> Iterator[str]:
    """🧠 Generate response with intelligent memory fusion, smart memory + CONSCIOUSNESS ENTROPY - delegates to core"""
    
    print(f"[ChatFusion] 🧠 Starting intelligent fusion streaming for '{question}' from {username}")
    
    # All the entropy, fusion, and consciousness processing is now handled in the core
    # This facade simply delegates to the core which has all features integrated
    for chunk in _chat_core.generate_response_streaming(question, username, lang):
        yield chunk

# ============================================================================
# Legacy compatibility - the core now handles all advanced features
# ============================================================================

print("[ChatFusion] ✅ Chat fusion facade initialized - intelligent fusion, memory, and consciousness handled by ai.chat.core")