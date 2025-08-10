"""
Shared chat core functionality - streaming logic, message assembly, and utilities.

This module contains the shared implementation for streaming request/response logic,
message/prompt assembly, smart responsive thresholds, and safety/context utilities
used across ai.chat and ai.chat_enhanced modules.
"""
import re
import json
import requests
import time
from typing import Iterator, List, Dict, Any, Optional, Tuple
from ai.core.types import ChatMessage, StreamingContext
from utils.time_helper import get_time_info_for_buddy


def get_current_brisbane_time() -> Dict[str, str]:
    """
    Get current Brisbane time - delegates to utils.time_helper while maintaining 
    identical return schema for backward compatibility.
    """
    time_info = get_time_info_for_buddy()
    
    # Transform to match the expected schema from the original function
    return {
        'datetime': f"{time_info['current_date']} {time_info['current_time_24h']}:00",  # Add seconds for compatibility
        'time_12h': time_info['current_time_12h'],
        'time_24h': time_info['current_time_24h'], 
        'date': time_info['current_date'],
        'day': time_info['day_name'],
        'timezone': f"{time_info['timezone']} (+10:00)"  # Brisbane timezone format
    }


def build_messages(question: str, username: str, context: Optional[str] = None, 
                  system_prompt: Optional[str] = None) -> List[Dict[str, str]]:
    """
    Build message array for LLM request with context and system prompts.
    """
    messages = []
    
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    if context:
        messages.append({"role": "system", "content": f"Context: {context}"})
    
    messages.append({"role": "user", "content": question})
    
    return messages


def extract_streaming_response_chunks(line_text: str) -> Optional[str]:
    """
    Extract content from streaming response lines.
    Returns the text content or None if no content found.
    """
    if not line_text.strip() or line_text.startswith(':'):
        return None
        
    if line_text.startswith('data: '):
        data_content = line_text[6:]
        
        if data_content.strip() == '[DONE]':
            return None
            
        try:
            chunk_data = json.loads(data_content)
            
            if 'choices' in chunk_data and len(chunk_data['choices']) > 0:
                choice = chunk_data['choices'][0]
                
                content = ""
                if 'delta' in choice and 'content' in choice['delta']:
                    content = choice['delta']['content']
                elif 'message' in choice and 'content' in choice['message']:
                    content = choice['message']['content']
                
                return content if content else None
                
        except json.JSONDecodeError:
            return None
            
    return None


def apply_smart_responsive_logic(buffer: str, word_count: int, estimated_total_words: int,
                               first_chunk_sent: bool, min_words: int = 8,
                               target_completion: float = 0.45) -> Tuple[Optional[str], bool, str]:
    """
    Apply smart responsive logic to determine when to send chunks.
    
    Returns:
        - chunk to send (or None)
        - whether first chunk was sent
        - remaining buffer
    """
    if first_chunk_sent or word_count < min_words:
        return None, first_chunk_sent, buffer
        
    target_words = int(estimated_total_words * target_completion)
    
    # Priority 1: Look for complete sentences
    sentence_match = re.search(r'^(.*?[.!?])\s+', buffer)
    if sentence_match:
        first_chunk = sentence_match.group(1).strip()
        if len(first_chunk.split()) >= 4:  # Ensure meaningful length
            remaining_buffer = buffer[sentence_match.end():].strip()
            return first_chunk, True, remaining_buffer
    
    # Priority 2: Natural phrase boundaries
    phrase_match = re.search(r'^(.*?[,;:])\s+', buffer)
    if phrase_match and word_count >= 12:
        first_chunk = phrase_match.group(1).strip()
        if len(first_chunk.split()) >= 6:
            remaining_buffer = buffer[phrase_match.end():].strip()
            return first_chunk, True, remaining_buffer
    
    # Priority 3: Target completion reached
    if word_count >= target_words:
        # Find last complete word
        words = buffer.split()
        chunk_words = words[:target_words]
        first_chunk = " ".join(chunk_words)
        remaining_buffer = " ".join(words[target_words:])
        return first_chunk, True, remaining_buffer
    
    return None, first_chunk_sent, buffer


