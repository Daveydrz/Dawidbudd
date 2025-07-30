"""
Belief Memory - Consolidated belief and memory management system
Created: 2025-01-29
Purpose: Unified belief and memory subsystem combining belief_analyzer.py, belief_evolution_tracker.py, 
         belief_memory_refiner.py, belief_qualia_linking.py, belief_reinforcement.py, memory.py, 
         and memory_context_corrector.py

This module consolidates:
- Belief Analyzer (belief analysis, contradiction detection, consistency management)
- Belief Evolution Tracker (dynamic belief formation and evolution)
- Belief Memory Refiner (belief refinement and optimization)
- Belief Qualia Linking (belief-qualia connections)
- Belief Reinforcement (belief confidence and learning system)
- Memory System (comprehensive memory management with context awareness)
- Memory Context Corrector (context-aware memory correction)
"""

import json
import os
import time
import threading
import random
import logging
import math
import hashlib
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Set, Callable
from dataclasses import dataclass, asdict, field
from enum import Enum
from pathlib import Path
from collections import defaultdict, deque
import tempfile

# Optional imports with fallbacks
try:
    from ai.consciousness_core import consciousness_manager
    CONSCIOUSNESS_AVAILABLE = True
except ImportError:
    CONSCIOUSNESS_AVAILABLE = False

try:
    from ai.entropy import get_entropy_engine, probabilistic_select, inject_consciousness_entropy, EntropyLevel
    ENTROPY_AVAILABLE = True
except ImportError:
    ENTROPY_AVAILABLE = False
    def probabilistic_select(items, weights=None):
        if not items:
            return None
        return random.choice(items)

try:
    from config import MAX_HISTORY_LENGTH, DEBUG
    MAX_HISTORY_LENGTH = MAX_HISTORY_LENGTH or 100
    DEBUG = DEBUG or False
except ImportError:
    MAX_HISTORY_LENGTH = 100
    DEBUG = False

# ============================================================================
# CONSOLIDATED ENUMS AND DATA STRUCTURES
# ============================================================================

class BeliefType(Enum):
    """Types of beliefs the system can hold"""
    FACTUAL = "factual"           # Beliefs about facts and objective reality
    EVALUATIVE = "evaluative"     # Beliefs about value judgments
    CAUSAL = "causal"            # Beliefs about cause-and-effect relationships
    PREDICTIVE = "predictive"     # Beliefs about future outcomes
    NORMATIVE = "normative"       # Beliefs about what should be done
    PERSONAL = "personal"         # Beliefs about individuals and relationships
    EXPERIENTIAL = "experiential" # Beliefs formed from direct experience
    CONCEPTUAL = "conceptual"     # Beliefs about abstract concepts
    PREFERENCE = "preference"     # User preferences and likes/dislikes
    OPINION = "opinion"           # Subjective opinions
    TEMPORAL = "temporal"         # Time-related beliefs
    RELATIONAL = "relational"     # Relationship-based beliefs

class BeliefCertainty(Enum):
    """Certainty levels for beliefs"""
    CERTAIN = "certain"
    CONFIDENT = "confident"
    MODERATE = "moderate"
    UNCERTAIN = "uncertain"
    SPECULATIVE = "speculative"

class BeliefStrength(Enum):
    """Strength levels for beliefs"""
    WEAK = 0.2          # Tentative, easily changed
    MODERATE = 0.5      # Fairly confident
    STRONG = 0.8        # High confidence
    CONVICTION = 1.0    # Very strong belief, hard to change

class BeliefStatus(Enum):
    """Status of beliefs in the system"""
    ACTIVE = "active"           # Currently held belief
    QUESTIONED = "questioned"   # Under examination due to conflicts
    SUSPENDED = "suspended"     # Temporarily not held due to contradictions
    EVOLVED = "evolved"         # Changed into a new form
    ABANDONED = "abandoned"     # No longer held

class ContradictionType(Enum):
    """Types of belief contradictions"""
    DIRECT = "direct"
    LOGICAL = "logical"
    TEMPORAL = "temporal"
    CONTEXTUAL = "contextual"

class EvidenceType(Enum):
    """Types of evidence that can support or contradict beliefs"""
    DIRECT_EXPERIENCE = "direct_experience"
    USER_STATEMENT = "user_statement"
    LOGICAL_REASONING = "logical_reasoning"
    PATTERN_RECOGNITION = "pattern_recognition"
    EXTERNAL_SOURCE = "external_source"
    CONSENSUS = "consensus"
    CONTRADICTION = "contradiction"

class BeliefReinforcement(Enum):
    """Types of belief reinforcement"""
    POSITIVE = "positive"      # Belief was confirmed
    NEGATIVE = "negative"      # Belief was contradicted
    NEUTRAL = "neutral"        # No clear evidence either way
    CONTEXTUAL = "contextual"  # Belief applies in some contexts but not others

class LearningOutcome(Enum):
    """Outcomes of learning attempts"""
    SUCCESS = "success"                  # Successfully updated belief
    PARTIAL_SUCCESS = "partial_success"  # Some progress made
    FAILURE = "failure"                  # Failed to resolve contradiction
    DEFERRED = "deferred"               # Postponed resolution
    COMPLEXITY_REVEALED = "complexity_revealed"  # Discovered issue is more complex

