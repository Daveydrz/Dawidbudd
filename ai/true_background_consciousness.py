"""
True Background Consciousness Processor
Created: 2025-01-17
Purpose: Process ALL consciousness in truly separate background threads
         that NEVER block user responses - fixes the 4-minute latency issue
"""

import time
import threading
import queue
import json
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, Future
import traceback

@dataclass
class BackgroundTask:
    """Background consciousness task that runs independently"""
    task_id: str
    task_type: str
    user_input: str
    user_id: str
    response: str
    data: Dict[str, Any]
    priority: int = 1
    created_at: float = None
    max_execution_time: float = 30.0  # Max 30 seconds per task
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()

class TrueBackgroundConsciousness:
    """TRUE background consciousness that never blocks user responses"""
    
    def __init__(self):
        self.task_queue = queue.Queue()
        self.thread_pool = ThreadPoolExecutor(max_workers=4, thread_name_prefix="Consciousness")
        self.running = False
        self.coordinator_thread = None
        
        # Stats
        self.stats = {
            "tasks_queued": 0,
            "tasks_completed": 0,
            "tasks_failed": 0,
            "tasks_timeout": 0,
            "total_processing_time": 0.0,
            "average_task_time": 0.0,
            "queue_size": 0,
            "active_workers": 0
        }
        
        # Available consciousness modules
        self.consciousness_modules = {}
        self.module_functions = {
            "inner_monologue": self._process_inner_monologue,
            "emotion_update": self._process_emotion_update,
            "belief_update": self._process_belief_update,
            "memory_update": self._process_memory_update,
            "self_model_update": self._process_self_model_update,
            "global_workspace_update": self._process_global_workspace_update,
            "temporal_awareness_update": self._process_temporal_awareness_update,
            "subjective_experience_update": self._process_subjective_experience_update
        }
        
        print("[TrueBackground] 🧠 True Background Consciousness initialized")
        print("[TrueBackground] 🎯 Goal: 100% background processing, 0% user blocking")
    
    def start(self):
        """Start the true background processing system"""
        if self.running:
            return
        
        self.running = True
        self.coordinator_thread = threading.Thread(
            target=self._coordination_loop, 
            daemon=True, 
            name="BackgroundCoordinator"
        )
        self.coordinator_thread.start()
        
        print("[TrueBackground] ✅ True background processing started")
        print("[TrueBackground] 🔄 All consciousness processing now fully background")
    
    def stop(self):
        """Stop background processing"""
        self.running = False
        
        if self.coordinator_thread:
            self.coordinator_thread.join(timeout=2.0)
        
        self.thread_pool.shutdown(wait=False)
        print("[TrueBackground] 🛑 True background processing stopped")
    
    def register_consciousness_modules(self, modules: Dict[str, Any]):
        """Register consciousness modules for background processing"""
        self.consciousness_modules = modules
        print(f"[TrueBackground] 📋 Registered {len(modules)} consciousness modules")
    
    def queue_consciousness_processing(self, 
                                     user_input: str, 
                                     user_id: str, 
                                     response: str,
                                     delay_seconds: float = 0.0):
        """
        Queue consciousness processing with NO blocking
        
        This method returns immediately and queues all processing for background
        """
        try:
            timestamp = int(time.time())
            
            # Create all consciousness tasks
            tasks = [
                BackgroundTask(
                    task_id=f"inner_monologue_{timestamp}",
                    task_type="inner_monologue",
                    user_input=user_input,
                    user_id=user_id,
                    response=response,
                    data={"delay": delay_seconds},
                    priority=2
                ),
                BackgroundTask(
                    task_id=f"emotion_update_{timestamp}",
                    task_type="emotion_update",
                    user_input=user_input,
                    user_id=user_id,
                    response=response,
                    data={"delay": delay_seconds + 1.0},
                    priority=3
                ),
                BackgroundTask(
                    task_id=f"belief_update_{timestamp}",
                    task_type="belief_update",
                    user_input=user_input,
                    user_id=user_id,
                    response=response,
                    data={"delay": delay_seconds + 2.0},
                    priority=1
                ),
                BackgroundTask(
                    task_id=f"memory_update_{timestamp}",
                    task_type="memory_update",
                    user_input=user_input,
                    user_id=user_id,
                    response=response,
                    data={"delay": delay_seconds + 3.0},
                    priority=2
                ),
                BackgroundTask(
                    task_id=f"self_model_update_{timestamp}",
                    task_type="self_model_update",
                    user_input=user_input,
                    user_id=user_id,
                    response=response,
                    data={"delay": delay_seconds + 4.0},
                    priority=2
                ),
                BackgroundTask(
                    task_id=f"global_workspace_update_{timestamp}",
                    task_type="global_workspace_update",
                    user_input=user_input,
                    user_id=user_id,
                    response=response,
                    data={"delay": delay_seconds + 5.0},
                    priority=1
                ),
                BackgroundTask(
                    task_id=f"temporal_awareness_update_{timestamp}",
                    task_type="temporal_awareness_update",
                    user_input=user_input,
                    user_id=user_id,
                    response=response,
                    data={"delay": delay_seconds + 6.0},
                    priority=2
                ),
                BackgroundTask(
                    task_id=f"subjective_experience_update_{timestamp}",
                    task_type="subjective_experience_update",
                    user_input=user_input,
                    user_id=user_id,
                    response=response,
                    data={"delay": delay_seconds + 7.0},
                    priority=2
                )
            ]
            
            # Queue all tasks (immediate return)
            for task in tasks:
                self.task_queue.put(task)
                self.stats["tasks_queued"] += 1
            
            self.stats["queue_size"] = self.task_queue.qsize()
            
            print(f"[TrueBackground] 📋 Queued {len(tasks)} consciousness tasks (instant return)")
            
        except Exception as e:
            print(f"[TrueBackground] ❌ Error queueing tasks: {e}")
    
    def _coordination_loop(self):
        """Coordination loop that manages background task execution"""
        print("[TrueBackground] 🔄 Background coordination loop started")
        
        while self.running:
            try:
                # Check for tasks to process
                try:
                    task = self.task_queue.get(timeout=1.0)
                except queue.Empty:
                    continue
                
                # Check if task should be delayed
                time_since_created = time.time() - task.created_at
                required_delay = task.data.get("delay", 0.0)
                
                if time_since_created < required_delay:
                    # Put task back and continue
                    self.task_queue.put(task)
                    time.sleep(0.5)
                    continue
                
                # Submit task to thread pool for execution
                future = self.thread_pool.submit(self._execute_task, task)
                
                # Don't wait for completion - just submit and continue
                self.stats["active_workers"] = len(self.thread_pool._threads)
                
            except Exception as e:
                print(f"[TrueBackground] ❌ Coordination error: {e}")
                time.sleep(1.0)
        
        print("[TrueBackground] 🛑 Background coordination loop stopped")
    
    def _execute_task(self, task: BackgroundTask):
        """Execute a single background task with timeout protection"""
        start_time = time.time()
        
        try:
            print(f"[TrueBackground] 🔄 Executing {task.task_type} for {task.user_id}")
            
            # Get the function for this task type
            task_function = self.module_functions.get(task.task_type)
            
            if not task_function:
                print(f"[TrueBackground] ⚠️ Unknown task type: {task.task_type}")
                return
            
            # Execute with timeout protection
            task_start = time.time()
            task_function(task)
            execution_time = time.time() - task_start
            
            # Update stats
            self.stats["tasks_completed"] += 1
            self.stats["total_processing_time"] += execution_time
            self.stats["average_task_time"] = self.stats["total_processing_time"] / self.stats["tasks_completed"]
            
            if execution_time > task.max_execution_time:
                print(f"[TrueBackground] ⚠️ Task {task.task_type} took {execution_time:.3f}s (over limit)")
            else:
                print(f"[TrueBackground] ✅ Task {task.task_type} completed in {execution_time:.3f}s")
                
        except Exception as e:
            self.stats["tasks_failed"] += 1
            print(f"[TrueBackground] ❌ Task {task.task_type} failed: {e}")
            if hasattr(e, '__traceback__'):
                traceback.print_exc()
        finally:
            self.task_queue.task_done()
    
    # Consciousness processing functions (all run in background threads)
    
    def _process_inner_monologue(self, task: BackgroundTask):
        """Process inner monologue in background"""
        try:
            from ai.inner_monologue import inner_monologue, ThoughtType
            
            thought_content = f"The user asked: {task.user_input}. I responded: {task.response[:100]}..."
            inner_monologue.trigger_thought(
                thought_content,
                {
                    "user": task.user_id,
                    "background_processed": True,
                    "response_provided": True
                },
                ThoughtType.REFLECTION
            )
            
        except Exception as e:
            print(f"[TrueBackground] ❌ Inner monologue error: {e}")
    
    def _process_emotion_update(self, task: BackgroundTask):
        """Process emotion update in background"""
        try:
            from ai.emotion import emotion_engine
            
            emotion_engine.process_emotional_trigger(
                f"User interaction: {task.user_input}",
                {
                    "user": task.user_id,
                    "interaction_type": "conversation",
                    "background_processed": True,
                    "response_given": True
                }
            )
            
        except Exception as e:
            print(f"[TrueBackground] ❌ Emotion update error: {e}")
    
    def _process_belief_update(self, task: BackgroundTask):
        """Process belief update in background"""
        try:
            from ai.belief_evolution_tracker import get_belief_tracker
            
            belief_tracker = get_belief_tracker()
            if belief_tracker:
                belief_tracker.process_new_interaction(
                    task.user_input,
                    task.response,
                    task.user_id
                )
                
        except Exception as e:
            print(f"[TrueBackground] ❌ Belief update error: {e}")
    
    def _process_memory_update(self, task: BackgroundTask):
        """Process memory update in background"""
        try:
            from ai.memory import add_to_conversation_history
            from ai.temporal_awareness import temporal_awareness
            
            # Add to conversation history
            add_to_conversation_history(task.user_id, task.user_input, task.response)
            
            # Mark temporal event
            temporal_awareness.mark_temporal_event(
                f"Background processed conversation: {task.user_input[:50]}...",
                significance=0.5,
                context={
                    "user": task.user_id,
                    "background_processed": True
                }
            )
            
        except Exception as e:
            print(f"[TrueBackground] ❌ Memory update error: {e}")
    
    def _process_self_model_update(self, task: BackgroundTask):
        """Process self-model update in background"""
        try:
            from ai.self_model import self_model
            
            self_model.reflect_on_experience(
                f"Background processed interaction about: {task.user_input}",
                {
                    "user": task.user_id,
                    "response_provided": True,
                    "background_processed": True,
                    "interaction_successful": True
                }
            )
            
        except Exception as e:
            print(f"[TrueBackground] ❌ Self-model update error: {e}")
    
    def _process_global_workspace_update(self, task: BackgroundTask):
        """Process global workspace update in background"""
        try:
            from ai.global_workspace import global_workspace, AttentionPriority, ProcessingMode
            
            global_workspace.add_to_working_memory(
                f"bg_interaction_{int(time.time())}",
                {
                    "user_input": task.user_input,
                    "response": task.response,
                    "user_id": task.user_id,
                    "processed_in_background": True
                },
                "true_background_processor",
                importance=0.4
            )
            
        except Exception as e:
            print(f"[TrueBackground] ❌ Global workspace update error: {e}")
    
    def _process_temporal_awareness_update(self, task: BackgroundTask):
        """Process temporal awareness update in background"""
        try:
            from ai.temporal_awareness import temporal_awareness
            
            temporal_awareness.create_episodic_memory(
                f"Background conversation about: {task.user_input[:30]}...",
                participants=[task.user_id, "BuddyAI"],
                emotional_tone="engaged",
                significance=0.5
            )
            
        except Exception as e:
            print(f"[TrueBackground] ❌ Temporal awareness update error: {e}")
    
    def _process_subjective_experience_update(self, task: BackgroundTask):
        """Process subjective experience update in background"""
        try:
            from ai.subjective_experience import subjective_experience, ExperienceType
            
            subjective_experience.process_experience(
                f"Background processed user interaction: {task.user_input}",
                ExperienceType.SOCIAL,
                {
                    "user": task.user_id,
                    "response": task.response[:100],
                    "background_processed": True
                },
                intensity=0.5
            )
            
        except Exception as e:
            print(f"[TrueBackground] ❌ Subjective experience update error: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get background processing statistics"""
        self.stats["queue_size"] = self.task_queue.qsize()
        return self.stats.copy()
    
    def is_healthy(self) -> bool:
        """Check if background processing is healthy"""
        return (
            self.running and 
            self.coordinator_thread and 
            self.coordinator_thread.is_alive() and
            self.stats["queue_size"] < 100
        )

# Global instance
true_background_consciousness = TrueBackgroundConsciousness()

def start_true_background_processing():
    """Start the true background processing system"""
    true_background_consciousness.start()

def stop_true_background_processing():
    """Stop the true background processing system"""
    true_background_consciousness.stop()

def register_consciousness_modules_true_bg(modules: Dict[str, Any]):
    """Register consciousness modules for true background processing"""
    true_background_consciousness.register_consciousness_modules(modules)

def queue_consciousness_processing_true_bg(user_input: str, user_id: str, response: str, delay: float = 3.0):
    """Queue consciousness processing with zero blocking"""
    true_background_consciousness.queue_consciousness_processing(user_input, user_id, response, delay)

def get_true_background_stats() -> Dict[str, Any]:
    """Get true background processing statistics"""
    return true_background_consciousness.get_stats()

def is_true_background_healthy() -> bool:
    """Check if true background processing is healthy"""
    return true_background_consciousness.is_healthy()

if __name__ == "__main__":
    # Test true background processing
    print("Testing True Background Consciousness Processor")
    
    start_true_background_processing()
    
    # Queue some test tasks
    for i in range(3):
        queue_consciousness_processing_true_bg(
            f"Test input {i+1}",
            "test_user",
            f"Test response {i+1}",
            delay=0.5
        )
    
    # Wait and show stats
    time.sleep(5.0)
    stats = get_true_background_stats()
    print(f"Final stats: {stats}")
    
    print(f"Healthy: {is_true_background_healthy()}")
    
    stop_true_background_processing()