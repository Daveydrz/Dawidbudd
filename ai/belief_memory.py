"""
Belief and Memory System - Unified Belief and Memory Subsystem

This consolidated module combines belief and memory management:
- Manages conversation history and context awareness  
- Handles user-specific long-term context and belief systems
- Provides memory persistence and retrieval
- Tracks emotional impact and entity relationships

Consolidated from:
- memory.py - Conversation history and context management
"""

import time
import json
import datetime
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from config import MAX_HISTORY_LENGTH, DEBUG
from enum import Enum

# Import entropy system if available
try:
    from ai.entropy_engine import get_entropy_engine, probabilistic_select, inject_consciousness_entropy, EntropyLevel
    ENTROPY_AVAILABLE = True
except ImportError as e:
    ENTROPY_AVAILABLE = False

# Enhanced settings with fallbacks
try:
    from config import (ENHANCED_CONVERSATION_MEMORY, CONVERSATION_MEMORY_LENGTH, 
                       CONVERSATION_CONTEXT_LENGTH, CONVERSATION_SUMMARY_ENABLED,
                       CONVERSATION_SUMMARY_THRESHOLD, TOPIC_TRACKING_ENABLED,
                       MAX_CONVERSATION_TOPICS, CONTEXT_COMPRESSION_ENABLED,
                       MAX_CONTEXT_TOKENS)
except ImportError:
    ENHANCED_CONVERSATION_MEMORY = True
    CONVERSATION_MEMORY_LENGTH = 25
    CONVERSATION_CONTEXT_LENGTH = 10
    CONVERSATION_SUMMARY_ENABLED = True
    CONVERSATION_SUMMARY_THRESHOLD = 18
    TOPIC_TRACKING_ENABLED = True
    MAX_CONVERSATION_TOPICS = 6
    CONTEXT_COMPRESSION_ENABLED = True
    MAX_CONTEXT_TOKENS = 1500

class EntityStatus(Enum):
    """Track current status of entities"""
    CURRENT = "current"
    FORMER = "former"
    DECEASED = "deceased"
    SOLD = "sold"
    LOST = "lost"
    ENDED = "ended"
    UNKNOWN = "unknown"

class EmotionalImpact(Enum):
    """Emotional impact levels"""
    VERY_POSITIVE = "very_positive"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    VERY_NEGATIVE = "very_negative"

@dataclass
class ConversationEntry:
    """Individual conversation entry"""
    timestamp: str
    user_input: str
    ai_response: str
    context: Dict[str, Any]
    emotional_tone: str = "neutral"
    topics: List[str] = None
    
    def __post_init__(self):
        if self.topics is None:
            self.topics = []

@dataclass
class BeliefEntry:
    """Individual belief entry"""
    belief: str
    confidence: float
    source: str
    timestamp: str
    context: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.context is None:
            self.context = {}

