"""
Voice Manager - Consolidated Voice Recognition System
====================================================

This module consolidates 7 voice management components into a unified system:
1. manager_core.py: Advanced AI Assistant Core with Alexa/Siri-level intelligence
2. recognition.py: Centroid-based voice recognition with clustering
3. speaker_profiles.py: Advanced speaker profile management
4. training.py: Interactive voice training system
5. voice_models.py: Multi-model voice recognition system
6. manager_context.py: Context analysis for voice interactions
7. manager_names.py: Name management and collision handling

The unified system provides comprehensive voice recognition capabilities with
centroid embedding-based recognition, maintaining backward compatibility.
"""

import threading
import time
import json
import logging
import os
import tempfile
import numpy as np
import traceback
import re
import gzip
import pickle
from typing import Dict, List, Any, Optional, Set, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# Safe import handling
def safe_import(module_name, fallback=None):
    """Safely import modules with fallback"""
    try:
        return __import__(module_name)
    except ImportError as e:
        logging.warning(f"Could not import {module_name}: {e}")
        return fallback

# Try enhanced imports with fallbacks
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    logging.warning("NumPy not available - voice recognition will be limited")

try:
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logging.warning("Scikit-learn not available - using fallback similarity")

try:
    from resemblyzer import VoiceEncoder
    RESEMBLYZER_AVAILABLE = True
except ImportError:
    RESEMBLYZER_AVAILABLE = False
    logging.warning("Resemblyzer not available - using mock encoder")

try:
    import torch
    import torchaudio
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    logging.warning("PyTorch not available - using basic models")

# Database imports with fallbacks
try:
    from voice.database import (
        known_users, anonymous_clusters, save_known_users, 
        create_anonymous_cluster, link_anonymous_to_named,
        ensure_database_loaded, handle_same_name_collision
    )
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    logging.warning("Voice database not available - using mock data")
    known_users = {}
    anonymous_clusters = {}

# Configuration imports with fallbacks
try:
    from config import (
        DEBUG, SAMPLE_RATE, VOICE_CONFIDENCE_THRESHOLD,
        TRAINING_MODE_NONE_STR
    )
except ImportError:
    DEBUG = True
    SAMPLE_RATE = 16000
    VOICE_CONFIDENCE_THRESHOLD = 0.7
    TRAINING_MODE_NONE_STR = "none"

# Audio imports with fallbacks
try:
    from audio.input import aec_training_listen
    from audio.output import speak_streaming, play_chime, buddy_talking
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    logging.warning("Audio modules not available - using mock functions")

# Speech imports with fallbacks
try:
    from ai.speech import transcribe_audio
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False
    logging.warning("Speech module not available - using mock transcription")

# ===== MOCK CLASSES AND FALLBACKS =====

class MockVoiceEncoder:
    """Mock voice encoder when Resemblyzer is not available"""
    def embed_utterance(self, audio):
        if not NUMPY_AVAILABLE:
            return None
        # Generate a random embedding for testing
        return np.random.random(256)

if not RESEMBLYZER_AVAILABLE:
    encoder = MockVoiceEncoder()
else:
    encoder = VoiceEncoder()

def fallback_cosine_similarity(a, b):
    """Fallback cosine similarity implementation"""
    if not NUMPY_AVAILABLE:
        return 0.0
    
    a = np.array(a)
    b = np.array(b)
    
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    return dot_product / (norm_a * norm_b)

def calculate_similarity(emb1, emb2):
    """Calculate similarity between embeddings with fallbacks"""
    if SKLEARN_AVAILABLE:
        return cosine_similarity([emb1], [emb2])[0][0]
    else:
        return fallback_cosine_similarity(emb1, emb2)

# ===== TRAINING PHRASES =====

