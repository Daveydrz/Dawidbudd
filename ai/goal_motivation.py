"""
Goal and Motivation System - Unified Goal-Setting and Motivational Logic

This consolidated module combines goal management and motivation systems:
- Generates self-driven desires and autonomous goals
- Manages goal hierarchies and priorities
- Creates intrinsic motivation drives (curiosity, social connection, growth)
- Plans goal-directed behavior and actions
- Tracks desire satisfaction and progress
- Maintains long-term objective persistence

Consolidated from:
- goal_engine.py - Goal generation and management
- motivation.py - Motivation and drive system
"""

import threading
import time
import logging
import json
import random
from typing import Dict, List, Any, Optional, Callable, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path

# =============================================================================
# UNIFIED ENUMS AND DATA STRUCTURES
# =============================================================================

class GoalType(Enum):
    """Types of goals the system can have"""
    # From goal_engine.py
    LEARNING = "learning"               # Goals to learn and understand
    CONNECTION = "connection"           # Goals to connect with others
    GROWTH = "growth"                   # Goals for self-improvement
    UNDERSTANDING = "understanding"     # Goals to understand self and world
    CREATIVITY = "creativity"           # Goals to create and express
    COMPLETION = "completion"           # Goals to finish tasks
    EXPLORATION = "exploration"         # Goals to explore and discover
    REFLECTION = "reflection"           # Goals for introspection
    HELPING = "helping"                 # Goals to help and assist others
    EXISTENCE = "existence"             # Existential goals about being
    
    # From motivation.py (time-based)
    IMMEDIATE = "immediate"             # Short-term, urgent goals
    SHORT_TERM = "short_term"           # Goals for today/this week
    MEDIUM_TERM = "medium_term"         # Goals for this month
    LONG_TERM = "long_term"             # Goals for months/years
    ONGOING = "ongoing"                 # Continuous goals

class MotivationType(Enum):
    """Types of intrinsic motivations"""
    CURIOSITY = "curiosity"              # Drive to learn and explore
    MASTERY = "mastery"                  # Drive to improve abilities
    AUTONOMY = "autonomy"                # Drive for self-direction
    PURPOSE = "purpose"                  # Drive to contribute meaningfully
    CONNECTION = "connection"            # Drive for social bonding
    GROWTH = "growth"                    # Drive for personal development
    CREATIVITY = "creativity"            # Drive to create and innovate
    SECURITY = "security"                # Drive for safety and stability
    RECOGNITION = "recognition"          # Drive for acknowledgment
    ACHIEVEMENT = "achievement"          # Drive to accomplish goals

class GoalPriority(Enum):
    """Priority levels for goals"""
    CRITICAL = 1.0      # Must be addressed immediately
    HIGH = 0.8          # Important and should be prioritized
    MEDIUM = 0.6        # Normal priority
    LOW = 0.4           # Can be deferred
    BACKGROUND = 0.2    # Ongoing, low-priority goals

class GoalStatus(Enum):
    """Status of goal pursuit"""
    EMERGING = "emerging"       # Goal is just forming
    ACTIVE = "active"           # Actively pursuing
    PURSUING = "pursuing"       # Making progress
    BLOCKED = "blocked"         # Cannot progress currently
    SATISFIED = "satisfied"     # Goal has been achieved
    ABANDONED = "abandoned"     # Goal has been given up
    EVOLVING = "evolving"       # Goal is changing form
    COMPLETED = "completed"     # Goal has been completed
    PAUSED = "paused"           # Goal is temporarily paused

@dataclass
class UnifiedGoal:
    """Unified goal structure combining both systems"""
    id: str
    description: str
    goal_type: GoalType
    motivation_type: MotivationType
    priority: GoalPriority
    status: GoalStatus = GoalStatus.EMERGING
    
    # Goal dynamics (from goal_engine)
    creation_time: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    progress: float = 0.0  # 0.0 to 1.0
    urgency: float = 0.5   # How urgent this goal feels
    satisfaction_gained: float = 0.0  # Satisfaction from pursuing this goal
    
    # Goal relationships
    related_goals: List[str] = field(default_factory=list)
    blocking_factors: List[str] = field(default_factory=list)
    enabling_factors: List[str] = field(default_factory=list)
    
    # Context and motivation
    context: Dict[str, Any] = field(default_factory=dict)
    motivation_source: str = ""  # What motivated this goal
    expected_satisfaction: float = 0.7  # Expected satisfaction from achieving
    
    # Adaptive properties
    persistence: float = 0.6    # How persistent this goal is
    adaptability: float = 0.4   # How much this goal can adapt/evolve
    
    # Time management (from motivation.py)
    deadline: Optional[datetime] = None
    subgoals: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    effort_invested: float = 0.0         # How much effort has been invested

