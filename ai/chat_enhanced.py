# ai/chat_enhanced.py - Enhanced chat that integrates memory - thin wrapper over core
import random
from ai.chat_core.core import (
    ask_kobold_streaming,
    get_current_brisbane_time,
    build_messages,
    add_memory_context_to_messages,
    validate_and_enhance_response,
    apply_safety_filters
)
from ai.human_memory import HumanLikeMemory
from ai.memory import add_to_conversation_history

# Global human memory instances
human_memories = {}

def get_human_memory(username: str) -> HumanLikeMemory:
    """Get or create human memory for user"""
    if username not in human_memories:
        human_memories[username] = HumanLikeMemory(username)
    return human_memories[username]

def reset_session_for_user(username: str):
    """Reset session when conversation starts"""
    memory = get_human_memory(username)
    memory.reset_session_context()

def generate_response_with_human_memory(question, username, lang="en"):
    """Generate response with human-like memory integration - uses streaming internally"""
    try:
        print(f"[ChatEnhanced] 🧠 Starting human-like response for '{question}' from {username}")
        
        # Use streaming version internally but collect all chunks
        response_parts = []
        for chunk in generate_response_streaming_with_human_memory(question, username, lang):
            if chunk and chunk.strip():
                response_parts.append(chunk.strip())
        
        # Combine all parts
        complete_response = " ".join(response_parts)
        
        return complete_response if complete_response.strip() else "Sorry, I'm having trouble thinking right now."
        
    except Exception as e:
        print(f"[ChatEnhanced] ❌ Error: {e}")
        return "Sorry, I'm having trouble thinking right now."

def generate_response_streaming_with_human_memory(question, username, lang="en"):
    """Streaming version with human-like memory - uses core streaming"""
    try:
        print(f"[ChatEnhanced] 🧠 Starting human-like streaming for '{question}' from {username}")
        
        # Get human memory
        human_memory = get_human_memory(username)
        
        # Extract and store memories from user input
        human_memory.extract_and_store_human_memories(question)
        
        # Check for natural context response
        context_response = human_memory.check_for_natural_context_response()
        
        # If we have natural context, yield it first
        if context_response:
            print(f"[ChatEnhanced] 💭 Natural memory response: {context_response}")
            yield context_response
            
            # Small pause for natural flow
            import time
            time.sleep(0.3)
            
            # Add natural connector
            connectors = [" ", "Also, ", "And ", "By the way, ", "Oh, and "]
            yield random.choice(connectors)
        
        # Build messages and use core streaming directly
        messages = build_messages(question, username)
        messages = add_memory_context_to_messages(messages, username, question)
        
        # Stream from core with validation
        full_response = ""
        for chunk in ask_kobold_streaming(messages):
            if chunk and chunk.strip():
                safe_chunk = apply_safety_filters(chunk.strip())
                validated_chunk = validate_and_enhance_response(safe_chunk, username)
                
                if validated_chunk:
                    full_response += validated_chunk + " "
                    yield validated_chunk
        
        # Add to conversation history
        if full_response.strip():
            complete_response = context_response + " " + full_response if context_response else full_response
            add_to_conversation_history(username, question, complete_response.strip())
        
    except Exception as e:
        print(f"[ChatEnhanced] ❌ Error: {e}")
        yield "Sorry, I'm having trouble thinking right now."