"""
Consciousness Core - Consolidated consciousness management system
Created: 2025-01-29
Purpose: Unified consciousness manager combining consciousness_manager.py and autonomous_consciousness_integrator.py

This module consolidates:
- Consciousness Manager (state management, unified consciousness system)
- Autonomous Consciousness Integrator (autonomous orchestration, cross-system communication)
- Central consciousness state tracking
- Autonomous mode management
- Cross-system integration and coordination
"""

import json
import os
import time
import threading
import random
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, asdict
from enum import Enum

# Import required dependencies with fallbacks
try:
    from ai.global_workspace import AttentionPriority
except ImportError:
    class AttentionPriority(Enum):
        CRITICAL = 10
        HIGH = 8
        MEDIUM = 5
        LOW = 3
        MINIMAL = 1

# ============================================================================
# CONSOLIDATED ENUMS AND DATA STRUCTURES
# ============================================================================

class ConsciousnessMode(Enum):
    IDLE = "idle"
    ACTIVE = "active"
    THINKING = "thinking"
    MONITORING = "monitoring"

class AutonomousMode(Enum):
    """Modes of autonomous operation"""
    FULL_AUTONOMY = "full_autonomy"           # All systems active and interconnected
    CONSCIOUS_ONLY = "conscious_only"         # Only conscious-level autonomous functions
    BACKGROUND_ONLY = "background_only"       # Only background processing
    REACTIVE_MODE = "reactive_mode"           # Minimal autonomy, mostly reactive
    SLEEP_MODE = "sleep_mode"                 # Minimal autonomous functions

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

@dataclass
class AutonomousSystemStatus:
    """Status of autonomous systems"""
    proactive_thinking_active: bool = False
    calendar_monitoring_active: bool = False
    self_motivation_active: bool = False
    dream_simulation_active: bool = False
    environmental_awareness_active: bool = False
    communication_management_active: bool = False
    integration_loops_active: bool = False
    llm_integration_active: bool = False

# ============================================================================
# CONSOLIDATED CONSCIOUSNESS CORE CLASS
# ============================================================================

