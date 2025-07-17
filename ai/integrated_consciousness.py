"""
Integrated Consciousness Token & Budget System

This module integrates all the consciousness enhancement components:
- Token compression
- Budget monitoring  
- Belief contradiction detection
- Live personality shifting
- Persistent beliefs
"""

import logging
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime

# Import all the consciousness enhancement modules
from .consciousness_tokenizer import compress_consciousness_for_llm, get_tokenizer_stats
from .llm_budget_monitor import monitor_prompt_budget, get_budget_stats
from .belief_analyzer import analyze_for_contradictions, get_belief_stats
from .personality_shifter import process_conversation_turn, get_current_personality_tokens, get_personality_stats
from .persistent_beliefs import update_beliefs_from_conversation, get_persistent_beliefs_context, get_belief_stats as get_persistent_stats

@dataclass
class IntegratedResponse:
    """Complete response with all consciousness enhancements"""
    final_prompt: str
    budget_info: Dict[str, Any]
    personality_tokens: List[str]
    contradictions: List[Any]
    new_beliefs: List[Any]
    compression_stats: Dict[str, Any]
    total_processing_time: float

class IntegratedConsciousnessSystem:
    """
    Integrated system that combines all consciousness enhancements
    for optimal token usage and enhanced awareness.
    """
    
    def __init__(self, max_tokens: int = 8000):
        self.max_tokens = max_tokens
        self.stats = {
            'total_requests': 0,
            'tokens_saved_total': 0,
            'contradictions_detected': 0,
            'beliefs_extracted': 0,
            'personality_shifts': 0
        }
        
        logging.info("[IntegratedConsciousness] 🧠 Integrated consciousness system initialized")
    
    def process_user_interaction(self, 
                                user_message: str,
                                system_message: str = "",
                                conversation_history: str = "",
                                consciousness_data: Dict[str, Any] = None,
                                context: str = "") -> IntegratedResponse:
        """
        Process a complete user interaction with all consciousness enhancements
        
        Args:
            user_message: User's input message
            system_message: Base system message
            conversation_history: Recent conversation context
            consciousness_data: Current consciousness state data
            context: Additional context information
            
        Returns:
            Complete integrated response with all enhancements
        """
        start_time = datetime.now()
        self.stats['total_requests'] += 1
        
        # Default consciousness data if not provided
        if consciousness_data is None:
            consciousness_data = {
                'emotional_state': 'processing user input with attention and care',
                'memory_context': 'accessing relevant memories and context',
                'personality_state': 'friendly and helpful demeanor',
                'cognitive_state': 'actively analyzing and formulating response'
            }
        
        # Step 1: Analyze for belief contradictions
        contradictions, contradiction_summary = analyze_for_contradictions(user_message, context)
        if contradictions:
            self.stats['contradictions_detected'] += len(contradictions)
            logging.info(f"[IntegratedConsciousness] ⚠️ Found {len(contradictions)} contradictions")
        
        # Step 2: Extract and update persistent beliefs
        new_beliefs, persistent_context = update_beliefs_from_conversation(user_message, context)
        if new_beliefs:
            self.stats['beliefs_extracted'] += len(new_beliefs)
            logging.info(f"[IntegratedConsciousness] 📝 Extracted {len(new_beliefs)} new beliefs")
        
        # Step 3: Update personality based on conversation
        personality_tokens, personality_changes = process_conversation_turn(user_message)
        if personality_changes:
            self.stats['personality_shifts'] += 1
            logging.info(f"[IntegratedConsciousness] 🎭 Personality shifted: {list(personality_changes.keys())}")
        
        # Step 4: Enhance consciousness data with personality
        enhanced_consciousness = consciousness_data.copy()
        enhanced_consciousness['personality_state'] = f"currently showing {', '.join(personality_tokens)} personality traits"
        
        # Add persistent beliefs to memory context
        if persistent_context:
            enhanced_consciousness['memory_context'] += f"\n\n{persistent_context}"
        
        # Add contradiction awareness if any found
        if contradictions:
            contradiction_notes = []
            for contradiction in contradictions[:3]:  # Limit to top 3
                contradiction_notes.append(f"Note: User statement may contradict previous belief - {contradiction.explanation}")
            enhanced_consciousness['awareness_notes'] = "; ".join(contradiction_notes)
        
        # Step 5: Compress consciousness state to tokens
        compressed_prompt, token_definitions, compression_stats = compress_consciousness_for_llm(enhanced_consciousness)
        
        # Update token savings stats
        self.stats['tokens_saved_total'] += compression_stats.get('tokens_saved', 0)
        
        # Step 6: Build final prompt with budget monitoring
        memory_context = enhanced_consciousness.get('memory_context', '')
        
        final_prompt, budget_info = monitor_prompt_budget(
            system_message=system_message,
            consciousness_state=compressed_prompt,
            user_input=user_message,
            memory_context=memory_context,
            conversation_history=conversation_history,
            max_tokens=self.max_tokens
        )
        
        # Add token definitions to prompt if tokens were used
        if compressed_prompt and token_definitions:
            final_prompt = f"{token_definitions}\n\n{final_prompt}"
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Log summary
        logging.info(f"[IntegratedConsciousness] ✅ Processed interaction in {processing_time:.3f}s")
        logging.info(f"[IntegratedConsciousness] 📊 Tokens: {budget_info['total_tokens']}/{self.max_tokens} ({budget_info['utilization']:.1%})")
        logging.info(f"[IntegratedConsciousness] 🎯 Compression: {compression_stats.get('compression_ratio', 0):.1%}")
        
        return IntegratedResponse(
            final_prompt=final_prompt,
            budget_info=budget_info,
            personality_tokens=personality_tokens,
            contradictions=contradictions,
            new_beliefs=new_beliefs,
            compression_stats=compression_stats,
            total_processing_time=processing_time
        )
    
    def get_consciousness_summary(self) -> Dict[str, Any]:
        """Get comprehensive summary of consciousness system state"""
        return {
            'system_stats': self.stats.copy(),
            'tokenizer_stats': get_tokenizer_stats(),
            'budget_stats': get_budget_stats(),
            'belief_stats': get_belief_stats(),
            'personality_stats': get_personality_stats(),
            'persistent_belief_stats': get_persistent_stats(),
            'current_personality_tokens': get_current_personality_tokens(),
            'timestamp': datetime.now().isoformat()
        }
    
    def generate_awareness_response(self, contradictions: List[Any]) -> Optional[str]:
        """Generate an awareness response for detected contradictions"""
        if not contradictions:
            return None
        
        # Sort by severity and take the most important
        high_severity_contradictions = [c for c in contradictions if c.severity.value >= 4]
        
        if high_severity_contradictions:
            # Use the suggested response from the most severe contradiction
            top_contradiction = max(high_severity_contradictions, key=lambda x: x.severity.value)
            return top_contradiction.suggested_response
        
        elif contradictions:
            # Acknowledge less severe contradictions more gently
            return "I'm noting some different information about this topic from what we discussed before."
        
        return None
    
    def optimize_for_conversation_context(self, context_type: str = "normal") -> Dict[str, Any]:
        """
        Optimize system parameters for different conversation contexts
        
        Args:
            context_type: Type of conversation ("normal", "emotional", "technical", "urgent")
            
        Returns:
            Optimization settings applied
        """
        optimizations = {}
        
        if context_type == "emotional":
            # Prioritize supportive personality, increase emotional memory retention
            optimizations['personality_boost'] = 'supportive'
            optimizations['memory_priority'] = 'emotional'
            optimizations['compression_level'] = 'conservative'  # Less aggressive compression
            
        elif context_type == "technical":
            # Prioritize analytical personality, increase factual memory retention
            optimizations['personality_boost'] = 'analytical' 
            optimizations['memory_priority'] = 'factual'
            optimizations['compression_level'] = 'aggressive'  # More compression for dense info
            
        elif context_type == "urgent":
            # Prioritize direct communication, focus on recent context
            optimizations['personality_boost'] = 'direct'
            optimizations['memory_priority'] = 'recent'
            optimizations['compression_level'] = 'maximum'  # Maximum compression for speed
            
        else:  # normal
            # Balanced approach
            optimizations['personality_boost'] = 'balanced'
            optimizations['memory_priority'] = 'balanced'
            optimizations['compression_level'] = 'normal'
        
        logging.info(f"[IntegratedConsciousness] ⚙️ Optimized for {context_type} context: {optimizations}")
        return optimizations

