"""
Meta-Cognitive Monitor - Thinking About Thinking Module

This module implements meta-cognitive awareness and monitoring:
- Monitoring of cognitive processes and mental states
- Self-awareness of thinking patterns and strategies
- Cognitive performance assessment and optimization
- Metacognitive knowledge management
- Strategy selection and adaptation
- Error detection and correction in thinking
- Learning from cognitive experiences
"""

import threading
import time
import logging
from typing import Dict, List, Any, Optional, Set, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import json
from pathlib import Path
import statistics

class CognitiveProcess(Enum):
    """Types of cognitive processes to monitor"""
    ATTENTION = "attention"
    MEMORY = "memory"
    REASONING = "reasoning"
    DECISION_MAKING = "decision_making"
    PROBLEM_SOLVING = "problem_solving"
    LEARNING = "learning"
    LANGUAGE_PROCESSING = "language"
    EMOTIONAL_PROCESSING = "emotion"
    PERCEPTION = "perception"
    PLANNING = "planning"

class MetaCognitiveStrategy(Enum):
    """Meta-cognitive strategies"""
    MONITORING = "monitoring"        # Keeping track of progress
    EVALUATION = "evaluation"        # Assessing performance
    PLANNING = "planning"           # Strategy selection
    REGULATION = "regulation"       # Adjusting strategies
    REFLECTION = "reflection"       # Reflecting on thinking
    PREDICTION = "prediction"       # Predicting outcomes

class CognitiveState(Enum):
    """Current cognitive state"""
    OPTIMAL = "optimal"             # Performing at peak
    GOOD = "good"                  # Performing well
    MODERATE = "moderate"          # Average performance
    SUBOPTIMAL = "suboptimal"      # Below average
    STRUGGLING = "struggling"      # Having difficulties
    OVERLOADED = "overloaded"      # Cognitive overload

@dataclass
class CognitiveEvent:
    """An event in cognitive processing"""
    timestamp: datetime
    process: CognitiveProcess
    event_type: str  # "start", "end", "error", "success", etc.
    details: Dict[str, Any]
    performance_score: Optional[float] = None
    strategy_used: Optional[str] = None
    outcome: Optional[str] = None

@dataclass
class MetaCognitiveInsight:
    """An insight about cognitive processing"""
    timestamp: datetime
    insight_type: str
    content: str
    confidence: float
    supporting_evidence: List[str]
    potential_actions: List[str]
    cognitive_processes_involved: List[CognitiveProcess]

@dataclass
class CognitivePattern:
    """A detected pattern in cognitive processing"""
    pattern_id: str
    pattern_type: str
    description: str
    frequency: int
    success_rate: float
    contexts: List[str]
    triggers: List[str]
    outcomes: List[str]
    first_observed: datetime
    last_observed: datetime

@dataclass
class StrategyPerformance:
    """Performance metrics for a cognitive strategy"""
    strategy_name: str
    times_used: int
    success_rate: float
    average_duration: float
    contexts_used: List[str]
    performance_scores: List[float]
    last_used: datetime

