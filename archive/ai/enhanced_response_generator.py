"""
Enhanced Response Generator with Consciousness Integration
Created: 2025-01-17
"""

def generate_enhanced_response_with_consciousness(text: str, user_id: str, consciousness_context: str = None) -> str:
    """
    Generate enhanced response with full consciousness integration
    Fallback for when servers are not available
    """
    try:
        from ai.local_memory_manager import local_memory_manager
        
        # Get user context from memory
        user_context = local_memory_manager.get_user_context(user_id)
        
        # Check for name questions
        text_lower = text.lower().strip()
        if any(phrase in text_lower for phrase in ["what's my name", "whats my name", "what is my name", "my name", "who am i"]):
            facts = user_context.get('facts', [])
            for fact in facts:
                if isinstance(fact, str) and any(name_word in fact.lower() for name_word in ['name', 'called', 'david', 'francesco']):
                    # Extract name from fact
                    import re
                    name_patterns = [
                        r"name is (\w+(?:\s+\w+)?)",
                        r"called (\w+(?:\s+\w+)?)",
                        r"(\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)(?:\s|$)"
                    ]
                    
                    for pattern in name_patterns:
                        match = re.search(pattern, fact)
                        if match:
                            name = match.group(1).strip()
                            if name and len(name) > 1:
                                return f"Your name is {name}."
            
            # If no name found in facts, check context
            contexts = user_context.get('context', [])
            for ctx in contexts[-10:]:  # Check last 10 context items
                if isinstance(ctx, str) and ("i'm" in ctx.lower() or "name is" in ctx.lower()):
                    import re
                    name_match = re.search(r"(?:i'm|name is)\s+(\w+)", ctx.lower())
                    if name_match:
                        name = name_match.group(1).capitalize()
                        return f"Your name is {name}."
            
            return "I don't have your name stored yet. Could you tell me your name so I can remember it?"
        
        # Check for name introduction
        name_patterns = [
            r"my name is (\w+(?:\s+\w+)?)",
            r"i'?m (\w+(?:\s+\w+)?)(?:\s+by the way|$|\.|!)",
            r"call me (\w+(?:\s+\w+)?)",
            r"i'?m called (\w+(?:\s+\w+)?)"
        ]
        
        extracted_name = None
        for pattern in name_patterns:
            import re
            match = re.search(pattern, text_lower)
            if match:
                extracted_name = match.group(1).strip().title()
                break
        
        if extracted_name:
            # Store the name immediately
            from ai.local_memory_manager import MemoryEntry
            from datetime import datetime
            
            name_memory = MemoryEntry(
                timestamp=datetime.now().isoformat(),
                user_id=user_id,
                text=f"User's name is {extracted_name}",
                memory_type="fact",
                extracted_info={
                    "fact_category": "identity",
                    "fact_value": extracted_name,
                    "name_introduction": True,
                    "confidence": 0.95,
                    "source": "enhanced_response_generation"
                },
                confidence=0.95
            )
            local_memory_manager.store_memories([name_memory])
            
            return f"Nice to meet you, {extracted_name}! I'll remember your name. How can I help you today?"
        
        # Generate contextual response based on memory
        facts = user_context.get('facts', [])
        preferences = user_context.get('preferences', [])
        recent_context = user_context.get('context', [])
        
        # Create consciousness-aware response
        if facts:
            response = f"I remember some things about you: {', '.join(facts[:2])}. "
        else:
            response = ""
        
        # Add helpful response based on input
        if "how are you" in text_lower:
            response += "I'm doing well, thank you for asking! I'm here and ready to help with whatever you need."
        elif "what" in text_lower and "time" in text_lower:
            from datetime import datetime
            import pytz
            brisbane_tz = pytz.timezone('Australia/Brisbane')
            current_time = datetime.now(brisbane_tz)
            response += f"The current time in Brisbane is {current_time.strftime('%I:%M %p')}."
        elif "hello" in text_lower or "hi" in text_lower:
            if facts:
                response += "Hello! Good to see you again. What can I help you with?"
            else:
                response += "Hello! Nice to meet you. I'm Buddy, your AI assistant. What can I help you with?"
        else:
            response += "I understand you're asking about something. While I'm processing your request, is there anything specific I can help you with?"
        
        return response
        
    except Exception as e:
        print(f"[Enhanced Response] ❌ Error: {e}")
        return "I'm here and ready to help! What can I do for you?"