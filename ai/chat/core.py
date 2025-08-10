"""
ai/chat/core.py - Core chat functionality with streaming, memory, and fusion

This module consolidates all chat functionality into a clean core that handles:
- Basic LLM streaming responses 
- Human-like memory integration
- Smart LLM-based memory
- Memory fusion and consciousness/entropy integration
- Message assembly and threshold management
- Safety/appropriateness validation
"""

import re
import json
import time
import random
import requests
from datetime import datetime
from typing import Iterator, Optional, Dict, Any, List
import pytz

# Import from core boundary to avoid cycles
from ai.core.types import ChatResponse, StreamingChunk, ChatProvider, UserContext

# Memory systems
from ai.memory import get_conversation_context, get_user_memory, add_to_conversation_history

# Time and location helpers
try:
    from utils.time_helper import get_time_info_for_buddy, get_buddy_current_time, get_buddy_location
    LOCATION_HELPERS_AVAILABLE = True
except ImportError:
    LOCATION_HELPERS_AVAILABLE = False

# Memory fusion
try:
    from ai.memory_fusion_intelligent import get_intelligent_unified_username
    MEMORY_FUSION_AVAILABLE = True
except ImportError:
    MEMORY_FUSION_AVAILABLE = False

# Human-like memory
try:
    from ai.human_memory_smart import SmartHumanLikeMemory
    SMART_MEMORY_AVAILABLE = True
except ImportError:
    SMART_MEMORY_AVAILABLE = False

# Consciousness and entropy system
try:
    from ai.entropy_engine import get_entropy_engine, probabilistic_select, inject_consciousness_entropy, EntropyLevel
    from ai.emotion import get_emotional_system, process_emotional_context
    CONSCIOUSNESS_AVAILABLE = True
except ImportError:
    CONSCIOUSNESS_AVAILABLE = False


