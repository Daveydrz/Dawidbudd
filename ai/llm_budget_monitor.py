"""
LLM Prompt Budget Monitor

This module monitors token usage in LLM prompts and automatically manages
memory trimming to prevent token overflow while preserving important context.
"""

import re
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

class MemoryPriority(Enum):
    """Memory priority levels for budget management"""
    CRITICAL = 10      # Never trim (current emotional context, consciousness state)
    HIGH = 8          # Trim only when desperate (recent significant events)
    MEDIUM = 6        # Trim when space needed (personal facts, preferences)
    LOW = 4           # Trim early (old conversations, routine interactions)
    EXPENDABLE = 2    # Trim first (duplicate info, low-value memories)

@dataclass
class MemoryItem:
    """A memory item with priority and metadata"""
    content: str
    priority: MemoryPriority
    timestamp: datetime
    category: str
    emotional_weight: float = 0.5
    token_estimate: int = 0
    tags: List[str] = field(default_factory=list)

@dataclass
class BudgetAllocation:
    """Token budget allocation for different prompt components"""
    system_message: int = 200       # Base system message
    consciousness_state: int = 150  # Current consciousness
    memory_context: int = 800       # User memories and context
    conversation_history: int = 400 # Recent conversation
    user_input: int = 100          # Current user message
    response_buffer: int = 150     # Buffer for response generation
    safety_margin: int = 50        # Safety margin for variations

