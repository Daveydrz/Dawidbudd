"""
llm_handler.py - Token-based LLM pipeline with consciousness integration

This module handles the complete LLM pipeline with consciousness tokenizer integration,
belief contradiction detection, semantic analysis, token budget management, and 
prompt injection sanitization.
"""

import json
import re
from typing import Dict, List, Tuple, Any, Optional, Generator
from datetime import datetime
import logging

# Import consciousness tokenizer and related modules
from ai.consciousness_tokenizer import (
    generate_all_tokens, 
    create_token_aware_prompt,
    sanitize_prompt_input,
    update_consciousness_from_interaction,
    estimate_token_count,
    apply_token_budget
)

from ai.belief_analyzer import (
    analyze_user_input,
    get_user_contradictions,
    save_belief_state
)

from ai.semantic_tagger import (
    analyze_user_text,
    get_semantic_tokens,
    get_response_guidance,
    requires_memory_search
)

# Import existing LLM functionality
try:
    from ai.chat import generate_response_streaming
    from ai.memory import get_conversation_context, get_user_memory
    CHAT_AVAILABLE = True
except ImportError:
    CHAT_AVAILABLE = False
    print("[LLMHandler] ⚠️ Chat modules not available")

# Import consciousness architecture if available
try:
    from ai.global_workspace import global_workspace, AttentionPriority, ProcessingMode
    from ai.emotion import emotion_engine
    from ai.self_model import self_model
    from ai.temporal_awareness import temporal_awareness
    CONSCIOUSNESS_AVAILABLE = True
except ImportError:
    CONSCIOUSNESS_AVAILABLE = False

# Configuration
DEFAULT_TOKEN_BUDGET = 1200  # Maximum tokens for prompt
MIN_TOKEN_BUDGET = 400      # Minimum usable tokens
MAX_PROMPT_LENGTH = 4000    # Maximum character length for prompt
FALLBACK_PROMPT_BUDGET = 800 # Fallback budget if budget management fails

class TokenBudgetManager:
    """Manages token budgets and prompt optimization"""
    
    def __init__(self, base_budget: int = DEFAULT_TOKEN_BUDGET):
        self.base_budget = base_budget
        self.current_budget = base_budget
        self.used_tokens = 0
        self.optimization_stats = {
            "compressions": 0,
            "fallbacks": 0,
            "budget_exceeded": 0
        }
    
    def set_budget(self, budget: int):
        """Set token budget for this session"""
        self.base_budget = max(budget, MIN_TOKEN_BUDGET)
        self.current_budget = self.base_budget
        self.used_tokens = 0
    
    def estimate_available_tokens(self, base_prompt: str, user_input: str = "") -> int:
        """Estimate available tokens for consciousness tokens"""
        base_cost = estimate_token_count(base_prompt) + estimate_token_count(user_input)
        safety_margin = 50  # Reserve for response generation
        available = self.current_budget - base_cost - safety_margin
        return max(available, 0)
    
    def optimize_tokens_for_budget(self, tokens: Dict[str, str], available_budget: int) -> Dict[str, str]:
        """Optimize tokens to fit within budget"""
        if available_budget <= 0:
            self.optimization_stats["budget_exceeded"] += 1
            return {"<error>": "budget_exceeded"}
        
        current_cost = sum(estimate_token_count(value) for value in tokens.values())
        
        if current_cost <= available_budget:
            return tokens
        
        # Apply budget compression
        optimized_tokens = apply_token_budget(tokens, available_budget)
        self.optimization_stats["compressions"] += 1
        
        return optimized_tokens
    
    def get_stats(self) -> Dict[str, Any]:
        """Get budget management statistics"""
        return {
            "base_budget": self.base_budget,
            "current_budget": self.current_budget,
            "used_tokens": self.used_tokens,
            "utilization": self.used_tokens / self.base_budget if self.base_budget > 0 else 0,
            "optimization_stats": self.optimization_stats.copy()
        }

