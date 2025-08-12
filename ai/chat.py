# ai/chat.py - Enhanced LLM chat integration facade
# Delegates to ai.chat.core while preserving public API for backward compatibility

import requests
from ai.chat_core.core import (
    get_current_brisbane_time,
    ask_kobold_streaming as core_ask_kobold_streaming,
    build_messages,
    add_memory_context_to_messages,
    validate_and_enhance_response,
    apply_safety_filters,
    get_response_context_info
)
from config import KOBOLD_URL, MAX_TOKENS, TEMPERATURE, DEFAULT_LANG

# Import time and location helpers - kept for backward compatibility
try:
    from utils.time_helper import get_time_info_for_buddy
    LOCATION_HELPERS_AVAILABLE = True
except ImportError:
    LOCATION_HELPERS_AVAILABLE = False
    print("[Chat] ⚠️ Location helpers not available, using fallback")


def ask_kobold_streaming(messages, max_tokens=MAX_TOKENS):
    """✅ SMART RESPONSIVE: Wait for 40-50% completion or first complete phrase - delegates to core"""
    return core_ask_kobold_streaming(messages, max_tokens, TEMPERATURE, KOBOLD_URL)


def ask_kobold(messages, max_tokens=MAX_TOKENS):
    """Original non-streaming KoboldCpp request (kept for compatibility)"""
    payload = {
        "model": "llama3",
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": TEMPERATURE,
        "stream": False
    }
    
    try:
        response = requests.post(KOBOLD_URL, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if "choices" in data and len(data["choices"]) > 0:
                result = data["choices"][0]["message"]["content"].strip()
                return result
            else:
                return "KoboldCpp responded but no choices found."
        else:
            return f"KoboldCpp HTTP error: {response.status_code}"
            
    except requests.exceptions.ConnectionError:
        return "Cannot connect to KoboldCpp"
    except requests.exceptions.Timeout:
        return "KoboldCpp request timed out"
    except Exception as e:
        return f"Unexpected error: {e}"


def generate_response_streaming(question, username, lang=DEFAULT_LANG):
    """✅ ULTRA-RESPONSIVE: Generate AI response with TRUE streaming - delegates to core with enhancements"""
    try:
        print(f"[ChatStream] ⚡ Starting ULTRA-RESPONSIVE streaming generation for '{question}' from user '{username}'")
        
        # Check for unified username from memory fusion
        try:
            from ai.memory_fusion_intelligent import get_intelligent_unified_username
            unified_username = get_intelligent_unified_username(username)
            if unified_username != username:
                print(f"[ChatStream] 🎯 Using unified username: {username} → {unified_username}")
                username = unified_username
        except ImportError:
            pass
        except Exception as e:
            print(f"[ChatStream] ⚠️ Memory fusion error: {e}")

        # Build messages with enhanced memory context
        messages = build_messages(question, username)
        messages = add_memory_context_to_messages(messages, username, question)
        
        # Start streaming from core
        full_response = ""
        for chunk in ask_kobold_streaming(messages):
            if chunk and chunk.strip():
                # Apply safety filters and validation
                safe_chunk = apply_safety_filters(chunk.strip())
                validated_chunk = validate_and_enhance_response(safe_chunk, username)
                
                if validated_chunk:
                    full_response += validated_chunk + " "
                    print(f"[ChatStream] 📝 Streaming chunk: '{validated_chunk[:50]}...'")
                    yield validated_chunk
        
        # Add to conversation history
        if full_response.strip():
            from ai.memory import add_to_conversation_history  # Lazy import to break cycle
            add_to_conversation_history(username, question, full_response.strip())
            print(f"[ChatStream] ✅ Streaming complete for '{username}' - {len(full_response.split())} words")
        else:
            print(f"[ChatStream] ⚠️ No response generated for '{question}'")
            yield "I'm sorry, I didn't generate a proper response."
            
    except Exception as e:
        print(f"[ChatStream] ❌ Error in streaming generation: {e}")
        yield "Sorry, I encountered an error while generating a response."


def generate_response(question, username, lang=DEFAULT_LANG):
    """Original generate response function - uses streaming internally"""
    try:
        # Use streaming version internally but return complete response
        response_parts = []
        for chunk in generate_response_streaming(question, username, lang):
            response_parts.append(chunk)
        
        complete_response = " ".join(response_parts).strip()
        return complete_response if complete_response else "I couldn't generate a response."
        
    except Exception as e:
        print(f"[Chat] ❌ Error in non-streaming generation: {e}")
        return "Sorry, I encountered an error while generating a response."


def get_response_with_context_stats(question, username, lang=DEFAULT_LANG):
    """Get response with context statistics - facade function"""
    try:
        # Get context info
        from ai.memory import get_conversation_context  # Lazy import to break cycle
        context = get_conversation_context(username)
        context_length = len(context) if context else 0
        
        # Generate response
        response = generate_response(question, username, lang)
        
        stats = {
            'response': response,
            'context_length': context_length,
            'username': username,
            'question_length': len(question)
        }
        
        return stats
        
    except Exception as e:
        print(f"[Chat] ❌ Error getting response with stats: {e}")
        return {
            'response': "Sorry, I encountered an error.",
            'context_length': 0,
            'username': username,
            'question_length': len(question)
        }


def optimize_context_for_token_limit(context: str, max_tokens: int = 1500) -> str:
    """Optimize context for token limit - simplified implementation"""
    if not context:
        return ""
    
    # Simple truncation - core module can provide more sophisticated logic
    max_chars = max_tokens * 4  # Rough chars to tokens ratio
    
    if len(context) <= max_chars:
        return context
    
    # Truncate while preserving recent parts
    lines = context.split('\n')
    optimized_lines = []
    remaining_chars = max_chars
    
    # Take lines from the end (most recent) first
    for line in reversed(lines):
        if len(line) < remaining_chars:
            optimized_lines.insert(0, line)
            remaining_chars -= len(line)
        else:
            break
    
    return '\n'.join(optimized_lines)


def generate_streaming_response(question, username, lang=DEFAULT_LANG):
    """Generate streaming response - alias for main streaming function"""
    return generate_response_streaming(question, username, lang)


def get_response_mode():
    """Get current response mode"""
    return "ultra-responsive"