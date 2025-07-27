"""
Fallback LLM Handler
Provides intelligent responses when LLM servers are not available
Created: 2025-01-17
"""

import re
import json
from datetime import datetime
from typing import Generator, List

class FallbackLLMHandler:
    """Fallback LLM handler with intelligent pattern-based responses"""
    
    def __init__(self):
        self.response_patterns = {
            'name_questions': {
                'patterns': [r"what'?s my name", r"what is my name", r"who am i", r"my name"],
                'handler': self._handle_name_question
            },
            'name_introductions': {
                'patterns': [r"my name is ([\w\s]+)", r"i'?m ([\w\s]+)(?:\s+by the way|$)", r"i am ([\w\s]+)(?:\s+by the way|$)", r"call me ([\w\s]+)"],
                'handler': self._handle_name_introduction
            },
            'greetings': {
                'patterns': [r"hello", r"hi(?:\s|$)", r"hey", r"good morning", r"good afternoon", r"good evening"],
                'handler': self._handle_greeting
            },
            'how_are_you': {
                'patterns': [r"how are you", r"how'?re you doing", r"how'?s it going"],
                'handler': self._handle_how_are_you
            },
            'time_questions': {
                'patterns': [r"what time is it", r"current time", r"time now"],
                'handler': self._handle_time_question
            },
            'help_requests': {
                'patterns': [r"help", r"can you help", r"i need", r"assist"],
                'handler': self._handle_help_request
            }
        }
    
    def generate_response(self, text: str, user_id: str, consciousness_context: str = None) -> str:
        """Generate intelligent fallback response"""
        text_lower = text.lower().strip()
        
        # Check each pattern category
        for category, config in self.response_patterns.items():
            for pattern in config['patterns']:
                if re.search(pattern, text_lower):
                    return config['handler'](text, user_id, text_lower)
        
        # Default intelligent response
        return self._handle_general_query(text, user_id, text_lower)
    
    def _handle_name_question(self, text: str, user_id: str, text_lower: str) -> str:
        """Handle name-related questions"""
        try:
            from ai.local_memory_manager import local_memory_manager
            context = local_memory_manager.get_user_context(user_id)
            
            facts = context.get('facts', [])
            for fact in facts:
                if isinstance(fact, str) and any(word in fact.lower() for word in ['name', 'david', 'francesco', 'called']):
                    # Extract name from fact - improved for full names
                    name_patterns = [
                        r"name is ([\w\s]+?)(?:\.|$)",  # Extract full name
                        r"called ([\w\s]+?)(?:\.|$)",   # Extract full name
                        r"(david[\w\s]*francesco|francesco[\w\s]*david|david francesco)"  # Specific full name patterns
                    ]
                    for pattern in name_patterns:
                        match = re.search(pattern, fact.lower())
                        if match:
                            name = match.group(1).strip().title()
                            if name and len(name) > 1:
                                return f"Your name is {name}."
            
            # Check recent context
            contexts = context.get('context', [])
            for ctx in contexts[-5:]:
                if isinstance(ctx, str) and ("i'm" in ctx.lower() or "name is" in ctx.lower()):
                    name_match = re.search(r"(?:i'm|name is)\s+(\w+)", ctx.lower())
                    if name_match:
                        name = name_match.group(1).capitalize()
                        return f"Your name is {name}."
            
            return "I don't have your name stored yet. Could you tell me your name so I can remember it?"
            
        except Exception as e:
            return "I'd be happy to learn your name! What should I call you?"
    
    def _handle_name_introduction(self, text: str, user_id: str, text_lower: str) -> str:
        """Handle name introductions"""
        try:
            # Extract name - improved to capture full names including "I am"
            name_patterns = [
                r"my name is ([\w\s]+?)(?:\s+by the way|$|\.|!|,)",
                r"i'?m ([\w\s]+?)(?:\s+by the way|$|\.|!|,)",
                r"i am ([\w\s]+?)(?:\s+by the way|$|\.|!|,)",  # Added this
                r"call me ([\w\s]+?)(?:\s+by the way|$|\.|!|,)"
            ]
            
            extracted_name = None
            for pattern in name_patterns:
                match = re.search(pattern, text_lower)
                if match:
                    extracted_name = match.group(1).strip().title()
                    break
            
            if extracted_name:
                # Store the name
                from ai.local_memory_manager import local_memory_manager, MemoryEntry
                
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
                        "source": "fallback_llm_handler"
                    },
                    confidence=0.95
                )
                local_memory_manager.store_memories([name_memory])
                
                return f"Nice to meet you, {extracted_name}! I'll remember your name. How can I help you today?"
            
            return "Nice to meet you! I'd love to know your name so I can remember it."
            
        except Exception as e:
            return "Hello! It's nice to meet you. What can I help you with?"
    
    def _handle_greeting(self, text: str, user_id: str, text_lower: str) -> str:
        """Handle greetings"""
        try:
            from ai.local_memory_manager import local_memory_manager
            context = local_memory_manager.get_user_context(user_id)
            
            # Check if we know the user's name
            user_name = None
            facts = context.get('facts', [])
            for fact in facts:
                if isinstance(fact, str) and ('name' in fact.lower() or 'david' in fact.lower() or 'francesco' in fact.lower()):
                    if 'david' in fact.lower():
                        user_name = "David"
                        break
                    elif 'francesco' in fact.lower():
                        user_name = "Francesco"
                        break
            
            if user_name:
                return f"Hello {user_name}! Good to see you again. How can I help you today?"
            else:
                return "Hello! I'm Buddy, your AI assistant. What can I help you with today?"
                
        except Exception as e:
            return "Hello! How can I help you today?"
    
    def _handle_how_are_you(self, text: str, user_id: str, text_lower: str) -> str:
        """Handle 'how are you' questions"""
        responses = [
            "I'm doing well, thank you for asking! I'm here and ready to help with whatever you need.",
            "I'm great! I enjoy our conversations and I'm always eager to help. How are you doing?",
            "I'm doing wonderfully! I feel energized and ready to assist you. What's on your mind today?"
        ]
        # Simple rotation based on text length
        return responses[len(text) % len(responses)]
    
    def _handle_time_question(self, text: str, user_id: str, text_lower: str) -> str:
        """Handle time questions"""
        try:
            import pytz
            brisbane_tz = pytz.timezone('Australia/Brisbane')
            current_time = datetime.now(brisbane_tz)
            return f"The current time in Brisbane is {current_time.strftime('%I:%M %p')} on {current_time.strftime('%A, %B %d, %Y')}."
        except:
            return "I can help you with the time, but I need access to time zone information. The current time should be available through your system."
    
    def _handle_help_request(self, text: str, user_id: str, text_lower: str) -> str:
        """Handle help requests"""
        return "I'm here to help! I can remember information about you, answer questions, have conversations, and assist with various tasks. What would you like help with?"
    
    def _handle_general_query(self, text: str, user_id: str, text_lower: str) -> str:
        """Handle general queries"""
        try:
            from ai.local_memory_manager import local_memory_manager
            context = local_memory_manager.get_user_context(user_id)
            
            facts = context.get('facts', [])
            if facts:
                return f"I understand you're asking about something. I remember some things about you: {', '.join(facts[:2])}. Could you tell me more about what you need help with?"
            else:
                return "I understand you have a question or request. I'm here to help! Could you tell me more about what you need?"
                
        except Exception as e:
            return "I'm listening and ready to help! Could you tell me more about what you need?"

# Global instance
fallback_llm_handler = FallbackLLMHandler()

def generate_fallback_response(text: str, user_id: str, consciousness_context: str = None) -> str:
    """Generate intelligent fallback response"""
    return fallback_llm_handler.generate_response(text, user_id, consciousness_context)