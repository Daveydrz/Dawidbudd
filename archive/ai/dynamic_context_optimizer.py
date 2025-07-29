#!/usr/bin/env python3
"""
Dynamic Context Optimizer - Smart Prompt and Context Management for Performance
Created: 2025-01-18
Purpose: Dynamically trim context and optimize prompts to reduce token usage
        while maintaining response quality.
"""

import re
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass

@dataclass
class ContextOptimization:
    """Context optimization settings"""
    max_tokens: int = 2000
    priority_weight: float = 1.0
    compression_ratio: float = 0.7
    keep_recent_turns: int = 5
    keep_important_memories: int = 10

class DynamicContextOptimizer:
    """
    Intelligently manages context and prompt tokens for performance
    """
    
    def __init__(self):
        self.optimization_stats = {
            "total_optimizations": 0,
            "tokens_saved": 0,
            "compression_ratio": 0.0
        }
        
        # Priority keywords for keeping important context
        self.high_priority_keywords = [
            "remember", "important", "never forget", "always", "promise",
            "love", "hate", "birthday", "anniversary", "family", "friend",
            "emergency", "critical", "urgent", "help", "problem"
        ]
        
        self.medium_priority_keywords = [
            "like", "dislike", "prefer", "favorite", "enjoy", "hobby",
            "work", "job", "school", "study", "live", "home", "address"
        ]
        
        logging.info("[ContextOptimizer] 🎯 Dynamic context optimizer initialized")
    
    def optimize_conversation_context(self, conversation_history: List[Dict], 
                                    current_question: str,
                                    max_tokens: int = 2000) -> Tuple[str, Dict[str, Any]]:
        """
        Optimize conversation context to fit within token limits
        
        Args:
            conversation_history: List of conversation turns
            current_question: Current user question
            max_tokens: Maximum tokens allowed
            
        Returns:
            Tuple of (optimized_context, optimization_info)
        """
        
        # Estimate current token usage (rough approximation: 1 token ≈ 4 characters)
        def estimate_tokens(text: str) -> int:
            return len(text) // 4
        
        total_tokens = estimate_tokens(current_question)
        optimization_info = {
            "original_turns": len(conversation_history),
            "original_tokens": total_tokens,
            "kept_turns": 0,
            "compression_applied": False
        }
        
        if not conversation_history:
            return "", optimization_info
        
        # ✅ PERFORMANCE: Prioritize recent and important conversations
        prioritized_turns = self._prioritize_conversation_turns(conversation_history, current_question)
        
        optimized_turns = []
        
        for turn in prioritized_turns:
            turn_text = self._format_conversation_turn(turn)
            turn_tokens = estimate_tokens(turn_text)
            
            if total_tokens + turn_tokens <= max_tokens:
                optimized_turns.append(turn_text)
                total_tokens += turn_tokens
                optimization_info["kept_turns"] += 1
            else:
                # Try compressed version
                compressed_turn = self._compress_conversation_turn(turn)
                compressed_tokens = estimate_tokens(compressed_turn)
                
                if total_tokens + compressed_tokens <= max_tokens:
                    optimized_turns.append(compressed_turn)
                    total_tokens += compressed_tokens
                    optimization_info["kept_turns"] += 1
                    optimization_info["compression_applied"] = True
                else:
                    # Skip this turn if it won't fit
                    break
        
        # Create optimized context
        optimized_context = "\n".join(optimized_turns)
        
        optimization_info["final_context"] = optimized_context
        optimization_info["final_tokens"] = estimate_tokens(optimized_context)
        optimization_info["tokens_saved"] = optimization_info["original_tokens"] - optimization_info["final_tokens"]
        
        # Update stats
        self.optimization_stats["total_optimizations"] += 1
        self.optimization_stats["tokens_saved"] += optimization_info["tokens_saved"]
        
        if optimization_info["original_tokens"] > 0:
            compression_ratio = optimization_info["final_tokens"] / optimization_info["original_tokens"]
            self.optimization_stats["compression_ratio"] = compression_ratio
        
        logging.debug(f"[ContextOptimizer] 🎯 Optimized: {optimization_info['original_turns']} → {optimization_info['kept_turns']} turns, saved {optimization_info['tokens_saved']} tokens")
        
        return optimized_context, optimization_info
    
    def _prioritize_conversation_turns(self, conversation_history: List[Dict], 
                                     current_question: str) -> List[Dict]:
        """Prioritize conversation turns by importance and recency"""
        
        def calculate_priority(turn: Dict, index: int) -> float:
            """Calculate priority score for a conversation turn"""
            priority = 0.0
            turn_text = str(turn.get('human', '')) + ' ' + str(turn.get('ai', ''))
            
            # Recency bonus (more recent = higher priority)
            recency_bonus = (index / len(conversation_history)) * 2.0
            priority += recency_bonus
            
            # High priority keywords
            for keyword in self.high_priority_keywords:
                if keyword.lower() in turn_text.lower():
                    priority += 3.0
            
            # Medium priority keywords  
            for keyword in self.medium_priority_keywords:
                if keyword.lower() in turn_text.lower():
                    priority += 1.5
            
            # Relevance to current question
            current_words = set(current_question.lower().split())
            turn_words = set(turn_text.lower().split())
            relevance = len(current_words.intersection(turn_words)) / max(len(current_words), 1)
            priority += relevance * 2.0
            
            # Length penalty (very long turns get lower priority unless they're recent)
            if len(turn_text) > 500 and index < len(conversation_history) * 0.8:
                priority -= 1.0
            
            return priority
        
        # Calculate priorities
        prioritized = []
        for i, turn in enumerate(conversation_history):
            priority = calculate_priority(turn, i)
            prioritized.append((priority, turn))
        
        # Sort by priority (highest first)
        prioritized.sort(key=lambda x: x[0], reverse=True)
        
        # Return just the turns
        return [turn for priority, turn in prioritized]
    
    def _format_conversation_turn(self, turn: Dict) -> str:
        """Format a conversation turn for context"""
        human_text = turn.get('human', '')
        ai_text = turn.get('ai', '')
        
        formatted = ""
        if human_text:
            formatted += f"Human: {human_text}\n"
        if ai_text:
            formatted += f"Assistant: {ai_text}\n"
        
        return formatted.strip()
    
    def _compress_conversation_turn(self, turn: Dict) -> str:
        """Compress a conversation turn to reduce tokens"""
        human_text = turn.get('human', '')
        ai_text = turn.get('ai', '')
        
        # Compress by summarizing key points
        compressed_human = self._compress_text(human_text, max_length=50)
        compressed_ai = self._compress_text(ai_text, max_length=100)
        
        formatted = ""
        if compressed_human:
            formatted += f"H: {compressed_human}\n"
        if compressed_ai:
            formatted += f"A: {compressed_ai}\n"
        
        return formatted.strip()
    
    def _compress_text(self, text: str, max_length: int = 100) -> str:
        """Compress text while preserving key information"""
        if not text or len(text) <= max_length:
            return text
        
        # Try to preserve important sentences
        sentences = re.split(r'[.!?]+', text)
        
        # Prioritize sentences with important keywords
        prioritized_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            priority = 0
            for keyword in self.high_priority_keywords:
                if keyword.lower() in sentence.lower():
                    priority += 2
            for keyword in self.medium_priority_keywords:
                if keyword.lower() in sentence.lower():
                    priority += 1
            
            prioritized_sentences.append((priority, sentence))
        
        # Sort by priority
        prioritized_sentences.sort(key=lambda x: x[0], reverse=True)
        
        # Build compressed text
        compressed = ""
        for priority, sentence in prioritized_sentences:
            if len(compressed) + len(sentence) <= max_length:
                if compressed:
                    compressed += ". "
                compressed += sentence
            else:
                break
        
        # If still too long, truncate with ellipsis
        if len(compressed) > max_length:
            compressed = compressed[:max_length-3] + "..."
        
        return compressed
    
    def optimize_memory_context(self, memories: List[str], 
                               current_question: str,
                               max_memories: int = 10) -> List[str]:
        """Optimize memory context by selecting most relevant memories"""
        
        if len(memories) <= max_memories:
            return memories
        
        # Score memories by relevance to current question
        current_words = set(current_question.lower().split())
        scored_memories = []
        
        for memory in memories:
            memory_words = set(memory.lower().split())
            
            # Relevance score
            relevance = len(current_words.intersection(memory_words)) / max(len(current_words), 1)
            
            # Priority keyword bonus
            priority_bonus = 0
            for keyword in self.high_priority_keywords:
                if keyword.lower() in memory.lower():
                    priority_bonus += 2
            for keyword in self.medium_priority_keywords:
                if keyword.lower() in memory.lower():
                    priority_bonus += 1
            
            total_score = relevance + priority_bonus
            scored_memories.append((total_score, memory))
        
        # Sort by score and take top memories
        scored_memories.sort(key=lambda x: x[0], reverse=True)
        optimized_memories = [memory for score, memory in scored_memories[:max_memories]]
        
        logging.debug(f"[ContextOptimizer] 🧠 Optimized memories: {len(memories)} → {len(optimized_memories)}")
        
        return optimized_memories
    
    def create_optimized_prompt(self, base_prompt: str, 
                              context: str,
                              max_tokens: int = 3000) -> str:
        """Create an optimized prompt that fits within token limits"""
        
        def estimate_tokens(text: str) -> int:
            return len(text) // 4
        
        base_tokens = estimate_tokens(base_prompt)
        context_tokens = estimate_tokens(context)
        total_tokens = base_tokens + context_tokens
        
        if total_tokens <= max_tokens:
            return f"{context}\n\n{base_prompt}"
        
        # Need to compress context
        available_context_tokens = max_tokens - base_tokens - 50  # 50 token buffer
        
        if available_context_tokens <= 0:
            # Base prompt is too long, use minimal context
            return base_prompt
        
        # Compress context to fit
        target_context_length = available_context_tokens * 4  # Convert tokens to chars
        
        if len(context) > target_context_length:
            # Truncate context intelligently
            sentences = re.split(r'[.!?]+', context)
            compressed_context = ""
            
            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence:
                    continue
                    
                if len(compressed_context) + len(sentence) + 2 <= target_context_length:
                    if compressed_context:
                        compressed_context += ". "
                    compressed_context += sentence
                else:
                    break
            
            context = compressed_context
        
        optimized_prompt = f"{context}\n\n{base_prompt}"
        
        logging.debug(f"[ContextOptimizer] 📝 Optimized prompt: {total_tokens} → {estimate_tokens(optimized_prompt)} tokens")
        
        return optimized_prompt
    
    def get_optimization_stats(self) -> Dict[str, Any]:
        """Get optimization statistics"""
        return {
            **self.optimization_stats,
            "average_compression": self.optimization_stats.get("compression_ratio", 0.0),
            "total_tokens_saved": self.optimization_stats.get("tokens_saved", 0)
        }

# Global instance
dynamic_context_optimizer = DynamicContextOptimizer()