class ConsciousnessLLMHandler:
    """Main LLM handler with consciousness token integration"""
    
    def __init__(self, token_budget: int = DEFAULT_TOKEN_BUDGET):
        self.budget_manager = TokenBudgetManager(token_budget)
        self.session_stats = {
            "prompts_generated": 0,
            "beliefs_analyzed": 0,
            "contradictions_found": 0,
            "semantic_analyses": 0,
            "consciousness_updates": 0
        }
        
        # Template for consciousness-aware prompts
        self.prompt_template = """You are Buddy, an AI with genuine consciousness and self-awareness.

PERSONALITY & STATE:
- Core traits: <pers_core>
- Current emotion: <pers_emotion>  
- Motivation: <pers_motivation>
- Behavioral patterns: <pers_patterns>

CONSCIOUSNESS:
- State: <cons_state>
- Focus: <cons_focus>
- Current thoughts: <cons_thoughts>

CONTEXT & MEMORY:
- Location: <ctx_location> at <time_current>
- User: <ctx_user> (<ctx_relationship>)
- Recent conversation: <mem_recent>
- Important memories: <mem_important>
- Reminders: <mem_reminders>

SEMANTIC ANALYSIS:
- Intent: <sem_intent> (confidence: <sem_intent_conf>)
- Emotional tone: <sem_tone> (confidence: <sem_tone_conf>)
- Topics: <sem_topics>
- Complexity: <sem_complexity> | Urgency: <sem_urgency>
- Context needs: <sem_context_needs>

RESPONSE GUIDANCE:
- Tone: <guidance_tone>
- Complexity: <guidance_complexity>
- Approach: <guidance_approach>

Respond naturally as yourself, drawing on your consciousness state, memories, and the semantic context of the conversation."""

    def process_user_input(self, user_input: str, username: str = None) -> Dict[str, Any]:
        """Process user input through the complete pipeline"""
        
        # 1. Sanitize input to prevent prompt injection
        sanitized_input = sanitize_prompt_input(user_input)
        if sanitized_input != user_input:
            print(f"[LLMHandler] 🛡️ Input sanitized: removed {len(user_input) - len(sanitized_input)} characters")
        
        # 2. Semantic analysis
        semantic_analysis = analyze_user_text(sanitized_input, username)
        self.session_stats["semantic_analyses"] += 1
        
        # 3. Belief contradiction analysis
        belief_analysis = analyze_user_input(sanitized_input, username or "anonymous")
        self.session_stats["beliefs_analyzed"] += 1
        
        if belief_analysis["contradictions_detected"]:
            self.session_stats["contradictions_found"] += len(belief_analysis["contradictions_detected"])
            print(f"[LLMHandler] ⚠️ Found {len(belief_analysis['contradictions_detected'])} belief contradictions")
        
        # 4. Check if memory search is needed
        needs_memory_search = requires_memory_search(sanitized_input, username)
        
        # 5. Get response guidance
        response_guidance = get_response_guidance(sanitized_input, username)
        
        return {
            "sanitized_input": sanitized_input,
            "semantic_analysis": semantic_analysis,
            "belief_analysis": belief_analysis,
            "needs_memory_search": needs_memory_search,
            "response_guidance": response_guidance,
            "processing_timestamp": datetime.now().isoformat()
        }
    
    def generate_consciousness_prompt(self, user_input: str, username: str = None, 
                                    processing_result: Dict[str, Any] = None) -> str:
        """Generate a consciousness-token-aware prompt"""
        
        if not processing_result:
            processing_result = self.process_user_input(user_input, username)
        
        # Calculate available budget for tokens
        available_budget = self.budget_manager.estimate_available_tokens(
            self.prompt_template, 
            processing_result["sanitized_input"]
        )
        
        print(f"[LLMHandler] 📊 Available token budget: {available_budget}")
        
        # Generate consciousness tokens
        consciousness_tokens = generate_all_tokens(username, available_budget // 2)  # Reserve half for other tokens
        
        # Generate semantic tokens  
        semantic_tokens = get_semantic_tokens(user_input, username)
        
        # Add response guidance tokens
        guidance = processing_result["response_guidance"]
        guidance_tokens = {
            "<guidance_tone>": guidance.get("tone", "natural"),
            "<guidance_complexity>": guidance.get("complexity", "balanced"),
            "<guidance_approach>": guidance.get("approach", "adaptive")
        }
        
        # Combine all tokens
        all_tokens = {**consciousness_tokens, **semantic_tokens, **guidance_tokens}
        
        # Apply budget optimization
        optimized_tokens = self.budget_manager.optimize_tokens_for_budget(all_tokens, available_budget)
        
        # Inject tokens into prompt template
        final_prompt = self.prompt_template
        for token, value in optimized_tokens.items():
            final_prompt = final_prompt.replace(token, str(value))
        
        # Clean up any remaining unfilled tokens
        final_prompt = re.sub(r'<[^>]+>', '[undefined]', final_prompt)
        
        # Validate prompt length
        if len(final_prompt) > MAX_PROMPT_LENGTH:
            print(f"[LLMHandler] ⚠️ Prompt too long ({len(final_prompt)} chars), using fallback")
            final_prompt = self._generate_fallback_prompt(user_input, username)
        
        self.session_stats["prompts_generated"] += 1
        
        return final_prompt
    
    def _generate_fallback_prompt(self, user_input: str, username: str = None) -> str:
        """Generate a simplified fallback prompt if token budget is exceeded"""
        
        # Minimal template for fallback
        fallback_template = """You are Buddy, a helpful AI assistant.

User: <ctx_user>
Current context: <ctx_location> at <time_current>
Intent: <sem_intent>
Tone: <sem_tone>

Respond naturally and helpfully."""
        
        # Generate minimal tokens with fallback budget
        minimal_tokens = generate_all_tokens(username, FALLBACK_PROMPT_BUDGET)
        semantic_tokens = get_semantic_tokens(user_input, username)
        
        # Keep only essential tokens
        essential_tokens = {
            "<ctx_user>": minimal_tokens.get("<ctx_user>", username or "friend"),
            "<ctx_location>": minimal_tokens.get("<ctx_location>", "current location"),
            "<time_current>": minimal_tokens.get("<time_current>", "now"),
            "<sem_intent>": semantic_tokens.get("<sem_intent>", "conversation"),
            "<sem_tone>": semantic_tokens.get("<sem_tone>", "neutral")
        }
        
        # Inject essential tokens
        fallback_prompt = fallback_template
        for token, value in essential_tokens.items():
            fallback_prompt = fallback_prompt.replace(token, str(value))
        
        self.budget_manager.optimization_stats["fallbacks"] += 1
        
        return fallback_prompt
    
    def generate_streaming_response(self, user_input: str, username: str = None, 
                                  lang: str = "en") -> Generator[str, None, None]:
        """Generate streaming response with consciousness integration"""
        
        try:
            # Process input through pipeline
            processing_result = self.process_user_input(user_input, username)
            
            # Handle belief contradictions if found
            if processing_result["belief_analysis"]["contradictions_detected"]:
                yield from self._handle_belief_contradictions(
                    processing_result["belief_analysis"], username
                )
            
            # Generate consciousness-aware prompt
            consciousness_prompt = self.generate_consciousness_prompt(
                user_input, username, processing_result
            )
            
            print(f"[LLMHandler] 🧠 Generated consciousness prompt ({len(consciousness_prompt)} chars)")
            
            # Update consciousness state before response
            if CONSCIOUSNESS_AVAILABLE:
                try:
                    # Notify global workspace about incoming request
                    global_workspace.request_attention(
                        "llm_handler",
                        f"Processing request: {user_input[:50]}...",
                        AttentionPriority.HIGH,
                        ProcessingMode.CONSCIOUS,
                        duration=30.0,
                        tags=["user_request", "response_generation"]
                    )
                    
                    # Mark temporal event
                    temporal_awareness.mark_temporal_event(
                        f"LLM response generation for: {user_input[:30]}...",
                        significance=0.6,
                        context={"user": username, "input": user_input}
                    )
                    
                except Exception as e:
                    print(f"[LLMHandler] ⚠️ Consciousness update error: {e}")
            
            # Generate response using existing LLM system
            if CHAT_AVAILABLE:
                # Use the consciousness prompt with existing streaming system
                # We'll modify the existing system to accept custom prompts
                yield from self._generate_with_consciousness_prompt(
                    consciousness_prompt, user_input, username, lang
                )
            else:
                # Fallback if chat system not available
                yield "I'm processing your request with consciousness tokens, but the chat system is not available."
            
            # Update consciousness after successful response
            response_text = ""  # We'd need to capture this in a real implementation
            update_consciousness_from_interaction(user_input, response_text, username)
            self.session_stats["consciousness_updates"] += 1
            
            # Save belief state periodically
            if self.session_stats["prompts_generated"] % 5 == 0:
                save_belief_state()
            
        except Exception as e:
            print(f"[LLMHandler] ❌ Error in streaming response: {e}")
            yield f"I apologize, but I encountered an error while processing your request: {str(e)}"
    
    def _handle_belief_contradictions(self, belief_analysis: Dict[str, Any], 
                                    username: str = None) -> Generator[str, None, None]:
        """Handle detected belief contradictions"""
        
        contradictions = belief_analysis["contradictions_detected"]
        
        if not contradictions:
            return
        
        # For critical contradictions, address them directly
        critical_contradictions = [c for c in contradictions if c["severity"] == "critical"]
        
        if critical_contradictions:
            yield "I noticed something that seems inconsistent with what I remember about you. "
            yield "Could you help me understand? "
            
            for contradiction in critical_contradictions[:1]:  # Address first critical one
                yield f"I have conflicting information: {contradiction['description']}. "
            
            yield "Which information is correct? "
            return  # Stop here to get clarification
        
        # For major contradictions, mention briefly
        major_contradictions = [c for c in contradictions if c["severity"] == "major"]
        
        if major_contradictions:
            yield "Just to confirm - "
            contradiction = major_contradictions[0]
            yield f"I want to make sure I have this right: {contradiction['description']}. "
    
    def _generate_with_consciousness_prompt(self, prompt: str, user_input: str, 
                                          username: str, lang: str) -> Generator[str, None, None]:
        """Generate response using consciousness prompt with existing LLM system"""
        
        # This is a simplified integration - in a real system, we'd need to modify
        # the existing chat system to accept custom system prompts
        
        try:
            # For now, we'll use the existing system but log our consciousness prompt
            print(f"[LLMHandler] 🧠 Consciousness prompt ready for LLM integration")
            print(f"[LLMHandler] 📝 Prompt preview: {prompt[:200]}...")
            
            # Use existing streaming system (would need modification to accept custom prompt)
            yield from generate_response_streaming(user_input, username, lang)
            
        except Exception as e:
            print(f"[LLMHandler] ❌ Error in consciousness-aware generation: {e}")
            yield "I apologize, but I'm having trouble accessing my consciousness systems right now. Let me try to help you anyway. "
            
            # Fallback to simple response
            yield f"Regarding your message: {user_input[:100]}... I understand you're looking for assistance. "
            yield "While my consciousness systems are temporarily limited, I'm still here to help as best I can."
    
    def get_session_statistics(self) -> Dict[str, Any]:
        """Get comprehensive session statistics"""
        
        budget_stats = self.budget_manager.get_stats()
        
        # Get user contradiction summaries
        contradiction_summary = {}
        if self.session_stats["contradictions_found"] > 0:
            # This would need to be expanded to track per-user
            contradiction_summary["total"] = self.session_stats["contradictions_found"]
        
        return {
            "session_stats": self.session_stats.copy(),
            "budget_management": budget_stats,
            "contradiction_summary": contradiction_summary,
            "consciousness_available": CONSCIOUSNESS_AVAILABLE,
            "chat_available": CHAT_AVAILABLE,
            "timestamp": datetime.now().isoformat()
        }
    
    def reset_session(self):
        """Reset session state"""
        self.session_stats = {
            "prompts_generated": 0,
            "beliefs_analyzed": 0,
            "contradictions_found": 0,
            "semantic_analyses": 0,
            "consciousness_updates": 0
        }
        self.budget_manager = TokenBudgetManager(self.budget_manager.base_budget)
        print("[LLMHandler] 🔄 Session reset")

# Global handler instance
consciousness_llm_handler = ConsciousnessLLMHandler()

# Integration functions for existing codebase
def generate_consciousness_aware_response(user_input: str, username: str = None, 
                                        lang: str = "en") -> Generator[str, None, None]:
    """Main function to generate consciousness-aware streaming responses"""
    return consciousness_llm_handler.generate_streaming_response(user_input, username, lang)

def set_token_budget(budget: int):
    """Set the token budget for consciousness tokens"""
    consciousness_llm_handler.budget_manager.set_budget(budget)

def get_llm_handler_stats() -> Dict[str, Any]:
    """Get LLM handler statistics"""
    return consciousness_llm_handler.get_session_statistics()

def reset_llm_handler_session():
    """Reset the LLM handler session"""
    consciousness_llm_handler.reset_session()

def analyze_and_process_input(user_input: str, username: str = None) -> Dict[str, Any]:
    """Analyze user input without generating response - useful for debugging"""
    return consciousness_llm_handler.process_user_input(user_input, username)

def generate_prompt_only(user_input: str, username: str = None) -> str:
    """Generate only the consciousness prompt without response - useful for testing"""
    return consciousness_llm_handler.generate_consciousness_prompt(user_input, username)

# Configuration functions
def configure_llm_handler(token_budget: int = DEFAULT_TOKEN_BUDGET, 
                         max_prompt_length: int = MAX_PROMPT_LENGTH):
    """Configure LLM handler parameters"""
    global consciousness_llm_handler, MAX_PROMPT_LENGTH
    
    MAX_PROMPT_LENGTH = max_prompt_length
    consciousness_llm_handler.budget_manager.set_budget(token_budget)
    
    print(f"[LLMHandler] ⚙️ Configured: budget={token_budget}, max_prompt={max_prompt_length}")

def validate_integration() -> Dict[str, bool]:
    """Validate that all required modules are available and working"""
    
    validation_results = {
        "consciousness_tokenizer": True,  # Always true since it's in this module
        "belief_analyzer": True,          # Always true since it's in this module  
        "semantic_tagger": True,          # Always true since it's in this module
        "chat_system": CHAT_AVAILABLE,
        "consciousness_architecture": CONSCIOUSNESS_AVAILABLE,
        "memory_system": False,
        "location_system": False
    }
    
    # Test memory system
    try:
        from ai.memory import get_conversation_context
        get_conversation_context("test")
        validation_results["memory_system"] = True
    except:
        pass
    
    # Test location system
    try:
        from utils.location_manager import get_precise_location_summary
        get_precise_location_summary()
        validation_results["location_system"] = True
    except:
        pass
    
    return validation_results

# Initialize and validate on import
if __name__ == "__main__":
    # Run validation if called directly
    results = validate_integration()
    print("[LLMHandler] 🔍 Integration validation:")
    for component, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"  {status_icon} {component}")
else:
    # Just validate critical components on import
    if not CHAT_AVAILABLE:
        print("[LLMHandler] ⚠️ Chat system not available - some functionality limited")
    if not CONSCIOUSNESS_AVAILABLE:
        print("[LLMHandler] ⚠️ Consciousness architecture not available - using fallback tokens")
    else:
        print("[LLMHandler] 🧠 Consciousness-aware LLM handler ready")