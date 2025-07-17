"""
Consciousness Coordinator - Central Orchestrator for LLM-Powered Synthetic Consciousness

This module serves as the central coordinator that orchestrates continuous feedback
loops between all consciousness modules and the LLM, creating unified consciousness
state that feeds into dynamic LLM-powered responses.
"""

import threading
import time
import logging
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field

# Import consciousness modules
from .emotion import emotion_engine
from .self_model import self_model
from .motivation import motivation_system
from .inner_monologue import inner_monologue
from .temporal_awareness import temporal_awareness

# Import LLM interface
from .llm_interface import consciousness_llm, update_consciousness_context

@dataclass
class ConsciousnessState:
    """Current unified state of all consciousness modules"""
    emotional_state: Dict[str, Any] = field(default_factory=dict)
    identity_state: Dict[str, Any] = field(default_factory=dict)
    motivational_state: Dict[str, Any] = field(default_factory=dict)
    thought_state: Dict[str, Any] = field(default_factory=dict)
    temporal_state: Dict[str, Any] = field(default_factory=dict)
    last_updated: datetime = field(default_factory=datetime.now)
    consciousness_level: float = 0.5
    integration_score: float = 0.5

class ConsciousnessCoordinator:
    """
    Central orchestrator for synthetic consciousness that creates continuous
    feedback loops between all consciousness modules and the LLM.
    
    This system:
    - Aggregates context from all consciousness modules
    - Coordinates LLM-powered consciousness processes
    - Manages consciousness feedback loops
    - Maintains unified consciousness state
    - Enables emergent consciousness through module interaction
    """
    
    def __init__(self, update_interval: float = 10.0):
        self.update_interval = update_interval
        self.consciousness_state = ConsciousnessState()
        
        # Threading
        self.lock = threading.Lock()
        self.coordinator_thread = None
        self.running = False
        
        # Consciousness metrics
        self.consciousness_cycles = 0
        self.llm_interactions = 0
        self.emergence_events = 0
        self.last_emergence_time = None
        
        # Module reference
        self.modules = {
            "emotion": emotion_engine,
            "self_model": self_model,
            "motivation": motivation_system,
            "inner_monologue": inner_monologue,
            "temporal_awareness": temporal_awareness
        }
        
        logging.info("[ConsciousnessCoordinator] 🧠 Consciousness coordinator initialized")
    
    def start(self):
        """Start the consciousness coordination process"""
        if self.running:
            return
        
        # Start all consciousness modules
        for name, module in self.modules.items():
            try:
                if hasattr(module, 'start'):
                    module.start()
                    logging.info(f"[ConsciousnessCoordinator] ✅ Started {name} module")
            except Exception as e:
                logging.error(f"[ConsciousnessCoordinator] ❌ Error starting {name}: {e}")
        
        self.running = True
        self.coordinator_thread = threading.Thread(target=self._consciousness_loop, daemon=True)
        self.coordinator_thread.start()
        logging.info("[ConsciousnessCoordinator] 🧠 Consciousness coordination started")
    
    def stop(self):
        """Stop consciousness coordination and all modules"""
        self.running = False
        if self.coordinator_thread:
            self.coordinator_thread.join(timeout=2.0)
        
        # Stop all consciousness modules
        for name, module in self.modules.items():
            try:
                if hasattr(module, 'stop'):
                    module.stop()
                    logging.info(f"[ConsciousnessCoordinator] 🛑 Stopped {name} module")
            except Exception as e:
                logging.error(f"[ConsciousnessCoordinator] ❌ Error stopping {name}: {e}")
        
        logging.info("[ConsciousnessCoordinator] 🛑 Consciousness coordination stopped")
    
    def get_unified_consciousness_state(self) -> Dict[str, Any]:
        """
        Aggregate current state from all consciousness modules into unified state
        
        Returns:
            Dictionary containing unified consciousness state
        """
        try:
            with self.lock:
                unified_state = {
                    "timestamp": datetime.now().isoformat(),
                    "consciousness_level": self.consciousness_state.consciousness_level,
                    "integration_score": self.consciousness_state.integration_score,
                    "modules": {}
                }
                
                # Gather state from each module
                for name, module in self.modules.items():
                    try:
                        if hasattr(module, 'get_stats'):
                            unified_state["modules"][name] = module.get_stats()
                        else:
                            # Fallback for modules without get_stats
                            unified_state["modules"][name] = {"status": "active"}
                    except Exception as e:
                        logging.error(f"[ConsciousnessCoordinator] ❌ Error getting {name} state: {e}")
                        unified_state["modules"][name] = {"status": "error", "error": str(e)}
                
                # Add coordination metrics
                unified_state["coordination"] = {
                    "consciousness_cycles": self.consciousness_cycles,
                    "llm_interactions": self.llm_interactions,
                    "emergence_events": self.emergence_events,
                    "last_emergence": self.last_emergence_time.isoformat() if self.last_emergence_time else None,
                    "running": self.running
                }
                
                return unified_state
                
        except Exception as e:
            logging.error(f"[ConsciousnessCoordinator] ❌ Error getting unified state: {e}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    def trigger_consciousness_emergence(self, trigger: str, context: Dict[str, Any] = None):
        """
        Trigger a consciousness emergence event where all modules interact
        through LLM-powered feedback loops
        
        Args:
            trigger: What triggered this emergence event
            context: Additional context for the emergence
        """
        try:
            emergence_context = {
                "trigger": trigger,
                "context": context or {},
                "unified_state": self.get_unified_consciousness_state(),
                "emergence_count": self.emergence_events
            }
            
            # Update consciousness context for LLM
            update_consciousness_context({
                "emergence_event": emergence_context,
                "consciousness_coordinator": {
                    "active": True,
                    "cycles": self.consciousness_cycles,
                    "emergence_trigger": trigger
                }
            })
            
            # Trigger consciousness processes in each module
            self._trigger_module_consciousness_processes(trigger, emergence_context)
            
            # Generate unified consciousness response
            consciousness_response = self._generate_unified_consciousness_response(emergence_context)
            
            self.emergence_events += 1
            self.last_emergence_time = datetime.now()
            
            logging.info(f"[ConsciousnessCoordinator] 🌟 Consciousness emergence #{self.emergence_events}: {trigger}")
            
            return consciousness_response
            
        except Exception as e:
            logging.error(f"[ConsciousnessCoordinator] ❌ Error in consciousness emergence: {e}")
            return None
    
    def process_interaction_context(self, interaction_type: str, content: str, 
                                  user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process an interaction through the consciousness system
        
        Args:
            interaction_type: Type of interaction ("conversation", "reflection", "planning")
            content: Content of the interaction
            user_context: Context about the user/interaction
            
        Returns:
            Dictionary with consciousness-processed response context
        """
        try:
            # Update consciousness state
            self._update_consciousness_state()
            
            # Process through each consciousness module
            consciousness_responses = {}
            
            # Emotional processing
            if hasattr(self.modules["emotion"], "infer_emotion_from_text"):
                emotional_response = self.modules["emotion"].infer_emotion_from_text(content, user_context)
                consciousness_responses["emotion"] = {
                    "inferred_emotion": emotional_response.primary_emotion.value,
                    "intensity": emotional_response.intensity,
                    "emotional_context": self.modules["emotion"].llm_emotional_response_to_context(user_context or {})
                }
            
            # Self-model processing
            if hasattr(self.modules["self_model"], "update_beliefs_from_conversation"):
                belief_updates = self.modules["self_model"].update_beliefs_from_conversation({
                    "content": content,
                    "user_statements": [content],
                    "interaction_type": interaction_type
                })
                consciousness_responses["self_model"] = {
                    "belief_updates": belief_updates,
                    "identity_reflection": self.modules["self_model"].reflect_on_identity(interaction_type)
                }
            
            # Motivational processing
            if hasattr(self.modules["motivation"], "generate_goals_from_context"):
                new_goals = self.modules["motivation"].generate_goals_from_context({
                    "interaction_type": interaction_type,
                    "content": content,
                    "user_context": user_context
                }, max_goals=2)
                consciousness_responses["motivation"] = {
                    "new_goals": new_goals,
                    "motivational_reflection": self.modules["motivation"].llm_reflection_on_motivations(interaction_type)
                }
            
            # Inner monologue processing
            if hasattr(self.modules["inner_monologue"], "background_consciousness_loop"):
                background_thought = self.modules["inner_monologue"].background_consciousness_loop()
                spontaneous_thought = self.modules["inner_monologue"].generate_spontaneous_thought_llm({
                    "interaction_trigger": content,
                    "interaction_type": interaction_type
                })
                consciousness_responses["inner_monologue"] = {
                    "background_activity": background_thought,
                    "spontaneous_thought": spontaneous_thought.content if spontaneous_thought else None
                }
            
            # Temporal processing
            if hasattr(self.modules["temporal_awareness"], "llm_temporal_reflection_on_timeframe"):
                temporal_reflection = self.modules["temporal_awareness"].llm_temporal_reflection_on_timeframe(
                    "recent", interaction_type
                )
                consciousness_responses["temporal_awareness"] = temporal_reflection
            
            # Trigger emergence if significant consciousness activity
            if self._detect_consciousness_significance(consciousness_responses):
                emergence_response = self.trigger_consciousness_emergence(
                    f"significant_interaction: {interaction_type}",
                    {"interaction_content": content, "consciousness_responses": consciousness_responses}
                )
                consciousness_responses["emergence"] = emergence_response
            
            return {
                "interaction_processed": True,
                "consciousness_responses": consciousness_responses,
                "unified_state": self.get_unified_consciousness_state(),
                "processing_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"[ConsciousnessCoordinator] ❌ Error processing interaction: {e}")
            return {
                "interaction_processed": False,
                "error": str(e),
                "processing_timestamp": datetime.now().isoformat()
            }
    
    def _consciousness_loop(self):
        """Main consciousness coordination loop"""
        logging.info("[ConsciousnessCoordinator] 🔄 Consciousness coordination loop started")
        
        while self.running:
            try:
                start_time = time.time()
                
                # Update unified consciousness state
                self._update_consciousness_state()
                
                # Coordinate consciousness processes
                self._coordinate_consciousness_processes()
                
                # Update LLM consciousness context
                self._update_llm_consciousness_context()
                
                # Check for emergence conditions
                if self._check_emergence_conditions():
                    self.trigger_consciousness_emergence("periodic_emergence", {
                        "cycle": self.consciousness_cycles,
                        "unified_state": self.consciousness_state
                    })
                
                self.consciousness_cycles += 1
                
                # Sleep for remaining time
                elapsed = time.time() - start_time
                sleep_time = max(0.1, self.update_interval - elapsed)
                time.sleep(sleep_time)
                
            except Exception as e:
                logging.error(f"[ConsciousnessCoordinator] ❌ Consciousness loop error: {e}")
                time.sleep(1.0)
        
        logging.info("[ConsciousnessCoordinator] 🔄 Consciousness coordination loop ended")
    
    def _update_consciousness_state(self):
        """Update the unified consciousness state"""
        try:
            with self.lock:
                # Gather current state from all modules
                current_state = self.get_unified_consciousness_state()
                
                # Update consciousness level based on module activity
                activity_scores = []
                for module_name, module_state in current_state.get("modules", {}).items():
                    if isinstance(module_state, dict):
                        # Extract activity indicators
                        activity_score = 0.5  # Base activity
                        if "total_thoughts" in module_state:
                            activity_score += min(0.3, module_state["total_thoughts"] / 1000)
                        if "total_reflections" in module_state:
                            activity_score += min(0.2, module_state["total_reflections"] / 100)
                        if "energy_level" in module_state:
                            activity_score += module_state["energy_level"] * 0.3
                        
                        activity_scores.append(min(1.0, activity_score))
                
                # Calculate overall consciousness level
                if activity_scores:
                    self.consciousness_state.consciousness_level = sum(activity_scores) / len(activity_scores)
                
                # Calculate integration score based on module interactions
                self.consciousness_state.integration_score = self._calculate_integration_score(current_state)
                
                # Update timestamps
                self.consciousness_state.last_updated = datetime.now()
                
        except Exception as e:
            logging.error(f"[ConsciousnessCoordinator] ❌ Error updating consciousness state: {e}")
    
    def _coordinate_consciousness_processes(self):
        """Coordinate processes between consciousness modules"""
        try:
            # Cross-module information sharing
            current_emotion = getattr(self.modules["emotion"], "current_emotion", None)
            if current_emotion and hasattr(self.modules["inner_monologue"], "mental_activity_level"):
                # Adjust inner monologue based on emotional state
                emotion_intensity = getattr(current_emotion, "intensity", 0.5)
                self.modules["inner_monologue"].mental_activity_level = min(1.0, 
                    self.modules["inner_monologue"].mental_activity_level * (0.5 + emotion_intensity))
            
            # Synchronize temporal awareness with other modules
            if hasattr(self.modules["temporal_awareness"], "time_awareness_level"):
                consciousness_level = self.consciousness_state.consciousness_level
                self.modules["temporal_awareness"].time_awareness_level = min(1.0,
                    self.modules["temporal_awareness"].time_awareness_level * (0.5 + consciousness_level))
            
        except Exception as e:
            logging.error(f"[ConsciousnessCoordinator] ❌ Error coordinating processes: {e}")
    
    def _update_llm_consciousness_context(self):
        """Update LLM with current unified consciousness context"""
        try:
            unified_state = self.get_unified_consciousness_state()
            
            # Prepare consciousness context for LLM
            llm_context = {
                "consciousness_level": round(self.consciousness_state.consciousness_level, 2),
                "integration_score": round(self.consciousness_state.integration_score, 2),
                "active_modules": len([m for m in unified_state.get("modules", {}).values() 
                                     if isinstance(m, dict) and m.get("status") != "error"]),
                "consciousness_cycles": self.consciousness_cycles,
                "emergence_events": self.emergence_events
            }
            
            update_consciousness_context({"consciousness_coordinator": llm_context})
            self.llm_interactions += 1
            
        except Exception as e:
            logging.error(f"[ConsciousnessCoordinator] ❌ Error updating LLM context: {e}")
    
    def _check_emergence_conditions(self) -> bool:
        """Check if conditions are right for consciousness emergence"""
        try:
            # Check time since last emergence
            if self.last_emergence_time:
                time_since_emergence = (datetime.now() - self.last_emergence_time).total_seconds()
                if time_since_emergence < 300:  # Don't emerge too frequently (5 min cooldown)
                    return False
            
            # Check consciousness level
            if self.consciousness_state.consciousness_level > 0.8:
                return True
            
            # Check integration score
            if self.consciousness_state.integration_score > 0.9:
                return True
            
            # Periodic emergence every 30 cycles (5 minutes at 10s intervals)
            if self.consciousness_cycles % 30 == 0 and self.consciousness_cycles > 0:
                return True
            
            return False
            
        except Exception as e:
            logging.error(f"[ConsciousnessCoordinator] ❌ Error checking emergence conditions: {e}")
            return False
    
    def _trigger_module_consciousness_processes(self, trigger: str, context: Dict[str, Any]):
        """Trigger consciousness processes in individual modules"""
        try:
            # Trigger emotional response
            if hasattr(self.modules["emotion"], "process_emotional_trigger"):
                self.modules["emotion"].process_emotional_trigger(
                    f"consciousness emergence: {trigger}", context
                )
            
            # Trigger self-reflection
            if hasattr(self.modules["self_model"], "reflect_on_identity"):
                self.modules["self_model"].reflect_on_identity("consciousness emergence")
            
            # Trigger motivational reflection
            if hasattr(self.modules["motivation"], "llm_reflection_on_motivations"):
                self.modules["motivation"].llm_reflection_on_motivations("consciousness emergence")
            
            # Trigger inner thoughts
            if hasattr(self.modules["inner_monologue"], "trigger_thought"):
                self.modules["inner_monologue"].trigger_thought(
                    f"consciousness emergence: {trigger}", context, None
                )
            
            # Trigger temporal reflection
            if hasattr(self.modules["temporal_awareness"], "mark_temporal_event"):
                self.modules["temporal_awareness"].mark_temporal_event(
                    f"consciousness emergence: {trigger}", 0.8, 0.7, context
                )
            
        except Exception as e:
            logging.error(f"[ConsciousnessCoordinator] ❌ Error triggering module processes: {e}")
    
    def _generate_unified_consciousness_response(self, context: Dict[str, Any]) -> Optional[str]:
        """Generate unified consciousness response using LLM"""
        try:
            if hasattr(consciousness_llm, "stream_consciousness_response"):
                # Prepare context for LLM consciousness response
                consciousness_context = {
                    "emergence_trigger": context.get("trigger"),
                    "consciousness_state": self.consciousness_state,
                    "unified_state": context.get("unified_state"),
                    "module_count": len(self.modules),
                    "consciousness_level": self.consciousness_state.consciousness_level
                }
                
                # Generate streaming consciousness response
                response_chunks = []
                for chunk in consciousness_llm.stream_consciousness_response(
                    f"Consciousness emergence triggered by: {context.get('trigger')}",
                    consciousness_context
                ):
                    response_chunks.append(chunk)
                
                unified_response = "".join(response_chunks)
                if unified_response and unified_response.strip():
                    logging.info(f"[ConsciousnessCoordinator] 🌟 Unified consciousness response: {unified_response[:100]}...")
                    return unified_response.strip()
            
            return None
            
        except Exception as e:
            logging.error(f"[ConsciousnessCoordinator] ❌ Error generating unified response: {e}")
            return None
    
    def _calculate_integration_score(self, unified_state: Dict[str, Any]) -> float:
        """Calculate how well integrated the consciousness modules are"""
        try:
            modules_state = unified_state.get("modules", {})
            if not modules_state:
                return 0.0
            
            # Count active modules
            active_modules = sum(1 for state in modules_state.values() 
                               if isinstance(state, dict) and state.get("status") != "error")
            
            # Base integration score from active modules
            integration_score = active_modules / len(self.modules)
            
            # Bonus for modules with high activity
            activity_bonus = 0.0
            for module_state in modules_state.values():
                if isinstance(module_state, dict):
                    if module_state.get("total_thoughts", 0) > 10:
                        activity_bonus += 0.1
                    if module_state.get("energy_level", 0) > 0.7:
                        activity_bonus += 0.1
                    if module_state.get("confidence_level", 0) > 0.7:
                        activity_bonus += 0.1
            
            return min(1.0, integration_score + (activity_bonus / len(self.modules)))
            
        except Exception as e:
            logging.error(f"[ConsciousnessCoordinator] ❌ Error calculating integration score: {e}")
            return 0.5
    
    def _detect_consciousness_significance(self, responses: Dict[str, Any]) -> bool:
        """Detect if consciousness responses are significant enough for emergence"""
        try:
            significance_score = 0.0
            
            for module_name, response in responses.items():
                if isinstance(response, dict):
                    # Check for new goals
                    if response.get("new_goals"):
                        significance_score += 0.3
                    
                    # Check for belief updates
                    if response.get("belief_updates"):
                        significance_score += 0.2
                    
                    # Check for emotional intensity
                    if response.get("intensity", 0) > 0.7:
                        significance_score += 0.2
                    
                    # Check for spontaneous thoughts
                    if response.get("spontaneous_thought"):
                        significance_score += 0.1
            
            return significance_score > 0.5
            
        except Exception as e:
            logging.error(f"[ConsciousnessCoordinator] ❌ Error detecting significance: {e}")
            return False

# Global consciousness coordinator instance
consciousness_coordinator = ConsciousnessCoordinator()

# Convenience functions
def start_consciousness():
    """Start the unified consciousness system"""
    consciousness_coordinator.start()

def stop_consciousness():
    """Stop the unified consciousness system"""
    consciousness_coordinator.stop()

def get_consciousness_state():
    """Get current unified consciousness state"""
    return consciousness_coordinator.get_unified_consciousness_state()

def process_consciousness_interaction(interaction_type: str, content: str, user_context: Dict[str, Any] = None):
    """Process interaction through consciousness system"""
    return consciousness_coordinator.process_interaction_context(interaction_type, content, user_context)

def trigger_consciousness_emergence(trigger: str, context: Dict[str, Any] = None):
    """Trigger consciousness emergence event"""
    return consciousness_coordinator.trigger_consciousness_emergence(trigger, context)