class MemoryType(Enum):
    """Types of memories"""
    EPISODIC = "episodic"       # Specific events and experiences
    SEMANTIC = "semantic"       # Facts and knowledge
    PROCEDURAL = "procedural"   # Skills and procedures
    EMOTIONAL = "emotional"     # Emotionally significant memories
    WORKING = "working"         # Short-term working memory
    CONTEXTUAL = "contextual"   # Context-specific memories

class MemoryImportance(Enum):
    """Importance levels for memories"""
    CRITICAL = 1.0
    HIGH = 0.8
    MEDIUM = 0.6
    LOW = 0.4
    MINIMAL = 0.2

# ============================================================================
# CONSOLIDATED DATA STRUCTURES
# ============================================================================

@dataclass
class Belief:
    """Comprehensive belief representation"""
    id: str
    content: str
    belief_type: BeliefType
    certainty: BeliefCertainty
    strength: float  # 0.0 to 1.0
    status: BeliefStatus
    source: str
    timestamp: datetime
    user: str
    context: Dict[str, Any] = field(default_factory=dict)
    supporting_evidence: List[str] = field(default_factory=list)
    contradicting_evidence: List[str] = field(default_factory=list)
    contradictions: List[str] = field(default_factory=list)
    confidence_score: float = 0.5
    last_confirmed: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    evolution_history: List[Dict[str, Any]] = field(default_factory=list)
    qualia_links: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp)
        if not self.last_confirmed:
            self.last_confirmed = self.timestamp
        if not self.last_updated:
            self.last_updated = self.timestamp

@dataclass
class Evidence:
    """Evidence supporting or contradicting a belief"""
    evidence_id: str
    content: str
    evidence_type: EvidenceType
    strength: float  # 0.0 to 1.0
    source: str
    timestamp: datetime
    supports_belief: bool  # True if supports, False if contradicts
    context: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp)

@dataclass
class Contradiction:
    """Represents a contradiction between beliefs"""
    id: str
    belief_a_id: str
    belief_b_id: str
    contradiction_type: ContradictionType
    severity: float
    explanation: str
    detected_at: datetime
    resolved: bool = False
    resolution_strategy: str = ""
    resolution_date: Optional[datetime] = None
    
    def __post_init__(self):
        if isinstance(self.detected_at, str):
            self.detected_at = datetime.fromisoformat(self.detected_at)

@dataclass
class BeliefConflict:
    """Conflict between beliefs"""
    conflict_id: str
    belief_ids: List[str]
    conflict_type: str  # "contradiction", "tension", "inconsistency"
    severity: float  # 0.0 to 1.0
    description: str
    discovered_date: datetime
    resolution_strategy: Optional[str] = None
    resolved: bool = False
    resolution_date: Optional[datetime] = None
    
    def __post_init__(self):
        if isinstance(self.discovered_date, str):
            self.discovered_date = datetime.fromisoformat(self.discovered_date)

@dataclass
class ContextItem:
    """Individual context/event tracking for memory"""
    context_id: str
    event_type: str
    description: str
    place: Optional[str] = None
    time_reference: Optional[str] = None
    status: str = "planned"
    priority: int = 1
    timestamp: Optional[datetime] = None
    related_contexts: List[str] = field(default_factory=list)
    completion_status: float = 0.0
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        elif isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp)

@dataclass
class WorkingMemoryState:
    """Track multiple simultaneous actions/contexts for reference resolution"""
    active_contexts: Dict[str, ContextItem] = field(default_factory=dict)
    last_action: Optional[str] = None
    last_place: Optional[str] = None
    last_topic: Optional[str] = None
    last_goal: Optional[str] = None
    last_timestamp: Optional[datetime] = None
    action_status: str = "unknown"
    context_sequence: List[str] = field(default_factory=list)

@dataclass
class InteractionThread:
    """Track individual conversation threads for reference resolution"""
    interaction_id: int
    timestamp: datetime
    intent: str
    query: str
    status: str
    user_message: str
    ai_response: Optional[str] = None
    related_threads: List[int] = field(default_factory=list)
    
    def __post_init__(self):
        if isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp)

@dataclass
class EpisodicTurn:
    """Track individual conversation turns with full context"""
    turn_number: int
    timestamp: datetime
    user_message: str
    ai_response: str
    intent_detected: str
    entities_mentioned: List[str] = field(default_factory=list)
    emotional_tone: str = "neutral"
    context_references: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp)

@dataclass
class Memory:
    """Comprehensive memory representation"""
    memory_id: str
    content: str
    memory_type: MemoryType
    importance: MemoryImportance
    timestamp: datetime
    user_id: str
    context: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    related_memories: List[str] = field(default_factory=list)
    emotional_valence: float = 0.0  # -1.0 to 1.0
    access_count: int = 0
    last_accessed: Optional[datetime] = None
    decay_factor: float = 1.0
    consolidation_level: float = 0.0
    
    def __post_init__(self):
        if isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp)
        if not self.last_accessed:
            self.last_accessed = self.timestamp

# ============================================================================
# BELIEF ANALYSIS FUNCTIONALITY (FROM belief_analyzer.py)
# ============================================================================

