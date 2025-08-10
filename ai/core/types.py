"""
ai/core/types.py - Neutral boundary types to break import cycles

This module contains core types, enums, dataclasses and protocols that are shared
across the ai, voice, and audio modules. By centralizing these here, we can break
import cycles while maintaining type safety.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any, Optional, Callable, Protocol
from datetime import datetime


# ============================================================================
# Core Processing Types
# ============================================================================

class ProcessingMode(Enum):
    """Consciousness processing modes"""
    CONSCIOUS = "conscious"
    UNCONSCIOUS = "unconscious" 
    PRECONSCIOUS = "preconscious"


class AttentionPriority(Enum):
    """Priority levels for attention systems"""
    CRITICAL = 10
    HIGH = 8
    MEDIUM = 5
    LOW = 3
    MINIMAL = 1


# ============================================================================
# Response and Message Types
# ============================================================================

@dataclass
class ChatResponse:
    """Standard response from AI chat systems"""
    content: str
    user: str
    language: str = "en"
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StreamingChunk:
    """Chunk of streaming response data"""
    content: str
    chunk_id: int
    is_final: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# Voice and Audio Types  
# ============================================================================

@dataclass
class VoiceProfile:
    """Basic voice profile information"""
    user_id: str
    embeddings: List[Any] = field(default_factory=list)
    confidence_threshold: float = 0.7
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AudioData:
    """Audio data container"""
    samples: Any  # numpy array or similar
    sample_rate: int
    duration: float
    format: str = "pcm16"
    metadata: Dict[str, Any] = field(default_factory=dict)


class AudioState(Enum):
    """Audio processing states"""
    IDLE = "idle"
    LISTENING = "listening"
    PROCESSING = "processing"
    SPEAKING = "speaking"
    ERROR = "error"


# ============================================================================
# User and Session Types
# ============================================================================

@dataclass  
class UserContext:
    """Context information about current user"""
    user_id: str
    display_name: str
    is_anonymous: bool = False
    session_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class SessionState(Enum):
    """Session states"""
    INACTIVE = "inactive"
    ACTIVE = "active" 
    PAUSED = "paused"
    ENDING = "ending"


# ============================================================================
# Event and Notification Types
# ============================================================================

@dataclass
class SystemEvent:
    """System-level event for inter-module communication"""
    event_type: str
    source_module: str
    data: Any
    timestamp: datetime = field(default_factory=datetime.now)
    priority: AttentionPriority = AttentionPriority.MEDIUM


# ============================================================================
# Protocols for Dependency Injection
# ============================================================================

class SpeechProvider(Protocol):
    """Protocol for speech/TTS providers"""
    
    def speak_text(self, text: str, voice: Optional[str] = None) -> None:
        """Speak the given text"""
        ...
    
    def speak_streaming(self, text: str, voice: Optional[str] = None) -> None:
        """Speak text in streaming fashion"""
        ...


class ChatProvider(Protocol):
    """Protocol for chat/LLM providers"""
    
    def generate_response(self, prompt: str, user: str, language: str = "en") -> str:
        """Generate a single response"""
        ...
    
    def generate_streaming(self, prompt: str, user: str, language: str = "en") -> Any:
        """Generate streaming response chunks"""
        ...


class VoiceRecognitionProvider(Protocol):
    """Protocol for voice recognition providers"""
    
    def identify_speaker(self, audio_data: AudioData) -> str:
        """Identify speaker from audio"""
        ...
    
    def train_voice(self, user_id: str, audio_samples: List[AudioData]) -> bool:
        """Train voice recognition for user"""
        ...


# ============================================================================
# Configuration Types
# ============================================================================

@dataclass
class CoreConfig:
    """Core configuration settings"""
    debug_mode: bool = False
    log_level: str = "INFO"
    enable_streaming: bool = True
    default_language: str = "en"
    session_timeout: float = 300.0  # 5 minutes
    
    # Audio settings
    audio_sample_rate: int = 16000
    audio_chunk_size: int = 1024
    
    # Voice settings  
    voice_confidence_threshold: float = 0.7
    voice_training_samples: int = 15
    
    # Chat settings
    chat_max_tokens: int = 500
    chat_temperature: float = 0.7