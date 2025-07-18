"""
Belief Reinforcement - Dynamic Belief Confidence and Learning System

This module manages belief strength, confidence adjustment, and learning from
contradiction resolution attempts. It tracks how beliefs evolve over time
and learns from successful and failed belief updates.
"""

import json
import time
import os
from typing import Dict, List, Any, Optional, Tuple, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import random
import math

class BeliefReinforcement(Enum):
    """Types of belief reinforcement"""
    POSITIVE = "positive"      # Belief was confirmed
    NEGATIVE = "negative"      # Belief was contradicted
    NEUTRAL = "neutral"        # No clear evidence either way
    CONTEXTUAL = "contextual"  # Belief applies in some contexts but not others

class LearningOutcome(Enum):
    """Outcomes of learning attempts"""
    SUCCESS = "success"                  # Successfully updated belief
    PARTIAL_SUCCESS = "partial_success"  # Some progress made
    FAILURE = "failure"                  # Failed to resolve contradiction
    DEFERRED = "deferred"               # Postponed resolution
    COMPLEXITY_REVEALED = "complexity_revealed"  # Discovered issue is more complex

@dataclass
class BeliefUpdate:
    """Record of a belief update attempt"""
    id: str
    timestamp: datetime
    belief_id: str
    old_confidence: float
    new_confidence: float
    reinforcement_type: BeliefReinforcement
    evidence: List[str]
    context: Dict[str, Any]
    learning_outcome: LearningOutcome
    resolution_method: str
    effectiveness_score: float

@dataclass
class BeliefPattern:
    """Pattern in belief evolution"""
    pattern_id: str
    belief_categories: List[str]
    common_reinforcement_types: List[BeliefReinforcement]
    typical_confidence_changes: List[float]
    success_rate: float
    context_factors: List[str]
    last_observed: datetime

@dataclass
class ContradictionResolution:
    """Record of contradiction resolution attempt"""
    id: str
    timestamp: datetime
    contradiction_description: str
    conflicting_beliefs: List[str]
    resolution_strategy: str
    outcome: LearningOutcome
    new_synthesis: Optional[str]
    confidence_adjustments: Dict[str, float]
    learning_insights: List[str]
    time_to_resolve: float  # in seconds
    complexity_score: float