class MetaCognitiveMonitor:
    """
    Meta-cognitive monitoring system for consciousness.
    
    This module provides advanced self-awareness of cognitive processes,
    enabling the AI to monitor, evaluate, and optimize its own thinking.
    """
    
    def __init__(self, save_path: str = "ai_metacognitive_monitor.json"):
        self.save_path = Path(save_path)
        
        # Core monitoring state
        self.cognitive_events: List[CognitiveEvent] = []
        self.active_processes: Dict[CognitiveProcess, CognitiveEvent] = {}
        self.metacognitive_insights: List[MetaCognitiveInsight] = []
        self.cognitive_patterns: Dict[str, CognitivePattern] = {}
        self.strategy_performance: Dict[str, StrategyPerformance] = {}
        
        # Current state
        self.current_cognitive_state = CognitiveState.MODERATE
        self.active_strategies: Set[MetaCognitiveStrategy] = set()
        self.cognitive_load_history: List[Tuple[datetime, float]] = []
        self.performance_history: List[Tuple[datetime, float]] = []
        
        # Configuration
        self.max_event_history = 1000
        self.max_insight_history = 200
        self.pattern_detection_threshold = 3  # Minimum occurrences to detect pattern
        self.performance_window = 300  # Seconds for performance averaging
        
        # Monitoring parameters
        self.monitoring_interval = 1.0  # Seconds between monitoring cycles
        self.insight_generation_threshold = 0.7  # Confidence threshold for insights
        self.strategy_adaptation_threshold = 0.6  # Performance threshold for strategy changes
        
        # Metrics
        self.total_cognitive_events = 0
        self.insights_generated = 0
        self.patterns_detected = 0
        self.strategy_adaptations = 0
        
        # Threading
        self.is_active = False
        self.monitor_thread = None
        self.state_lock = threading.Lock()
        
        # Callbacks for different processes
        self.process_monitors: Dict[CognitiveProcess, Callable] = {}
        
        # Load persisted state
        self._load_state()
        
        logging.info("[MetaCognitive] 🧠 Meta-Cognitive Monitor initialized")
    
    def start(self):
        """Start the meta-cognitive monitoring system"""
        if self.is_active:
            return
        
        self.is_active = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()
        
        logging.info("[MetaCognitive] 🧠 Meta-cognitive monitoring started")
    
    def stop(self):
        """Stop the meta-cognitive monitoring system"""
        if not self.is_active:
            return
        
        self.is_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2.0)
        
        self._save_state()
        logging.info("[MetaCognitive] 🧠 Meta-cognitive monitoring stopped")
    
    def start_cognitive_process(self, process: CognitiveProcess, details: Dict[str, Any] = None,
                               strategy: str = None) -> str:
        """Start monitoring a cognitive process"""
        with self.state_lock:
            event = CognitiveEvent(
                timestamp=datetime.now(),
                process=process,
                event_type="start",
                details=details or {},
                strategy_used=strategy
            )
            
            self.cognitive_events.append(event)
            self.active_processes[process] = event
            self.total_cognitive_events += 1
            
            # Trim history if needed
            if len(self.cognitive_events) > self.max_event_history:
                self.cognitive_events = self.cognitive_events[-self.max_event_history:]
            
            event_id = f"{process.value}_{event.timestamp.timestamp()}"
            logging.debug(f"[MetaCognitive] 🔄 Started monitoring: {process.value}")
            
            return event_id
    
    def end_cognitive_process(self, process: CognitiveProcess, outcome: str = None,
                             performance_score: float = None, details: Dict[str, Any] = None):
        """End monitoring a cognitive process"""
        with self.state_lock:
            if process not in self.active_processes:
                logging.warning(f"[MetaCognitive] ⚠️ Attempted to end untracked process: {process.value}")
                return
            
            start_event = self.active_processes[process]
            duration = (datetime.now() - start_event.timestamp).total_seconds()
            
            end_event = CognitiveEvent(
                timestamp=datetime.now(),
                process=process,
                event_type="end",
                details={
                    "duration": duration,
                    "start_timestamp": start_event.timestamp.isoformat(),
                    **(details or {})
                },
                performance_score=performance_score,
                strategy_used=start_event.strategy_used,
                outcome=outcome
            )
            
            self.cognitive_events.append(end_event)
            del self.active_processes[process]
            
            # Update strategy performance if applicable
            if start_event.strategy_used:
                self._update_strategy_performance(start_event.strategy_used, duration, 
                                                performance_score, outcome)
            
            # Detect patterns
            self._detect_cognitive_patterns(process, start_event, end_event)
            
            # Generate insights if warranted
            self._potentially_generate_insight(process, start_event, end_event)
            
            logging.debug(f"[MetaCognitive] ✅ Ended monitoring: {process.value} (duration: {duration:.1f}s)")
    
    def report_cognitive_error(self, process: CognitiveProcess, error_type: str,
                              details: Dict[str, Any] = None):
        """Report an error in cognitive processing"""
        with self.state_lock:
            error_event = CognitiveEvent(
                timestamp=datetime.now(),
                process=process,
                event_type="error",
                details={
                    "error_type": error_type,
                    **(details or {})
                },
                performance_score=0.0,
                outcome="error"
            )
            
            self.cognitive_events.append(error_event)
            
            # Generate insight about the error
            self._generate_error_insight(process, error_type, details or {})
            
            logging.warning(f"[MetaCognitive] ❌ Cognitive error reported: {process.value} - {error_type}")
    
    def assess_cognitive_state(self) -> CognitiveState:
        """Assess current overall cognitive state"""
        with self.state_lock:
            recent_events = [
                e for e in self.cognitive_events
                if (datetime.now() - e.timestamp).total_seconds() < self.performance_window
            ]
            
            if not recent_events:
                return CognitiveState.MODERATE
            
            # Calculate average performance
            performance_scores = [
                e.performance_score for e in recent_events
                if e.performance_score is not None
            ]
            
            if not performance_scores:
                return CognitiveState.MODERATE
            
            avg_performance = statistics.mean(performance_scores)
            error_rate = len([e for e in recent_events if e.event_type == "error"]) / len(recent_events)
            
            # Determine cognitive state
            if avg_performance >= 0.9 and error_rate < 0.05:
                state = CognitiveState.OPTIMAL
            elif avg_performance >= 0.7 and error_rate < 0.1:
                state = CognitiveState.GOOD
            elif avg_performance >= 0.5 and error_rate < 0.2:
                state = CognitiveState.MODERATE
            elif avg_performance >= 0.3 and error_rate < 0.3:
                state = CognitiveState.SUBOPTIMAL
            elif error_rate < 0.5:
                state = CognitiveState.STRUGGLING
            else:
                state = CognitiveState.OVERLOADED
            
            if state != self.current_cognitive_state:
                logging.info(f"[MetaCognitive] 🧠 Cognitive state changed: {self.current_cognitive_state.value} → {state.value}")
                self.current_cognitive_state = state
            
            return state
    
    def generate_metacognitive_insight(self, insight_type: str, content: str,
                                     confidence: float, evidence: List[str] = None,
                                     actions: List[str] = None,
                                     processes: List[CognitiveProcess] = None):
        """Generate a meta-cognitive insight"""
        with self.state_lock:
            insight = MetaCognitiveInsight(
                timestamp=datetime.now(),
                insight_type=insight_type,
                content=content,
                confidence=confidence,
                supporting_evidence=evidence or [],
                potential_actions=actions or [],
                cognitive_processes_involved=processes or []
            )
            
            self.metacognitive_insights.append(insight)
            self.insights_generated += 1
            
            # Trim history if needed
            if len(self.metacognitive_insights) > self.max_insight_history:
                self.metacognitive_insights = self.metacognitive_insights[-self.max_insight_history:]
            
            logging.info(f"[MetaCognitive] 💡 Generated insight: {insight_type} (confidence: {confidence:.2f})")
    
    def get_cognitive_performance(self, process: CognitiveProcess = None,
                                time_window: int = 300) -> Dict[str, Any]:
        """Get cognitive performance metrics"""
        with self.state_lock:
            cutoff_time = datetime.now() - timedelta(seconds=time_window)
            
            if process:
                relevant_events = [
                    e for e in self.cognitive_events
                    if e.process == process and e.timestamp >= cutoff_time
                ]
            else:
                relevant_events = [
                    e for e in self.cognitive_events
                    if e.timestamp >= cutoff_time
                ]
            
            if not relevant_events:
                return {"error": "No relevant events found"}
            
            # Calculate metrics
            performance_scores = [
                e.performance_score for e in relevant_events
                if e.performance_score is not None
            ]
            
            durations = [
                e.details.get("duration", 0) for e in relevant_events
                if e.event_type == "end" and "duration" in e.details
            ]
            
            error_events = [e for e in relevant_events if e.event_type == "error"]
            success_events = [e for e in relevant_events if e.outcome == "success"]
            
            return {
                "process": process.value if process else "all",
                "time_window": time_window,
                "total_events": len(relevant_events),
                "average_performance": statistics.mean(performance_scores) if performance_scores else None,
                "performance_std": statistics.stdev(performance_scores) if len(performance_scores) > 1 else 0,
                "average_duration": statistics.mean(durations) if durations else None,
                "error_rate": len(error_events) / len(relevant_events) if relevant_events else 0,
                "success_rate": len(success_events) / len(relevant_events) if relevant_events else 0,
                "most_used_strategies": self._get_most_used_strategies(relevant_events)
            }
    
    def recommend_cognitive_strategy(self, process: CognitiveProcess,
                                   context: Dict[str, Any] = None) -> Optional[str]:
        """Recommend a cognitive strategy based on performance history"""
        with self.state_lock:
            # Find strategies used for this process
            process_events = [e for e in self.cognitive_events if e.process == process]
            strategy_performance = {}
            
            for event in process_events:
                if event.strategy_used and event.performance_score is not None:
                    if event.strategy_used not in strategy_performance:
                        strategy_performance[event.strategy_used] = []
                    strategy_performance[event.strategy_used].append(event.performance_score)
            
            if not strategy_performance:
                return None
            
            # Find best performing strategy
            best_strategy = None
            best_avg_performance = 0
            
            for strategy, scores in strategy_performance.items():
                avg_performance = statistics.mean(scores)
                if avg_performance > best_avg_performance and len(scores) >= 2:
                    best_avg_performance = avg_performance
                    best_strategy = strategy
            
            if best_strategy and best_avg_performance > self.strategy_adaptation_threshold:
                logging.debug(f"[MetaCognitive] 💡 Recommended strategy for {process.value}: {best_strategy}")
                return best_strategy
            
            return None
    
    def get_metacognitive_insights(self, insight_type: str = None,
                                 min_confidence: float = 0.0) -> List[MetaCognitiveInsight]:
        """Get meta-cognitive insights"""
        with self.state_lock:
            insights = self.metacognitive_insights
            
            if insight_type:
                insights = [i for i in insights if i.insight_type == insight_type]
            
            if min_confidence > 0:
                insights = [i for i in insights if i.confidence >= min_confidence]
            
            return sorted(insights, key=lambda i: i.timestamp, reverse=True)
    
    def get_cognitive_patterns(self, pattern_type: str = None) -> List[CognitivePattern]:
        """Get detected cognitive patterns"""
        with self.state_lock:
            patterns = list(self.cognitive_patterns.values())
            
            if pattern_type:
                patterns = [p for p in patterns if p.pattern_type == pattern_type]
            
            return sorted(patterns, key=lambda p: p.frequency, reverse=True)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get meta-cognitive monitoring statistics"""
        with self.state_lock:
            return {
                "cognitive_state": self.current_cognitive_state.value,
                "active_processes": len(self.active_processes),
                "total_events": self.total_cognitive_events,
                "insights_generated": self.insights_generated,
                "patterns_detected": len(self.cognitive_patterns),
                "strategy_adaptations": self.strategy_adaptations,
                "active_strategies": [s.value for s in self.active_strategies],
                "recent_performance": self._get_recent_performance(),
                "cognitive_load": self._calculate_cognitive_load()
            }
    
    def _monitoring_loop(self):
        """Main meta-cognitive monitoring loop"""
        logging.info("[MetaCognitive] 🔄 Meta-cognitive monitoring loop started")
        
        while self.is_active:
            try:
                # Assess cognitive state
                self.assess_cognitive_state()
                
                # Update cognitive load history
                self._update_cognitive_load_history()
                
                # Check for strategy adaptations
                self._check_strategy_adaptations()
                
                # Generate periodic insights
                self._generate_periodic_insights()
                
                # Save state periodically
                if datetime.now().timestamp() % 300 < 1:  # Every 5 minutes
                    self._save_state()
                
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                logging.error(f"[MetaCognitive] ❌ Monitoring loop error: {e}")
                time.sleep(1.0)
        
        logging.info("[MetaCognitive] 🔄 Meta-cognitive monitoring loop ended")
    
    def _update_strategy_performance(self, strategy: str, duration: float,
                                   performance_score: float, outcome: str):
        """Update performance metrics for a strategy"""
        if strategy not in self.strategy_performance:
            self.strategy_performance[strategy] = StrategyPerformance(
                strategy_name=strategy,
                times_used=0,
                success_rate=0.0,
                average_duration=0.0,
                contexts_used=[],
                performance_scores=[],
                last_used=datetime.now()
            )
        
        perf = self.strategy_performance[strategy]
        perf.times_used += 1
        perf.last_used = datetime.now()
        
        if performance_score is not None:
            perf.performance_scores.append(performance_score)
            # Keep only recent scores
            if len(perf.performance_scores) > 20:
                perf.performance_scores = perf.performance_scores[-20:]
        
        # Update success rate
        if outcome:
            success_count = len([s for s in perf.performance_scores if s >= 0.7])
            perf.success_rate = success_count / len(perf.performance_scores) if perf.performance_scores else 0.0
        
        # Update average duration
        if duration > 0:
            perf.average_duration = (perf.average_duration * (perf.times_used - 1) + duration) / perf.times_used
    
    def _detect_cognitive_patterns(self, process: CognitiveProcess,
                                 start_event: CognitiveEvent, end_event: CognitiveEvent):
        """Detect patterns in cognitive processing"""
        # Simple pattern detection based on strategy + outcome combinations
        if not start_event.strategy_used or not end_event.outcome:
            return
        
        pattern_id = f"{process.value}_{start_event.strategy_used}_{end_event.outcome}"
        
        if pattern_id not in self.cognitive_patterns:
            self.cognitive_patterns[pattern_id] = CognitivePattern(
                pattern_id=pattern_id,
                pattern_type="strategy_outcome",
                description=f"Using {start_event.strategy_used} for {process.value} resulting in {end_event.outcome}",
                frequency=0,
                success_rate=0.0,
                contexts=[],
                triggers=[],
                outcomes=[],
                first_observed=datetime.now(),
                last_observed=datetime.now()
            )
            self.patterns_detected += 1
        
        pattern = self.cognitive_patterns[pattern_id]
        pattern.frequency += 1
        pattern.last_observed = datetime.now()
        pattern.outcomes.append(end_event.outcome)
        
        # Update success rate
        success_count = len([o for o in pattern.outcomes if o == "success"])
        pattern.success_rate = success_count / len(pattern.outcomes)
    
    def _potentially_generate_insight(self, process: CognitiveProcess,
                                    start_event: CognitiveEvent, end_event: CognitiveEvent):
        """Generate insights based on cognitive events"""
        # Generate insight for particularly good or bad performance
        if end_event.performance_score is None:
            return
        
        if end_event.performance_score >= 0.9:
            self.generate_metacognitive_insight(
                "high_performance",
                f"Excellent performance in {process.value} using {start_event.strategy_used or 'default strategy'}",
                0.8,
                [f"Performance score: {end_event.performance_score:.2f}"],
                [f"Continue using {start_event.strategy_used or 'current approach'} for {process.value}"],
                [process]
            )
        elif end_event.performance_score <= 0.3:
            self.generate_metacognitive_insight(
                "low_performance",
                f"Poor performance in {process.value} - consider strategy adjustment",
                0.7,
                [f"Performance score: {end_event.performance_score:.2f}"],
                [f"Try different strategy for {process.value}", "Investigate root cause of poor performance"],
                [process]
            )
    
    def _generate_error_insight(self, process: CognitiveProcess, error_type: str, details: Dict[str, Any]):
        """Generate insight about cognitive errors"""
        self.generate_metacognitive_insight(
            "error_analysis",
            f"Error in {process.value}: {error_type}",
            0.6,
            [f"Error type: {error_type}", f"Details: {details}"],
            ["Review error pattern", "Adjust strategy", "Increase monitoring"],
            [process]
        )
    
    def _get_most_used_strategies(self, events: List[CognitiveEvent]) -> List[Tuple[str, int]]:
        """Get most frequently used strategies from events"""
        strategy_counts = {}
        for event in events:
            if event.strategy_used:
                strategy_counts[event.strategy_used] = strategy_counts.get(event.strategy_used, 0) + 1
        
        return sorted(strategy_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    def _get_recent_performance(self) -> Optional[float]:
        """Get recent average performance"""
        recent_events = [
            e for e in self.cognitive_events
            if (datetime.now() - e.timestamp).total_seconds() < 300 and
               e.performance_score is not None
        ]
        
        if not recent_events:
            return None
        
        return statistics.mean([e.performance_score for e in recent_events])
    
    def _calculate_cognitive_load(self) -> float:
        """Calculate current cognitive load based on active processes"""
        base_load = len(self.active_processes) * 0.2
        return min(1.0, base_load)
    
    def _update_cognitive_load_history(self):
        """Update cognitive load history"""
        current_load = self._calculate_cognitive_load()
        self.cognitive_load_history.append((datetime.now(), current_load))
        
        # Keep only recent history (last hour)
        cutoff_time = datetime.now() - timedelta(hours=1)
        self.cognitive_load_history = [
            (timestamp, load) for timestamp, load in self.cognitive_load_history
            if timestamp >= cutoff_time
        ]
    
    def _check_strategy_adaptations(self):
        """Check if strategy adaptations are needed"""
        # Simple check for strategies with declining performance
        for strategy_name, perf in self.strategy_performance.items():
            if len(perf.performance_scores) >= 5:
                recent_scores = perf.performance_scores[-3:]
                older_scores = perf.performance_scores[-6:-3] if len(perf.performance_scores) >= 6 else []
                
                if older_scores and statistics.mean(recent_scores) < statistics.mean(older_scores) - 0.2:
                    self.generate_metacognitive_insight(
                        "strategy_decline",
                        f"Strategy '{strategy_name}' showing performance decline",
                        0.6,
                        [f"Recent average: {statistics.mean(recent_scores):.2f}",
                         f"Previous average: {statistics.mean(older_scores):.2f}"],
                        [f"Consider alternative to {strategy_name}", "Investigate cause of decline"],
                        []
                    )
                    self.strategy_adaptations += 1
    
    def _generate_periodic_insights(self):
        """Generate periodic insights about overall cognitive patterns"""
        # Generate insights every 10 minutes
        if datetime.now().timestamp() % 600 < self.monitoring_interval:
            cognitive_state = self.assess_cognitive_state()
            
            if cognitive_state in [CognitiveState.OPTIMAL, CognitiveState.GOOD]:
                self.generate_metacognitive_insight(
                    "periodic_assessment",
                    f"Cognitive state is {cognitive_state.value} - maintaining good performance",
                    0.5,
                    [f"Current state: {cognitive_state.value}"],
                    ["Continue current strategies"],
                    []
                )
            elif cognitive_state in [CognitiveState.STRUGGLING, CognitiveState.OVERLOADED]:
                self.generate_metacognitive_insight(
                    "periodic_assessment",
                    f"Cognitive state is {cognitive_state.value} - intervention may be needed",
                    0.7,
                    [f"Current state: {cognitive_state.value}"],
                    ["Reduce cognitive load", "Take break", "Simplify current tasks"],
                    []
                )
    
    def _save_state(self):
        """Save meta-cognitive state to file"""
        try:
            # Prepare data for serialization
            state_data = {
                "current_cognitive_state": self.current_cognitive_state.value,
                "active_strategies": [s.value for s in self.active_strategies],
                "metrics": {
                    "total_cognitive_events": self.total_cognitive_events,
                    "insights_generated": self.insights_generated,
                    "patterns_detected": len(self.cognitive_patterns),
                    "strategy_adaptations": self.strategy_adaptations
                },
                "recent_insights": [
                    {
                        "timestamp": insight.timestamp.isoformat(),
                        "insight_type": insight.insight_type,
                        "content": insight.content,
                        "confidence": insight.confidence
                    }
                    for insight in self.metacognitive_insights[-10:]  # Last 10 insights
                ],
                "cognitive_patterns": {
                    pattern_id: {
                        "pattern_type": pattern.pattern_type,
                        "description": pattern.description,
                        "frequency": pattern.frequency,
                        "success_rate": pattern.success_rate,
                        "first_observed": pattern.first_observed.isoformat(),
                        "last_observed": pattern.last_observed.isoformat()
                    }
                    for pattern_id, pattern in self.cognitive_patterns.items()
                },
                "timestamp": datetime.now().isoformat()
            }
            
            with open(self.save_path, 'w') as f:
                json.dump(state_data, f, indent=2)
                
        except Exception as e:
            logging.error(f"[MetaCognitive] ❌ Error saving state: {e}")
    
    def _load_state(self):
        """Load meta-cognitive state from file"""
        try:
            if not self.save_path.exists():
                return
            
            with open(self.save_path, 'r') as f:
                state_data = json.load(f)
            
            # Restore cognitive state
            if "current_cognitive_state" in state_data:
                self.current_cognitive_state = CognitiveState(state_data["current_cognitive_state"])
            
            # Restore metrics
            if "metrics" in state_data:
                metrics = state_data["metrics"]
                self.total_cognitive_events = metrics.get("total_cognitive_events", 0)
                self.insights_generated = metrics.get("insights_generated", 0)
                self.strategy_adaptations = metrics.get("strategy_adaptations", 0)
            
            # Restore cognitive patterns
            if "cognitive_patterns" in state_data:
                for pattern_id, pattern_data in state_data["cognitive_patterns"].items():
                    self.cognitive_patterns[pattern_id] = CognitivePattern(
                        pattern_id=pattern_id,
                        pattern_type=pattern_data["pattern_type"],
                        description=pattern_data["description"],
                        frequency=pattern_data["frequency"],
                        success_rate=pattern_data["success_rate"],
                        contexts=[],
                        triggers=[],
                        outcomes=[],
                        first_observed=datetime.fromisoformat(pattern_data["first_observed"]),
                        last_observed=datetime.fromisoformat(pattern_data["last_observed"])
                    )
            
            logging.info("[MetaCognitive] 💾 Meta-cognitive state loaded from disk")
            
        except Exception as e:
            logging.error(f"[MetaCognitive] ❌ Error loading state: {e}")


# Create singleton instance
metacognitive_monitor = MetaCognitiveMonitor()