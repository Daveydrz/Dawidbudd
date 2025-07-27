#!/usr/bin/env python3
"""
Async Consciousness Processor - Background Consciousness Processing for Performance
Created: 2025-01-18
Purpose: Move inner monologue, reflection, and consciousness processing to background
        threads so the user doesn't wait for them before getting a response.
"""

import threading
import time
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, field
import queue
from enum import Enum

class ProcessingType(Enum):
    """Types of consciousness processing"""
    INNER_MONOLOGUE = "inner_monologue"
    REFLECTION = "reflection"
    MEMORY_UPDATE = "memory_update"
    BELIEF_PROCESSING = "belief_processing"
    EMOTIONAL_PROCESSING = "emotional_processing"
    CONSCIOUSNESS_UPDATE = "consciousness_update"

@dataclass
class ProcessingTask:
    """A background consciousness processing task"""
    task_type: ProcessingType
    text: str
    user_id: str
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    priority: int = 1  # 1 = high, 5 = low

class AsyncConsciousnessProcessor:
    """
    Background processor for consciousness tasks that don't need to block user responses
    """
    
    def __init__(self):
        self.processing_queue = queue.PriorityQueue()
        self.worker_thread = None
        self.running = False
        self.processed_count = 0
        self.error_count = 0
        
        # Import consciousness modules
        self._import_consciousness_modules()
        
        logging.info("[AsyncConsciousness] 🧠 Async consciousness processor initialized")
    
    def _import_consciousness_modules(self):
        """Import consciousness modules for background processing"""
        try:
            from ai.inner_monologue import inner_monologue
            from ai.cognitive_integration import cognitive_integrator
            from ai.emotion import emotion_engine
            from ai.memory import get_user_memory
            from ai.belief_analyzer import belief_analyzer
            
            self.inner_monologue = inner_monologue
            self.cognitive_integrator = cognitive_integrator
            self.emotion_engine = emotion_engine
            self.get_user_memory = get_user_memory
            self.belief_analyzer = belief_analyzer
            
            logging.info("[AsyncConsciousness] ✅ Consciousness modules imported")
            
        except ImportError as e:
            logging.warning(f"[AsyncConsciousness] ⚠️ Some consciousness modules not available: {e}")
            self.inner_monologue = None
            self.cognitive_integrator = None
    
    def start(self):
        """Start the background processing thread"""
        if self.running:
            return
            
        self.running = True
        self.worker_thread = threading.Thread(target=self._processing_loop, daemon=True)
        self.worker_thread.start()
        logging.info("[AsyncConsciousness] ✅ Background consciousness processing started")
    
    def stop(self):
        """Stop the background processing"""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=5.0)
        logging.info("[AsyncConsciousness] 🛑 Background consciousness processing stopped")
    
    def queue_inner_monologue(self, text: str, user_id: str, context: Dict[str, Any] = None):
        """Queue inner monologue processing in background"""
        task = ProcessingTask(
            ProcessingType.INNER_MONOLOGUE,
            text,
            user_id,
            context or {},
            priority=2  # Medium priority
        )
        self.processing_queue.put((task.priority, time.time(), task))
        logging.debug(f"[AsyncConsciousness] 💭 Queued inner monologue for {user_id}")
    
    def queue_reflection(self, text: str, user_id: str, context: Dict[str, Any] = None):
        """Queue reflection processing in background"""
        task = ProcessingTask(
            ProcessingType.REFLECTION,
            text,
            user_id,
            context or {},
            priority=3  # Lower priority
        )
        self.processing_queue.put((task.priority, time.time(), task))
        logging.debug(f"[AsyncConsciousness] 🤔 Queued reflection for {user_id}")
    
    def queue_memory_update(self, text: str, user_id: str, context: Dict[str, Any] = None):
        """Queue memory update processing in background"""
        task = ProcessingTask(
            ProcessingType.MEMORY_UPDATE,
            text,
            user_id,
            context or {},
            priority=4  # Lower priority
        )
        self.processing_queue.put((task.priority, time.time(), task))
        logging.debug(f"[AsyncConsciousness] 💾 Queued memory update for {user_id}")
    
    def queue_belief_processing(self, text: str, user_id: str, context: Dict[str, Any] = None):
        """Queue belief processing in background"""
        task = ProcessingTask(
            ProcessingType.BELIEF_PROCESSING,
            text,
            user_id,
            context or {},
            priority=4  # Lower priority
        )
        self.processing_queue.put((task.priority, time.time(), task))
        logging.debug(f"[AsyncConsciousness] 🧩 Queued belief processing for {user_id}")
    
    def queue_emotional_processing(self, text: str, user_id: str, context: Dict[str, Any] = None):
        """Queue emotional processing in background"""
        task = ProcessingTask(
            ProcessingType.EMOTIONAL_PROCESSING,
            text,
            user_id,
            context or {},
            priority=3  # Medium priority
        )
        self.processing_queue.put((task.priority, time.time(), task))
        logging.debug(f"[AsyncConsciousness] 🎭 Queued emotional processing for {user_id}")
    
    def _processing_loop(self):
        """Main background processing loop"""
        while self.running:
            try:
                # Get next task (blocks for up to 1 second)
                try:
                    _, timestamp, task = self.processing_queue.get(timeout=1.0)
                except queue.Empty:
                    continue
                
                # Process the task
                self._process_task(task)
                self.processed_count += 1
                
                # Mark task as done
                self.processing_queue.task_done()
                
            except Exception as e:
                logging.error(f"[AsyncConsciousness] ❌ Processing loop error: {e}")
                self.error_count += 1
                time.sleep(0.1)  # Brief pause on error
    
    def _process_task(self, task: ProcessingTask):
        """Process a single consciousness task"""
        try:
            if task.task_type == ProcessingType.INNER_MONOLOGUE:
                self._process_inner_monologue(task)
            elif task.task_type == ProcessingType.REFLECTION:
                self._process_reflection(task)
            elif task.task_type == ProcessingType.MEMORY_UPDATE:
                self._process_memory_update(task)
            elif task.task_type == ProcessingType.BELIEF_PROCESSING:
                self._process_belief_processing(task)
            elif task.task_type == ProcessingType.EMOTIONAL_PROCESSING:
                self._process_emotional_processing(task)
            
            logging.debug(f"[AsyncConsciousness] ✅ Processed {task.task_type.value} for {task.user_id}")
            
        except Exception as e:
            logging.error(f"[AsyncConsciousness] ❌ Error processing {task.task_type.value}: {e}")
    
    def _process_inner_monologue(self, task: ProcessingTask):
        """Process inner monologue in background"""
        if not self.inner_monologue:
            return
            
        try:
            from ai.inner_monologue import ThoughtType
            
            # Trigger inner monologue thought
            self.inner_monologue.trigger_thought(
                f"User {task.user_id} said: {task.text}",
                {"user_id": task.user_id, "interaction_type": "conversation"},
                ThoughtType.OBSERVATION
            )
            
        except Exception as e:
            logging.error(f"[AsyncConsciousness] ❌ Inner monologue processing error: {e}")
    
    def _process_reflection(self, task: ProcessingTask):
        """Process reflection in background"""
        if not self.inner_monologue:
            return
            
        try:
            from ai.inner_monologue import ThoughtType
            
            # Generate reflective thought
            self.inner_monologue.trigger_thought(
                f"Reflecting on interaction with {task.user_id}: {task.text[:50]}...",
                {"user_id": task.user_id, "interaction_type": "reflection"},
                ThoughtType.REFLECTION
            )
            
        except Exception as e:
            logging.error(f"[AsyncConsciousness] ❌ Reflection processing error: {e}")
    
    def _process_memory_update(self, task: ProcessingTask):
        """Process memory updates in background"""
        try:
            if self.get_user_memory:
                user_memory = self.get_user_memory(task.user_id)
                # Memory updates are handled automatically by the memory system
                # This is just a placeholder for potential future memory processing
                
        except Exception as e:
            logging.error(f"[AsyncConsciousness] ❌ Memory update processing error: {e}")
    
    def _process_belief_processing(self, task: ProcessingTask):
        """Process belief analysis in background"""
        try:
            if self.belief_analyzer:
                # Analyze text for beliefs in background
                belief_analysis = self.belief_analyzer.analyze_text_for_beliefs(task.text, task.user_id)
                
        except Exception as e:
            logging.error(f"[AsyncConsciousness] ❌ Belief processing error: {e}")
    
    def _process_emotional_processing(self, task: ProcessingTask):
        """Process emotional responses in background"""
        try:
            if self.emotion_engine:
                # Process emotional context in background
                self.emotion_engine.process_external_stimulus(
                    f"User {task.user_id} said: {task.text}",
                    {"user_id": task.user_id, "input": task.text}
                )
                
        except Exception as e:
            logging.error(f"[AsyncConsciousness] ❌ Emotional processing error: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get processor status"""
        return {
            "running": self.running,
            "queue_size": self.processing_queue.qsize(),
            "processed_count": self.processed_count,
            "error_count": self.error_count,
            "error_rate": self.error_count / max(self.processed_count, 1)
        }

# Global instance
async_consciousness_processor = AsyncConsciousnessProcessor()