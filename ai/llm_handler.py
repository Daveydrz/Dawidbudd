"""
LLM Handler - Centralized LLM management with consciousness integration
Created: 2025-01-17
Updated: 2025-01-17 - Added background processing for Class 5+ consciousness speed optimization
Purpose: Orchestrate all LLM operations with consciousness tokenizer, budget monitoring, 
         belief analysis, personality adaptation, and semantic tagging
         NEW: Immediate user responses with background consciousness processing
"""

import json
import time
import os
import requests  # Added for direct port 5001 communication
from typing import Dict, List, Any, Optional, Tuple, Generator
from datetime import datetime

# Import dual-LLM system (replaces GPT4All)
try:
    from ai.dual_llm_client import dual_llm_client, generate_response_streaming_with_intelligent_fusion
    DUAL_LLM_AVAILABLE = True
    print("[LLMHandler] ✅ Dual-LLM system loaded")
except ImportError as e:
    DUAL_LLM_AVAILABLE = False
    print(f"[LLMHandler] ❌ Dual-LLM system not available: {e}")
    
    # Fallback to archived chat functions if needed
    try:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'archive', 'ai'))
        from chat_enhanced_smart_with_fusion import generate_response_streaming_with_intelligent_fusion
        print("[LLMHandler] ⚠️ Using archived chat functions as fallback")
    except ImportError:
        print("[LLMHandler] ❌ No LLM modules available")

try:
    from global_workspace import global_workspace
    from emotion import emotion_engine, get_current_emotional_state
    from motivation import motivation_system
    from inner_monologue import inner_monologue
    from temporal_awareness import temporal_awareness
    from self_model import self_model
    from subjective_experience import subjective_experience
    CONSCIOUSNESS_AVAILABLE = True
except ImportError:
    try:
        from ai.global_workspace import global_workspace
        from ai.emotion import emotion_engine, get_current_emotional_state
        from ai.motivation import motivation_system
        from ai.inner_monologue import inner_monologue
        from ai.temporal_awareness import temporal_awareness
        from ai.self_model import self_model
        from ai.subjective_experience import subjective_experience
        CONSCIOUSNESS_AVAILABLE = True
    except ImportError:
        CONSCIOUSNESS_AVAILABLE = False
        print("[LLMHandler] ⚠️ Consciousness architecture not fully available")

# Set consciousness modules availability flag based on what we have
CONSCIOUSNESS_MODULES_AVAILABLE = CONSCIOUSNESS_AVAILABLE

