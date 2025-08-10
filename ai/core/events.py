"""
ai/core/events.py - Event definitions for inter-module communication

This module contains event type definitions and event handling protocols
to allow clean communication between modules without creating import cycles.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional
from datetime import datetime

from .types import AttentionPriority, SystemEvent


# ============================================================================
# Core Event Types
# ============================================================================

class EventType(Enum):
    """Core system event types"""
    # User interaction events
    USER_SPEECH_DETECTED = "user_speech_detected"
    USER_SPEECH_RECOGNIZED = "user_speech_recognized"
    USER_MESSAGE_RECEIVED = "user_message_received"
    
    # AI response events  
    AI_THINKING_STARTED = "ai_thinking_started"
    AI_RESPONSE_CHUNK = "ai_response_chunk"
    AI_RESPONSE_COMPLETE = "ai_response_complete"
    
    # Voice system events
    VOICE_TRAINING_STARTED = "voice_training_started"
    VOICE_PROFILE_UPDATED = "voice_profile_updated"
    SPEAKER_IDENTIFIED = "speaker_identified"
    VOICE_QUALITY_ASSESSED = "voice_quality_assessed"
    
    # Audio system events
    AUDIO_PLAYBACK_STARTED = "audio_playback_started"
    AUDIO_PLAYBACK_COMPLETE = "audio_playback_complete"
    AUDIO_INTERRUPTED = "audio_interrupted"
    MICROPHONE_ACTIVATED = "microphone_activated"
    
    # Session events
    SESSION_STARTED = "session_started"
    SESSION_ENDED = "session_ended"
    SESSION_PAUSED = "session_paused"
    SESSION_RESUMED = "session_resumed"
    
    # System events
    MODULE_INITIALIZED = "module_initialized"
    MODULE_ERROR = "module_error"
    CONFIGURATION_CHANGED = "configuration_changed"
    

# ============================================================================
# Specialized Event Classes
# ============================================================================

@dataclass
class SpeechEvent(SystemEvent):
    """Speech-related system event"""
    text: str = ""
    audio_data: Optional[Any] = None
    confidence: float = 0.0
    speaker_id: Optional[str] = None
    
    def __post_init__(self):
        if not hasattr(self, 'event_type'):
            self.event_type = EventType.USER_SPEECH_RECOGNIZED.value


@dataclass  
class ChatEvent(SystemEvent):
    """Chat/AI response event"""
    message: str = ""
    user_id: str = ""
    response_id: Optional[str] = None
    is_streaming: bool = False
    chunk_index: Optional[int] = None
    
    def __post_init__(self):
        if not hasattr(self, 'event_type'):
            self.event_type = EventType.AI_RESPONSE_CHUNK.value


@dataclass
class VoiceEvent(SystemEvent):
    """Voice recognition/training event"""  
    user_id: str = ""
    profile_updated: bool = False
    confidence: float = 0.0
    quality_score: float = 0.0
    
    def __post_init__(self):
        if not hasattr(self, 'event_type'):
            self.event_type = EventType.SPEAKER_IDENTIFIED.value


@dataclass
class AudioEvent(SystemEvent):
    """Audio system event"""
    audio_id: Optional[str] = None
    duration: float = 0.0
    volume_level: float = 0.0
    is_interrupted: bool = False
    
    def __post_init__(self):
        if not hasattr(self, 'event_type'):
            self.event_type = EventType.AUDIO_PLAYBACK_STARTED.value


# ============================================================================
# Event Bus Interface
# ============================================================================

class EventBus:
    """Simple event bus for inter-module communication"""
    
    def __init__(self):
        self._subscribers = {}
        self._lock = threading.Lock()
    
    def subscribe(self, event_type: str, callback: Callable[[SystemEvent], None]):
        """Subscribe to events of a specific type"""
        with self._lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            self._subscribers[event_type].append(callback)
    
    def unsubscribe(self, event_type: str, callback: Callable[[SystemEvent], None]):
        """Unsubscribe from events"""
        with self._lock:
            if event_type in self._subscribers:
                try:
                    self._subscribers[event_type].remove(callback)
                except ValueError:
                    pass  # Callback not found
    
    def publish(self, event: SystemEvent):
        """Publish an event to all subscribers"""
        with self._lock:
            subscribers = self._subscribers.get(event.event_type, []).copy()
        
        # Call subscribers outside the lock to avoid deadlocks
        for callback in subscribers:
            try:
                callback(event)
            except Exception as e:
                # Log error but don't let it stop other subscribers
                import logging
                logging.error(f"Error in event subscriber: {e}")


# ============================================================================
# Event Factory Functions
# ============================================================================

def create_speech_event(text: str, speaker_id: str = "", confidence: float = 0.0) -> SpeechEvent:
    """Create a speech recognition event"""
    return SpeechEvent(
        event_type=EventType.USER_SPEECH_RECOGNIZED.value,
        source_module="voice_recognition",
        data={"text": text, "speaker_id": speaker_id, "confidence": confidence},
        text=text,
        speaker_id=speaker_id,
        confidence=confidence,
        priority=AttentionPriority.HIGH
    )


def create_chat_response_event(message: str, user_id: str, is_streaming: bool = False) -> ChatEvent:
    """Create a chat response event"""
    return ChatEvent(
        event_type=EventType.AI_RESPONSE_CHUNK.value if is_streaming else EventType.AI_RESPONSE_COMPLETE.value,
        source_module="ai_chat",
        data={"message": message, "user_id": user_id, "is_streaming": is_streaming},
        message=message,
        user_id=user_id,
        is_streaming=is_streaming,
        priority=AttentionPriority.HIGH
    )


def create_voice_profile_event(user_id: str, confidence: float = 0.0) -> VoiceEvent:
    """Create a voice profile update event"""
    return VoiceEvent(
        event_type=EventType.VOICE_PROFILE_UPDATED.value,
        source_module="voice_manager", 
        data={"user_id": user_id, "confidence": confidence},
        user_id=user_id,
        confidence=confidence,
        profile_updated=True,
        priority=AttentionPriority.MEDIUM
    )


def create_audio_playback_event(audio_id: str = "", duration: float = 0.0) -> AudioEvent:
    """Create an audio playback event"""
    return AudioEvent(
        event_type=EventType.AUDIO_PLAYBACK_STARTED.value,
        source_module="audio_output",
        data={"audio_id": audio_id, "duration": duration},
        audio_id=audio_id,
        duration=duration,
        priority=AttentionPriority.MEDIUM
    )


# ============================================================================
# Global Event Bus Instance
# ============================================================================

# Import threading here to avoid any issues
import threading
from typing import Callable

# Global event bus instance for the application
global_event_bus = EventBus()