class UnifiedBeliefMemorySystem:
    """
    Unified belief and memory management system.
    
    This system combines functionality for:
    - Conversation history and context management
    - User-specific belief tracking and evolution
    - Memory persistence and intelligent retrieval
    - Emotional context and relationship mapping
    """
    
    def __init__(self, memory_file: str = "belief_memory.json"):
        self.memory_file = memory_file
        self.conversation_history: List[ConversationEntry] = []
        self.user_beliefs: Dict[str, List[BeliefEntry]] = {}
        self.user_context: Dict[str, Dict[str, Any]] = {}
        self.topic_memory: Dict[str, List[str]] = {}
        self.emotional_history: List[Dict[str, Any]] = []
        
        # Load existing memory
        self.load_memory()
        
        print("[UnifiedBeliefMemory] 🧠 Unified belief and memory system initialized")
    
    def add_to_conversation_history(self, user_input: str, ai_response: str, 
                                  user_id: str = "default", context: Dict[str, Any] = None):
        """Add conversation entry to history"""
        entry = ConversationEntry(
            timestamp=datetime.datetime.now().isoformat(),
            user_input=user_input,
            ai_response=ai_response,
            context=context or {},
            topics=self._extract_topics(user_input + " " + ai_response)
        )
        
        self.conversation_history.append(entry)
        
        # Maintain size limit
        if len(self.conversation_history) > CONVERSATION_MEMORY_LENGTH:
            self.conversation_history.pop(0)
        
        # Update user context
        if user_id not in self.user_context:
            self.user_context[user_id] = {}
        
        self.user_context[user_id].update({
            'last_interaction': entry.timestamp,
            'recent_topics': entry.topics[:3]
        })
        
        self.save_memory()
    
    def get_conversation_context(self, user_id: str = "default", limit: int = None) -> List[Dict[str, Any]]:
        """Get conversation context for user"""
        if limit is None:
            limit = CONVERSATION_CONTEXT_LENGTH
        
        recent_conversations = self.conversation_history[-limit:]
        return [asdict(entry) for entry in recent_conversations]
    
    def add_belief(self, user_id: str, belief: str, confidence: float = 0.8, source: str = "conversation"):
        """Add or update a belief for a user"""
        if user_id not in self.user_beliefs:
            self.user_beliefs[user_id] = []
        
        belief_entry = BeliefEntry(
            belief=belief,
            confidence=confidence,
            source=source,
            timestamp=datetime.datetime.now().isoformat()
        )
        
        self.user_beliefs[user_id].append(belief_entry)
        self.save_memory()
    
    def get_user_beliefs(self, user_id: str) -> List[Dict[str, Any]]:
        """Get beliefs for a specific user"""
        if user_id not in self.user_beliefs:
            return []
        
        return [asdict(belief) for belief in self.user_beliefs[user_id]]
    
    def search_memory(self, query: str, user_id: str = None) -> List[Dict[str, Any]]:
        """Search through conversation history"""
        results = []
        query_lower = query.lower()
        
        for entry in self.conversation_history:
            if (query_lower in entry.user_input.lower() or 
                query_lower in entry.ai_response.lower()):
                results.append(asdict(entry))
        
        return results[-10:]  # Return last 10 matches
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract topics from text (simplified)"""
        # Simple topic extraction - could be enhanced
        words = re.findall(r'\b\w+\b', text.lower())
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        topics = [word for word in words if len(word) > 3 and word not in common_words]
        return list(set(topics))[:5]  # Return up to 5 unique topics
    
    def save_memory(self):
        """Save memory to persistent storage"""
        try:
            data = {
                'conversation_history': [asdict(entry) for entry in self.conversation_history],
                'user_beliefs': {uid: [asdict(belief) for belief in beliefs] 
                               for uid, beliefs in self.user_beliefs.items()},
                'user_context': self.user_context,
                'topic_memory': self.topic_memory,
                'emotional_history': self.emotional_history,
                'last_updated': datetime.datetime.now().isoformat()
            }
            
            with open(self.memory_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"[UnifiedBeliefMemory] ❌ Failed to save memory: {e}")
    
    def load_memory(self):
        """Load memory from persistent storage"""
        try:
            if Path(self.memory_file).exists():
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                
                # Load conversation history
                if 'conversation_history' in data:
                    self.conversation_history = [
                        ConversationEntry(**entry) for entry in data['conversation_history']
                    ]
                
                # Load user beliefs
                if 'user_beliefs' in data:
                    for uid, beliefs in data['user_beliefs'].items():
                        self.user_beliefs[uid] = [BeliefEntry(**belief) for belief in beliefs]
                
                # Load other data
                self.user_context = data.get('user_context', {})
                self.topic_memory = data.get('topic_memory', {})
                self.emotional_history = data.get('emotional_history', [])
                
                print("[UnifiedBeliefMemory] 📂 Memory loaded from storage")
        except Exception as e:
            print(f"[UnifiedBeliefMemory] ❌ Failed to load memory: {e}")

# =============================================================================
# COMPATIBILITY ALIASES - Maintain backward compatibility
# =============================================================================

# Create global instance
unified_belief_memory_system = UnifiedBeliefMemorySystem()

# Backward compatibility functions from memory.py
def add_to_conversation_history(user_input: str, ai_response: str, user_id: str = "default", context: Dict[str, Any] = None):
    return unified_belief_memory_system.add_to_conversation_history(user_input, ai_response, user_id, context)

def get_conversation_context(user_id: str = "default", limit: int = None) -> List[Dict[str, Any]]:
    return unified_belief_memory_system.get_conversation_context(user_id, limit)

def validate_ai_response_appropriateness(response: str) -> bool:
    """Validate AI response appropriateness (simplified)"""
    return len(response.strip()) > 0 and not any(word in response.lower() for word in ['error', 'failed', 'crashed'])

# Global instance aliases
belief_memory_system = unified_belief_memory_system
memory_system = unified_belief_memory_system
