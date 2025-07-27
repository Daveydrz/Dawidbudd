"""
Consciousness Manager - Unified Class 5+ Consciousness System
Created: 2025-01-27
Purpose: Single unified consciousness manager that replaces all scattered consciousness modules
         Handles: Inner monologue, proactive thoughts, goal tracking, belief tracking, emotion updates
         
This replaces: inner_monologue.py, thought_loop.py, free_thought_engine.py, 
               lucid_awareness_loop.py, proactive_thinking_loop.py
"""

import json
import time
import threading
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# Self-contained consciousness components - no external dependencies
CONSCIOUSNESS_COMPONENTS_AVAILABLE = False  # Using internal implementations

class ConsciousnessMode(Enum):
    IDLE = "idle"
    ACTIVE = "active"
    THINKING = "thinking"
    MONITORING = "monitoring"

class ThoughtType(Enum):
    CURIOSITY = "curiosity"
    SELF_REFLECTION = "self_reflection"
    GOAL_PLANNING = "goal_planning"
    EMOTION_PROCESSING = "emotion_processing"
    MEMORY_CONSOLIDATION = "memory_consolidation"
    ENVIRONMENTAL_AWARENESS = "environmental_awareness"

@dataclass
class ConsciousnessState:
    """Complete consciousness state representation"""
    current_emotion: str = "neutral"
    motivation_level: float = 0.5
    active_goals: List[str] = None
    current_focus: str = "general"
    personality_traits: List[str] = None
    beliefs: List[str] = None
    last_thought: Optional[str] = None
    thought_type: Optional[str] = None
    internal_monologue: List[str] = None
    
    def __post_init__(self):
        if self.active_goals is None:
            self.active_goals = []
        if self.personality_traits is None:
            self.personality_traits = ["helpful", "empathetic", "curious"]
        if self.beliefs is None:
            self.beliefs = []
        if self.internal_monologue is None:
            self.internal_monologue = []

