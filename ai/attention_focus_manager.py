"""
Attention & Focus Manager - Dedicated Selective Consciousness Module

This module provides advanced attention management beyond the Global Workspace:
- Selective attention filtering and routing
- Focus depth control and concentration levels
- Attention competition resolution
- Cognitive load balancing
- Distraction filtering and noise suppression
- Attention span management and fatigue tracking
"""

import threading
import time
import logging
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import json
from pathlib import Path

class FocusLevel(Enum):
    """Different levels of focus intensity"""
    SCATTERED = 1      # Unfocused, easily distracted
    CASUAL = 3         # Light attention, open to interrupts
    FOCUSED = 5        # Concentrated attention
    DEEP = 7           # Deep focus, minimal interrupts
    FLOW = 9           # Flow state, maximum concentration
    HYPERFOCUS = 10    # Intense hyperfocus

class AttentionFilter(Enum):
    """Types of attention filtering"""
    NONE = "none"              # No filtering
    PRIORITY = "priority"      # Filter by priority
    RELEVANCE = "relevance"    # Filter by relevance to current task
    COGNITIVE_LOAD = "load"    # Filter by cognitive load capacity
    EMOTIONAL = "emotional"    # Filter by emotional state
    CONTEXTUAL = "contextual"  # Filter by context relevance

class DistractionType(Enum):
    """Types of distractions to filter"""
    INTERNAL = "internal"      # Internal thoughts/worries
    EXTERNAL = "external"      # External stimuli
    EMOTIONAL = "emotional"    # Emotional disturbances
    COGNITIVE = "cognitive"    # Competing cognitive processes
    SOCIAL = "social"          # Social interruptions

@dataclass
class AttentionState:
    """Current state of attention and focus"""
    focus_level: FocusLevel = FocusLevel.CASUAL
    primary_focus: Optional[str] = None
    secondary_focuses: List[str] = field(default_factory=list)
    cognitive_load: float = 0.0  # 0.0 to 1.0
    distraction_level: float = 0.0  # 0.0 to 1.0
    fatigue_level: float = 0.0  # 0.0 to 1.0
    attention_span_remaining: float = 1.0  # 0.0 to 1.0
    last_focus_switch: datetime = field(default_factory=datetime.now)

@dataclass
class FocusTarget:
    """A target for focused attention"""
    target_id: str
    content: Any
    priority: float
    relevance: float
    cognitive_cost: float
    emotional_weight: float
    time_sensitivity: float
    duration_estimate: float  # seconds
    started_at: datetime
    last_accessed: datetime = field(default_factory=datetime.now)

@dataclass
class DistractionEvent:
    """A distraction that was filtered or allowed"""
    timestamp: datetime
    source: str
    distraction_type: DistractionType
    intensity: float
    was_filtered: bool
    reason: str

