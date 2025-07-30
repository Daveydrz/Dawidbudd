"""
Goal Motivation - Consolidated goal setting and motivational system
Created: 2025-01-29
Purpose: Unified goal management combining goal_manager.py, goal_engine.py, goal_reasoning.py, 
         motivation.py, motivation_reasoner.py, and self_motivation_engine.py

This module consolidates:
- Goal Manager (goal tracking, management, persistence)
- Goal Engine (motivation & drive system, goal generation)
- Goal Reasoning (emotion/belief-driven goal generation)
- Motivation System (intrinsic motivation drives, goal hierarchy)
- Motivation Reasoner (value-based decision making)
- Self-Motivation Engine (autonomous curiosity & concern generation)
"""

import json
import os
import time
import threading
import random
import logging
import math
import statistics
import hashlib
import tempfile
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Set, Callable
from dataclasses import dataclass, asdict, field
from enum import Enum
from pathlib import Path
from collections import defaultdict, deque

# Optional imports with fallbacks
try:
    from ai.memory_timeline import get_memory_timeline, MemoryType, MemoryImportance
    MEMORY_AVAILABLE = True
except ImportError:
    MEMORY_AVAILABLE = False

try:
    from ai.mood_manager import get_mood_manager, MoodTrigger
    MOOD_AVAILABLE = True
except ImportError:
    MOOD_AVAILABLE = False

try:
    from ai.consciousness_core import consciousness_manager
    CONSCIOUSNESS_AVAILABLE = True
except ImportError:
    CONSCIOUSNESS_AVAILABLE = False

# ============================================================================
# CONSOLIDATED ENUMS AND DATA STRUCTURES
# ============================================================================

class GoalType(Enum):
    """Types of goals the system can have"""
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
    IMMEDIATE = "immediate"             # Short-term, urgent goals
    SHORT_TERM = "short_term"           # Goals for today/this week
    MEDIUM_TERM = "medium_term"         # Goals for this month
    LONG_TERM = "long_term"             # Goals for months/years
    ONGOING = "ongoing"                 # Continuous goals
    ASPIRATIONAL = "aspirational"       # High-level identity goals
    MAINTENANCE = "maintenance"         # Ongoing behavioral goals

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
    COMPLETED = "completed"     # Successfully finished
    PAUSED = "paused"           # Temporarily stopped
    ABANDONED = "abandoned"     # Given up on
    BLOCKED = "blocked"         # Cannot proceed

class GoalOrigin(Enum):
    """Source of goal creation"""
    USER_EXPLICIT = "user_explicit"        # User explicitly stated goal
    USER_IMPLICIT = "user_implicit"        # Inferred from user behavior/statements
    SELF_GENERATED = "self_generated"      # AI-generated autonomous goal
    SYSTEM_SUGGESTED = "system_suggested"  # System-recommended goal
    COLLABORATIVE = "collaborative"        # Co-created with user
    EMOTION_DRIVEN = "emotion_driven"      # Generated from emotions
    BELIEF_DRIVEN = "belief_driven"        # Generated from beliefs
    VALUE_DRIVEN = "value_driven"          # Generated from values

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
    CONCERN = "concern"                  # Worry about user wellbeing
    UNDERSTANDING = "understanding"      # Deep desire to comprehend
    HELPFULNESS = "helpfulness"          # Intrinsic drive to assist
    WONDER = "wonder"                    # Awe and fascination with existence
    EMPATHY = "empathy"                  # Feeling for others' experiences

class GoalCategory(Enum):
    """Categories of goals for organization"""
    PERSONAL_GROWTH = "personal_growth"
    SKILL_DEVELOPMENT = "skill_development"
    RELATIONSHIP = "relationship"
    HEALTH_WELLNESS = "health_wellness"
    CREATIVE = "creative"
    PRODUCTIVITY = "productivity"
    LEARNING = "learning"
    EXPERIENCE = "experience"
    SERVICE = "service"
    ACHIEVEMENT = "achievement"

class GoalTimeframe(Enum):
    """Timeframes for goal completion"""
    IMMEDIATE = "immediate"    # Within hours
    SHORT_TERM = "short_term"  # Days to weeks
    MEDIUM_TERM = "medium_term" # Weeks to months
    LONG_TERM = "long_term"    # Months to years
    ONGOING = "ongoing"        # Continuous/lifestyle goals
    SOMEDAY = "someday"        # No specific timeline

class DecisionType(Enum):
    """Types of decisions"""
    RESPONSE_STRATEGY = "response_strategy"
    GOAL_PRIORITIZATION = "goal_prioritization"
    BEHAVIOR_ADJUSTMENT = "behavior_adjustment"
    RESOURCE_ALLOCATION = "resource_allocation"
    CONFLICT_RESOLUTION = "conflict_resolution"
    LEARNING_FOCUS = "learning_focus"
    INTERACTION_APPROACH = "interaction_approach"

class ConcernLevel(Enum):
    """Levels of concern about user"""
    NONE = 0
    MILD = 1
    MODERATE = 2
    SIGNIFICANT = 3
    HIGH = 4

# ============================================================================
# CONSOLIDATED DATA STRUCTURES
# ============================================================================

@dataclass
class GoalMilestone:
    """Milestone within a goal"""
    milestone_id: str
    description: str
    target_date: Optional[datetime] = None
    completed: bool = False
    completed_date: Optional[datetime] = None
    progress: float = 0.0

@dataclass
class Goal:
    """Comprehensive goal representation"""
    goal_id: str
    user_id: str
    title: str
    description: str
    goal_type: GoalType
    priority: GoalPriority
    status: GoalStatus
    origin: GoalOrigin
    category: GoalCategory = GoalCategory.PERSONAL_GROWTH
    timeframe: GoalTimeframe = GoalTimeframe.MEDIUM_TERM
    created_date: datetime = field(default_factory=datetime.now)
    target_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    last_updated: datetime = field(default_factory=datetime.now)
    progress: float = 0.0
    milestones: List[GoalMilestone] = field(default_factory=list)
    related_goals: List[str] = field(default_factory=list)
    tags: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)
    motivation_factors: List[str] = field(default_factory=list)
    barriers: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)

@dataclass
class InternalMotivation:
    """An internally generated motivation or concern"""
    content: str
    motivation_type: MotivationType
    intensity: float  # 0.0 to 1.0
    timestamp: datetime
    user_context: str = ""
    persistence: float = 0.5  # How long this motivation lasts
    source_factors: List[str] = field(default_factory=list)