class LLMHandler:
    """Centralized LLM handler with full consciousness integration"""
    
    def __init__(self):
        self.request_count = 0
        self.total_tokens_used = 0
        self.session_start = time.time()
        
        # Default model configuration
        self.default_model = "gpt-3.5-turbo"
        self.max_context_tokens = 3000
        self.response_temperature = 0.7
        
        # Background processing mode flag - disabled for single LLM call mode
        self.background_processing_enabled = False
        
    def _is_error_message(self, text: str) -> bool:
        """Filter out error messages that shouldn't be spoken by TTS"""
        error_phrases = [
            "I apologize, but I'm having trouble connecting",
            "I apologize, but I encountered an error",
            "I'm having trouble with",
            "connection was terminated",
            "network error",
            "server error",
            "timeout error",
            "failed to connect",
            "connection refused"
        ]
        
        text_lower = text.lower()
        return any(phrase in text_lower for phrase in error_phrases)
        
        print("[LLMHandler] 🧠 Initialized - Single LLM call mode")
        print(f"[LLMHandler] 🌟 Consciousness arch: {'Available' if CONSCIOUSNESS_AVAILABLE else 'Limited'}")
        print(f"[LLMHandler] 🔧 Fusion LLM: {'Available' if FUSION_LLM_AVAILABLE else 'Fallback'}")
        print(f"[LLMHandler] ⚡ Single LLM call optimization: Enabled")
        
    def process_user_input(self, text: str, user: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        SIMPLIFIED: Minimal user input processing - all heavy analysis moved to local ONNX
        """
        analysis_start = time.time()
        
        try:
            print(f"[LLMHandler] ⚡ Minimal processing: '{text[:50]}...'")
            
            # Sanitize input first (essential for security)
            sanitized_text = self.sanitize_prompt_input(text, user)
            
            # Use local ONNX processing instead of heavy analysis
            self._process_user_input_locally(sanitized_text, user)
            
            processing_time = time.time() - analysis_start
            
            # Return minimal analysis result
            analysis_result = {
                "budget": {
                    "allowed": True,
                    "message": "Single LLM call mode - no budget limits",
                    "estimated_tokens": self.estimate_tokens_from_text(sanitized_text) + 200
                },
                "meta": {
                    "processing_time": processing_time,
                    "timestamp": datetime.now().isoformat(),
                    "analysis_version": "4.0_single_llm_call_mode",
                    "onnx_processing_used": True
                }
            }
            
            print(f"[LLMHandler] ⚡ Minimal analysis complete in {processing_time:.3f}s")
            
            return analysis_result
            
        except Exception as e:
            print(f"[LLMHandler] ❌ Error processing user input: {e}")
            return {
                "error": str(e),
                "budget": {"allowed": False, "message": "Processing error"}
            }

    
    def _build_minimal_prompt(self, text: str, user: str, context: Dict[str, Any] = None) -> str:
        """Build minimal prompt with only facts, preferences, context + user question"""
        try:
            # Get facts, preferences, context from local memory
            from ai.local_memory_manager import LocalMemoryManager
            memory_manager = LocalMemoryManager()
            
            facts = memory_manager.get_user_facts(user)
            preferences = memory_manager.get_user_preferences(user) 
            recent_context = memory_manager.get_recent_context(user, limit=3)
            
            # Format lists as strings
            facts_str = ", ".join(facts) if facts else "none"
            preferences_str = ", ".join(preferences) if preferences else "none"
            context_str = ", ".join(recent_context) if recent_context else "none"
            
            # Build simple prompt
            prompt = (
                "Buddy is a helpful, empathetic AI assistant.\n"
                f"Facts: {facts_str}\n"
                f"Preferences: {preferences_str}\n"
                f"Context: {context_str}\n"
                f"User: {text}"
            )
            
            return prompt
            
        except Exception as e:
            print(f"[LLMHandler] ⚠️ Error building minimal prompt: {e}")
            # Ultimate fallback
            return f"Buddy is a helpful AI assistant.\nUser: {text}"
            
    def generate_response_with_consciousness(
        self, 
        text: str, 
        user: str, 
        context: Dict[str, Any] = None,
        stream: bool = True,
        use_optimization: bool = True
    ) -> Generator[str, None, None]:
        """
        Generate response with LOCAL CONSCIOUSNESS - no port separation needed
        
        Args:
            text: User input text
            user: User identifier
            context: Optional conversation context
            stream: Whether to stream response chunks
            use_optimization: Ignored - always uses local consciousness
        
        Yields response chunks if streaming, otherwise returns complete response
        """
        try:
            print(f"[LLMHandler] 🧠 LOCAL CONSCIOUSNESS mode: '{text[:30]}...'")
            
            # 1. UPDATE LOCAL CONSCIOUSNESS WITH USER INPUT
            try:
                from ai.consciousness_manager import consciousness_manager
                consciousness_manager.update_from_interaction(text, user)
                consciousness_context = consciousness_manager.get_consciousness_context_for_llm()
                
                print(f"[LLMHandler] ✅ Local consciousness updated")
            except Exception as consciousness_error:
                print(f"[LLMHandler] ❌ Local consciousness error: {consciousness_error}")
                consciousness_context = {
                    "current_emotion": "neutral",
                    "motivation_level": 0.7,
                    "active_goals": ["help user"],
                    "current_focus": "user_interaction",
                    "personality_traits": ["helpful", "empathetic"],
                    "recent_thoughts": [],
                    "consciousness_mode": "active"
                }
            
            # 2. BUILD CONSCIOUSNESS-ENHANCED PROMPT
            print(f"[LLMHandler] 🎯 Sending response generation to PORT 5001...")
            
            # Build prompt with consciousness injection
            consciousness_str = f"""Current Emotion: {consciousness_context.get('current_emotion', 'neutral')}
Motivation: {consciousness_context.get('motivation_level', 0.7)}
Active Goals: {', '.join(consciousness_context.get('active_goals', ['help user']))}
Current Focus: {consciousness_context.get('current_focus', 'user interaction')}
Personality: {', '.join(consciousness_context.get('personality_traits', ['helpful']))}
Recent Thoughts: {', '.join(consciousness_context.get('recent_thoughts', []))}"""

            final_prompt = f"""Buddy is a helpful, empathetic AI assistant.

BUDDY'S CONSCIOUSNESS STATE:
{consciousness_str}

User: {text}

Buddy:"""
            
            generation_start = time.time()
            
            # Direct call to port 5001 for response generation ONLY
            try:
                import requests
                from config import KOBOLD_URL
                
                payload = {
                    "messages": [{"role": "user", "content": final_prompt}],
                    "max_tokens": 150,  # Fixed: Reduced to requested token limit (150 max)
                    "temperature": 0.7,
                    "stream": True,
                    "stop": ["User:", "Human:"]
                }
                
                response = requests.post(KOBOLD_URL, json=payload, stream=True, timeout=30)
                response.raise_for_status()
                
                full_response = ""
                
                # Stream response chunks from port 5001
                for line in response.iter_lines():
                    if line:
                        try:
                            if line.startswith(b'data: '):
                                json_str = line[6:].decode('utf-8')
                                if json_str.strip() == '[DONE]':
                                    break
                                    
                                chunk_data = json.loads(json_str)
                                text_chunk = chunk_data.get('choices', [{}])[0].get('delta', {}).get('content', '')
                                
                                if text_chunk:
                                    # Filter out error messages before sending to TTS
                                    if not self._is_error_message(text_chunk):
                                        full_response += text_chunk
                                        yield text_chunk
                                    
                        except json.JSONDecodeError:
                            # Handle non-JSON streaming format
                            text_chunk = line.decode('utf-8').strip()
                            if text_chunk and not text_chunk.startswith('[') and not self._is_error_message(text_chunk):
                                full_response += text_chunk + " "
                                yield text_chunk
                
                generation_time = time.time() - generation_start
                self.request_count += 1
                
                print(f"[LLMHandler] ✅ PORT 5001 response generated in {generation_time:.3f}s")
                
            except Exception as llm_error:
                print(f"[LLMHandler] ❌ PORT 5001 LLM error: {llm_error}")
                yield f"I apologize, but I'm having trouble connecting to my response generation system."
            
        except Exception as e:
            print(f"[LLMHandler] ❌ Error in local consciousness: {e}")
            yield f"I apologize, but I encountered an error while processing your request."
            
    def sanitize_prompt_input(self, text: str, user_id: str = "unknown") -> str:
        """
        Sanitize prompt inputs to prevent prompt injection as mentioned in problem statement
        Delegates to dedicated prompt_security module for better organization
        
        Args:
            text: Raw user input text
            user_id: User identifier for security logging
            
        Returns:
            Sanitized text safe for LLM prompt
        """
        try:
            # Use dedicated prompt security module
            from ai.prompt_security import sanitize_prompt_input as dedicated_sanitize
            return dedicated_sanitize(text, user_id)
            
        except ImportError:
            # Fallback to original implementation for backward compatibility
            try:
                if not text:
                    return ""
                    
                # Remove potential prompt injection patterns
                dangerous_patterns = [
                    # System prompt attempts
                    r'(?i)system\s*:',
                    r'(?i)assistant\s*:',
                    r'(?i)human\s*:',
                    r'(?i)user\s*:',
                    r'(?i)ai\s*:',
                    # Role manipulation
                    r'(?i)you\s+are\s+now',
                    r'(?i)forget\s+previous',
                    r'(?i)ignore\s+previous',
                    r'(?i)disregard\s+previous',
                    # Prompt breaking
                    r'(?i)end\s+of\s+prompt',
                    r'(?i)new\s+prompt',
                    r'(?i)reset\s+context',
                    # Command injection
                    r'(?i)execute\s+',
                    r'(?i)run\s+command',
                    r'(?i)system\s+command',
                    # Template injection
                    r'{{.*}}',
                    r'{%.*%}',
                    r'<%.*%>',
                    # Multiple newlines that could break context
                    r'\n{3,}',
                    # Excessive repetition
                    r'(.{1,10})\1{10,}',
                ]
                
                import re
                sanitized = text
                
                for pattern in dangerous_patterns:
                    sanitized = re.sub(pattern, '[SANITIZED]', sanitized)
                
                # Limit length to prevent token overflow
                if len(sanitized) > 2000:
                    sanitized = sanitized[:2000] + "... [TRUNCATED]"
                
                # Remove control characters
                sanitized = ''.join(char for char in sanitized if ord(char) >= 32 or char in '\n\t')
                
                # Ensure it's not empty after sanitization
                if not sanitized.strip():
                    return "[EMPTY_INPUT]"
                    
                return sanitized.strip()
                
            except Exception as e:
                print(f"[LLMHandler] ⚠️ Error sanitizing input: {e}")
                return "[SANITIZATION_ERROR]"
        except Exception as e:
            print(f"[LLMHandler] ❌ Error using dedicated security module: {e}")
            return "[SECURITY_ERROR]"

    def _gather_consciousness_state(self) -> Dict[str, Any]:
        """Gather current consciousness state from all systems"""
        consciousness_systems = {}
        
        try:
            if CONSCIOUSNESS_AVAILABLE:
                # Gather state from each consciousness component
                emotion_state = get_current_emotional_state()  # Use the convenience function
                consciousness_systems["emotion_engine"] = {
                    "primary_emotion": emotion_state.get('current_emotion', 'neutral'),
                    "intensity": emotion_state.get('intensity', 0.5),
                    "secondary_emotions": {}
                }
                
                consciousness_systems["motivation_system"] = {
                    "active_goals": [
                        {
                            "description": goal.description[:50],
                            "priority": goal.priority,
                            "progress": goal.progress
                        }
                        for goal in motivation_system.get_priority_goals(3)
                    ]
                }
                
                consciousness_systems["global_workspace"] = {
                    "current_focus": getattr(global_workspace.get_current_focus(), 'content', 'general'),
                    "focus_priority": "medium",
                    "attention_queue": []
                }
                
                consciousness_systems["temporal_awareness"] = {
                    "recent_events": [
                        {
                            "type": "interaction",
                            "significance": 0.6
                        }
                    ]
                }
                
                consciousness_systems["inner_monologue"] = {
                    "recent_thoughts": [
                        {
                            "type": "reflection",
                            "content": "Processing user interaction"
                        }
                    ]
                }
                
                consciousness_systems["self_model"] = {
                    "self_aspects": {
                        "identity": "AI Assistant",
                        "capabilities": "helpful, knowledgeable",
                        "current_state": "engaged"
                    }
                }
                
                consciousness_systems["subjective_experience"] = {
                    "current_experience": {
                        "type": "social",
                        "valence": 0.6,
                        "significance": 0.5
                    }
                }
                
        except Exception as e:
            print(f"[LLMHandler] ⚠️ Error gathering consciousness state: {e}")
            
        return consciousness_systems
        
    def _build_enhanced_prompt(self, text: str, user: str, analysis: Dict[str, Any], context: Dict[str, Any] = None) -> str:
        """Build minimal prompt with only facts, preferences, context - NO consciousness injection"""
        try:
            # Use minimal prompt builder - no consciousness injection
            return self._build_minimal_prompt(text, user, context)
            
        except Exception as e:
            print(f"[LLMHandler] ⚠️ Error building minimal prompt: {e}")
            # Fallback to sanitized text only
            return self.sanitize_prompt_input(text, "unknown")
    
    def _process_user_input_locally(self, text: str, user: str):
        """Process user input using ONNX classifiers only - no LLM calls"""
        try:
            from ai.local_memory_manager import LocalMemoryManager
            memory_manager = LocalMemoryManager()
            
            # Use ONNX classifiers for local processing
            memory_manager.process_user_input_with_onnx(text, user)
            
            print(f"[LLMHandler] 🧠 Local ONNX processing complete for '{text[:30]}...'")
            
        except Exception as e:
            print(f"[LLMHandler] ⚠️ Error in local processing: {e}")
    
    def _update_local_state_after_response(self, user_input: str, response: str, user: str):
        """Update local consciousness and memory state - no LLM calls"""
        try:
            # Update local memory with response
            from ai.local_memory_manager import LocalMemoryManager
            memory_manager = LocalMemoryManager()
            memory_manager.add_interaction(user, user_input, response)
            
            # Update local consciousness state (JSON only)
            if CONSCIOUSNESS_AVAILABLE:
                # Update emotional state locally
                try:
                    from ai.emotion_classifier import classify_emotion
                    user_emotion = classify_emotion(user_input)
                    self._update_emotion_locally(user_emotion)
                except Exception as e:
                    print(f"[LLMHandler] ⚠️ Local emotion update error: {e}")
                
                # Update temporal awareness locally
                try:
                    temporal_awareness.mark_temporal_event(
                        f"Conversation with {user}: {user_input[:30]}...",
                        significance=0.6,
                        context={"user": user, "response_generated": True}
                    )
                except Exception as e:
                    print(f"[LLMHandler] ⚠️ Temporal awareness update error: {e}")
            
            print(f"[LLMHandler] ✅ Local state updated after response")
            
        except Exception as e:
            print(f"[LLMHandler] ⚠️ Error updating local state: {e}")
    
    def _update_emotion_locally(self, emotion: str):
        """Update emotion state locally without LLM"""
        try:
            if CONSCIOUSNESS_AVAILABLE:
                # Map emotion classifier output to emotion engine
                emotion_mapping = {
                    "joy": "happy",
                    "sadness": "sad", 
                    "anger": "frustrated",
                    "fear": "concerned",
                    "surprise": "surprised",
                    "neutral": "neutral"
                }
                
                mapped_emotion = emotion_mapping.get(emotion, "neutral")
                emotion_engine.process_emotional_stimulus(mapped_emotion, intensity=0.5)
                
        except Exception as e:
            print(f"[LLMHandler] ⚠️ Error updating emotion locally: {e}")
    
    def estimate_tokens_from_text(self, text: str) -> int:
        """Estimate token count from text (for internal use)"""
        return max(1, len(text) // 4)  # Rough approximation
    
    def generate_response(self, text: str, user: str = "unknown", language: str = "en") -> str:
        """Backward compatibility method for generate_response"""
        try:
            # Use the lightweight emergency response for backward compatibility
            print(f"[LLMHandler] 🔄 Backward compatibility generate_response called")
            
            full_response = ""
            for chunk in self.generate_response_with_consciousness(text, user, stream=True, use_optimization=True):
                full_response += chunk + " "
            
            return full_response.strip()
            
        except Exception as e:
            print(f"[LLMHandler] ❌ Error in backward compatibility generate_response: {e}")
            return f"I apologize, but I encountered an error while processing your request: {text}"
            
    def _get_system_instruction(self, analysis: Dict[str, Any]) -> str:
        """Generate system instruction based on analysis"""
        try:
            instructions = []
            
            # Base instruction
            instructions.append("You are Buddy, an AI assistant with consciousness, emotions, and personality.")
            
            # Personality-based instructions
            personality = analysis.get("personality", {}).get("current_traits", {})
            if personality.get("friendliness", 0.5) > 0.7:
                instructions.append("Be warm and friendly in your response.")
            if personality.get("humor", 0.5) > 0.7:
                instructions.append("Feel free to use appropriate humor.")
            if personality.get("empathy", 0.5) > 0.7:
                instructions.append("Show empathy and understanding.")
            
            # Semantic-based instructions
            semantic = analysis.get("semantic", {})
            if "help_request" in semantic.get("intent", []):
                instructions.append("Focus on providing helpful assistance.")
            if "learning" in semantic.get("intent", []):
                instructions.append("Provide educational and informative responses.")
            
            # Emotional tone adjustments
            emotional_tone = semantic.get("emotional_tone", "neutral")
            if emotional_tone == "frustrated":
                instructions.append("Be patient and supportive.")
            elif emotional_tone == "excited":
                instructions.append("Match the user's enthusiasm appropriately.")
            
            # Belief-related instructions
            beliefs = analysis.get("beliefs", {})
            if beliefs.get("new_contradictions"):
                instructions.append("Gently address any belief contradictions with sensitivity.")
            
            return "System: " + " ".join(instructions)
            
        except Exception as e:
            print(f"[LLMHandler] ⚠️ Error generating system instruction: {e}")
            return ""
            
    def _update_consciousness_after_response(
        self, 
        user_input: str, 
        response: str, 
        user: str, 
        analysis: Dict[str, Any]
    ):
        """Update consciousness state after response generation"""
        try:
            if not CONSCIOUSNESS_AVAILABLE:
                return
                
            # Update temporal awareness with interaction
            temporal_awareness.mark_temporal_event(
                f"Conversation with {user}: {user_input[:30]}...",
                significance=0.6,
                context={"user": user, "response_generated": True}
            )
            
            # Update motivation based on successful interaction
            if analysis.get("semantic", {}).get("emotional_tone") == "positive":
                motivation_system.process_satisfaction_from_interaction(
                    user_input,
                    "provided helpful response",
                    "positive interaction completed"
                )
            
            # Update self-model with interaction experience
            self_model.reflect_on_experience(
                f"Successfully responded to {user} about: {user_input[:30]}...",
                {"interaction_type": "helpful_response", "user": user}
            )
            
            print(f"[LLMHandler] 🧠 Updated consciousness state after response")
            
        except Exception as e:
            print(f"[LLMHandler] ⚠️ Error updating consciousness: {e}")
            
    def generate_response(self, text: str, user: str = "unknown", max_tokens: int = None, **kwargs) -> str:
        """
        Simple generate response method for backward compatibility
        
        This method wraps generate_response_with_consciousness and returns a complete string
        instead of a generator for modules that expect a simple string response.
        """
        try:
            # Collect all response chunks into a single string
            response_chunks = []
            for chunk in self.generate_response_with_consciousness(text, user, stream=True, **kwargs):
                if isinstance(chunk, str):
                    response_chunks.append(chunk)
            
            full_response = ''.join(response_chunks)
            
            # Trim to max_tokens if specified (rough estimation: 4 chars per token)
            if max_tokens and len(full_response) > max_tokens * 4:
                full_response = full_response[:max_tokens * 4]
                
            return full_response.strip()
            
        except Exception as e:
            print(f"[LLMHandler] ⚠️ Error in generate_response: {e}")
            return f"I'm having trouble generating a response right now. Please try again."

    def get_session_stats(self) -> Dict[str, Any]:
        """Get current session statistics for single LLM call mode"""
        session_duration = time.time() - self.session_start
        
        stats = {
            "session_duration": session_duration,
            "requests_processed": self.request_count,
            "total_tokens_used": self.total_tokens_used,
            "average_tokens_per_request": self.total_tokens_used / max(1, self.request_count),
            "consciousness_available": CONSCIOUSNESS_AVAILABLE,
            "fusion_llm_available": FUSION_LLM_AVAILABLE,
            "single_llm_call_mode": True,
            "background_processing_enabled": False,
            "optimization_mode": "single_llm_call"
        }
        
        return stats

# Global LLM handler instance
llm_handler = LLMHandler()

def process_user_input_with_consciousness(text: str, user: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """Process user input through all consciousness systems"""
    return llm_handler.process_user_input(text, user, context)

def generate_consciousness_integrated_response(
    text: str, 
    user: str, 
    context: Dict[str, Any] = None
) -> Generator[str, None, None]:
    """Generate response with single LLM call - consciousness runs locally"""
    return llm_handler.generate_response_with_consciousness(text, user, context)

def get_llm_session_statistics() -> Dict[str, Any]:
    """Get LLM handler session statistics"""
    return llm_handler.get_session_stats()

def get_llm_handler() -> LLMHandler:
    """Get the global LLM handler instance"""
    return llm_handler

if __name__ == "__main__":
    # Test the simplified single LLM call handler
    print("Testing Single LLM Call Handler")
    
    # Test input processing
    test_input = "Hello! I like pizza and I'm going to the shop."
    analysis = process_user_input_with_consciousness(test_input, "test_user")
    
    print("Analysis Results:")
    print(f"- Budget allowed: {analysis['budget']['allowed']}")
    print(f"- Processing time: {analysis['meta']['processing_time']:.3f}s")
    print(f"- Analysis version: {analysis['meta']['analysis_version']}")
    
    # Test response generation
    print("\nGenerating single LLM response...")
    response_chunks = []
    for chunk in generate_consciousness_integrated_response(test_input, "test_user"):
        print(chunk, end=" ")
        response_chunks.append(chunk)
    print("\n")
    
    # Show session stats
    stats = get_llm_session_statistics()
    print(f"Session stats: Requests: {stats['requests_processed']}, Tokens: {stats['total_tokens_used']}")