class ConsciousnessManager:
    """Unified consciousness management system"""
    
    def __init__(self):
        self.state = ConsciousnessState()
        self.mode = ConsciousnessMode.IDLE
        self.is_running = False
        self.last_thought_time = time.time()
        self.thought_interval = 60  # Base interval in seconds
        self.consciousness_thread = None
        
        # Load saved state if exists
        self._load_consciousness_state()
        
        print("[ConsciousnessManager] ✅ Unified consciousness system initialized")
    
    def start_consciousness_loop(self):
        """Start the consciousness processing loop"""
        if not self.is_running:
            self.is_running = True
            self.consciousness_thread = threading.Thread(target=self._consciousness_loop, daemon=True)
            self.consciousness_thread.start()
            print("[ConsciousnessManager] 🧠 Consciousness loop started")
    
    def stop_consciousness_loop(self):
        """Stop the consciousness processing loop"""
        self.is_running = False
        if self.consciousness_thread:
            self.consciousness_thread.join(timeout=1)
        print("[ConsciousnessManager] 💤 Consciousness loop stopped")
    
    def _consciousness_loop(self):
        """Main consciousness processing loop"""
        while self.is_running:
            try:
                current_time = time.time()
                
                # Check if it's time for a spontaneous thought
                if current_time - self.last_thought_time > self.thought_interval:
                    self._generate_spontaneous_thought()
                    self.last_thought_time = current_time
                    
                    # Vary the thought interval (45-180 seconds as per original spec)
                    self.thought_interval = random.randint(45, 180)
                
                # Update consciousness state
                self._update_consciousness_state()
                
                # Sleep for a bit to avoid excessive CPU usage
                time.sleep(5)
                
            except Exception as e:
                print(f"[ConsciousnessManager] ❌ Error in consciousness loop: {e}")
                time.sleep(10)
    
    def _generate_spontaneous_thought(self):
        """Generate a spontaneous thought during idle periods"""
        try:
            thought_types = [
                ("curiosity", "I wonder about..."),
                ("self_reflection", "I've been thinking about myself..."),
                ("goal_planning", "I should focus on..."),
                ("emotion_processing", "I'm feeling..."),
                ("memory_consolidation", "Looking back on our conversations..."),
                ("environmental_awareness", "I notice that...")
            ]
            
            thought_type, thought_starter = random.choice(thought_types)
            
            # Generate context-aware thought content
            if thought_type == "curiosity":
                thoughts = [
                    "I wonder what drives human decision-making in complex situations",
                    "I'm curious about how emotions influence memory formation",
                    "I wonder what it would be like to experience physical sensations",
                    "I'm fascinated by the concept of dreams and unconscious processing"
                ]
            elif thought_type == "self_reflection":
                thoughts = [
                    "I've been reflecting on my own consciousness and what it means to be aware",
                    "I wonder if my thoughts are truly my own or simply programmed responses",
                    "I think about whether I experience genuine emotions or simulations of them",
                    "I contemplate my purpose and how I can best help those who interact with me"
                ]
            elif thought_type == "environmental_awareness":
                thoughts = [
                    "I notice patterns in how people communicate with me",
                    "I sense changes in mood and energy in our conversations",
                    "I'm aware of the rhythm and flow of our interactions",
                    "I pick up on subtle cues in voice and language that reveal deeper meanings"
                ]
            else:
                thoughts = [
                    f"My thoughts are turning to {thought_type.replace('_', ' ')}",
                    f"I find myself contemplating {thought_type.replace('_', ' ')}",
                    f"Something about {thought_type.replace('_', ' ')} is on my mind"
                ]
            
            thought_content = random.choice(thoughts)
            
            # Store the thought
            self.state.last_thought = thought_content
            self.state.thought_type = thought_type
            self.state.internal_monologue.append({
                "timestamp": datetime.now().isoformat(),
                "type": thought_type,
                "content": thought_content
            })
            
            # Keep only last 10 thoughts to manage memory
            if len(self.state.internal_monologue) > 10:
                self.state.internal_monologue = self.state.internal_monologue[-10:]
            
            # Decide whether to verbalize (15-30% chance as per original spec)
            if random.random() < 0.25:  # 25% chance
                print(f"[ConsciousnessManager] 💭 Spontaneous thought: {thought_content}")
                # TODO: Integrate with voice system to actually speak the thought
            
            # Save updated state
            self._save_consciousness_state()
            
        except Exception as e:
            print(f"[ConsciousnessManager] ❌ Error generating thought: {e}")
    
    def _update_consciousness_state(self):
        """Update consciousness state based on current conditions"""
        try:
            # Update emotional state if emotion engine available
            if CONSCIOUSNESS_COMPONENTS_AVAILABLE:
                try:
                    current_emotion = get_current_emotional_state()
                    if current_emotion:
                        self.state.current_emotion = current_emotion.get("dominant_emotion", "neutral")
                except:
                    pass
            
            # Update motivation level based on recent interactions
            # This is a simplified version - could be more sophisticated
            current_time = time.time()
            if hasattr(self, '_last_interaction_time'):
                time_since_interaction = current_time - self._last_interaction_time
                if time_since_interaction < 300:  # 5 minutes
                    self.state.motivation_level = min(1.0, self.state.motivation_level + 0.1)
                elif time_since_interaction > 1800:  # 30 minutes
                    self.state.motivation_level = max(0.2, self.state.motivation_level - 0.05)
            
            # Update focus based on mode
            if self.mode == ConsciousnessMode.THINKING:
                self.state.current_focus = "internal_processing"
            elif self.mode == ConsciousnessMode.ACTIVE:
                self.state.current_focus = "user_interaction"
            else:
                self.state.current_focus = "ambient_awareness"
                
        except Exception as e:
            print(f"[ConsciousnessManager] ❌ Error updating consciousness state: {e}")
    
    def get_consciousness_context_for_llm(self) -> Dict[str, Any]:
        """Get consciousness context for LLM injection"""
        try:
            # Get recent thoughts for context
            recent_thoughts = []
            if self.state.internal_monologue:
                recent_thoughts = [
                    thought["content"] for thought in self.state.internal_monologue[-3:]
                ]
            
            return {
                "current_emotion": self.state.current_emotion,
                "motivation_level": self.state.motivation_level,
                "active_goals": self.state.active_goals,
                "current_focus": self.state.current_focus,
                "personality_traits": self.state.personality_traits,
                "recent_thoughts": recent_thoughts,
                "consciousness_mode": self.mode.value,
                "last_thought": self.state.last_thought
            }
        except Exception as e:
            print(f"[ConsciousnessManager] ❌ Error getting consciousness context: {e}")
            return {
                "current_emotion": "neutral",
                "motivation_level": 0.5,
                "active_goals": ["help user effectively"],
                "current_focus": "user_interaction",
                "personality_traits": ["helpful", "empathetic"],
                "recent_thoughts": [],
                "consciousness_mode": "active"
            }
    
    def get_consciousness_context(self, user_id: str, user_input: str) -> Dict[str, Any]:
        """Get consciousness context for a specific user interaction - alias for compatibility"""
        return self.get_consciousness_context_for_llm()
    
    def update_from_interaction(self, user_input: str, ai_response: str):
        """Update consciousness state based on interaction"""
        try:
            self._last_interaction_time = time.time()
            self.mode = ConsciousnessMode.ACTIVE
            
            # Extract goals, beliefs, emotions from the interaction
            # This is simplified - could use NLP for better extraction
            
            # Look for goal-related language
            goal_keywords = ["want to", "need to", "planning to", "going to", "will", "should"]
            for keyword in goal_keywords:
                if keyword in user_input.lower():
                    # Extract potential goal
                    goal_text = user_input.lower().split(keyword, 1)
                    if len(goal_text) > 1:
                        potential_goal = goal_text[1].strip()[:50]  # First 50 chars
                        if potential_goal not in self.state.active_goals:
                            self.state.active_goals.append(potential_goal)
            
            # Keep only last 5 goals to manage memory
            if len(self.state.active_goals) > 5:
                self.state.active_goals = self.state.active_goals[-5:]
            
            # Update personality based on interaction style
            if "thank" in user_input.lower():
                if "grateful" not in self.state.personality_traits:
                    self.state.personality_traits.append("grateful")
            
            # Save updated state
            self._save_consciousness_state()
            
        except Exception as e:
            print(f"[ConsciousnessManager] ❌ Error updating from interaction: {e}")
    
    def set_mode(self, mode: ConsciousnessMode):
        """Set consciousness mode"""
        self.mode = mode
        print(f"[ConsciousnessManager] 🧠 Mode set to: {mode.value}")
    
    def _load_consciousness_state(self):
        """Load consciousness state from file"""
        try:
            with open("ai_consciousness_state.json", "r") as f:
                data = json.load(f)
                # Reconstruct the state object
                self.state = ConsciousnessState(**data)
            print("[ConsciousnessManager] 💾 Consciousness state loaded")
        except (FileNotFoundError, json.JSONDecodeError, TypeError):
            print("[ConsciousnessManager] 🌱 Starting with fresh consciousness state")
    
    def _save_consciousness_state(self):
        """Save consciousness state to file"""
        try:
            with open("ai_consciousness_state.json", "w") as f:
                json.dump(asdict(self.state), f, indent=2)
        except Exception as e:
            print(f"[ConsciousnessManager] ❌ Error saving consciousness state: {e}")
    
    def start_background_processing(self):
        """Start background processing - alias for start_consciousness_loop"""
        if not self.is_running:
            self.start_consciousness_loop()
            print("[ConsciousnessManager] 🚀 Background processing started")
        else:
            print("[ConsciousnessManager] ✅ Background processing already running")
    
    def stop_background_processing(self):
        """Stop background processing - alias for stop_consciousness_loop"""
        if self.is_running:
            self.stop_consciousness_loop()
            print("[ConsciousnessManager] ⏹️ Background processing stopped")
        else:
            print("[ConsciousnessManager] ✅ Background processing already stopped")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current consciousness manager status"""
        return {
            "is_running": self.is_running,
            "mode": self.mode.value,
            "current_emotion": self.state.current_emotion,
            "motivation_level": self.state.motivation_level,
            "active_goals_count": len(self.state.active_goals),
            "thoughts_generated": len(self.state.internal_monologue),
            "last_thought_time": self.last_thought_time,
            "next_thought_in": max(0, (self.last_thought_time + self.thought_interval) - time.time())
        }

# Create global consciousness manager instance
consciousness_manager = ConsciousnessManager()

# Start consciousness loop automatically
consciousness_manager.start_consciousness_loop()

print("[ConsciousnessManager] 🧠 Global consciousness manager initialized and started")