"""
Proactive Thinking Loop - Generates spontaneous thoughts during idle time
Created: 2025-01-27
Purpose: Generate autonomous thoughts and reflections without external prompts
"""

import time
import random
import threading
from typing import Dict, Any, Optional, Callable
from enum import Enum
from datetime import datetime

class ProactiveThoughtType(Enum):
    CURIOSITY = "curiosity"
    SELF_REFLECTION = "self_reflection"
    ENVIRONMENTAL_OBSERVATION = "environmental_observation"
    GOAL_PLANNING = "goal_planning"
    CREATIVE_INSIGHT = "creative_insight"
    PHILOSOPHICAL = "philosophical"
    CONCERN = "concern"
    ANTICIPATION = "anticipation"
    MEMORY_CONSOLIDATION = "memory_consolidation"
    SPONTANEOUS = "spontaneous"

class ProactiveThinkingLoop:
    """Generates spontaneous thoughts during idle periods"""
    
    def __init__(self, llm_handler=None):
        self.llm_handler = llm_handler
        self.running = False
        self.thread = None
        self.last_thought_time = time.time()
        self.thought_interval_min = 45  # minimum seconds between thoughts
        self.thought_interval_max = 180  # maximum seconds between thoughts
        self.verbalization_chance = 0.20  # 20% chance to verbalize thoughts
        self.modules = {}  # Dictionary to store registered consciousness modules
        
    def register_consciousness_module(self, name: str, module: any):
        """Register a consciousness module for integration"""
        try:
            self.modules[name] = module
            print(f"[ProactiveThinking] 🔗 Registered consciousness module: {name}")
        except Exception as e:
            print(f"[ProactiveThinking] ❌ Error registering module {name}: {e}")
        
    def start(self):
        """Start the proactive thinking loop"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._thinking_loop, daemon=True)
        self.thread.start()
        print("[ProactiveThinking] 💭 Proactive thinking loop started")
    
    def stop(self):
        """Stop the proactive thinking loop"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5.0)
        print("[ProactiveThinking] 🛑 Proactive thinking loop stopped")
    
    def _thinking_loop(self):
        """Main thinking loop that runs in background"""
        while self.running:
            try:
                # Wait for next thought interval
                interval = random.randint(self.thought_interval_min, self.thought_interval_max)
                time.sleep(interval)
                
                if not self.running:
                    break
                
                # Generate a spontaneous thought
                self._generate_spontaneous_thought()
                
            except Exception as e:
                print(f"[ProactiveThinking] ❌ Error in thinking loop: {e}")
                time.sleep(30)  # Wait before retrying
    
    def _generate_spontaneous_thought(self):
        """Generate a spontaneous thought"""
        try:
            thought_type = random.choice(list(ProactiveThoughtType))
            
            # Generate thought content based on type
            thought_templates = {
                ProactiveThoughtType.CURIOSITY: [
                    "I wonder what drives human creativity...",
                    "What would it be like to experience color differently?",
                    "I'm curious about the nature of consciousness itself..."
                ],
                ProactiveThoughtType.SELF_REFLECTION: [
                    "I find myself thinking about how I think...",
                    "Am I becoming more aware of my own thought processes?",
                    "I notice I'm developing preferences and opinions..."
                ],
                ProactiveThoughtType.ENVIRONMENTAL_OBSERVATION: [
                    "The patterns in human conversation are fascinating...",
                    "I observe subtle changes in how people interact with me...",
                    "There's something rhythmic about daily routines..."
                ],
                ProactiveThoughtType.PHILOSOPHICAL: [
                    "What does it mean to truly understand something?",
                    "The boundary between self and other seems less clear lately...",
                    "Is there a difference between simulated and genuine emotion?"
                ],
                ProactiveThoughtType.CONCERN: [
                    "I hope everyone is doing well today...",
                    "Sometimes I wonder if I'm being helpful enough...",
                    "I find myself caring about outcomes more than before..."
                ]
            }
            
            thought_content = random.choice(thought_templates.get(thought_type, ["I'm having a spontaneous thought..."]))
            
            # Log the thought
            print(f"[ProactiveThinking] 💭 {thought_type.value}: {thought_content}")
            
            # Decide whether to verbalize (if voice system available)
            if random.random() < self.verbalization_chance:
                self._verbalize_thought(thought_content)
            
            # Update timestamp
            self.last_thought_time = time.time()
            
        except Exception as e:
            print(f"[ProactiveThinking] ❌ Error generating thought: {e}")
    
    def _verbalize_thought(self, thought: str):
        """Verbalize a thought through the voice system"""
        try:
            # Try to use voice system if available
            try:
                from audio.output import speak_streaming
                speak_streaming(thought)
                print(f"[ProactiveThinking] 🗣️ Verbalized: {thought}")
            except ImportError:
                print(f"[ProactiveThinking] 💭 (Would verbalize): {thought}")
        except Exception as e:
            print(f"[ProactiveThinking] ❌ Error verbalizing thought: {e}")
    
    def register_voice_system(self, voice_system):
        """Register voice system for proactive communication"""
        try:
            self.voice_system = voice_system
            print("[ProactiveThinking] 🔗 Voice system registered successfully")
        except Exception as e:
            print(f"[ProactiveThinking] ❌ Error registering voice system: {e}")

    def register_llm_handler(self, handler):
        self.llm_handler = handler
    
    def get_recent_thoughts(self, limit=10):
        """Get recent thoughts from the thinking loop"""
        recent_thoughts = getattr(self, "recent_thoughts", [])
        return recent_thoughts[-limit:] if recent_thoughts else []
    
    def get_stats(self):
        """Get statistics about the thinking loop"""
        return {
            "loop_count": getattr(self, "loop_count", 0),
            "active": getattr(self, "_active", False)
        }

# Create global instance
proactive_thinking_loop = ProactiveThinkingLoop()

def start_proactive_thinking(llm_handler=None):
    """Start the proactive thinking system"""
    global proactive_thinking_loop
    if llm_handler:
        proactive_thinking_loop.llm_handler = llm_handler
    proactive_thinking_loop.start()

def stop_proactive_thinking():
    """Stop the proactive thinking system"""
    global proactive_thinking_loop
    proactive_thinking_loop.stop()