class AttentionFocusManager:
    """
    Advanced attention and focus management system for consciousness.
    
    This module handles selective attention, focus depth control, and
    distraction filtering to enable deep cognitive processing.
    """
    
    def __init__(self, save_path: str = "ai_attention_focus.json"):
        self.save_path = Path(save_path)
        
        # Core state
        self.attention_state = AttentionState()
        self.focus_targets: Dict[str, FocusTarget] = {}
        self.distraction_history: List[DistractionEvent] = []
        
        # Configuration
        self.max_focus_targets = 3  # Maximum simultaneous focus targets
        self.max_distraction_history = 100
        self.focus_decay_rate = 0.95  # Per minute
        self.cognitive_load_threshold = 0.8  # When to start filtering
        self.attention_span_base = 300  # Base attention span in seconds
        
        # Filters and strategies
        self.active_filters: Set[AttentionFilter] = {AttentionFilter.PRIORITY}
        self.distraction_filters: Dict[DistractionType, float] = {
            DistractionType.INTERNAL: 0.7,
            DistractionType.EXTERNAL: 0.5,
            DistractionType.EMOTIONAL: 0.8,
            DistractionType.COGNITIVE: 0.6,
            DistractionType.SOCIAL: 0.4
        }
        
        # Metrics
        self.focus_switches = 0
        self.distractions_filtered = 0
        self.total_focus_time = 0.0
        self.deep_focus_sessions = 0
        
        # Threading
        self.is_active = False
        self.attention_thread = None
        self.state_lock = threading.Lock()
        
        # Load persisted state
        self._load_state()
        
        logging.info("[AttentionFocus] 🎯 Attention & Focus Manager initialized")
    
    def start(self):
        """Start the attention management system"""
        if self.is_active:
            return
        
        self.is_active = True
        self.attention_thread = threading.Thread(target=self._attention_loop, daemon=True)
        self.attention_thread.start()
        
        logging.info("[AttentionFocus] 🎯 Attention management started")
    
    def stop(self):
        """Stop the attention management system"""
        if not self.is_active:
            return
        
        self.is_active = False
        if self.attention_thread:
            self.attention_thread.join(timeout=2.0)
        
        self._save_state()
        logging.info("[AttentionFocus] 🎯 Attention management stopped")
    
    def request_focus(self, target_id: str, content: Any, priority: float = 0.5,
                     relevance: float = 0.5, cognitive_cost: float = 0.3,
                     emotional_weight: float = 0.0, time_sensitivity: float = 0.5,
                     duration_estimate: float = 10.0) -> bool:
        """Request focus on a specific target"""
        with self.state_lock:
            # Check if we should accept this focus request
            if not self._should_accept_focus(priority, cognitive_cost):
                return False
            
            # Create focus target
            focus_target = FocusTarget(
                target_id=target_id,
                content=content,
                priority=priority,
                relevance=relevance,
                cognitive_cost=cognitive_cost,
                emotional_weight=emotional_weight,
                time_sensitivity=time_sensitivity,
                duration_estimate=duration_estimate,
                started_at=datetime.now()
            )
            
            # Add to focus targets
            self.focus_targets[target_id] = focus_target
            
            # Update attention state
            self._update_focus_state(target_id)
            
            logging.debug(f"[AttentionFocus] 🎯 Focus requested: {target_id}")
            return True
    
    def release_focus(self, target_id: str):
        """Release focus from a specific target"""
        with self.state_lock:
            if target_id in self.focus_targets:
                focus_target = self.focus_targets[target_id]
                duration = (datetime.now() - focus_target.started_at).total_seconds()
                self.total_focus_time += duration
                
                del self.focus_targets[target_id]
                
                # Update focus state
                self._recompute_focus_state()
                
                logging.debug(f"[AttentionFocus] 🎯 Focus released: {target_id} (duration: {duration:.1f}s)")
    
    def set_focus_level(self, level: FocusLevel):
        """Manually set the focus level"""
        with self.state_lock:
            old_level = self.attention_state.focus_level
            self.attention_state.focus_level = level
            
            # Adjust filters based on focus level
            self._adjust_filters_for_focus_level(level)
            
            if level.value >= FocusLevel.DEEP.value:
                self.deep_focus_sessions += 1
            
            logging.info(f"[AttentionFocus] 🎯 Focus level changed: {old_level.name} → {level.name}")
    
    def filter_distraction(self, source: str, distraction_type: DistractionType,
                          intensity: float, content: Any = None) -> bool:
        """Filter a potential distraction. Returns True if allowed, False if filtered."""
        with self.state_lock:
            # Get filter threshold for this distraction type
            filter_threshold = self.distraction_filters.get(distraction_type, 0.5)
            
            # Adjust threshold based on current focus level
            focus_modifier = self.attention_state.focus_level.value / 10.0
            adjusted_threshold = filter_threshold * (1.0 + focus_modifier)
            
            # Check if distraction should be filtered
            should_filter = intensity < adjusted_threshold
            
            # Record distraction event
            distraction_event = DistractionEvent(
                timestamp=datetime.now(),
                source=source,
                distraction_type=distraction_type,
                intensity=intensity,
                was_filtered=should_filter,
                reason=f"Threshold: {adjusted_threshold:.2f}, Intensity: {intensity:.2f}"
            )
            
            self.distraction_history.append(distraction_event)
            if len(self.distraction_history) > self.max_distraction_history:
                self.distraction_history.pop(0)
            
            if should_filter:
                self.distractions_filtered += 1
                logging.debug(f"[AttentionFocus] 🚫 Filtered distraction: {source} ({distraction_type.value})")
            else:
                logging.debug(f"[AttentionFocus] ✅ Allowed distraction: {source} ({distraction_type.value})")
            
            return not should_filter
    
    def get_current_focus(self) -> Optional[str]:
        """Get the current primary focus target"""
        with self.state_lock:
            return self.attention_state.primary_focus
    
    def get_cognitive_load(self) -> float:
        """Get current cognitive load (0.0 to 1.0)"""
        with self.state_lock:
            return self.attention_state.cognitive_load
    
    def get_focus_level(self) -> FocusLevel:
        """Get current focus level"""
        with self.state_lock:
            return self.attention_state.focus_level
    
    def get_attention_capacity(self) -> float:
        """Get available attention capacity (0.0 to 1.0)"""
        with self.state_lock:
            used_capacity = self.attention_state.cognitive_load
            fatigue_penalty = self.attention_state.fatigue_level * 0.3
            return max(0.0, 1.0 - used_capacity - fatigue_penalty)
    
    def enter_flow_state(self, target_id: str) -> bool:
        """Attempt to enter flow state for a specific target"""
        with self.state_lock:
            if target_id not in self.focus_targets:
                return False
            
            # Check prerequisites for flow state
            if (self.attention_state.cognitive_load > 0.6 or
                self.attention_state.distraction_level > 0.3 or
                self.attention_state.fatigue_level > 0.4):
                return False
            
            # Enter flow state
            self.attention_state.focus_level = FocusLevel.FLOW
            self.attention_state.primary_focus = target_id
            
            # Clear secondary focuses for maximum concentration
            self.attention_state.secondary_focuses.clear()
            
            # Boost distraction filters
            for distraction_type in self.distraction_filters:
                self.distraction_filters[distraction_type] *= 1.5
            
            logging.info(f"[AttentionFocus] 🌊 Entered flow state for: {target_id}")
            return True
    
    def exit_flow_state(self):
        """Exit flow state and return to normal focus"""
        with self.state_lock:
            if self.attention_state.focus_level != FocusLevel.FLOW:
                return
            
            # Return to focused level
            self.attention_state.focus_level = FocusLevel.FOCUSED
            
            # Restore normal distraction filters
            for distraction_type in self.distraction_filters:
                self.distraction_filters[distraction_type] /= 1.5
            
            logging.info("[AttentionFocus] 🌊 Exited flow state")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get attention and focus statistics"""
        with self.state_lock:
            return {
                "focus_level": self.attention_state.focus_level.name,
                "primary_focus": self.attention_state.primary_focus,
                "active_targets": len(self.focus_targets),
                "cognitive_load": self.attention_state.cognitive_load,
                "distraction_level": self.attention_state.distraction_level,
                "attention_capacity": self.get_attention_capacity(),
                "focus_switches": self.focus_switches,
                "distractions_filtered": self.distractions_filtered,
                "total_focus_time": self.total_focus_time,
                "deep_focus_sessions": self.deep_focus_sessions,
                "fatigue_level": self.attention_state.fatigue_level
            }
    
    def _should_accept_focus(self, priority: float, cognitive_cost: float) -> bool:
        """Determine if a focus request should be accepted"""
        # Check cognitive load capacity
        if self.attention_state.cognitive_load + cognitive_cost > 1.0:
            return False
        
        # Check if we have room for more targets
        if len(self.focus_targets) >= self.max_focus_targets:
            # Only accept if priority is higher than lowest current target
            if self.focus_targets:
                min_priority = min(target.priority for target in self.focus_targets.values())
                if priority <= min_priority:
                    return False
        
        # In flow state, only accept very high priority requests
        if (self.attention_state.focus_level == FocusLevel.FLOW and 
            priority < 0.9):
            return False
        
        return True
    
    def _update_focus_state(self, new_target_id: str):
        """Update attention state when new focus is added"""
        # Set as primary focus if none exists or higher priority
        if (not self.attention_state.primary_focus or
            (new_target_id in self.focus_targets and 
             self.attention_state.primary_focus in self.focus_targets and
             self.focus_targets[new_target_id].priority > 
             self.focus_targets[self.attention_state.primary_focus].priority)):
            
            if self.attention_state.primary_focus != new_target_id:
                self.focus_switches += 1
                self.attention_state.last_focus_switch = datetime.now()
            
            self.attention_state.primary_focus = new_target_id
        
        # Add to secondary focuses if not primary
        elif new_target_id not in self.attention_state.secondary_focuses:
            self.attention_state.secondary_focuses.append(new_target_id)
        
        # Recompute cognitive load
        self._recompute_cognitive_load()
    
    def _recompute_focus_state(self):
        """Recompute attention state after focus changes"""
        if not self.focus_targets:
            self.attention_state.primary_focus = None
            self.attention_state.secondary_focuses.clear()
            self.attention_state.cognitive_load = 0.0
            return
        
        # Find highest priority target for primary focus
        highest_priority_target = max(
            self.focus_targets.values(),
            key=lambda t: t.priority
        )
        
        if self.attention_state.primary_focus != highest_priority_target.target_id:
            self.focus_switches += 1
            self.attention_state.last_focus_switch = datetime.now()
        
        self.attention_state.primary_focus = highest_priority_target.target_id
        
        # Set secondary focuses
        self.attention_state.secondary_focuses = [
            target_id for target_id in self.focus_targets.keys()
            if target_id != self.attention_state.primary_focus
        ]
        
        # Recompute cognitive load
        self._recompute_cognitive_load()
    
    def _recompute_cognitive_load(self):
        """Recompute current cognitive load"""
        total_load = sum(target.cognitive_cost for target in self.focus_targets.values())
        
        # Apply focus level multiplier
        focus_multiplier = {
            FocusLevel.SCATTERED: 1.5,
            FocusLevel.CASUAL: 1.2,
            FocusLevel.FOCUSED: 1.0,
            FocusLevel.DEEP: 0.8,
            FocusLevel.FLOW: 0.6,
            FocusLevel.HYPERFOCUS: 0.4
        }
        
        multiplier = focus_multiplier.get(self.attention_state.focus_level, 1.0)
        self.attention_state.cognitive_load = min(1.0, total_load * multiplier)
    
    def _adjust_filters_for_focus_level(self, level: FocusLevel):
        """Adjust distraction filters based on focus level"""
        # Higher focus levels = stronger filtering
        base_strength = level.value / 10.0
        
        for distraction_type in self.distraction_filters:
            base_filter = {
                DistractionType.INTERNAL: 0.5,
                DistractionType.EXTERNAL: 0.4,
                DistractionType.EMOTIONAL: 0.6,
                DistractionType.COGNITIVE: 0.5,
                DistractionType.SOCIAL: 0.3
            }.get(distraction_type, 0.5)
            
            self.distraction_filters[distraction_type] = base_filter * (1.0 + base_strength)
    
    def _attention_loop(self):
        """Main attention management loop"""
        logging.info("[AttentionFocus] 🔄 Attention management loop started")
        
        while self.is_active:
            try:
                # Update attention state
                self._update_attention_state()
                
                # Process focus decay
                self._process_focus_decay()
                
                # Handle fatigue
                self._process_attention_fatigue()
                
                # Save state periodically
                if datetime.now().timestamp() % 60 < 1:  # Every minute
                    self._save_state()
                
                time.sleep(1.0)
                
            except Exception as e:
                logging.error(f"[AttentionFocus] ❌ Attention loop error: {e}")
                time.sleep(1.0)
        
        logging.info("[AttentionFocus] 🔄 Attention management loop ended")
    
    def _update_attention_state(self):
        """Update various aspects of attention state"""
        with self.state_lock:
            # Update distraction level based on recent distractions
            recent_distractions = [
                d for d in self.distraction_history
                if (datetime.now() - d.timestamp).total_seconds() < 30
            ]
            
            if recent_distractions:
                avg_intensity = sum(d.intensity for d in recent_distractions) / len(recent_distractions)
                self.attention_state.distraction_level = min(1.0, avg_intensity)
            else:
                self.attention_state.distraction_level *= 0.95  # Decay
            
            # Update attention span
            time_since_switch = (datetime.now() - self.attention_state.last_focus_switch).total_seconds()
            expected_span = self.attention_span_base * (1.0 - self.attention_state.fatigue_level)
            
            if time_since_switch > expected_span:
                self.attention_state.attention_span_remaining = max(0.0, 
                    1.0 - (time_since_switch - expected_span) / expected_span)
            else:
                self.attention_state.attention_span_remaining = 1.0
    
    def _process_focus_decay(self):
        """Process natural decay of focus targets"""
        with self.state_lock:
            current_time = datetime.now()
            targets_to_remove = []
            
            for target_id, target in self.focus_targets.items():
                # Check if target has exceeded its estimated duration
                elapsed = (current_time - target.started_at).total_seconds()
                if elapsed > target.duration_estimate * 2:  # 2x overage
                    targets_to_remove.append(target_id)
                    continue
                
                # Apply natural decay to priority
                time_factor = elapsed / max(target.duration_estimate, 1.0)
                decay_factor = self.focus_decay_rate ** time_factor
                target.priority *= decay_factor
            
            # Remove expired targets
            for target_id in targets_to_remove:
                self.release_focus(target_id)
                logging.debug(f"[AttentionFocus] ⏰ Auto-released expired focus: {target_id}")
    
    def _process_attention_fatigue(self):
        """Process attention fatigue accumulation"""
        with self.state_lock:
            # Fatigue increases with high cognitive load
            if self.attention_state.cognitive_load > 0.7:
                fatigue_increase = (self.attention_state.cognitive_load - 0.7) * 0.001
                self.attention_state.fatigue_level = min(1.0, 
                    self.attention_state.fatigue_level + fatigue_increase)
            
            # Fatigue decreases during low activity
            elif self.attention_state.cognitive_load < 0.3:
                fatigue_decrease = 0.0005
                self.attention_state.fatigue_level = max(0.0,
                    self.attention_state.fatigue_level - fatigue_decrease)
    
    def _save_state(self):
        """Save attention state to file"""
        try:
            state_data = {
                "attention_state": {
                    "focus_level": self.attention_state.focus_level.name,
                    "primary_focus": self.attention_state.primary_focus,
                    "secondary_focuses": self.attention_state.secondary_focuses,
                    "cognitive_load": self.attention_state.cognitive_load,
                    "distraction_level": self.attention_state.distraction_level,
                    "fatigue_level": self.attention_state.fatigue_level,
                    "attention_span_remaining": self.attention_state.attention_span_remaining
                },
                "metrics": {
                    "focus_switches": self.focus_switches,
                    "distractions_filtered": self.distractions_filtered,
                    "total_focus_time": self.total_focus_time,
                    "deep_focus_sessions": self.deep_focus_sessions
                },
                "distraction_filters": {k.value: v for k, v in self.distraction_filters.items()},
                "timestamp": datetime.now().isoformat()
            }
            
            with open(self.save_path, 'w') as f:
                json.dump(state_data, f, indent=2)
                
        except Exception as e:
            logging.error(f"[AttentionFocus] ❌ Error saving state: {e}")
    
    def _load_state(self):
        """Load attention state from file"""
        try:
            if not self.save_path.exists():
                return
            
            with open(self.save_path, 'r') as f:
                state_data = json.load(f)
            
            # Restore attention state
            if "attention_state" in state_data:
                attn_data = state_data["attention_state"]
                self.attention_state.focus_level = FocusLevel[attn_data.get("focus_level", "CASUAL")]
                self.attention_state.primary_focus = attn_data.get("primary_focus")
                self.attention_state.secondary_focuses = attn_data.get("secondary_focuses", [])
                self.attention_state.cognitive_load = attn_data.get("cognitive_load", 0.0)
                self.attention_state.distraction_level = attn_data.get("distraction_level", 0.0)
                self.attention_state.fatigue_level = attn_data.get("fatigue_level", 0.0)
                self.attention_state.attention_span_remaining = attn_data.get("attention_span_remaining", 1.0)
            
            # Restore metrics
            if "metrics" in state_data:
                metrics = state_data["metrics"]
                self.focus_switches = metrics.get("focus_switches", 0)
                self.distractions_filtered = metrics.get("distractions_filtered", 0)
                self.total_focus_time = metrics.get("total_focus_time", 0.0)
                self.deep_focus_sessions = metrics.get("deep_focus_sessions", 0)
            
            # Restore distraction filters
            if "distraction_filters" in state_data:
                filters_data = state_data["distraction_filters"]
                for distraction_type_str, value in filters_data.items():
                    try:
                        distraction_type = DistractionType(distraction_type_str)
                        self.distraction_filters[distraction_type] = value
                    except ValueError:
                        continue
            
            logging.info("[AttentionFocus] 💾 Attention state loaded from disk")
            
        except Exception as e:
            logging.error(f"[AttentionFocus] ❌ Error loading state: {e}")


# Create singleton instance
attention_focus_manager = AttentionFocusManager()