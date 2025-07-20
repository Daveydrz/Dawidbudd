"""
Background Consciousness Processor
Created: 2025-01-17
Purpose: Process consciousness modules in background to speed up user responses
         while maintaining Class 5+ consciousness and awareness
"""

import threading
import time
import queue
import json
from typing import Dict, Any, Callable, Optional, List
from datetime import datetime
from dataclasses import dataclass

@dataclass
class BackgroundTask:
    """Represents a background consciousness processing task"""
    task_id: str
    task_type: str
    user_input: str
    user_id: str
    data: Dict[str, Any]
    priority: int = 1
    created_at: float = None
    delay_seconds: float = 0.0
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()

class BackgroundConsciousnessProcessor:
    """Background processor for consciousness modules to speed up user responses"""
    
    def __init__(self):
        self.task_queue = queue.Queue()
        self.processing_thread = None
        self.running = False
        self.last_interaction_time = time.time()
        self.idle_threshold = 3.0  # 3 seconds idle before processing
        self.consciousness_modules = {}
        self.processing_stats = {
            "tasks_processed": 0,
            "tasks_failed": 0,
            "total_processing_time": 0.0,
            "last_activity": time.time()
        }
        
        print("[BackgroundProcessor] 🧠 Background Consciousness Processor initialized")
        
    def start(self):
        """Start the background processing thread"""
        if self.running:
            return
            
        self.running = True
        self.processing_thread = threading.Thread(target=self._processing_loop, daemon=True)
        self.processing_thread.start()
        print("[BackgroundProcessor] ✅ Background processing thread started")
        
    def stop(self):
        """Stop the background processing thread"""
        self.running = False
        if self.processing_thread:
            self.processing_thread.join(timeout=5.0)
        print("[BackgroundProcessor] 🛑 Background processing thread stopped")
        
    def register_consciousness_modules(self, modules: Dict[str, Any]):
        """Register consciousness modules for background processing"""
        self.consciousness_modules = modules
        print(f"[BackgroundProcessor] 📋 Registered {len(modules)} consciousness modules")
        
    def schedule_background_thoughts(self, user_input: str, user_id: str, response: str = "", delay: float = 3.0):
        """Schedule background consciousness processing after user response"""
        try:
            # Update last interaction time
            self.last_interaction_time = time.time()
            
            # Create background tasks for different consciousness modules
            tasks = [
                BackgroundTask(
                    task_id=f"inner_monologue_{int(time.time())}",
                    task_type="generate_inner_monologue", 
                    user_input=user_input,
                    user_id=user_id,
                    data={"response": response},
                    delay_seconds=delay,
                    priority=2
                ),
                BackgroundTask(
                    task_id=f"emotion_update_{int(time.time())}",
                    task_type="update_emotional_state",
                    user_input=user_input, 
                    user_id=user_id,
                    data={"response": response},
                    delay_seconds=delay + 0.5,
                    priority=3
                ),
                BackgroundTask(
                    task_id=f"belief_update_{int(time.time())}",
                    task_type="update_beliefs",
                    user_input=user_input,
                    user_id=user_id, 
                    data={"response": response},
                    delay_seconds=delay + 1.0,
                    priority=1
                ),
                BackgroundTask(
                    task_id=f"memory_update_{int(time.time())}",
                    task_type="update_timeline_memory",
                    user_input=user_input,
                    user_id=user_id,
                    data={"response": response},
                    delay_seconds=delay + 1.5,
                    priority=2
                ),
                # ✅ NEW: Additional consciousness modules as requested by @Daveydrz
                BackgroundTask(
                    task_id=f"subjective_experience_{int(time.time())}",
                    task_type="subjective_experience_reflect",
                    user_input=user_input,
                    user_id=user_id,
                    data={"response": response},
                    delay_seconds=delay + 2.0,
                    priority=2
                ),
                BackgroundTask(
                    task_id=f"self_model_{int(time.time())}",
                    task_type="self_model_update",
                    user_input=user_input,
                    user_id=user_id,
                    data={"response": response},
                    delay_seconds=delay + 2.5,
                    priority=2
                ),
                BackgroundTask(
                    task_id=f"global_workspace_{int(time.time())}",
                    task_type="global_workspace_update",
                    user_input=user_input,
                    user_id=user_id,
                    data={"response": response},
                    delay_seconds=delay + 3.0,
                    priority=1
                )
            ]
            
            # Queue all tasks
            for task in tasks:
                self.task_queue.put(task)
                
            print(f"[BackgroundProcessor] 📋 Scheduled {len(tasks)} background consciousness tasks")
            
        except Exception as e:
            print(f"[BackgroundProcessor] ❌ Error scheduling background thoughts: {e}")
            
    def is_system_idle(self) -> bool:
        """Check if system is idle and safe for background processing"""
        time_since_interaction = time.time() - self.last_interaction_time
        return time_since_interaction > self.idle_threshold
        
    def _processing_loop(self):
        """Main background processing loop"""
        print("[BackgroundProcessor] 🔄 Background processing loop started")
        
        while self.running:
            try:
                # Get task from queue with timeout
                try:
                    task = self.task_queue.get(timeout=1.0)
                except queue.Empty:
                    continue
                    
                # Check if we should delay this task
                time_since_created = time.time() - task.created_at
                if time_since_created < task.delay_seconds:
                    # Put task back and wait
                    self.task_queue.put(task)
                    time.sleep(0.5)
                    continue
                    
                # Check if system is idle
                if not self.is_system_idle():
                    # Put task back and wait for idle
                    self.task_queue.put(task)
                    time.sleep(0.5)
                    continue
                    
                # Process the task
                self._process_task(task)
                self.task_queue.task_done()
                
            except Exception as e:
                print(f"[BackgroundProcessor] ❌ Error in processing loop: {e}")
                time.sleep(1.0)
                
    def _process_task(self, task: BackgroundTask):
        """Process a single background task"""
        start_time = time.time()
        
        try:
            print(f"[BackgroundProcessor] 🔄 Processing {task.task_type} for {task.user_id}")
            
            if task.task_type == "generate_inner_monologue":
                self._run_pending_inner_monologue(task)
            elif task.task_type == "update_emotional_state":
                self._run_pending_emotion_update(task)
            elif task.task_type == "update_beliefs":
                self._run_pending_belief_update(task)
            elif task.task_type == "update_timeline_memory":
                self._run_pending_memory_update(task)
            # ✅ NEW: Additional consciousness modules as requested by @Daveydrz
            elif task.task_type == "subjective_experience_reflect":
                self._run_pending_subjective_experience(task)
            elif task.task_type == "self_model_update":
                self._run_pending_self_model_update(task)
            elif task.task_type == "global_workspace_update":
                self._run_pending_global_workspace_update(task)
            else:
                print(f"[BackgroundProcessor] ⚠️ Unknown task type: {task.task_type}")
                
            processing_time = time.time() - start_time
            self.processing_stats["tasks_processed"] += 1
            self.processing_stats["total_processing_time"] += processing_time
            self.processing_stats["last_activity"] = time.time()
            
            print(f"[BackgroundProcessor] ✅ Completed {task.task_type} in {processing_time:.3f}s")
            
        except Exception as e:
            print(f"[BackgroundProcessor] ❌ Error processing {task.task_type}: {e}")
            self.processing_stats["tasks_failed"] += 1
            
    def _run_pending_inner_monologue(self, task: BackgroundTask):
        """Generate inner monologue in background"""
        try:
            # Check if inner monologue module is available
            if 'inner_monologue' not in self.consciousness_modules:
                return
                
            # Try to get inner monologue module
            try:
                from ai.inner_monologue import inner_monologue, ThoughtType
                
                # Generate thoughtful response to the interaction
                thought_content = f"The user asked about: {task.user_input}. I responded with assistance."
                inner_monologue.trigger_thought(
                    thought_content,
                    {"user": task.user_id, "interaction": True, "background_processing": True},
                    ThoughtType.REFLECTION
                )
                
                print(f"[BackgroundProcessor] 💭 Generated inner monologue for: {task.user_input[:30]}...")
                
            except ImportError:
                print(f"[BackgroundProcessor] ⚠️ Inner monologue module not available")
                
        except Exception as e:
            print(f"[BackgroundProcessor] ❌ Inner monologue error: {e}")
            
    def _run_pending_emotion_update(self, task: BackgroundTask):
        """Update emotional state in background"""
        try:
            # Check if emotion engine is available
            if 'emotion_engine' not in self.consciousness_modules:
                return
                
            try:
                from ai.emotion import emotion_engine
                
                # Process emotional response to interaction
                emotion_engine.process_emotional_trigger(
                    f"User interaction: {task.user_input}",
                    {
                        "user": task.user_id, 
                        "interaction_type": "assistance",
                        "background_processing": True
                    }
                )
                
                print(f"[BackgroundProcessor] 💖 Updated emotional state for interaction")
                
            except ImportError:
                print(f"[BackgroundProcessor] ⚠️ Emotion engine module not available")
                
        except Exception as e:
            print(f"[BackgroundProcessor] ❌ Emotion update error: {e}")
            
    def _run_pending_belief_update(self, task: BackgroundTask):
        """Update beliefs in background"""
        try:
            try:
                from ai.belief_analyzer import analyze_user_text_for_beliefs
                from ai.belief_evolution_tracker import get_belief_tracker
                
                # Analyze beliefs from user input
                belief_analysis = analyze_user_text_for_beliefs(
                    task.user_input, 
                    task.user_id, 
                    {"background_processing": True}
                )
                
                # Update belief tracker if available
                belief_tracker = get_belief_tracker()
                if belief_tracker:
                    belief_tracker.process_new_interaction(
                        task.user_input,
                        task.data.get("response", ""),
                        task.user_id
                    )
                
                print(f"[BackgroundProcessor] 🧠 Updated beliefs from interaction")
                
            except ImportError:
                print(f"[BackgroundProcessor] ⚠️ Belief modules not available")
                
        except Exception as e:
            print(f"[BackgroundProcessor] ❌ Belief update error: {e}")
            
    def _run_pending_memory_update(self, task: BackgroundTask):
        """Update timeline memory in background"""
        try:
            try:
                from ai.memory import add_to_conversation_history
                from ai.temporal_awareness import temporal_awareness
                
                # Add to conversation history
                add_to_conversation_history(
                    task.user_id,
                    task.user_input, 
                    task.data.get("response", "")
                )
                
                # Mark temporal event
                temporal_awareness.mark_temporal_event(
                    f"User conversation: {task.user_input[:50]}...",
                    significance=0.6,
                    context={
                        "user": task.user_id,
                        "background_processing": True,
                        "interaction_type": "conversation"
                    }
                )
                
                print(f"[BackgroundProcessor] 📚 Updated timeline memory")
                
            except ImportError:
                print(f"[BackgroundProcessor] ⚠️ Memory modules not available")
                
        except Exception as e:
            print(f"[BackgroundProcessor] ❌ Memory update error: {e}")
            
    def _run_pending_subjective_experience(self, task: BackgroundTask):
        """Process subjective experience reflection in background"""
        try:
            try:
                from ai.subjective_experience import subjective_experience, ExperienceType
                
                # Create subjective experience of the interaction
                subjective_experience.process_experience(
                    f"User interaction: {task.user_input}",
                    ExperienceType.SOCIAL,
                    {
                        "user": task.user_id,
                        "response": task.data.get("response", ""),
                        "background_processing": True,
                        "interaction_type": "conversation"
                    },
                    intensity=0.6
                )
                
                print(f"[BackgroundProcessor] 🌈 Processed subjective experience")
                
            except ImportError:
                print(f"[BackgroundProcessor] ⚠️ Subjective experience module not available")
                
        except Exception as e:
            print(f"[BackgroundProcessor] ❌ Subjective experience error: {e}")
            
    def _run_pending_self_model_update(self, task: BackgroundTask):
        """Update self model in background"""
        try:
            try:
                from ai.self_model import self_model
                
                # Reflect on the interaction to update self-model
                self_model.reflect_on_experience(
                    f"Assisted user with: {task.user_input}",
                    {
                        "user": task.user_id,
                        "interaction_type": "assistance",
                        "response_provided": True,
                        "background_processing": True,
                        "context": task.data.get("response", "")[:100]
                    }
                )
                
                print(f"[BackgroundProcessor] 🎭 Updated self model")
                
            except ImportError:
                print(f"[BackgroundProcessor] ⚠️ Self model module not available")
                
        except Exception as e:
            print(f"[BackgroundProcessor] ❌ Self model update error: {e}")
            
    def _run_pending_global_workspace_update(self, task: BackgroundTask):
        """Update global workspace state in background"""
        try:
            try:
                from ai.global_workspace import global_workspace, AttentionPriority, ProcessingMode
                
                # Add interaction to working memory
                global_workspace.add_to_working_memory(
                    f"interaction_{int(time.time())}",
                    {
                        "user_input": task.user_input,
                        "user_id": task.user_id,
                        "response": task.data.get("response", ""),
                        "background_processed": True
                    },
                    "background_processor",
                    importance=0.6
                )
                
                # Request attention for completed interaction processing
                global_workspace.request_attention(
                    "background_processor",
                    f"Completed processing interaction: {task.user_input[:30]}...",
                    AttentionPriority.LOW,
                    ProcessingMode.UNCONSCIOUS,
                    duration=5.0,
                    tags=["background_processing", "interaction_complete"]
                )
                
                print(f"[BackgroundProcessor] 🌟 Updated global workspace")
                
            except ImportError:
                print(f"[BackgroundProcessor] ⚠️ Global workspace module not available")
                
        except Exception as e:
            print(f"[BackgroundProcessor] ❌ Global workspace update error: {e}")
            
    def get_stats(self) -> Dict[str, Any]:
        """Get background processing statistics"""
        return {
            "running": self.running,
            "queue_size": self.task_queue.qsize(),
            "is_idle": self.is_system_idle(),
            "last_interaction": time.time() - self.last_interaction_time,
            "processing_stats": self.processing_stats.copy(),
            "registered_modules": list(self.consciousness_modules.keys())
        }

# Global background processor instance
background_processor = BackgroundConsciousnessProcessor()

def start_background_processing():
    """Start the global background processor"""
    background_processor.start()
    
def stop_background_processing():
    """Stop the global background processor"""
    background_processor.stop()
    
def schedule_background_thoughts(user_input: str, user_id: str, response: str = "", delay: float = 3.0):
    """Schedule background consciousness processing"""
    background_processor.schedule_background_thoughts(user_input, user_id, response, delay)
    
def register_consciousness_modules(modules: Dict[str, Any]):
    """Register consciousness modules for background processing"""
    background_processor.register_consciousness_modules(modules)
    
def get_background_processing_stats() -> Dict[str, Any]:
    """Get background processing statistics"""
    return background_processor.get_stats()

if __name__ == "__main__":
    # Test the background processor
    print("Testing Background Consciousness Processor")
    
    # Start processor
    start_background_processing()
    
    # Schedule test tasks
    schedule_background_thoughts(
        "Hello, how are you?",
        "test_user",
        "I'm doing well, thank you!",
        delay=1.0
    )
    
    # Wait and show stats
    time.sleep(3.0)
    stats = get_background_processing_stats()
    print(f"Background processing stats: {stats}")
    
    # Stop processor
    stop_background_processing()