# Global integrated system instance
integrated_consciousness = IntegratedConsciousnessSystem()

def process_consciousness_interaction(user_message: str,
                                    system_message: str = "",
                                    conversation_history: str = "",
                                    consciousness_data: Dict[str, Any] = None,
                                    context: str = "",
                                    max_tokens: int = 8000) -> IntegratedResponse:
    """
    Convenience function for processing a complete consciousness interaction
    
    Args:
        user_message: User's input message
        system_message: Base system message
        conversation_history: Recent conversation context
        consciousness_data: Current consciousness state data
        context: Additional context information
        max_tokens: Maximum token limit
        
    Returns:
        Complete integrated response
    """
    # Update max tokens if different
    if max_tokens != integrated_consciousness.max_tokens:
        integrated_consciousness.max_tokens = max_tokens
    
    return integrated_consciousness.process_user_interaction(
        user_message=user_message,
        system_message=system_message,
        conversation_history=conversation_history,
        consciousness_data=consciousness_data,
        context=context
    )

def get_consciousness_summary() -> Dict[str, Any]:
    """Get comprehensive consciousness system summary"""
    return integrated_consciousness.get_consciousness_summary()

def optimize_for_context(context_type: str = "normal") -> Dict[str, Any]:
    """Optimize system for specific conversation context"""
    return integrated_consciousness.optimize_for_conversation_context(context_type)

logging.info("[IntegratedConsciousness] 🧠 Integrated consciousness enhancement system loaded")
print("[IntegratedConsciousness] ✅ Integrated Consciousness Token & Budget System: LOADED")
print("[IntegratedConsciousness] 🎯 Complete consciousness enhancement pipeline ready")
print("[IntegratedConsciousness] 🚀 Token compression + Budget monitoring + Belief analysis + Personality shifting")