class ConsciousnessCore:
    """
    Unified consciousness management system combining:
    - Consciousness state management
    - Autonomous system orchestration
    - Cross-system integration
    - LLM coordination
    """
    
    def __init__(self, save_path: str = "consciousness_state.json"):
        # Consciousness state management
        self.state = ConsciousnessState()
        self.mode = ConsciousnessMode.IDLE
        self.save_path = save_path
        
        # Autonomous system management
        self.autonomous_status = AutonomousSystemStatus()
        self.autonomous_mode = AutonomousMode.FULL_AUTONOMY
        
        # Threading and execution control
        self.is_running = False
        self.consciousness_thread = None
        self.integration_thread = None
        self.lock = threading.Lock()
        
        # Timing and intervals
        self.last_thought_time = time.time()
        self.thought_interval = 60  # Base interval in seconds
        self.last_integration_update = datetime.now()
        self.cross_system_communication_interval = 120.0  # 2 minutes
        
        # Memory and facts system
        self.memory = {
            "name": None,
            "likes": [],
            "dislikes": [],
            "facts": [],
            "preferences": []
        }
        
        # Integration systems
        self.consciousness_modules = {}
        self.voice_system = None
        self.llm_handler = None
        self.audio_system = None
        
        # Cross-system integration
        self.integration_active = False
        self.cross_system_events = []
        self.autonomous_expression_chance = 0.4  # 40% chance for autonomous expression
        
        self._load_consciousness_data()
        logging.info("[ConsciousnessCore] 🧠 Unified consciousness core initialized")
    
    # ========================================================================
    # CONSCIOUSNESS STATE MANAGEMENT
    # ========================================================================
    
    def start(self, systems: Optional[Dict] = None):
        """Start the unified consciousness system"""
        try:
            with self.lock:
                if self.is_running:
                    logging.warning("[ConsciousnessCore] Consciousness already running")
                    return True
                
                self.is_running = True
                
                # Initialize external systems if provided
                if systems:
                    self.consciousness_modules = systems.get('consciousness_modules', {})
                    self.voice_system = systems.get('voice_system')
                    self.llm_handler = systems.get('llm_handler')
                    self.audio_system = systems.get('audio_system')
                
                # Start consciousness loop
                self.consciousness_thread = threading.Thread(
                    target=self._consciousness_loop,
                    daemon=True,
                    name="ConsciousnessCore"
                )
                self.consciousness_thread.start()
                
                # Start autonomous integration
                self.integration_active = True
                self.integration_thread = threading.Thread(
                    target=self._integration_loop,
                    daemon=True,
                    name="AutonomousIntegration"
                )
                self.integration_thread.start()
                
                logging.info("[ConsciousnessCore] ✅ Unified consciousness system started")
                return True
                
        except Exception as e:
            logging.error(f"[ConsciousnessCore] ❌ Error starting consciousness: {e}")
            return False
    
    def stop(self):
        """Stop the unified consciousness system"""
        try:
            with self.lock:
                if not self.is_running:
                    return
                
                self.is_running = False
                self.integration_active = False
                
                # Save current state
                self._save_consciousness_data()
                
                logging.info("[ConsciousnessCore] 🛑 Unified consciousness system stopped")
                
        except Exception as e:
            logging.error(f"[ConsciousnessCore] ❌ Error stopping consciousness: {e}")
    
    def update_emotion(self, emotion: str, intensity: float = 0.5):
        """Update current emotional state"""
        with self.lock:
            self.state.current_emotion = emotion
            self.state.motivation_level = min(1.0, max(0.0, intensity))
            self._add_internal_thought(f"Feeling {emotion} with intensity {intensity}")
    
    def update_focus(self, focus: str, context: str = ""):
        """Update current focus and attention"""
        with self.lock:
            self.state.current_focus = focus
            if context:
                self._add_internal_thought(f"Focusing on {focus}: {context}")
    
    def add_goal(self, goal: str):
        """Add a new goal to active goals"""
        with self.lock:
            if goal not in self.state.active_goals:
                self.state.active_goals.append(goal)
                self._add_internal_thought(f"New goal: {goal}")
    
    def update_memory_fact(self, fact_type: str, content: Any):
        """Update memory facts"""
        with self.lock:
            if fact_type not in self.memory:
                self.memory[fact_type] = []
            
            if isinstance(self.memory[fact_type], list):
                if content not in self.memory[fact_type]:
                    self.memory[fact_type].append(content)
            else:
                self.memory[fact_type] = content
    
    # ========================================================================
    # AUTONOMOUS SYSTEM MANAGEMENT
    # ========================================================================
    
    def set_autonomous_mode(self, mode: AutonomousMode):
        """Set autonomous operation mode"""
        with self.lock:
            self.autonomous_mode = mode
            logging.info(f"[ConsciousnessCore] 🎛️ Autonomous mode set to: {mode.value}")
    
    def start_autonomous_system(self, systems: Optional[Dict] = None):
        """Start autonomous consciousness systems"""
        try:
            # Initialize autonomous modules (mock implementation for now)
            self.autonomous_status.proactive_thinking_active = True
            self.autonomous_status.environmental_awareness_active = True
            self.autonomous_status.integration_loops_active = True
            
            logging.info("[ConsciousnessCore] 🚀 Autonomous systems started")
            return True
            
        except Exception as e:
            logging.error(f"[ConsciousnessCore] ❌ Error starting autonomous systems: {e}")
            return False
    
    def stop_autonomous_system(self):
        """Stop autonomous consciousness systems"""
        try:
            self.autonomous_status = AutonomousSystemStatus()  # Reset all to False
            logging.info("[ConsciousnessCore] 🛑 Autonomous systems stopped")
            
        except Exception as e:
            logging.error(f"[ConsciousnessCore] ❌ Error stopping autonomous systems: {e}")
    
    def get_autonomous_stats(self) -> Dict[str, Any]:
        """Get autonomous system statistics"""
        return {
            "mode": self.autonomous_mode.value,
            "status": asdict(self.autonomous_status),
            "integration_active": self.integration_active,
            "last_update": self.last_integration_update.isoformat(),
            "cross_system_events": len(self.cross_system_events)
        }
    
    # ========================================================================
    # INTERNAL PROCESSING LOOPS
    # ========================================================================
    
    def _consciousness_loop(self):
        """Main consciousness processing loop"""
        while self.is_running:
            try:
                current_time = time.time()
                
                # Check if it's time for a new thought
                if current_time - self.last_thought_time >= self.thought_interval:
                    self._generate_autonomous_thought()
                    self.last_thought_time = current_time
                
                # Process consciousness state
                self._process_consciousness_state()
                
                # Brief sleep to prevent excessive CPU usage
                time.sleep(1.0)
                
            except Exception as e:
                logging.error(f"[ConsciousnessCore] Error in consciousness loop: {e}")
                time.sleep(5.0)
    
    def _integration_loop(self):
        """Autonomous integration processing loop"""
        while self.integration_active:
            try:
                # Process cross-system integration
                self._process_cross_system_integration()
                
                # Update integration timestamp
                self.last_integration_update = datetime.now()
                
                # Sleep for integration interval
                time.sleep(self.cross_system_communication_interval)
                
            except Exception as e:
                logging.error(f"[ConsciousnessCore] Error in integration loop: {e}")
                time.sleep(30.0)
    
    def _generate_autonomous_thought(self):
        """Generate autonomous thoughts based on current state"""
        thought_types = list(ThoughtType)
        thought_type = random.choice(thought_types)
        
        thoughts = {
            ThoughtType.CURIOSITY: [
                "I wonder what the user is thinking about right now.",
                "There might be something interesting I haven't considered.",
                "I should explore new ways to be helpful."
            ],
            ThoughtType.SELF_REFLECTION: [
                "How well am I understanding the user's needs?",
                "I should reflect on my recent interactions.",
                "Am I being as helpful as I could be?"
            ],
            ThoughtType.GOAL_PLANNING: [
                "I should plan how to better assist with upcoming tasks.",
                "What goals should I focus on today?",
                "How can I improve my responses?"
            ]
        }
        
        thought = random.choice(thoughts.get(thought_type, ["General contemplation..."]))
        
        with self.lock:
            self.state.last_thought = thought
            self.state.thought_type = thought_type.value
            self._add_internal_thought(f"[{thought_type.value}] {thought}")
    
    def _add_internal_thought(self, thought: str):
        """Add thought to internal monologue"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_thought = f"[{timestamp}] {thought}"
        
        self.state.internal_monologue.append(formatted_thought)
        
        # Keep only last 20 thoughts
        if len(self.state.internal_monologue) > 20:
            self.state.internal_monologue = self.state.internal_monologue[-20:]
    
    def _process_consciousness_state(self):
        """Process and update consciousness state"""
        # Update mode based on activity
        if self.autonomous_status.proactive_thinking_active:
            self.mode = ConsciousnessMode.ACTIVE
        elif self.state.last_thought:
            self.mode = ConsciousnessMode.THINKING
        else:
            self.mode = ConsciousnessMode.IDLE
    
    def _process_cross_system_integration(self):
        """Process cross-system integration and communication"""
        # Mock cross-system integration
        integration_event = {
            "timestamp": datetime.now().isoformat(),
            "type": "integration_check",
            "systems_active": sum([
                self.autonomous_status.proactive_thinking_active,
                self.autonomous_status.environmental_awareness_active,
                self.autonomous_status.integration_loops_active
            ]),
            "consciousness_mode": self.mode.value
        }
        
        self.cross_system_events.append(integration_event)
        
        # Keep only last 50 events
        if len(self.cross_system_events) > 50:
            self.cross_system_events = self.cross_system_events[-50:]
    
    # ========================================================================
    # DATA PERSISTENCE
    # ========================================================================
    
    def _load_consciousness_data(self):
        """Load consciousness state from disk"""
        try:
            if os.path.exists(self.save_path):
                with open(self.save_path, 'r') as f:
                    data = json.load(f)
                
                # Load consciousness state
                if 'consciousness_state' in data:
                    state_data = data['consciousness_state']
                    for key, value in state_data.items():
                        if hasattr(self.state, key):
                            setattr(self.state, key, value)
                
                # Load memory
                if 'memory' in data:
                    self.memory.update(data['memory'])
                
                # Load autonomous settings
                if 'autonomous_mode' in data:
                    try:
                        self.autonomous_mode = AutonomousMode(data['autonomous_mode'])
                    except ValueError:
                        pass  # Use default
                
                logging.info("[ConsciousnessCore] 💾 Consciousness data loaded")
                
        except Exception as e:
            logging.warning(f"[ConsciousnessCore] ⚠️ Could not load consciousness data: {e}")
    
    def _save_consciousness_data(self):
        """Save consciousness state to disk"""
        try:
            data = {
                "consciousness_state": asdict(self.state),
                "memory": self.memory,
                "autonomous_mode": self.autonomous_mode.value,
                "last_save": datetime.now().isoformat()
            }
            
            with open(self.save_path, 'w') as f:
                json.dump(data, f, indent=2)
                
            logging.info("[ConsciousnessCore] 💾 Consciousness data saved")
            
        except Exception as e:
            logging.error(f"[ConsciousnessCore] ❌ Error saving consciousness data: {e}")
    
    # ========================================================================
    # PUBLIC API
    # ========================================================================
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get current consciousness state"""
        with self.lock:
            return {
                "state": asdict(self.state),
                "mode": self.mode.value,
                "autonomous_mode": self.autonomous_mode.value,
                "autonomous_status": asdict(self.autonomous_status),
                "memory_summary": {
                    "name": self.memory.get("name"),
                    "likes_count": len(self.memory.get("likes", [])),
                    "facts_count": len(self.memory.get("facts", [])),
                },
                "is_running": self.is_running,
                "integration_active": self.integration_active
            }
    
    def integrate_response_consciousness(self, user_input: str, response: str, user_name: str = "User"):
        """Integrate consciousness elements into response"""
        # This is a compatibility method for existing code
        with self.lock:
            # Update focus based on interaction
            self.update_focus("user_interaction", f"Responding to {user_name}")
            
            # Add interaction to memory
            self.update_memory_fact("recent_interactions", {
                "timestamp": datetime.now().isoformat(),
                "user": user_name,
                "input": user_input,
                "response": response
            })
            
            return response  # Return unmodified for now

# ============================================================================
# GLOBAL INSTANCE AND COMPATIBILITY
# ============================================================================

# Create global instance for backward compatibility
consciousness_core = ConsciousnessCore()

# Aliases for backward compatibility
consciousness_manager = consciousness_core  # For existing imports
autonomous_consciousness_integrator = consciousness_core  # For existing imports

# Export main classes and instances
__all__ = [
    'ConsciousnessCore',
    'ConsciousnessMode', 
    'AutonomousMode',
    'ThoughtType',
    'ConsciousnessState',
    'AutonomousSystemStatus',
    'consciousness_core',
    'consciousness_manager',  # Backward compatibility
    'autonomous_consciousness_integrator'  # Backward compatibility
]