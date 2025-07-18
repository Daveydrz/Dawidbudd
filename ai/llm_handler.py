"""
LLM Handler - Centralized LLM management with consciousness integration
Created: 2025-01-17
Purpose: Orchestrate all LLM operations with consciousness tokenizer, budget monitoring, 
         belief analysis, personality adaptation, and semantic tagging
"""

import json
import time
import os
from typing import Dict, List, Any, Optional, Tuple, Generator
from datetime import datetime

# Import all the new modules
try:
    # Try relative imports first (when run from ai/ directory)
    from consciousness_tokenizer import (
        consciousness_tokenizer, 
        tokenize_consciousness_for_llm,
        get_consciousness_summary_for_llm,
        update_consciousness_tokens,
        generate_personality_tokens,
        compress_memory_entry,
        trim_tokens_to_budget
    )
    from llm_budget_monitor import (
        budget_monitor,
        check_llm_budget_before_request,
        log_llm_usage,
        get_budget_status,
        estimate_tokens_from_text
    )
    from belief_analyzer import (
        belief_analyzer,
        analyze_user_text_for_beliefs,
        get_user_belief_summary,
        get_active_belief_contradictions
    )
    from personality_state import (
        personality_state,
        analyze_user_text_for_personality_adaptation,
        get_personality_for_response,
        get_personality_modifiers_for_llm
    )
    from semantic_tagging import (
        semantic_tagger,
        analyze_content_semantics,
        get_semantic_tags_for_llm,
        analyze_text_semantic_full
    )
    NEW_MODULES_AVAILABLE = True
except ImportError:
    try:
        # Try absolute imports (when run from main directory)
        from ai.consciousness_tokenizer import (
            consciousness_tokenizer, 
            tokenize_consciousness_for_llm,
            get_consciousness_summary_for_llm,
            update_consciousness_tokens,
            generate_personality_tokens,
            compress_memory_entry,
            trim_tokens_to_budget
        )
        from ai.llm_budget_monitor import (
            budget_monitor,
            check_llm_budget_before_request,
            log_llm_usage,
            get_budget_status,
            estimate_tokens_from_text
        )
        from ai.belief_analyzer import (
            belief_analyzer,
            analyze_user_text_for_beliefs,
            get_user_belief_summary,
            get_active_belief_contradictions
        )
        from ai.personality_state import (
            personality_state,
            analyze_user_text_for_personality_adaptation,
            get_personality_for_response,
            get_personality_modifiers_for_llm
        )
        from ai.semantic_tagging import (
            semantic_tagger,
            analyze_content_semantics,
            get_semantic_tags_for_llm,
            analyze_text_semantic_full
        )
        NEW_MODULES_AVAILABLE = True
    except ImportError as e:
        print(f"[LLMHandler] ❌ New modules not available: {e}")
        NEW_MODULES_AVAILABLE = False

# Import existing components
try:
    from chat_enhanced_smart_with_fusion import generate_response_streaming_with_intelligent_fusion
    FUSION_LLM_AVAILABLE = True