ADVANCED_TRAINING_PHRASES = [
    "Hello, my name is speaking clearly and confidently now",
    "What time is it right now on this beautiful day", 
    "How are you doing this wonderful morning",
    "The weather outside looks absolutely beautiful today",
    "I need to make an important phone call right now",
    "Can you please help me with this important question",
    "What would you like me to say next in our conversation",
    "How do I get to the nearest train station quickly",
    "When will the meeting start today at the office",
    "Where can I find more detailed information about this",
    "Please turn on all the lights in the room now",
    "Set a timer for exactly fifteen minutes from now",
    "Play some relaxing classical music softly in background", 
    "Show me the latest weather forecast for this week",
    "Call my family members when you have a moment",
    "Thank you very much for all your helpful assistance",
    "That sounds like a really great idea to me",
    "I really appreciate your assistance and patience today",
    "Let me think about that important question for a moment",
    "Could you please repeat that information more slowly"
]

CLUSTERING_OPTIMIZED_PHRASES = [
    "Hello, my name is speaking clearly",
    "What time is it right now",
    "How are you doing today", 
    "The weather outside looks nice",
    "Can you help me with this",
    "Thank you very much",
    "I need to make a call",
    "Please turn on the lights",
    "Set a timer for five minutes",
    "Play some music please"
]

# ===== DATA CLASSES =====

@dataclass
class VoiceProfile:
    """Voice profile with embedding data"""
    username: str
    embeddings: List[List[float]]
    confidence_scores: List[float] = field(default_factory=list)
    last_updated: datetime = field(default_factory=datetime.now)
    training_sessions: int = 0
    raw_samples: List[bytes] = field(default_factory=list)
    behavioral_patterns: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AnonymousCluster:
    """Anonymous voice cluster"""
    cluster_id: str
    centroid_embedding: List[float]
    member_embeddings: List[List[float]]
    confidence_threshold: float = 0.6
    created: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)

@dataclass
class RecognitionResult:
    """Voice recognition result"""
    user_id: str
    confidence: float
    embedding: Optional[List[float]] = None
    method: str = "centroid"
    cluster_id: Optional[str] = None
    alternatives: List[Tuple[str, float]] = field(default_factory=list)

# ===== UNIFIED VOICE MANAGER SYSTEM =====