class LLMBudgetMonitor:
    """
    Monitors and manages token budget for LLM prompts to prevent overflow
    while intelligently preserving the most important context.
    """
    
    def __init__(self, max_tokens: int = 8000, target_utilization: float = 0.9):
        self.max_tokens = max_tokens
        self.target_utilization = target_utilization
        self.target_tokens = int(max_tokens * target_utilization)  # 7200 for 8k model
        
        self.budget_allocation = BudgetAllocation()
        self.memory_items: List[MemoryItem] = []
        
        # Token estimation patterns (approximate)
        self.token_patterns = {
            # English text approximation: ~4 chars per token
            'english_ratio': 4.0,
            # Code/structured data: ~3 chars per token  
            'code_ratio': 3.0,
            # Consciousness tokens: ~1 token per compressed token
            'consciousness_token_ratio': 1.0
        }
        
        # Statistics
        self.stats = {
            'total_requests': 0,
            'trimming_events': 0,
            'tokens_trimmed': 0,
            'memory_items_trimmed': 0,
            'fallback_activations': 0
        }
        
        logging.info(f"[LLMBudgetMonitor] 💰 Budget monitor initialized: {max_tokens} max tokens, {self.target_tokens} target")
    
    def estimate_tokens(self, text: str, content_type: str = "english") -> int:
        """
        Estimate token count for text based on content type
        
        Args:
            text: Text to estimate
            content_type: Type of content ("english", "code", "consciousness_tokens")
            
        Returns:
            Estimated token count
        """
        if not text:
            return 0
        
        # Handle consciousness tokens specially
        if content_type == "consciousness_tokens":
            consciousness_tokens = re.findall(r'<[A-Z_]+>', text)
            return len(consciousness_tokens)
        
        # Use appropriate ratio for estimation
        if content_type == "code":
            ratio = self.token_patterns['code_ratio']
        else:
            ratio = self.token_patterns['english_ratio']
        
        # Basic estimation: character count / ratio
        base_estimate = len(text) / ratio
        
        # Adjust for common token patterns
        # Punctuation and short words are often 1 token
        words = len(text.split())
        punctuation = len(re.findall(r'[.!?,:;]', text))
        
        # Use the higher estimate (conservative approach)
        word_based_estimate = words * 1.3  # Average 1.3 tokens per word
        
        return int(max(base_estimate, word_based_estimate))
    
    def add_memory_item(self, content: str, priority: MemoryPriority, 
                       category: str, emotional_weight: float = 0.5,
                       tags: List[str] = None) -> MemoryItem:
        """
        Add a memory item to the budget tracking
        
        Args:
            content: Memory content
            priority: Priority level
            category: Memory category
            emotional_weight: Emotional significance (0-1)
            tags: Optional tags for categorization
            
        Returns:
            Created memory item
        """
        if tags is None:
            tags = []
        
        item = MemoryItem(
            content=content,
            priority=priority,
            timestamp=datetime.now(),
            category=category,
            emotional_weight=emotional_weight,
            token_estimate=self.estimate_tokens(content),
            tags=tags
        )
        
        self.memory_items.append(item)
        
        # Keep memory items sorted by priority and recency
        self.memory_items.sort(key=lambda x: (x.priority.value, x.timestamp), reverse=True)
        
        return item
    
    def build_prompt_with_budget(self, 
                                system_message: str,
                                consciousness_state: str,
                                user_input: str,
                                memory_context: str = "",
                                conversation_history: str = "",
                                use_consciousness_tokens: bool = True) -> Tuple[str, Dict[str, Any]]:
        """
        Build a prompt within token budget, automatically trimming if necessary
        
        Args:
            system_message: System prompt
            consciousness_state: Current consciousness state
            user_input: User's message
            memory_context: Memory context (will be trimmed if needed)
            conversation_history: Recent conversation (will be trimmed if needed)
            use_consciousness_tokens: Whether to use compressed consciousness tokens
            
        Returns:
            Tuple of (final_prompt, budget_info)
        """
        self.stats['total_requests'] += 1
        
        # Estimate token usage for fixed components
        system_tokens = self.estimate_tokens(system_message)
        user_input_tokens = self.estimate_tokens(user_input)
        
        # Handle consciousness state (potentially compressed)
        if use_consciousness_tokens:
            consciousness_tokens = self.estimate_tokens(consciousness_state, "consciousness_tokens")
        else:
            consciousness_tokens = self.estimate_tokens(consciousness_state)
        
        # Calculate available space for variable content
        fixed_tokens = (system_tokens + consciousness_tokens + user_input_tokens + 
                       self.budget_allocation.response_buffer + 
                       self.budget_allocation.safety_margin)
        
        available_tokens = self.target_tokens - fixed_tokens
        
        # Distribute available tokens between memory and conversation
        memory_allocation = int(available_tokens * 0.65)  # 65% for memory
        conversation_allocation = available_tokens - memory_allocation
        
        # Trim memory context if needed
        trimmed_memory, memory_trimming_info = self._trim_text_to_budget(
            memory_context, memory_allocation, "memory"
        )
        
        # Trim conversation history if needed
        trimmed_conversation, conversation_trimming_info = self._trim_text_to_budget(
            conversation_history, conversation_allocation, "conversation"
        )
        
        # Build final prompt
        prompt_parts = []
        
        if system_message:
            prompt_parts.append(system_message)
        
        if consciousness_state:
            prompt_parts.append(f"Consciousness State: {consciousness_state}")
        
        if trimmed_memory:
            prompt_parts.append(f"Memory Context: {trimmed_memory}")
        
        if trimmed_conversation:
            prompt_parts.append(f"Recent Conversation: {trimmed_conversation}")
        
        if user_input:
            prompt_parts.append(f"User: {user_input}")
        
        final_prompt = "\n\n".join(prompt_parts)
        final_tokens = self.estimate_tokens(final_prompt)
        
        # Compile budget information
        budget_info = {
            'total_tokens': final_tokens,
            'max_tokens': self.max_tokens,
            'target_tokens': self.target_tokens,
            'utilization': final_tokens / self.max_tokens,
            'within_budget': final_tokens <= self.target_tokens,
            'components': {
                'system_message': system_tokens,
                'consciousness_state': consciousness_tokens,
                'memory_context': self.estimate_tokens(trimmed_memory),
                'conversation_history': self.estimate_tokens(trimmed_conversation),
                'user_input': user_input_tokens
            },
            'trimming': {
                'memory_trimmed': memory_trimming_info['trimmed'],
                'conversation_trimmed': conversation_trimming_info['trimmed'],
                'memory_reduction': memory_trimming_info.get('reduction_ratio', 0),
                'conversation_reduction': conversation_trimming_info.get('reduction_ratio', 0)
            },
            'fallback_needed': final_tokens > self.target_tokens
        }
        
        # Handle fallback if still over budget
        if final_tokens > self.target_tokens:
            final_prompt, budget_info = self._emergency_fallback(
                final_prompt, budget_info, use_consciousness_tokens
            )
        
        logging.info(f"[LLMBudgetMonitor] 📊 Prompt built: {final_tokens}/{self.target_tokens} tokens ({budget_info['utilization']:.1%})")
        
        return final_prompt, budget_info
    
    def _trim_text_to_budget(self, text: str, budget: int, content_type: str) -> Tuple[str, Dict[str, Any]]:
        """
        Trim text to fit within token budget intelligently
        
        Args:
            text: Text to trim
            budget: Token budget
            content_type: Type of content for trimming strategy
            
        Returns:
            Tuple of (trimmed_text, trimming_info)
        """
        if not text:
            return "", {"trimmed": False, "original_tokens": 0, "final_tokens": 0}
        
        original_tokens = self.estimate_tokens(text)
        
        if original_tokens <= budget:
            return text, {
                "trimmed": False,
                "original_tokens": original_tokens,
                "final_tokens": original_tokens,
                "reduction_ratio": 0
            }
        
        self.stats['trimming_events'] += 1
        
        # Trimming strategy based on content type
        if content_type == "memory":
            trimmed_text = self._trim_memory_content(text, budget)
        elif content_type == "conversation":
            trimmed_text = self._trim_conversation_content(text, budget)
        else:
            trimmed_text = self._trim_generic_content(text, budget)
        
        final_tokens = self.estimate_tokens(trimmed_text)
        tokens_saved = original_tokens - final_tokens
        
        self.stats['tokens_trimmed'] += tokens_saved
        
        return trimmed_text, {
            "trimmed": True,
            "original_tokens": original_tokens,
            "final_tokens": final_tokens,
            "tokens_saved": tokens_saved,
            "reduction_ratio": tokens_saved / original_tokens if original_tokens > 0 else 0
        }
    
    def _trim_memory_content(self, memory_text: str, budget: int) -> str:
        """
        Intelligently trim memory content preserving most important information
        """
        lines = memory_text.split('\n')
        
        # Prioritize lines by importance indicators
        prioritized_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            priority = self._assess_line_priority(line)
            tokens = self.estimate_tokens(line)
            
            prioritized_lines.append((priority, tokens, line))
        
        # Sort by priority (higher first)
        prioritized_lines.sort(reverse=True)
        
        # Build result within budget
        result_lines = []
        used_tokens = 0
        
        for priority, tokens, line in prioritized_lines:
            if used_tokens + tokens <= budget:
                result_lines.append(line)
                used_tokens += tokens
            else:
                # Try to fit a truncated version of high-priority lines
                if priority >= 8 and used_tokens < budget:
                    remaining_budget = budget - used_tokens
                    truncated_line = self._truncate_line_to_budget(line, remaining_budget)
                    if truncated_line:
                        result_lines.append(truncated_line)
                break
        
        return '\n'.join(result_lines)
    
    def _trim_conversation_content(self, conversation_text: str, budget: int) -> str:
        """
        Trim conversation history starting from oldest entries
        """
        lines = conversation_text.split('\n')
        
        # Calculate tokens per line
        line_tokens = [(line, self.estimate_tokens(line)) for line in lines if line.strip()]
        
        # Start from the most recent and work backwards
        result_lines = []
        used_tokens = 0
        
        for line, tokens in reversed(line_tokens):
            if used_tokens + tokens <= budget:
                result_lines.insert(0, line)  # Insert at beginning to maintain order
                used_tokens += tokens
            else:
                break
        
        return '\n'.join(result_lines)
    
    def _trim_generic_content(self, text: str, budget: int) -> str:
        """
        Generic text trimming - truncate from the end
        """
        if self.estimate_tokens(text) <= budget:
            return text
        
        # Estimate target character count
        target_chars = int(budget * self.token_patterns['english_ratio'])
        
        if len(text) <= target_chars:
            return text
        
        # Truncate and try to end at a sentence boundary
        truncated = text[:target_chars]
        
        # Find last sentence boundary
        last_period = truncated.rfind('.')
        last_newline = truncated.rfind('\n')
        boundary = max(last_period, last_newline)
        
        if boundary > target_chars * 0.8:  # If boundary is not too far back
            return truncated[:boundary + 1]
        else:
            return truncated + "..."
    
    def _assess_line_priority(self, line: str) -> int:
        """
        Assess the priority of a memory line (1-10)
        """
        line_lower = line.lower()
        
        # Critical emotional context
        if any(word in line_lower for word in ['died', 'death', 'passed away', 'grief', 'loss']):
            return 10
        
        # High emotional significance
        if any(word in line_lower for word in ['love', 'hate', 'fear', 'anxiety', 'depression', 'joy']):
            return 9
        
        # Recent temporal markers
        if any(word in line_lower for word in ['today', 'yesterday', 'recently', 'just', 'now']):
            return 8
        
        # Personal facts
        if any(word in line_lower for word in ['my', 'i am', 'i have', 'i work', 'i live']):
            return 7
        
        # Relationships
        if any(word in line_lower for word in ['family', 'friend', 'partner', 'spouse', 'child']):
            return 6
        
        # Basic preferences
        if any(word in line_lower for word in ['like', 'dislike', 'prefer', 'enjoy']):
            return 5
        
        # Factual information
        if any(word in line_lower for word in ['fact', 'information', 'knows']):
            return 4
        
        # General conversation
        return 3
    
    def _truncate_line_to_budget(self, line: str, budget: int) -> str:
        """
        Truncate a single line to fit within budget
        """
        if self.estimate_tokens(line) <= budget:
            return line
        
        target_chars = int(budget * self.token_patterns['english_ratio'])
        
        if len(line) <= target_chars:
            return line
        
        # Try to truncate at word boundary
        truncated = line[:target_chars]
        last_space = truncated.rfind(' ')
        
        if last_space > target_chars * 0.7:
            return truncated[:last_space] + "..."
        else:
            return truncated + "..."
    
    def _emergency_fallback(self, prompt: str, budget_info: Dict[str, Any], 
                           use_consciousness_tokens: bool) -> Tuple[str, Dict[str, Any]]:
        """
        Emergency fallback when prompt is still over budget
        """
        self.stats['fallback_activations'] += 1
        
        logging.warning(f"[LLMBudgetMonitor] ⚠️ Emergency fallback activated")
        
        # If not already using consciousness tokens, switch to them
        if not use_consciousness_tokens:
            # This would require re-processing with consciousness tokens
            # For now, just log and proceed with aggressive trimming
            logging.info("[LLMBudgetMonitor] 🧠 Switching to consciousness tokens in fallback")
        
        # Aggressive trimming - cut everything by 30%
        lines = prompt.split('\n')
        target_lines = int(len(lines) * 0.7)
        
        # Keep the most important lines (system message, consciousness, user input)
        important_prefixes = ['System:', 'Consciousness State:', 'User:']
        important_lines = []
        other_lines = []
        
        for line in lines:
            if any(line.startswith(prefix) for prefix in important_prefixes):
                important_lines.append(line)
            else:
                other_lines.append(line)
        
        # Keep all important lines and some other lines
        remaining_budget = target_lines - len(important_lines)
        selected_other_lines = other_lines[:max(0, remaining_budget)]
        
        final_lines = important_lines + selected_other_lines
        fallback_prompt = '\n'.join(final_lines)
        
        budget_info['fallback_applied'] = True
        budget_info['total_tokens'] = self.estimate_tokens(fallback_prompt)
        budget_info['utilization'] = budget_info['total_tokens'] / self.max_tokens
        
        return fallback_prompt, budget_info
    
    def trim_memory_by_priority(self, memory_items: List[str], 
                               priorities: List[MemoryPriority],
                               target_budget: int) -> Tuple[List[str], Dict[str, Any]]:
        """
        Trim memory items by priority to fit within budget
        
        Args:
            memory_items: List of memory content strings
            priorities: List of corresponding priorities
            target_budget: Target token budget
            
        Returns:
            Tuple of (trimmed_items, trimming_stats)
        """
        if not memory_items:
            return [], {"items_removed": 0, "tokens_saved": 0}
        
        # Create prioritized list
        prioritized_items = list(zip(memory_items, priorities))
        prioritized_items.sort(key=lambda x: x[1].value, reverse=True)
        
        # Select items within budget
        selected_items = []
        used_tokens = 0
        items_removed = 0
        
        for content, priority in prioritized_items:
            tokens = self.estimate_tokens(content)
            
            if used_tokens + tokens <= target_budget:
                selected_items.append(content)
                used_tokens += tokens
            else:
                items_removed += 1
        
        original_tokens = sum(self.estimate_tokens(item) for item in memory_items)
        tokens_saved = original_tokens - used_tokens
        
        self.stats['memory_items_trimmed'] += items_removed
        
        trimming_stats = {
            "items_removed": items_removed,
            "tokens_saved": tokens_saved,
            "original_count": len(memory_items),
            "final_count": len(selected_items),
            "original_tokens": original_tokens,
            "final_tokens": used_tokens
        }
        
        return selected_items, trimming_stats
    
    def get_budget_status(self) -> Dict[str, Any]:
        """Get current budget monitor status and statistics"""
        return {
            'configuration': {
                'max_tokens': self.max_tokens,
                'target_tokens': self.target_tokens,
                'target_utilization': self.target_utilization
            },
            'statistics': self.stats.copy(),
            'memory_items_tracked': len(self.memory_items),
            'budget_allocation': {
                'system_message': self.budget_allocation.system_message,
                'consciousness_state': self.budget_allocation.consciousness_state,
                'memory_context': self.budget_allocation.memory_context,
                'conversation_history': self.budget_allocation.conversation_history,
                'user_input': self.budget_allocation.user_input,
                'response_buffer': self.budget_allocation.response_buffer,
                'safety_margin': self.budget_allocation.safety_margin
            }
        }
    
    def reset_stats(self):
        """Reset statistics counters"""
        self.stats = {
            'total_requests': 0,
            'trimming_events': 0,
            'tokens_trimmed': 0,
            'memory_items_trimmed': 0,
            'fallback_activations': 0
        }

