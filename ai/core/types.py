"""
Shared core types and lightweight interfaces for AI modules.

This module provides neutral interfaces and data structures used across
cognition modules (attention, workspace, emotion, entropy, memory, chat)
to break import cycles and provide consistent typing.
"""
from typing import Protocol, TypedDict, List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod


# ============================================================================
# ATTENTION & WORKSPACE TYPES
# ============================================================================

class AttentionPriority(Enum):
    """Priority levels for attention requests"""
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"
    CRITICAL = "critical"

class ProcessingMode(Enum):
    """Processing modes for consciousness"""
    CONSCIOUS = "conscious"
    UNCONSCIOUS = "unconscious"
    AUTOMATIC = "automatic"

@dataclass
class AttentionRequest:
    """Lightweight attention request data structure"""
    source: str
    content: str
    priority: AttentionPriority
    mode: ProcessingMode
    duration: float = 5.0
    tags: List[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []


# ============================================================================
# EMOTION & MOOD TYPES  
# ============================================================================

class EmotionType(Enum):
    """Basic emotion types"""
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    ANTICIPATION = "anticipation"
    TRUST = "trust"
    CURIOSITY = "curiosity"
    CONTENTMENT = "contentment"
    EXCITEMENT = "excitement"
    CALM = "calm"
    NEUTRAL = "neutral"

class MoodType(Enum):
    """Overall mood states"""
    VERY_POSITIVE = "very_positive"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    VERY_NEGATIVE = "very_negative"

@dataclass
class EmotionalState:
    """Lightweight emotional state representation"""
    primary_emotion: EmotionType
    intensity: float = 0.5
    arousal: float = 0.5
    valence: float = 0.5
    mood: MoodType = MoodType.NEUTRAL


# ============================================================================
# MEMORY TYPES
# ============================================================================

class MemoryType(Enum):
    """Types of memory storage"""
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    WORKING = "working"
    PROCEDURAL = "procedural"
    CONVERSATION = "conversation"

@dataclass
class MemoryItem:
    """Basic memory item structure"""
    content: str
    memory_type: MemoryType
    timestamp: float
    importance: float = 0.5
    tags: List[str] = None
    decay_rate: float = 0.1

    def __post_init__(self):
        if self.tags is None:
            self.tags = []


# ============================================================================
# ENTROPY & UNCERTAINTY TYPES
# ============================================================================

class EntropyType(Enum):
    """Types of entropy/uncertainty"""
    COGNITIVE = "cognitive"
    EMOTIONAL = "emotional"
    BEHAVIORAL = "behavioral"
    DECISION = "decision"
    TEMPORAL = "temporal"

@dataclass
class EntropyEvent:
    """Entropy injection event"""
    entropy_type: EntropyType
    intensity: float
    parameters: Dict[str, Any] = None

    def __post_init__(self):
        if self.parameters is None:
            self.parameters = {}


# ============================================================================
# CHAT & RESPONSE TYPES
# ============================================================================

class ResponseMode(Enum):
    """Response generation modes"""
    STREAMING = "streaming"
    COMPLETE = "complete"
    ENHANCED = "enhanced"
    FUSION = "fusion"

@dataclass
class ChatMessage:
    """Basic chat message structure"""
    role: str  # "user", "assistant", "system"
    content: str
    timestamp: float
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class StreamingContext(TypedDict, total=False):
    """Context for streaming responses"""
    user: str
    language: str
    mode: ResponseMode
    memory_context: bool
    emotional_modulation: bool


# ============================================================================
# PROTOCOLS FOR MINIMAL INTERFACES
# ============================================================================

class EmotionalProcessor(Protocol):
    """Minimal interface for emotional processing"""
    
    def process_emotional_context(self, text: str, user: str) -> Dict[str, Any]:
        """Process emotional context from text"""
        ...

    def get_current_emotional_state(self) -> EmotionalState:
        """Get current emotional state"""
        ...


class AttentionManager(Protocol):
    """Minimal interface for attention management"""
    
    def request_attention(self, request: AttentionRequest) -> bool:
        """Request attention from the system"""
        ...
    
    def get_current_focus(self) -> Optional[str]:
        """Get current attention focus"""
        ...


class MemoryInterface(Protocol):
    """Minimal interface for memory operations"""
    
    def store_memory(self, item: MemoryItem) -> bool:
        """Store a memory item"""
        ...
    
    def retrieve_memories(self, query: str, memory_type: Optional[MemoryType] = None) -> List[MemoryItem]:
        """Retrieve relevant memories"""
        ...


class EntropyProvider(Protocol):
    """Minimal interface for entropy injection"""
    
    def should_inject_entropy(self, context: str) -> bool:
        """Determine if entropy should be injected"""
        ...
    
    def get_entropy_parameters(self, entropy_type: EntropyType) -> Dict[str, Any]:
        """Get parameters for entropy injection"""
        ...


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_attention_request(
    source: str,
    content: str,
    priority: str = "medium",
    mode: str = "conscious",
    duration: float = 5.0,
    tags: Optional[List[str]] = None
) -> AttentionRequest:
    """Create an attention request with enum conversion"""
    return AttentionRequest(
        source=source,
        content=content,
        priority=AttentionPriority(priority.lower()),
        mode=ProcessingMode(mode.lower()),
        duration=duration,
        tags=tags or []
    )

def create_emotional_state(
    emotion: str = "neutral",
    intensity: float = 0.5,
    mood: str = "neutral"
) -> EmotionalState:
    """Create an emotional state with enum conversion"""
    return EmotionalState(
        primary_emotion=EmotionType(emotion.lower()),
        intensity=max(0.0, min(1.0, intensity)),
        mood=MoodType(mood.lower())
    )

def create_memory_item(
    content: str,
    memory_type: str = "episodic",
    timestamp: float = 0.0,
    importance: float = 0.5,
    tags: Optional[List[str]] = None
) -> MemoryItem:
    """Create a memory item with enum conversion"""
    import time
    return MemoryItem(
        content=content,
        memory_type=MemoryType(memory_type.lower()),
        timestamp=timestamp or time.time(),
        importance=max(0.0, min(1.0, importance)),
        tags=tags or []
    )