class ChatCore:
    """Core chat engine with all features consolidated"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._default_config()
        
        # Memory storage
        self._human_memories = {}  # Traditional human memory
        self._smart_memories = {}  # Smart LLM-based memory
        
        # User context provider (dependency injection)
        self._user_context_provider = None
        
        # LLM provider (dependency injection) 
        self._llm_provider = None
    
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration"""
        return {
            'max_tokens': 500,
            'temperature': 0.7,
            'streaming_enabled': True,
            'chunk_words': 8,
            'response_delay': 0.5,
            'enable_memory': True,
            'enable_fusion': True,
            'enable_consciousness': True,
            'kobold_url': 'http://127.0.0.1:5001/api/v1/generate',
            'kobold_timeout': 30,
        }
    
    def set_user_context_provider(self, provider):
        """Set user context provider for dependency injection"""
        self._user_context_provider = provider
    
    def set_llm_provider(self, provider: ChatProvider):
        """Set LLM provider for dependency injection"""
        self._llm_provider = provider
    
    def get_human_memory(self, username: str):
        """Get or create human memory for user"""
        if not SMART_MEMORY_AVAILABLE:
            return None
        if username not in self._human_memories:
            self._human_memories[username] = SmartHumanLikeMemory(username)
        return self._human_memories[username]
    
    def get_smart_memory(self, username: str):
        """Get or create smart memory for user"""
        if not SMART_MEMORY_AVAILABLE:
            return None
        if username not in self._smart_memories:
            self._smart_memories[username] = SmartHumanLikeMemory(username)
        return self._smart_memories[username]
    
    def reset_session_for_user(self, username: str):
        """Reset session when conversation starts"""
        if username in self._human_memories:
            self._human_memories[username].reset_session_context()
        if username in self._smart_memories:
            self._smart_memories[username].reset_session_context()
    
    def get_user_display_name(self, username: str) -> str:
        """Get user display name using context provider"""
        if self._user_context_provider:
            return self._user_context_provider.get_display_name(username)
        return username
    
    def get_current_brisbane_time(self) -> Dict[str, str]:
        """Get current Brisbane time with multiple formats"""
        if LOCATION_HELPERS_AVAILABLE:
            try:
                return get_buddy_current_time()
            except:
                pass
        
        # Fallback implementation
        try:
            brisbane_tz = pytz.timezone('Australia/Brisbane')
            current_time = datetime.now(brisbane_tz)
            return {
                'datetime': current_time.strftime("%Y-%m-%d %H:%M:%S"),
                'time_12h': current_time.strftime("%I:%M %p"),
                'time_24h': current_time.strftime("%H:%M"),
                'date': current_time.strftime("%A, %B %d, %Y"),
                'day': current_time.strftime("%A"),
                'timezone': 'Australia/Brisbane (+10:00)'
            }
        except:
            return {
                'datetime': "2025-07-06 18:59:59",
                'time_12h': "6:59 PM", 
                'time_24h': "18:59",
                'date': "Sunday, July 6, 2025",
                'day': "Sunday",
                'timezone': 'Australia/Brisbane (+10:00)'
            }
    
    def generate_response_streaming(self, question: str, username: str, language: str = "en") -> Iterator[str]:
        """
        Generate streaming response with full feature integration:
        - Memory fusion (if available)
        - Human-like memory integration (if available)
        - Consciousness/entropy processing (if available)
        - LLM streaming with proper chunking
        """
        print(f"[ChatCore] 🚀 Starting integrated response for '{question}' from {username}")
        
        # Step 1: Apply memory fusion if available
        effective_username = username
        if MEMORY_FUSION_AVAILABLE and self.config.get('enable_fusion', True):
            try:
                unified_username = get_intelligent_unified_username(username)
                if unified_username != username:
                    effective_username = unified_username
                    print(f"[ChatCore] 🎯 Memory fusion: {username} → {effective_username}")
            except Exception as e:
                print(f"[ChatCore] ⚠️ Memory fusion error: {e}")
        
        # Step 2: Process consciousness/entropy if available
        emotional_context = {}
        if CONSCIOUSNESS_AVAILABLE and self.config.get('enable_consciousness', True):
            try:
                emotional_context = process_emotional_context(question, f"chat_{effective_username}")
                entropy_engine = get_entropy_engine()
                print(f"[ChatCore] 🎭 Emotional state: {emotional_context.get('primary_emotion', 'neutral')}")
                print(f"[ChatCore] 🌀 Consciousness: {entropy_engine.get_consciousness_metrics().get('consciousness_score', 0):.2f}")
            except Exception as e:
                print(f"[ChatCore] ⚠️ Consciousness error: {e}")
        
        # Step 3: Check for memory-based context responses
        memory_response = ""
        if self.config.get('enable_memory', True):
            memory = self.get_smart_memory(effective_username)
            if memory:
                try:
                    memory.extract_and_store_human_memories(question)
                    context_response = memory.check_for_natural_context_response()
                    if context_response:
                        memory_response = context_response
                        print(f"[ChatCore] 💭 Memory response: {memory_response}")
                except Exception as e:
                    print(f"[ChatCore] ⚠️ Memory error: {e}")
        
        # Step 4: Yield memory response first if available
        if memory_response:
            yield memory_response
            time.sleep(0.3)  # Brief pause
            connectors = [" ", "Also, ", "And ", "By the way, ", "Oh, and "]
            yield random.choice(connectors)
        
        # Step 5: Generate main LLM response
        full_response = ""
        try:
            # Get user display name for personalization
            display_name = self.get_user_display_name(effective_username)
            
            # Build enhanced prompt with context
            enhanced_question = self._build_enhanced_prompt(question, effective_username, display_name, emotional_context)
            
            # Stream LLM response
            for chunk in self._stream_llm_response(enhanced_question, effective_username, language):
                if chunk and chunk.strip():
                    # Apply consciousness entropy if available
                    if CONSCIOUSNESS_AVAILABLE and emotional_context:
                        chunk = self._apply_entropy_to_chunk(chunk, emotional_context)
                    
                    full_response += chunk.strip() + " "
                    yield chunk.strip()
        
        except Exception as e:
            print(f"[ChatCore] ❌ LLM streaming error: {e}")
            yield "Sorry, I'm having trouble thinking right now."
            return
        
        # Step 6: Store conversation history
        if full_response.strip():
            complete_response = memory_response + " " + full_response if memory_response else full_response
            try:
                add_to_conversation_history(effective_username, question, complete_response.strip())
                print(f"[ChatCore] ✅ Stored conversation for {effective_username}")
            except Exception as e:
                print(f"[ChatCore] ⚠️ History storage error: {e}")
    
    def _build_enhanced_prompt(self, question: str, username: str, display_name: str, emotional_context: Dict) -> str:
        """Build enhanced prompt with context"""
        # Get user memory for context
        memory_context = ""
        try:
            memory = get_user_memory(username)
            reminders = memory.get_today_reminders()
            if reminders:
                top_reminders = reminders[:2]  # Top 2 only
                memory_context = f"\\nImportant for today: {', '.join(top_reminders)}"
        except:
            pass
        
        # Get location and time context
        time_info = self.get_current_brisbane_time()
        location = "Birtinya, Sunshine Coast, Queensland"  # This should come from config
        
        # Build the enhanced prompt
        enhanced_prompt = f"""You are Buddy, an AI assistant in {location}. Current time: {time_info['time_12h']} on {time_info['date']}.

User: {question}{memory_context}

Respond naturally and helpfully. Be concise but friendly."""
        
        return enhanced_prompt
    
    def _stream_llm_response(self, prompt: str, username: str, language: str) -> Iterator[str]:
        """Stream response from LLM with proper chunking"""
        if self._llm_provider:
            # Use injected provider
            try:
                for chunk in self._llm_provider.generate_streaming(prompt, username, language):
                    yield chunk
                return
            except:
                pass  # Fall back to direct implementation
        
        # Direct Kobold implementation (fallback)
        try:
            messages = [{"role": "user", "content": prompt}]
            
            payload = {
                "model": "llama3",
                "messages": messages,
                "max_tokens": self.config['max_tokens'],
                "temperature": self.config['temperature'],
                "stream": True
            }
            
            response = requests.post(
                self.config['kobold_url'],
                json=payload,
                timeout=self.config['kobold_timeout'],
                stream=True
            )
            
            if response.status_code != 200:
                yield f"Error: API returned {response.status_code}"
                return
            
            buffer = ""
            chunk_count = 0
            
            for line in response.iter_lines(decode_unicode=True):
                if not line or not line.startswith("data: "):
                    continue
                
                try:
                    data = json.loads(line[6:])  # Remove "data: " prefix
                    
                    if 'choices' in data and len(data['choices']) > 0:
                        delta = data['choices'][0].get('delta', {})
                        content = delta.get('content', '')
                        
                        if content:
                            buffer += content
                            
                            # Yield when we have enough words or hit sentence boundaries
                            words = buffer.split()
                            if len(words) >= self.config['chunk_words'] or any(p in buffer for p in '.!?'):
                                yield buffer.strip()
                                buffer = ""
                                chunk_count += 1
                                
                                # Brief pause between chunks for natural flow
                                time.sleep(0.05)
                
                except json.JSONDecodeError:
                    continue
            
            # Yield any remaining content
            if buffer.strip():
                yield buffer.strip()
                
        except Exception as e:
            print(f"[ChatCore] ❌ Direct LLM error: {e}")
            yield "Sorry, I encountered an error."
    
    def _apply_entropy_to_chunk(self, chunk: str, emotional_context: Dict) -> str:
        """Apply consciousness entropy to response chunk"""
        try:
            if not CONSCIOUSNESS_AVAILABLE:
                return chunk
            
            # Apply textual entropy modifications
            enhanced_chunk = inject_consciousness_entropy("response", chunk)
            
            # Apply emotional modifiers
            if emotional_context and 'text_modifiers' in emotional_context:
                modifiers = emotional_context['text_modifiers']
                
                # Add hesitation markers occasionally
                if modifiers.get('hesitation_markers') and random.random() < 0.1:
                    hesitation = random.choice(modifiers['hesitation_markers'])
                    enhanced_chunk = f"{hesitation}, {enhanced_chunk}"
                
                # Modify punctuation for emotional tone
                if modifiers.get('emotional_punctuation') and random.random() < 0.2:
                    enhanced_chunk = enhanced_chunk.rstrip('.!?') + modifiers['emotional_punctuation']
            
            return enhanced_chunk
            
        except Exception as e:
            print(f"[ChatCore] ⚠️ Entropy application error: {e}")
            return chunk
    
    def generate_response_simple(self, question: str, username: str, language: str = "en") -> str:
        """Generate simple non-streaming response"""
        chunks = list(self.generate_response_streaming(question, username, language))
        return " ".join(chunks)


# Global chat core instance
_chat_core_instance = None

def get_chat_core() -> ChatCore:
    """Get the global chat core instance"""
    global _chat_core_instance
    if _chat_core_instance is None:
        _chat_core_instance = ChatCore()
    return _chat_core_instance