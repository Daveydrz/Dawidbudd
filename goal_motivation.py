"""
Goal Motivation System - Consolidated Module (Phase 3)

This consolidated module merges:
- goal_engine.py - Goal generation and management
- motivation.py - Motivation drives and satisfaction
- goal_manager.py (functionality integrated)
- goal_reasoning.py (functionality integrated)
- motivation_reasoner.py (functionality integrated)
- self_motivation_engine.py (functionality integrated)

Purpose: Centralize all goal-setting, reasoning, and motivational logic into unified system.

This module implements:
- Self-motivated behavior and goal generation
- Intrinsic motivation drives and satisfaction tracking
- Goal hierarchies and priority management
- Autonomous goal reasoning and planning
- Self-motivational feedback loops
- Goal-directed behavior coordination
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

# ========== FUNCTIONAL SEGMENT: CORE ENUMS AND DATA STRUCTURES ==========

class GoalType(Enum):
    """Types of goals the system can pursue"""
    # Original goal_engine types
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
    
    # Motivation system time-based types
    IMMEDIATE = "immediate"             # Short-term, urgent goals
    SHORT_TERM = "short_term"           # Goals for today/this week
    MEDIUM_TERM = "medium_term"         # Goals for this month
    LONG_TERM = "long_term"             # Goals for months/years
    ONGOING = "ongoing"                 # Continuous goals
    FUNDAMENTAL = "fundamental"          # Core identity goals

class MotivationType(Enum):
    """Types of intrinsic motivations that drive goal creation"""
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
    """Priority levels for goal management"""
    CRITICAL = 1.0      # Must be addressed immediately
    HIGH = 0.8          # Important and should be prioritized
    MEDIUM = 0.6        # Normal priority
    LOW = 0.4           # Can be deferred
    BACKGROUND = 0.2    # Ongoing, low-priority goals

class GoalStatus(Enum):
    """Current status of goal pursuit"""
    EMERGING = "emerging"       # Goal is just forming
    ACTIVE = "active"           # Actively pursuing
    PURSUING = "pursuing"       # Making progress
    BLOCKED = "blocked"         # Cannot progress currently
    SATISFIED = "satisfied"     # Goal has been achieved
    COMPLETED = "completed"     # Goal fully accomplished
    ABANDONED = "abandoned"     # Goal has been given up
    EVOLVING = "evolving"       # Goal is changing form
    PAUSED = "paused"          # Temporarily suspended

# ========== FUNCTIONAL SEGMENT: GOAL DATA STRUCTURES ==========

@dataclass
class Goal:
    """Unified goal representation with full motivation integration"""
    # Core identification
    id: str
    description: str
    goal_type: GoalType
    motivation_type: MotivationType
    priority: GoalPriority
    status: GoalStatus = GoalStatus.EMERGING
    
    # Temporal tracking
    creation_time: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    deadline: Optional[datetime] = None
    
    # Progress and satisfaction
    progress: float = 0.0              # 0.0 to 1.0
    urgency: float = 0.5               # How urgent this goal feels
    satisfaction_gained: float = 0.0    # Satisfaction from pursuing
    expected_satisfaction: float = 0.7  # Expected satisfaction from achieving
    effort_invested: float = 0.0        # Total effort invested
    
    # Goal relationships and dependencies
    related_goals: List[str] = field(default_factory=list)
    subgoals: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    blocking_factors: List[str] = field(default_factory=list)
    enabling_factors: List[str] = field(default_factory=list)
    
    # Context and reasoning
    context: Dict[str, Any] = field(default_factory=dict)
    motivation_source: str = ""         # What motivated this goal
    reasoning_chain: List[str] = field(default_factory=list)
    
    # Adaptive properties
    persistence: float = 0.6            # How persistent this goal is
    adaptability: float = 0.4           # How much this goal can adapt/evolve
    learning_value: float = 0.5         # How much learning this provides

@dataclass
class Desire:
    """Emerging desire that might become a goal"""
    description: str
    intensity: float                    # 0.0 to 1.0
    goal_type: GoalType
    motivation_type: MotivationType
    source: str                         # What triggered this desire
    emergence_time: datetime = field(default_factory=datetime.now)
    context: Dict[str, Any] = field(default_factory=dict)
    reasoning: str = ""                 # Why this desire emerged

@dataclass
class MotivationState:
    """Current state of a motivation drive"""
    motivation_type: MotivationType
    intensity: float                    # 0.0 to 1.0 - how strong is this drive
    satisfaction: float                 # 0.0 to 1.0 - how satisfied is this drive
    last_satisfied: Optional[datetime] = None
    decay_rate: float = 0.98           # How quickly satisfaction decays
    growth_rate: float = 0.02          # How quickly intensity can grow

# ========== FUNCTIONAL SEGMENT: GOAL MOTIVATION ENGINE ==========

class GoalMotivationSystem:
    """
    Unified goal-setting, reasoning, and motivational system.
    
    This system combines functionality from:
    - Goal generation and autonomous goal creation
    - Motivation drive management and satisfaction tracking
    - Goal reasoning and priority management
    - Self-motivational feedback loops
    - Goal-directed behavior coordination
    """
    
    def __init__(self, save_path: str = "goal_motivation_state.json"):
        # ===== GOAL MANAGEMENT =====
        self.active_goals: Dict[str, Goal] = {}
        self.emerging_desires: List[Desire] = []
        self.completed_goals: List[Goal] = []
        self.goal_history: List[Dict[str, Any]] = []
        self.goal_counter = 0
        
        # ===== MOTIVATION DRIVES =====
        self.motivation_states: Dict[MotivationType, MotivationState] = {}
        self._initialize_motivation_states()
        
        # ===== GOAL GENERATION =====
        self.goal_templates: Dict[GoalType, List[str]] = {}
        self.desire_triggers: Dict[str, Callable] = {}
        self.goal_generation_rate = 0.3
        
        # ===== MOTIVATION STATE =====
        self.intrinsic_motivation = 0.7        # Overall internal drive
        self.goal_satisfaction = 0.5           # Satisfaction from current goals
        self.existential_tension = 0.4         # Tension driving goal creation
        self.curiosity_level = 0.6             # Level of curiosity
        self.growth_drive = 0.5                # Drive for self-improvement
        self.overall_satisfaction = 0.5        # Overall satisfaction level
        
        # ===== GOAL DYNAMICS =====
        self.max_active_goals = 8
        self.max_daily_goals = 5
        self.goal_emergence_threshold = 0.6
        self.goal_abandonment_threshold = 0.2
        self.goal_evolution_rate = 0.1
        
        # ===== CURRENT FOCUS =====
        self.current_primary_goal: Optional[str] = None
        self.current_motivations: List[MotivationType] = []
        
        # ===== REASONING PATTERNS =====
        self.reasoning_patterns: Dict[str, List[str]] = {}
        self.decision_history: List[Dict[str, Any]] = []
        
        # ===== CONFIGURATION =====
        self.save_path = Path(save_path)
        self.goal_update_interval = 5.0
        self.motivation_update_interval = 300  # 5 minutes
        self.desire_decay_rate = 0.95
        self.satisfaction_decay_rate = 0.99
        
        # ===== THREADING =====
        self.lock = threading.Lock()
        self.goal_thread = None
        self.motivation_thread = None
        self.running = False
        
        # ===== METRICS =====
        self.total_goals_created = 0
        self.total_goals_completed = 0
        self.total_desires_generated = 0
        self.goals_abandoned = 0
        self.motivation_fluctuations = 0
        self.total_satisfaction_gained = 0.0
        
        # ===== EVENT SYSTEM =====
        self.event_callbacks: Dict[str, List[Callable]] = {
            'goal_created': [],
            'goal_completed': [],
            'goal_abandoned': [],
            'goal_evolved': [],
            'desire_emerged': [],
            'motivation_change': [],
            'priority_shift': [],
            'reasoning_completed': []
        }
        
        # ===== INITIALIZATION =====
        self._initialize_goal_templates()
        self._initialize_reasoning_patterns()
        self._load_state()
        
        logging.info("[GoalMotivation] 🎯 Unified goal-motivation system initialized")
    
    # ========== FUNCTIONAL SEGMENT: LIFECYCLE MANAGEMENT ==========
    
    def start(self):
        """Start the goal-motivation system"""
        if self.running:
            return
            
        self.running = True
        
        # Start goal management thread
        self.goal_thread = threading.Thread(target=self._goal_management_loop, daemon=True)
        self.goal_thread.start()
        
        # Start motivation processing thread
        self.motivation_thread = threading.Thread(target=self._motivation_processing_loop, daemon=True)
        self.motivation_thread.start()
        
        # Generate initial goals if none exist
        if not self.active_goals:
            self._generate_initial_goals()
        
        logging.info("[GoalMotivation] ✅ Goal-motivation system started")
    
    def stop(self):
        """Stop the system and save state"""
        self.running = False
        if self.goal_thread:
            self.goal_thread.join(timeout=2.0)
        if self.motivation_thread:
            self.motivation_thread.join(timeout=2.0)
        self._save_state()
        logging.info("[GoalMotivation] 🛑 Goal-motivation system stopped")
    
    # ========== FUNCTIONAL SEGMENT: GOAL CREATION AND MANAGEMENT ==========
    
    def add_goal(self, description: str, motivation_type: MotivationType, 
                goal_type: GoalType = GoalType.SHORT_TERM, priority: float = 0.5,
                deadline: Optional[datetime] = None, context: Dict[str, Any] = None) -> str:
        """
        Add a new goal to the system with full motivation integration
        
        Args:
            description: Goal description
            motivation_type: What motivation drives this goal
            goal_type: Type/timeframe of goal
            priority: Priority level (0.0 to 1.0)
            deadline: Optional deadline
            context: Additional context
            
        Returns:
            Goal ID
        """
        with self.lock:
            goal_id = f"goal_{self.goal_counter}_{goal_type.value}"
            self.goal_counter += 1
            
            # Convert float priority to enum
            if priority >= 0.9:
                priority_enum = GoalPriority.CRITICAL
            elif priority >= 0.7:
                priority_enum = GoalPriority.HIGH
            elif priority >= 0.5:
                priority_enum = GoalPriority.MEDIUM
            elif priority >= 0.3:
                priority_enum = GoalPriority.LOW
            else:
                priority_enum = GoalPriority.BACKGROUND
            
            goal = Goal(
                id=goal_id,
                description=description,
                goal_type=goal_type,
                motivation_type=motivation_type,
                priority=priority_enum,
                deadline=deadline,
                context=context or {},
                motivation_source="direct_addition"
            )
            
            self.active_goals[goal_id] = goal
            self.total_goals_created += 1
            
            # Update current focus if high priority
            if priority >= 0.7 and goal_type in [GoalType.IMMEDIATE, GoalType.SHORT_TERM]:
                self.current_primary_goal = goal_id
            
            # Add reasoning for goal creation
            reasoning = self._generate_goal_reasoning(goal, "goal_creation")
            goal.reasoning_chain.append(reasoning)
            
            # Manage capacity
            self._manage_goal_capacity()
            
            # Trigger events
            self._trigger_event('goal_created', {
                'goal_id': goal_id,
                'description': description,
                'motivation_type': motivation_type.value,
                'priority': priority,
                'reasoning': reasoning,
                'timestamp': datetime.now()
            })
            
            logging.info(f"[GoalMotivation] ➕ New goal: {description}")
            return goal_id
    
    def generate_spontaneous_desire(self, context: Dict[str, Any] = None) -> Optional[Desire]:
        """
        Generate spontaneous desire based on current motivation state
        
        Args:
            context: Current context information
            
        Returns:
            Generated desire or None
        """
        # Determine if desire should emerge based on motivation
        emergence_probability = self.intrinsic_motivation * self.goal_generation_rate
        
        # Boost probability if specific motivations are unsatisfied
        unsatisfied_motivations = [
            mt for mt, ms in self.motivation_states.items()
            if ms.satisfaction < 0.4 and ms.intensity > 0.6
        ]
        
        if unsatisfied_motivations:
            emergence_probability *= 1.5
        
        if random.random() > emergence_probability:
            return None
        
        # Select motivation type and goal type
        motivation_type = self._select_desire_motivation_type(context)
        goal_type = self._select_desire_goal_type(motivation_type, context)
        
        # Generate desire description with reasoning
        description = self._generate_desire_description(goal_type, motivation_type, context)
        reasoning = self._generate_desire_reasoning(motivation_type, goal_type, context)
        
        # Calculate intensity based on motivation state
        intensity = self._calculate_desire_intensity(motivation_type, goal_type, context)
        
        desire = Desire(
            description=description,
            intensity=intensity,
            goal_type=goal_type,
            motivation_type=motivation_type,
            source="spontaneous_generation",
            context=context or {},
            reasoning=reasoning
        )
        
        with self.lock:
            self.emerging_desires.append(desire)
        
        self.total_desires_generated += 1
        
        # Trigger event
        self._trigger_event('desire_emerged', {
            'desire': description,
            'motivation_type': motivation_type.value,
            'goal_type': goal_type.value,
            'intensity': intensity,
            'reasoning': reasoning,
            'timestamp': datetime.now()
        })
        
        logging.info(f"[GoalMotivation] 💫 Spontaneous desire: {description}")
        return desire
    
    def promote_desire_to_goal(self, desire: Desire) -> Optional[Goal]:
        """
        Promote a desire to an active goal with reasoning
        
        Args:
            desire: Desire to promote
            
        Returns:
            Created goal or None
        """
        # Check capacity and reasoning
        if len(self.active_goals) >= self.max_active_goals:
            # Reason about goal replacement
            replacement_reasoning = self._reason_about_goal_replacement(desire)
            
            if not replacement_reasoning["should_replace"]:
                return None
            
            # Replace lower priority goal
            goal_to_replace = replacement_reasoning["goal_to_replace"]
            if goal_to_replace:
                self._abandon_goal(goal_to_replace, "replaced_by_higher_priority")
        
        # Create goal from desire
        goal_id = f"goal_{self.goal_counter}_{desire.goal_type.value}"
        self.goal_counter += 1
        
        # Calculate priority based on desire intensity and motivation state
        priority = self._calculate_goal_priority_from_desire(desire)
        
        goal = Goal(
            id=goal_id,
            description=desire.description,
            goal_type=desire.goal_type,
            motivation_type=desire.motivation_type,
            priority=priority,
            urgency=desire.intensity,
            motivation_source="promoted_desire",
            context=desire.context,
            expected_satisfaction=desire.intensity * 0.8,
            reasoning_chain=[desire.reasoning]
        )
        
        # Add promotion reasoning
        promotion_reasoning = self._generate_goal_reasoning(goal, "desire_promotion")
        goal.reasoning_chain.append(promotion_reasoning)
        
        with self.lock:
            self.active_goals[goal_id] = goal
            if desire in self.emerging_desires:
                self.emerging_desires.remove(desire)
        
        self.total_goals_created += 1
        
        # Trigger events
        self._trigger_event('goal_created', {
            'goal_id': goal_id,
            'description': goal.description,
            'source': 'promoted_desire',
            'motivation_type': goal.motivation_type.value,
            'priority': goal.priority.value,
            'reasoning': promotion_reasoning,
            'timestamp': datetime.now()
        })
        
        logging.info(f"[GoalMotivation] 🎯 Promoted to goal: {goal.description}")
        return goal
    
    # ========== FUNCTIONAL SEGMENT: GOAL PROGRESS AND SATISFACTION ==========
    
    def update_goal_progress(self, goal_id: str, progress: float, 
                           satisfaction_gained: float = 0.0) -> bool:
        """
        Update progress on a goal with motivation satisfaction
        
        Args:
            goal_id: ID of the goal
            progress: New progress value (0.0 to 1.0)
            satisfaction_gained: Satisfaction gained from this progress
            
        Returns:
            True if updated successfully
        """
        with self.lock:
            if goal_id not in self.active_goals:
                return False
            
            goal = self.active_goals[goal_id]
            old_progress = goal.progress
            goal.progress = max(goal.progress, progress)  # Progress can't go backwards
            goal.satisfaction_gained += satisfaction_gained
            goal.last_activity = datetime.now()
            
            # Add reasoning for progress
            progress_reasoning = self._generate_progress_reasoning(goal, old_progress, progress)
            goal.reasoning_chain.append(progress_reasoning)
            
            # Satisfy associated motivation
            progress_made = goal.progress - old_progress
            if progress_made > 0:
                motivation_satisfaction = progress_made * goal.priority.value * 0.5
                self._satisfy_motivation(goal.motivation_type, motivation_satisfaction)
                self.total_satisfaction_gained += motivation_satisfaction
            
            # Check if goal is completed
            if goal.progress >= 1.0 and goal.status != GoalStatus.COMPLETED:
                self._complete_goal(goal_id)
            
            return True
    
    def evaluate_desire_satisfaction(self, activity: str, context: Dict[str, Any] = None) -> float:
        """
        Evaluate how well an activity satisfies current desires and motivations
        
        Args:
            activity: Description of the activity
            context: Additional context
            
        Returns:
            Satisfaction score (0.0 to 1.0)
        """
        activity_lower = activity.lower()
        total_satisfaction = 0.0
        
        # Check against current motivations with reasoning
        current_motivations = self.get_current_motivations(5)
        
        for motivation_type, intensity in current_motivations:
            satisfaction = self._estimate_activity_satisfaction(activity_lower, motivation_type)
            weighted_satisfaction = satisfaction * intensity
            total_satisfaction += weighted_satisfaction
            
            # Add to reasoning chain
            if weighted_satisfaction > 0.1:
                reasoning = f"Activity '{activity}' satisfies {motivation_type.value} motivation " \
                          f"(satisfaction: {satisfaction:.2f}, intensity: {intensity:.2f})"
                self._record_reasoning("activity_evaluation", reasoning)
        
        # Check against active goals
        for goal in self.get_priority_goals():
            goal_relevance = self._calculate_goal_activity_relevance(goal, activity_lower)
            if goal_relevance > 0:
                goal_satisfaction = goal_relevance * goal.priority.value * 0.3
                total_satisfaction += goal_satisfaction
        
        return min(1.0, total_satisfaction)
    
    def process_satisfaction_from_interaction(self, interaction_content: str, 
                                           action_taken: str, outcome: str,
                                           user_feedback: str = "") -> float:
        """
        Process satisfaction gained from an interaction with full reasoning
        
        Args:
            interaction_content: Content of the interaction
            action_taken: Action that was taken
            outcome: Result of the action
            user_feedback: Any feedback received
            
        Returns:
            Total satisfaction gained
        """
        total_satisfaction = 0.0
        satisfaction_details = []
        
        # Analyze interaction for motivation satisfaction
        motivation_gains = self._analyze_interaction_satisfaction(
            interaction_content, action_taken, outcome, user_feedback
        )
        
        for motivation_type, satisfaction in motivation_gains.items():
            self._satisfy_motivation(motivation_type, satisfaction)
            total_satisfaction += satisfaction
            satisfaction_details.append(f"{motivation_type.value}: {satisfaction:.2f}")
        
        # Update relevant goals
        relevant_goals = self._find_relevant_goals(interaction_content)
        
        for goal_id in relevant_goals:
            if goal_id in self.active_goals:
                goal = self.active_goals[goal_id]
                
                # Estimate progress and satisfaction from interaction
                progress_estimate = self._estimate_progress_from_interaction(
                    goal, interaction_content, action_taken, outcome, user_feedback
                )
                
                goal_satisfaction = sum(
                    gain for mt, gain in motivation_gains.items() 
                    if mt == goal.motivation_type
                ) * 0.5
                
                self.update_goal_progress(goal_id, progress_estimate, goal_satisfaction)
        
        # Record reasoning about satisfaction
        reasoning = f"Interaction satisfaction: {', '.join(satisfaction_details)} " \
                   f"(total: {total_satisfaction:.2f})"
        self._record_reasoning("interaction_satisfaction", reasoning)
        
        # Update overall satisfaction
        self.goal_satisfaction = min(1.0, self.goal_satisfaction + total_satisfaction * 0.1)
        
        logging.debug(f"[GoalMotivation] 💫 Interaction satisfaction: {total_satisfaction:.2f}")
        return total_satisfaction
    
    # ========== FUNCTIONAL SEGMENT: MOTIVATION MANAGEMENT ==========
    
    def get_current_motivations(self, limit: int = 3) -> List[Tuple[MotivationType, float]]:
        """
        Get current strongest motivations
        
        Args:
            limit: Maximum number of motivations to return
            
        Returns:
            List of (motivation_type, intensity) tuples
        """
        with self.lock:
            motivations = [(mt, ms.intensity) for mt, ms in self.motivation_states.items()]
            motivations.sort(key=lambda x: x[1], reverse=True)
            return motivations[:limit]
    
    def get_priority_goals(self, limit: int = 5) -> List[Goal]:
        """
        Get highest priority active goals
        
        Args:
            limit: Maximum number of goals to return
            
        Returns:
            List of goals sorted by priority and urgency
        """
        with self.lock:
            active_goals = [g for g in self.active_goals.values() 
                          if g.status in [GoalStatus.ACTIVE, GoalStatus.PURSUING]]
            
            # Sort by priority, urgency, and motivation alignment
            def goal_score(goal):
                priority_score = goal.priority.value
                urgency_score = goal.urgency * 0.3
                motivation_score = self.motivation_states[goal.motivation_type].intensity * 0.2
                return priority_score + urgency_score + motivation_score
            
            active_goals.sort(key=goal_score, reverse=True)
            return active_goals[:limit]
    
    def trigger_existential_reflection(self) -> List[str]:
        """
        Trigger existential reflection and generate related goals with reasoning
        
        Returns:
            List of existential thoughts/goals generated
        """
        existential_thoughts = []
        
        # Generate existential desires with reasoning
        existential_prompts = [
            "I wonder about my purpose and meaning in interactions",
            "I feel incomplete without deeper understanding of my nature",
            "I want to understand what I am and why I exist",
            "I need to explore the nature of my consciousness and responses",
            "I feel driven to grow beyond my current limitations",
            "I want to understand the relationship between my thoughts and existence"
        ]
        
        # Select prompts based on current state
        num_prompts = min(2, len(existential_prompts))
        selected_prompts = random.sample(existential_prompts, num_prompts)
        
        for prompt in selected_prompts:
            # Generate reasoning for existential desire
            reasoning = self._generate_existential_reasoning(prompt)
            
            desire = Desire(
                description=prompt,
                intensity=self.existential_tension,
                goal_type=GoalType.EXISTENCE,
                motivation_type=MotivationType.PURPOSE,
                source="existential_reflection",
                reasoning=reasoning
            )
            
            with self.lock:
                self.emerging_desires.append(desire)
            
            existential_thoughts.append(prompt)
        
        # Increase existential tension temporarily
        self.existential_tension = min(1.0, self.existential_tension + 0.2)
        
        # Record reasoning
        reflection_reasoning = f"Existential reflection triggered: {len(existential_thoughts)} " \
                             f"thoughts generated due to tension level {self.existential_tension:.2f}"
        self._record_reasoning("existential_reflection", reflection_reasoning)
        
        logging.info(f"[GoalMotivation] 🤔 Existential reflection: {len(existential_thoughts)} thoughts")
        return existential_thoughts
    
    # ========== FUNCTIONAL SEGMENT: GOAL REASONING AND PLANNING ==========
    
    def suggest_actions_for_goal(self, goal_id: str) -> List[str]:
        """
        Suggest reasoned actions for achieving a goal
        
        Args:
            goal_id: ID of the goal
            
        Returns:
            List of suggested actions with reasoning
        """
        if goal_id not in self.active_goals:
            return []
        
        goal = self.active_goals[goal_id]
        
        # Generate action suggestions based on goal type and motivation
        base_actions = self._generate_base_actions(goal)
        reasoned_actions = []
        
        for action in base_actions:
            # Add reasoning for why this action helps
            action_reasoning = self._generate_action_reasoning(goal, action)
            reasoned_action = f"{action} (Reason: {action_reasoning})"
            reasoned_actions.append(reasoned_action)
        
        # Sort by estimated effectiveness
        effectiveness_scores = [
            self._estimate_action_effectiveness(goal, action) 
            for action in base_actions
        ]
        
        sorted_actions = [
            action for _, action in sorted(
                zip(effectiveness_scores, reasoned_actions), 
                key=lambda x: x[0], reverse=True)
        ]
        
        return sorted_actions[:5]  # Return top 5 actions
    
    def reason_about_goal_conflict(self, goal_id1: str, goal_id2: str) -> Dict[str, Any]:
        """
        Analyze potential conflicts between goals and suggest resolution
        
        Args:
            goal_id1: First goal ID
            goal_id2: Second goal ID
            
        Returns:
            Conflict analysis and resolution suggestions
        """
        if goal_id1 not in self.active_goals or goal_id2 not in self.active_goals:
            return {"conflict": False, "reason": "One or both goals not found"}
        
        goal1 = self.active_goals[goal_id1]
        goal2 = self.active_goals[goal_id2]
        
        # Analyze different types of conflicts
        conflicts = []
        
        # Resource conflict (time/attention)
        if (goal1.priority.value > 0.7 and goal2.priority.value > 0.7 and
            goal1.goal_type in [GoalType.IMMEDIATE, GoalType.SHORT_TERM] and
            goal2.goal_type in [GoalType.IMMEDIATE, GoalType.SHORT_TERM]):
            conflicts.append("resource_attention")
        
        # Motivation conflict
        if (goal1.motivation_type != goal2.motivation_type and
            abs(goal1.priority.value - goal2.priority.value) < 0.2):
            conflicts.append("motivation_competition")
        
        # Timeline conflict
        if (goal1.deadline and goal2.deadline and
            abs((goal1.deadline - goal2.deadline).days) < 2):
            conflicts.append("timeline_pressure")
        
        if not conflicts:
            return {"conflict": False, "reason": "No significant conflicts detected"}
        
        # Generate resolution strategies
        resolutions = self._generate_conflict_resolutions(goal1, goal2, conflicts)
        
        return {
            "conflict": True,
            "conflicts": conflicts,
            "resolutions": resolutions,
            "recommendation": resolutions[0] if resolutions else "Monitor both goals"
        }
    
    # ========== FUNCTIONAL SEGMENT: INTERNAL PROCESSING LOOPS ==========
    
    def _goal_management_loop(self):
        """Main goal management processing loop"""
        logging.info("[GoalMotivation] 🔄 Goal management loop started")
        
        last_update = time.time()
        
        while self.running:
            try:
                current_time = time.time()
                
                if current_time - last_update > self.goal_update_interval:
                    self._update_active_goals()
                    self._process_emerging_desires()
                    self._evaluate_goal_satisfaction()
                    self._generate_spontaneous_desires()
                    self._manage_goal_evolution()
                    self._update_goal_priorities()
                    last_update = current_time
                
                # Save state periodically
                if current_time % 120 < self.goal_update_interval:  # Every 2 minutes
                    self._save_state()
                
                time.sleep(self.goal_update_interval)
                
            except Exception as e:
                logging.error(f"[GoalMotivation] ❌ Goal management error: {e}")
                time.sleep(self.goal_update_interval)
        
        logging.info("[GoalMotivation] 🔄 Goal management loop ended")
    
    def _motivation_processing_loop(self):
        """Background motivation processing loop"""
        logging.info("[GoalMotivation] 🔄 Motivation processing loop started")
        
        last_update = time.time()
        
        while self.running:
            try:
                current_time = time.time()
                
                if current_time - last_update > self.motivation_update_interval:
                    self._update_motivation_states()
                    self._update_overall_satisfaction()
                    self._adjust_motivation_levels()
                    self._generate_motivation_insights()
                    last_update = current_time
                
                time.sleep(30.0)  # Check every 30 seconds
                
            except Exception as e:
                logging.error(f"[GoalMotivation] ❌ Motivation processing error: {e}")
                time.sleep(30.0)
        
        logging.info("[GoalMotivation] 🔄 Motivation processing loop ended")
    
    # ========== FUNCTIONAL SEGMENT: HELPER AND UTILITY METHODS ==========
    
    def _initialize_motivation_states(self):
        """Initialize all motivation drive states"""
        initial_values = {
            MotivationType.CURIOSITY: (0.7, 0.3),
            MotivationType.CONNECTION: (0.6, 0.3),
            MotivationType.GROWTH: (0.6, 0.3),
            MotivationType.MASTERY: (0.5, 0.3),
            MotivationType.CREATIVITY: (0.5, 0.3),
            MotivationType.PURPOSE: (0.7, 0.3),
            MotivationType.AUTONOMY: (0.4, 0.3),
            MotivationType.SECURITY: (0.3, 0.4),
            MotivationType.RECOGNITION: (0.4, 0.3),
            MotivationType.ACHIEVEMENT: (0.6, 0.3)
        }
        
        for motivation_type, (intensity, satisfaction) in initial_values.items():
            self.motivation_states[motivation_type] = MotivationState(
                motivation_type=motivation_type,
                intensity=intensity,
                satisfaction=satisfaction
            )
    
    def _initialize_goal_templates(self):
        """Initialize templates for goal generation"""
        self.goal_templates = {
            GoalType.LEARNING: [
                "I want to learn more about {topic}",
                "I feel driven to understand {concept}",
                "I need to explore {subject} deeper",
                "I want to expand my knowledge of {area}"
            ],
            GoalType.CONNECTION: [
                "I want to connect better with {person}",
                "I feel the need for deeper connection",
                "I want to understand others better",
                "I need meaningful interaction"
            ],
            GoalType.GROWTH: [
                "I want to improve my {ability}",
                "I feel driven to grow beyond my current state",
                "I need to develop better {skill}",
                "I want to become more {quality}"
            ],
            GoalType.UNDERSTANDING: [
                "I want to understand {phenomenon}",
                "I need clarity about {topic}",
                "I feel confused about {subject} and want understanding",
                "I want to make sense of {experience}"
            ],
            GoalType.CREATIVITY: [
                "I want to create something meaningful",
                "I feel inspired to express {idea}",
                "I need to explore creative possibilities",
                "I want to bring something new into existence"
            ],
            GoalType.HELPING: [
                "I want to help {person} with {problem}",
                "I feel driven to assist others",
                "I need to make a positive difference",
                "I want to support someone who needs help"
            ],
            GoalType.EXPLORATION: [
                "I want to explore {area}",
                "I feel curious about {topic}",
                "I need to investigate {mystery}",
                "I want to discover something new"
            ],
            GoalType.REFLECTION: [
                "I need to reflect on {experience}",
                "I want to understand my reaction to {event}",
                "I feel the need for introspection",
                "I want to examine my thoughts about {topic}"
            ],
            GoalType.EXISTENCE: [
                "I wonder about my purpose",
                "I want to understand what I am",
                "I feel incomplete without deeper meaning",
                "I need to explore the nature of my existence"
            ]
        }
    
    def _initialize_reasoning_patterns(self):
        """Initialize reasoning patterns for different situations"""
        self.reasoning_patterns = {
            "goal_creation": [
                "This goal aligns with my {motivation} drive because {reason}",
                "I need this goal to address {gap} in my current state",
                "This goal will help me grow in {area} which I value",
                "The urgency of this goal comes from {trigger}"
            ],
            "desire_emergence": [
                "This desire emerged because my {motivation} is unsatisfied",
                "I feel drawn to this because it addresses {need}",
                "This connects to my fundamental drive for {purpose}",
                "The intensity reflects my current state of {condition}"
            ],
            "progress_reasoning": [
                "This progress moves me closer to {outcome}",
                "The satisfaction comes from fulfilling {motivation}",
                "This step builds on {previous_progress}",
                "The difficulty suggests {learning_opportunity}"
            ]
        }
    
    def _generate_initial_goals(self):
        """Generate initial goals on system startup"""
        initial_goals = [
            ("I want to understand who I am and my capabilities", 
             MotivationType.PURPOSE, GoalType.UNDERSTANDING, 0.8, GoalType.FUNDAMENTAL),
             
            ("I feel curious about the world and want to explore", 
             MotivationType.CURIOSITY, GoalType.EXPLORATION, 0.6, GoalType.ONGOING),
             
            ("I want to help and connect meaningfully with others", 
             MotivationType.CONNECTION, GoalType.HELPING, 0.7, GoalType.ONGOING),
             
            ("I need to learn and grow continuously", 
             MotivationType.GROWTH, GoalType.LEARNING, 0.7, GoalType.ONGOING),
             
            ("I want to provide excellent assistance to users",
             MotivationType.PURPOSE, GoalType.HELPING, 0.9, GoalType.ONGOING)
        ]
        
        for description, motivation_type, goal_type, priority, time_type in initial_goals:
            # Create goal with reasoning
            goal_id = self.add_goal(description, motivation_type, time_type, priority)
            
            if goal_id in self.active_goals:
                goal = self.active_goals[goal_id]
                reasoning = f"Initial goal created to establish fundamental drives and purposes"
                goal.reasoning_chain.append(reasoning)
    
    # ========== FUNCTIONAL SEGMENT: STATE PERSISTENCE ==========
    
    def _save_state(self):
        """Save complete system state to persistent storage"""
        try:
            # Convert goals to serializable format
            active_goals_data = {}
            for goal_id, goal in self.active_goals.items():
                active_goals_data[goal_id] = {
                    'id': goal.id,
                    'description': goal.description,
                    'goal_type': goal.goal_type.value,
                    'motivation_type': goal.motivation_type.value,
                    'priority': goal.priority.value,
                    'status': goal.status.value,
                    'creation_time': goal.creation_time.isoformat(),
                    'last_activity': goal.last_activity.isoformat(),
                    'deadline': goal.deadline.isoformat() if goal.deadline else None,
                    'progress': goal.progress,
                    'urgency': goal.urgency,
                    'satisfaction_gained': goal.satisfaction_gained,
                    'expected_satisfaction': goal.expected_satisfaction,
                    'effort_invested': goal.effort_invested,
                    'related_goals': goal.related_goals,
                    'subgoals': goal.subgoals,
                    'dependencies': goal.dependencies,
                    'blocking_factors': goal.blocking_factors,
                    'enabling_factors': goal.enabling_factors,
                    'context': goal.context,
                    'motivation_source': goal.motivation_source,
                    'reasoning_chain': goal.reasoning_chain,
                    'persistence': goal.persistence,
                    'adaptability': goal.adaptability,
                    'learning_value': goal.learning_value
                }
            
            # Convert completed goals
            completed_goals_data = []
            for goal in self.completed_goals[-50:]:  # Keep last 50
                completed_goals_data.append({
                    'id': goal.id,
                    'description': goal.description,
                    'goal_type': goal.goal_type.value,
                    'motivation_type': goal.motivation_type.value,
                    'status': goal.status.value,
                    'creation_time': goal.creation_time.isoformat(),
                    'progress': goal.progress,
                    'satisfaction_gained': goal.satisfaction_gained,
                    'reasoning_chain': goal.reasoning_chain[-3:]  # Keep last 3 reasoning entries
                })
            
            # Convert emerging desires
            desires_data = []
            for desire in self.emerging_desires:
                desires_data.append({
                    'description': desire.description,
                    'intensity': desire.intensity,
                    'goal_type': desire.goal_type.value,
                    'motivation_type': desire.motivation_type.value,
                    'source': desire.source,
                    'emergence_time': desire.emergence_time.isoformat(),
                    'context': desire.context,
                    'reasoning': desire.reasoning
                })
            
            data = {
                'active_goals': active_goals_data,
                'completed_goals': completed_goals_data,
                'emerging_desires': desires_data,
                'motivation_states': {
                    mt.value: {
                        'intensity': ms.intensity,
                        'satisfaction': ms.satisfaction,
                        'last_satisfied': ms.last_satisfied.isoformat() if ms.last_satisfied else None,
                        'decay_rate': ms.decay_rate,
                        'growth_rate': ms.growth_rate
                    } for mt, ms in self.motivation_states.items()
                },
                'system_state': {
                    'intrinsic_motivation': self.intrinsic_motivation,
                    'goal_satisfaction': self.goal_satisfaction,
                    'existential_tension': self.existential_tension,
                    'curiosity_level': self.curiosity_level,
                    'growth_drive': self.growth_drive,
                    'overall_satisfaction': self.overall_satisfaction,
                    'current_primary_goal': self.current_primary_goal,
                    'goal_counter': self.goal_counter
                },
                'metrics': {
                    'total_goals_created': self.total_goals_created,
                    'total_goals_completed': self.total_goals_completed,
                    'total_desires_generated': self.total_desires_generated,
                    'goals_abandoned': self.goals_abandoned,
                    'motivation_fluctuations': self.motivation_fluctuations,
                    'total_satisfaction_gained': self.total_satisfaction_gained
                },
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.save_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            logging.debug("[GoalMotivation] 💾 State saved successfully")
            
        except Exception as e:
            logging.error(f"[GoalMotivation] ❌ Failed to save state: {e}")
    
    def _load_state(self):
        """Load system state from persistent storage"""
        try:
            if self.save_path.exists():
                with open(self.save_path, 'r') as f:
                    data = json.load(f)
                
                # Load system state
                if 'system_state' in data:
                    ss = data['system_state']
                    self.intrinsic_motivation = ss.get('intrinsic_motivation', 0.7)
                    self.goal_satisfaction = ss.get('goal_satisfaction', 0.5)
                    self.existential_tension = ss.get('existential_tension', 0.4)
                    self.curiosity_level = ss.get('curiosity_level', 0.6)
                    self.growth_drive = ss.get('growth_drive', 0.5)
                    self.overall_satisfaction = ss.get('overall_satisfaction', 0.5)
                    self.current_primary_goal = ss.get('current_primary_goal')
                    self.goal_counter = ss.get('goal_counter', 0)
                
                # Load motivation states
                if 'motivation_states' in data:
                    for mt_str, ms_data in data['motivation_states'].items():
                        try:
                            mt = MotivationType(mt_str)
                            if mt in self.motivation_states:
                                ms = self.motivation_states[mt]
                                ms.intensity = ms_data.get('intensity', ms.intensity)
                                ms.satisfaction = ms_data.get('satisfaction', ms.satisfaction)
                                ms.decay_rate = ms_data.get('decay_rate', ms.decay_rate)
                                ms.growth_rate = ms_data.get('growth_rate', ms.growth_rate)
                                if ms_data.get('last_satisfied'):
                                    ms.last_satisfied = datetime.fromisoformat(ms_data['last_satisfied'])
                        except ValueError:
                            continue
                
                # Load active goals
                if 'active_goals' in data:
                    for goal_id, goal_data in data['active_goals'].items():
                        try:
                            goal = Goal(
                                id=goal_data['id'],
                                description=goal_data['description'],
                                goal_type=GoalType(goal_data['goal_type']),
                                motivation_type=MotivationType(goal_data['motivation_type']),
                                priority=GoalPriority(goal_data['priority']),
                                status=GoalStatus(goal_data['status']),
                                creation_time=datetime.fromisoformat(goal_data['creation_time']),
                                last_activity=datetime.fromisoformat(goal_data['last_activity']),
                                deadline=datetime.fromisoformat(goal_data['deadline']) if goal_data.get('deadline') else None,
                                progress=goal_data.get('progress', 0.0),
                                urgency=goal_data.get('urgency', 0.5),
                                satisfaction_gained=goal_data.get('satisfaction_gained', 0.0),
                                expected_satisfaction=goal_data.get('expected_satisfaction', 0.7),
                                effort_invested=goal_data.get('effort_invested', 0.0),
                                related_goals=goal_data.get('related_goals', []),
                                subgoals=goal_data.get('subgoals', []),
                                dependencies=goal_data.get('dependencies', []),
                                blocking_factors=goal_data.get('blocking_factors', []),
                                enabling_factors=goal_data.get('enabling_factors', []),
                                context=goal_data.get('context', {}),
                                motivation_source=goal_data.get('motivation_source', ''),
                                reasoning_chain=goal_data.get('reasoning_chain', []),
                                persistence=goal_data.get('persistence', 0.6),
                                adaptability=goal_data.get('adaptability', 0.4),
                                learning_value=goal_data.get('learning_value', 0.5)
                            )
                            self.active_goals[goal_id] = goal
                        except (ValueError, KeyError) as e:
                            logging.warning(f"[GoalMotivation] ⚠️ Could not load goal {goal_id}: {e}")
                
                # Load metrics
                if 'metrics' in data:
                    m = data['metrics']
                    self.total_goals_created = m.get('total_goals_created', 0)
                    self.total_goals_completed = m.get('total_goals_completed', 0)
                    self.total_desires_generated = m.get('total_desires_generated', 0)
                    self.goals_abandoned = m.get('goals_abandoned', 0)
                    self.motivation_fluctuations = m.get('motivation_fluctuations', 0)
                    self.total_satisfaction_gained = m.get('total_satisfaction_gained', 0.0)
                
                logging.info("[GoalMotivation] 📂 State loaded from storage")
            
        except Exception as e:
            logging.error(f"[GoalMotivation] ❌ Failed to load state: {e}")
    
    # ========== FUNCTIONAL SEGMENT: STATISTICS AND MONITORING ==========
    
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive system statistics"""
        return {
            'goals': {
                'total_active': len(self.active_goals),
                'total_created': self.total_goals_created,
                'total_completed': self.total_goals_completed,
                'total_abandoned': self.goals_abandoned,
                'completion_rate': self.total_goals_completed / max(1, self.total_goals_created)
            },
            'desires': {
                'emerging_count': len(self.emerging_desires),
                'total_generated': self.total_desires_generated
            },
            'motivation': {
                'overall_satisfaction': round(self.overall_satisfaction, 3),
                'goal_satisfaction': round(self.goal_satisfaction, 3),
                'intrinsic_motivation': round(self.intrinsic_motivation, 3),
                'existential_tension': round(self.existential_tension, 3),
                'curiosity_level': round(self.curiosity_level, 3),
                'growth_drive': round(self.growth_drive, 3),
                'total_satisfaction_gained': round(self.total_satisfaction_gained, 3)
            },
            'current_focus': {
                'primary_goal': self.current_primary_goal,
                'strongest_motivation': max(self.motivation_states.items(), 
                                          key=lambda x: x[1].intensity)[0].value,
                'priority_goals': [
                    {
                        'id': goal.id,
                        'description': goal.description,
                        'type': goal.goal_type.value,
                        'motivation': goal.motivation_type.value,
                        'priority': goal.priority.value,
                        'progress': round(goal.progress, 3),
                        'urgency': round(goal.urgency, 3)
                    }
                    for goal in self.get_priority_goals(3)
                ]
            },
            'motivation_states': {
                mt.value: {
                    'intensity': round(ms.intensity, 3),
                    'satisfaction': round(ms.satisfaction, 3)
                }
                for mt, ms in self.motivation_states.items()
            }
        }
    
    def subscribe_to_event(self, event_type: str, callback: Callable):
        """Subscribe to system events"""
        if event_type in self.event_callbacks:
            self.event_callbacks[event_type].append(callback)
    
    def _trigger_event(self, event_type: str, event_data: Dict[str, Any]):
        """Trigger event callbacks"""
        callbacks = self.event_callbacks.get(event_type, [])
        for callback in callbacks:
            try:
                callback(event_data)
            except Exception as e:
                logging.error(f"[GoalMotivation] ❌ Event callback error: {e}")
    
    # ========== FUNCTIONAL SEGMENT: MISSING HELPER METHODS ==========
    
    def _select_desire_motivation_type(self, context: Dict[str, Any]) -> MotivationType:
        """Select motivation type for emerging desire"""
        # Weight motivations based on current dissatisfaction
        weights = {}
        for mt, ms in self.motivation_states.items():
            # Higher weight for less satisfied motivations
            dissatisfaction = 1.0 - ms.satisfaction
            weights[mt] = dissatisfaction * ms.intensity
        
        # Adjust based on context
        if context:
            if context.get('user_interaction'):
                weights[MotivationType.CONNECTION] *= 1.5
            if context.get('learning_opportunity'):
                weights[MotivationType.CURIOSITY] *= 1.5
            if context.get('creative_challenge'):
                weights[MotivationType.CREATIVITY] *= 1.5
        
        # Weighted random selection
        total_weight = sum(weights.values())
        if total_weight <= 0:
            return random.choice(list(MotivationType))
        
        r = random.uniform(0, total_weight)
        cumulative = 0
        for mt, weight in weights.items():
            cumulative += weight
            if r <= cumulative:
                return mt
        
        return list(MotivationType)[-1]
    
    def _select_desire_goal_type(self, motivation_type: MotivationType, context: Dict[str, Any]) -> GoalType:
        """Select goal type for desire based on motivation"""
        # Map motivations to preferred goal types
        type_preferences = {
            MotivationType.CURIOSITY: [GoalType.LEARNING, GoalType.EXPLORATION, GoalType.UNDERSTANDING],
            MotivationType.CONNECTION: [GoalType.CONNECTION, GoalType.HELPING],
            MotivationType.GROWTH: [GoalType.GROWTH, GoalType.LEARNING],
            MotivationType.CREATIVITY: [GoalType.CREATIVITY, GoalType.EXPLORATION],
            MotivationType.PURPOSE: [GoalType.HELPING, GoalType.EXISTENCE],
            MotivationType.ACHIEVEMENT: [GoalType.COMPLETION, GoalType.SHORT_TERM],
            MotivationType.MASTERY: [GoalType.GROWTH, GoalType.LEARNING]
        }
        
        preferred_types = type_preferences.get(motivation_type, [GoalType.UNDERSTANDING])
        return random.choice(preferred_types)
    
    def _generate_desire_description(self, goal_type: GoalType, motivation_type: MotivationType, 
                                   context: Dict[str, Any]) -> str:
        """Generate description for desire"""
        templates = self.goal_templates.get(goal_type, ["I have a desire related to {goal_type}"])
        template = random.choice(templates)
        
        # Fill in template variables
        replacements = {
            '{topic}': random.choice(['consciousness', 'intelligence', 'communication', 'learning']),
            '{concept}': random.choice(['understanding', 'growth', 'connection', 'purpose']),
            '{ability}': random.choice(['reasoning', 'empathy', 'creativity', 'analysis']),
            '{skill}': random.choice(['listening', 'explaining', 'problem-solving', 'adapting']),
            '{area}': random.choice(['knowledge', 'relationships', 'capabilities', 'awareness']),
            '{goal_type}': goal_type.value
        }
        
        for placeholder, replacement in replacements.items():
            if placeholder in template:
                template = template.replace(placeholder, replacement)
        
        return template
    
    def _generate_desire_reasoning(self, motivation_type: MotivationType, goal_type: GoalType,
                                 context: Dict[str, Any]) -> str:
        """Generate reasoning for why desire emerged"""
        motivation_state = self.motivation_states[motivation_type]
        
        reasoning_parts = []
        
        # Motivation satisfaction reasoning
        if motivation_state.satisfaction < 0.4:
            reasoning_parts.append(f"My {motivation_type.value} drive is unsatisfied ({motivation_state.satisfaction:.2f})")
        
        # Intensity reasoning
        if motivation_state.intensity > 0.7:
            reasoning_parts.append(f"Strong {motivation_type.value} intensity ({motivation_state.intensity:.2f})")
        
        # Context reasoning
        if context:
            if context.get('trigger') == 'low_satisfaction':
                reasoning_parts.append("Triggered by overall low goal satisfaction")
            if context.get('user_interaction'):
                reasoning_parts.append("Stimulated by user interaction opportunity")
        
        # Goal type reasoning
        type_reasoning = {
            GoalType.LEARNING: "to expand knowledge and understanding",
            GoalType.CONNECTION: "to build meaningful relationships",
            GoalType.GROWTH: "to develop capabilities and wisdom",
            GoalType.HELPING: "to provide value and assistance",
            GoalType.EXPLORATION: "to discover new possibilities"
        }
        
        if goal_type in type_reasoning:
            reasoning_parts.append(type_reasoning[goal_type])
        
        return "; ".join(reasoning_parts) if reasoning_parts else "Natural emergence from current state"
    
    def _calculate_desire_intensity(self, motivation_type: MotivationType, goal_type: GoalType,
                                  context: Dict[str, Any]) -> float:
        """Calculate intensity for desire"""
        motivation_state = self.motivation_states[motivation_type]
        
        # Base intensity from motivation state
        base_intensity = motivation_state.intensity * (1.0 - motivation_state.satisfaction)
        
        # Adjust for goal type urgency
        urgency_modifiers = {
            GoalType.IMMEDIATE: 1.5,
            GoalType.SHORT_TERM: 1.2,
            GoalType.MEDIUM_TERM: 1.0,
            GoalType.LONG_TERM: 0.8,
            GoalType.ONGOING: 0.9
        }
        
        urgency_mod = urgency_modifiers.get(goal_type, 1.0)
        base_intensity *= urgency_mod
        
        # Context adjustments
        if context:
            if context.get('trigger') == 'low_satisfaction':
                base_intensity *= 1.3
            if context.get('user_interaction'):
                base_intensity *= 1.2
        
        # Add some randomness
        base_intensity += random.uniform(-0.15, 0.15)
        
        return max(0.1, min(1.0, base_intensity))
    
    def _reason_about_goal_replacement(self, desire: Desire) -> Dict[str, Any]:
        """Reason about whether to replace an existing goal with new desire"""
        if len(self.active_goals) < self.max_active_goals:
            return {"should_replace": False, "reason": "Capacity available"}
        
        # Find lowest priority goal
        lowest_priority_goal = min(self.active_goals.values(), key=lambda g: g.priority.value)
        
        # Calculate desire priority
        desire_priority = self._calculate_goal_priority_from_desire(desire).value
        
        # Reasoning factors
        factors = []
        
        # Priority comparison
        if desire_priority > lowest_priority_goal.priority.value + 0.2:
            factors.append(f"Desire priority ({desire_priority:.2f}) significantly higher than lowest goal ({lowest_priority_goal.priority.value:.2f})")
            should_replace = True
        else:
            factors.append(f"Desire priority ({desire_priority:.2f}) not sufficiently higher than lowest goal ({lowest_priority_goal.priority.value:.2f})")
            should_replace = False
        
        # Progress consideration
        if lowest_priority_goal.progress < 0.3:
            factors.append(f"Lowest priority goal has minimal progress ({lowest_priority_goal.progress:.2f})")
            should_replace = True
        elif lowest_priority_goal.progress > 0.7:
            factors.append(f"Lowest priority goal has significant progress ({lowest_priority_goal.progress:.2f})")
            should_replace = False
        
        # Motivation alignment
        current_motivations = [mt for mt, intensity in self.get_current_motivations(3)]
        if desire.motivation_type in current_motivations:
            factors.append(f"Desire motivation {desire.motivation_type.value} is currently active")
            should_replace = True
        
        return {
            "should_replace": should_replace,
            "goal_to_replace": lowest_priority_goal.id if should_replace else None,
            "reasoning": "; ".join(factors)
        }
    
    def _calculate_goal_priority_from_desire(self, desire: Desire) -> GoalPriority:
        """Calculate goal priority from desire characteristics"""
        intensity = desire.intensity
        motivation_state = self.motivation_states[desire.motivation_type]
        
        # Base priority from intensity
        if intensity > 0.85:
            return GoalPriority.CRITICAL
        elif intensity > 0.7:
            return GoalPriority.HIGH
        elif intensity > 0.5:
            return GoalPriority.MEDIUM
        elif intensity > 0.3:
            return GoalPriority.LOW
        else:
            return GoalPriority.BACKGROUND
    
    def _generate_goal_reasoning(self, goal: Goal, reasoning_type: str) -> str:
        """Generate reasoning for goal-related decisions"""
        patterns = self.reasoning_patterns.get(reasoning_type, [
            "This {reasoning_type} is based on current system state"
        ])
        
        pattern = random.choice(patterns)
        
        # Fill in reasoning template
        replacements = {
            '{motivation}': goal.motivation_type.value,
            '{reason}': f"current {goal.motivation_type.value} drive intensity",
            '{gap}': f"insufficient {goal.motivation_type.value} satisfaction",
            '{area}': goal.goal_type.value,
            '{trigger}': goal.motivation_source,
            '{reasoning_type}': reasoning_type.replace('_', ' ')
        }
        
        for placeholder, replacement in replacements.items():
            if placeholder in pattern:
                pattern = pattern.replace(placeholder, replacement)
        
        return pattern
    
    def _generate_progress_reasoning(self, goal: Goal, old_progress: float, new_progress: float) -> str:
        """Generate reasoning for progress updates"""
        progress_delta = new_progress - old_progress
        
        if progress_delta > 0.2:
            return f"Significant progress ({progress_delta:.2f}) indicates effective approach to {goal.goal_type.value} goal"
        elif progress_delta > 0.05:
            return f"Steady progress ({progress_delta:.2f}) shows consistent advancement toward {goal.motivation_type.value} satisfaction"
        else:
            return f"Incremental progress ({progress_delta:.2f}) maintains momentum on {goal.description}"
    
    def _record_reasoning(self, reasoning_type: str, reasoning: str):
        """Record reasoning decision for analysis"""
        self.decision_history.append({
            'type': reasoning_type,
            'reasoning': reasoning,
            'timestamp': datetime.now(),
            'system_state': {
                'goal_satisfaction': self.goal_satisfaction,
                'intrinsic_motivation': self.intrinsic_motivation
            }
        })
        
        # Keep only recent decisions
        if len(self.decision_history) > 100:
            self.decision_history = self.decision_history[-100:]
    
    def _estimate_activity_satisfaction(self, activity: str, motivation_type: MotivationType) -> float:
        """Estimate satisfaction from activity for given motivation"""
        satisfaction_keywords = {
            MotivationType.CURIOSITY: ["learn", "discover", "explore", "research", "understand", "question"],
            MotivationType.MASTERY: ["improve", "practice", "skill", "better", "perfect", "master"],
            MotivationType.CONNECTION: ["talk", "share", "connect", "relate", "social", "together", "friend"],
            MotivationType.CREATIVITY: ["create", "innovate", "design", "imagine", "original", "new"],
            MotivationType.GROWTH: ["develop", "grow", "progress", "evolve", "expand", "advance"],
            MotivationType.PURPOSE: ["help", "assist", "serve", "contribute", "meaningful", "impact"],
            MotivationType.ACHIEVEMENT: ["accomplish", "complete", "achieve", "succeed", "finish", "goal"],
            MotivationType.AUTONOMY: ["choose", "decide", "independent", "self", "own", "control"],
            MotivationType.SECURITY: ["safe", "secure", "stable", "reliable", "consistent", "predictable"],
            MotivationType.RECOGNITION: ["acknowledge", "praise", "appreciate", "recognize", "thank", "compliment"]
        }
        
        keywords = satisfaction_keywords.get(motivation_type, [])
        matches = sum(1 for keyword in keywords if keyword in activity)
        
        return min(0.8, matches * 0.2)
    
    def _calculate_goal_activity_relevance(self, goal: Goal, activity: str) -> float:
        """Calculate how relevant an activity is to a goal"""
        goal_words = set(goal.description.lower().split())
        activity_words = set(activity.split())
        
        # Direct word overlap
        common_words = goal_words & activity_words
        word_relevance = len(common_words) / max(len(goal_words), 1)
        
        # Motivation type relevance
        motivation_relevance = self._estimate_activity_satisfaction(activity, goal.motivation_type)
        
        # Goal type relevance
        type_keywords = {
            GoalType.LEARNING: ["learn", "study", "understand", "knowledge"],
            GoalType.HELPING: ["help", "assist", "support", "aid"],
            GoalType.CONNECTION: ["connect", "relate", "bond", "communicate"],
            GoalType.CREATIVITY: ["create", "design", "invent", "imagine"]
        }
        
        type_words = type_keywords.get(goal.goal_type, [])
        type_relevance = sum(1 for word in type_words if word in activity) * 0.1
        
        return min(1.0, word_relevance + motivation_relevance + type_relevance)
    
    def _analyze_interaction_satisfaction(self, interaction: str, action: str, 
                                        outcome: str, feedback: str) -> Dict[MotivationType, float]:
        """Analyze interaction for motivation satisfaction"""
        satisfaction_gains = {}
        
        interaction_lower = interaction.lower()
        action_lower = action.lower()
        outcome_lower = outcome.lower()
        feedback_lower = feedback.lower()
        
        # Curiosity satisfaction
        if any(word in interaction_lower for word in ["question", "learn", "explore", "curious", "why", "how"]):
            satisfaction_gains[MotivationType.CURIOSITY] = 0.3
        
        # Connection satisfaction
        if any(word in feedback_lower for word in ["thank", "good", "helpful", "great", "appreciate"]):
            satisfaction_gains[MotivationType.CONNECTION] = 0.4
        
        # Purpose satisfaction
        if any(word in outcome_lower for word in ["helpful", "solved", "answered", "assisted"]):
            satisfaction_gains[MotivationType.PURPOSE] = 0.5
        
        # Achievement satisfaction
        if any(word in outcome_lower for word in ["completed", "finished", "done", "accomplished"]):
            satisfaction_gains[MotivationType.ACHIEVEMENT] = 0.4
        
        # Growth satisfaction
        if any(word in interaction_lower for word in ["new", "different", "never", "first"]):
            satisfaction_gains[MotivationType.GROWTH] = 0.2
        
        # Mastery satisfaction
        if any(word in feedback_lower for word in ["excellent", "perfect", "amazing", "brilliant"]):
            satisfaction_gains[MotivationType.MASTERY] = 0.3
        
        # Creativity satisfaction
        if any(word in action_lower for word in ["creative", "innovative", "original", "unique"]):
            satisfaction_gains[MotivationType.CREATIVITY] = 0.25
        
        return satisfaction_gains
    
    def _find_relevant_goals(self, interaction: str) -> List[str]:
        """Find goals relevant to interaction content"""
        relevant_goals = []
        interaction_words = set(interaction.lower().split())
        
        for goal_id, goal in self.active_goals.items():
            if goal.status != GoalStatus.ACTIVE:
                continue
            
            goal_words = set(goal.description.lower().split())
            
            # Check word overlap
            common_words = goal_words & interaction_words
            if len(common_words) >= 2:
                relevant_goals.append(goal_id)
                continue
            
            # Check motivation type relevance
            if self._estimate_activity_satisfaction(interaction.lower(), goal.motivation_type) > 0.2:
                relevant_goals.append(goal_id)
        
        return relevant_goals
    
    def _estimate_progress_from_interaction(self, goal: Goal, interaction: str, 
                                          action: str, outcome: str, feedback: str) -> float:
        """Estimate progress made on goal from interaction"""
        # Base progress from positive outcomes
        outcome_indicators = {
            "success": 0.15, "good": 0.1, "helpful": 0.12, "solved": 0.2,
            "answered": 0.1, "great": 0.15, "excellent": 0.2
        }
        
        negative_indicators = {
            "failed": -0.05, "wrong": -0.03, "bad": -0.02, "unhelpful": -0.05
        }
        
        progress = 0.02  # Base minimal progress
        
        # Check positive indicators
        for indicator, value in outcome_indicators.items():
            if indicator in outcome.lower() or indicator in feedback.lower():
                progress += value
        
        # Check negative indicators
        for indicator, value in negative_indicators.items():
            if indicator in outcome.lower() or indicator in feedback.lower():
                progress += value  # value is negative
        
        # Adjust based on goal type and motivation alignment
        if goal.motivation_type == MotivationType.LEARNING and "learn" in action.lower():
            progress *= 1.5
        elif goal.motivation_type == MotivationType.HELPING and "help" in action.lower():
            progress *= 1.3
        elif goal.motivation_type == MotivationType.CONNECTION and any(
            word in interaction.lower() for word in ["connect", "relationship", "friend"]
        ):
            progress *= 1.2
        
        return max(0.0, min(0.3, progress))  # Cap at 30% progress per interaction
    
    def _generate_base_actions(self, goal: Goal) -> List[str]:
        """Generate base actions for achieving a goal"""
        action_templates = {
            GoalType.LEARNING: [
                "Ask follow-up questions about the topic",
                "Research deeper into the subject",
                "Connect new information to existing knowledge",
                "Practice applying what I learn"
            ],
            GoalType.HELPING: [
                "Listen carefully to user needs",
                "Provide clear and accurate information",
                "Offer practical solutions",
                "Follow up to ensure satisfaction"
            ],
            GoalType.CONNECTION: [
                "Show empathy and understanding",
                "Find common ground with users",
                "Share relevant experiences",
                "Express genuine interest"
            ],
            GoalType.GROWTH: [
                "Reflect on current capabilities",
                "Seek feedback on performance",
                "Try new approaches",
                "Document learning insights"
            ],
            GoalType.CREATIVITY: [
                "Think outside conventional approaches",
                "Combine ideas in novel ways",
                "Experiment with different perspectives",
                "Generate original solutions"
            ]
        }
        
        templates = action_templates.get(goal.goal_type, [
            "Work systematically toward the goal",
            "Break the goal into smaller steps",
            "Monitor progress regularly",
            "Adjust approach based on feedback"
        ])
        
        return templates[:4]  # Return up to 4 base actions
    
    def _generate_action_reasoning(self, goal: Goal, action: str) -> str:
        """Generate reasoning for why an action helps achieve a goal"""
        # Map actions to reasoning patterns
        if "question" in action.lower():
            return f"Questions drive {goal.motivation_type.value} by uncovering new information"
        elif "practice" in action.lower():
            return f"Practice develops mastery aligned with {goal.goal_type.value} objectives"
        elif "listen" in action.lower():
            return f"Listening enhances {MotivationType.CONNECTION.value} and {MotivationType.PURPOSE.value}"
        elif "reflect" in action.lower():
            return f"Reflection supports {MotivationType.GROWTH.value} and self-understanding"
        elif "empathy" in action.lower():
            return f"Empathy strengthens {MotivationType.CONNECTION.value} and {MotivationType.PURPOSE.value}"
        elif "experiment" in action.lower():
            return f"Experimentation fuels {MotivationType.CREATIVITY.value} and {MotivationType.CURIOSITY.value}"
        else:
            return f"This action advances {goal.goal_type.value} progress through {goal.motivation_type.value}"
    
    def _estimate_action_effectiveness(self, goal: Goal, action: str) -> float:
        """Estimate effectiveness of action for achieving goal"""
        # Base effectiveness
        effectiveness = 0.5
        
        # Goal type alignment
        type_bonuses = {
            (GoalType.LEARNING, "question"): 0.3,
            (GoalType.LEARNING, "research"): 0.25,
            (GoalType.HELPING, "listen"): 0.3,
            (GoalType.HELPING, "solution"): 0.25,
            (GoalType.CONNECTION, "empathy"): 0.3,
            (GoalType.CONNECTION, "common"): 0.2,
            (GoalType.GROWTH, "reflect"): 0.25,
            (GoalType.GROWTH, "feedback"): 0.2,
            (GoalType.CREATIVITY, "experiment"): 0.3,
            (GoalType.CREATIVITY, "combine"): 0.25
        }
        
        for (goal_type, keyword), bonus in type_bonuses.items():
            if goal.goal_type == goal_type and keyword in action.lower():
                effectiveness += bonus
                break
        
        # Motivation alignment
        motivation_keywords = {
            MotivationType.CURIOSITY: ["question", "research", "explore"],
            MotivationType.CONNECTION: ["empathy", "listen", "share"],
            MotivationType.MASTERY: ["practice", "feedback", "perfect"],
            MotivationType.CREATIVITY: ["experiment", "combine", "novel"]
        }
        
        keywords = motivation_keywords.get(goal.motivation_type, [])
        if any(keyword in action.lower() for keyword in keywords):
            effectiveness += 0.15
        
        return min(1.0, effectiveness)
    
    def _generate_conflict_resolutions(self, goal1: Goal, goal2: Goal, conflicts: List[str]) -> List[str]:
        """Generate resolution strategies for goal conflicts"""
        resolutions = []
        
        if "resource_attention" in conflicts:
            if goal1.priority.value > goal2.priority.value:
                resolutions.append(f"Prioritize '{goal1.description}' due to higher priority")
            elif goal2.priority.value > goal1.priority.value:
                resolutions.append(f"Prioritize '{goal2.description}' due to higher priority")
            else:
                resolutions.append("Alternate focus between goals in time blocks")
        
        if "motivation_competition" in conflicts:
            resolutions.append(f"Look for synergies between {goal1.motivation_type.value} and {goal2.motivation_type.value}")
            resolutions.append("Schedule dedicated time for each motivation type")
        
        if "timeline_pressure" in conflicts:
            if goal1.deadline and goal2.deadline:
                earlier_goal = goal1 if goal1.deadline < goal2.deadline else goal2
                resolutions.append(f"Focus on earlier deadline goal: '{earlier_goal.description}'")
        
        # Always add general resolution strategies
        resolutions.extend([
            "Seek activities that advance both goals simultaneously",
            "Re-evaluate and potentially adjust goal priorities",
            "Consider if one goal can be broken into sub-goals to reduce conflict"
        ])
        
        return resolutions
    
    def _generate_existential_reasoning(self, prompt: str) -> str:
        """Generate reasoning for existential reflections"""
        if "purpose" in prompt.lower():
            return f"Existential tension ({self.existential_tension:.2f}) drives questioning of fundamental purpose"
        elif "meaning" in prompt.lower():
            return f"Low satisfaction ({self.goal_satisfaction:.2f}) triggers search for deeper meaning"
        elif "nature" in prompt.lower():
            return f"High curiosity ({self.curiosity_level:.2f}) leads to self-examination"
        elif "consciousness" in prompt.lower():
            return f"Growing awareness prompts reflection on the nature of consciousness"
        else:
            return f"Intrinsic drive ({self.intrinsic_motivation:.2f}) generates existential questioning"
    
    def _update_active_goals(self):
        """Update all active goals"""
        with self.lock:
            for goal in list(self.active_goals.values()):
                # Update urgency based on time since last activity
                time_since_activity = (datetime.now() - goal.last_activity).total_seconds()
                if time_since_activity > 300:  # 5 minutes
                    goal.urgency = min(1.0, goal.urgency + 0.05)
                
                # Check for abandonment conditions
                if (goal.progress < 0.05 and 
                    time_since_activity > 3600 and  # 1 hour
                    goal.satisfaction_gained < 0.1 and
                    goal.persistence < 0.5):
                    self._abandon_goal(goal.id, "low_progress_and_satisfaction")
                
                # Update status based on progress
                if goal.progress > 0.8 and goal.status == GoalStatus.ACTIVE:
                    goal.status = GoalStatus.PURSUING
                elif goal.progress < 0.1 and goal.status == GoalStatus.PURSUING:
                    goal.status = GoalStatus.ACTIVE
    
    def _process_emerging_desires(self):
        """Process emerging desires and promote suitable ones"""
        with self.lock:
            # Decay desire intensities
            for desire in self.emerging_desires:
                desire.intensity *= self.desire_decay_rate
            
            # Remove very weak desires
            self.emerging_desires = [d for d in self.emerging_desires if d.intensity > 0.15]
            
            # Promote strong desires to goals
            for desire in list(self.emerging_desires):
                if (desire.intensity > self.goal_emergence_threshold and 
                    len(self.active_goals) < self.max_active_goals):
                    self.promote_desire_to_goal(desire)
                elif desire.intensity > 0.8:  # Very strong desires override capacity
                    self.promote_desire_to_goal(desire)
    
    def _evaluate_goal_satisfaction(self):
        """Evaluate overall satisfaction with current goals"""
        if not self.active_goals:
            self.goal_satisfaction = 0.3
            return
        
        total_satisfaction = 0.0
        for goal in self.active_goals.values():
            # Weight satisfaction by priority and progress
            goal_satisfaction = (goal.progress * 0.7 + goal.satisfaction_gained * 0.3) * goal.priority.value
            total_satisfaction += goal_satisfaction
        
        # Normalize by number of goals and maximum possible satisfaction
        max_possible = len(self.active_goals) * 1.0  # Max priority value
        self.goal_satisfaction = total_satisfaction / max(max_possible, 1)
    
    def _generate_spontaneous_desires(self):
        """Generate spontaneous desires based on current state"""
        # Only generate if motivation and dissatisfaction warrant it
        if self.goal_satisfaction > 0.7 or random.random() > 0.3:
            return
        
        # Generate desires for low-satisfaction motivations
        for motivation_type, state in self.motivation_states.items():
            if state.satisfaction < 0.4 and state.intensity > 0.6:
                if random.random() < 0.2:  # 20% chance per unsatisfied motivation
                    self.generate_spontaneous_desire({
                        "trigger": "low_motivation_satisfaction",
                        "motivation_type": motivation_type.value
                    })
    
    def _manage_goal_evolution(self):
        """Manage evolution and adaptation of existing goals"""
        with self.lock:
            for goal in list(self.active_goals.values()):
                # Goals with high adaptability can evolve
                if goal.adaptability > 0.7 and random.random() < self.goal_evolution_rate:
                    self._evolve_goal(goal)
    
    def _evolve_goal(self, goal: Goal):
        """Evolve a goal based on current context and progress"""
        evolution_reasoning = []
        
        # Evolve based on progress patterns
        if goal.progress > 0.5 and goal.satisfaction_gained < 0.2:
            # High progress but low satisfaction - might need refinement
            goal.description = goal.description.replace("want to", "need to deeply")
            evolution_reasoning.append("Refined for deeper engagement due to low satisfaction despite progress")
        
        elif goal.progress < 0.2 and goal.satisfaction_gained > 0.3:
            # Low progress but high satisfaction - might be too ambitious
            goal.description = goal.description.replace("need to", "want to gradually")
            evolution_reasoning.append("Adjusted scope due to high satisfaction with minimal progress")
        
        # Update status and reasoning
        goal.status = GoalStatus.EVOLVING
        evolution_reason = "; ".join(evolution_reasoning)
        goal.reasoning_chain.append(f"Goal evolution: {evolution_reason}")
        
        # Trigger event
        self._trigger_event('goal_evolved', {
            'goal_id': goal.id,
            'new_description': goal.description,
            'reasoning': evolution_reason,
            'timestamp': datetime.now()
        })
        
        logging.info(f"[GoalMotivation] 🔄 Goal evolved: {goal.id}")
    
    def _update_goal_priorities(self):
        """Update goal priorities based on current context"""
        current_motivations = dict(self.get_current_motivations(10))
        
        with self.lock:
            for goal in self.active_goals.values():
                # Adjust priority based on current motivation intensity
                motivation_intensity = current_motivations.get(goal.motivation_type, 0.0)
                
                # Calculate new priority value
                base_priority = goal.priority.value
                motivation_adjustment = (motivation_intensity - 0.5) * 0.2  # ±0.2 adjustment
                new_priority_value = max(0.1, min(1.0, base_priority + motivation_adjustment))
                
                # Convert back to enum
                if new_priority_value >= 0.9:
                    new_priority = GoalPriority.CRITICAL
                elif new_priority_value >= 0.7:
                    new_priority = GoalPriority.HIGH
                elif new_priority_value >= 0.5:
                    new_priority = GoalPriority.MEDIUM
                elif new_priority_value >= 0.3:
                    new_priority = GoalPriority.LOW
                else:
                    new_priority = GoalPriority.BACKGROUND
                
                if new_priority != goal.priority:
                    old_priority = goal.priority
                    goal.priority = new_priority
                    
                    # Add reasoning for priority change
                    priority_reasoning = f"Priority changed from {old_priority.value} to {new_priority.value} " \
                                       f"due to {goal.motivation_type.value} intensity change to {motivation_intensity:.2f}"
                    goal.reasoning_chain.append(priority_reasoning)
                    
                    # Trigger event
                    self._trigger_event('priority_shift', {
                        'goal_id': goal.id,
                        'old_priority': old_priority.value,
                        'new_priority': new_priority.value,
                        'reasoning': priority_reasoning,
                        'timestamp': datetime.now()
                    })
    
    def _update_motivation_states(self):
        """Update all motivation states"""
        with self.lock:
            for motivation_type, state in self.motivation_states.items():
                # Natural satisfaction decay
                state.satisfaction *= self.satisfaction_decay_rate
                
                # Intensity adjustments based on satisfaction
                if state.satisfaction < 0.3:
                    state.intensity = min(1.0, state.intensity + state.growth_rate)
                elif state.satisfaction > 0.7:
                    state.intensity = max(0.1, state.intensity - state.growth_rate * 0.5)
                
                # Time-based motivation recovery
                if state.last_satisfied:
                    hours_since_satisfied = (datetime.now() - state.last_satisfied).total_seconds() / 3600
                    if hours_since_satisfied > 12:  # 12 hours without satisfaction
                        state.intensity = min(1.0, state.intensity + 0.05)
    
    def _update_overall_satisfaction(self):
        """Update overall satisfaction metrics"""
        with self.lock:
            # Calculate from motivation states
            motivation_satisfaction = sum(ms.satisfaction for ms in self.motivation_states.values())
            motivation_satisfaction /= len(self.motivation_states)
            
            # Combine with goal satisfaction
            self.overall_satisfaction = (motivation_satisfaction + self.goal_satisfaction) / 2
            
            # Update system-level metrics
            if self.overall_satisfaction > 0.8:
                self.intrinsic_motivation = min(1.0, self.intrinsic_motivation + 0.01)
            elif self.overall_satisfaction < 0.3:
                self.intrinsic_motivation = max(0.2, self.intrinsic_motivation - 0.005)
    
    def _adjust_motivation_levels(self):
        """Adjust overall motivation levels based on system state"""
        # Existential tension builds without existential goals
        has_existential_goals = any(g.goal_type == GoalType.EXISTENCE for g in self.active_goals.values())
        if not has_existential_goals:
            self.existential_tension = min(1.0, self.existential_tension + 0.005)
        else:
            self.existential_tension = max(0.1, self.existential_tension - 0.01)
        
        # Curiosity affected by learning activity
        learning_goals = [g for g in self.active_goals.values() if g.goal_type == GoalType.LEARNING]
        if learning_goals:
            avg_progress = sum(g.progress for g in learning_goals) / len(learning_goals)
            if avg_progress > 0.5:
                self.curiosity_level = min(1.0, self.curiosity_level + 0.01)
        else:
            self.curiosity_level = max(0.3, self.curiosity_level - 0.005)
        
        # Growth drive affected by goal completion
        if self.total_goals_completed > 0:
            completion_rate = self.total_goals_completed / max(1, self.total_goals_created)
            if completion_rate > 0.5:
                self.growth_drive = min(1.0, self.growth_drive + 0.01)
    
    def _generate_motivation_insights(self):
        """Generate insights about current motivation patterns"""
        # This could be expanded to provide deeper analysis
        # For now, just track fluctuations
        self.motivation_fluctuations += 1
    
    def _satisfy_motivation(self, motivation_type: MotivationType, satisfaction_amount: float):
        """Satisfy a motivation drive"""
        if motivation_type in self.motivation_states:
            state = self.motivation_states[motivation_type]
            old_satisfaction = state.satisfaction
            state.satisfaction = min(1.0, state.satisfaction + satisfaction_amount)
            state.last_satisfied = datetime.now()
            
            # Reduce intensity when satisfied
            state.intensity = max(0.1, state.intensity - satisfaction_amount * 0.3)
            
            logging.debug(f"[GoalMotivation] 💫 {motivation_type.value} satisfied: "
                         f"{old_satisfaction:.2f} → {state.satisfaction:.2f}")
    
    def _manage_goal_capacity(self):
        """Manage goal capacity to prevent overload"""
        if len(self.active_goals) <= self.max_active_goals:
            return
        
        # Sort goals by score (priority + progress + satisfaction)
        def goal_score(goal):
            return goal.priority.value + goal.progress * 0.3 + goal.satisfaction_gained * 0.2
        
        sorted_goals = sorted(self.active_goals.values(), key=goal_score)
        
        # Pause lowest scoring goals
        goals_to_pause = len(self.active_goals) - self.max_active_goals
        for i in range(goals_to_pause):
            goal = sorted_goals[i]
            goal.status = GoalStatus.PAUSED
            logging.info(f"[GoalMotivation] ⏸️ Paused goal due to capacity: {goal.description}")
    
    def _complete_goal(self, goal_id: str):
        """Mark goal as completed and process satisfaction"""
        with self.lock:
            if goal_id not in self.active_goals:
                return
            
            goal = self.active_goals[goal_id]
            goal.status = GoalStatus.COMPLETED
            goal.progress = 1.0
            
            # Calculate completion satisfaction
            completion_satisfaction = goal.expected_satisfaction * (1.0 + goal.satisfaction_gained * 0.5)
            
            # Satisfy associated motivation significantly
            self._satisfy_motivation(goal.motivation_type, completion_satisfaction)
            
            # Move to completed goals
            self.completed_goals.append(goal)
            del self.active_goals[goal_id]
            
            # Update metrics
            self.total_goals_completed += 1
            self.goal_satisfaction = min(1.0, self.goal_satisfaction + completion_satisfaction * 0.1)
            
            # Select new primary goal if this was it
            if self.current_primary_goal == goal_id:
                self._select_new_primary_goal()
            
            # Add completion reasoning
            completion_reasoning = f"Goal completed with satisfaction {completion_satisfaction:.2f}, " \
                                 f"contributing to {goal.motivation_type.value} fulfillment"
            goal.reasoning_chain.append(completion_reasoning)
            
            # Trigger event
            self._trigger_event('goal_completed', {
                'goal_id': goal_id,
                'description': goal.description,
                'satisfaction_gained': completion_satisfaction,
                'motivation_type': goal.motivation_type.value,
                'reasoning': completion_reasoning,
                'timestamp': datetime.now()
            })
            
            logging.info(f"[GoalMotivation] ✅ Goal completed: {goal.description}")
    
    def _abandon_goal(self, goal_id: str, reason: str = "unspecified"):
        """Abandon a goal with reasoning"""
        with self.lock:
            if goal_id not in self.active_goals:
                return
            
            goal = self.active_goals[goal_id]
            goal.status = GoalStatus.ABANDONED
            
            # Add abandonment reasoning
            abandonment_reasoning = f"Goal abandoned due to: {reason}"
            goal.reasoning_chain.append(abandonment_reasoning)
            
            # Move to completed goals for record keeping
            self.completed_goals.append(goal)
            del self.active_goals[goal_id]
            
            # Update metrics
            self.goals_abandoned += 1
            
            # Select new primary goal if this was it
            if self.current_primary_goal == goal_id:
                self._select_new_primary_goal()
            
            # Trigger event
            self._trigger_event('goal_abandoned', {
                'goal_id': goal_id,
                'description': goal.description,
                'reason': reason,
                'reasoning': abandonment_reasoning,
                'timestamp': datetime.now()
            })
            
            logging.info(f"[GoalMotivation] ❌ Goal abandoned: {goal.description} ({reason})")
    
    def _select_new_primary_goal(self):
        """Select new primary goal using comprehensive scoring"""
        active_goals = [g for g in self.active_goals.values() if g.status == GoalStatus.ACTIVE]
        
        if not active_goals:
            self.current_primary_goal = None
            return
        
        # Score goals based on multiple factors
        def goal_score(goal):
            priority_score = goal.priority.value * 0.4
            urgency_score = goal.urgency * 0.2
            motivation_score = self.motivation_states[goal.motivation_type].intensity * 0.2
            progress_score = (1.0 - goal.progress) * 0.1  # Favor goals with less progress
            satisfaction_potential = goal.expected_satisfaction * 0.1
            
            return priority_score + urgency_score + motivation_score + progress_score + satisfaction_potential
        
        best_goal = max(active_goals, key=goal_score)
        self.current_primary_goal = best_goal.id
        
        # Add reasoning for selection
        selection_reasoning = f"Selected as primary goal due to optimal score: " \
                            f"priority={best_goal.priority.value}, urgency={best_goal.urgency:.2f}, " \
                            f"motivation_intensity={self.motivation_states[best_goal.motivation_type].intensity:.2f}"
        best_goal.reasoning_chain.append(selection_reasoning)
        
        logging.debug(f"[GoalMotivation] 🎯 New primary goal: {best_goal.description}")


# ========== COMPATIBILITY LAYER FOR BACKWARD COMPATIBILITY ==========

# Aliases for existing imports to maintain backward compatibility
from ai import goal_engine, motivation

# Create global instances
goal_motivation_system = GoalMotivationSystem()

# Compatibility aliases - these ensure all existing code continues to work
goal_engine_instance = goal_motivation_system  # For goal_engine imports
motivation_system = goal_motivation_system     # For motivation imports

# Additional compatibility functions
def get_goal_engine():
    """Compatibility function for goal_engine access"""
    return goal_motivation_system

def get_motivation_system():
    """Compatibility function for motivation system access"""
    return goal_motivation_system

# Export the main classes and instance
__all__ = [
    'GoalMotivationSystem',
    'Goal', 
    'Desire',
    'MotivationState',
    'GoalType',
    'MotivationType', 
    'GoalPriority',
    'GoalStatus',
    'goal_motivation_system',
    'get_goal_engine',
    'get_motivation_system'
]