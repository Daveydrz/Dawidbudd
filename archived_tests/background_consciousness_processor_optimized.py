"""
Background Consciousness Processor - Handle consciousness updates without blocking responses
Created: 2025-01-17
Purpose: Process consciousness updates in background threads for optimal performance
Features: Non-blocking, optional inner thoughts, configurable processing
"""

import threading
import time
import queue
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass
from config import *

@dataclass
class ConsciousnessTask:
    """Task for background consciousness processing"""
    task_type: str  # 'inner_thought', 'self_reflection', 'emotion_update', 'memory_formation'
    user_input: str
    user_id: str
    context: Dict[str, Any]
    priority: int = 1  # 1=low, 2=medium, 3=high
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

class BackgroundConsciousnessProcessor:
    """Process consciousness updates in background without blocking responses"""
    
    def __init__(self):
        self.task_queue = queue.PriorityQueue()
        self.worker_thread = None
        self.running = False
        self.processed_tasks = 0
        self.inner_thoughts_generated = 0
        self.processing_stats = {}
        
    def start(self):
        """Start the background processor"""
        if not self.running:
            self.running = True
            self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
            self.worker_thread.start()
            print("[BackgroundConsciousness] 🧠 Background consciousness processor started")
    
    def stop(self):
        """Stop the background processor"""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=2.0)
        print("[BackgroundConsciousness] 🛑 Background consciousness processor stopped")
    
    def _worker_loop(self):
        """Main worker loop for processing consciousness tasks"""
        while self.running:
            try:
                # Get task with timeout
                try:
                    priority, task = self.task_queue.get(timeout=1.0)
                except queue.Empty:
                    continue
                
                # Process the task
                self._process_task(task)
                self.processed_tasks += 1
                
                # Mark task as done
                self.task_queue.task_done()
                
            except Exception as e:
                if LOG_CONSCIOUSNESS_PROCESSING:
                    print(f"[BackgroundConsciousness] ⚠️ Error processing task: {e}")
    
    def _process_task(self, task: ConsciousnessTask):
        """Process a single consciousness task"""
        start_time = time.time()
        
        try:
            if task.task_type == "inner_thought" and ENABLE_INNER_THOUGHTS:
                self._process_inner_thought(task)
            elif task.task_type == "self_reflection" and ENABLE_SELF_REFLECTION:
                self._process_self_reflection(task)
            elif task.task_type == "emotion_update" and ENABLE_EMOTIONAL_PROCESSING:
                self._process_emotion_update(task)
            elif task.task_type == "memory_formation" and ENABLE_MEMORY_FORMATION:
                self._process_memory_formation(task)
            else:
                if LOG_CONSCIOUSNESS_PROCESSING:
                    print(f"[BackgroundConsciousness] ⏭️ Skipping {task.task_type} (disabled in config)")
                return
            
            processing_time = time.time() - start_time
            self.processing_stats[task.task_type] = self.processing_stats.get(task.task_type, [])
            self.processing_stats[task.task_type].append(processing_time)
            
            if LOG_CONSCIOUSNESS_PROCESSING:
                print(f"[BackgroundConsciousness] ✅ Processed {task.task_type} in {processing_time:.2f}s")
                
        except Exception as e:
            if LOG_CONSCIOUSNESS_PROCESSING:
                print(f"[BackgroundConsciousness] ❌ Error processing {task.task_type}: {e}")
    
    def _process_inner_thought(self, task: ConsciousnessTask):
        """Process inner thought generation (local, no LLM)"""
        # Generate simple inner thoughts based on patterns
        thought_templates = [
            f"The user asked about {self._extract_topic(task.user_input)}...",
            f"I'm thinking about how to best help with this request.",
            f"This reminds me of previous conversations we've had.",
            f"I wonder if there's more context I should consider.",
            f"The user seems {self._detect_mood(task.user_input)} today.",
        ]
        
        # Simple template selection (no LLM needed)
        import random
        thought = random.choice(thought_templates)
        
        # Store the inner thought locally
        self._store_inner_thought(task.user_id, thought, task.timestamp)
        self.inner_thoughts_generated += 1
        
        if LOG_CONSCIOUSNESS_PROCESSING:
            print(f"[BackgroundConsciousness] 💭 Generated inner thought: {thought[:50]}...")
    
    def _process_self_reflection(self, task: ConsciousnessTask):
        """Process self-reflection (local, no LLM)"""
        # Simple self-reflection based on interaction patterns
        reflection_templates = [
            f"I responded well to the user's request about {self._extract_topic(task.user_input)}.",
            "I'm maintaining good conversation flow and staying helpful.",
            "The user seems engaged and I'm providing useful information.",
            "I should continue being authentic and supportive.",
        ]
        
        import random
        reflection = random.choice(reflection_templates)
        
        # Store reflection locally
        self._store_self_reflection(task.user_id, reflection, task.timestamp)
        
        if LOG_CONSCIOUSNESS_PROCESSING:
            print(f"[BackgroundConsciousness] 🪞 Generated self-reflection: {reflection[:50]}...")
    
    def _process_emotion_update(self, task: ConsciousnessTask):
        """Process emotional state update (local, no LLM)"""
        # Simple emotion detection based on text patterns
        detected_emotion = self._detect_emotion(task.user_input)
        
        # Update emotional state locally
        self._update_emotional_state(task.user_id, detected_emotion, task.timestamp)
        
        if LOG_CONSCIOUSNESS_PROCESSING:
            print(f"[BackgroundConsciousness] 💖 Updated emotion to: {detected_emotion}")
    
    def _process_memory_formation(self, task: ConsciousnessTask):
        """Process memory formation (handled by local memory manager)"""
        try:
            from ai.local_memory_manager import local_memory_manager
            
            # Memory formation is already handled by local memory manager
            # This just logs the event for consciousness tracking
            
            memories = local_memory_manager.get_recent_memories(task.user_id, 1)
            memory_count = len(memories.get("actions", [])) + len(memories.get("facts", []))
            
            if LOG_CONSCIOUSNESS_PROCESSING:
                print(f"[BackgroundConsciousness] 📚 Memory formation processed: {memory_count} items")
                
        except ImportError:
            if LOG_CONSCIOUSNESS_PROCESSING:
                print(f"[BackgroundConsciousness] ⚠️ Local memory manager not available")
    
    def _extract_topic(self, text: str) -> str:
        """Simple topic extraction without LLM"""
        # Basic keyword matching
        topics = {
            "weather": ["weather", "rain", "sunny", "temperature"],
            "time": ["time", "date", "when", "clock"],
            "location": ["where", "location", "place"],
            "help": ["help", "assist", "support"],
            "question": ["what", "how", "why", "who"],
        }
        
        text_lower = text.lower()
        for topic, keywords in topics.items():
            if any(keyword in text_lower for keyword in keywords):
                return topic
        
        return "general conversation"
    
    def _detect_mood(self, text: str) -> str:
        """Simple mood detection without LLM"""
        positive_words = ["good", "great", "happy", "excited", "awesome", "wonderful"]
        negative_words = ["bad", "sad", "angry", "frustrated", "terrible", "awful"]
        
        text_lower = text.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "concerned"
        else:
            return "neutral"
    
    def _detect_emotion(self, text: str) -> str:
        """Simple emotion detection without LLM"""
        emotions = {
            "excited": ["excited", "amazing", "awesome", "fantastic"],
            "happy": ["happy", "good", "great", "wonderful"],
            "curious": ["why", "how", "what", "interesting"],
            "concerned": ["worried", "concerned", "problem", "issue"],
            "confused": ["confused", "don't understand", "unclear"],
            "grateful": ["thank", "thanks", "appreciate"],
        }
        
        text_lower = text.lower()
        for emotion, keywords in emotions.items():
            if any(keyword in text_lower for keyword in keywords):
                return emotion
        
        return "neutral"
    
    def _store_inner_thought(self, user_id: str, thought: str, timestamp: str):
        """Store inner thought locally"""
        try:
            import json
            thoughts_file = "ai_inner_thoughts.json"
            
            # Load existing thoughts
            try:
                with open(thoughts_file, 'r') as f:
                    thoughts_data = json.load(f)
            except:
                thoughts_data = {"users": {}}
            
            # Add new thought
            if user_id not in thoughts_data["users"]:
                thoughts_data["users"][user_id] = []
            
            thoughts_data["users"][user_id].append({
                "thought": thought,
                "timestamp": timestamp,
                "type": "inner_thought"
            })
            
            # Keep only recent thoughts (last 50)
            if len(thoughts_data["users"][user_id]) > 50:
                thoughts_data["users"][user_id] = thoughts_data["users"][user_id][-50:]
            
            # Save thoughts
            with open(thoughts_file, 'w') as f:
                json.dump(thoughts_data, f, indent=2)
                
        except Exception as e:
            if LOG_CONSCIOUSNESS_PROCESSING:
                print(f"[BackgroundConsciousness] ⚠️ Error storing inner thought: {e}")
    
    def _store_self_reflection(self, user_id: str, reflection: str, timestamp: str):
        """Store self-reflection locally"""
        try:
            import json
            reflections_file = "ai_self_reflections.json"
            
            # Load existing reflections
            try:
                with open(reflections_file, 'r') as f:
                    reflections_data = json.load(f)
            except:
                reflections_data = {"users": {}}
            
            # Add new reflection
            if user_id not in reflections_data["users"]:
                reflections_data["users"][user_id] = []
            
            reflections_data["users"][user_id].append({
                "reflection": reflection,
                "timestamp": timestamp,
                "type": "self_reflection"
            })
            
            # Keep only recent reflections (last 30)
            if len(reflections_data["users"][user_id]) > 30:
                reflections_data["users"][user_id] = reflections_data["users"][user_id][-30:]
            
            # Save reflections
            with open(reflections_file, 'w') as f:
                json.dump(reflections_data, f, indent=2)
                
        except Exception as e:
            if LOG_CONSCIOUSNESS_PROCESSING:
                print(f"[BackgroundConsciousness] ⚠️ Error storing self-reflection: {e}")
    
    def _update_emotional_state(self, user_id: str, emotion: str, timestamp: str):
        """Update emotional state locally"""
        try:
            import json
            emotions_file = "ai_emotions.json"
            
            # Load existing emotions
            try:
                with open(emotions_file, 'r') as f:
                    emotions_data = json.load(f)
            except:
                emotions_data = {"users": {}}
            
            # Update emotion
            if user_id not in emotions_data["users"]:
                emotions_data["users"][user_id] = {"current_emotion": "neutral", "history": []}
            
            emotions_data["users"][user_id]["current_emotion"] = emotion
            emotions_data["users"][user_id]["history"].append({
                "emotion": emotion,
                "timestamp": timestamp
            })
            
            # Keep only recent emotion history (last 20)
            if len(emotions_data["users"][user_id]["history"]) > 20:
                emotions_data["users"][user_id]["history"] = emotions_data["users"][user_id]["history"][-20:]
            
            # Save emotions
            with open(emotions_file, 'w') as f:
                json.dump(emotions_data, f, indent=2)
                
        except Exception as e:
            if LOG_CONSCIOUSNESS_PROCESSING:
                print(f"[BackgroundConsciousness] ⚠️ Error updating emotional state: {e}")
    
    def queue_consciousness_task(self, task_type: str, user_input: str, user_id: str, context: Dict[str, Any] = None, priority: int = 1):
        """Queue a consciousness task for background processing"""
        if not BACKGROUND_CONSCIOUSNESS_PROCESSING:
            return
        
        task = ConsciousnessTask(
            task_type=task_type,
            user_input=user_input,
            user_id=user_id,
            context=context or {},
            priority=priority
        )
        
        # Priority queue uses negative priority for max-heap behavior
        self.task_queue.put((-priority, task))
        
        if LOG_CONSCIOUSNESS_PROCESSING:
            print(f"[BackgroundConsciousness] 📝 Queued {task_type} task for {user_id}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get processing statistics"""
        avg_times = {}
        for task_type, times in self.processing_stats.items():
            avg_times[f"avg_{task_type}_time"] = sum(times) / len(times) if times else 0
        
        return {
            "tasks_processed": self.processed_tasks,
            "inner_thoughts_generated": self.inner_thoughts_generated,
            "queue_size": self.task_queue.qsize(),
            "is_running": self.running,
            "processing_times": avg_times,
            "config": {
                "inner_thoughts_enabled": ENABLE_INNER_THOUGHTS,
                "self_reflection_enabled": ENABLE_SELF_REFLECTION,
                "emotional_processing_enabled": ENABLE_EMOTIONAL_PROCESSING,
                "memory_formation_enabled": ENABLE_MEMORY_FORMATION,
                "background_processing_enabled": BACKGROUND_CONSCIOUSNESS_PROCESSING
            }
        }

# Global instance
background_consciousness_processor = BackgroundConsciousnessProcessor()

def schedule_consciousness_processing(user_input: str, user_id: str, context: Dict[str, Any] = None):
    """Schedule all consciousness processing tasks in background"""
    if not BACKGROUND_CONSCIOUSNESS_PROCESSING:
        return
    
    # Queue different types of consciousness processing
    background_consciousness_processor.queue_consciousness_task(
        "memory_formation", user_input, user_id, context, priority=3
    )
    
    background_consciousness_processor.queue_consciousness_task(
        "emotion_update", user_input, user_id, context, priority=2
    )
    
    if ENABLE_INNER_THOUGHTS:
        background_consciousness_processor.queue_consciousness_task(
            "inner_thought", user_input, user_id, context, priority=1
        )
    
    if ENABLE_SELF_REFLECTION:
        background_consciousness_processor.queue_consciousness_task(
            "self_reflection", user_input, user_id, context, priority=1
        )