# Global budget monitor instance
budget_monitor = LLMBudgetMonitor()

def monitor_prompt_budget(system_message: str, consciousness_state: str, 
                         user_input: str, memory_context: str = "",
                         conversation_history: str = "",
                         max_tokens: int = 8000) -> Tuple[str, Dict[str, Any]]:
    """
    Convenience function to build a prompt within token budget
    
    Args:
        system_message: System prompt
        consciousness_state: Current consciousness state
        user_input: User's message
        memory_context: Memory context
        conversation_history: Recent conversation
        max_tokens: Maximum token limit
        
    Returns:
        Tuple of (final_prompt, budget_info)
    """
    global budget_monitor
    
    # Update budget monitor if different max_tokens
    if max_tokens != budget_monitor.max_tokens:
        budget_monitor = LLMBudgetMonitor(max_tokens)
    
    return budget_monitor.build_prompt_with_budget(
        system_message=system_message,
        consciousness_state=consciousness_state,
        user_input=user_input,
        memory_context=memory_context,
        conversation_history=conversation_history,
        use_consciousness_tokens=True
    )

def get_budget_stats() -> Dict[str, Any]:
    """Get global budget monitor statistics"""
    return budget_monitor.get_budget_status()

logging.info("[LLMBudgetMonitor] 💰 LLM budget monitor module loaded")
print("[LLMBudgetMonitor] ✅ LLM Prompt Budget Monitor: LOADED")
print("[LLMBudgetMonitor] 🎯 Target: Prevent token overflow, maintain conversation flow")
print("[LLMBudgetMonitor] 📊 Auto-trim: Oldest memories when approaching limits")
print("[LLMBudgetMonitor] 🛡️ Priority system: Preserve emotional context & consciousness state")