class BeliefReinforcementSystem:
    """Manages belief confidence and learning from contradiction resolution"""
    
    def __init__(self, save_path: str = "ai_belief_reinforcement.json"):
        self.save_path = save_path
        self.belief_updates: List[BeliefUpdate] = []
        self.contradiction_resolutions: List[ContradictionResolution] = []
        self.belief_patterns: List[BeliefPattern] = []
        self.running = False
        
        # Learning parameters
        self.confidence_adjustment_rate = 0.1  # How much to adjust confidence per update
        self.pattern_detection_threshold = 5   # Minimum occurrences to detect pattern
        self.max_confidence = 0.95            # Maximum confidence level
        self.min_confidence = 0.05            # Minimum confidence level
        
        # Tracking current beliefs and their confidence
        self.belief_confidence: Dict[str, float] = {}
        self.belief_evidence_counts: Dict[str, int] = {}
        self.belief_contradiction_counts: Dict[str, int] = {}
        
        self._load_reinforcement_data()
        print(f"[BeliefReinforcement] 🧠 Initialized with {len(self.belief_updates)} belief updates")
    
    def start(self):
        """Start the belief reinforcement system"""
        self.running = True
        print("[BeliefReinforcement] 🧠 Belief reinforcement system started")
    
    def stop(self):
        """Stop the belief reinforcement system"""
        self.running = False
        self._save_reinforcement_data()
        print("[BeliefReinforcement] 🧠 Belief reinforcement system stopped")
    
    def reinforce_belief(self, belief_id: str, reinforcement_type: BeliefReinforcement, 
                        evidence: List[str], context: Dict[str, Any] = None) -> BeliefUpdate:
        """Reinforce or weaken a belief based on evidence"""
        if not self.running:
            return None
            
        try:
            current_confidence = self.belief_confidence.get(belief_id, 0.5)
            
            # Calculate new confidence based on reinforcement type
            new_confidence = self._calculate_new_confidence(
                current_confidence, reinforcement_type, len(evidence)
            )
            
            # Determine learning outcome
            outcome = self._assess_learning_outcome(reinforcement_type, evidence, context or {})
            
            # Create belief update record
            update = BeliefUpdate(
                id=f"update_{int(time.time() * 1000)}",
                timestamp=datetime.now(),
                belief_id=belief_id,
                old_confidence=current_confidence,
                new_confidence=new_confidence,
                reinforcement_type=reinforcement_type,
                evidence=evidence,
                context=context or {},
                learning_outcome=outcome,
                resolution_method=self._get_resolution_method(reinforcement_type),
                effectiveness_score=self._calculate_effectiveness(current_confidence, new_confidence, evidence)
            )
            
            # Update tracking
            self.belief_confidence[belief_id] = new_confidence
            self.belief_updates.append(update)
            
            if reinforcement_type == BeliefReinforcement.POSITIVE:
                self.belief_evidence_counts[belief_id] = self.belief_evidence_counts.get(belief_id, 0) + 1
            elif reinforcement_type == BeliefReinforcement.NEGATIVE:
                self.belief_contradiction_counts[belief_id] = self.belief_contradiction_counts.get(belief_id, 0) + 1
            
            print(f"[BeliefReinforcement] 🔄 Belief {belief_id} confidence: {current_confidence:.3f} → {new_confidence:.3f} ({reinforcement_type.value})")
            
            # Detect patterns
            self._detect_reinforcement_patterns()
            
            # Save periodically
            if len(self.belief_updates) % 10 == 0:
                self._save_reinforcement_data()
            
            return update
            
        except Exception as e:
            print(f"[BeliefReinforcement] ❌ Error reinforcing belief: {e}")
            return None
    
    def resolve_contradiction(self, contradiction_description: str, conflicting_beliefs: List[str],
                            resolution_strategy: str = "synthesis") -> ContradictionResolution:
        """Attempt to resolve a contradiction between beliefs"""
        if not self.running:
            return None
            
        start_time = time.time()
        
        try:
            print(f"[BeliefReinforcement] ⚖️ Attempting to resolve contradiction: {contradiction_description[:50]}...")
            
            # Attempt resolution using specified strategy
            resolution_result = self._attempt_resolution(
                contradiction_description, conflicting_beliefs, resolution_strategy
            )
            
            # Calculate time taken
            resolution_time = time.time() - start_time
            
            # Create resolution record
            resolution = ContradictionResolution(
                id=f"resolution_{int(time.time() * 1000)}",
                timestamp=datetime.now(),
                contradiction_description=contradiction_description,
                conflicting_beliefs=conflicting_beliefs,
                resolution_strategy=resolution_strategy,
                outcome=resolution_result["outcome"],
                new_synthesis=resolution_result.get("synthesis"),
                confidence_adjustments=resolution_result.get("confidence_adjustments", {}),
                learning_insights=resolution_result.get("insights", []),
                time_to_resolve=resolution_time,
                complexity_score=self._assess_contradiction_complexity(conflicting_beliefs)
            )
            
            # Apply confidence adjustments
            for belief_id, adjustment in resolution_result.get("confidence_adjustments", {}).items():
                current_confidence = self.belief_confidence.get(belief_id, 0.5)
                new_confidence = max(self.min_confidence, 
                                   min(self.max_confidence, current_confidence + adjustment))
                self.belief_confidence[belief_id] = new_confidence
            
            self.contradiction_resolutions.append(resolution)
            
            print(f"[BeliefReinforcement] ✅ Contradiction resolution: {resolution.outcome.value} in {resolution_time:.2f}s")
            
            return resolution
            
        except Exception as e:
            print(f"[BeliefReinforcement] ❌ Error resolving contradiction: {e}")
            return None
    
    def get_belief_confidence(self, belief_id: str) -> float:
        """Get current confidence in a belief"""
        return self.belief_confidence.get(belief_id, 0.5)
    
    def get_belief_statistics(self, belief_id: str) -> Dict[str, Any]:
        """Get comprehensive statistics for a belief"""
        updates = [u for u in self.belief_updates if u.belief_id == belief_id]
        
        if not updates:
            return {"error": "No updates found for belief"}
        
        reinforcement_counts = {}
        for update in updates:
            reinforcement_counts[update.reinforcement_type.value] = reinforcement_counts.get(update.reinforcement_type.value, 0) + 1
        
        return {
            "current_confidence": self.belief_confidence.get(belief_id, 0.5),
            "total_updates": len(updates),
            "evidence_count": self.belief_evidence_counts.get(belief_id, 0),
            "contradiction_count": self.belief_contradiction_counts.get(belief_id, 0),
            "reinforcement_breakdown": reinforcement_counts,
            "average_effectiveness": sum(u.effectiveness_score for u in updates) / len(updates),
            "confidence_trend": [u.new_confidence for u in updates[-10:]],  # Last 10 updates
            "last_updated": updates[-1].timestamp.isoformat() if updates else None
        }
    
    def get_learning_insights(self) -> List[str]:
        """Get insights learned from belief reinforcement and contradiction resolution"""
        insights = []
        
        # Insights from successful resolutions
        successful_resolutions = [r for r in self.contradiction_resolutions if r.outcome == LearningOutcome.SUCCESS]
        if successful_resolutions:
            avg_time = sum(r.time_to_resolve for r in successful_resolutions) / len(successful_resolutions)
            insights.append(f"Successfully resolved {len(successful_resolutions)} contradictions with average time {avg_time:.1f}s")
        
        # Insights from belief patterns
        if self.belief_patterns:
            most_common_pattern = max(self.belief_patterns, key=lambda p: p.success_rate)
            insights.append(f"Most effective belief reinforcement pattern: {most_common_pattern.pattern_id}")
        
        # Insights from confidence changes
        high_confidence_beliefs = [bid for bid, conf in self.belief_confidence.items() if conf > 0.8]
        low_confidence_beliefs = [bid for bid, conf in self.belief_confidence.items() if conf < 0.3]
        
        if high_confidence_beliefs:
            insights.append(f"High confidence in {len(high_confidence_beliefs)} beliefs")
        if low_confidence_beliefs:
            insights.append(f"Low confidence in {len(low_confidence_beliefs)} beliefs - may need revision")
        
        # Recent learning insights from resolutions
        recent_resolutions = [r for r in self.contradiction_resolutions[-5:] if r.learning_insights]
        for resolution in recent_resolutions:
            insights.extend(resolution.learning_insights[:2])  # Top 2 insights
        
        return insights[:10]  # Return top 10 insights
    
    def _calculate_new_confidence(self, current_confidence: float, reinforcement_type: BeliefReinforcement, evidence_count: int) -> float:
        """Calculate new confidence level based on reinforcement"""
        base_adjustment = self.confidence_adjustment_rate * (1 + evidence_count * 0.1)
        
        if reinforcement_type == BeliefReinforcement.POSITIVE:
            # Positive reinforcement increases confidence
            adjustment = base_adjustment * (1 - current_confidence)  # Diminishing returns
        elif reinforcement_type == BeliefReinforcement.NEGATIVE:
            # Negative reinforcement decreases confidence
            adjustment = -base_adjustment * current_confidence  # Proportional to current confidence
        elif reinforcement_type == BeliefReinforcement.CONTEXTUAL:
            # Contextual reinforcement moderates confidence
            adjustment = base_adjustment * 0.5 * (0.6 - current_confidence)  # Moves toward moderate confidence
        else:  # NEUTRAL
            # Neutral reinforcement has minimal impact
            adjustment = base_adjustment * 0.1 * (0.5 - current_confidence)  # Slight move toward 0.5
        
        new_confidence = current_confidence + adjustment
        return max(self.min_confidence, min(self.max_confidence, new_confidence))
    
    def _assess_learning_outcome(self, reinforcement_type: BeliefReinforcement, evidence: List[str], context: Dict[str, Any]) -> LearningOutcome:
        """Assess the outcome of a learning attempt"""
        evidence_quality = len([e for e in evidence if len(e) > 20])  # Quality based on detail
        
        if reinforcement_type == BeliefReinforcement.POSITIVE and evidence_quality >= 2:
            return LearningOutcome.SUCCESS
        elif reinforcement_type == BeliefReinforcement.NEGATIVE and evidence_quality >= 1:
            return LearningOutcome.PARTIAL_SUCCESS
        elif reinforcement_type == BeliefReinforcement.CONTEXTUAL:
            return LearningOutcome.COMPLEXITY_REVEALED
        elif evidence_quality == 0:
            return LearningOutcome.FAILURE
        else:
            return LearningOutcome.PARTIAL_SUCCESS
    
    def _get_resolution_method(self, reinforcement_type: BeliefReinforcement) -> str:
        """Get the resolution method used for this reinforcement type"""
        methods = {
            BeliefReinforcement.POSITIVE: "evidence_accumulation",
            BeliefReinforcement.NEGATIVE: "contradiction_analysis",
            BeliefReinforcement.CONTEXTUAL: "context_differentiation",
            BeliefReinforcement.NEUTRAL: "suspended_judgment"
        }
        return methods.get(reinforcement_type, "unknown")
    
    def _calculate_effectiveness(self, old_confidence: float, new_confidence: float, evidence: List[str]) -> float:
        """Calculate the effectiveness of a belief update"""
        confidence_change = abs(new_confidence - old_confidence)
        evidence_quality = min(1.0, len(evidence) / 3.0)  # Quality based on evidence count
        
        # Effectiveness is higher when confidence change is appropriate and evidence is strong
        effectiveness = (confidence_change * 2 + evidence_quality) / 3
        return min(1.0, effectiveness)
    
    def _attempt_resolution(self, contradiction_description: str, conflicting_beliefs: List[str], strategy: str) -> Dict[str, Any]:
        """Attempt to resolve a contradiction using the specified strategy"""
        
        if strategy == "synthesis":
            return self._synthesis_resolution(contradiction_description, conflicting_beliefs)
        elif strategy == "context_separation":
            return self._context_separation_resolution(contradiction_description, conflicting_beliefs)
        elif strategy == "evidence_evaluation":
            return self._evidence_evaluation_resolution(contradiction_description, conflicting_beliefs)
        elif strategy == "hierarchy_establishment":
            return self._hierarchy_resolution(contradiction_description, conflicting_beliefs)
        else:
            return self._default_resolution(contradiction_description, conflicting_beliefs)
    
    def _synthesis_resolution(self, contradiction: str, beliefs: List[str]) -> Dict[str, Any]:
        """Attempt to synthesize conflicting beliefs into a higher-order understanding"""
        synthesis_templates = [
            "Both beliefs are true in different contexts",
            "The beliefs represent different aspects of a more complex truth",
            "The contradiction reveals the need for a more nuanced understanding",
            "The beliefs operate at different levels of abstraction",
            "The apparent contradiction dissolves when viewed from a broader perspective"
        ]
        
        synthesis = random.choice(synthesis_templates)
        
        # Moderate confidence adjustments - synthesis doesn't eliminate beliefs but contextualizes them
        confidence_adjustments = {belief: -0.1 for belief in beliefs}  # Slight reduction in absolute confidence
        
        return {
            "outcome": LearningOutcome.SUCCESS,
            "synthesis": synthesis,
            "confidence_adjustments": confidence_adjustments,
            "insights": [
                "Synthesis approach reveals complexity rather than eliminating contradiction",
                "Multiple perspectives can coexist in a more sophisticated framework"
            ]
        }
    
    def _context_separation_resolution(self, contradiction: str, beliefs: List[str]) -> Dict[str, Any]:
        """Resolve by separating beliefs into different contextual domains"""
        contexts = ["professional", "personal", "theoretical", "practical", "short-term", "long-term"]
        assigned_contexts = random.sample(contexts, min(len(beliefs), len(contexts)))
        
        # Maintain confidence but add contextual qualifiers
        confidence_adjustments = {belief: 0.05 for belief in beliefs}  # Slight increase due to clarity
        
        return {
            "outcome": LearningOutcome.SUCCESS,
            "synthesis": f"Beliefs separated into contexts: {', '.join(assigned_contexts)}",
            "confidence_adjustments": confidence_adjustments,
            "insights": [
                "Context separation resolves apparent contradictions",
                "Different domains can have different rules and truths"
            ]
        }
    
    def _evidence_evaluation_resolution(self, contradiction: str, beliefs: List[str]) -> Dict[str, Any]:
        """Resolve by evaluating the strength of evidence for each belief"""
        # Simulate evidence evaluation
        evidence_strengths = [random.uniform(0.2, 0.9) for _ in beliefs]
        strongest_belief = beliefs[evidence_strengths.index(max(evidence_strengths))]
        
        # Adjust confidence based on evidence strength
        confidence_adjustments = {}
        for i, belief in enumerate(beliefs):
            strength = evidence_strengths[i]
            if belief == strongest_belief:
                confidence_adjustments[belief] = 0.2 * strength
            else:
                confidence_adjustments[belief] = -0.1 * (1 - strength)
        
        return {
            "outcome": LearningOutcome.PARTIAL_SUCCESS,
            "synthesis": f"Evidence evaluation favors: {strongest_belief}",
            "confidence_adjustments": confidence_adjustments,
            "insights": [
                "Evidence-based resolution provides clearer direction",
                "Some beliefs have stronger empirical support than others"
            ]
        }
    
    def _hierarchy_resolution(self, contradiction: str, beliefs: List[str]) -> Dict[str, Any]:
        """Resolve by establishing a hierarchy of beliefs"""
        # Assign importance levels
        importance_levels = ["fundamental", "important", "moderate", "minor"]
        belief_hierarchy = dict(zip(beliefs, importance_levels[:len(beliefs)]))
        
        # Adjust confidence based on hierarchy
        hierarchy_multipliers = {"fundamental": 0.3, "important": 0.1, "moderate": 0.0, "minor": -0.1}
        confidence_adjustments = {
            belief: hierarchy_multipliers.get(level, 0.0) 
            for belief, level in belief_hierarchy.items()
        }
        
        return {
            "outcome": LearningOutcome.SUCCESS,
            "synthesis": f"Belief hierarchy established: {belief_hierarchy}",
            "confidence_adjustments": confidence_adjustments,
            "insights": [
                "Hierarchical organization resolves conflicts between beliefs",
                "Core beliefs take precedence over peripheral ones"
            ]
        }
    
    def _default_resolution(self, contradiction: str, beliefs: List[str]) -> Dict[str, Any]:
        """Default resolution when other strategies don't apply"""
        return {
            "outcome": LearningOutcome.DEFERRED,
            "synthesis": "Contradiction requires further analysis",
            "confidence_adjustments": {belief: -0.05 for belief in beliefs},  # Slight decrease due to uncertainty
            "insights": [
                "Some contradictions require more information to resolve",
                "Deferring judgment is sometimes the wisest approach"
            ]
        }
    
    def _assess_contradiction_complexity(self, conflicting_beliefs: List[str]) -> float:
        """Assess the complexity of a contradiction"""
        # Complexity based on number of beliefs and their content
        base_complexity = len(conflicting_beliefs) / 5.0  # Normalize to 0-1 range
        
        # Add complexity based on content (simplified heuristic)
        content_complexity = 0.0
        for belief in conflicting_beliefs:
            if len(belief) > 100:  # Long, detailed beliefs are more complex
                content_complexity += 0.2
            if any(word in belief.lower() for word in ["context", "depends", "sometimes", "usually"]):
                content_complexity += 0.1  # Nuanced beliefs are more complex
        
        total_complexity = min(1.0, base_complexity + content_complexity)
        return total_complexity
    
    def _detect_reinforcement_patterns(self):
        """Detect patterns in belief reinforcement"""
        if len(self.belief_updates) < self.pattern_detection_threshold:
            return
        
        # Simple pattern detection - could be enhanced with more sophisticated analysis
        recent_updates = self.belief_updates[-20:]  # Look at recent updates
        
        # Group by reinforcement type
        type_groups = {}
        for update in recent_updates:
            reinforcement_type = update.reinforcement_type
            if reinforcement_type not in type_groups:
                type_groups[reinforcement_type] = []
            type_groups[reinforcement_type].append(update)
        
        # Detect patterns in effectiveness
        for reinforcement_type, updates in type_groups.items():
            if len(updates) >= 3:  # Minimum for pattern detection
                avg_effectiveness = sum(u.effectiveness_score for u in updates) / len(updates)
                
                # Create or update pattern
                pattern_id = f"pattern_{reinforcement_type.value}_{len(self.belief_patterns)}"
                
                pattern = BeliefPattern(
                    pattern_id=pattern_id,
                    belief_categories=list(set(u.belief_id.split('_')[0] for u in updates if '_' in u.belief_id)),
                    common_reinforcement_types=[reinforcement_type],
                    typical_confidence_changes=[u.new_confidence - u.old_confidence for u in updates],
                    success_rate=avg_effectiveness,
                    context_factors=list(set(u.context.get('context_type', 'unknown') for u in updates if u.context)),
                    last_observed=datetime.now()
                )
                
                # Only add if it's significantly different from existing patterns
                if not any(p.pattern_id.startswith(f"pattern_{reinforcement_type.value}") for p in self.belief_patterns):
                    self.belief_patterns.append(pattern)
    
    def _save_reinforcement_data(self):
        """Save belief reinforcement data to file"""
        try:
            data = {
                "belief_updates": [asdict(update) for update in self.belief_updates],
                "contradiction_resolutions": [asdict(resolution) for resolution in self.contradiction_resolutions],
                "belief_patterns": [asdict(pattern) for pattern in self.belief_patterns],
                "belief_confidence": self.belief_confidence,
                "belief_evidence_counts": self.belief_evidence_counts,
                "belief_contradiction_counts": self.belief_contradiction_counts,
                "statistics": {
                    "total_updates": len(self.belief_updates),
                    "total_resolutions": len(self.contradiction_resolutions),
                    "successful_resolutions": len([r for r in self.contradiction_resolutions if r.outcome == LearningOutcome.SUCCESS]),
                    "average_confidence": sum(self.belief_confidence.values()) / max(1, len(self.belief_confidence)),
                    "patterns_detected": len(self.belief_patterns)
                },
                "last_updated": datetime.now().isoformat()
            }
            
            with open(self.save_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
                
        except Exception as e:
            print(f"[BeliefReinforcement] ❌ Error saving reinforcement data: {e}")
    
    def _load_reinforcement_data(self):
        """Load belief reinforcement data from file"""
        try:
            if os.path.exists(self.save_path):
                with open(self.save_path, 'r') as f:
                    data = json.load(f)
                
                # Load belief updates
                for update_data in data.get("belief_updates", []):
                    update_data["timestamp"] = datetime.fromisoformat(update_data["timestamp"])
                    update_data["reinforcement_type"] = BeliefReinforcement(update_data["reinforcement_type"])
                    update_data["learning_outcome"] = LearningOutcome(update_data["learning_outcome"])
                    self.belief_updates.append(BeliefUpdate(**update_data))
                
                # Load contradiction resolutions
                for resolution_data in data.get("contradiction_resolutions", []):
                    resolution_data["timestamp"] = datetime.fromisoformat(resolution_data["timestamp"])
                    resolution_data["outcome"] = LearningOutcome(resolution_data["outcome"])
                    self.contradiction_resolutions.append(ContradictionResolution(**resolution_data))
                
                # Load patterns
                for pattern_data in data.get("belief_patterns", []):
                    pattern_data["last_observed"] = datetime.fromisoformat(pattern_data["last_observed"])
                    pattern_data["common_reinforcement_types"] = [
                        BeliefReinforcement(rt) for rt in pattern_data["common_reinforcement_types"]
                    ]
                    self.belief_patterns.append(BeliefPattern(**pattern_data))
                
                # Load tracking data
                self.belief_confidence = data.get("belief_confidence", {})
                self.belief_evidence_counts = data.get("belief_evidence_counts", {})
                self.belief_contradiction_counts = data.get("belief_contradiction_counts", {})
                
                print(f"[BeliefReinforcement] ✅ Loaded reinforcement data with {len(self.belief_updates)} updates")
                
        except Exception as e:
            print(f"[BeliefReinforcement] ❌ Error loading reinforcement data: {e}")

# Global instance
belief_reinforcement = BeliefReinforcementSystem()