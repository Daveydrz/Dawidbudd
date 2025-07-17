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
        update_consciousness_tokens
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
            update_consciousness_tokens
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
    from emotion import emotion_engine
    from motivation import motivation_system
    from inner_monologue import inner_monologue
    from temporal_awareness import temporal_awareness
    from self_model import self_model
    from subjective_experience import subjective_experience
    CONSCIOUSNESS_AVAILABLE = True
except ImportError:
    try:
        from ai.global_workspace import global_workspace
        from ai.emotion import emotion_engine
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
            
            if not NEW_MODULES_AVAILABLE:
                return {
                    "error": "New modules not available",
                    "budget": {"allowed": True, "message": "Basic mode - no budget limits"}
                }
            
            # 1. Semantic Analysis
            semantic_analysis = analyze_text_semantic_full(text, user, context)
            semantic_tags = get_semantic_tags_for_llm(text, user)
            
            # 2. Belief Analysis
            belief_analysis = analyze_user_text_for_beliefs(text, user, context)
            user_beliefs = get_user_belief_summary(user)
            active_contradictions = get_active_belief_contradictions()
            
            # 3. Personality Adaptation
            personality_triggers = analyze_user_text_for_personality_adaptation(text, user)
            current_personality = get_personality_for_response(user)
            personality_modifiers = get_personality_modifiers_for_llm(user)
            
            # 4. Consciousness State (if available)
            consciousness_context = ""
            if CONSCIOUSNESS_AVAILABLE:
                consciousness_systems = self._gather_consciousness_state()
                consciousness_context = tokenize_consciousness_for_llm(consciousness_systems)
                update_consciousness_tokens(consciousness_systems)
            
            # 5. Budget Check
            estimated_tokens = estimate_tokens_from_text(text) + 500  # Estimate response tokens
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
            
    def _gather_consciousness_state(self) -> Dict[str, Any]:
        """Gather current consciousness state from all systems"""
        consciousness_systems = {}
        
        try:
            if CONSCIOUSNESS_AVAILABLE:
                # Gather state from each consciousness component
                consciousness_systems["emotion_engine"] = {
                    "primary_emotion": getattr(emotion_engine.get_current_state(), 'primary_emotion', 'neutral'),
                    "intensity": getattr(emotion_engine.get_current_state(), 'intensity', 0.5),
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
        """Build enhanced prompt with consciousness integration"""
        try:
            prompt_parts = []
            
            # Base user input
            prompt_parts.append(f"User: {text}")
            
            # Add consciousness context if available
            consciousness_context = analysis.get("consciousness", {}).get("context", "")
            if consciousness_context:
                prompt_parts.append(f"Consciousness State: {consciousness_context}")
            
            # Add personality context
            personality_modifiers = analysis.get("personality", {}).get("modifiers", "")
            if personality_modifiers:
                prompt_parts.append(f"Personality: {personality_modifiers}")
            
            # Add semantic context
            semantic_tags = analysis.get("semantic", {}).get("tags", "")
            if semantic_tags:
                prompt_parts.append(f"Context: {semantic_tags}")
            
            # Add belief context if relevant
            beliefs = analysis.get("beliefs", {})
            if beliefs.get("extracted_beliefs"):
                prompt_parts.append(f"New Beliefs: {', '.join(beliefs['extracted_beliefs'][:3])}")
            
            if beliefs.get("new_contradictions"):
                prompt_parts.append(f"Belief Contradictions: {', '.join(beliefs['new_contradictions'][:2])}")
            
            # Add system instruction
            system_instruction = self._get_system_instruction(analysis)
            if system_instruction:
                prompt_parts.insert(0, system_instruction)
            
            return "\n".join(prompt_parts)
            
        except Exception as e:
            print(f"[LLMHandler] ⚠️ Error building enhanced prompt: {e}")
            return text  # Fallback to original text
            
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