# ai/chat_enhanced_smart.py - Smart LLM-based chat integration
import random
try:
    from ai.chat import generate_response_streaming, ask_kobold_streaming, get_current_brisbane_time
    from ai.human_memory_smart import SmartHumanLikeMemory
    from ai.memory import add_to_conversation_history
    _SMART_IMPORTS_AVAILABLE = True
except ImportError:
    print("[ChatSmart] ⚠️ Full smart memory system unavailable (missing dependencies)")
    _SMART_IMPORTS_AVAILABLE = False

# --- Provide reset API expected by main.py (safe even if no caches yet) ---
try:
    # If a base reset exists in ai.chat, re-export it for consistency.
    from ai.chat import reset_session_for_user as reset_session_for_user_smart
except Exception:
    # Local safe fallback: clear any per-user module caches if present.
    _SESSION_STATE = globals().get("_SESSION_STATE", {})
    _DIALOG_SUMMARIES = globals().get("_DIALOG_SUMMARIES", {})
    _FUSION_STATE = globals().get("_FUSION_STATE", {})

    def reset_session_for_user_smart(username: str) -> None:
        try:
            if isinstance(_SESSION_STATE, dict):
                _SESSION_STATE.pop(username, None)
            if isinstance(_DIALOG_SUMMARIES, dict):
                _DIALOG_SUMMARIES.pop(username, None)
            if isinstance(_FUSION_STATE, dict):
                _FUSION_STATE.pop(username, None)
        except Exception as e:
            print(f"[ChatSmart] reset_session_for_user_smart warning for {username}: {e}")
        print(f"[ChatSmart] reset session for {username}")

# Global smart memory instances
smart_memories = {}

def get_smart_memory(username: str):
    """Get or create smart memory for user"""
    if not _SMART_IMPORTS_AVAILABLE:
        print(f"[ChatSmart] ⚠️ Smart memory unavailable for {username} - missing dependencies")
        return None
    if username not in smart_memories:
        smart_memories[username] = SmartHumanLikeMemory(username)
    return smart_memories[username]

# Removed original function - replaced with safe export above

def generate_response_streaming_with_smart_memory(question, username, lang="en"):
    """Streaming version with smart LLM-based memory"""
    try:
        if not _SMART_IMPORTS_AVAILABLE:
            print(f"[SmartChat] ⚠️ Smart memory unavailable - using basic response for: '{question}' from {username}")
            yield "I'm having trouble accessing my smart memory system right now. "
            return
            
        print(f"[SmartChat] 🧠 Starting smart LLM-based streaming for '{question}' from {username}")
        
        # Get smart memory
        smart_memory = get_smart_memory(username)
        if not smart_memory:
            print("[SmartChat] ⚠️ Could not get smart memory - using basic response")
            yield "I'm having trouble accessing my memory system right now. "
            return
        
        # Smart LLM-based memory extraction
        smart_memory.extract_and_store_human_memories(question)
        
        # Check for natural context response
        context_response = smart_memory.check_for_natural_context_response()
        
        # If we have natural context, yield it first
        if context_response:
            print(f"[SmartChat] 💭 Smart memory response: {context_response}")
            yield context_response
            
            import time
            time.sleep(0.3)
            
            connectors = [" ", "Also, ", "And ", "By the way, ", "Oh, and "]
            yield random.choice(connectors)
        
        # Use existing streaming generation
        full_response = ""
        if _SMART_IMPORTS_AVAILABLE:
            for chunk in generate_response_streaming(question, username, lang):
                if chunk and chunk.strip():
                    full_response += chunk.strip() + " "
                    yield chunk.strip()
        else:
            yield "I'm currently operating in basic mode due to missing dependencies."
        
        # Add to conversation history
        if full_response.strip() and _SMART_IMPORTS_AVAILABLE:
            complete_response = context_response + " " + full_response if context_response else full_response
            add_to_conversation_history(username, question, complete_response.strip())
        
    except Exception as e:
        print(f"[SmartChat] ❌ Error: {e}")
        yield "Sorry, I'm having trouble thinking right now."