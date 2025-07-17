"""
Enhanced Persistent Beliefs System
Manages long-term belief storage and continuity across sessions.
"""

import json
import logging
import threading
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum

class BeliefType(Enum):
    """Types of beliefs that can be stored"""
    CORE_FACT = "core_fact"           # Fundamental facts (name, age, etc.)
    PREFERENCE = "preference"          # Likes, dislikes, preferences
    RELATIONSHIP = "relationship"      # People, pets, relationships
    GOAL = "goal"                     # Aspirations, plans, objectives
    HABIT = "habit"                   # Regular behaviors, routines
    EXPERIENCE = "experience"         # Past experiences, events
    KNOWLEDGE = "knowledge"           # Learned information, skills
    OPINION = "opinion"               # Views, beliefs, perspectives

@dataclass
class PersistentBelief:
    """A belief that persists across sessions"""
    id: str
    content: str
    belief_type: BeliefType
    confidence: float  # 0.0 to 1.0
    importance: float  # How important this belief is (0.0 to 1.0)
    created_at: str
    last_updated: str
    last_accessed: str
    access_count: int = 1
    confirmation_count: int = 1
    source: str = "conversation"
    context: Dict[str, Any] = None
    tags: List[str] = None
    
    def __post_init__(self):
        if self.context is None:
            self.context = {}
        if self.tags is None:
            self.tags = []