class BeliefAnalyzer:
    """Analyze and manage beliefs, detect contradictions"""
    
    def __init__(self, belief_store_file: str = "belief_store.json"):
        self.belief_store_file = belief_store_file
        self.beliefs: Dict[str, Belief] = {}
        self.contradictions: Dict[str, Contradiction] = {}
        self.evidence_store: Dict[str, Evidence] = {}
        self.lock = threading.Lock()
        
        # Patterns for extracting beliefs from text
        self.belief_patterns = {
            BeliefType.FACTUAL: [
                r"(.+) is (.+)",
                r"(.+) are (.+)",
                r"(.+) has (.+)",
                r"(.+) was (.+)",
                r"(.+) will be (.+)",
                r"the fact that (.+)",
                r"it's true that (.+)",
            ],
            BeliefType.PERSONAL: [
                r"I am (.+)",
                r"I have (.+)",
                r"I live (.+)",
                r"I work (.+)",
                r"my (.+) is (.+)",
            ],
            BeliefType.PREFERENCE: [
                r"I like (.+)",
                r"I dislike (.+)",
                r"I prefer (.+)",
                r"I enjoy (.+)",
                r"I hate (.+)",
            ],
            BeliefType.OPINION: [
                r"I think (.+)",
                r"I believe (.+)",
                r"in my opinion (.+)",
                r"I feel that (.+)",
            ]
        }
        
        self.load_beliefs()
        logging.info("[BeliefAnalyzer] Belief analyzer initialized")

    def extract_beliefs_from_text(self, text: str, user: str, source: str = "conversation") -> List[Belief]:
        """Extract beliefs from conversational text"""
        beliefs = []
        text_lower = text.lower()
        
        for belief_type, patterns in self.belief_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text_lower, re.IGNORECASE)
                for match in matches:
                    belief_content = match.group(0)
                    
                    # Create belief
                    belief_id = self._generate_belief_id(belief_content, user)
                    belief = Belief(
                        id=belief_id,
                        content=belief_content,
                        belief_type=belief_type,
                        certainty=BeliefCertainty.MODERATE,
                        strength=0.6,
                        status=BeliefStatus.ACTIVE,
                        source=source,
                        timestamp=datetime.now(),
                        user=user,
                        context={"extraction_source": text}
                    )
                    
                    beliefs.append(belief)
        
        # Store extracted beliefs
        with self.lock:
            for belief in beliefs:
                self.beliefs[belief.id] = belief
        
        return beliefs

    def detect_contradictions(self, new_belief: Belief) -> List[Contradiction]:
        """Detect contradictions with existing beliefs"""
        contradictions = []
        
        with self.lock:
            for existing_id, existing_belief in self.beliefs.items():
                if existing_belief.user != new_belief.user:
                    continue
                
                if existing_belief.id == new_belief.id:
                    continue
                
                # Check for direct contradictions
                if self._are_beliefs_contradictory(existing_belief, new_belief):
                    contradiction = Contradiction(
                        id=f"contradiction_{int(time.time() * 1000)}",
                        belief_a_id=existing_belief.id,
                        belief_b_id=new_belief.id,
                        contradiction_type=ContradictionType.DIRECT,
                        severity=0.8,
                        explanation=f"'{existing_belief.content}' contradicts '{new_belief.content}'",
                        detected_at=datetime.now()
                    )
                    contradictions.append(contradiction)
                    self.contradictions[contradiction.id] = contradiction
        
        return contradictions

    def _are_beliefs_contradictory(self, belief_a: Belief, belief_b: Belief) -> bool:
        """Check if two beliefs are contradictory"""
        # Simple heuristic: look for opposing keywords
        content_a = belief_a.content.lower()
        content_b = belief_b.content.lower()
        
        # Check for direct negations
        if "not" in content_a and content_a.replace("not", "").strip() in content_b:
            return True
        if "not" in content_b and content_b.replace("not", "").strip() in content_a:
            return True
        
        # Check for opposing pairs
        opposing_pairs = [
            ("like", "dislike"), ("love", "hate"), ("good", "bad"),
            ("positive", "negative"), ("agree", "disagree"),
            ("yes", "no"), ("true", "false")
        ]
        
        for pos, neg in opposing_pairs:
            if (pos in content_a and neg in content_b) or (neg in content_a and pos in content_b):
                return True
        
        return False

    def _generate_belief_id(self, content: str, user: str) -> str:
        """Generate unique belief ID"""
        content_hash = hashlib.md5(f"{content}_{user}".encode()).hexdigest()[:8]
        return f"belief_{content_hash}_{int(time.time())}"

    def get_user_beliefs(self, user: str, belief_type: Optional[BeliefType] = None) -> List[Belief]:
        """Get beliefs for a specific user"""
        with self.lock:
            user_beliefs = [b for b in self.beliefs.values() if b.user == user]
            
            if belief_type:
                user_beliefs = [b for b in user_beliefs if b.belief_type == belief_type]
            
            return sorted(user_beliefs, key=lambda b: b.timestamp, reverse=True)

    def update_belief_confidence(self, belief_id: str, confidence_delta: float):
        """Update belief confidence based on new evidence"""
        with self.lock:
            if belief_id in self.beliefs:
                belief = self.beliefs[belief_id]
                old_confidence = belief.confidence_score
                belief.confidence_score = max(0.0, min(1.0, old_confidence + confidence_delta))
                belief.last_updated = datetime.now()
                
                logging.debug(f"[BeliefAnalyzer] Updated belief confidence: {old_confidence:.2f} -> {belief.confidence_score:.2f}")

    def save_beliefs(self):
        """Save beliefs to file"""
        try:
            data = {
                "beliefs": {bid: asdict(belief) for bid, belief in self.beliefs.items()},
                "contradictions": {cid: asdict(contradiction) for cid, contradiction in self.contradictions.items()},
                "evidence": {eid: asdict(evidence) for eid, evidence in self.evidence_store.items()},
                "last_updated": datetime.now().isoformat()
            }
            
            # Convert datetime objects to strings for JSON serialization
            self._serialize_datetime_fields(data)
            
            with open(self.belief_store_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
                
        except Exception as e:
            logging.error(f"[BeliefAnalyzer] Error saving beliefs: {e}")

    def load_beliefs(self):
        """Load beliefs from file"""
        try:
            if os.path.exists(self.belief_store_file):
                with open(self.belief_store_file, 'r') as f:
                    data = json.load(f)
                
                # Load beliefs
                for bid, belief_data in data.get("beliefs", {}).items():
                    self._deserialize_datetime_fields(belief_data)
                    belief = Belief(**belief_data)
                    self.beliefs[bid] = belief
                
                # Load contradictions
                for cid, contradiction_data in data.get("contradictions", {}).items():
                    self._deserialize_datetime_fields(contradiction_data)
                    contradiction = Contradiction(**contradiction_data)
                    self.contradictions[cid] = contradiction
                
                # Load evidence
                for eid, evidence_data in data.get("evidence", {}).items():
                    self._deserialize_datetime_fields(evidence_data)
                    evidence = Evidence(**evidence_data)
                    self.evidence_store[eid] = evidence
                
                logging.info(f"[BeliefAnalyzer] Loaded {len(self.beliefs)} beliefs, {len(self.contradictions)} contradictions")
        except Exception as e:
            logging.error(f"[BeliefAnalyzer] Error loading beliefs: {e}")

    def _serialize_datetime_fields(self, data: Dict[str, Any]):
        """Convert datetime objects to ISO strings for JSON serialization"""
        for category in ["beliefs", "contradictions", "evidence"]:
            if category in data:
                for item_data in data[category].values():
                    for field in ["timestamp", "detected_at", "discovered_date", "last_confirmed", "last_updated", "resolution_date"]:
                        if field in item_data and isinstance(item_data[field], datetime):
                            item_data[field] = item_data[field].isoformat()

    def _deserialize_datetime_fields(self, item_data: Dict[str, Any]):
        """Convert ISO strings back to datetime objects"""
        for field in ["timestamp", "detected_at", "discovered_date", "last_confirmed", "last_updated", "resolution_date"]:
            if field in item_data and isinstance(item_data[field], str):
                try:
                    item_data[field] = datetime.fromisoformat(item_data[field])
                except:
                    item_data[field] = None

# ============================================================================
# MEMORY SYSTEM FUNCTIONALITY (FROM memory.py)
# ============================================================================

class MemorySystem:
    """Comprehensive memory management system with context awareness"""
    
    def __init__(self, save_path: str = "local_memory.json"):
        self.save_path = Path(save_path)
        self.memories: Dict[str, Memory] = {}
        self.working_memory = WorkingMemoryState()
        self.interaction_threads: List[InteractionThread] = []
        self.episodic_turns: List[EpisodicTurn] = []
        self.context_history: List[Dict[str, Any]] = []
        self.lock = threading.Lock()
        
        # Memory parameters
        self.max_working_memory_items = 10
        self.episodic_memory_limit = 100
        self.memory_decay_rate = 0.01
        self.consolidation_threshold = 0.8
        
        # Load existing memories
        self.load_memories()
        
        # Start memory maintenance thread
        self.running = True
        self.maintenance_thread = threading.Thread(target=self._memory_maintenance_loop, daemon=True)
        self.maintenance_thread.start()
        
        logging.info("[MemorySystem] Memory system initialized")

    def store_memory(
        self, 
        content: str, 
        memory_type: MemoryType, 
        user_id: str,
        importance: MemoryImportance = MemoryImportance.MEDIUM,
        context: Dict[str, Any] = None,
        tags: List[str] = None,
        emotional_valence: float = 0.0
    ) -> str:
        """Store a new memory"""
        memory_id = f"memory_{int(time.time() * 1000)}_{random.randint(1000, 9999)}"
        
        memory = Memory(
            memory_id=memory_id,
            content=content,
            memory_type=memory_type,
            importance=importance,
            timestamp=datetime.now(),
            user_id=user_id,
            context=context or {},
            tags=tags or [],
            emotional_valence=emotional_valence
        )
        
        with self.lock:
            self.memories[memory_id] = memory
            
            # Link to related memories
            related_memories = self._find_related_memories(memory)
            memory.related_memories = [m.memory_id for m in related_memories[:5]]
            
            # Update related memories to link back
            for related_memory in related_memories[:3]:
                if memory_id not in related_memory.related_memories:
                    related_memory.related_memories.append(memory_id)
        
        logging.debug(f"[MemorySystem] Stored memory: {content[:50]}...")
        return memory_id

    def retrieve_memories(
        self, 
        user_id: str, 
        query: str = "", 
        memory_type: Optional[MemoryType] = None,
        limit: int = 10,
        min_importance: MemoryImportance = MemoryImportance.LOW
    ) -> List[Memory]:
        """Retrieve memories based on criteria"""
        with self.lock:
            candidate_memories = [
                m for m in self.memories.values() 
                if m.user_id == user_id and m.importance.value >= min_importance.value
            ]
            
            if memory_type:
                candidate_memories = [m for m in candidate_memories if m.memory_type == memory_type]
            
            # Simple relevance scoring (can be enhanced with embedding similarity)
            if query:
                scored_memories = []
                query_lower = query.lower()
                
                for memory in candidate_memories:
                    score = 0.0
                    content_lower = memory.content.lower()
                    
                    # Exact match bonus
                    if query_lower in content_lower:
                        score += 1.0
                    
                    # Word overlap scoring
                    query_words = set(query_lower.split())
                    content_words = set(content_lower.split())
                    overlap = len(query_words.intersection(content_words))
                    score += overlap / max(len(query_words), 1) * 0.5
                    
                    # Importance and recency bonus
                    score += memory.importance.value * 0.3
                    days_ago = (datetime.now() - memory.timestamp).days
                    score += max(0, 1 - days_ago / 30) * 0.2  # Recency bonus
                    
                    # Access frequency bonus
                    score += min(memory.access_count / 10, 0.2)
                    
                    if score > 0:
                        scored_memories.append((memory, score))
                
                # Sort by score and return top results
                scored_memories.sort(key=lambda x: x[1], reverse=True)
                result_memories = [m for m, _ in scored_memories[:limit]]
            else:
                # No query - return most recent and important
                result_memories = sorted(
                    candidate_memories,
                    key=lambda m: (m.importance.value, m.timestamp),
                    reverse=True
                )[:limit]
            
            # Update access counts
            for memory in result_memories:
                memory.access_count += 1
                memory.last_accessed = datetime.now()
            
            return result_memories

    def update_working_memory(self, context_updates: Dict[str, Any]):
        """Update working memory with new context"""
        with self.lock:
            current_time = datetime.now()
            
            # Update working memory fields
            for key, value in context_updates.items():
                if hasattr(self.working_memory, key):
                    setattr(self.working_memory, key, value)
            
            self.working_memory.last_timestamp = current_time
            
            # Add to context history
            self.context_history.append({
                "timestamp": current_time.isoformat(),
                "updates": context_updates
            })
            
            # Limit context history size
            if len(self.context_history) > 50:
                self.context_history = self.context_history[-50:]

    def add_interaction_thread(
        self, 
        interaction_id: int, 
        intent: str, 
        query: str, 
        user_message: str,
        status: str = "pending"
    ) -> InteractionThread:
        """Add new interaction thread"""
        thread = InteractionThread(
            interaction_id=interaction_id,
            timestamp=datetime.now(),
            intent=intent,
            query=query,
            status=status,
            user_message=user_message
        )
        
        with self.lock:
            self.interaction_threads.append(thread)
            
            # Limit thread history
            if len(self.interaction_threads) > 20:
                self.interaction_threads = self.interaction_threads[-20:]
        
        return thread

    def add_episodic_turn(
        self, 
        turn_number: int, 
        user_message: str, 
        ai_response: str,
        intent_detected: str = "general",
        entities_mentioned: List[str] = None,
        emotional_tone: str = "neutral"
    ) -> EpisodicTurn:
        """Add episodic conversation turn"""
        turn = EpisodicTurn(
            turn_number=turn_number,
            timestamp=datetime.now(),
            user_message=user_message,
            ai_response=ai_response,
            intent_detected=intent_detected,
            entities_mentioned=entities_mentioned or [],
            emotional_tone=emotional_tone
        )
        
        with self.lock:
            self.episodic_turns.append(turn)
            
            # Limit episodic memory
            if len(self.episodic_turns) > self.episodic_memory_limit:
                self.episodic_turns = self.episodic_turns[-self.episodic_memory_limit:]
        
        return turn

    def _find_related_memories(self, memory: Memory) -> List[Memory]:
        """Find memories related to the given memory"""
        related = []
        memory_content_lower = memory.content.lower()
        memory_words = set(memory_content_lower.split())
        
        for existing_memory in self.memories.values():
            if existing_memory.memory_id == memory.memory_id:
                continue
            
            if existing_memory.user_id != memory.user_id:
                continue
            
            # Calculate similarity based on word overlap
            existing_content_lower = existing_memory.content.lower()
            existing_words = set(existing_content_lower.split())
            
            overlap = len(memory_words.intersection(existing_words))
            similarity = overlap / max(len(memory_words.union(existing_words)), 1)
            
            if similarity > 0.2:  # Threshold for relatedness
                related.append(existing_memory)
        
        # Sort by similarity (approximate)
        return sorted(related, key=lambda m: len(set(m.content.lower().split()).intersection(memory_words)), reverse=True)

    def _memory_maintenance_loop(self):
        """Background memory maintenance"""
        while self.running:
            try:
                with self.lock:
                    current_time = datetime.now()
                    
                    # Apply memory decay
                    for memory in self.memories.values():
                        days_since_access = (current_time - memory.last_accessed).days
                        if days_since_access > 7:  # Decay after a week
                            memory.decay_factor = max(0.1, memory.decay_factor - self.memory_decay_rate)
                    
                    # Consolidate important memories
                    for memory in self.memories.values():
                        if memory.access_count > 5 and memory.consolidation_level < self.consolidation_threshold:
                            memory.consolidation_level = min(1.0, memory.consolidation_level + 0.1)
                
                # Save memories periodically
                self.save_memories()
                
            except Exception as e:
                logging.error(f"[MemorySystem] Error in maintenance loop: {e}")
            
            time.sleep(3600)  # Run hourly

    def get_memory_summary(self, user_id: str) -> str:
        """Get summary of user's memory state"""
        with self.lock:
            user_memories = [m for m in self.memories.values() if m.user_id == user_id]
            
            if not user_memories:
                return f"No memories stored for user {user_id}"
            
            # Count by type
            type_counts = defaultdict(int)
            importance_counts = defaultdict(int)
            
            for memory in user_memories:
                type_counts[memory.memory_type.value] += 1
                importance_counts[memory.importance.value] += 1
            
            summary = f"Memory Summary for {user_id}: {len(user_memories)} total memories\n"
            summary += f"By type: {dict(type_counts)}\n"
            summary += f"By importance: {dict(importance_counts)}\n"
            summary += f"Episodic turns: {len(self.episodic_turns)}\n"
            summary += f"Active contexts: {len(self.working_memory.active_contexts)}"
            
            return summary

    def save_memories(self):
        """Save memories to file"""
        try:
            data = {
                "memories": {mid: asdict(memory) for mid, memory in self.memories.items()},
                "working_memory": asdict(self.working_memory),
                "interaction_threads": [asdict(thread) for thread in self.interaction_threads],
                "episodic_turns": [asdict(turn) for turn in self.episodic_turns],
                "context_history": self.context_history,
                "last_updated": datetime.now().isoformat()
            }
            
            # Serialize datetime fields
            self._serialize_memory_datetime_fields(data)
            
            with open(self.save_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
                
        except Exception as e:
            logging.error(f"[MemorySystem] Error saving memories: {e}")

    def load_memories(self):
        """Load memories from file"""
        try:
            if self.save_path.exists():
                with open(self.save_path, 'r') as f:
                    data = json.load(f)
                
                # Load memories
                for mid, memory_data in data.get("memories", {}).items():
                    self._deserialize_memory_datetime_fields(memory_data)
                    # Convert enum strings back to enums
                    memory_data["memory_type"] = MemoryType(memory_data.get("memory_type", "episodic"))
                    memory_data["importance"] = MemoryImportance(memory_data.get("importance", 0.6))
                    
                    memory = Memory(**memory_data)
                    self.memories[mid] = memory
                
                # Load working memory
                working_memory_data = data.get("working_memory", {})
                if working_memory_data:
                    self._deserialize_memory_datetime_fields(working_memory_data)
                    self.working_memory = WorkingMemoryState(**working_memory_data)
                
                # Load interaction threads
                for thread_data in data.get("interaction_threads", []):
                    self._deserialize_memory_datetime_fields(thread_data)
                    thread = InteractionThread(**thread_data)
                    self.interaction_threads.append(thread)
                
                # Load episodic turns
                for turn_data in data.get("episodic_turns", []):
                    self._deserialize_memory_datetime_fields(turn_data)
                    turn = EpisodicTurn(**turn_data)
                    self.episodic_turns.append(turn)
                
                self.context_history = data.get("context_history", [])
                
                logging.info(f"[MemorySystem] Loaded {len(self.memories)} memories, {len(self.episodic_turns)} episodic turns")
        except Exception as e:
            logging.error(f"[MemorySystem] Error loading memories: {e}")

    def _serialize_memory_datetime_fields(self, data: Dict[str, Any]):
        """Serialize datetime fields for JSON storage"""
        for memory_data in data.get("memories", {}).values():
            for field in ["timestamp", "last_accessed"]:
                if field in memory_data and isinstance(memory_data[field], datetime):
                    memory_data[field] = memory_data[field].isoformat()
        
        # Working memory
        working_memory = data.get("working_memory", {})
        if "last_timestamp" in working_memory and isinstance(working_memory["last_timestamp"], datetime):
            working_memory["last_timestamp"] = working_memory["last_timestamp"].isoformat()
        
        # Interaction threads and episodic turns
        for thread_data in data.get("interaction_threads", []):
            if "timestamp" in thread_data and isinstance(thread_data["timestamp"], datetime):
                thread_data["timestamp"] = thread_data["timestamp"].isoformat()
        
        for turn_data in data.get("episodic_turns", []):
            if "timestamp" in turn_data and isinstance(turn_data["timestamp"], datetime):
                turn_data["timestamp"] = turn_data["timestamp"].isoformat()

    def _deserialize_memory_datetime_fields(self, item_data: Dict[str, Any]):
        """Deserialize datetime fields from JSON storage"""
        for field in ["timestamp", "last_accessed", "last_timestamp"]:
            if field in item_data and isinstance(item_data[field], str):
                try:
                    item_data[field] = datetime.fromisoformat(item_data[field])
                except:
                    item_data[field] = None

# ============================================================================
# UNIFIED BELIEF MEMORY MANAGER
# ============================================================================

class BeliefMemoryManager:
    """Unified manager for all belief and memory systems"""
    
    def __init__(self):
        # Initialize all subsystems
        self.belief_analyzer = BeliefAnalyzer()
        self.memory_system = MemorySystem()
        
        # Integration settings
        self.auto_belief_extraction = True
        self.cross_system_updates = True
        self.belief_memory_linking = True
        
        self.lock = threading.Lock()
        
        logging.info("[BeliefMemoryManager] Unified belief-memory system initialized")

    def process_user_input(self, user_id: str, user_message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process user input through belief and memory systems"""
        result = {
            "extracted_beliefs": [],
            "stored_memories": [],
            "detected_contradictions": [],
            "memory_updates": {}
        }
        
        # Extract beliefs from user message
        if self.auto_belief_extraction:
            extracted_beliefs = self.belief_analyzer.extract_beliefs_from_text(
                user_message, user_id, "conversation"
            )
            result["extracted_beliefs"] = [b.id for b in extracted_beliefs]
            
            # Check for contradictions
            for belief in extracted_beliefs:
                contradictions = self.belief_analyzer.detect_contradictions(belief)
                result["detected_contradictions"].extend([c.id for c in contradictions])
        
        # Store as episodic memory
        memory_id = self.memory_system.store_memory(
            content=user_message,
            memory_type=MemoryType.EPISODIC,
            user_id=user_id,
            importance=MemoryImportance.MEDIUM,
            context=context or {},
            tags=["user_input", "conversation"]
        )
        result["stored_memories"].append(memory_id)
        
        # Update working memory
        if context:
            self.memory_system.update_working_memory(context)
            result["memory_updates"] = context
        
        return result

    def get_user_context(self, user_id: str, query: str = "") -> Dict[str, Any]:
        """Get comprehensive user context including beliefs and memories"""
        context = {
            "beliefs": {},
            "memories": [],
            "working_memory": {},
            "recent_interactions": []
        }
        
        # Get user beliefs
        user_beliefs = self.belief_analyzer.get_user_beliefs(user_id)
        context["beliefs"] = {
            "total_count": len(user_beliefs),
            "by_type": {},
            "recent_beliefs": []
        }
        
        # Group beliefs by type
        belief_types = defaultdict(int)
        for belief in user_beliefs:
            belief_types[belief.belief_type.value] += 1
        context["beliefs"]["by_type"] = dict(belief_types)
        
        # Recent beliefs
        context["beliefs"]["recent_beliefs"] = [
            {
                "id": b.id,
                "content": b.content,
                "type": b.belief_type.value,
                "strength": b.strength,
                "timestamp": b.timestamp.isoformat()
            }
            for b in user_beliefs[:5]
        ]
        
        # Get relevant memories
        memories = self.memory_system.retrieve_memories(user_id, query, limit=10)
        context["memories"] = [
            {
                "id": m.memory_id,
                "content": m.content,
                "type": m.memory_type.value,
                "importance": m.importance.value,
                "timestamp": m.timestamp.isoformat()
            }
            for m in memories
        ]
        
        # Working memory
        context["working_memory"] = {
            "active_contexts": len(self.memory_system.working_memory.active_contexts),
            "last_action": self.memory_system.working_memory.last_action,
            "last_topic": self.memory_system.working_memory.last_topic
        }
        
        # Recent interactions
        context["recent_interactions"] = [
            {
                "turn": turn.turn_number,
                "user_message": turn.user_message[:100],
                "ai_response": turn.ai_response[:100] if turn.ai_response else None,
                "timestamp": turn.timestamp.isoformat()
            }
            for turn in self.memory_system.episodic_turns[-3:]
        ]
        
        return context

    def get_unified_summary(self, user_id: str) -> str:
        """Get comprehensive summary of belief and memory state"""
        summary = "=== BELIEF & MEMORY SYSTEM SUMMARY ===\n\n"
        
        # Belief summary
        user_beliefs = self.belief_analyzer.get_user_beliefs(user_id)
        summary += f"BELIEFS ({len(user_beliefs)} total):\n"
        
        if user_beliefs:
            belief_type_counts = defaultdict(int)
            for belief in user_beliefs:
                belief_type_counts[belief.belief_type.value] += 1
            
            for belief_type, count in belief_type_counts.items():
                summary += f"  • {belief_type}: {count}\n"
            
            summary += f"  • Recent: {user_beliefs[0].content[:50]}...\n" if user_beliefs else ""
        
        summary += "\n"
        
        # Memory summary
        summary += self.memory_system.get_memory_summary(user_id) + "\n\n"
        
        # Contradictions
        contradictions = [c for c in self.belief_analyzer.contradictions.values() if not c.resolved]
        if contradictions:
            summary += f"Active contradictions: {len(contradictions)}\n"
        
        return summary

    def shutdown(self):
        """Shutdown all subsystems"""
        try:
            self.memory_system.running = False
            self.belief_analyzer.save_beliefs()
            self.memory_system.save_memories()
            logging.info("[BeliefMemoryManager] Belief-memory system shutdown complete")
        except Exception as e:
            logging.error(f"[BeliefMemoryManager] Error during shutdown: {e}")

# ============================================================================
# BACKWARD COMPATIBILITY ALIASES
# ============================================================================

# Belief Analyzer aliases
from ai.belief_memory import BeliefAnalyzer as belief_analyzer_instance
from ai.belief_memory import BeliefAnalyzer

# Memory System aliases - Use existing memory system for compatibility
try:
    from ai.memory import UserMemorySystem as memory_instance
    from ai.memory import store_memory as original_store_memory
    
    # Override the store_memory function to be compatible
    def store_memory_compatible(content: str, memory_type=None, user_id: str = "default", **kwargs):
        """Compatible store_memory function that works with existing memory system"""
        # Use the existing memory system's interface
        return original_store_memory(content, user_id=user_id, **kwargs) if hasattr(original_store_memory, '__call__') else f"memory_{int(time.time() * 1000)}"
    
    # Replace our store_memory with the compatible version
    store_memory = store_memory_compatible
    
except ImportError:
    # Use our own implementation if the existing system isn't available
    from ai.belief_memory import MemorySystem as memory_instance
    from ai.belief_memory import MemorySystem

# Additional backward compatibility for specific modules
try:
    # belief_memory_refiner.py compatibility
    class BeliefMemoryRefiner:
        def __init__(self):
            self.manager = BeliefMemoryManager()
        
        def refine_beliefs(self, user_id: str):
            return self.manager.get_user_context(user_id)
    
    belief_memory_refiner_instance = BeliefMemoryRefiner()
    
    # belief_qualia_linking.py compatibility
    class BeliefQualiaLinker:
        def __init__(self):
            self.manager = BeliefMemoryManager()
        
        def link_beliefs_to_qualia(self, belief_id: str, qualia_data: Dict[str, Any]):
            # Placeholder implementation
            return True
    
    belief_qualia_linking_instance = BeliefQualiaLinker()
    
    # belief_reinforcement.py compatibility  
    class BeliefReinforcementSystem:
        def __init__(self):
            self.manager = BeliefMemoryManager()
        
        def reinforce_belief(self, belief_id: str, reinforcement_type: str):
            return True  # Simplified implementation
    
    belief_reinforcement_instance = BeliefReinforcementSystem()
    
    # memory_context_corrector.py compatibility
    class MemoryContextCorrector:
        def __init__(self):
            self.manager = BeliefMemoryManager()
        
        def correct_context(self, user_id: str, corrections: Dict[str, Any]):
            return self.manager.memory_system.update_working_memory(corrections)
    
    memory_context_corrector_instance = MemoryContextCorrector()
    
    # belief_evolution_tracker.py compatibility
    class BeliefEvolutionTracker:
        def __init__(self):
            self.manager = BeliefMemoryManager()
        
        def track_belief_evolution(self, belief, trigger, context=None):
            return True  # Simplified implementation
    
    belief_evolution_tracker_instance = BeliefEvolutionTracker()
    
except Exception as e:
    logging.warning(f"[BeliefMemory] Error creating compatibility classes: {e}")

# Create global instance for backward compatibility
belief_memory_manager = BeliefMemoryManager()

# Legacy function aliases
def extract_beliefs_from_text(text: str, user: str, source: str = "conversation") -> List[Belief]:
    """Legacy function for extracting beliefs"""
    return belief_memory_manager.belief_analyzer.extract_beliefs_from_text(text, user, source)

def store_memory(content: str, memory_type: MemoryType = MemoryType.EPISODIC, user_id: str = "default", **kwargs) -> str:
    """Legacy function for storing memories"""
    return belief_memory_manager.memory_system.store_memory(content, memory_type, user_id, **kwargs)

def retrieve_memories(user_id: str, query: str = "", **kwargs) -> List[Memory]:
    """Legacy function for retrieving memories"""
    return belief_memory_manager.memory_system.retrieve_memories(user_id, query, **kwargs)

def get_user_beliefs(user: str, belief_type: Optional[BeliefType] = None) -> List[Belief]:
    """Legacy function for getting user beliefs"""
    return belief_memory_manager.belief_analyzer.get_user_beliefs(user, belief_type)

# Export main classes and functions
__all__ = [
    'BeliefMemoryManager', 'BeliefAnalyzer', 'MemorySystem',
    'Belief', 'Evidence', 'Contradiction', 'Memory', 'ContextItem', 'WorkingMemoryState',
    'BeliefType', 'BeliefCertainty', 'BeliefStrength', 'BeliefStatus', 'MemoryType', 'MemoryImportance',
    'belief_memory_manager', 'extract_beliefs_from_text', 'store_memory', 'retrieve_memories', 'get_user_beliefs'
]

logging.info("[BeliefMemory] Consolidated belief-memory system loaded successfully")