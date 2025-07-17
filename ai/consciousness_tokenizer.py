"""
Consciousness Token Compression System
Compresses consciousness states, memory types, and personality states into tokens for 60% token reduction.
"""

import re
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from enum import Enum
from dataclasses import dataclass

class ConsciousnessTokenType(Enum):
    """Types of consciousness tokens"""
    STATE = "state"           # Emotional/mental states
    MEMORY = "memory"         # Memory type markers
    PERSONALITY = "personality"  # Personality traits
    TEMPORAL = "temporal"     # Time-based context
    RELATIONSHIP = "relationship"  # User relationship context

@dataclass
class TokenMapping:
    """Token mapping definition"""
    full_text: str
    token: str
    category: ConsciousnessTokenType
    priority: int  # Higher priority = more important to preserve
    context_hints: List[str]  # Additional context for LLM understanding

class ConsciousnessTokenizer:
    """
    Consciousness Token Compression System
    
    Compresses consciousness states and context into tokens for efficient LLM processing
    while preserving meaning and enabling 60% token reduction.
    """
    
    def __init__(self):
        self.token_mappings: Dict[str, TokenMapping] = {}
        self.reverse_mappings: Dict[str, TokenMapping] = {}
        self._initialize_token_mappings()
        logging.info("[ConsciousnessTokenizer] 🧠 Token compression system initialized")
    
    def _initialize_token_mappings(self):
        """Initialize consciousness token mappings"""
        
        # Consciousness States (emotional/mental)
        state_mappings = [
            ("feeling calm and peaceful", "<CALM>", 8, ["relaxed", "serene", "tranquil"]),
            ("feeling excited and energetic", "<EXCITED>", 7, ["enthusiastic", "animated", "vibrant"]),
            ("currently reflecting and introspective", "<REFLECTING>", 9, ["contemplative", "thoughtful", "analyzing"]),
            ("experiencing uncertainty", "<UNCERTAIN>", 6, ["unsure", "hesitant", "questioning"]),
            ("in a focused analytical state", "<ANALYTICAL>", 8, ["logical", "systematic", "reasoning"]),
            ("feeling empathetic and understanding", "<EMPATHETIC>", 7, ["compassionate", "caring", "supportive"]),
            ("in a creative thinking mode", "<CREATIVE>", 6, ["imaginative", "innovative", "inspired"]),
            ("feeling curious about information", "<CURIOUS>", 7, ["inquisitive", "interested", "exploring"]),
            ("experiencing confusion", "<CONFUSED>", 5, ["perplexed", "unclear", "puzzled"]),
            ("in a helping and supportive mindset", "<HELPFUL>", 8, ["assisting", "guiding", "facilitating"])
        ]
        
        # Memory Types
        memory_mappings = [
            ("recent conversation memory", "<MEM_RECENT>", 9, ["immediate", "current", "latest"]),
            ("emotional and significant memory", "<MEM_EMOTIONAL>", 10, ["meaningful", "important", "feelings"]),
            ("factual information memory", "<MEM_FACTUAL>", 7, ["data", "facts", "information"]),
            ("personal user details memory", "<MEM_PERSONAL>", 9, ["individual", "private", "specific"]),
            ("conversation history memory", "<MEM_HISTORY>", 6, ["past", "previous", "background"]),
            ("contextual situation memory", "<MEM_CONTEXT>", 8, ["situational", "environmental", "setting"]),
            ("belief and preference memory", "<MEM_BELIEFS>", 8, ["values", "opinions", "preferences"]),
            ("temporal and time-based memory", "<MEM_TEMPORAL>", 6, ["chronological", "timeline", "sequence"])
        ]
        
        # Personality States
        personality_mappings = [
            ("friendly and approachable personality", "<FRIENDLY>", 8, ["warm", "welcoming", "sociable"]),
            ("analytical and logical personality", "<ANALYTICAL_P>", 7, ["systematic", "methodical", "rational"]),
            ("empathetic and caring personality", "<EMPATHETIC_P>", 8, ["understanding", "compassionate", "sensitive"]),
            ("curious and inquisitive personality", "<CURIOUS_P>", 7, ["questioning", "exploring", "learning"]),
            ("helpful and supportive personality", "<HELPFUL_P>", 9, ["assisting", "collaborative", "enabling"]),
            ("creative and imaginative personality", "<CREATIVE_P>", 6, ["innovative", "artistic", "original"]),
            ("confident and assured personality", "<CONFIDENT>", 7, ["self-assured", "certain", "decisive"]),
            ("casual and relaxed personality", "<CASUAL>", 7, ["informal", "laid-back", "easy-going"])
        ]
        
        # Temporal Context  
        temporal_mappings = [
            ("in the context of recent events", "<TIME_RECENT>", 7, ["lately", "recently", "current"]),
            ("considering past experiences", "<TIME_PAST>", 6, ["previously", "before", "historical"]),
            ("thinking about future possibilities", "<TIME_FUTURE>", 6, ["upcoming", "potential", "planning"]),
            ("in the immediate present moment", "<TIME_NOW>", 8, ["currently", "right now", "immediate"]),
            ("reflecting on longer-term patterns", "<TIME_PATTERN>", 7, ["trends", "cycles", "recurring"])
        ]
        
        # Relationship Context
        relationship_mappings = [
            ("established trusted relationship", "<REL_TRUSTED>", 9, ["familiar", "known", "reliable"]),
            ("new or developing relationship", "<REL_NEW>", 7, ["getting to know", "introducing", "initial"]),
            ("close personal connection", "<REL_CLOSE>", 8, ["intimate", "personal", "bonded"]),
            ("professional interaction context", "<REL_PROFESSIONAL>", 6, ["formal", "business", "work"]),
            ("casual friendly interaction", "<REL_CASUAL>", 7, ["informal", "relaxed", "buddy"])
        ]
        
        # Combine all mappings
        all_mappings = [
            (text, token, ConsciousnessTokenType.STATE, priority, hints) 
            for text, token, priority, hints in state_mappings
        ] + [
            (text, token, ConsciousnessTokenType.MEMORY, priority, hints)
            for text, token, priority, hints in memory_mappings
        ] + [
            (text, token, ConsciousnessTokenType.PERSONALITY, priority, hints)
            for text, token, priority, hints in personality_mappings
        ] + [
            (text, token, ConsciousnessTokenType.TEMPORAL, priority, hints)
            for text, token, priority, hints in temporal_mappings
        ] + [
            (text, token, ConsciousnessTokenType.RELATIONSHIP, priority, hints)
            for text, token, priority, hints in relationship_mappings
        ]
        
        # Build mappings
        for text, token, category, priority, hints in all_mappings:
            mapping = TokenMapping(text, token, category, priority, hints)
            self.token_mappings[text] = mapping
            self.reverse_mappings[token] = mapping
    
    def compress_consciousness_context(self, consciousness_context: Dict[str, Any]) -> str:
        """
        Compress consciousness context into tokenized form
        
        Args:
            consciousness_context: Dictionary containing consciousness state info
            
        Returns:
            Compressed tokenized consciousness context string
        """
        tokens = []
        
        # Extract and tokenize emotional state
        if 'emotional_state' in consciousness_context:
            emotion = consciousness_context['emotional_state']
            tokens.append(self._find_best_state_token(emotion))
        
        # Extract and tokenize personality traits
        if 'personality_traits' in consciousness_context:
            traits = consciousness_context['personality_traits']
            if isinstance(traits, list):
                for trait in traits[:2]:  # Limit to top 2 traits
                    token = self._find_best_personality_token(trait)
                    if token:
                        tokens.append(token)
        
        # Extract and tokenize memory context
        if 'memory_types' in consciousness_context:
            memory_types = consciousness_context['memory_types']
            if isinstance(memory_types, list):
                for mem_type in memory_types[:3]:  # Limit to top 3 memory types
                    token = self._find_best_memory_token(mem_type)
                    if token:
                        tokens.append(token)
        
        # Extract temporal awareness
        if 'temporal_focus' in consciousness_context:
            temporal = consciousness_context['temporal_focus']
            token = self._find_best_temporal_token(temporal)
            if token:
                tokens.append(token)
        
        # Extract relationship context
        if 'relationship_context' in consciousness_context:
            relationship = consciousness_context['relationship_context']
            token = self._find_best_relationship_token(relationship)
            if token:
                tokens.append(token)
        
        # Join tokens with spaces
        compressed = ' '.join(filter(None, tokens))
        
        logging.debug(f"[ConsciousnessTokenizer] 🧠 Compressed context: {compressed}")
        return compressed
    
    def compress_text_consciousness(self, text: str) -> str:
        """
        Compress consciousness-related text by replacing full descriptions with tokens
        
        Args:
            text: Full text containing consciousness descriptions
            
        Returns:
            Text with consciousness descriptions replaced by tokens
        """
        compressed_text = text
        
        # Sort mappings by length (longest first) to avoid partial replacements
        sorted_mappings = sorted(self.token_mappings.items(), 
                               key=lambda x: len(x[0]), reverse=True)
        
        for full_text, mapping in sorted_mappings:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(full_text) + r'\b'
            compressed_text = re.sub(pattern, mapping.token, compressed_text, flags=re.IGNORECASE)
        
        return compressed_text
    
    def generate_token_definitions_block(self) -> str:
        """
        Generate TOKEN_DEFINITIONS block for LLM understanding
        
        Returns:
            Formatted token definitions for LLM prompt
        """
        definitions = ["TOKEN_DEFINITIONS:"]
        
        # Group by category
        categories = {}
        for token, mapping in self.reverse_mappings.items():
            category = mapping.category.value
            if category not in categories:
                categories[category] = []
            categories[category].append((token, mapping.full_text, mapping.context_hints))
        
        # Format each category
        for category, items in categories.items():
            definitions.append(f"\n{category.upper()} TOKENS:")
            for token, full_text, hints in sorted(items):
                hint_text = f" ({', '.join(hints)})" if hints else ""
                definitions.append(f"  {token} = {full_text}{hint_text}")
        
        definitions.append("\nUse these tokens to understand consciousness context efficiently.")
        return '\n'.join(definitions)
    
    def _find_best_state_token(self, state_description: str) -> Optional[str]:
        """Find best matching state token"""
        return self._find_best_token(state_description, ConsciousnessTokenType.STATE)
    
    def _find_best_personality_token(self, trait_description: str) -> Optional[str]:
        """Find best matching personality token"""
        return self._find_best_token(trait_description, ConsciousnessTokenType.PERSONALITY)
    
    def _find_best_memory_token(self, memory_description: str) -> Optional[str]:
        """Find best matching memory token"""
        return self._find_best_token(memory_description, ConsciousnessTokenType.MEMORY)
    
    def _find_best_temporal_token(self, temporal_description: str) -> Optional[str]:
        """Find best matching temporal token"""
        return self._find_best_token(temporal_description, ConsciousnessTokenType.TEMPORAL)
    
    def _find_best_relationship_token(self, relationship_description: str) -> Optional[str]:
        """Find best matching relationship token"""
        return self._find_best_token(relationship_description, ConsciousnessTokenType.RELATIONSHIP)
    
    def _find_best_token(self, description: str, token_type: ConsciousnessTokenType) -> Optional[str]:
        """Find best matching token for description and type"""
        if not description:
            return None
        
        description_lower = description.lower()
        best_match = None
        best_score = 0
        
        for mapping in self.token_mappings.values():
            if mapping.category != token_type:
                continue
            
            # Check for keyword matches
            score = 0
            
            # Check full text match
            if mapping.full_text.lower() in description_lower:
                score += 10
            
            # Check context hints
            for hint in mapping.context_hints:
                if hint.lower() in description_lower:
                    score += 3
            
            # Check individual words from the mapping
            mapping_words = mapping.full_text.lower().split()
            for word in mapping_words:
                if len(word) > 3 and word in description_lower:  # Only count meaningful words
                    score += 1
            
            # Prefer higher priority tokens when scores are equal
            if score > 0:
                score += mapping.priority * 0.1
            
            if score > best_score:
                best_score = score
                best_match = mapping.token
        
        return best_match
    
    def estimate_compression_ratio(self, original_text: str) -> float:
        """
        Estimate compression ratio achieved
        
        Args:
            original_text: Original uncompressed text
            
        Returns:
            Compression ratio (0.0 to 1.0, where 0.6 = 60% reduction)
        """
        compressed_text = self.compress_text_consciousness(original_text)
        
        original_length = len(original_text)
        compressed_length = len(compressed_text)
        
        if original_length == 0:
            return 0.0
        
        compression_ratio = 1.0 - (compressed_length / original_length)
        return compression_ratio
    
    def get_token_count_estimate(self, text: str) -> int:
        """
        Estimate token count for text (rough approximation: 1 token ≈ 4 characters)
        
        Args:
            text: Text to estimate
            
        Returns:
            Estimated token count
        """
        return len(text) // 4

# Global tokenizer instance
consciousness_tokenizer = ConsciousnessTokenizer()

def compress_consciousness_for_llm(consciousness_context: Dict[str, Any], 
                                 memory_context: str = "", 
                                 personality_context: str = "") -> Tuple[str, str]:
    """
    Compress consciousness context for LLM prompt inclusion
    
    Args:
        consciousness_context: Current consciousness state
        memory_context: Memory context text 
        personality_context: Personality context text
        
    Returns:
        Tuple of (compressed_context, token_definitions)
    """
    # Compress the consciousness context
    compressed_consciousness = consciousness_tokenizer.compress_consciousness_context(consciousness_context)
    
    # Compress text-based contexts
    compressed_memory = consciousness_tokenizer.compress_text_consciousness(memory_context)
    compressed_personality = consciousness_tokenizer.compress_text_consciousness(personality_context)
    
    # Combine compressed contexts
    contexts = [compressed_consciousness, compressed_memory, compressed_personality]
    combined_context = ' '.join(filter(None, contexts))
    
    # Generate token definitions for LLM understanding
    token_definitions = consciousness_tokenizer.generate_token_definitions_block()
    
    return combined_context, token_definitions