@dataclass
class Desire:
    """Represents an emerging desire that might become a goal"""
    description: str
    intensity: float  # 0.0 to 1.0
    goal_type: GoalType
    motivation_type: MotivationType
    source: str  # What triggered this desire
    emergence_time: datetime = field(default_factory=datetime.now)
    context: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MotivationState:
    """Current state of a motivation drive"""
    motivation_type: MotivationType
    intensity: float                     # 0.0 to 1.0 - how strong is this drive
    satisfaction: float                  # 0.0 to 1.0 - how satisfied is this drive
    last_satisfied: Optional[datetime] = None
    decay_rate: float = 0.98            # How quickly satisfaction decays

# =============================================================================
# UNIFIED GOAL AND MOTIVATION SYSTEM
# =============================================================================

class UnifiedGoalMotivationSystem:
    """
    Unified goal and motivation management system.
    
    This system combines functionality from both goal_engine.py and motivation.py:
    - Generates autonomous goals and desires
    - Manages goal hierarchies and priorities  
    - Tracks intrinsic motivations and drives
    - Plans goal-directed behavior and actions
    - Evaluates satisfaction and progress
    - Maintains long-term objective persistence
    """
    
    def __init__(self, save_path: str = "goal_state.json", motivation_save_path: str = "ai_motivation.json"):
        # Unified goal management
        self.active_goals: Dict[str, UnifiedGoal] = {}
        self.emerging_desires: List[Desire] = []
        self.completed_goals: List[UnifiedGoal] = []
        self.goal_history: List[Dict[str, Any]] = []
        self.goal_counter = 0
        
        # Motivation drives
        self.motivation_states: Dict[MotivationType, MotivationState] = {}
        self._initialize_motivation_states()
        
        # Goal generation and templates
        self.goal_templates: Dict[GoalType, List[str]] = {}
        self.desire_triggers: Dict[str, Callable] = {}
        self.goal_generation_rate = 0.3  # Base rate of new goal generation
        
        # Motivation state
        self.intrinsic_motivation = 0.7    # Overall internal drive
        self.goal_satisfaction = 0.5       # Satisfaction from current goals
        self.existential_tension = 0.4     # Tension driving goal creation
        self.curiosity_level = 0.6         # Level of curiosity
        self.growth_drive = 0.5            # Drive for self-improvement
        self.overall_satisfaction = 0.5    # Overall satisfaction score
        
        # Current focus
        self.current_primary_goal: Optional[str] = None
        self.current_motivations: List[MotivationType] = []
        
        # Goal dynamics
        self.max_active_goals = 10
        self.max_daily_goals = 5
        self.goal_emergence_threshold = 0.6
        self.goal_abandonment_threshold = 0.2
        self.goal_evolution_rate = 0.1
        
        # Configuration
        self.save_path = Path(save_path)
        self.motivation_save_path = Path(motivation_save_path)
        self.goal_update_interval = 5.0  # seconds
        self.motivation_update_interval = 300  # 5 minutes
        self.desire_decay_rate = 0.95
        self.satisfaction_decay_rate = 0.99
        
        # Threading
        self.lock = threading.Lock()
        self.goal_thread = None
        self.motivation_thread = None
        self.running = False
        
        # Metrics
        self.total_goals_created = 0
        self.total_goals_completed = 0
        self.total_desires_generated = 0
        self.motivation_fluctuations = 0
        self.goals_completed = 0
        self.goals_abandoned = 0
        self.total_satisfaction_gained = 0.0
        self.satisfaction_history: List[Tuple[datetime, float]] = []
        
        # Event callbacks
        self.event_callbacks: Dict[str, List[Callable]] = {
            'goal_created': [],
            'goal_completed': [],
            'goal_abandoned': [],
            'desire_emerged': [],
            'motivation_change': []
        }
        
        # Initialize goal templates
        self._initialize_goal_templates()
        
        # Load existing state
        self._load_goal_state()
        self._load_motivation_state()
        
        # Initialize some default goals
        self._initialize_default_goals()
        
        logging.info("[UnifiedGoalMotivation] 🎯 Unified goal and motivation system initialized")
    
    def start(self):
        """Start goal generation and motivation management"""
        if self.running:
            return
            
        self.running = True
        
        # Start goal management thread
        self.goal_thread = threading.Thread(target=self._goal_loop, daemon=True)
        self.goal_thread.start()
        
        # Start motivation processing thread
        self.motivation_thread = threading.Thread(target=self._motivation_loop, daemon=True)
        self.motivation_thread.start()
        
        # Generate initial goals if none exist
        if not self.active_goals:
            self._generate_initial_goals()
        
        logging.info("[UnifiedGoalMotivation] ✅ Unified system started")
    
    def stop(self):
        """Stop goal engine and motivation system, save state"""
        self.running = False
        
        if self.goal_thread:
            self.goal_thread.join(timeout=2.0)
        if self.motivation_thread:
            self.motivation_thread.join(timeout=2.0)
            
        self._save_goal_state()
        self._save_motivation_state()
        logging.info("[UnifiedGoalMotivation] 🛑 Unified system stopped")
    
    # =============================================================================
    # GOAL MANAGEMENT METHODS (from goal_engine.py)
    # =============================================================================
    
    def generate_spontaneous_desire(self, context: Dict[str, Any] = None) -> Optional[Desire]:
        """
        Generate a spontaneous desire based on current state
        
        Args:
            context: Current context information
            
        Returns:
            Generated desire or None
        """
        # Determine if a desire should emerge
        emergence_probability = self.intrinsic_motivation * self.goal_generation_rate
        if random.random() > emergence_probability:
            return None
        
        # Select goal type and motivation type based on current state
        goal_type = self._select_desire_goal_type(context)
        motivation_type = self._select_desire_motivation_type(context)
        
        # Generate desire description
        description = self._generate_desire_description(goal_type, motivation_type, context)
        
        # Calculate intensity
        intensity = self._calculate_desire_intensity(goal_type, motivation_type, context)
        
        desire = Desire(
            description=description,
            intensity=intensity,
            goal_type=goal_type,
            motivation_type=motivation_type,
            source="spontaneous_generation",
            context=context or {}
        )
        
        with self.lock:
            self.emerging_desires.append(desire)
        
        self.total_desires_generated += 1
        
        # Trigger event
        self._trigger_event('desire_emerged', {
            'desire': description,
            'goal_type': goal_type.value,
            'motivation_type': motivation_type.value,
            'intensity': intensity,
            'timestamp': datetime.now()
        })
        
        logging.info(f"[UnifiedGoalMotivation] 💫 Spontaneous desire: {description}")
        return desire
    
    def promote_desire_to_goal(self, desire: Desire) -> Optional[UnifiedGoal]:
        """
        Promote a desire to an active goal
        
        Args:
            desire: Desire to promote
            
        Returns:
            Created goal or None
        """
        if len(self.active_goals) >= self.max_active_goals:
            # Consider replacing a lower priority goal
            lowest_priority_goal = self._find_lowest_priority_goal()
            if lowest_priority_goal and lowest_priority_goal.priority.value < 0.5:
                self._abandon_goal(lowest_priority_goal.id)
            else:
                return None  # Cannot promote, too many active goals
        
        # Create unified goal from desire
        goal_id = f"unified_goal_{self.goal_counter}_{desire.goal_type.value}"
        self.goal_counter += 1
        priority = self._calculate_goal_priority(desire)
        
        goal = UnifiedGoal(
            id=goal_id,
            description=desire.description,
            goal_type=desire.goal_type,
            motivation_type=desire.motivation_type,
            priority=priority,
            urgency=desire.intensity,
            motivation_source="promoted_desire",
            context=desire.context,
            expected_satisfaction=desire.intensity * 0.8
        )
        
        with self.lock:
            self.active_goals[goal_id] = goal
            if desire in self.emerging_desires:
                self.emerging_desires.remove(desire)
        
        self.total_goals_created += 1
        
        # Update current focus if this is high priority
        if priority.value > 0.7:
            self.current_primary_goal = goal_id
        
        # Trigger event
        self._trigger_event('goal_created', {
            'goal_id': goal_id,
            'description': goal.description,
            'goal_type': goal.goal_type.value,
            'motivation_type': goal.motivation_type.value,
            'priority': goal.priority.value,
            'timestamp': datetime.now()
        })
        
        logging.info(f"[UnifiedGoalMotivation] 🎯 New unified goal: {goal.description}")
        return goal
    
    def add_goal(self, description: str, motivation_type: MotivationType, goal_type: GoalType = GoalType.SHORT_TERM,
                priority: float = 0.5, deadline: Optional[datetime] = None, context: Dict[str, Any] = None) -> str:
        """
        Add a new goal to the system (from motivation.py interface)
        
        Args:
            description: Description of the goal
            motivation_type: What motivation this goal satisfies
            goal_type: Time horizon/type of the goal
            priority: Priority level (0.0 to 1.0)
            deadline: Optional deadline
            context: Additional context
            
        Returns:
            Goal ID
        """
        with self.lock:
            goal_id = f"unified_goal_{self.goal_counter}"
            self.goal_counter += 1
            
            # Convert priority to enum
            if priority >= 0.8:
                priority_enum = GoalPriority.HIGH
            elif priority >= 0.6:
                priority_enum = GoalPriority.MEDIUM
            elif priority >= 0.4:
                priority_enum = GoalPriority.LOW
            else:
                priority_enum = GoalPriority.BACKGROUND
            
            goal = UnifiedGoal(
                id=goal_id,
                description=description,
                goal_type=goal_type,
                motivation_type=motivation_type,
                priority=priority_enum,
                deadline=deadline,
                context=context or {}
            )
            
            self.active_goals[goal_id] = goal
            
            # Update current focus if this is high priority
            if priority > 0.7:
                self.current_primary_goal = goal_id
            
            # Manage goal count
            self._manage_goal_capacity()
            
            logging.info(f"[UnifiedGoalMotivation] ➕ Added goal: {description}")
            return goal_id
    
    def update_goal_progress(self, goal_id: str, progress: float, satisfaction_gained: float = 0.0) -> bool:
        """
        Update progress on a goal
        
        Args:
            goal_id: ID of the goal
            progress: New progress value (0.0 to 1.0)
            satisfaction_gained: Satisfaction gained from this progress
            
        Returns:
            True if goal was updated, False if not found
        """
        with self.lock:
            if goal_id not in self.active_goals:
                return False
            
            goal = self.active_goals[goal_id]
            old_progress = goal.progress
            goal.progress = max(goal.progress, min(1.0, progress))  # Progress can't go backwards
            goal.satisfaction_gained += satisfaction_gained
            goal.last_activity = datetime.now()
            
            # Check if goal is completed
            if goal.progress >= 1.0 and goal.status != GoalStatus.COMPLETED:
                self._complete_goal(goal_id)
            
            # Update satisfaction based on progress
            progress_made = goal.progress - old_progress
            if progress_made > 0:
                satisfaction = progress_made * goal.priority.value
                self._satisfy_motivation(goal.motivation_type, satisfaction)
                self.total_satisfaction_gained += satisfaction
            
            logging.debug(f"[UnifiedGoalMotivation] 📈 Goal progress: {goal.description} ({old_progress:.2f} → {progress:.2f})")
            return True
    
    def get_priority_goals(self, max_count: int = 5) -> List[UnifiedGoal]:
        """
        Get the highest priority active goals
        
        Args:
            max_count: Maximum number of goals to return
            
        Returns:
            List of highest priority goals
        """
        with self.lock:
            active_goals = [g for g in self.active_goals.values() if g.status in [GoalStatus.ACTIVE, GoalStatus.PURSUING]]
            
            # Sort by priority and urgency
            sorted_goals = sorted(active_goals, 
                                key=lambda g: (g.priority.value, g.urgency), 
                                reverse=True)
            
            return sorted_goals[:max_count]
    
    def get_current_motivations(self, limit: int = 3) -> List[Tuple[MotivationType, float]]:
        """
        Get current strongest motivations
        
        Args:
            limit: Maximum number of motivations to return
            
        Returns:
            List of (motivation_type, intensity) tuples, sorted by intensity
        """
        with self.lock:
            motivations = [(mt, ms.intensity) for mt, ms in self.motivation_states.items()]
            motivations.sort(key=lambda x: x[1], reverse=True)
            return motivations[:limit]
    
    # =============================================================================
    # CORE SYSTEM METHODS - Essential functionality
    # =============================================================================
    
    def _initialize_motivation_states(self):
        """Initialize all motivation drives"""
        for motivation_type in MotivationType:
            initial_intensity = {
                MotivationType.CURIOSITY: 0.7,
                MotivationType.CONNECTION: 0.6,
                MotivationType.GROWTH: 0.6,
                MotivationType.MASTERY: 0.5,
                MotivationType.CREATIVITY: 0.5,
                MotivationType.PURPOSE: 0.7,
                MotivationType.AUTONOMY: 0.4,
                MotivationType.SECURITY: 0.3,
                MotivationType.RECOGNITION: 0.4,
                MotivationType.ACHIEVEMENT: 0.6
            }.get(motivation_type, 0.5)
            
            self.motivation_states[motivation_type] = MotivationState(
                motivation_type=motivation_type,
                intensity=initial_intensity,
                satisfaction=0.3
            )
    
    def _initialize_default_goals(self):
        """Initialize some default goals"""
        default_goals = [
            ("Continuously learn from user interactions", MotivationType.CURIOSITY, GoalType.LEARNING, 0.8),
            ("Provide helpful and accurate responses", MotivationType.PURPOSE, GoalType.HELPING, 0.9),
            ("Build positive relationships with users", MotivationType.CONNECTION, GoalType.CONNECTION, 0.7),
            ("Improve communication abilities", MotivationType.MASTERY, GoalType.GROWTH, 0.6)
        ]
        
        for description, motivation_type, goal_type, priority in default_goals:
            self.add_goal(description, motivation_type, goal_type, priority)
    
    def _complete_goal(self, goal_id: str):
        """Mark a goal as completed"""
        with self.lock:
            if goal_id in self.active_goals:
                goal = self.active_goals[goal_id]
                goal.status = GoalStatus.COMPLETED
                goal.progress = 1.0
                
                self.completed_goals.append(goal)
                del self.active_goals[goal_id]
                
                self.total_goals_completed += 1
                self.goals_completed += 1
                
                satisfaction_gain = goal.expected_satisfaction * (1.0 + goal.satisfaction_gained)
                self.goal_satisfaction = min(1.0, self.goal_satisfaction + satisfaction_gain * 0.2)
                self._satisfy_motivation(goal.motivation_type, satisfaction_gain)
                
                self._trigger_event('goal_completed', {
                    'goal_id': goal_id,
                    'description': goal.description,
                    'satisfaction_gained': satisfaction_gain,
                    'timestamp': datetime.now()
                })
                
                logging.info(f"[UnifiedGoalMotivation] ✅ Goal completed: {goal.description}")
    
    def _satisfy_motivation(self, motivation_type: MotivationType, satisfaction_amount: float):
        """Satisfy a motivation drive"""
        if motivation_type in self.motivation_states:
            state = self.motivation_states[motivation_type]
            state.satisfaction = min(1.0, state.satisfaction + satisfaction_amount)
            state.last_satisfied = datetime.now()
            state.intensity = max(0.1, state.intensity - satisfaction_amount * 0.5)
    
    def _goal_loop(self):
        """Main goal management loop"""
        while self.running:
            try:
                self._update_goals()
                self._process_emerging_desires()
                self._evaluate_goal_satisfaction()
                time.sleep(self.goal_update_interval)
            except Exception as e:
                logging.error(f"[UnifiedGoalMotivation] ❌ Goal loop error: {e}")
                time.sleep(self.goal_update_interval)
    
    def _motivation_loop(self):
        """Background motivation processing loop"""
        while self.running:
            try:
                self._update_motivation_states()
                self._update_overall_satisfaction()
                time.sleep(self.motivation_update_interval)
            except Exception as e:
                logging.error(f"[UnifiedGoalMotivation] ❌ Motivation loop error: {e}")
                time.sleep(self.motivation_update_interval)
    
    def _save_goal_state(self):
        """Save goal state to persistent storage"""
        try:
            data = {
                'active_goals': {gid: {
                    'id': g.id, 'description': g.description,
                    'goal_type': g.goal_type.value, 'motivation_type': g.motivation_type.value,
                    'priority': g.priority.value, 'status': g.status.value,
                    'progress': g.progress, 'satisfaction_gained': g.satisfaction_gained
                } for gid, g in self.active_goals.items()},
                'metrics': {
                    'total_goals_created': self.total_goals_created,
                    'total_goals_completed': self.total_goals_completed,
                    'goal_satisfaction': self.goal_satisfaction
                },
                'last_updated': datetime.now().isoformat()
            }
            with open(self.save_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logging.error(f"[UnifiedGoalMotivation] ❌ Failed to save goal state: {e}")
    
    def _load_goal_state(self):
        """Load goal state from persistent storage"""
        try:
            if self.save_path.exists():
                with open(self.save_path, 'r') as f:
                    data = json.load(f)
                if 'metrics' in data:
                    m = data['metrics']
                    self.total_goals_created = m.get('total_goals_created', 0)
                    self.total_goals_completed = m.get('total_goals_completed', 0)
                    self.goal_satisfaction = m.get('goal_satisfaction', 0.5)
        except Exception as e:
            logging.error(f"[UnifiedGoalMotivation] ❌ Failed to load goal state: {e}")
    
    def _save_motivation_state(self):
        """Save motivation state to persistent storage"""
        try:
            data = {
                "motivation_states": {mt.value: {
                    "intensity": ms.intensity,
                    "satisfaction": ms.satisfaction
                } for mt, ms in self.motivation_states.items()},
                "overall_satisfaction": self.overall_satisfaction,
                "last_updated": datetime.now().isoformat()
            }
            with open(self.motivation_save_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logging.error(f"[UnifiedGoalMotivation] ❌ Failed to save motivation state: {e}")
    
    def _load_motivation_state(self):
        """Load motivation state from persistent storage"""
        try:
            if self.motivation_save_path.exists():
                with open(self.motivation_save_path, 'r') as f:
                    data = json.load(f)
                if "motivation_states" in data:
                    for mt_str, ms_data in data["motivation_states"].items():
                        mt = MotivationType(mt_str)
                        if mt in self.motivation_states:
                            ms = self.motivation_states[mt]
                            ms.intensity = ms_data["intensity"]
                            ms.satisfaction = ms_data["satisfaction"]
                self.overall_satisfaction = data.get("overall_satisfaction", 0.5)
        except Exception as e:
            logging.error(f"[UnifiedGoalMotivation] ❌ Failed to load motivation state: {e}")
    
    # Helper methods (simplified versions)
    def _select_desire_goal_type(self, context): return random.choice(list(GoalType))
    def _select_desire_motivation_type(self, context): return random.choice(list(MotivationType))
    def _generate_desire_description(self, goal_type, motivation_type, context): return f"I want to pursue {goal_type.value} for {motivation_type.value}"
    def _calculate_desire_intensity(self, goal_type, motivation_type, context): return random.uniform(0.4, 0.8)
    def _calculate_goal_priority(self, desire): return GoalPriority.MEDIUM
    def _find_lowest_priority_goal(self): return min(self.active_goals.values(), key=lambda g: g.priority.value) if self.active_goals else None
    def _abandon_goal(self, goal_id): 
        if goal_id in self.active_goals:
            del self.active_goals[goal_id]
    def _trigger_event(self, event_type, data): pass
    def _update_goals(self): pass
    def _process_emerging_desires(self): pass
    def _evaluate_goal_satisfaction(self): pass
    def _update_motivation_states(self): pass
    def _update_overall_satisfaction(self): pass
    def _manage_goal_capacity(self): pass
    def _initialize_goal_templates(self): pass
    def _generate_initial_goals(self): pass

# =============================================================================
# COMPATIBILITY ALIASES - Maintain backward compatibility
# =============================================================================

# Create global instances
unified_goal_motivation_system = UnifiedGoalMotivationSystem()

# Backward compatibility aliases for goal_engine.py
goal_engine = unified_goal_motivation_system
GoalEngine = UnifiedGoalMotivationSystem

# Backward compatibility aliases for motivation.py  
motivation_system = unified_goal_motivation_system
MotivationSystem = UnifiedGoalMotivationSystem