def ask_kobold_streaming(messages: List[Dict[str, str]], max_tokens: int = 1024,
                        temperature: float = 0.8, kobold_url: str = None) -> Iterator[str]:
    """
    Core streaming request to Kobold API with smart responsive logic.
    """
    from config import KOBOLD_URL, MAX_TOKENS, TEMPERATURE  # Import here to avoid cycles
    
    url = kobold_url or KOBOLD_URL
    payload = {
        "model": "llama3",
        "messages": messages,
        "max_tokens": max_tokens or MAX_TOKENS,
        "temperature": temperature or TEMPERATURE,
        "stream": True
    }
    
    try:
        print(f"[ChatCore] 🎭 Starting smart responsive streaming to: {url}")
        
        response = requests.post(url, json=payload, timeout=60, stream=True)
        
        if response.status_code == 200:
            buffer = ""
            word_count = 0
            first_chunk_sent = False
            estimated_total_words = (max_tokens or MAX_TOKENS) // 1.3  # Rough estimate
            
            # Smart thresholds
            MIN_WORDS_FOR_FIRST_CHUNK = 8
            TARGET_COMPLETION_PERCENTAGE = 0.45
            
            print(f"[ChatCore] 🎯 Targeting 40-50% completion (~{int(estimated_total_words * TARGET_COMPLETION_PERCENTAGE)} words) or first complete phrase")
            
            for line in response.iter_lines():
                if line:
                    line_text = line.decode('utf-8')
                    content = extract_streaming_response_chunks(line_text)
                    
                    if content:
                        buffer += content
                        word_count = len(buffer.split())
                        
                        # Apply smart responsive logic
                        chunk, first_chunk_sent, buffer = apply_smart_responsive_logic(
                            buffer, word_count, estimated_total_words, first_chunk_sent,
                            MIN_WORDS_FOR_FIRST_CHUNK, TARGET_COMPLETION_PERCENTAGE
                        )
                        
                        if chunk:
                            print(f"[ChatCore] 📝 SMART chunk: '{chunk[:50]}...'")
                            yield chunk
                        
                        # Yield remaining chunks when completion threshold is reached
                        elif first_chunk_sent and word_count >= 15:
                            # Find next natural break
                            next_break = re.search(r'^(.*?[.!?,:;])\s*', buffer)
                            if next_break:
                                next_chunk = next_break.group(1).strip()
                                if next_chunk and len(next_chunk.split()) >= 3:
                                    yield next_chunk
                                    buffer = buffer[next_break.end():].strip()
                                    word_count = len(buffer.split())
            
            # Yield any remaining content
            if buffer.strip():
                print(f"[ChatCore] 🏁 Final chunk: '{buffer.strip()[:50]}...'")
                yield buffer.strip()
        else:
            print(f"[ChatCore] ❌ HTTP {response.status_code}: {response.text}")
            yield "I'm having trouble connecting to the language model."
            
    except Exception as e:
        print(f"[ChatCore] ❌ Streaming error: {e}")
        yield "I encountered an error while generating a response."


def add_memory_context_to_messages(messages: List[Dict[str, str]], username: str, 
                                  question: str) -> List[Dict[str, str]]:
    """
    Add memory context to messages if available.
    This is a hook for memory integration - specific implementations
    should be in the enhanced modules.
    """
    # Basic implementation - enhanced modules can override this behavior
    from ai.memory import get_conversation_context, get_user_memory
    
    try:
        # Get conversation context
        context = get_conversation_context(username)
        if context:
            messages.insert(-1, {"role": "system", "content": f"Recent conversation: {context}"})
        
        # Get user memory
        user_memory = get_user_memory(username)  
        if user_memory:
            messages.insert(-1, {"role": "system", "content": f"User context: {user_memory}"})
            
    except Exception as e:
        print(f"[ChatCore] ⚠️ Memory context error: {e}")
    
    return messages


def validate_and_enhance_response(response: str, username: str) -> str:
    """
    Validate and enhance response appropriateness.
    Hook for validation systems.
    """
    try:
        from ai.memory import validate_ai_response_appropriateness
        is_appropriate, validated_response = validate_ai_response_appropriateness(username, response)
        
        if not is_appropriate:
            print(f"[ChatCore] 🛡️ Response corrected for appropriateness")
            return validated_response
            
    except Exception as e:
        print(f"[ChatCore] ⚠️ Validation error: {e}")
    
    return response


def apply_safety_filters(text: str) -> str:
    """
    Apply basic safety filters to text content.
    """
    # Basic content filtering - can be extended
    if not text or not text.strip():
        return "I need a moment to think about that."
    
    # Remove excessive whitespace
    text = ' '.join(text.split())
    
    return text


def get_response_context_info(username: str) -> Dict[str, Any]:
    """
    Get context information for response generation.
    """
    time_info = get_current_brisbane_time()
    
    context_info = {
        'username': username,
        'current_time': time_info,
        'timestamp': time.time()
    }
    
    return context_info