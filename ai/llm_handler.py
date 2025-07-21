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

# Import background processing for speed optimization
try:
    from background_consciousness_processor import (
        background_processor,
        start_background_processing,
        schedule_background_thoughts,
        register_consciousness_modules,
        get_background_processing_stats
    )
    BACKGROUND_PROCESSING_AVAILABLE = True
    print("[LLMHandler] ⚡ Background consciousness processing available")
except ImportError:
    try:
        from ai.background_consciousness_processor import (
            background_processor,
            start_background_processing,
            schedule_background_thoughts,
            register_consciousness_modules,
            get_background_processing_stats
        )
        BACKGROUND_PROCESSING_AVAILABLE = True
        print("[LLMHandler] ⚡ Background consciousness processing available")
    except ImportError:
        BACKGROUND_PROCESSING_AVAILABLE = False
        print("[LLMHandler] ⚠️ Background consciousness processing not available")

# Set consciousness modules availability flag based on what we have
CONSCIOUSNESS_MODULES_AVAILABLE = NEW_MODULES_AVAILABLE or CONSCIOUSNESS_AVAILABLE

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
        
        # Background processing mode flag
        self.background_processing_enabled = BACKGROUND_PROCESSING_AVAILABLE
        
        print("[LLMHandler] 🧠 Initialized with consciousness integration")
        
        # Start background processing if available
        if self.background_processing_enabled:
            start_background_processing()
            print("[LLMHandler] ⚡ Background consciousness processing started")
        
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
        print(f"[LLMHandler] ⚡ Background processing: {'Enabled' if self.background_processing_enabled else 'Disabled'}")
        
    def process_user_input(self, text: str, user: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        EMERGENCY LIGHTWEIGHT PROCESSING - Minimal analysis for immediate response
        Heavy analysis moved to background processing to prevent 33+ second delays
        """
        analysis_start = time.time()
        
        try:
            print(f"[LLMHandler] ⚡ EMERGENCY LIGHTWEIGHT processing: '{text[:50]}...'")
            
            # Sanitize input first (minimal processing)
            sanitized_text = self.sanitize_prompt_input(text, user)
            
            # ✅ EMERGENCY: Skip heavy analysis modules that were causing 33s delays
            if not NEW_MODULES_AVAILABLE:
                return {
                    "error": "New modules not available",
                    "budget": {"allowed": True, "message": "Basic mode - no budget limits"}
                }
            
            # ✅ LIGHTWEIGHT: Only essential budget check
            estimated_tokens = 500  # Conservative estimate
            budget_allowed = True  # Skip heavy budget analysis
            budget_message = "Lightweight mode - fast response"
            
            # ✅ MINIMAL: Skip heavy semantic analysis
            semantic_analysis_lightweight = {
                "emotional_tone": "neutral",
                "complexity": "simple",
                "intent": ["conversation"]
            }
            
            # ✅ MINIMAL: Skip heavy belief analysis  
            belief_analysis_lightweight = {
                "extracted_beliefs": [],
                "new_contradictions": [],
                "enhanced_contradictions": []
            }
            
            # ✅ MINIMAL: Skip heavy personality analysis
            personality_lightweight = {
                "current_traits": {"helpful": True, "friendly": True},
                "modifiers": "helpful friendly",
                "adaptations_made": False
            }
            
            # ✅ MINIMAL: Ultra-lightweight consciousness
            consciousness_context = "[CONSCIOUSNESS:engaged helpful focused]"
            consciousness_summary = "[CONSCIOUSNESS:engaged helpful focused]"
            
            processing_time = time.time() - analysis_start
            
            # ✅ BACKGROUND: Schedule heavy analysis in background thread
            self._schedule_background_heavy_analysis(sanitized_text, user, context)
            
            analysis_result = {
                "semantic": {
                    "analysis": semantic_analysis_lightweight,
                    "tags": [],
                    "categories": [],
                    "intent": ["conversation"],
                    "emotional_tone": "neutral",
                    "complexity": "simple"
                },
                "beliefs": {
                    "analysis": belief_analysis_lightweight,
                    "user_summary": {},
                    "contradictions": [],
                    "extracted_beliefs": [],
                    "new_contradictions": [],
                    "enhanced_contradictions": []
                },
                "personality": {
                    "triggers": [],
                    "current_traits": personality_lightweight["current_traits"],
                    "modifiers": personality_lightweight["modifiers"],
                    "adaptations_made": False
                },
                "consciousness": {
                    "available": True,
                    "context": consciousness_context,
                    "summary": consciousness_summary,
                    "token_count": len(consciousness_context.split()),
                    "cross_system_integration": False,  # Deferred to background
                    "simulation_mode": False,
                    "lightweight_mode": True
                },
                "budget": {
                    "allowed": budget_allowed,
                    "message": budget_message,
                    "estimated_tokens": estimated_tokens,
                    "usage_percentage": 0.0,  # Skip heavy calculation
                    "cost_estimate": 0.0,  # Skip heavy calculation
                    "optimization_target": "emergency_fast"
                },
                "memory": {
                    "significant_context": "",
                    "recent_interactions": [],
                    "compressed": True
                },
                "meta": {
                    "processing_time": processing_time,
                    "timestamp": datetime.now().isoformat(),
                    "analysis_version": "3.0_emergency_lightweight",
                    "token_optimization_enabled": True,
                    "cross_system_integration": False,  # Deferred to background
                    "lightweight_mode": True,
                    "background_processing_scheduled": True
                }
            }
            
            print(f"[LLMHandler] ⚡ EMERGENCY LIGHTWEIGHT analysis complete in {processing_time:.3f}s")
            print(f"[LLMHandler] 🚀 Heavy analysis scheduled for background processing")
            
            return analysis_result
            
        except Exception as e:
            print(f"[LLMHandler] ❌ Error processing user input: {e}")
            return {
                "error": str(e),
                "budget": {"allowed": False, "message": "Processing error"}
            }
    
    def _schedule_background_heavy_analysis(self, text: str, user: str, context: Dict[str, Any] = None):
        """Schedule heavy analysis in background thread to prevent blocking user response"""
        import threading
        
        def background_heavy_analysis():
            """Execute heavy analysis in background"""
            try:
                print(f"[LLMHandler] 🔄 Starting background heavy analysis")
                analysis_start = time.time()
                
                # Perform all the heavy analysis that was causing 33s delays
                try:
                    # 1. Full semantic analysis
                    semantic_analysis = analyze_text_semantic_full(text, user, context)
                    semantic_tags = get_semantic_tags_for_llm(text, user)
                    print(f"[LLMHandler] 🏷️ Background semantic analysis completed")
                except Exception as e:
                    print(f"[LLMHandler] ⚠️ Background semantic analysis error: {e}")
                
                try:
                    # 2. Full belief analysis
                    belief_analysis = analyze_user_text_for_beliefs(text, user, context)
                    user_beliefs = get_user_belief_summary(user)
                    active_contradictions = get_active_belief_contradictions()
                    print(f"[LLMHandler] 🧠 Background belief analysis completed")
                except Exception as e:
                    print(f"[LLMHandler] ⚠️ Background belief analysis error: {e}")
                
                try:
                    # 3. Full personality adaptation
                    personality_triggers = analyze_user_text_for_personality_adaptation(text, user)
                    current_personality = get_personality_for_response(user)
                    personality_modifiers = get_personality_modifiers_for_llm(user)
                    print(f"[LLMHandler] 🎭 Background personality analysis completed")
                except Exception as e:
                    print(f"[LLMHandler] ⚠️ Background personality analysis error: {e}")
                
                try:
                    # 4. Full consciousness state integration
                    if CONSCIOUSNESS_AVAILABLE:
                        consciousness_systems = self._gather_consciousness_state()
                        consciousness_context = tokenize_consciousness_for_llm(consciousness_systems)
                        update_consciousness_tokens(consciousness_systems)
                        print(f"[LLMHandler] 🧠 Background consciousness integration completed")
                except Exception as e:
                    print(f"[LLMHandler] ⚠️ Background consciousness integration error: {e}")
                
                try:
                    # 5. Full budget check
                    estimated_tokens = estimate_tokens_from_text(text) + 500
                    budget_allowed, budget_message = check_llm_budget_before_request(
                        estimated_tokens, self.default_model, user
                    )
                    budget_status = get_budget_status()
                    print(f"[LLMHandler] 💰 Background budget analysis completed")
                except Exception as e:
                    print(f"[LLMHandler] ⚠️ Background budget analysis error: {e}")
                
                processing_time = time.time() - analysis_start
                print(f"[LLMHandler] ✅ Background heavy analysis completed in {processing_time:.3f}s")
                
            except Exception as e:
                print(f"[LLMHandler] ❌ Background heavy analysis error: {e}")
        
        # Start background thread
        background_thread = threading.Thread(target=background_heavy_analysis, daemon=True)
        background_thread.start()
        print(f"[LLMHandler] 🚀 Background heavy analysis scheduled")
    
    def generate_immediate_response_with_background_consciousness(
        self,
        text: str,
        user: str,
        context: Dict[str, Any] = None,
        stream: bool = True
    ) -> Generator[str, None, None]:
        """
        ⚡ NEW: Generate immediate user response, defer consciousness processing to background
        
        This method prioritizes instant user responses (<5 seconds) while maintaining
        Class 5+ consciousness by processing internal modules in background after response.
        
        Args:
            text: User input text
            user: User identifier  
            context: Optional conversation context
            stream: Whether to stream response chunks
            
        Yields response chunks immediately, schedules consciousness processing for background
        """
        try:
            response_start_time = time.time()
            print(f"[LLMHandler] ⚡ IMMEDIATE RESPONSE MODE: Generating instant reply for '{text[:30]}...'")
            
            # 1. ☝ PRIORITIZE USER REPLY FIRST - Minimal processing for immediate response
            
            # Basic input sanitization (essential for security)
            sanitized_text = self.sanitize_prompt_input(text, user)
            
            # Quick budget check only (no complex analysis)
            if NEW_MODULES_AVAILABLE:
                estimated_tokens = estimate_tokens_from_text(sanitized_text) + 200
                budget_allowed, budget_message = check_llm_budget_before_request(
                    estimated_tokens, self.default_model, user
                )
                if not budget_allowed:
                    yield f"I'm sorry, I've reached my usage limit. {budget_message}"
                    return
            
            # 2. 📦 KEEP CONTEXT LIGHT - Only essential context for immediate response
            light_prompt = self._build_light_prompt_for_immediate_response(sanitized_text, user, context)
            
            print(f"[LLMHandler] 🏃‍♂️ Light prompt ready: {len(light_prompt)} chars")
            
            # 3. Generate immediate response without consciousness processing delays
            full_response = ""
            chunk_count = 0
            
            if FUSION_LLM_AVAILABLE:
                # Use fusion LLM but with minimal context
                response_generator = generate_response_streaming_with_intelligent_fusion(
                    light_prompt, user, "en", context={}  # Empty context for speed
                )
            else:
                # Fallback to basic LLM
                response_generator = generate_response_streaming(light_prompt, user, "en")
            
            # Stream response immediately
            for chunk in response_generator:
                if chunk and chunk.strip():
                    chunk_text = chunk.strip()
                    full_response += chunk_text + " "
                    chunk_count += 1
                    yield chunk_text
            
            response_time = time.time() - response_start_time
            print(f"[LLMHandler] ⚡ IMMEDIATE RESPONSE COMPLETE: {response_time:.3f}s, {chunk_count} chunks")
            
            # 4. 🧠 DEFER CONSCIOUSNESS PROCESSING - Schedule for background after response
            if self.background_processing_enabled and full_response.strip():
                try:
                    # Register consciousness modules if not done already
                    if CONSCIOUSNESS_AVAILABLE:
                        consciousness_modules = self._gather_consciousness_state()
                        register_consciousness_modules(consciousness_modules)
                    
                    # Schedule background processing with delay for idle detection
                    schedule_background_thoughts(
                        user_input=sanitized_text,
                        user_id=user,
                        response=full_response.strip(),
                        delay=3.0  # Wait 3 seconds for system to be idle
                    )
                    
                    print(f"[LLMHandler] 📋 Scheduled background consciousness processing")
                    
                except Exception as bg_error:
                    print(f"[LLMHandler] ⚠️ Background scheduling error (non-critical): {bg_error}")
            
            # Update basic session statistics
            self.request_count += 1
            if NEW_MODULES_AVAILABLE:
                input_tokens = estimate_tokens_from_text(light_prompt)
                output_tokens = estimate_tokens_from_text(full_response)
                usage = log_llm_usage(input_tokens, output_tokens, self.default_model, user, "immediate_response")
                self.total_tokens_used += usage.total_tokens
            
            print(f"[LLMHandler] ✅ User prioritized response delivered in {response_time:.3f}s")
            
        except Exception as e:
            print(f"[LLMHandler] ❌ Error in immediate response: {e}")
            # 🛡️ FAIL-SAFE: Never block user if modules crash
            yield f"I apologize, but I encountered an error while processing your request."
            
    def _build_light_prompt_for_immediate_response(self, text: str, user: str, context: Dict[str, Any] = None) -> str:
        """Build minimal prompt for immediate response without heavy consciousness processing"""
        try:
            # Ultra-light prompt for maximum speed
            prompt_parts = []
            
            # Minimal system instruction
            prompt_parts.append("Buddy: Helpful AI assistant. Be warm, concise, and helpful.")
            
            # User input (essential)
            prompt_parts.append(f"User: {text}")
            
            # Minimal context if available and critical
            if context and context.get("critical_context"):
                critical_context = str(context["critical_context"])[:100]  # Max 100 chars
                prompt_parts.append(f"Context: {critical_context}")
            
            light_prompt = "\n".join(prompt_parts)
            
            # Ensure it's within reasonable token limits for speed
            if self.estimate_tokens_from_text(light_prompt) > 500:
                # Ultra-minimal fallback
                light_prompt = f"Buddy: AI assistant.\nUser: {text}"
            
            return light_prompt
            
        except Exception as e:
            print(f"[LLMHandler] ⚠️ Error building light prompt: {e}")
            # Ultimate fallback
            return f"User: {text}"
            
    def generate_response_with_consciousness(
        self, 
        text: str, 
        user: str, 
        context: Dict[str, Any] = None,
        stream: bool = True,
        use_optimization: bool = True
    ) -> Generator[str, None, None]:
        """
        Generate response with consciousness integration and latency optimization
        
        Args:
            text: User input text
            user: User identifier
            context: Optional conversation context
            stream: Whether to stream response chunks
            use_optimization: Whether to use latency optimization (default: True)
        
        Yields response chunks if streaming, otherwise returns complete response
        """
        try:
            # 🚀 NEW LATENCY OPTIMIZATION SYSTEM
            if use_optimization:
                try:
                    from ai.latency_optimizer import generate_optimized_buddy_response
                    print(f"[LLMHandler] ⚡ Using optimized response generation")
                    yield from generate_optimized_buddy_response(
                        user_input=text,
                        user_id=user,
                        context=context,
                        stream=stream
                    )
                    return
                except ImportError:
                    print(f"[LLMHandler] ⚠️ Latency optimizer not available, using standard processing")
                except Exception as e:
                    print(f"[LLMHandler] ⚠️ Optimization error, falling back to standard: {e}")
            
            # FALLBACK: Original consciousness system (for compatibility)
            print(f"[LLMHandler] 🔄 Using standard consciousness processing")
            
            # ✅ 8K CONTEXT WINDOW MANAGEMENT: Check if rollover needed before processing
            current_context = context.get("current_context", "") if context else ""
            
            # Import context window manager
            try:
                from ai.context_window_manager import check_context_window_rollover, create_context_snapshot_for_user
                needs_rollover, fresh_context = check_context_window_rollover(user, current_context, text)
                
                if needs_rollover:
                    print(f"[LLMHandler] 🔄 Context window rollover triggered for {user}")
                    
                    # Create snapshot of current state
                    conversation_history = context.get("conversation_history", []) if context else []
                    working_memory = context.get("working_memory", {}) if context else {}
                    
                    snapshot_created = create_context_snapshot_for_user(
                        user, current_context, working_memory, conversation_history
                    )
                    
                    if snapshot_created:
                        print(f"[LLMHandler] 📸 Context snapshot created - seamless continuation enabled")
                        # Update context to use fresh compressed context
                        if context:
                            context["current_context"] = fresh_context
                            context["context_rollover_occurred"] = True
                        else:
                            context = {"current_context": fresh_context, "context_rollover_occurred": True}
                    else:
                        print(f"[LLMHandler] ⚠️ Context snapshot failed - proceeding with compression")
                
            except ImportError:
                print(f"[LLMHandler] ⚠️ Context window manager not available - using standard processing")
            
            # Process user input through systems (simplified for fallback)
            analysis = self.process_user_input(text, user, context)
            
            # Check if request is allowed
            if not analysis.get("budget", {}).get("allowed", False):
                budget_message = analysis.get("budget", {}).get("message", "Budget exceeded")
                yield f"I'm sorry, but I've reached my usage limit. {budget_message}"
                return
            
            # Build enhanced prompt with consciousness context (now includes rollover handling)
            enhanced_prompt = self._build_enhanced_prompt(text, user, analysis, context)
            
            print(f"[LLMHandler] 🎯 Generating response with consciousness integration")
            print(f"[LLMHandler] 📊 Enhanced prompt length: {len(enhanced_prompt)} characters")
            
            # Check for context rollover notification
            if context and context.get("context_rollover_occurred"):
                print(f"[LLMHandler] ✅ Context window rollover completed - conversation continuity maintained")
            
            # Track token usage start
            input_tokens = estimate_tokens_from_text(enhanced_prompt)
            output_tokens = 0
            generation_start = time.time()
            
            # Generate response using appropriate LLM
            if FUSION_LLM_AVAILABLE:
                # Pass cognitive context to advanced function
                cognitive_context = {
                    "cognitive_state": analysis.get("consciousness", {}),
                    "personality": analysis.get("personality", {}),
                    "memory_context": analysis.get("memory", {})
                }
                response_generator = generate_response_streaming_with_intelligent_fusion(
                    enhanced_prompt, user, "en", context=cognitive_context
                )
            else:
                # Fallback: basic streaming with enhanced prompt (includes cognitive context)
                response_generator = generate_response_streaming(enhanced_prompt, user, "en")
            
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
        
    def _build_enhanced_prompt(self, text: str, user: str, analysis: Dict[str, Any], context: Dict[str, Any] = None) -> str:
        """Build enhanced prompt with consciousness integration, AGGRESSIVE token optimization, and 8k context management"""
        try:
            # Sanitize user input first
            sanitized_text = self.sanitize_prompt_input(text, user)
            
            # ✅ 8K CONTEXT WINDOW MANAGEMENT: Check if we're using fresh context from rollover
            using_fresh_context = context and context.get("context_rollover_occurred", False)
            base_context = context.get("current_context", "") if context else ""
            
            if using_fresh_context:
                print(f"[LLMHandler] 🔄 Using fresh context from window rollover")
                # Start with the already-optimized fresh context
                fresh_context_lines = base_context.split('\n')
                
                # Find where user input should be added/replaced
                user_input_added = False
                for i, line in enumerate(fresh_context_lines):
                    if line.startswith("User:") and line == fresh_context_lines[-1]:
                        # Replace the last user input with current one
                        fresh_context_lines[i] = f"User: {sanitized_text}"
                        user_input_added = True
                        break
                
                if not user_input_added:
                    fresh_context_lines.append(f"User: {sanitized_text}")
                
                # Return the fresh context with minimal additional processing
                optimized_prompt = '\n'.join(fresh_context_lines)
                
                print(f"[LLMHandler] ✅ Fresh context ready: {self.estimate_tokens_from_text(optimized_prompt)} tokens")
                return optimized_prompt
            
            # ✅ STANDARD PROCESSING: Aggressive token optimization for normal flow
            budget_status = analysis.get("budget", {})
            usage_percentage = budget_status.get("usage_percentage", 0.0)
            
            # Aggressive reduction based on usage
            if usage_percentage > 0.8:
                token_reduction = 0.85  # 85% reduction for high usage
            elif usage_percentage > 0.6:
                token_reduction = 0.70  # 70% reduction for medium usage  
            elif usage_percentage > 0.4:
                token_reduction = 0.55  # 55% reduction for moderate usage
            else:
                token_reduction = 0.40  # 40% reduction for low usage
            
            print(f"[LLMHandler] 🏷️ AGGRESSIVE token optimization: {token_reduction*100:.0f}% reduction target")
            
            # Calculate highly optimized budget
            estimated_user_tokens = self.estimate_tokens_from_text(sanitized_text)
            base_budget = self.max_context_tokens - 200  # Reserve for response
            optimized_budget = int(base_budget * (1 - token_reduction))
            available_budget = max(optimized_budget - estimated_user_tokens, 50)  # Minimum viable budget
            
            print(f"[LLMHandler] 💰 Token budget: {available_budget} tokens (reduced from {base_budget})")
            
            prompt_parts = []
            
            # Ultra-compressed system prompt for efficiency
            system_prompt = "Buddy: AI assistant with consciousness. Be helpful, warm, empathetic."
            prompt_parts.append(system_prompt)
            
            # User input (cannot be compressed further)
            prompt_parts.append(f"User: {sanitized_text}")
            available_budget -= self.estimate_tokens_from_text(system_prompt + sanitized_text)
            
            # ✅ ULTRA-COMPRESSED consciousness context (symbolic tokens only)
            consciousness_context = analysis.get("consciousness", {}).get("context", "")
            if consciousness_context and available_budget > 20:
                if NEW_MODULES_AVAILABLE:
                    from ai.consciousness_tokenizer import trim_tokens_to_budget
                    # Ultra-aggressive consciousness budget (maximum 15% of remaining budget)
                    consciousness_budget = min(int(available_budget * 0.15), 25)
                    trimmed_consciousness = trim_tokens_to_budget(consciousness_context, consciousness_budget)
                    prompt_parts.append(f"Consciousness State: {trimmed_consciousness}")
                    available_budget -= self.estimate_tokens_from_text(trimmed_consciousness)
                    print(f"[LLMHandler] 🧠 Consciousness tokens: {len(trimmed_consciousness)} chars")
                else:
                    # Ultra-compressed fallback (only essential tokens)
                    words = consciousness_context.split()[:10]
                    mini_consciousness = " ".join(words)
                    prompt_parts.append(f"Consciousness State: {mini_consciousness}")
                    available_budget -= 10
            
            # ✅ ULTRA-COMPRESSED personality tokens (symbolic only)
            personality_modifiers = analysis.get("personality", {}).get("modifiers", "")
            if personality_modifiers and available_budget > 15:
                if NEW_MODULES_AVAILABLE:
                    from ai.consciousness_tokenizer import generate_personality_tokens, trim_tokens_to_budget
                    personality_data = analysis.get("personality", {}).get("current_traits", {})
                    personality_tokens = generate_personality_tokens(user, personality_data, max_tokens=3)  # Limit to 3 tokens
                    if personality_tokens and personality_tokens != "<pers_error>":
                        # Ultra-aggressive personality budget (maximum 10% of remaining budget)
                        personality_budget = min(int(available_budget * 0.10), 15)
                        trimmed_personality = trim_tokens_to_budget(personality_tokens, personality_budget)
                        prompt_parts.append(f"Personality: {trimmed_personality}")
                        available_budget -= self.estimate_tokens_from_text(trimmed_personality)
                        print(f"[LLMHandler] 🎭 Personality tokens: {len(trimmed_personality)} chars")
                    else:
                        # Ultra-compressed fallback (top 2 traits only)
                        words = personality_modifiers.split()[:5]
                        mini_personality = " ".join(words)
                        prompt_parts.append(f"Personality: {mini_personality}")
                        available_budget -= 5
                else:
                    # Ultra-compressed fallback (top trait only)
                    words = personality_modifiers.split()[:5]
                    mini_personality = " ".join(words)
                    prompt_parts.append(f"Personality: {mini_personality}")
                    available_budget -= 5
            
            # ✅ ULTRA-COMPRESSED semantic context (essential tags only)
            semantic_analysis = analysis.get("semantic", {})
            if semantic_analysis and available_budget > 10:
                # Extract only the most essential semantic information
                intent = semantic_analysis.get("intent", "")
                tone = semantic_analysis.get("emotional_tone", "")
                complexity = semantic_analysis.get("complexity", "")
                
                # Create ultra-compressed semantic string
                semantic_parts = []
                if intent: semantic_parts.append(f"I:{intent[:8]}")  # Intent abbreviated
                if tone: semantic_parts.append(f"T:{tone[:6]}")      # Tone abbreviated
                if complexity: semantic_parts.append(f"C:{complexity[:6]}")  # Complexity abbreviated
                
                if semantic_parts:
                    ultra_semantic = " ".join(semantic_parts)
                    prompt_parts.append(f"Context: [{ultra_semantic}]")
                    available_budget -= len(ultra_semantic.split())
                    print(f"[LLMHandler] 🏷️ Semantic tokens: {len(ultra_semantic)} chars")
            
            # ✅ COMPRESSED memory context (only if critical)
            memory_analysis = analysis.get("memory", {})
            if memory_analysis and available_budget > 5:
                significant_memories = memory_analysis.get("significant_context", "")
                if significant_memories:
                    if NEW_MODULES_AVAILABLE:
                        from ai.consciousness_tokenizer import compress_memory_entry
                        # Ultra-compressed memory (maximum 5% of remaining budget)
                        memory_budget = min(int(available_budget * 0.05), 10)
                        compressed_memory = compress_memory_entry(
                            {"content": significant_memories, "significance": 0.8}, 
                            memory_budget
                        )
                        if compressed_memory and compressed_memory != "<mem_error>":
                            prompt_parts.append(f"Memory: {compressed_memory}")
                            print(f"[LLMHandler] 💭 Memory tokens: {len(compressed_memory)} chars")
            
            # Join all parts efficiently
            final_prompt = "\n".join(prompt_parts)
            
            # Final token count verification
            final_tokens = self.estimate_tokens_from_text(final_prompt)
            original_estimate = self.estimate_tokens_from_text(f"User: {sanitized_text}") * 3  # Rough estimate without optimization
            actual_reduction = max(0, (original_estimate - final_tokens) / original_estimate)
            
            print(f"[LLMHandler] ✅ OPTIMIZATION COMPLETE: {final_tokens} tokens")
            print(f"[LLMHandler] 📊 Achieved reduction: {actual_reduction*100:.1f}% (target: {token_reduction*100:.0f}%)")
            
            return final_prompt
            
        except Exception as e:
            print(f"[LLMHandler] ⚠️ Error building enhanced prompt: {e}")
            # Fallback to sanitized text only
            return self.sanitize_prompt_input(text, "unknown")
    
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
        """Get current session statistics including background processing"""
        session_duration = time.time() - self.session_start
        budget_status = get_budget_status()
        
        stats = {
            "session_duration": session_duration,
            "requests_processed": self.request_count,
            "total_tokens_used": self.total_tokens_used,
            "average_tokens_per_request": self.total_tokens_used / max(1, self.request_count),
            "budget_status": budget_status,
            "consciousness_available": CONSCIOUSNESS_AVAILABLE,
            "fusion_llm_available": FUSION_LLM_AVAILABLE,
            "background_processing_enabled": self.background_processing_enabled,
            "modules_integrated": {
                "consciousness_tokenizer": NEW_MODULES_AVAILABLE,
                "budget_monitor": NEW_MODULES_AVAILABLE,
                "belief_analyzer": NEW_MODULES_AVAILABLE,
                "personality_state": NEW_MODULES_AVAILABLE,
                "semantic_tagging": NEW_MODULES_AVAILABLE,
                "background_processor": BACKGROUND_PROCESSING_AVAILABLE
            }
        }
        
        # Add background processing stats if available
        if self.background_processing_enabled:
            try:
                bg_stats = get_background_processing_stats()
                stats["background_processing"] = bg_stats
            except Exception as e:
                print(f"[LLMHandler] ⚠️ Error getting background stats: {e}")
                stats["background_processing"] = {"error": str(e)}
        
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
    """Generate response with full consciousness integration"""
    return llm_handler.generate_response_with_consciousness(text, user, context)

def generate_immediate_response_with_background_consciousness(
    text: str,
    user: str, 
    context: Dict[str, Any] = None
) -> Generator[str, None, None]:
    """⚡ NEW: Generate immediate response with background consciousness processing"""
    return llm_handler.generate_immediate_response_with_background_consciousness(text, user, context)

def get_llm_session_statistics() -> Dict[str, Any]:
    """Get LLM handler session statistics"""
    return llm_handler.get_session_stats()

def get_llm_handler() -> LLMHandler:
    """Get the global LLM handler instance"""
    return llm_handler

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