class PersistentBeliefsManager:
    """
    Enhanced Persistent Beliefs System
    
    Manages long-term storage of beliefs that survive across sessions,
    providing consciousness continuity and better user understanding.
    """
    
    def __init__(self, belief_file: str = "persistent_beliefs.json", auto_save_interval: int = 300):
        self.belief_file = Path(belief_file)
        self.auto_save_interval = auto_save_interval  # seconds
        self.beliefs: Dict[str, Dict[str, PersistentBelief]] = {}  # user_id -> {belief_id -> belief}
        self.last_save_time = datetime.now()
        self._lock = threading.Lock()
        
        self.load_beliefs()
        self._start_auto_save()
        
        logging.info(f"[PersistentBeliefs] 🧠 Persistent beliefs manager initialized")
    
    def load_beliefs(self):
        """Load persistent beliefs from storage"""
        try:
            if self.belief_file.exists():
                with open(self.belief_file, 'r') as f:
                    data = json.load(f)
                
                # Convert data back to PersistentBelief objects
                for user_id, user_beliefs in data.get('beliefs', {}).items():
                    self.beliefs[user_id] = {}
                    for belief_id, belief_data in user_beliefs.items():
                        # Convert belief_type string back to enum
                        belief_data['belief_type'] = BeliefType(belief_data['belief_type'])
                        self.beliefs[user_id][belief_id] = PersistentBelief(**belief_data)
                
                total_beliefs = sum(len(user_beliefs) for user_beliefs in self.beliefs.values())
                logging.info(f"[PersistentBeliefs] 📚 Loaded {total_beliefs} persistent beliefs for {len(self.beliefs)} users")
            else:
                logging.info(f"[PersistentBeliefs] 🆕 Creating new persistent beliefs store")
                
        except Exception as e:
            logging.error(f"[PersistentBeliefs] ❌ Error loading beliefs: {e}")
            self.beliefs = {}
    
    def save_beliefs(self):
        """Save persistent beliefs to storage"""
        try:
            with self._lock:
                # Convert PersistentBelief objects to dictionaries
                beliefs_data = {}
                for user_id, user_beliefs in self.beliefs.items():
                    beliefs_data[user_id] = {}
                    for belief_id, belief in user_beliefs.items():
                        belief_dict = asdict(belief)
                        # Convert enum to string for JSON serialization
                        belief_dict['belief_type'] = belief.belief_type.value
                        beliefs_data[user_id][belief_id] = belief_dict
                
                data = {
                    'beliefs': beliefs_data,
                    'metadata': {
                        'last_updated': datetime.now().isoformat(),
                        'total_beliefs': sum(len(user_beliefs) for user_beliefs in self.beliefs.values()),
                        'total_users': len(self.beliefs)
                    }
                }
                
                with open(self.belief_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                self.last_save_time = datetime.now()
                logging.debug(f"[PersistentBeliefs] 💾 Persistent beliefs saved")
                
        except Exception as e:
            logging.error(f"[PersistentBeliefs] ❌ Error saving beliefs: {e}")
    
    def _start_auto_save(self):
        """Start automatic saving thread"""
        def auto_save():
            import time
            while True:
                time.sleep(self.auto_save_interval)
                if (datetime.now() - self.last_save_time).seconds >= self.auto_save_interval:
                    self.save_beliefs()
        
        thread = threading.Thread(target=auto_save, daemon=True)
        thread.start()
    
    def add_belief(self, user_id: str, content: str, belief_type: BeliefType, 
                  confidence: float = 0.8, importance: float = 0.5, 
                  context: Dict[str, Any] = None, tags: List[str] = None) -> str:
        """
        Add a new persistent belief
        
        Args:
            user_id: User identifier
            content: Belief content
            belief_type: Type of belief
            confidence: Confidence in this belief (0.0 to 1.0)
            importance: Importance of this belief (0.0 to 1.0)
            context: Additional context
            tags: Tags for categorization
            
        Returns:
            Belief ID
        """
        with self._lock:
            if user_id not in self.beliefs:
                self.beliefs[user_id] = {}
            
            # Generate unique belief ID
            belief_id = f"{belief_type.value}_{len(self.beliefs[user_id])}_{int(datetime.now().timestamp())}"
            
            # Check for similar existing beliefs
            existing_belief = self._find_similar_belief(user_id, content, belief_type)
            if existing_belief:
                # Update existing belief instead of creating duplicate
                existing_belief.confirmation_count += 1
                existing_belief.last_updated = datetime.now().isoformat()
                existing_belief.confidence = min(1.0, existing_belief.confidence + 0.1)
                logging.debug(f"[PersistentBeliefs] ✅ Updated existing belief: {content}")
                return existing_belief.id
            
            # Create new belief
            belief = PersistentBelief(
                id=belief_id,
                content=content,
                belief_type=belief_type,
                confidence=confidence,
                importance=importance,
                created_at=datetime.now().isoformat(),
                last_updated=datetime.now().isoformat(),
                last_accessed=datetime.now().isoformat(),
                context=context or {},
                tags=tags or []
            )
            
            self.beliefs[user_id][belief_id] = belief
            
            logging.debug(f"[PersistentBeliefs] 🆕 Added belief: {content} (type: {belief_type.value})")
            return belief_id
    
    def _find_similar_belief(self, user_id: str, content: str, belief_type: BeliefType) -> Optional[PersistentBelief]:
        """Find similar existing belief to avoid duplicates"""
        if user_id not in self.beliefs:
            return None
        
        content_lower = content.lower()
        content_words = set(content_lower.split())
        
        for belief in self.beliefs[user_id].values():
            if belief.belief_type == belief_type:
                belief_words = set(belief.content.lower().split())
                
                # Calculate similarity based on word overlap
                overlap = len(content_words.intersection(belief_words))
                total_words = len(content_words.union(belief_words))
                
                if total_words > 0 and overlap / total_words > 0.7:  # 70% similarity threshold
                    return belief
        
        return None
    
    def get_beliefs(self, user_id: str, belief_type: Optional[BeliefType] = None,
                   min_importance: float = 0.0, limit: Optional[int] = None) -> List[PersistentBelief]:
        """
        Get beliefs for a user
        
        Args:
            user_id: User identifier
            belief_type: Filter by belief type (optional)
            min_importance: Minimum importance threshold
            limit: Maximum number of beliefs to return
            
        Returns:
            List of beliefs
        """
        if user_id not in self.beliefs:
            return []
        
        user_beliefs = list(self.beliefs[user_id].values())
        
        # Filter by type if specified
        if belief_type:
            user_beliefs = [b for b in user_beliefs if b.belief_type == belief_type]
        
        # Filter by importance
        user_beliefs = [b for b in user_beliefs if b.importance >= min_importance]
        
        # Sort by importance and recency
        user_beliefs.sort(key=lambda b: (b.importance, b.last_accessed), reverse=True)
        
        # Update access time
        current_time = datetime.now().isoformat()
        for belief in user_beliefs[:limit] if limit else user_beliefs:
            belief.last_accessed = current_time
            belief.access_count += 1
        
        return user_beliefs[:limit] if limit else user_beliefs
    
    def get_core_beliefs(self, user_id: str) -> Dict[str, List[PersistentBelief]]:
        """Get core beliefs organized by category"""
        core_categories = [
            BeliefType.CORE_FACT,
            BeliefType.PREFERENCE, 
            BeliefType.RELATIONSHIP,
            BeliefType.GOAL
        ]
        
        core_beliefs = {}
        for category in core_categories:
            beliefs = self.get_beliefs(user_id, category, min_importance=0.3, limit=5)
            if beliefs:
                core_beliefs[category.value] = beliefs
        
        return core_beliefs
    
    def update_belief_importance(self, user_id: str, belief_id: str, importance: float):
        """Update the importance of a belief"""
        with self._lock:
            if user_id in self.beliefs and belief_id in self.beliefs[user_id]:
                belief = self.beliefs[user_id][belief_id]
                belief.importance = max(0.0, min(1.0, importance))
                belief.last_updated = datetime.now().isoformat()
                logging.debug(f"[PersistentBeliefs] 📊 Updated belief importance: {belief.content} -> {importance}")
    
    def remove_belief(self, user_id: str, belief_id: str):
        """Remove a belief (use carefully)"""
        with self._lock:
            if user_id in self.beliefs and belief_id in self.beliefs[user_id]:
                belief = self.beliefs[user_id][belief_id]
                del self.beliefs[user_id][belief_id]
                logging.debug(f"[PersistentBeliefs] 🗑️ Removed belief: {belief.content}")
    
    def get_belief_context_for_conversation(self, user_id: str, max_beliefs: int = 10) -> str:
        """
        Get formatted belief context for conversation
        
        Args:
            user_id: User identifier
            max_beliefs: Maximum number of beliefs to include
            
        Returns:
            Formatted belief context string
        """
        core_beliefs = self.get_core_beliefs(user_id)
        
        if not core_beliefs:
            return ""
        
        context_parts = ["PERSISTENT BELIEFS & FACTS:"]
        belief_count = 0
        
        for category, beliefs in core_beliefs.items():
            if belief_count >= max_beliefs:
                break
                
            category_beliefs = []
            for belief in beliefs[:3]:  # Limit per category
                if belief_count >= max_beliefs:
                    break
                category_beliefs.append(f"- {belief.content}")
                belief_count += 1
            
            if category_beliefs:
                context_parts.append(f"{category.upper().replace('_', ' ')}:")
                context_parts.extend(category_beliefs)
        
        # Ensure we return some context even if no core beliefs
        if belief_count == 0:
            # Get any beliefs with reasonable importance
            all_beliefs = self.get_beliefs(user_id, min_importance=0.3, limit=max_beliefs)
            if all_beliefs:
                context_parts = ["KNOWN FACTS:"]
                for belief in all_beliefs[:max_beliefs]:
                    context_parts.append(f"- {belief.content}")
        
        return "\n".join(context_parts) if len(context_parts) > 1 else ""
    
    def extract_and_store_beliefs_from_conversation(self, user_id: str, conversation_text: str):
        """
        Extract and store beliefs from conversation text
        
        Args:
            user_id: User identifier
            conversation_text: Text to analyze for beliefs
        """
        # Import belief analyzer for extraction
        try:
            from .belief_analyzer import belief_analyzer
            
            analysis = belief_analyzer.analyze_statement(conversation_text, user_id)
            
            # Convert extracted beliefs to persistent beliefs
            for belief_data in analysis.get('new_beliefs', []):
                # Map categories
                category_mapping = {
                    'personal': BeliefType.CORE_FACT,
                    'preference': BeliefType.PREFERENCE,
                    'relationship': BeliefType.RELATIONSHIP,
                    'goal': BeliefType.GOAL,
                    'fact': BeliefType.CORE_FACT
                }
                
                belief_type = category_mapping.get(belief_data['category'], BeliefType.KNOWLEDGE)
                importance = 0.7 if belief_type in [BeliefType.CORE_FACT, BeliefType.RELATIONSHIP] else 0.5
                
                self.add_belief(
                    user_id=user_id,
                    content=belief_data['content'],
                    belief_type=belief_type,
                    confidence=belief_data['confidence'],
                    importance=importance,
                    context={'extracted_from': 'conversation'},
                    tags=['auto_extracted']
                )
            
            logging.debug(f"[PersistentBeliefs] 🔍 Extracted {len(analysis.get('new_beliefs', []))} beliefs from conversation")
            
        except ImportError:
            logging.warning("[PersistentBeliefs] ⚠️ Belief analyzer not available for extraction")
    
    def get_user_summary(self, user_id: str) -> Dict[str, Any]:
        """Get summary of user's persistent beliefs"""
        if user_id not in self.beliefs:
            return {'total_beliefs': 0, 'categories': {}}
        
        user_beliefs = self.beliefs[user_id]
        categories = {}
        
        for belief in user_beliefs.values():
            category = belief.belief_type.value
            if category not in categories:
                categories[category] = 0
            categories[category] += 1
        
        return {
            'total_beliefs': len(user_beliefs),
            'categories': categories,
            'most_recent': max((b.last_updated for b in user_beliefs.values()), default=None),
            'most_important': max((b.importance for b in user_beliefs.values()), default=0.0)
        }
    
    def cleanup_old_beliefs(self, days_threshold: int = 365):
        """Clean up old, low-importance beliefs"""
        with self._lock:
            current_time = datetime.now()
            threshold_date = current_time - timedelta(days=days_threshold)
            
            removed_count = 0
            for user_id in list(self.beliefs.keys()):
                user_beliefs = self.beliefs[user_id]
                
                for belief_id in list(user_beliefs.keys()):
                    belief = user_beliefs[belief_id]
                    last_accessed = datetime.fromisoformat(belief.last_accessed)
                    
                    # Remove if old, low importance, and rarely accessed
                    if (last_accessed < threshold_date and 
                        belief.importance < 0.3 and 
                        belief.access_count < 3):
                        del user_beliefs[belief_id]
                        removed_count += 1
                
                # Remove user if no beliefs left
                if not user_beliefs:
                    del self.beliefs[user_id]
            
            if removed_count > 0:
                logging.info(f"[PersistentBeliefs] 🧹 Cleaned up {removed_count} old beliefs")

# Global persistent beliefs manager
persistent_beliefs_manager = PersistentBeliefsManager()

def get_persistent_belief_context(user_id: str, max_beliefs: int = 8) -> str:
    """
    Get persistent belief context for conversation
    
    Args:
        user_id: User identifier
        max_beliefs: Maximum number of beliefs to include
        
    Returns:
        Formatted belief context string
    """
    return persistent_beliefs_manager.get_belief_context_for_conversation(user_id, max_beliefs)

def store_conversation_beliefs(user_id: str, conversation_text: str):
    """
    Store beliefs extracted from conversation
    
    Args:
        user_id: User identifier
        conversation_text: Conversation text to analyze
    """
    persistent_beliefs_manager.extract_and_store_beliefs_from_conversation(user_id, conversation_text)