"""
LLM Budget Monitor - Smart Token Budget Management
Prevents token overflow while preserving important consciousness context.
"""

import logging
import json
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

class MemoryPriority(Enum):
    """Memory priority levels for budget management"""
    CRITICAL = 10      # Current consciousness state, immediate context
    HIGH = 8          # Recent emotional events, personal details
    MEDIUM = 6        # General conversation history
    LOW = 4           # Older factual information
    MINIMAL = 2       # Background information

@dataclass
class TokenBudget:
    """Token budget configuration"""
    total_limit: int = 8000          # Total token limit for model
    safety_margin: int = 500         # Safety margin before limit
    system_reserved: int = 1000      # Reserved for system prompt
    response_reserved: int = 1500    # Reserved for response generation
    context_limit: int = 5000        # Available for context (calculated)
    
    def __post_init__(self):
        """Calculate available context limit"""
        self.context_limit = self.total_limit - self.safety_margin - self.system_reserved - self.response_reserved

@dataclass
class MemorySegment:
    """Memory segment with priority and token estimation"""
    content: str
    priority: MemoryPriority
    token_estimate: int
    timestamp: datetime
    category: str  # "consciousness", "emotional", "factual", "history"
    compression_ratio: float = 0.0  # How much this can be compressed

class LLMBudgetMonitor:
    """
    Smart Token Budget Management System
    
    Monitors token usage and intelligently trims context while preserving
    important consciousness state and emotional context.
    """
    
    def __init__(self, model_context_limit: int = 8000):
        self.budget = TokenBudget(total_limit=model_context_limit)
        self.current_usage = 0
        self.memory_segments: List[MemorySegment] = []
        
        # Import consciousness tokenizer for compression
        try:
            from .consciousness_tokenizer import consciousness_tokenizer
            self.tokenizer = consciousness_tokenizer
            self.compression_available = True
            logging.info("[BudgetMonitor] 🧠 Consciousness tokenizer integration enabled")
        except ImportError:
            self.tokenizer = None
            self.compression_available = False
            logging.warning("[BudgetMonitor] ⚠️ Consciousness tokenizer not available")
        
        logging.info(f"[BudgetMonitor] 📊 Budget monitor initialized: {self.budget.context_limit} tokens available for context")
    
    def estimate_tokens(self, text: str) -> int:
        """
        Estimate token count for text
        Uses more accurate estimation than simple 4-char rule
        """
        if not text:
            return 0
        
        # More sophisticated token estimation
        # Account for words, punctuation, and typical tokenization patterns
        words = len(text.split())
        chars = len(text)
        
        # Estimate based on character count with word boundary adjustments
        # Typical ratio: 1 token ≈ 3.5-4 characters for English
        char_estimate = chars / 3.7
        
        # Estimate based on word count  
        # Typical ratio: 1 token ≈ 0.75 words
        word_estimate = words / 0.75
        
        # Use the higher estimate for safety
        estimate = int(max(char_estimate, word_estimate))
        
        return max(1, estimate)  # Minimum 1 token
    
    def add_memory_segment(self, content: str, priority: MemoryPriority, 
                          category: str, compression_ratio: float = 0.0):
        """Add a memory segment to budget tracking"""
        if not content.strip():
            return
        
        token_estimate = self.estimate_tokens(content)
        segment = MemorySegment(
            content=content,
            priority=priority,
            token_estimate=token_estimate,
            timestamp=datetime.now(),
            category=category,
            compression_ratio=compression_ratio
        )
        
        self.memory_segments.append(segment)
        self.current_usage += token_estimate
        
        logging.debug(f"[BudgetMonitor] 📝 Added {category} segment: {token_estimate} tokens ({priority.name})")
    
    def check_budget_status(self) -> Dict[str, Any]:
        """Check current budget status"""
        available = self.budget.context_limit - self.current_usage
        usage_percent = (self.current_usage / self.budget.context_limit) * 100
        
        status = {
            'current_usage': self.current_usage,
            'context_limit': self.budget.context_limit,
            'available': available,
            'usage_percent': usage_percent,
            'needs_trimming': self.current_usage > self.budget.context_limit * 0.85,  # 85% threshold
            'critical_level': self.current_usage > self.budget.context_limit * 0.95   # 95% threshold
        }
        
        return status
    
    def optimize_context_for_budget(self, user_input: str, system_prompt: str) -> Tuple[str, str, Dict[str, Any]]:
        """
        Optimize context to fit within token budget
        
        Args:
            user_input: Current user input
            system_prompt: System prompt text
            
        Returns:
            Tuple of (optimized_context, final_system_prompt, optimization_info)
        """
        # Add user input to budget calculation
        user_tokens = self.estimate_tokens(user_input)
        system_tokens = self.estimate_tokens(system_prompt)
        
        # Calculate available space for memory context
        total_fixed = user_tokens + system_tokens
        available_for_memory = self.budget.context_limit - total_fixed
        
        logging.info(f"[BudgetMonitor] 📊 Budget analysis: {total_fixed} fixed tokens, {available_for_memory} available for memory")
        
        # Check if we need to trim
        if self.current_usage <= available_for_memory:
            # No trimming needed
            context = self._build_context_from_segments()
            return context, system_prompt, {
                'trimmed': False, 
                'compression_used': False,
                'original_tokens': self.current_usage,
                'final_tokens': self.current_usage,
                'compression_ratio': 1.0,
                'segments_removed': 0
            }
        
        # Need to optimize - start with compression
        optimized_segments = self._apply_consciousness_compression()
        compressed_usage = sum(seg.token_estimate for seg in optimized_segments)
        
        if compressed_usage <= available_for_memory:
            # Compression sufficient
            context = self._build_context_from_segments(optimized_segments)
            return context, system_prompt, {
                'trimmed': False, 
                'compression_used': True, 
                'original_tokens': self.current_usage,
                'final_tokens': compressed_usage,
                'compression_ratio': compressed_usage / self.current_usage if self.current_usage > 0 else 1.0,
                'segments_removed': 0
            }
        
        # Still need trimming after compression
        trimmed_segments = self._intelligent_trim(optimized_segments, available_for_memory)
        final_context = self._build_context_from_segments(trimmed_segments)
        
        final_usage = sum(seg.token_estimate for seg in trimmed_segments)
        optimization_info = {
            'trimmed': True,
            'compression_used': True,
            'original_tokens': self.current_usage,
            'final_tokens': final_usage,
            'compression_ratio': final_usage / self.current_usage if self.current_usage > 0 else 1.0,
            'segments_removed': len(self.memory_segments) - len(trimmed_segments)
        }
        
        logging.info(f"[BudgetMonitor] ✂️ Context optimized: {self.current_usage} → {final_usage} tokens ({optimization_info['compression_ratio']:.2%} ratio)")
        
        return final_context, system_prompt, optimization_info
    
    def _apply_consciousness_compression(self) -> List[MemorySegment]:
        """Apply consciousness tokenizer compression to segments"""
        if not self.compression_available:
            return self.memory_segments.copy()
        
        compressed_segments = []
        
        for segment in self.memory_segments:
            if segment.category in ['consciousness', 'emotional', 'personality']:
                # Apply consciousness compression
                compressed_content = self.tokenizer.compress_text_consciousness(segment.content)
                compressed_tokens = self.estimate_tokens(compressed_content)
                
                # Create compressed segment
                compressed_segment = MemorySegment(
                    content=compressed_content,
                    priority=segment.priority,
                    token_estimate=compressed_tokens,
                    timestamp=segment.timestamp,
                    category=segment.category,
                    compression_ratio=compressed_tokens / segment.token_estimate if segment.token_estimate > 0 else 1.0
                )
                compressed_segments.append(compressed_segment)
                
                logging.debug(f"[BudgetMonitor] 🧠 Compressed {segment.category}: {segment.token_estimate} → {compressed_tokens} tokens")
            else:
                # Keep segment as-is
                compressed_segments.append(segment)
        
        return compressed_segments
    
    def _intelligent_trim(self, segments: List[MemorySegment], target_tokens: int) -> List[MemorySegment]:
        """Intelligently trim segments to fit target token count"""
        # Sort by priority (highest first), then by recency (newest first)
        sorted_segments = sorted(segments, 
                               key=lambda x: (x.priority.value, x.timestamp.timestamp()), 
                               reverse=True)
        
        selected_segments = []
        current_tokens = 0
        
        # Always preserve critical segments
        for segment in sorted_segments:
            if segment.priority == MemoryPriority.CRITICAL:
                selected_segments.append(segment)
                current_tokens += segment.token_estimate
        
        # Add high-priority segments if space allows
        for segment in sorted_segments:
            if segment.priority == MemoryPriority.HIGH and current_tokens + segment.token_estimate <= target_tokens:
                selected_segments.append(segment)
                current_tokens += segment.token_estimate
        
        # Add medium and lower priority segments as space allows
        for priority_level in [MemoryPriority.MEDIUM, MemoryPriority.LOW, MemoryPriority.MINIMAL]:
            for segment in sorted_segments:
                if (segment.priority == priority_level and 
                    segment not in selected_segments and 
                    current_tokens + segment.token_estimate <= target_tokens):
                    selected_segments.append(segment)
                    current_tokens += segment.token_estimate
        
        return selected_segments
    
    def _build_context_from_segments(self, segments: Optional[List[MemorySegment]] = None) -> str:
        """Build context string from memory segments"""
        if segments is None:
            segments = self.memory_segments
        
        if not segments:
            return ""
        
        # Group segments by category for better organization
        categories = {}
        for segment in segments:
            if segment.category not in categories:
                categories[segment.category] = []
            categories[segment.category].append(segment)
        
        # Build context with sections
        context_parts = []
        
        # Order categories by importance
        category_order = ['consciousness', 'emotional', 'recent', 'personal', 'factual', 'history']
        
        for category in category_order:
            if category in categories:
                # Sort segments in category by priority and recency
                category_segments = sorted(categories[category], 
                                         key=lambda x: (x.priority.value, x.timestamp.timestamp()), 
                                         reverse=True)
                
                for segment in category_segments:
                    context_parts.append(segment.content)
        
        # Add any remaining categories
        for category, category_segments in categories.items():
            if category not in category_order:
                for segment in category_segments:
                    context_parts.append(segment.content)
        
        return '\n'.join(context_parts)
    
    def clear_memory_segments(self):
        """Clear all memory segments and reset usage"""
        self.memory_segments.clear()
        self.current_usage = 0
        logging.debug("[BudgetMonitor] 🧹 Memory segments cleared")
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """Get summary of current memory segments"""
        if not self.memory_segments:
            return {'total_segments': 0, 'total_tokens': 0, 'categories': {}}
        
        categories = {}
        for segment in self.memory_segments:
            if segment.category not in categories:
                categories[segment.category] = {'count': 0, 'tokens': 0}
            categories[segment.category]['count'] += 1
            categories[segment.category]['tokens'] += segment.token_estimate
        
        return {
            'total_segments': len(self.memory_segments),
            'total_tokens': self.current_usage,
            'categories': categories,
            'oldest_segment': min(seg.timestamp for seg in self.memory_segments),
            'newest_segment': max(seg.timestamp for seg in self.memory_segments)
        }