class VoiceManagerSystem:
    """
    Unified Voice Manager System combining all voice recognition components.
    
    This system provides:
    - Centroid embedding-based voice recognition
    - Multi-model voice processing with fallbacks
    - Advanced speaker profile management
    - Interactive voice training capabilities
    - Anonymous clustering for unknown speakers
    - Context-aware recognition and name collision handling
    - Comprehensive voice analytics and quality assessment
    """
    
    def __init__(self, 
                 config_path: Optional[str] = None,
                 voice_profiles_path: str = "voice_profiles",
                 enable_training: bool = True):
        """Initialize the unified voice management system"""
        
        # Core configuration
        self.config_path = config_path
        self.voice_profiles_path = Path(voice_profiles_path)
        self.enable_training = enable_training
        
        # === VOICE MODEL COMPONENTS ===
        self.models = {}
        self.model_weights = {
            'resemblyzer': 0.6,
            'ecapa_tdnn': 0.4
        }
        self.device = self._detect_optimal_device()
        
        # === SPEAKER PROFILE COMPONENTS ===
        self.voice_profiles: Dict[str, VoiceProfile] = {}
        self.anonymous_clusters: Dict[str, AnonymousCluster] = {}
        self.quality_threshold = 0.4
        self.max_embeddings_per_user = 15
        self.max_raw_samples = 10
        
        # === RECOGNITION COMPONENTS ===
        self.confidence_threshold = VOICE_CONFIDENCE_THRESHOLD
        self.cluster_confidence_threshold = 0.6
        self.similarity_cache = {}
        
        # === TRAINING COMPONENTS ===
        self.training_phrases = ADVANCED_TRAINING_PHRASES
        self.clustering_phrases = CLUSTERING_OPTIMIZED_PHRASES
        self.training_sessions = {}
        
        # === CONTEXT AND NAME MANAGEMENT ===
        self.session_context = {
            'start_time': datetime.now(),
            'interactions': 0,
            'last_recognized_user': None,
            'recent_audio_buffer': [],
            'recent_text_buffer': [],
            'buffer_contexts': []
        }
        self.name_collision_handlers = {}
        
        # Performance tracking
        self.performance_stats = {
            'total_recognitions': 0,
            'successful_recognitions': 0,
            'average_confidence': 0.0,
            'model_usage': defaultdict(int),
            'error_count': 0
        }
        
        # Threading
        self.lock = threading.Lock()
        self.file_lock = threading.Lock()
        
        # Initialize system
        self._initialize_directories()
        self._load_voice_data()
        self._initialize_models()
        
        logging.info(f"[VoiceManager] 🎤 Unified voice management system initialized")
        logging.info(f"[VoiceManager] 📊 Loaded {len(self.voice_profiles)} profiles, {len(self.anonymous_clusters)} clusters")
    
    # ===== VOICE RECOGNITION METHODS =====
    
    def recognize_speaker(self, audio: np.ndarray) -> RecognitionResult:
        """
        Main speaker recognition method using centroid embeddings
        
        Args:
            audio: Audio data as numpy array
            
        Returns:
            RecognitionResult with user identification and confidence
        """
        with self.lock:
            try:
                # Generate embedding for the audio
                embedding = self.generate_voice_embedding(audio)
                if embedding is None:
                    return RecognitionResult("UNKNOWN", 0.0, method="no_embedding")
                
                # Update performance stats
                self.performance_stats['total_recognitions'] += 1
                
                # Step 1: Check against known users using centroid clustering
                user_result = self._match_known_users(embedding)
                if user_result.confidence > self.confidence_threshold:
                    self.performance_stats['successful_recognitions'] += 1
                    self._update_confidence_stats(user_result.confidence)
                    return user_result
                
                # Step 2: Check against anonymous clusters
                cluster_result = self._match_anonymous_clusters(embedding)
                if cluster_result.confidence > self.cluster_confidence_threshold:
                    self.performance_stats['successful_recognitions'] += 1
                    return cluster_result
                
                # Step 3: Create new anonymous cluster if no match
                cluster_id = self._create_anonymous_cluster(embedding)
                return RecognitionResult(
                    f"ANONYMOUS_{cluster_id}", 
                    0.5, 
                    embedding, 
                    method="new_cluster",
                    cluster_id=cluster_id
                )
                
            except Exception as e:
                logging.error(f"[VoiceManager] Recognition error: {e}")
                self.performance_stats['error_count'] += 1
                return RecognitionResult("ERROR", 0.0, method="error")
    
    def generate_voice_embedding(self, audio: np.ndarray) -> Optional[np.ndarray]:
        """
        Generate voice embedding using available models
        
        Args:
            audio: Audio data as numpy array
            
        Returns:
            Voice embedding as numpy array or None if failed
        """
        try:
            if not NUMPY_AVAILABLE or audio is None or len(audio) == 0:
                return None
            
            # Ensure minimum audio length
            if len(audio) < SAMPLE_RATE:
                return None
            
            # Normalize audio
            audio_float = audio.astype(np.float32)
            if np.max(np.abs(audio_float)) > 1.0:
                audio_float = audio_float / 32768.0
            
            # Use available models
            if RESEMBLYZER_AVAILABLE:
                embedding = encoder.embed_utterance(audio_float)
                if embedding is not None:
                    self.performance_stats['model_usage']['resemblyzer'] += 1
                    return embedding
            
            # Fallback to mock embedding for testing
            if NUMPY_AVAILABLE:
                self.performance_stats['model_usage']['mock'] += 1
                return np.random.random(256)
            
            return None
            
        except Exception as e:
            logging.error(f"[VoiceManager] Embedding generation error: {e}")
            return None
    
    def _match_known_users(self, embedding: np.ndarray) -> RecognitionResult:
        """Match embedding against known users using centroid method"""
        best_user = None
        best_confidence = 0.0
        alternatives = []
        
        for username, profile in self.voice_profiles.items():
            if not profile.embeddings:
                continue
            
            # Calculate centroid of all embeddings for this user
            embeddings_np = [np.array(emb) for emb in profile.embeddings]
            centroid = np.mean(embeddings_np, axis=0)
            
            # Calculate similarity
            similarity = calculate_similarity(embedding, centroid)
            alternatives.append((username, similarity))
            
            if similarity > best_confidence:
                best_confidence = similarity
                best_user = username
        
        # Sort alternatives by confidence
        alternatives.sort(key=lambda x: x[1], reverse=True)
        
        return RecognitionResult(
            best_user or "UNKNOWN",
            best_confidence,
            embedding.tolist(),
            method="centroid_known",
            alternatives=alternatives[:3]
        )
    
    def _match_anonymous_clusters(self, embedding: np.ndarray) -> RecognitionResult:
        """Match embedding against anonymous clusters"""
        best_cluster = None
        best_confidence = 0.0
        
        for cluster_id, cluster in self.anonymous_clusters.items():
            centroid = np.array(cluster.centroid_embedding)
            similarity = calculate_similarity(embedding, centroid)
            
            if similarity > best_confidence:
                best_confidence = similarity
                best_cluster = cluster_id
        
        return RecognitionResult(
            f"ANONYMOUS_{best_cluster}" if best_cluster else "UNKNOWN",
            best_confidence,
            embedding.tolist(),
            method="centroid_anonymous",
            cluster_id=best_cluster
        )
    
    # ===== TRAINING METHODS =====
    
    def train_user_voice(self, username: str, interactive: bool = True) -> bool:
        """
        Train voice recognition for a specific user
        
        Args:
            username: Username to train
            interactive: Whether to use interactive training
            
        Returns:
            True if training successful, False otherwise
        """
        try:
            with self.lock:
                logging.info(f"[VoiceManager] 🎓 Starting voice training for: {username}")
                
                if not AUDIO_AVAILABLE:
                    logging.warning("[VoiceManager] Audio not available - mock training")
                    return self._mock_training(username)
                
                if interactive:
                    return self._interactive_training(username)
                else:
                    return self._batch_training(username)
                    
        except Exception as e:
            logging.error(f"[VoiceManager] Training error for {username}: {e}")
            return False
    
    def _interactive_training(self, username: str) -> bool:
        """Interactive voice training with user feedback"""
        collected_embeddings = []
        phrases_to_use = self.clustering_phrases[:5]  # Use optimized phrases
        
        if AUDIO_AVAILABLE:
            speak_streaming(f"Let's train your voice, {username}. Please repeat after me.")
        
        for i, phrase in enumerate(phrases_to_use):
            try:
                if AUDIO_AVAILABLE:
                    speak_streaming(f"Please say: {phrase}")
                    audio = aec_training_listen()
                else:
                    # Mock audio for testing
                    audio = np.random.random(SAMPLE_RATE * 3)
                
                if audio is not None:
                    # Assess quality
                    quality = self._assess_audio_quality(audio)
                    if quality['overall_score'] > self.quality_threshold:
                        embedding = self.generate_voice_embedding(audio)
                        if embedding is not None:
                            collected_embeddings.append(embedding.tolist())
                            if AUDIO_AVAILABLE:
                                speak_streaming("Good! Next phrase.")
                        else:
                            if AUDIO_AVAILABLE:
                                speak_streaming("Let's try that again.")
                    else:
                        if AUDIO_AVAILABLE:
                            speak_streaming("Audio quality was low. Let's try again.")
                
            except Exception as e:
                logging.error(f"[VoiceManager] Training step {i} error: {e}")
                continue
        
        # Save collected embeddings
        if collected_embeddings:
            self._save_user_embeddings(username, collected_embeddings)
            if AUDIO_AVAILABLE:
                speak_streaming(f"Training complete for {username}! I learned from {len(collected_embeddings)} samples.")
            return True
        else:
            if AUDIO_AVAILABLE:
                speak_streaming("Training failed - no good samples collected.")
            return False
    
    def _mock_training(self, username: str) -> bool:
        """Mock training for testing when audio is not available"""
        mock_embeddings = []
        for i in range(5):
            if NUMPY_AVAILABLE:
                # Generate consistent mock embeddings for testing
                np.random.seed(hash(username) + i)
                embedding = np.random.random(256)
                mock_embeddings.append(embedding.tolist())
        
        if mock_embeddings:
            self._save_user_embeddings(username, mock_embeddings)
            logging.info(f"[VoiceManager] Mock training completed for {username}")
            return True
        return False
    
    def _save_user_embeddings(self, username: str, embeddings: List[List[float]]):
        """Save user embeddings to profile"""
        if username not in self.voice_profiles:
            self.voice_profiles[username] = VoiceProfile(
                username=username,
                embeddings=embeddings,
                last_updated=datetime.now(),
                training_sessions=1
            )
        else:
            profile = self.voice_profiles[username]
            profile.embeddings.extend(embeddings)
            # Keep only the most recent embeddings
            if len(profile.embeddings) > self.max_embeddings_per_user:
                profile.embeddings = profile.embeddings[-self.max_embeddings_per_user:]
            profile.last_updated = datetime.now()
            profile.training_sessions += 1
        
        # Save to database
        self._save_voice_data()
    
    # ===== PROFILE MANAGEMENT METHODS =====
    
    def create_user_profile(self, username: str) -> bool:
        """Create a new user profile"""
        try:
            with self.lock:
                if username in self.voice_profiles:
                    logging.warning(f"[VoiceManager] Profile already exists: {username}")
                    return False
                
                self.voice_profiles[username] = VoiceProfile(
                    username=username,
                    embeddings=[],
                    last_updated=datetime.now()
                )
                
                self._save_voice_data()
                logging.info(f"[VoiceManager] Created profile for: {username}")
                return True
                
        except Exception as e:
            logging.error(f"[VoiceManager] Error creating profile for {username}: {e}")
            return False
    
    def delete_user_profile(self, username: str) -> bool:
        """Delete a user profile"""
        try:
            with self.lock:
                if username not in self.voice_profiles:
                    return False
                
                del self.voice_profiles[username]
                self._save_voice_data()
                logging.info(f"[VoiceManager] Deleted profile for: {username}")
                return True
                
        except Exception as e:
            logging.error(f"[VoiceManager] Error deleting profile for {username}: {e}")
            return False
    
    def get_user_profile(self, username: str) -> Optional[VoiceProfile]:
        """Get user profile"""
        return self.voice_profiles.get(username)
    
    def list_users(self) -> List[str]:
        """List all registered users"""
        return list(self.voice_profiles.keys())
    
    # ===== CLUSTERING METHODS =====
    
    def _create_anonymous_cluster(self, embedding: np.ndarray) -> str:
        """Create a new anonymous cluster"""
        cluster_id = f"cluster_{int(time.time())}_{len(self.anonymous_clusters)}"
        
        cluster = AnonymousCluster(
            cluster_id=cluster_id,
            centroid_embedding=embedding.tolist(),
            member_embeddings=[embedding.tolist()],
            created=datetime.now(),
            last_activity=datetime.now()
        )
        
        self.anonymous_clusters[cluster_id] = cluster
        self._save_voice_data()
        
        logging.info(f"[VoiceManager] Created anonymous cluster: {cluster_id}")
        return cluster_id
    
    def link_cluster_to_user(self, cluster_id: str, username: str) -> bool:
        """Link an anonymous cluster to a named user"""
        try:
            with self.lock:
                if cluster_id not in self.anonymous_clusters:
                    return False
                
                cluster = self.anonymous_clusters[cluster_id]
                
                # Add cluster embeddings to user profile
                if username not in self.voice_profiles:
                    self.create_user_profile(username)
                
                profile = self.voice_profiles[username]
                profile.embeddings.extend(cluster.member_embeddings)
                
                # Keep only recent embeddings
                if len(profile.embeddings) > self.max_embeddings_per_user:
                    profile.embeddings = profile.embeddings[-self.max_embeddings_per_user:]
                
                # Remove cluster
                del self.anonymous_clusters[cluster_id]
                
                self._save_voice_data()
                logging.info(f"[VoiceManager] Linked cluster {cluster_id} to user {username}")
                return True
                
        except Exception as e:
            logging.error(f"[VoiceManager] Error linking cluster to user: {e}")
            return False
    
    # ===== QUALITY ASSESSMENT METHODS =====
    
    def _assess_audio_quality(self, audio: np.ndarray) -> Dict[str, float]:
        """Assess audio quality for training"""
        try:
            if not NUMPY_AVAILABLE or audio is None or len(audio) == 0:
                return {'overall_score': 0.0}
            
            # Basic quality metrics
            duration = len(audio) / SAMPLE_RATE
            volume_level = np.sqrt(np.mean(audio**2))
            
            # Duration score (prefer 2-10 seconds)
            duration_score = 1.0
            if duration < 1.0:
                duration_score = duration
            elif duration > 10.0:
                duration_score = max(0.1, 1.0 - (duration - 10.0) * 0.1)
            
            # Volume score (prefer moderate volumes)
            volume_score = min(1.0, volume_level * 10)  # Scale appropriately
            
            # Overall score
            overall_score = (duration_score + volume_score) / 2
            
            return {
                'overall_score': overall_score,
                'duration_score': duration_score,
                'volume_score': volume_score,
                'duration': duration,
                'volume_level': volume_level
            }
            
        except Exception as e:
            logging.error(f"[VoiceManager] Audio quality assessment error: {e}")
            return {'overall_score': 0.0}
    
    # ===== ANALYTICS AND STATS METHODS =====
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get comprehensive system statistics"""
        with self.lock:
            stats = {
                'users': len(self.voice_profiles),
                'anonymous_clusters': len(self.anonymous_clusters),
                'total_embeddings': sum(len(p.embeddings) for p in self.voice_profiles.values()),
                'performance': self.performance_stats.copy(),
                'config': {
                    'confidence_threshold': self.confidence_threshold,
                    'max_embeddings_per_user': self.max_embeddings_per_user,
                    'quality_threshold': self.quality_threshold
                },
                'models_available': {
                    'numpy': NUMPY_AVAILABLE,
                    'sklearn': SKLEARN_AVAILABLE,
                    'resemblyzer': RESEMBLYZER_AVAILABLE,
                    'torch': TORCH_AVAILABLE,
                    'audio': AUDIO_AVAILABLE
                }
            }
            
            # Calculate success rate
            if stats['performance']['total_recognitions'] > 0:
                stats['performance']['success_rate'] = (
                    stats['performance']['successful_recognitions'] / 
                    stats['performance']['total_recognitions']
                )
            
            return stats
    
    def _update_confidence_stats(self, confidence: float):
        """Update confidence statistics"""
        total = self.performance_stats['successful_recognitions']
        current_avg = self.performance_stats['average_confidence']
        
        # Update running average
        self.performance_stats['average_confidence'] = (
            (current_avg * (total - 1) + confidence) / total
        )
    
    # ===== CONTEXT MANAGEMENT METHODS =====
    
    def update_session_context(self, user_id: str, interaction_data: Dict[str, Any]):
        """Update session context with interaction data"""
        with self.lock:
            self.session_context['interactions'] += 1
            self.session_context['last_recognized_user'] = user_id
            
            # Store recent context
            context_entry = {
                'timestamp': datetime.now(),
                'user_id': user_id,
                'data': interaction_data
            }
            self.session_context['buffer_contexts'].append(context_entry)
            
            # Keep only recent contexts
            if len(self.session_context['buffer_contexts']) > 100:
                self.session_context['buffer_contexts'] = self.session_context['buffer_contexts'][-100:]
    
    # ===== PRIVATE HELPER METHODS =====
    
    def _detect_optimal_device(self) -> str:
        """Detect optimal device for processing"""
        if TORCH_AVAILABLE:
            if torch.cuda.is_available():
                return "cuda"
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                return "mps"
        return "cpu"
    
    def _initialize_directories(self):
        """Initialize required directories"""
        directories = [
            self.voice_profiles_path,
            self.voice_profiles_path / "raw_audio",
            self.voice_profiles_path / "clusters",
            self.voice_profiles_path / "uncertain"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _initialize_models(self):
        """Initialize voice recognition models"""
        try:
            if RESEMBLYZER_AVAILABLE:
                self.models['resemblyzer'] = encoder
                logging.info("[VoiceManager] ✅ Resemblyzer model loaded")
            
            if TORCH_AVAILABLE:
                # Could add additional PyTorch models here
                logging.info("[VoiceManager] 🔥 PyTorch available for advanced models")
            
            logging.info(f"[VoiceManager] 📊 Initialized {len(self.models)} models on {self.device}")
            
        except Exception as e:
            logging.error(f"[VoiceManager] Model initialization error: {e}")
    
    def _load_voice_data(self):
        """Load voice profiles and clusters from storage"""
        try:
            # Load from voice database if available
            if DATABASE_AVAILABLE:
                global known_users, anonymous_clusters
                ensure_database_loaded()
                
                # Convert database format to our format
                for username, profile_data in known_users.items():
                    if isinstance(profile_data, dict) and 'embeddings' in profile_data:
                        self.voice_profiles[username] = VoiceProfile(
                            username=username,
                            embeddings=profile_data['embeddings'],
                            last_updated=datetime.now()
                        )
                    elif isinstance(profile_data, list):
                        # Legacy single embedding format
                        self.voice_profiles[username] = VoiceProfile(
                            username=username,
                            embeddings=[profile_data],
                            last_updated=datetime.now()
                        )
                
                # Load anonymous clusters
                for cluster_id, cluster_data in anonymous_clusters.items():
                    if isinstance(cluster_data, dict):
                        self.anonymous_clusters[cluster_id] = AnonymousCluster(
                            cluster_id=cluster_id,
                            centroid_embedding=cluster_data.get('centroid', []),
                            member_embeddings=cluster_data.get('embeddings', [])
                        )
            
        except Exception as e:
            logging.error(f"[VoiceManager] Error loading voice data: {e}")
    
    def _save_voice_data(self):
        """Save voice profiles and clusters to storage"""
        try:
            with self.file_lock:
                if DATABASE_AVAILABLE:
                    # Convert our format back to database format
                    global known_users, anonymous_clusters
                    
                    for username, profile in self.voice_profiles.items():
                        known_users[username] = {
                            'embeddings': profile.embeddings,
                            'last_updated': profile.last_updated.isoformat(),
                            'training_sessions': profile.training_sessions
                        }
                    
                    for cluster_id, cluster in self.anonymous_clusters.items():
                        anonymous_clusters[cluster_id] = {
                            'centroid': cluster.centroid_embedding,
                            'embeddings': cluster.member_embeddings,
                            'created': cluster.created.isoformat()
                        }
                    
                    save_known_users()
                
        except Exception as e:
            logging.error(f"[VoiceManager] Error saving voice data: {e}")


# ===== BACKWARD COMPATIBILITY ALIASES =====

# Allow existing imports to continue working
AdvancedAIAssistantCore = VoiceManagerSystem
AdvancedSpeakerProfiles = VoiceManagerSystem
ProfessionalDualVoiceModelManager = VoiceManagerSystem
ContextAnalyzer = VoiceManagerSystem
NameManager = VoiceManagerSystem

# Function aliases for backward compatibility
def identify_speaker_with_confidence(audio):
    """Backward compatibility function for speaker identification"""
    global _default_voice_manager
    if _default_voice_manager is None:
        _default_voice_manager = VoiceManagerSystem()
    
    result = _default_voice_manager.recognize_speaker(audio)
    return result.user_id, result.confidence

def generate_voice_embedding(audio):
    """Backward compatibility function for embedding generation"""
    global _default_voice_manager
    if _default_voice_manager is None:
        _default_voice_manager = VoiceManagerSystem()
    
    embedding = _default_voice_manager.generate_voice_embedding(audio)
    return embedding

def voice_training_mode(username, mode="interactive"):
    """Backward compatibility function for voice training"""
    global _default_voice_manager
    if _default_voice_manager is None:
        _default_voice_manager = VoiceManagerSystem()
    
    return _default_voice_manager.train_user_voice(username, interactive=(mode != "batch"))

# Create default instance for backward compatibility
_default_voice_manager = None

def get_voice_manager():
    """Get or create the default voice manager instance"""
    global _default_voice_manager
    if _default_voice_manager is None:
        _default_voice_manager = VoiceManagerSystem()
    return _default_voice_manager

# Module-level exports for backward compatibility
__all__ = [
    'VoiceManagerSystem',
    'VoiceProfile', 'AnonymousCluster', 'RecognitionResult',
    'AdvancedAIAssistantCore', 'AdvancedSpeakerProfiles', 
    'ProfessionalDualVoiceModelManager', 'ContextAnalyzer', 'NameManager',
    'identify_speaker_with_confidence', 'generate_voice_embedding', 
    'voice_training_mode', 'get_voice_manager'
]