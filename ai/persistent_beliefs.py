"""
Persistent Beliefs & Knowledge Management System

This module manages long-term beliefs and facts that survive reboots,
providing consciousness continuity across sessions and auto-updating
the belief store during conversations.
"""

import json
import logging
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path

class BeliefType(Enum):
    """Types of beliefs and knowledge"""
    CORE_FACT = "core_fact"           # Fundamental facts (name, age, location)
    PREFERENCE = "preference"         # Likes, dislikes, preferences
    RELATIONSHIP = "relationship"     # Information about people/relationships
    EXPERIENCE = "experience"         # Past experiences and memories
    KNOWLEDGE = "knowledge"           # General knowledge and understanding
    BELIEF = "belief"                # Personal beliefs and opinions
    GOAL = "goal"                    # Goals and aspirations
    SKILL = "skill"                  # Skills and abilities
    HABIT = "habit"                  # Habits and routines

class BeliefCertainty(Enum):
    """Certainty levels for beliefs"""
    ABSOLUTE = 1.0      # 100% certain (verified facts)
    VERY_HIGH = 0.9     # 90% certain (strong evidence)
    HIGH = 0.8          # 80% certain (good evidence)
    MEDIUM = 0.6        # 60% certain (some evidence)
    LOW = 0.4           # 40% certain (weak evidence)
    UNCERTAIN = 0.2     # 20% certain (speculative)

@dataclass
class PersistentBelief:
    """A persistent belief or fact that survives sessions"""
    id: str
    content: str
    belief_type: BeliefType
    certainty: BeliefCertainty
    created_at: datetime
    last_confirmed: datetime
    confirmation_count: int = 0
    source_contexts: List[str] = field(default_factory=list)
    related_beliefs: Set[str] = field(default_factory=set)
    tags: Set[str] = field(default_factory=set)
    emotional_significance: float = 0.5  # 0.0 to 1.0
    decay_rate: float = 0.95             # How fast belief fades without reinforcement
    
    def __post_init__(self):
        if isinstance(self.related_beliefs, list):
            self.related_beliefs = set(self.related_beliefs)
        if isinstance(self.tags, list):
            self.tags = set(self.tags)