# Global budget monitor instance
llm_budget_monitor = LLMBudgetMonitor()

def prepare_llm_context_with_budget(consciousness_context: Dict[str, Any],
                                   memory_context: str,
                                   user_input: str,
                                   system_prompt: str,
                                   personality_context: str = "") -> Tuple[str, str, Dict[str, Any]]:
    """
    Prepare LLM context with budget management
    
    Args:
        consciousness_context: Current consciousness state
        memory_context: Memory context text
        user_input: User's current input
        system_prompt: Base system prompt
        personality_context: Personality context
        
    Returns:
        Tuple of (final_context, final_system_prompt, budget_info)
    """
    # Clear previous segments
    llm_budget_monitor.clear_memory_segments()
    
    # Add consciousness context (highest priority)
    if consciousness_context:
        consciousness_text = json.dumps(consciousness_context, indent=2)
        llm_budget_monitor.add_memory_segment(
            consciousness_text, 
            MemoryPriority.CRITICAL, 
            'consciousness',
            compression_ratio=0.6  # Consciousness tokenizer can achieve ~60% compression
        )
    
    # Add memory context (high priority)
    if memory_context:
        llm_budget_monitor.add_memory_segment(
            memory_context,
            MemoryPriority.HIGH,
            'recent',
            compression_ratio=0.2  # Some compression possible
        )
    
    # Add personality context (medium priority)
    if personality_context:
        llm_budget_monitor.add_memory_segment(
            personality_context,
            MemoryPriority.MEDIUM,
            'personality',
            compression_ratio=0.4  # Personality can be compressed
        )
    
    # Optimize context for budget
    optimized_context, final_system_prompt, optimization_info = llm_budget_monitor.optimize_context_for_budget(
        user_input, system_prompt
    )
    
    # Add token definitions if compression was used
    if optimization_info.get('compression_used', False) and llm_budget_monitor.compression_available:
        token_definitions = llm_budget_monitor.tokenizer.generate_token_definitions_block()
        final_system_prompt = final_system_prompt + "\n\n" + token_definitions
    
    # Get budget status for monitoring
    budget_status = llm_budget_monitor.check_budget_status()
    
    budget_info = {
        **optimization_info,
        **budget_status,
        'memory_summary': llm_budget_monitor.get_memory_summary()
    }
    
    logging.info(f"[BudgetMonitor] 📊 Context prepared: {budget_info['final_tokens']} tokens, {budget_info['usage_percent']:.1f}% budget used")
    
    return optimized_context, final_system_prompt, budget_info