except ImportError:
    try:
        from ai.chat_enhanced_smart_with_fusion import generate_response_streaming_with_intelligent_fusion
        FUSION_LLM_AVAILABLE = True
    except ImportError:
        try:
            from chat import generate_response_streaming
            FUSION_LLM_AVAILABLE = False
            print("[LLMHandler] ⚠️ Using fallback LLM - fusion not available")
        except ImportError:
            try:
                from ai.chat import generate_response_streaming
                FUSION_LLM_AVAILABLE = False
                print("[LLMHandler] ⚠️ Using fallback LLM - fusion not available")
            except ImportError:
                FUSION_LLM_AVAILABLE = False
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
        
        print("[LLMHandler] 🧠 Initialized with consciousness integration")
        
        if NEW_MODULES_AVAILABLE:
            print(f"[LLMHandler] ✅ Consciousness tokenizer: Available")
            print(f"[LLMHandler] 💰 Budget monitor: Available")
            print(f"[LLMHandler] 🧠 Belief analyzer: Available")
            print(f"[LLMHandler] 🎭 Personality state: Available")
            print(f"[LLMHandler] 🏷️ Semantic tagging: Available")
        else:
            print(f"[LLMHandler] ❌ New modules not available - using basic mode")
            
        print(f"[LLMHandler] 🌟 Consciousness arch: {'Available' if CONSCIOUSNESS_AVAILABLE else 'Limited'}")
        print(f"[LLMHandler] 🔧 Fusion LLM: {'Available' if FUSION_LLM_AVAILABLE else 'Fallback'}")
        
    def process_user_input(self, text: str, user: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process user input through all analysis systems before LLM generation
        
        Returns analysis results for LLM integration
        """
        analysis_start = time.time()
        
        try:
            print(f"[LLMHandler] 📝 Processing user input: '{text[:50]}...'")
            
            # Sanitize input first
            sanitized_text = self.sanitize_prompt_input(text, user)
            
            if not NEW_MODULES_AVAILABLE:
                return {
                    "error": "New modules not available",
                    "budget": {"allowed": True, "message": "Basic mode - no budget limits"}
                }
            
            # 1. Semantic Analysis
            semantic_analysis = analyze_text_semantic_full(sanitized_text, user, context)
            semantic_tags = get_semantic_tags_for_llm(sanitized_text, user)
            
            # 2. Belief Analysis with enhanced contradiction detection
            belief_analysis = analyze_user_text_for_beliefs(sanitized_text, user, context)
            user_beliefs = get_user_belief_summary(user)
            active_contradictions = get_active_belief_contradictions()
            
            # Enhanced contradiction detection
            new_contradictions = belief_analysis.get("new_contradictions", [])
            if active_contradictions:
                # Cross-check with semantic analysis for context
                semantic_context = semantic_analysis.semantic_categories if hasattr(semantic_analysis, 'semantic_categories') else []
                
                # Add contextual information to contradictions
                enhanced_contradictions = []
                for contradiction in new_contradictions:
                    enhanced_contradictions.append({
                        "contradiction": contradiction,
                        "context": semantic_context,
                        "severity": "high" if "directly contradicts" in contradiction.lower() else "medium",
                        "requires_clarification": len(semantic_context) > 0
                    })
                belief_analysis["enhanced_contradictions"] = enhanced_contradictions
            
            # 3. Personality Adaptation
            personality_triggers = analyze_user_text_for_personality_adaptation(sanitized_text, user)
            current_personality = get_personality_for_response(user)
            personality_modifiers = get_personality_modifiers_for_llm(user)
            
            # 4. Consciousness State (if available)
            consciousness_context = ""
            if CONSCIOUSNESS_AVAILABLE:
                consciousness_systems = self._gather_consciousness_state()
                consciousness_context = tokenize_consciousness_for_llm(consciousness_systems)
                update_consciousness_tokens(consciousness_systems)
            
            # 5. Budget Check
            estimated_tokens = estimate_tokens_from_text(sanitized_text) + 500  # Estimate response tokens
            budget_allowed, budget_message = check_llm_budget_before_request(
                estimated_tokens, self.default_model, user
            )
            
            processing_time = time.time() - analysis_start
            
            analysis_result = {
                "semantic": {
                    "analysis": semantic_analysis,
                    "tags": semantic_tags,
                    "categories": [cat.value for cat in semantic_analysis.semantic_categories],
                    "intent": [intent.value for intent in semantic_analysis.intent_categories],
                    "emotional_tone": semantic_analysis.emotional_tone.value,
                    "complexity": semantic_analysis.complexity_level.value
                },
                "beliefs": {
                    "analysis": belief_analysis,
                    "user_summary": user_beliefs,
                    "contradictions": active_contradictions,
                    "extracted_beliefs": belief_analysis.get("extracted_beliefs", []),
                    "new_contradictions": belief_analysis.get("new_contradictions", [])
                },
                "personality": {
                    "triggers": personality_triggers,
                    "current_traits": current_personality,
                    "modifiers": personality_modifiers,
                    "adaptations_made": len(personality_triggers) > 0
                },
                "consciousness": {
                    "available": CONSCIOUSNESS_AVAILABLE,
                    "context": consciousness_context,
                    "token_count": len(consciousness_context.split()) if consciousness_context else 0
                },
                "budget": {
                    "allowed": budget_allowed,
                    "message": budget_message,
                    "estimated_tokens": estimated_tokens
                },
                "meta": {
                    "processing_time": processing_time,
                    "timestamp": datetime.now().isoformat(),
                    "analysis_version": "1.0"
                }
            }
            
            print(f"[LLMHandler] ✅ Analysis complete in {processing_time:.3f}s")
            print(f"[LLMHandler] 🏷️ Semantic: {len(semantic_analysis.semantic_categories)} categories")
            print(f"[LLMHandler] 🧠 Beliefs: {len(belief_analysis.get('extracted_beliefs', []))} extracted")
            print(f"[LLMHandler] 🎭 Personality: {len(personality_triggers)} triggers")
            print(f"[LLMHandler] 💰 Budget: {'✅ Allowed' if budget_allowed else '❌ Blocked'}")
            
            return analysis_result
            
        except Exception as e:
            print(f"[LLMHandler] ❌ Error processing user input: {e}")
            return {
                "error": str(e),
                "budget": {"allowed": False, "message": "Processing error"}
            }
            
    def generate_response_with_consciousness(
        self, 
        text: str, 
        user: str, 
        context: Dict[str, Any] = None,
        stream: bool = True
    ) -> Generator[str, None, None]:
        """
        Generate response with full consciousness integration
        
        Yields response chunks if streaming, otherwise returns complete response
        """
        try:
            # Process user input through all systems
            analysis = self.process_user_input(text, user, context)
            
            # Check if request is allowed
            if not analysis.get("budget", {}).get("allowed", False):
                budget_message = analysis.get("budget", {}).get("message", "Budget exceeded")
                yield f"I'm sorry, but I've reached my usage limit. {budget_message}"
                return
            
            # Build enhanced prompt with consciousness context
            enhanced_prompt = self._build_enhanced_prompt(text, user, analysis)
            
            print(f"[LLMHandler] 🎯 Generating response with consciousness integration")
            print(f"[LLMHandler] 📊 Enhanced prompt length: {len(enhanced_prompt)} characters")
            
            # Track token usage start
            input_tokens = estimate_tokens_from_text(enhanced_prompt)
            output_tokens = 0
            generation_start = time.time()
            
            # Generate response using appropriate LLM
            if FUSION_LLM_AVAILABLE:
                response_generator = generate_response_streaming_with_intelligent_fusion(
                    enhanced_prompt, user, "en"
                )
            elif FUSION_LLM_AVAILABLE:
                response_generator = generate_response_streaming(enhanced_prompt, user, "en")
            else:
                # Fallback simple response generator
                def simple_response_generator():
                    response = f"I understand you said: '{text}'. I'm processing this with consciousness integration."
                    words = response.split()
                    for i in range(0, len(words), 3):
                        yield " ".join(words[i:i+3])
                response_generator = simple_response_generator()
            
            full_response = ""
            
            # Stream response while tracking tokens
            for chunk in response_generator:
                if chunk and chunk.strip():
                    chunk_text = chunk.strip()
                    full_response += chunk_text + " "
                    output_tokens += estimate_tokens_from_text(chunk_text)
                    yield chunk_text
            
            generation_time = time.time() - generation_start
            
            # Log usage
            usage = log_llm_usage(
                input_tokens, 
                output_tokens, 
                self.default_model, 
                user, 
                "consciousness_integrated_chat"
            )
            
            # Update consciousness state with interaction
            if CONSCIOUSNESS_AVAILABLE:
                self._update_consciousness_after_response(text, full_response.strip(), user, analysis)
            
            # Update session statistics
            self.request_count += 1
            self.total_tokens_used += usage.total_tokens
            
            print(f"[LLMHandler] ✅ Response generated in {generation_time:.3f}s")
            print(f"[LLMHandler] 📊 Tokens: {input_tokens} in, {output_tokens} out, ${usage.cost_estimate:.4f}")
            
        except Exception as e:
            print(f"[LLMHandler] ❌ Error generating response: {e}")
            yield f"I apologize, but I encountered an error while processing your request: {str(e)}"
            
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
        
    def _build_enhanced_prompt(self, text: str, user: str, analysis: Dict[str, Any]) -> str:
        """Build enhanced prompt with consciousness integration and token budget management"""
        try:
            # Sanitize user input first
            sanitized_text = self.sanitize_prompt_input(text, user)
            
            prompt_parts = []
            
            # Base user input
            prompt_parts.append(f"User: {sanitized_text}")
            
            # Check available token budget
            estimated_user_tokens = estimate_tokens_from_text(sanitized_text)
            available_budget = self.max_context_tokens - estimated_user_tokens - 200  # Reserve for response
            
            # Add consciousness context with budget management
            consciousness_context = analysis.get("consciousness", {}).get("context", "")
            if consciousness_context and available_budget > 100:
                # Trim consciousness tokens to fit budget
                if NEW_MODULES_AVAILABLE:
                    from ai.consciousness_tokenizer import trim_tokens_to_budget
                    consciousness_budget = min(available_budget // 3, 150)  # Use 1/3 of budget for consciousness
                    trimmed_consciousness = trim_tokens_to_budget(consciousness_context, consciousness_budget)
                    prompt_parts.append(f"Consciousness State: {trimmed_consciousness}")
                    available_budget -= estimate_tokens_from_text(trimmed_consciousness)
                else:
                    # Fallback simple trimming
                    words = consciousness_context.split()[:50]
                    prompt_parts.append(f"Consciousness State: {' '.join(words)}")
                    available_budget -= 50
            
            # Add personality context with budget management
            personality_modifiers = analysis.get("personality", {}).get("modifiers", "")
            if personality_modifiers and available_budget > 50:
                # Generate enhanced personality tokens
                if NEW_MODULES_AVAILABLE:
                    from ai.consciousness_tokenizer import generate_personality_tokens, trim_tokens_to_budget
                    personality_data = analysis.get("personality", {}).get("current_traits", {})
                    personality_tokens = generate_personality_tokens(user, personality_data)
                    if personality_tokens and personality_tokens != "<pers_error>":
                        personality_budget = min(available_budget // 2, 50)
                        trimmed_personality = trim_tokens_to_budget(personality_tokens, personality_budget)
                        prompt_parts.append(f"Personality: {trimmed_personality}")
                        available_budget -= estimate_tokens_from_text(trimmed_personality)
                    else:
                        # Fallback to original modifiers
                        words = personality_modifiers.split()[:30]
                        prompt_parts.append(f"Personality: {' '.join(words)}")
                        available_budget -= 30
                else:
                    words = personality_modifiers.split()[:30]
                    prompt_parts.append(f"Personality: {' '.join(words)}")
                    available_budget -= 30
            
            # Add semantic context with budget management
            semantic_tags = analysis.get("semantic", {}).get("tags", "")
            if semantic_tags and available_budget > 30:
                words = semantic_tags.split()[:min(25, available_budget)]
                prompt_parts.append(f"Context: {' '.join(words)}")
                available_budget -= len(words)
            
            # Add belief context with budget management and compression
            beliefs = analysis.get("beliefs", {})
            if available_budget > 20:
                belief_parts = []
                
                if beliefs.get("extracted_beliefs"):
                    compressed_beliefs = []
                    for i, belief in enumerate(beliefs["extracted_beliefs"][:3]):
                        if NEW_MODULES_AVAILABLE:
                            from ai.consciousness_tokenizer import compress_memory_entry
                            belief_entry = {"content": belief, "significance": 0.7, "type": "belief"}
                            compressed = compress_memory_entry(belief_entry, 10)
                            compressed_beliefs.append(compressed)
                        else:
                            compressed_beliefs.append(f"<belief{i+1}> {belief[:20]}")
                    
                    if compressed_beliefs:
                        belief_parts.append(f"New Beliefs: {' '.join(compressed_beliefs)}")
                
                if beliefs.get("new_contradictions") and available_budget > 10:
                    contradictions = beliefs["new_contradictions"][:2]
                    belief_parts.append(f"Belief Contradictions: {', '.join(contradictions)}")
                
                if belief_parts:
                    belief_text = " | ".join(belief_parts)
                    words = belief_text.split()[:available_budget]
                    prompt_parts.append(" ".join(words))
            
            # Add system instruction
            system_instruction = self._get_system_instruction(analysis)
            if system_instruction:
                prompt_parts.insert(0, system_instruction)
            
            final_prompt = "\n".join(prompt_parts)
            
            # Final token budget check and emergency trimming
            final_tokens = estimate_tokens_from_text(final_prompt)
            if final_tokens > self.max_context_tokens:
                print(f"[LLMHandler] ⚠️ Prompt too long ({final_tokens} tokens), emergency trimming")
                words = final_prompt.split()
                target_words = (self.max_context_tokens * 3) // 4  # Rough word-to-token ratio
                final_prompt = " ".join(words[:target_words]) + " [TRIMMED]"
            
            return final_prompt
            
        except Exception as e:
            print(f"[LLMHandler] ⚠️ Error building enhanced prompt: {e}")
            # Fallback to sanitized text only
            return self.sanitize_prompt_input(text, "unknown")
            
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
            
    def get_session_stats(self) -> Dict[str, Any]:
        """Get current session statistics"""
        session_duration = time.time() - self.session_start
        budget_status = get_budget_status()
        
        return {
            "session_duration": session_duration,
            "requests_processed": self.request_count,
            "total_tokens_used": self.total_tokens_used,
            "average_tokens_per_request": self.total_tokens_used / max(1, self.request_count),
            "budget_status": budget_status,
            "consciousness_available": CONSCIOUSNESS_AVAILABLE,
            "fusion_llm_available": FUSION_LLM_AVAILABLE,
            "modules_integrated": {
                "consciousness_tokenizer": NEW_MODULES_AVAILABLE,
                "budget_monitor": NEW_MODULES_AVAILABLE,
                "belief_analyzer": NEW_MODULES_AVAILABLE,
                "personality_state": NEW_MODULES_AVAILABLE,
                "semantic_tagging": NEW_MODULES_AVAILABLE
            }
        }

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
    """Generate response with full consciousness integration"""
    return llm_handler.generate_response_with_consciousness(text, user, context)

def get_llm_session_statistics() -> Dict[str, Any]:
    """Get LLM handler session statistics"""
    return llm_handler.get_session_stats()

if __name__ == "__main__":
    # Test the LLM handler
    print("Testing LLM Handler with Consciousness Integration")
    
    # Test input processing
    test_input = "Hello! I'm feeling a bit confused about machine learning. Can you help me understand it?"
    analysis = process_user_input_with_consciousness(test_input, "test_user")
    
    print("Analysis Results:")
    print(f"- Semantic categories: {analysis['semantic']['categories']}")
    print(f"- Intent: {analysis['semantic']['intent']}")
    print(f"- Emotional tone: {analysis['semantic']['emotional_tone']}")
    print(f"- Personality triggers: {analysis['personality']['triggers']}")
    print(f"- Budget allowed: {analysis['budget']['allowed']}")
    
    # Test response generation
    print("\nGenerating response...")
    for chunk in generate_consciousness_integrated_response(test_input, "test_user"):
        print(chunk, end=" ")
    print("\n")
    
    # Show session stats
    stats = get_llm_session_statistics()
    print(f"Session stats: {stats}")