class PersistentBeliefManager:
    """
    Manages long-term beliefs and knowledge that persist across sessions.
    Provides consciousness continuity by maintaining core facts and beliefs.
    """
    
    def __init__(self, belief_store_path: str = "belief_store.json", 
                 backup_path: str = "belief_store_backup.json"):
        self.belief_store_path = Path(belief_store_path)
        self.backup_path = Path(backup_path)
        self.beliefs: Dict[str, PersistentBelief] = {}
        
        # Configuration
        self.max_beliefs = 1000              # Maximum beliefs to store
        self.confirmation_threshold = 3      # Confirmations needed for high certainty
        self.decay_interval_days = 30        # Days between decay calculations
        self.backup_interval_hours = 24      # Hours between backups
        
        # Extraction patterns for different belief types
        self.extraction_patterns = {
            BeliefType.CORE_FACT: [
                (r"my name is (\w+)", "name is {0}"),
                (r"i am (\d+) years old", "age is {0}"),
                (r"i live in ([^.]+)", "lives in {0}"),
                (r"i work (?:as|at) ([^.]+)", "works as/at {0}"),
                (r"i am from ([^.]+)", "from {0}"),
                (r"i have (\d+) (?:child|children|kids)", "has {0} children"),
                (r"i am (married|single|divorced|widowed)", "marital status: {0}")
            ],
            BeliefType.PREFERENCE: [
                (r"i (love|like|enjoy) ([^.]+)", "likes {1}"),
                (r"i (hate|dislike|can't stand) ([^.]+)", "dislikes {1}"),
                (r"my favorite ([^.]+) is ([^.]+)", "favorite {0} is {1}"),
                (r"i prefer ([^.]+) to ([^.]+)", "prefers {0} over {1}")
            ],
            BeliefType.RELATIONSHIP: [
                (r"my (\w+) is (\w+)", "relationship: {0} is {1}"),
                (r"i have a (\w+) named (\w+)", "has {0} named {1}"),
                (r"(\w+) is my (\w+)", "{0} is my {1}")
            ],
            BeliefType.EXPERIENCE: [
                (r"i (?:have|had) ([^.]+)", "has experienced: {0}"),
                (r"i went to ([^.]+)", "went to {0}"),
                (r"i studied ([^.]+)", "studied {0}"),
                (r"i worked at ([^.]+)", "worked at {0}")
            ],
            BeliefType.BELIEF: [
                (r"i believe (?:that )?([^.]+)", "believes {0}"),
                (r"i think (?:that )?([^.]+)", "thinks {0}"),
                (r"in my opinion[,]? ([^.]+)", "opinion: {0}")
            ],
            BeliefType.GOAL: [
                (r"i want to ([^.]+)", "wants to {0}"),
                (r"my goal is to ([^.]+)", "goal: {0}"),
                (r"i plan to ([^.]+)", "plans to {0}"),
                (r"i hope to ([^.]+)", "hopes to {0}")
            ],
            BeliefType.SKILL: [
                (r"i can ([^.]+)", "can {0}"),
                (r"i know how to ([^.]+)", "knows how to {0}"),
                (r"i am good at ([^.]+)", "good at {0}"),
                (r"i speak ([^.]+)", "speaks {0}")
            ],
            BeliefType.HABIT: [
                (r"i usually ([^.]+)", "usually {0}"),
                (r"i always ([^.]+)", "always {0}"),
                (r"i often ([^.]+)", "often {0}"),
                (r"every day i ([^.]+)", "daily habit: {0}")
            ]
        }
        
        # Initialize
        self.load_beliefs()
        self._schedule_maintenance()
        logging.info(f"[PersistentBeliefs] 🧠 Persistent belief manager initialized with {len(self.beliefs)} beliefs")
    
    def extract_beliefs_from_conversation(self, text: str, context: str = "") -> List[PersistentBelief]:
        """
        Extract new beliefs from conversation text
        
        Args:
            text: Conversation text to analyze
            context: Additional context information
            
        Returns:
            List of extracted beliefs
        """
        new_beliefs = []
        text_lower = text.lower().strip()
        
        for belief_type, patterns in self.extraction_patterns.items():
            for pattern, content_template in patterns:
                import re
                matches = re.finditer(pattern, text_lower)
                
                for match in matches:
                    # Generate belief content
                    groups = match.groups()
                    try:
                        content = content_template.format(*groups)
                    except (IndexError, KeyError):
                        content = match.group(0)  # Fallback to full match
                    
                    # Generate unique ID
                    belief_id = self._generate_belief_id(content, belief_type)
                    
                    # Check if similar belief already exists
                    existing_belief = self._find_similar_belief(content, belief_type)
                    
                    if existing_belief:
                        # Update existing belief
                        self._update_existing_belief(existing_belief, text, context)
                    else:
                        # Create new belief
                        certainty = self._assess_statement_certainty(text_lower)
                        emotional_sig = self._assess_emotional_significance(content, belief_type)
                        tags = self._extract_belief_tags(content, text)
                        
                        belief = PersistentBelief(
                            id=belief_id,
                            content=content,
                            belief_type=belief_type,
                            certainty=certainty,
                            created_at=datetime.now(),
                            last_confirmed=datetime.now(),
                            confirmation_count=1,
                            source_contexts=[text],
                            emotional_significance=emotional_sig,
                            tags=tags
                        )
                        
                        new_beliefs.append(belief)
                        self.beliefs[belief_id] = belief
        
        if new_beliefs:
            self.save_beliefs()
            logging.info(f"[PersistentBeliefs] 📝 Extracted {len(new_beliefs)} new beliefs")
        
        return new_beliefs
    
    def _generate_belief_id(self, content: str, belief_type: BeliefType) -> str:
        """Generate unique ID for a belief"""
        import hashlib
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        return f"{belief_type.value}_{content_hash}"
    
    def _find_similar_belief(self, content: str, belief_type: BeliefType) -> Optional[str]:
        """Find similar existing belief"""
        for belief_id, belief in self.beliefs.items():
            if belief.belief_type == belief_type:
                similarity = self._calculate_content_similarity(content, belief.content)
                if similarity > 0.8:  # 80% similarity threshold
                    return belief_id
        return None
    
    def _calculate_content_similarity(self, content1: str, content2: str) -> float:
        """Calculate similarity between two belief contents"""
        words1 = set(content1.lower().split())
        words2 = set(content2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def _update_existing_belief(self, belief_id: str, new_text: str, context: str):
        """Update an existing belief with new confirmation"""
        belief = self.beliefs[belief_id]
        
        belief.last_confirmed = datetime.now()
        belief.confirmation_count += 1
        belief.source_contexts.append(new_text)
        
        # Increase certainty with more confirmations
        if belief.confirmation_count >= self.confirmation_threshold:
            if belief.certainty.value < BeliefCertainty.HIGH.value:
                belief.certainty = BeliefCertainty.HIGH
        
        # Update emotional significance if warranted
        new_emotional_sig = self._assess_emotional_significance(new_text, belief.belief_type)
        if new_emotional_sig > belief.emotional_significance:
            belief.emotional_significance = new_emotional_sig
        
        logging.debug(f"[PersistentBeliefs] 🔄 Updated belief: {belief.content}")
    
    def _assess_statement_certainty(self, text: str) -> BeliefCertainty:
        """Assess certainty level of a statement"""
        # Look for certainty indicators
        if any(word in text for word in ['definitely', 'absolutely', 'certainly', 'always']):
            return BeliefCertainty.VERY_HIGH
        elif any(word in text for word in ['probably', 'likely', 'usually', 'often']):
            return BeliefCertainty.HIGH
        elif any(word in text for word in ['maybe', 'perhaps', 'might', 'could']):
            return BeliefCertainty.LOW
        elif any(word in text for word in ['unsure', 'not sure', 'don\'t know']):
            return BeliefCertainty.UNCERTAIN
        else:
            return BeliefCertainty.MEDIUM
    
    def _assess_emotional_significance(self, content: str, belief_type: BeliefType) -> float:
        """Assess emotional significance of a belief"""
        base_significance = {
            BeliefType.CORE_FACT: 0.8,      # High - identity facts
            BeliefType.RELATIONSHIP: 0.9,    # Very high - relationships important
            BeliefType.PREFERENCE: 0.6,      # Medium - preferences matter
            BeliefType.EXPERIENCE: 0.7,      # High - experiences shape us
            BeliefType.BELIEF: 0.7,          # High - core beliefs
            BeliefType.GOAL: 0.8,            # High - future orientation
            BeliefType.SKILL: 0.5,           # Medium - practical abilities
            BeliefType.HABIT: 0.4,           # Lower - routine behaviors
            BeliefType.KNOWLEDGE: 0.5        # Medium - general knowledge
        }.get(belief_type, 0.5)
        
        # Boost for emotional words
        emotional_words = ['love', 'hate', 'fear', 'joy', 'sadness', 'anger', 'passion', 'dream']
        emotional_boost = sum(0.1 for word in emotional_words if word in content.lower())
        
        return min(1.0, base_significance + emotional_boost)
    
    def _extract_belief_tags(self, content: str, original_text: str) -> Set[str]:
        """Extract tags for categorizing beliefs"""
        tags = set()
        content_lower = content.lower()
        text_lower = original_text.lower()
        
        # Domain tags
        if any(word in content_lower for word in ['family', 'parent', 'child', 'spouse', 'relative']):
            tags.add('family')
        if any(word in content_lower for word in ['work', 'job', 'career', 'office', 'company']):
            tags.add('work')
        if any(word in content_lower for word in ['health', 'medical', 'doctor', 'medicine']):
            tags.add('health')
        if any(word in content_lower for word in ['food', 'eating', 'cooking', 'restaurant']):
            tags.add('food')
        if any(word in content_lower for word in ['music', 'art', 'movie', 'book', 'creative']):
            tags.add('entertainment')
        if any(word in content_lower for word in ['travel', 'vacation', 'trip', 'visit']):
            tags.add('travel')
        if any(word in content_lower for word in ['sport', 'exercise', 'fitness', 'gym']):
            tags.add('sports')
        if any(word in content_lower for word in ['technology', 'computer', 'programming', 'digital']):
            tags.add('technology')
        
        # Temporal tags
        if any(word in text_lower for word in ['used to', 'previously', 'before', 'past']):
            tags.add('past')
        if any(word in text_lower for word in ['plan to', 'will', 'future', 'goal']):
            tags.add('future')
        if any(word in text_lower for word in ['currently', 'now', 'present', 'today']):
            tags.add('current')
        
        # Emotional tags
        if any(word in text_lower for word in ['love', 'passion', 'adore', 'cherish']):
            tags.add('positive_emotion')
        if any(word in text_lower for word in ['hate', 'dislike', 'fear', 'anxiety']):
            tags.add('negative_emotion')
        
        return tags
    
    def get_core_beliefs_context(self, max_beliefs: int = 20) -> str:
        """
        Get core beliefs formatted for consciousness context
        
        Args:
            max_beliefs: Maximum number of beliefs to include
            
        Returns:
            Formatted string of core beliefs
        """
        # Sort beliefs by importance (certainty + emotional significance + recency)
        belief_items = []
        for belief in self.beliefs.values():
            importance = (
                belief.certainty.value * 0.4 +
                belief.emotional_significance * 0.4 +
                self._calculate_recency_score(belief) * 0.2
            )
            belief_items.append((importance, belief))
        
        # Sort by importance and take top beliefs
        belief_items.sort(key=lambda x: x[0], reverse=True)
        top_beliefs = belief_items[:max_beliefs]
        
        if not top_beliefs:
            return ""
        
        # Format for context
        context_lines = ["Core Persistent Beliefs:"]
        
        # Group by type for better organization
        beliefs_by_type = {}
        for _, belief in top_beliefs:
            belief_type = belief.belief_type.value
            if belief_type not in beliefs_by_type:
                beliefs_by_type[belief_type] = []
            beliefs_by_type[belief_type].append(belief)
        
        for belief_type, beliefs in beliefs_by_type.items():
            context_lines.append(f"  {belief_type.title()}:")
            for belief in beliefs[:5]:  # Max 5 per type
                certainty_indicator = "✓" if belief.certainty.value >= 0.8 else "~"
                context_lines.append(f"    {certainty_indicator} {belief.content}")
        
        return "\n".join(context_lines)
    
    def _calculate_recency_score(self, belief: PersistentBelief) -> float:
        """Calculate recency score (0.0 to 1.0)"""
        days_since_confirmed = (datetime.now() - belief.last_confirmed).days
        
        # Decay over time, but never completely
        if days_since_confirmed <= 1:
            return 1.0
        elif days_since_confirmed <= 7:
            return 0.8
        elif days_since_confirmed <= 30:
            return 0.6
        elif days_since_confirmed <= 90:
            return 0.4
        else:
            return 0.2
    
    def find_related_beliefs(self, query: str, max_results: int = 5) -> List[PersistentBelief]:
        """
        Find beliefs related to a query
        
        Args:
            query: Search query
            max_results: Maximum results to return
            
        Returns:
            List of related beliefs
        """
        query_words = set(query.lower().split())
        scored_beliefs = []
        
        for belief in self.beliefs.values():
            # Calculate relevance score
            content_words = set(belief.content.lower().split())
            tag_words = belief.tags
            
            # Word overlap score
            content_overlap = len(query_words.intersection(content_words)) / len(query_words)
            tag_overlap = len(query_words.intersection(tag_words)) / len(query_words) if tag_words else 0
            
            # Combined score weighted by certainty and significance
            relevance_score = (
                content_overlap * 0.6 +
                tag_overlap * 0.2 +
                belief.certainty.value * 0.1 +
                belief.emotional_significance * 0.1
            )
            
            if relevance_score > 0.1:  # Minimum threshold
                scored_beliefs.append((relevance_score, belief))
        
        # Sort by relevance and return top results
        scored_beliefs.sort(reverse=True)
        return [belief for _, belief in scored_beliefs[:max_results]]
    
    def apply_belief_decay(self):
        """Apply natural decay to beliefs over time"""
        current_time = datetime.now()
        beliefs_to_remove = []
        
        for belief_id, belief in self.beliefs.items():
            days_since_confirmed = (current_time - belief.last_confirmed).days
            
            if days_since_confirmed > self.decay_interval_days:
                # Apply decay
                decay_factor = belief.decay_rate ** (days_since_confirmed / self.decay_interval_days)
                new_certainty_value = belief.certainty.value * decay_factor
                
                # Remove beliefs that have decayed too much
                if new_certainty_value < 0.1:
                    beliefs_to_remove.append(belief_id)
                    logging.info(f"[PersistentBeliefs] 🍂 Decayed belief removed: {belief.content}")
                else:
                    # Update certainty
                    for certainty_level in BeliefCertainty:
                        if new_certainty_value >= certainty_level.value:
                            belief.certainty = certainty_level
                            break
        
        # Remove highly decayed beliefs
        for belief_id in beliefs_to_remove:
            del self.beliefs[belief_id]
        
        if beliefs_to_remove:
            self.save_beliefs()
            logging.info(f"[PersistentBeliefs] 🧹 Removed {len(beliefs_to_remove)} decayed beliefs")
    
    def save_beliefs(self):
        """Save beliefs to persistent storage with backup"""
        try:
            # Create backup first
            if self.belief_store_path.exists():
                import shutil
                shutil.copy2(self.belief_store_path, self.backup_path)
            
            # Prepare data for saving
            beliefs_data = {}
            for belief_id, belief in self.beliefs.items():
                belief_dict = asdict(belief)
                
                # Convert datetime objects to ISO format
                belief_dict['created_at'] = belief.created_at.isoformat()
                belief_dict['last_confirmed'] = belief.last_confirmed.isoformat()
                
                # Convert enums to values
                belief_dict['belief_type'] = belief.belief_type.value
                belief_dict['certainty'] = belief.certainty.value
                
                # Convert sets to lists
                belief_dict['related_beliefs'] = list(belief.related_beliefs)
                belief_dict['tags'] = list(belief.tags)
                
                beliefs_data[belief_id] = belief_dict
            
            # Save metadata
            metadata = {
                'version': '1.0',
                'saved_at': datetime.now().isoformat(),
                'belief_count': len(beliefs_data),
                'beliefs': beliefs_data
            }
            
            with open(self.belief_store_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            logging.debug(f"[PersistentBeliefs] 💾 Saved {len(self.beliefs)} beliefs")
            
        except Exception as e:
            logging.error(f"[PersistentBeliefs] ❌ Failed to save beliefs: {e}")
    
    def load_beliefs(self):
        """Load beliefs from persistent storage"""
        try:
            if self.belief_store_path.exists():
                with open(self.belief_store_path, 'r') as f:
                    data = json.load(f)
                
                beliefs_data = data.get('beliefs', {})
                
                for belief_id, belief_dict in beliefs_data.items():
                    try:
                        # Convert ISO strings back to datetime
                        belief_dict['created_at'] = datetime.fromisoformat(belief_dict['created_at'])
                        belief_dict['last_confirmed'] = datetime.fromisoformat(belief_dict['last_confirmed'])
                        
                        # Convert values back to enums
                        belief_dict['belief_type'] = BeliefType(belief_dict['belief_type'])
                        # Handle certainty as either enum or float
                        certainty_value = belief_dict['certainty']
                        if isinstance(certainty_value, str):
                            belief_dict['certainty'] = BeliefCertainty(certainty_value)
                        else:
                            # Find closest certainty level
                            for certainty_level in sorted(BeliefCertainty, key=lambda x: x.value, reverse=True):
                                if certainty_value >= certainty_level.value:
                                    belief_dict['certainty'] = certainty_level
                                    break
                            else:
                                belief_dict['certainty'] = BeliefCertainty.UNCERTAIN
                        
                        # Convert lists back to sets
                        belief_dict['related_beliefs'] = set(belief_dict.get('related_beliefs', []))
                        belief_dict['tags'] = set(belief_dict.get('tags', []))
                        
                        # Create belief object
                        belief = PersistentBelief(**belief_dict)
                        self.beliefs[belief_id] = belief
                        
                    except Exception as belief_error:
                        logging.error(f"[PersistentBeliefs] ❌ Failed to load belief {belief_id}: {belief_error}")
                        continue
                
                logging.info(f"[PersistentBeliefs] 📂 Loaded {len(self.beliefs)} beliefs")
                
        except Exception as e:
            logging.error(f"[PersistentBeliefs] ❌ Failed to load beliefs: {e}")
            self.beliefs = {}
    
    def _schedule_maintenance(self):
        """Schedule periodic maintenance tasks"""
        # Apply decay every time beliefs are loaded
        self.apply_belief_decay()
        
        # Limit beliefs if too many
        if len(self.beliefs) > self.max_beliefs:
            self._prune_beliefs()
    
    def _prune_beliefs(self):
        """Remove least important beliefs to stay under limit"""
        # Calculate importance scores
        belief_scores = []
        for belief_id, belief in self.beliefs.items():
            importance = (
                belief.certainty.value * 0.3 +
                belief.emotional_significance * 0.3 +
                self._calculate_recency_score(belief) * 0.2 +
                min(belief.confirmation_count / 10, 0.2)  # Confirmation bonus
            )
            belief_scores.append((importance, belief_id))
        
        # Sort by importance and keep top beliefs
        belief_scores.sort(reverse=True)
        beliefs_to_keep = belief_scores[:self.max_beliefs]
        
        # Remove least important beliefs
        keep_ids = {belief_id for _, belief_id in beliefs_to_keep}
        remove_ids = set(self.beliefs.keys()) - keep_ids
        
        for belief_id in remove_ids:
            del self.beliefs[belief_id]
        
        logging.info(f"[PersistentBeliefs] 🧹 Pruned {len(remove_ids)} beliefs to stay under limit")
        self.save_beliefs()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get persistent beliefs statistics"""
        if not self.beliefs:
            return {'total_beliefs': 0}
        
        # Count by type
        type_counts = {}
        certainty_counts = {}
        tag_counts = {}
        
        total_emotional_significance = 0
        
        for belief in self.beliefs.values():
            # Count by type
            belief_type = belief.belief_type.value
            type_counts[belief_type] = type_counts.get(belief_type, 0) + 1
            
            # Count by certainty
            certainty = belief.certainty.name
            certainty_counts[certainty] = certainty_counts.get(certainty, 0) + 1
            
            # Count tags
            for tag in belief.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
            
            total_emotional_significance += belief.emotional_significance
        
        avg_emotional_significance = total_emotional_significance / len(self.beliefs)
        
        return {
            'total_beliefs': len(self.beliefs),
            'beliefs_by_type': type_counts,
            'beliefs_by_certainty': certainty_counts,
            'top_tags': dict(sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]),
            'average_emotional_significance': round(avg_emotional_significance, 2),
            'last_maintenance': datetime.now().isoformat()
        }

# Global persistent belief manager
persistent_beliefs = PersistentBeliefManager()

def update_beliefs_from_conversation(text: str, context: str = "") -> Tuple[List[PersistentBelief], str]:
    """
    Convenience function to extract and store beliefs from conversation
    
    Args:
        text: Conversation text
        context: Additional context
        
    Returns:
        Tuple of (new_beliefs, core_beliefs_context)
    """
    new_beliefs = persistent_beliefs.extract_beliefs_from_conversation(text, context)
    core_context = persistent_beliefs.get_core_beliefs_context()
    
    return new_beliefs, core_context

def get_persistent_beliefs_context(max_beliefs: int = 20) -> str:
    """Get core beliefs context for consciousness"""
    return persistent_beliefs.get_core_beliefs_context(max_beliefs)

def find_beliefs_about(query: str, max_results: int = 5) -> List[PersistentBelief]:
    """Find beliefs related to a query"""
    return persistent_beliefs.find_related_beliefs(query, max_results)

def get_belief_stats() -> Dict[str, Any]:
    """Get persistent beliefs statistics"""
    return persistent_beliefs.get_stats()

logging.info("[PersistentBeliefs] 🧠 Persistent beliefs & knowledge module loaded")
print("[PersistentBeliefs] ✅ Knowledge Updates & Persistent Beliefs: LOADED")
print("[PersistentBeliefs] 🎯 Consciousness continuity across sessions")
print("[PersistentBeliefs] 💾 Core facts and beliefs survive reboots")