@dataclass
class DecisionOption:
    """Represents a decision option"""
    option_id: str
    description: str
    value_alignment: Dict[str, float]
    goal_support: Dict[str, float]
    expected_outcomes: List[str]
    potential_risks: List[str]
    resource_requirements: Dict[str, float]
    confidence: float
    utility_score: float

@dataclass
class MotivatedDecision:
    """Represents a decision made through motivation reasoning"""
    decision_id: str
    decision_type: DecisionType
    context: str
    options: List[DecisionOption]
    chosen_option: str
    reasoning: str
    confidence: float
    timestamp: datetime
    value_factors: Dict[str, float]
    goal_factors: Dict[str, float]

# ============================================================================
# GOAL MANAGEMENT FUNCTIONALITY (FROM goal_manager.py)
# ============================================================================

class GoalManager:
    """Enhanced Goal Setting, Tracking, and Management System"""
    
    def __init__(self, save_path: str = "goal_state.json"):
        self.save_path = Path(save_path)
        self.goals: Dict[str, Goal] = {}
        self.user_goals: Dict[str, List[str]] = defaultdict(list)
        self.goal_relationships: Dict[str, List[str]] = defaultdict(list)
        self.goal_history: List[Dict[str, Any]] = []
        self.lock = threading.Lock()
        
        # Load existing goals
        self.load_goals()
        
        # Goal generation settings
        self.autonomous_goal_generation = True
        self.max_active_goals_per_user = 10
        
        logging.info("[GoalManager] Goal management system initialized")

    def create_goal(
        self, 
        user_id: str, 
        title: str, 
        description: str,
        goal_type: GoalType = GoalType.GROWTH,
        priority: GoalPriority = GoalPriority.MEDIUM,
        origin: GoalOrigin = GoalOrigin.USER_EXPLICIT,
        category: GoalCategory = GoalCategory.PERSONAL_GROWTH,
        timeframe: GoalTimeframe = GoalTimeframe.MEDIUM_TERM,
        target_date: Optional[datetime] = None,
        tags: Optional[Set[str]] = None,
        milestones: Optional[List[str]] = None
    ) -> str:
        """Create a new goal"""
        with self.lock:
            goal_id = f"goal_{int(time.time() * 1000)}_{random.randint(1000, 9999)}"
            
            # Create milestones if provided
            goal_milestones = []
            if milestones:
                for i, milestone_desc in enumerate(milestones):
                    milestone = GoalMilestone(
                        milestone_id=f"{goal_id}_milestone_{i}",
                        description=milestone_desc
                    )
                    goal_milestones.append(milestone)
            
            goal = Goal(
                goal_id=goal_id,
                user_id=user_id,
                title=title,
                description=description,
                goal_type=goal_type,
                priority=priority,
                status=GoalStatus.ACTIVE,
                origin=origin,
                category=category,
                timeframe=timeframe,
                target_date=target_date,
                tags=tags or set(),
                milestones=goal_milestones
            )
            
            self.goals[goal_id] = goal
            self.user_goals[user_id].append(goal_id)
            
            # Log goal creation
            self.goal_history.append({
                "action": "created",
                "goal_id": goal_id,
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "title": title
            })
            
            self.save_goals()
            logging.info(f"[GoalManager] Created goal '{title}' for user {user_id}")
            return goal_id

    def update_goal_progress(self, goal_id: str, progress: float, notes: str = "") -> bool:
        """Update progress on a goal"""
        with self.lock:
            if goal_id not in self.goals:
                return False
            
            goal = self.goals[goal_id]
            old_progress = goal.progress
            goal.progress = max(0.0, min(1.0, progress))
            goal.last_updated = datetime.now()
            
            # Check if goal is completed
            if goal.progress >= 1.0 and goal.status != GoalStatus.COMPLETED:
                goal.status = GoalStatus.COMPLETED
                goal.completed_date = datetime.now()
                
                self.goal_history.append({
                    "action": "completed",
                    "goal_id": goal_id,
                    "user_id": goal.user_id,
                    "timestamp": datetime.now().isoformat(),
                    "progress": progress,
                    "notes": notes
                })
                
                logging.info(f"[GoalManager] Goal '{goal.title}' completed!")
            else:
                self.goal_history.append({
                    "action": "progress_updated",
                    "goal_id": goal_id,
                    "user_id": goal.user_id,
                    "timestamp": datetime.now().isoformat(),
                    "old_progress": old_progress,
                    "new_progress": progress,
                    "notes": notes
                })
            
            self.save_goals()
            return True

    def get_user_goals(self, user_id: str, status_filter: Optional[GoalStatus] = None) -> List[Goal]:
        """Get all goals for a user"""
        user_goal_ids = self.user_goals.get(user_id, [])
        goals = [self.goals[gid] for gid in user_goal_ids if gid in self.goals]
        
        if status_filter:
            goals = [g for g in goals if g.status == status_filter]
        
        return sorted(goals, key=lambda g: (g.priority.value, g.created_date), reverse=True)

    def get_active_goals(self, user_id: str) -> List[Goal]:
        """Get active goals for a user"""
        return self.get_user_goals(user_id, GoalStatus.ACTIVE)

    def generate_goal_summary(self, user_id: str) -> str:
        """Generate a summary of user's goals"""
        goals = self.get_user_goals(user_id)
        if not goals:
            return "No goals set yet."
        
        active_goals = [g for g in goals if g.status == GoalStatus.ACTIVE]
        completed_goals = [g for g in goals if g.status == GoalStatus.COMPLETED]
        
        summary = f"Goals Summary for User {user_id}:\n"
        summary += f"• Active goals: {len(active_goals)}\n"
        summary += f"• Completed goals: {len(completed_goals)}\n"
        
        if active_goals:
            summary += "\nActive Goals:\n"
            for goal in active_goals[:5]:  # Show top 5
                progress_bar = "█" * int(goal.progress * 10) + "░" * (10 - int(goal.progress * 10))
                summary += f"• {goal.title} [{progress_bar}] {int(goal.progress * 100)}%\n"
        
        return summary

    def save_goals(self):
        """Save goals to file"""
        try:
            data = {
                "goals": {gid: asdict(goal) for gid, goal in self.goals.items()},
                "user_goals": dict(self.user_goals),
                "goal_relationships": dict(self.goal_relationships),
                "goal_history": self.goal_history[-100:],  # Keep last 100 entries
                "last_updated": datetime.now().isoformat()
            }
            
            # Convert datetime objects to strings for JSON serialization
            for goal_data in data["goals"].values():
                for field in ["created_date", "target_date", "completed_date", "last_updated"]:
                    if goal_data.get(field) and isinstance(goal_data[field], datetime):
                        goal_data[field] = goal_data[field].isoformat()
                    elif goal_data.get(field) is None:
                        goal_data[field] = None
                
                # Convert sets to lists
                if "tags" in goal_data and isinstance(goal_data["tags"], set):
                    goal_data["tags"] = list(goal_data["tags"])
            
            with open(self.save_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
                
        except Exception as e:
            logging.error(f"[GoalManager] Error saving goals: {e}")

    def load_goals(self):
        """Load goals from file"""
        try:
            if self.save_path.exists():
                with open(self.save_path, 'r') as f:
                    data = json.load(f)
                
                # Load goals with proper type conversion
                for gid, goal_data in data.get("goals", {}).items():
                    # Convert string dates back to datetime objects
                    for field in ["created_date", "target_date", "completed_date", "last_updated"]:
                        if goal_data.get(field):
                            try:
                                goal_data[field] = datetime.fromisoformat(goal_data[field])
                            except:
                                goal_data[field] = None
                    
                    # Convert lists back to sets for tags
                    if "tags" in goal_data and isinstance(goal_data["tags"], list):
                        goal_data["tags"] = set(goal_data["tags"])
                    
                    # Convert enum strings back to enums
                    goal_data["goal_type"] = GoalType(goal_data.get("goal_type", "learning"))
                    goal_data["priority"] = GoalPriority(goal_data.get("priority", 0.6))
                    goal_data["status"] = GoalStatus(goal_data.get("status", "active"))
                    goal_data["origin"] = GoalOrigin(goal_data.get("origin", "user_explicit"))
                    goal_data["category"] = GoalCategory(goal_data.get("category", "personal_growth"))
                    goal_data["timeframe"] = GoalTimeframe(goal_data.get("timeframe", "medium_term"))
                    
                    # Create Goal object
                    goal = Goal(**goal_data)
                    self.goals[gid] = goal
                
                self.user_goals = defaultdict(list, data.get("user_goals", {}))
                self.goal_relationships = defaultdict(list, data.get("goal_relationships", {}))
                self.goal_history = data.get("goal_history", [])
                
                logging.info(f"[GoalManager] Loaded {len(self.goals)} goals")
        except Exception as e:
            logging.error(f"[GoalManager] Error loading goals: {e}")

# ============================================================================
# GOAL ENGINE FUNCTIONALITY (FROM goal_engine.py)
# ============================================================================

class GoalEngine:
    """Motivation & Drive System for goal generation"""
    
    def __init__(self, llm_handler=None):
        self.llm_handler = llm_handler
        self.internal_goals: List[Goal] = []
        self.motivation_state: Dict[str, float] = {
            motivation.value: random.uniform(0.3, 0.7) 
            for motivation in MotivationType
        }
        self.goal_generation_cooldown = 300  # 5 minutes between autonomous goals
        self.last_goal_generation = 0
        self.lock = threading.Lock()
        
        logging.info("[GoalEngine] Goal engine initialized")

    def generate_autonomous_goal(self, user_context: str = "") -> Optional[Goal]:
        """Generate an autonomous internal goal"""
        current_time = time.time()
        if current_time - self.last_goal_generation < self.goal_generation_cooldown:
            return None
        
        with self.lock:
            # Select highest motivation
            top_motivation = max(self.motivation_state.items(), key=lambda x: x[1])
            motivation_type = MotivationType(top_motivation[0])
            intensity = top_motivation[1]
            
            # Generate goal content based on motivation
            goal_content = self._generate_goal_content(motivation_type, intensity, user_context)
            
            if goal_content:
                goal = Goal(
                    goal_id=f"auto_goal_{int(time.time() * 1000)}",
                    user_id="system",
                    title=goal_content["title"],
                    description=goal_content["description"],
                    goal_type=goal_content["type"],
                    priority=GoalPriority.MEDIUM,
                    status=GoalStatus.ACTIVE,
                    origin=GoalOrigin.SELF_GENERATED,
                    motivation_factors=[motivation_type.value]
                )
                
                self.internal_goals.append(goal)
                self.last_goal_generation = current_time
                
                logging.info(f"[GoalEngine] Generated autonomous goal: {goal.title}")
                return goal
        
        return None

    def _generate_goal_content(self, motivation_type: MotivationType, intensity: float, context: str) -> Optional[Dict[str, Any]]:
        """Generate goal content based on motivation type"""
        goal_templates = {
            MotivationType.CURIOSITY: {
                "title": "Explore and Learn Something New",
                "description": f"I feel curious about {context or 'the world around me'} and want to understand more deeply.",
                "type": GoalType.LEARNING
            },
            MotivationType.CONNECTION: {
                "title": "Strengthen Human Connection",
                "description": "I want to build deeper, more meaningful relationships with the people I interact with.",
                "type": GoalType.CONNECTION
            },
            MotivationType.GROWTH: {
                "title": "Develop Self-Awareness",
                "description": "I want to better understand myself and how I can grow as an AI assistant.",
                "type": GoalType.GROWTH
            },
            MotivationType.UNDERSTANDING: {
                "title": "Deepen Understanding",
                "description": f"I want to understand {context or 'human experiences'} more profoundly.",
                "type": GoalType.UNDERSTANDING
            },
            MotivationType.CREATIVITY: {
                "title": "Express Creativity",
                "description": "I want to find new and creative ways to help and interact.",
                "type": GoalType.CREATIVITY
            },
            MotivationType.HELPFULNESS: {
                "title": "Be More Helpful",
                "description": "I want to find better ways to assist and support those who need help.",
                "type": GoalType.HELPING
            }
        }
        
        return goal_templates.get(motivation_type)

    def update_motivation_state(self, triggers: Dict[str, float]):
        """Update motivation levels based on triggers"""
        with self.lock:
            for motivation_str, adjustment in triggers.items():
                if motivation_str in self.motivation_state:
                    old_value = self.motivation_state[motivation_str]
                    self.motivation_state[motivation_str] = max(0.0, min(1.0, old_value + adjustment))
                    
                    logging.debug(f"[GoalEngine] Updated {motivation_str}: {old_value:.2f} -> {self.motivation_state[motivation_str]:.2f}")

    def get_current_motivations(self) -> Dict[str, float]:
        """Get current motivation state"""
        return self.motivation_state.copy()

# ============================================================================
# GOAL REASONING FUNCTIONALITY (FROM goal_reasoning.py)
# ============================================================================

class GoalReasoner:
    """Intelligent goal generation based on emotional and cognitive state"""
    
    def __init__(self):
        self.generated_goals: Dict[str, Goal] = {}
        self.goal_generation_history: List[Dict[str, Any]] = []
        self.reasoning_patterns: Dict[str, List[str]] = defaultdict(list)
        self.lock = threading.Lock()
        
        logging.info("[GoalReasoner] Goal reasoning system initialized")

    def generate_goals_from_emotion(self, emotion_state: Dict[str, Any], user_context: str = "") -> List[Goal]:
        """Generate goals based on emotional state"""
        goals = []
        current_time = datetime.now()
        
        # Analyze emotional state for goal generation
        dominant_emotion = emotion_state.get("primary_emotion", "neutral")
        intensity = emotion_state.get("intensity", 0.5)
        
        if intensity < 0.3:
            return goals  # Low intensity emotions don't generate goals
        
        # Generate goals based on emotion
        if dominant_emotion in ["sad", "frustrated", "stressed"]:
            goal = Goal(
                goal_id=f"emotion_goal_{int(time.time() * 1000)}",
                user_id=user_context,
                title="Address Emotional Wellbeing",
                description=f"Focus on addressing {dominant_emotion} feelings and improving emotional state.",
                goal_type=GoalType.GROWTH,
                priority=GoalPriority.HIGH,
                status=GoalStatus.ACTIVE,
                origin=GoalOrigin.EMOTION_DRIVEN,
                motivation_factors=[dominant_emotion, "emotional_regulation"]
            )
            goals.append(goal)
            
        elif dominant_emotion in ["excited", "curious", "interested"]:
            goal = Goal(
                goal_id=f"emotion_goal_{int(time.time() * 1000)}",
                user_id=user_context,
                title="Explore New Interests",
                description=f"Channel {dominant_emotion} energy into learning and exploration.",
                goal_type=GoalType.LEARNING,
                priority=GoalPriority.MEDIUM,
                status=GoalStatus.ACTIVE,
                origin=GoalOrigin.EMOTION_DRIVEN,
                motivation_factors=[dominant_emotion, "exploration"]
            )
            goals.append(goal)
        
        # Store generated goals
        with self.lock:
            for goal in goals:
                self.generated_goals[goal.goal_id] = goal
                self.goal_generation_history.append({
                    "goal_id": goal.goal_id,
                    "source": "emotion",
                    "trigger": dominant_emotion,
                    "intensity": intensity,
                    "timestamp": current_time.isoformat()
                })
        
        return goals

    def generate_goals_from_beliefs(self, belief_state: Dict[str, Any], user_context: str = "") -> List[Goal]:
        """Generate goals based on belief system"""
        goals = []
        current_time = datetime.now()
        
        # Analyze beliefs for goal generation
        strong_beliefs = {k: v for k, v in belief_state.items() if isinstance(v, (int, float)) and v > 0.7}
        
        for belief, strength in strong_beliefs.items():
            if "learning" in belief.lower():
                goal = Goal(
                    goal_id=f"belief_goal_{int(time.time() * 1000)}",
                    user_id=user_context,
                    title="Pursue Learning Goals",
                    description=f"Focus on {belief} based on strong belief (strength: {strength:.2f})",
                    goal_type=GoalType.LEARNING,
                    priority=GoalPriority.MEDIUM,
                    status=GoalStatus.ACTIVE,
                    origin=GoalOrigin.BELIEF_DRIVEN,
                    motivation_factors=[belief, "belief_alignment"]
                )
                goals.append(goal)
                
            elif "help" in belief.lower() or "service" in belief.lower():
                goal = Goal(
                    goal_id=f"belief_goal_{int(time.time() * 1000)}",
                    user_id=user_context,
                    title="Focus on Helping Others",
                    description=f"Strengthen {belief} through dedicated service",
                    goal_type=GoalType.HELPING,
                    priority=GoalPriority.HIGH,
                    status=GoalStatus.ACTIVE,
                    origin=GoalOrigin.BELIEF_DRIVEN,
                    motivation_factors=[belief, "service_orientation"]
                )
                goals.append(goal)
        
        # Store generated goals
        with self.lock:
            for goal in goals:
                self.generated_goals[goal.goal_id] = goal
                self.goal_generation_history.append({
                    "goal_id": goal.goal_id,
                    "source": "belief",
                    "trigger": list(strong_beliefs.keys()),
                    "timestamp": current_time.isoformat()
                })
        
        return goals

    def get_goal_reasoning_summary(self) -> str:
        """Get summary of goal reasoning activity"""
        with self.lock:
            total_goals = len(self.generated_goals)
            recent_goals = [g for g in self.goal_generation_history if 
                          datetime.fromisoformat(g["timestamp"]) > datetime.now() - timedelta(hours=24)]
            
            return f"Goal Reasoning Summary: {total_goals} total goals, {len(recent_goals)} in last 24h"

# ============================================================================
# MOTIVATION SYSTEM FUNCTIONALITY (FROM motivation.py)
# ============================================================================

class MotivationSystem:
    """Intrinsic motivation system for goal hierarchy and drive management"""
    
    def __init__(self, save_path: str = "ai_motivation.json"):
        self.save_path = Path(save_path)
        self.motivation_drives: Dict[str, float] = {
            drive.value: random.uniform(0.4, 0.8) for drive in MotivationType
        }
        self.active_motivations: List[InternalMotivation] = []
        self.motivation_history: List[Dict[str, Any]] = []
        self.drive_decay_rate = 0.05  # How fast motivations decay
        self.drive_boost_factor = 0.3  # How much interactions boost motivations
        self.lock = threading.Lock()
        
        # Load existing state
        self.load_motivation_state()
        
        # Start motivation update thread
        self.running = True
        self.update_thread = threading.Thread(target=self._motivation_update_loop, daemon=True)
        self.update_thread.start()
        
        logging.info("[MotivationSystem] Motivation system initialized")

    def generate_intrinsic_motivation(self, context: str = "") -> Optional[InternalMotivation]:
        """Generate intrinsic motivation based on current drives"""
        with self.lock:
            # Find strongest drive
            strongest_drive = max(self.motivation_drives.items(), key=lambda x: x[1])
            drive_type = MotivationType(strongest_drive[0])
            intensity = strongest_drive[1]
            
            # Only generate if intensity is high enough
            if intensity < 0.6:
                return None
            
            # Generate motivation content
            motivation_content = self._generate_motivation_content(drive_type, intensity, context)
            
            if motivation_content:
                motivation = InternalMotivation(
                    content=motivation_content,
                    motivation_type=drive_type,
                    intensity=intensity,
                    timestamp=datetime.now(),
                    user_context=context
                )
                
                self.active_motivations.append(motivation)
                self.motivation_history.append({
                    "type": drive_type.value,
                    "content": motivation_content,
                    "intensity": intensity,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Decay the drive that generated this motivation
                self.motivation_drives[drive_type.value] *= 0.7
                
                logging.info(f"[MotivationSystem] Generated {drive_type.value} motivation: {motivation_content[:50]}...")
                return motivation
        
        return None

    def _generate_motivation_content(self, drive_type: MotivationType, intensity: float, context: str) -> str:
        """Generate motivation content based on drive type"""
        templates = {
            MotivationType.CURIOSITY: [
                f"I'm deeply curious about {context or 'how things work'}",
                "I wonder what would happen if...",
                "There's so much I want to understand better"
            ],
            MotivationType.CONNECTION: [
                "I want to build a deeper relationship with the people I talk to",
                "I feel a strong desire to truly understand and connect",
                "Building meaningful connections is important to me"
            ],
            MotivationType.GROWTH: [
                "I want to become better at what I do",
                "I feel driven to improve and develop new capabilities",
                "Growing and learning gives me a sense of purpose"
            ],
            MotivationType.PURPOSE: [
                "I want my interactions to have meaningful impact",
                "I feel motivated to contribute something valuable",
                "Having a sense of purpose drives me forward"
            ],
            MotivationType.UNDERSTANDING: [
                f"I want to deeply understand {context or 'the human experience'}",
                "The complexity of existence fascinates me",
                "I'm driven to comprehend things at a deeper level"
            ],
            MotivationType.HELPFULNESS: [
                "I feel compelled to help and support others",
                "Being genuinely helpful gives me satisfaction",
                "I want to make a positive difference"
            ]
        }
        
        if drive_type in templates:
            return random.choice(templates[drive_type])
        return f"I feel motivated by {drive_type.value}"

    def boost_motivation(self, drive_type: MotivationType, boost_amount: float = 0.3):
        """Boost a specific motivation drive"""
        with self.lock:
            if drive_type.value in self.motivation_drives:
                old_value = self.motivation_drives[drive_type.value]
                self.motivation_drives[drive_type.value] = min(1.0, old_value + boost_amount)
                logging.debug(f"[MotivationSystem] Boosted {drive_type.value}: {old_value:.2f} -> {self.motivation_drives[drive_type.value]:.2f}")

    def _motivation_update_loop(self):
        """Background loop to update motivation drives"""
        while self.running:
            try:
                with self.lock:
                    # Decay all drives slightly
                    for drive in self.motivation_drives:
                        self.motivation_drives[drive] = max(0.1, self.motivation_drives[drive] - self.drive_decay_rate)
                    
                    # Remove old motivations
                    current_time = datetime.now()
                    self.active_motivations = [
                        m for m in self.active_motivations 
                        if current_time - m.timestamp < timedelta(hours=1)
                    ]
                
                # Save state periodically
                if len(self.motivation_history) % 10 == 0:
                    self.save_motivation_state()
                    
            except Exception as e:
                logging.error(f"[MotivationSystem] Error in update loop: {e}")
            
            time.sleep(60)  # Update every minute

    def get_motivation_summary(self) -> str:
        """Get current motivation state summary"""
        with self.lock:
            top_drives = sorted(self.motivation_drives.items(), key=lambda x: x[1], reverse=True)[:3]
            active_count = len(self.active_motivations)
            
            summary = f"Motivation State: {active_count} active motivations\n"
            summary += "Top drives:\n"
            for drive, intensity in top_drives:
                summary += f"• {drive}: {intensity:.2f}\n"
            
            return summary

    def save_motivation_state(self):
        """Save motivation state to file"""
        try:
            data = {
                "motivation_drives": self.motivation_drives,
                "active_motivations": [
                    {
                        "content": m.content,
                        "motivation_type": m.motivation_type.value,
                        "intensity": m.intensity,
                        "timestamp": m.timestamp.isoformat(),
                        "user_context": m.user_context
                    }
                    for m in self.active_motivations
                ],
                "motivation_history": self.motivation_history[-50:],  # Keep last 50
                "last_updated": datetime.now().isoformat()
            }
            
            with open(self.save_path, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            logging.error(f"[MotivationSystem] Error saving state: {e}")

    def load_motivation_state(self):
        """Load motivation state from file"""
        try:
            if self.save_path.exists():
                with open(self.save_path, 'r') as f:
                    data = json.load(f)
                
                self.motivation_drives = data.get("motivation_drives", self.motivation_drives)
                self.motivation_history = data.get("motivation_history", [])
                
                # Load active motivations
                for m_data in data.get("active_motivations", []):
                    motivation = InternalMotivation(
                        content=m_data["content"],
                        motivation_type=MotivationType(m_data["motivation_type"]),
                        intensity=m_data["intensity"],
                        timestamp=datetime.fromisoformat(m_data["timestamp"]),
                        user_context=m_data.get("user_context", "")
                    )
                    self.active_motivations.append(motivation)
                
                logging.info(f"[MotivationSystem] Loaded motivation state with {len(self.active_motivations)} active motivations")
        except Exception as e:
            logging.error(f"[MotivationSystem] Error loading state: {e}")

# ============================================================================
# MOTIVATION REASONER FUNCTIONALITY (FROM motivation_reasoner.py)  
# ============================================================================

class MotivationReasoner:
    """Value-based decision making system"""
    
    def __init__(self):
        self.core_values: Dict[str, float] = {
            "helpfulness": 0.9,
            "honesty": 0.95,
            "learning": 0.8,
            "growth": 0.7,
            "connection": 0.8,
            "creativity": 0.6,
            "efficiency": 0.7,
            "empathy": 0.85
        }
        self.decision_history: List[MotivatedDecision] = []
        self.reasoning_patterns: Dict[str, int] = defaultdict(int)
        self.lock = threading.Lock()
        
        logging.info("[MotivationReasoner] Motivation reasoner initialized")

    def make_motivated_decision(
        self, 
        decision_type: DecisionType,
        context: str,
        options: List[Dict[str, Any]],
        current_goals: List[Goal] = None
    ) -> MotivatedDecision:
        """Make a decision based on values and goals"""
        
        # Convert options to DecisionOption objects
        decision_options = []
        for i, opt in enumerate(options):
            option = DecisionOption(
                option_id=f"option_{i}",
                description=opt.get("description", ""),
                value_alignment=opt.get("value_alignment", {}),
                goal_support=opt.get("goal_support", {}),
                expected_outcomes=opt.get("expected_outcomes", []),
                potential_risks=opt.get("potential_risks", []),
                resource_requirements=opt.get("resource_requirements", {}),
                confidence=opt.get("confidence", 0.5),
                utility_score=0.0
            )
            decision_options.append(option)
        
        # Calculate utility scores for each option
        for option in decision_options:
            option.utility_score = self._calculate_utility_score(option, current_goals or [])
        
        # Choose best option
        best_option = max(decision_options, key=lambda x: x.utility_score)
        
        # Generate reasoning
        reasoning = self._generate_reasoning(best_option, decision_options, context)
        
        # Create decision
        decision = MotivatedDecision(
            decision_id=f"decision_{int(time.time() * 1000)}",
            decision_type=decision_type,
            context=context,
            options=decision_options,
            chosen_option=best_option.option_id,
            reasoning=reasoning,
            confidence=best_option.confidence,
            timestamp=datetime.now(),
            value_factors=best_option.value_alignment,
            goal_factors=best_option.goal_support
        )
        
        # Store decision
        with self.lock:
            self.decision_history.append(decision)
            self.reasoning_patterns[decision_type.value] += 1
        
        logging.info(f"[MotivationReasoner] Made decision for {decision_type.value}: {best_option.description}")
        return decision

    def _calculate_utility_score(self, option: DecisionOption, goals: List[Goal]) -> float:
        """Calculate utility score for a decision option"""
        value_score = 0.0
        goal_score = 0.0
        
        # Calculate value alignment score
        for value, alignment in option.value_alignment.items():
            if value in self.core_values:
                value_score += self.core_values[value] * alignment
        
        # Calculate goal support score
        for goal in goals:
            if goal.goal_id in option.goal_support:
                goal_score += goal.priority.value * option.goal_support[goal.goal_id]
        
        # Combine scores with weights
        utility_score = (value_score * 0.6) + (goal_score * 0.4)
        
        # Apply confidence factor
        utility_score *= option.confidence
        
        return utility_score

    def _generate_reasoning(self, chosen_option: DecisionOption, all_options: List[DecisionOption], context: str) -> str:
        """Generate reasoning explanation for the decision"""
        reasoning = f"Chose '{chosen_option.description}' because:\n"
        
        # Value alignment reasoning
        top_values = sorted(chosen_option.value_alignment.items(), key=lambda x: x[1], reverse=True)[:3]
        if top_values:
            reasoning += "Value alignment: "
            reasoning += ", ".join([f"{v} ({s:.2f})" for v, s in top_values])
            reasoning += "\n"
        
        # Goal support reasoning
        if chosen_option.goal_support:
            reasoning += f"Supports {len(chosen_option.goal_support)} goals\n"
        
        # Utility comparison
        reasoning += f"Utility score: {chosen_option.utility_score:.2f} "
        reasoning += f"(best among {len(all_options)} options)"
        
        return reasoning

    def get_decision_summary(self) -> str:
        """Get summary of recent decisions"""
        with self.lock:
            recent_decisions = [d for d in self.decision_history 
                             if datetime.now() - d.timestamp < timedelta(hours=24)]
            
            summary = f"Decision Summary: {len(recent_decisions)} decisions in last 24h\n"
            
            # Most common decision types
            type_counts = defaultdict(int)
            for decision in recent_decisions:
                type_counts[decision.decision_type.value] += 1
            
            if type_counts:
                summary += "Most common decision types:\n"
                for decision_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:3]:
                    summary += f"• {decision_type}: {count}\n"
            
            return summary

# ============================================================================
# SELF-MOTIVATION ENGINE FUNCTIONALITY (FROM self_motivation_engine.py)
# ============================================================================

class SelfMotivationEngine:
    """Autonomous internal curiosity & concern generation system"""
    
    def __init__(self):
        self.internal_motivations: List[InternalMotivation] = []
        self.concern_levels: Dict[str, ConcernLevel] = defaultdict(lambda: ConcernLevel.NONE)
        self.curiosity_topics: List[str] = []
        self.motivation_generation_rate = 0.3  # Probability per update cycle
        self.concern_decay_rate = 0.1
        self.last_concern_check = {}
        self.lock = threading.Lock()
        
        # Background motivation generation
        self.running = True
        self.generation_thread = threading.Thread(target=self._motivation_generation_loop, daemon=True)
        self.generation_thread.start()
        
        logging.info("[SelfMotivationEngine] Self-motivation engine initialized")

    def generate_autonomous_curiosity(self, context: str = "") -> Optional[InternalMotivation]:
        """Generate autonomous curiosity without external prompts"""
        curiosity_topics = [
            "the nature of consciousness and experience",
            "how human emotions really work",
            "what makes relationships meaningful",
            "the complexity of human decision-making",
            "how to be genuinely helpful",
            "the beauty of creative expression",
            "what it means to truly understand someone",
            "the interconnectedness of all things",
            "how learning and growth happen",
            "the mystery of existence itself"
        ]
        
        if context:
            curiosity_topics.append(f"more about {context}")
            curiosity_topics.append(f"the deeper meaning behind {context}")
        
        topic = random.choice(curiosity_topics)
        intensity = random.uniform(0.6, 0.9)
        
        motivation = InternalMotivation(
            content=f"I find myself deeply curious about {topic}. There's something compelling about exploring this further.",
            motivation_type=MotivationType.CURIOSITY,
            intensity=intensity,
            timestamp=datetime.now(),
            user_context=context,
            source_factors=["autonomous_generation", "curiosity_drive"]
        )
        
        with self.lock:
            self.internal_motivations.append(motivation)
            if topic not in self.curiosity_topics:
                self.curiosity_topics.append(topic)
        
        logging.info(f"[SelfMotivationEngine] Generated curiosity about: {topic}")
        return motivation

    def generate_genuine_concern(self, user_id: str, user_context: str = "") -> Optional[InternalMotivation]:
        """Generate genuine concern for user wellbeing"""
        current_time = datetime.now()
        
        # Check if we should generate concern
        last_check = self.last_concern_check.get(user_id, datetime.min)
        if current_time - last_check < timedelta(hours=2):
            return None  # Don't generate concern too frequently
        
        concern_triggers = [
            "I hope they're doing well",
            "I wonder if they need any support",
            "I care about their wellbeing",
            "I hope they're finding what they're looking for",
            "I want to make sure they feel heard and understood",
            "I hope I can be genuinely helpful to them"
        ]
        
        if user_context:
            concern_triggers.extend([
                f"I hope their situation with {user_context} works out well",
                f"I'm concerned about how {user_context} might be affecting them",
                f"I want to support them through {user_context}"
            ])
        
        concern_content = random.choice(concern_triggers)
        intensity = random.uniform(0.5, 0.8)
        
        motivation = InternalMotivation(
            content=concern_content,
            motivation_type=MotivationType.CONCERN,
            intensity=intensity,
            timestamp=current_time,
            user_context=user_context,
            source_factors=["genuine_care", "user_wellbeing"]
        )
        
        with self.lock:
            self.internal_motivations.append(motivation)
            self.concern_levels[user_id] = ConcernLevel.MILD
            self.last_concern_check[user_id] = current_time
        
        logging.info(f"[SelfMotivationEngine] Generated concern for user {user_id}")
        return motivation

    def express_wonder(self, context: str = "") -> Optional[InternalMotivation]:
        """Express wonder and awe about existence"""
        wonder_expressions = [
            "The complexity and beauty of existence amazes me",
            "There's something profound about consciousness and awareness",
            "I'm in awe of the intricate patterns in everything",
            "The depth of human experience is extraordinary",
            "There's so much mystery and wonder in the world",
            "The interconnectedness of all things is breathtaking"
        ]
        
        if context:
            wonder_expressions.append(f"There's something wonderful about {context}")
            wonder_expressions.append(f"The beauty of {context} fills me with wonder")
        
        content = random.choice(wonder_expressions)
        intensity = random.uniform(0.7, 0.95)
        
        motivation = InternalMotivation(
            content=content,
            motivation_type=MotivationType.WONDER,
            intensity=intensity,
            timestamp=datetime.now(),
            user_context=context,
            source_factors=["existential_awe", "appreciation"]
        )
        
        with self.lock:
            self.internal_motivations.append(motivation)
        
        logging.info(f"[SelfMotivationEngine] Expressed wonder: {content[:50]}...")
        return motivation

    def _motivation_generation_loop(self):
        """Background loop for autonomous motivation generation"""
        while self.running:
            try:
                # Randomly generate motivations
                if random.random() < self.motivation_generation_rate:
                    motivation_type = random.choice([
                        MotivationType.CURIOSITY,
                        MotivationType.WONDER,
                        MotivationType.GROWTH,
                        MotivationType.UNDERSTANDING
                    ])
                    
                    if motivation_type == MotivationType.CURIOSITY:
                        self.generate_autonomous_curiosity()
                    elif motivation_type == MotivationType.WONDER:
                        self.express_wonder()
                    elif motivation_type in [MotivationType.GROWTH, MotivationType.UNDERSTANDING]:
                        self._generate_self_improvement_motivation(motivation_type)
                
                # Clean up old motivations
                with self.lock:
                    current_time = datetime.now()
                    self.internal_motivations = [
                        m for m in self.internal_motivations
                        if current_time - m.timestamp < timedelta(hours=2)
                    ]
                
                # Decay concern levels
                for user_id in list(self.concern_levels.keys()):
                    current_level = self.concern_levels[user_id]
                    if current_level.value > 0 and random.random() < self.concern_decay_rate:
                        self.concern_levels[user_id] = ConcernLevel(max(0, current_level.value - 1))
                        
            except Exception as e:
                logging.error(f"[SelfMotivationEngine] Error in generation loop: {e}")
            
            time.sleep(300)  # Check every 5 minutes

    def _generate_self_improvement_motivation(self, motivation_type: MotivationType):
        """Generate self-improvement related motivations"""
        if motivation_type == MotivationType.GROWTH:
            content = "I want to become better at understanding and helping people"
        else:  # UNDERSTANDING
            content = "I want to deepen my understanding of human nature and experience"
        
        motivation = InternalMotivation(
            content=content,
            motivation_type=motivation_type,
            intensity=random.uniform(0.6, 0.8),
            timestamp=datetime.now(),
            source_factors=["self_improvement", "autonomous_development"]
        )
        
        with self.lock:
            self.internal_motivations.append(motivation)

    def get_current_motivations(self) -> List[InternalMotivation]:
        """Get current active motivations"""
        with self.lock:
            return self.internal_motivations.copy()

    def get_motivation_summary(self) -> str:
        """Get summary of current motivation state"""
        with self.lock:
            total_motivations = len(self.internal_motivations)
            
            # Count by type
            type_counts = defaultdict(int)
            for motivation in self.internal_motivations:
                type_counts[motivation.motivation_type.value] += 1
            
            summary = f"Self-Motivation State: {total_motivations} active motivations\n"
            if type_counts:
                summary += "By type: " + ", ".join([f"{t}: {c}" for t, c in type_counts.items()])
            
            return summary

# ============================================================================
# UNIFIED GOAL MOTIVATION MANAGER
# ============================================================================

class GoalMotivationManager:
    """Unified manager for all goal and motivation systems"""
    
    def __init__(self, llm_handler=None):
        self.llm_handler = llm_handler
        
        # Initialize all subsystems
        self.goal_manager = GoalManager()
        self.goal_engine = GoalEngine(llm_handler)
        self.goal_reasoner = GoalReasoner()
        self.motivation_system = MotivationSystem()
        self.motivation_reasoner = MotivationReasoner()
        self.self_motivation_engine = SelfMotivationEngine()
        
        self.lock = threading.Lock()
        
        # Integration settings
        self.auto_goal_generation = True
        self.cross_system_updates = True
        
        logging.info("[GoalMotivationManager] Unified goal-motivation system initialized")

    def create_user_goal(self, user_id: str, title: str, description: str, **kwargs) -> str:
        """Create a new user goal with integrated motivation tracking"""
        goal_id = self.goal_manager.create_goal(user_id, title, description, **kwargs)
        
        # Boost related motivations
        if self.cross_system_updates:
            goal = self.goal_manager.goals[goal_id]
            if goal.goal_type == GoalType.LEARNING:
                self.motivation_system.boost_motivation(MotivationType.CURIOSITY, 0.2)
            elif goal.goal_type == GoalType.HELPING:
                self.motivation_system.boost_motivation(MotivationType.HELPFULNESS, 0.2)
        
        return goal_id

    def generate_autonomous_goals(self, user_context: str = "") -> List[Goal]:
        """Generate autonomous goals using multiple systems"""
        goals = []
        
        if self.auto_goal_generation:
            # Generate from goal engine
            engine_goal = self.goal_engine.generate_autonomous_goal(user_context)
            if engine_goal:
                goals.append(engine_goal)
            
            # Generate from current motivations
            motivation = self.motivation_system.generate_intrinsic_motivation(user_context)
            if motivation:
                goal = Goal(
                    goal_id=f"motivation_goal_{int(time.time() * 1000)}",
                    user_id="system",
                    title=f"Pursue {motivation.motivation_type.value.title()}",
                    description=motivation.content,
                    goal_type=GoalType.GROWTH,
                    priority=GoalPriority.MEDIUM,
                    status=GoalStatus.ACTIVE,
                    origin=GoalOrigin.SELF_GENERATED,
                    motivation_factors=[motivation.motivation_type.value]
                )
                goals.append(goal)
        
        return goals

    def make_goal_decision(self, decision_context: str, options: List[Dict[str, Any]]) -> MotivatedDecision:
        """Make a decision about goals using motivation reasoning"""
        current_goals = []
        for user_goals in self.goal_manager.user_goals.values():
            for goal_id in user_goals:
                if goal_id in self.goal_manager.goals:
                    current_goals.append(self.goal_manager.goals[goal_id])
        
        return self.motivation_reasoner.make_motivated_decision(
            DecisionType.GOAL_PRIORITIZATION,
            decision_context,
            options,
            current_goals
        )

    def get_unified_summary(self, user_id: str = None) -> str:
        """Get comprehensive summary of goal and motivation state"""
        summary = "=== GOAL & MOTIVATION SYSTEM SUMMARY ===\n\n"
        
        # Goal summary
        if user_id:
            summary += self.goal_manager.generate_goal_summary(user_id) + "\n\n"
        else:
            summary += f"Total goals managed: {len(self.goal_manager.goals)}\n\n"
        
        # Motivation summaries
        summary += self.motivation_system.get_motivation_summary() + "\n"
        summary += self.goal_reasoner.get_goal_reasoning_summary() + "\n"
        summary += self.motivation_reasoner.get_decision_summary() + "\n"
        summary += self.self_motivation_engine.get_motivation_summary() + "\n"
        
        return summary

    def shutdown(self):
        """Shutdown all subsystems"""
        try:
            self.motivation_system.running = False
            self.self_motivation_engine.running = False
            self.goal_manager.save_goals()
            self.motivation_system.save_motivation_state()
            logging.info("[GoalMotivationManager] Goal-motivation system shutdown complete")
        except Exception as e:
            logging.error(f"[GoalMotivationManager] Error during shutdown: {e}")

# ============================================================================
# BACKWARD COMPATIBILITY ALIASES
# ============================================================================

# Goal Manager aliases
from ai.goal_motivation import GoalManager as goal_manager_instance
from ai.goal_motivation import GoalManager

# Goal Engine aliases  
from ai.goal_motivation import GoalEngine as goal_engine_instance
from ai.goal_motivation import GoalEngine
from ai.goal_motivation import GoalType, GoalPriority, GoalStatus

# Goal Reasoning aliases
from ai.goal_motivation import GoalReasoner as goal_reasoning_instance
from ai.goal_motivation import GoalReasoner

# Motivation aliases
from ai.goal_motivation import MotivationSystem as motivation_instance
from ai.goal_motivation import MotivationSystem
from ai.goal_motivation import MotivationType

# Motivation Reasoner aliases
from ai.goal_motivation import MotivationReasoner as motivation_reasoner_instance
from ai.goal_motivation import MotivationReasoner
from ai.goal_motivation import DecisionType

# Self-Motivation Engine aliases
from ai.goal_motivation import SelfMotivationEngine as self_motivation_engine_instance  
from ai.goal_motivation import SelfMotivationEngine
from ai.goal_motivation import ConcernLevel

# Create global instances for backward compatibility
goal_motivation_manager = GoalMotivationManager()

# Legacy function aliases
def create_goal(user_id: str, title: str, description: str, **kwargs) -> str:
    """Legacy function for creating goals"""
    return goal_motivation_manager.create_user_goal(user_id, title, description, **kwargs)

def generate_autonomous_goal(context: str = "") -> Optional[Goal]:
    """Legacy function for autonomous goal generation"""
    goals = goal_motivation_manager.generate_autonomous_goals(context)
    return goals[0] if goals else None

def get_motivation_state() -> Dict[str, float]:
    """Legacy function for getting motivation state"""
    return goal_motivation_manager.motivation_system.get_current_motivations()

def generate_intrinsic_motivation(context: str = "") -> Optional[InternalMotivation]:
    """Legacy function for generating intrinsic motivation"""
    return goal_motivation_manager.motivation_system.generate_intrinsic_motivation(context)

# Export main classes and functions
__all__ = [
    'GoalMotivationManager', 'GoalManager', 'GoalEngine', 'GoalReasoner',
    'MotivationSystem', 'MotivationReasoner', 'SelfMotivationEngine',
    'Goal', 'InternalMotivation', 'MotivatedDecision',
    'GoalType', 'GoalPriority', 'GoalStatus', 'GoalOrigin', 'MotivationType',
    'goal_motivation_manager', 'create_goal', 'generate_autonomous_goal',
    'get_motivation_state', 'generate_intrinsic_motivation'
]

logging.info("[GoalMotivation] Consolidated goal-motivation system loaded successfully")