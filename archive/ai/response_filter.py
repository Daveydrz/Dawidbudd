"""
Response Filter - Prevents error messages from being sent to Kokoro TTS
Created: 2025-01-17
Purpose: Filter out error messages and technical failures from speech synthesis
Features: Error detection, fallback responses, connection failure handling
"""

import re
from typing import Optional, Tuple

def is_error_response(text: str) -> bool:
    """
    Check if a response text is an error message that shouldn't be spoken
    
    Args:
        text: Response text to check
        
    Returns:
        True if it's an error message, False otherwise
    """
    if not text or not text.strip():
        return True
    
    text_lower = text.lower().strip()
    
    # Common error message patterns
    error_patterns = [
        r"i apologize.*trouble.*connect",
        r"i'm having trouble connect",
        r"connection.*error",
        r"network.*error",
        r"timeout.*error",
        r"json.*parsing.*error",
        r"language model.*not.*available",
        r"processing system.*error",
        r"encountered.*error.*processing",
        r"response generation.*error",
        r"llm.*not.*available",
        r"server.*not.*responding",
        r"failed to connect",
        r"connection was aborted",
        r"winerror 10053",
        r"port \d+ is not available",
        r"gemma.*not.*available",
        r"consciousness.*processing.*failed"
    ]
    
    for pattern in error_patterns:
        if re.search(pattern, text_lower):
            return True
    
    # Check for very short responses (likely errors)
    if len(text.strip()) < 10:
        return True
    
    return False

def get_fallback_response(user_text: str, user_name: Optional[str] = None) -> str:
    """
    Generate a fallback response when the main LLM fails
    
    Args:
        user_text: Original user question/text
        user_name: User's name if known
        
    Returns:
        Appropriate fallback response
    """
    user_text_lower = user_text.lower().strip()
    
    # Personalize with name if available
    greeting = f"{user_name}, " if user_name else ""
    
    # Context-appropriate responses based on user input
    if any(word in user_text_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon"]):
        return f"Hey {greeting}good to hear from you!"
    
    elif any(word in user_text_lower for word in ["how are you", "how's it going", "what's up"]):
        return f"I'm doing well, {greeting}thanks for asking! How are you?"
    
    elif any(word in user_text_lower for word in ["time", "what time", "clock"]):
        return f"Let me check the time for you {greeting}in just a moment."
    
    elif any(word in user_text_lower for word in ["weather", "temperature", "rain", "sunny"]):
        return f"I'd be happy to help with weather information, {greeting}let me get that for you."
    
    elif any(word in user_text_lower for word in ["thank", "thanks", "appreciate"]):
        return f"You're very welcome, {greeting}happy to help!"
    
    elif any(word in user_text_lower for word in ["sorry", "apologize", "mistake"]):
        return f"No worries at all, {greeting}these things happen!"
    
    elif "?" in user_text:
        return f"That's a great question, {greeting}let me think about that for you."
    
    else:
        return f"I hear you, {greeting}let me process that and get back to you properly."

def filter_and_fix_response(response_text: str, user_text: str, user_name: Optional[str] = None) -> Tuple[str, bool]:
    """
    Filter response and provide fallback if it's an error message
    
    Args:
        response_text: Generated response text
        user_text: Original user input
        user_name: User's name if known
        
    Returns:
        Tuple of (filtered_response, was_filtered)
    """
    if is_error_response(response_text):
        fallback = get_fallback_response(user_text, user_name)
        print(f"[ResponseFilter] ❌ Filtered error response: '{response_text[:50]}...'")
        print(f"[ResponseFilter] ✅ Using fallback: '{fallback}'")
        return fallback, True
    
    return response_text.strip(), False

def should_speak_response(response_text: str) -> bool:
    """
    Determine if a response should be sent to TTS system
    
    Args:
        response_text: Response text to check
        
    Returns:
        True if it should be spoken, False otherwise
    """
    if not response_text or not response_text.strip():
        return False
    
    # Don't speak error messages
    if is_error_response(response_text):
        return False
    
    # Don't speak very short responses (likely incomplete)
    if len(response_text.strip()) < 5:
        return False
    
    return True

# Test the filter
if __name__ == "__main__":
    test_responses = [
        "Hello! How can I help you today?",
        "I apologize, but I'm having trouble connecting to my language model.",
        "I'm having trouble connecting to my processing systems right now.",
        "",
        "Hi",
        "That's a great question about the weather!",
        "Connection error occurred",
        "JSON parsing error: Expecting value",
        "WinError 10053: connection was aborted"
    ]
    
    print("🔍 Testing Response Filter:")
    for response in test_responses:
        is_error = is_error_response(response)
        should_speak = should_speak_response(response)
        filtered, was_filtered = filter_and_fix_response(response, "test question", "David")
        
        print(f"\nResponse: '{response}'")
        print(f"  Is Error: {is_error}")
        print(f"  Should Speak: {should_speak}")
        print(f"  Filtered: {was_filtered}")
        print(f"  Result: '{filtered}'")