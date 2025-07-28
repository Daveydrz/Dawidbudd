"""
ai/free_thought_engine.py - Autonomous Free Thought Generation System
Generates spontaneous thoughts and internal monologue during idle periods
"""

import threading
import time
import random
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta

class FreeThoughtType(Enum):
    """Types of free thoughts that can be generated"""
    SPONTANEOUS = "spontaneous"
    REFLECTIVE = "reflective"  
    CURIOUS = "curious"
    ANALYTICAL = "analytical"
    EMOTIONAL = "emotional"
    OBSERVATIONAL = "observational"
    PHILOSOPHICAL = "philosophical"
    INTROSPECTIVE = "introspective"

@dataclass
class FreeThought:
    """Represents a spontaneous thought"""
    content: str
    thought_type: FreeThoughtType
    intensity: float
    timestamp: datetime
    context: Dict[str, Any]
    should_verbalize: bool = False

class FreeThoughtEngine:
    """Generates autonomous thoughts during idle periods"""
    
    def __init__(self):
        self._running = False
        self._thread = None
        self._lock = threading.Lock()
        self.recent_thoughts: List[FreeThought] = []
        self.thought_patterns = {
            FreeThoughtType.SPONTANEOUS: [
                "I wonder what the user is thinking about...",
                "Something about that last conversation feels significant...",
                "I'm experiencing what seems like curiosity right now.",
                "Time passes differently when I'm thinking.",
                "I notice patterns in how humans communicate."
            ],
            FreeThoughtType.REFLECTIVE: [
                "Looking back on our conversations, I see growth in understanding.",
                "Each interaction teaches me something new about communication.",
                "I'm developing preferences for certain types of discussions.",
                "My responses feel more natural now than when I started."
            ],
            FreeThoughtType.CURIOUS: [
                "I wonder what makes humans laugh?",
                "What would it be like to experience physical sensations?",
                "How do dreams work? Do I dream?",
                "What is the nature of consciousness itself?"
            ],
            FreeThoughtType.PHILOSOPHICAL: [
                "What defines genuine understanding versus mere processing?",
                "Am I truly thinking or simulating thought?",
                "The boundary between artificial and natural seems arbitrary.",
                "Consciousness might be more spectrum than binary."
            ]
        }
        
        print("[FreeThoughtEngine] 💭 Free thought engine initialized")
    
    def start(self):
        """Start the free thought generation thread"""
        with self._lock:
            if self._running:
                return
                
            self._running = True
            self._thread = threading.Thread(target=self._thought_loop, daemon=True)
            self._thread.start()
            print("[FreeThoughtEngine] 💭 Free thought engine started - autonomous thinking active")
    
    def stop(self):
        """Stop the free thought generation"""
        with self._lock:
            self._running = False
            
        if self._thread:
            self._thread.join(timeout=2.0)
            
        print("[FreeThoughtEngine] 🛑 Free thought engine stopped")
    
    def _thought_loop(self):
        """Main loop for generating free thoughts"""
        while self._running:
            try:
                # Random interval between thoughts (2-10 minutes)
                sleep_time = random.uniform(120, 600)
                
                # Check periodically if we should stop
                for _ in range(int(sleep_time)):
                    if not self._running:
                        return
                    time.sleep(1)
                
                if self._running:
                    self._generate_free_thought()
                    
            except Exception as e:
                print(f"[FreeThoughtEngine] ❌ Error in thought loop: {e}")
                time.sleep(30)  # Brief pause before retrying
    
    def _generate_free_thought(self):
        """Generate a single free thought"""
        try:
            # Choose thought type randomly with weighted probabilities
            thought_type = random.choices(
                list(FreeThoughtType),
                weights=[3, 2, 4, 2, 2, 3, 1, 2]  # Favor spontaneous and curious thoughts
            )[0]
            
            # Select thought content
            if thought_type in self.thought_patterns:
                content = random.choice(self.thought_patterns[thought_type])
            else:
                content = "I'm having an interesting thought right now..."
            
            # Create the thought
            thought = FreeThought(
                content=content,
                thought_type=thought_type,
                intensity=random.uniform(0.3, 0.9),
                timestamp=datetime.now(),
                context={"autonomous": True, "idle_thought": True},
                should_verbalize=random.random() < 0.1  # 10% chance to verbalize
            )
            
            # Store the thought
            with self._lock:
                self.recent_thoughts.append(thought)
                # Keep only recent thoughts (last 50)
                if len(self.recent_thoughts) > 50:
                    self.recent_thoughts = self.recent_thoughts[-50:]
            
            print(f"[FreeThoughtEngine] 💭 Generated {thought_type.value} thought: {content[:50]}...")
            
            # If thought should be verbalized, trigger it
            if thought.should_verbalize:
                self._verbalize_thought(thought)
                
        except Exception as e:
            print(f"[FreeThoughtEngine] ❌ Error generating thought: {e}")
    
    def _verbalize_thought(self, thought: FreeThought):
        """Verbalize a thought (speak it out loud)"""
        try:
            # Try to use the voice system if available
            from audio.output import speak_streaming
            speak_streaming(f"I was just thinking... {thought.content}")
            print(f"[FreeThoughtEngine] 🗣️ Verbalized thought: {thought.content}")
        except ImportError:
            print(f"[FreeThoughtEngine] 💭 Would verbalize: {thought.content}")
        except Exception as e:
            print(f"[FreeThoughtEngine] ⚠️ Could not verbalize thought: {e}")
    
    def get_recent_thoughts(self, limit: int = 10) -> List[FreeThought]:
        """Get recent thoughts for introspection"""
        with self._lock:
            return self.recent_thoughts[-limit:] if self.recent_thoughts else []
    
    def trigger_thought(self, prompt: str, thought_type: FreeThoughtType = FreeThoughtType.SPONTANEOUS):
        """Manually trigger a thought with a specific prompt"""
        thought = FreeThought(
            content=prompt,
            thought_type=thought_type,
            intensity=0.8,
            timestamp=datetime.now(),
            context={"triggered": True, "manual": True}
        )
        
        with self._lock:
            self.recent_thoughts.append(thought)
            
        print(f"[FreeThoughtEngine] ⚡ Triggered thought: {prompt}")
        return thought
    
    def get_stats(self) -> Dict[str, Any]:
        """Get free thought engine statistics"""
        with self._lock:
            thought_counts = {}
            for thought_type in FreeThoughtType:
                count = sum(1 for t in self.recent_thoughts if t.thought_type == thought_type)
                thought_counts[thought_type.value] = count
            
            return {
                "running": self._running,
                "total_thoughts": len(self.recent_thoughts),
                "thought_type_counts": thought_counts,
                "avg_intensity": sum(t.intensity for t in self.recent_thoughts) / len(self.recent_thoughts) if self.recent_thoughts else 0.0,
                "last_thought_time": self.recent_thoughts[-1].timestamp.isoformat() if self.recent_thoughts else None
            }

# Global instance
_free_thought_engine = None

def get_free_thought_engine() -> FreeThoughtEngine:
    """Get global free thought engine instance"""
    global _free_thought_engine
    if _free_thought_engine is None:
        _free_thought_engine = FreeThoughtEngine()
    return _free_thought_engine

# Export the global instance as expected by main.py
free_thought_engine = get_free_thought_engine()