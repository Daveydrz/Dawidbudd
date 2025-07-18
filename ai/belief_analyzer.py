"""
belief_analyzer.py - Belief contradiction detection and consistency management

This module analyzes user statements and AI responses for belief contradictions,
maintaining consistency in the consciousness model and flagging potential conflicts
in memory or personality representation.
"""

import json
import re
from typing import Dict, List, Tuple, Any, Optional, Set
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

class ContradictionSeverity(Enum):
    """Severity levels for belief contradictions"""
    MINOR = "minor"           # Small inconsistencies, preference changes
    MODERATE = "moderate"     # Notable contradictions, should be addressed
    MAJOR = "major"          # Significant conflicts requiring intervention
    CRITICAL = "critical"    # Fundamental belief conflicts, potential error

class BeliefType(Enum):
    """Types of beliefs that can be tracked"""
    PERSONAL_FACT = "personal_fact"           # Name, age, location, etc.
    PREFERENCE = "preference"                 # Likes, dislikes, opinions
    RELATIONSHIP = "relationship"             # Family, friends, work
    EXPERIENCE = "experience"                 # Past events, memories
    CAPABILITY = "capability"                 # Skills, abilities, limitations
    TEMPORAL = "temporal"                     # Time-based facts, schedules
    EMOTIONAL = "emotional"                   # Emotional states, reactions
    GOAL = "goal"                            # Aspirations, objectives
    BELIEF_SYSTEM = "belief_system"          # Values, worldview, ethics

@dataclass
class Belief:
    """Represents a single belief or fact"""
    id: str
    content: str
    belief_type: BeliefType
    confidence: float           # 0.0 to 1.0
    source: str                # Where the belief came from
    timestamp: datetime
    user_id: str
    context: Dict[str, Any]
    contradictions: List[str] = None  # IDs of contradicting beliefs
    
    def __post_init__(self):
        if self.contradictions is None:
            self.contradictions = []

@dataclass
class Contradiction:
    """Represents a detected contradiction between beliefs"""
    id: str
    belief1_id: str
    belief2_id: str
    severity: ContradictionSeverity
    description: str
    timestamp: datetime
    resolved: bool = False
    resolution_strategy: str = None

class BeliefAnalyzer:
    """Main class for belief contradiction detection"""
    
    def __init__(self):
        self.beliefs: Dict[str, Belief] = {}
        self.contradictions: Dict[str, Contradiction] = {}
        self.user_belief_profiles: Dict[str, Set[str]] = {}  # user_id -> belief_ids
        
        # Load existing beliefs if available
        self._load_beliefs()
    
    def _generate_belief_id(self, content: str, user_id: str) -> str:
        """Generate a unique ID for a belief"""
        import hashlib
        content_hash = hashlib.md5(f"{user_id}:{content}".encode()).hexdigest()[:8]
        return f"belief_{user_id}_{content_hash}"
    
    def _generate_contradiction_id(self, belief1_id: str, belief2_id: str) -> str:
        """Generate a unique ID for a contradiction"""
        import hashlib
        pair_hash = hashlib.md5(f"{belief1_id}:{belief2_id}".encode()).hexdigest()[:8]
        return f"contradiction_{pair_hash}"
    
    def extract_beliefs_from_text(self, text: str, user_id: str, source: str = "conversation") -> List[Belief]:
        """Extract potential beliefs from user text"""
        beliefs = []
        
        # Personal facts patterns
        personal_patterns = [
            (r"my name is (\w+)", BeliefType.PERSONAL_FACT, 0.9),
            (r"i am (\d+) years old", BeliefType.PERSONAL_FACT, 0.9),
            (r"i live in ([^,.]+)", BeliefType.PERSONAL_FACT, 0.8),
            (r"i work as a ([^,.]+)", BeliefType.PERSONAL_FACT, 0.8),
            (r"i am a ([^,.]+)", BeliefType.PERSONAL_FACT, 0.7),
        ]
        
        # Preference patterns
        preference_patterns = [
            (r"i (love|hate|like|dislike|enjoy|prefer) ([^,.]+)", BeliefType.PREFERENCE, 0.8),
            (r"i don't like ([^,.]+)", BeliefType.PREFERENCE, 0.8),
            (r"my favorite ([^,]+) is ([^,.]+)", BeliefType.PREFERENCE, 0.9),
        ]
        
        # Relationship patterns
        relationship_patterns = [
            (r"my (wife|husband|partner|boyfriend|girlfriend) is ([^,.]+)", BeliefType.RELATIONSHIP, 0.9),
            (r"my (mother|father|mom|dad|parent) is ([^,.]+)", BeliefType.RELATIONSHIP, 0.9),
            (r"i have a (son|daughter|child) named ([^,.]+)", BeliefType.RELATIONSHIP, 0.9),
            (r"i am (married|single|divorced)", BeliefType.RELATIONSHIP, 0.8),
        ]
        
        # Experience patterns
        experience_patterns = [
            (r"i (went|visited|traveled) to ([^,.]+)", BeliefType.EXPERIENCE, 0.7),
            (r"i (graduated|studied) at ([^,.]+)", BeliefType.EXPERIENCE, 0.8),
            (r"i used to ([^,.]+)", BeliefType.EXPERIENCE, 0.6),
            (r"last (week|month|year) i ([^,.]+)", BeliefType.EXPERIENCE, 0.7),
        ]
        
        # Goal patterns
        goal_patterns = [
            (r"i want to ([^,.]+)", BeliefType.GOAL, 0.7),
            (r"i plan to ([^,.]+)", BeliefType.GOAL, 0.8),
            (r"my goal is to ([^,.]+)", BeliefType.GOAL, 0.9),
            (r"i hope to ([^,.]+)", BeliefType.GOAL, 0.6),
        ]
        
        all_patterns = (personal_patterns + preference_patterns + 
                       relationship_patterns + experience_patterns + goal_patterns)
        
        text_lower = text.lower()
        
        for pattern, belief_type, confidence in all_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                content = match.group(0)
                belief_id = self._generate_belief_id(content, user_id)
                
                belief = Belief(
                    id=belief_id,
                    content=content,
                    belief_type=belief_type,
                    confidence=confidence,
                    source=source,
                    timestamp=datetime.now(),
                    user_id=user_id,
                    context={"original_text": text, "pattern": pattern}
                )
                
                beliefs.append(belief)
        
        return beliefs
    
    def add_belief(self, belief: Belief) -> bool:
        """Add a belief and check for contradictions"""
        # Check if belief already exists
        if belief.id in self.beliefs:
            existing = self.beliefs[belief.id]
            # Update confidence if this is more recent/confident
            if belief.confidence > existing.confidence or belief.timestamp > existing.timestamp:
                self.beliefs[belief.id] = belief
            return True
        
        # Add new belief
        self.beliefs[belief.id] = belief
        
        # Add to user profile
        if belief.user_id not in self.user_belief_profiles:
            self.user_belief_profiles[belief.user_id] = set()
        self.user_belief_profiles[belief.user_id].add(belief.id)
        
        # Check for contradictions with existing beliefs
        contradictions = self._check_contradictions(belief)
        
        # Store any found contradictions
        for contradiction in contradictions:
            self.contradictions[contradiction.id] = contradiction
            
            # Update belief contradiction lists
            self.beliefs[contradiction.belief1_id].contradictions.append(contradiction.belief2_id)
            self.beliefs[contradiction.belief2_id].contradictions.append(contradiction.belief1_id)
        
        return len(contradictions) == 0  # Return True if no contradictions found
    
    def _check_contradictions(self, new_belief: Belief) -> List[Contradiction]:
        """Check for contradictions between new belief and existing beliefs"""
        contradictions = []
        
        # Only check against beliefs from the same user
        user_belief_ids = self.user_belief_profiles.get(new_belief.user_id, set())
        
        for existing_id in user_belief_ids:
            if existing_id == new_belief.id:
                continue
                
            existing_belief = self.beliefs[existing_id]
            
            # Check type-specific contradictions
            contradiction = self._detect_contradiction(new_belief, existing_belief)
            if contradiction:
                contradictions.append(contradiction)
        
        return contradictions
    
    def _detect_contradiction(self, belief1: Belief, belief2: Belief) -> Optional[Contradiction]:
        """Detect contradiction between two specific beliefs"""
        if belief1.belief_type != belief2.belief_type:
            return None  # Different types rarely contradict directly
        
        contradiction_rules = {
            BeliefType.PERSONAL_FACT: self._check_personal_fact_contradiction,
            BeliefType.PREFERENCE: self._check_preference_contradiction,
            BeliefType.RELATIONSHIP: self._check_relationship_contradiction,
            BeliefType.EXPERIENCE: self._check_experience_contradiction,
            BeliefType.GOAL: self._check_goal_contradiction,
        }
        
        checker = contradiction_rules.get(belief1.belief_type)
        if checker:
            return checker(belief1, belief2)
        
        return None
    
    def _check_personal_fact_contradiction(self, belief1: Belief, belief2: Belief) -> Optional[Contradiction]:
        """Check for contradictions in personal facts"""
        content1 = belief1.content.lower()
        content2 = belief2.content.lower()
        
        # Name contradictions
        if "my name is" in content1 and "my name is" in content2:
            name1 = re.search(r"my name is (\w+)", content1)
            name2 = re.search(r"my name is (\w+)", content2)
            if name1 and name2 and name1.group(1) != name2.group(1):
                return Contradiction(
                    id=self._generate_contradiction_id(belief1.id, belief2.id),
                    belief1_id=belief1.id,
                    belief2_id=belief2.id,
                    severity=ContradictionSeverity.MAJOR,
                    description=f"Name contradiction: {name1.group(1)} vs {name2.group(1)}",
                    timestamp=datetime.now()
                )
        
        # Age contradictions
        if "years old" in content1 and "years old" in content2:
            age1 = re.search(r"(\d+) years old", content1)
            age2 = re.search(r"(\d+) years old", content2)
            if age1 and age2:
                age_diff = abs(int(age1.group(1)) - int(age2.group(1)))
                time_diff = abs((belief1.timestamp - belief2.timestamp).days)
                expected_diff = time_diff / 365  # Expected age difference based on time
                
                if age_diff > expected_diff + 1:  # Allow for 1 year variance
                    severity = ContradictionSeverity.MAJOR if age_diff > 5 else ContradictionSeverity.MODERATE
                    return Contradiction(
                        id=self._generate_contradiction_id(belief1.id, belief2.id),
                        belief1_id=belief1.id,
                        belief2_id=belief2.id,
                        severity=severity,
                        description=f"Age contradiction: {age1.group(1)} vs {age2.group(1)}",
                        timestamp=datetime.now()
                    )
        
        # Location contradictions
        if "i live in" in content1 and "i live in" in content2:
            loc1 = re.search(r"i live in ([^,.]+)", content1)
            loc2 = re.search(r"i live in ([^,.]+)", content2)
            if loc1 and loc2 and loc1.group(1).strip() != loc2.group(1).strip():
                return Contradiction(
                    id=self._generate_contradiction_id(belief1.id, belief2.id),
                    belief1_id=belief1.id,
                    belief2_id=belief2.id,
                    severity=ContradictionSeverity.MODERATE,
                    description=f"Location contradiction: {loc1.group(1)} vs {loc2.group(1)}",
                    timestamp=datetime.now()
                )
        
        return None
    
    def _check_preference_contradiction(self, belief1: Belief, belief2: Belief) -> Optional[Contradiction]:
        """Check for contradictions in preferences"""
        content1 = belief1.content.lower()
        content2 = belief2.content.lower()
        
        # Extract preference subject
        def extract_preference_subject(content):
            patterns = [
                r"i (love|like|enjoy) ([^,.]+)",
                r"i (hate|dislike) ([^,.]+)",
                r"my favorite [^,]+ is ([^,.]+)"
            ]
            for pattern in patterns:
                match = re.search(pattern, content)
                if match:
                    return match.groups()[-1].strip()  # Get the subject
            return None
        
        subj1 = extract_preference_subject(content1)
        subj2 = extract_preference_subject(content2)
        
        if subj1 and subj2 and subj1 == subj2:
            # Same subject, check if sentiments conflict
            positive_words = ["love", "like", "enjoy", "prefer"]
            negative_words = ["hate", "dislike"]
            
            sent1 = any(word in content1 for word in positive_words)
            sent2 = any(word in content2 for word in positive_words)
            neg1 = any(word in content1 for word in negative_words)
            neg2 = any(word in content2 for word in negative_words)
            
            if (sent1 and neg2) or (neg1 and sent2):
                return Contradiction(
                    id=self._generate_contradiction_id(belief1.id, belief2.id),
                    belief1_id=belief1.id,
                    belief2_id=belief2.id,
                    severity=ContradictionSeverity.MINOR,  # Preferences can change
                    description=f"Preference contradiction about {subj1}",
                    timestamp=datetime.now()
                )
        
        return None
    
    def _check_relationship_contradiction(self, belief1: Belief, belief2: Belief) -> Optional[Contradiction]:
        """Check for contradictions in relationships"""
        content1 = belief1.content.lower()
        content2 = belief2.content.lower()
        
        # Marital status contradictions
        marital_states = ["married", "single", "divorced"]
        state1 = next((state for state in marital_states if state in content1), None)
        state2 = next((state for state in marital_states if state in content2), None)
        
        if state1 and state2 and state1 != state2:
            # Check time difference - marital status can change
            time_diff = abs((belief1.timestamp - belief2.timestamp).days)
            if time_diff < 30:  # If within a month, likely contradiction
                return Contradiction(
                    id=self._generate_contradiction_id(belief1.id, belief2.id),
                    belief1_id=belief1.id,
                    belief2_id=belief2.id,
                    severity=ContradictionSeverity.MODERATE,
                    description=f"Marital status contradiction: {state1} vs {state2}",
                    timestamp=datetime.now()
                )
        
        return None
    
    def _check_experience_contradiction(self, belief1: Belief, belief2: Belief) -> Optional[Contradiction]:
        """Check for contradictions in experiences"""
        # Experiences rarely contradict unless they're mutually exclusive
        # For now, just flag if same event described differently
        return None
    
    def _check_goal_contradiction(self, belief1: Belief, belief2: Belief) -> Optional[Contradiction]:
        """Check for contradictions in goals"""
        # Goals can change or be contradictory, flag as minor
        return None
    
    def get_contradictions_for_user(self, user_id: str, severity: ContradictionSeverity = None) -> List[Contradiction]:
        """Get all contradictions for a specific user"""
        result = []
        
        user_belief_ids = self.user_belief_profiles.get(user_id, set())
        
        for contradiction in self.contradictions.values():
            if not contradiction.resolved:
                if (contradiction.belief1_id in user_belief_ids or 
                    contradiction.belief2_id in user_belief_ids):
                    if severity is None or contradiction.severity == severity:
                        result.append(contradiction)
        
        return result
    
    def resolve_contradiction(self, contradiction_id: str, strategy: str = "newer_wins") -> bool:
        """Resolve a contradiction using specified strategy"""
        if contradiction_id not in self.contradictions:
            return False
        
        contradiction = self.contradictions[contradiction_id]
        belief1 = self.beliefs[contradiction.belief1_id]
        belief2 = self.beliefs[contradiction.belief2_id]
        
        if strategy == "newer_wins":
            # Keep the newer belief, mark older as resolved
            if belief1.timestamp > belief2.timestamp:
                winning_belief = belief1
                losing_belief = belief2
            else:
                winning_belief = belief2
                losing_belief = belief1
            
            # Lower confidence of losing belief
            losing_belief.confidence *= 0.5
            contradiction.resolved = True
            contradiction.resolution_strategy = strategy
            
        elif strategy == "higher_confidence":
            # Keep the belief with higher confidence
            if belief1.confidence > belief2.confidence:
                winning_belief = belief1
                losing_belief = belief2
            else:
                winning_belief = belief2
                losing_belief = belief1
            
            losing_belief.confidence *= 0.3
            contradiction.resolved = True
            contradiction.resolution_strategy = strategy
        
        elif strategy == "manual_review":
            # Mark for manual review but don't auto-resolve
            contradiction.resolution_strategy = "pending_manual_review"
            return False
        
        return True
    
    def analyze_memory_update(self, memory_content: str, user_id: str) -> Dict[str, Any]:
        """Analyze a memory update for potential contradictions"""
        # Extract beliefs from the memory content
        new_beliefs = self.extract_beliefs_from_text(memory_content, user_id, "memory_update")
        
        analysis = {
            "new_beliefs_found": len(new_beliefs),
            "contradictions_detected": [],
            "severity_summary": {
                "critical": 0,
                "major": 0,
                "moderate": 0,
                "minor": 0
            },
            "recommended_actions": []
        }
        
        # Process each new belief
        for belief in new_beliefs:
            success = self.add_belief(belief)
            if not success:
                # Get contradictions for this belief
                belief_contradictions = [
                    c for c in self.contradictions.values() 
                    if c.belief1_id == belief.id or c.belief2_id == belief.id
                ]
                
                for contradiction in belief_contradictions:
                    analysis["contradictions_detected"].append({
                        "id": contradiction.id,
                        "severity": contradiction.severity.value,
                        "description": contradiction.description,
                        "belief1": self.beliefs[contradiction.belief1_id].content,
                        "belief2": self.beliefs[contradiction.belief2_id].content
                    })
                    
                    analysis["severity_summary"][contradiction.severity.value] += 1
        
        # Generate recommendations
        if analysis["severity_summary"]["critical"] > 0:
            analysis["recommended_actions"].append("IMMEDIATE: Review critical contradictions")
        if analysis["severity_summary"]["major"] > 0:
            analysis["recommended_actions"].append("HIGH: Address major belief conflicts")
        if analysis["severity_summary"]["moderate"] > 0:
            analysis["recommended_actions"].append("MEDIUM: Resolve moderate inconsistencies")
        
        return analysis
    
    def get_belief_summary_for_user(self, user_id: str) -> Dict[str, Any]:
        """Get a summary of beliefs for a user"""
        user_belief_ids = self.user_belief_profiles.get(user_id, set())
        beliefs = [self.beliefs[bid] for bid in user_belief_ids]
        
        summary = {
            "total_beliefs": len(beliefs),
            "by_type": {},
            "confidence_distribution": {
                "high": 0,    # > 0.8
                "medium": 0,  # 0.5 - 0.8
                "low": 0      # < 0.5
            },
            "recent_beliefs": [],
            "contradictions": len(self.get_contradictions_for_user(user_id))
        }
        
        for belief in beliefs:
            # Count by type
            belief_type = belief.belief_type.value
            summary["by_type"][belief_type] = summary["by_type"].get(belief_type, 0) + 1
            
            # Confidence distribution
            if belief.confidence > 0.8:
                summary["confidence_distribution"]["high"] += 1
            elif belief.confidence > 0.5:
                summary["confidence_distribution"]["medium"] += 1
            else:
                summary["confidence_distribution"]["low"] += 1
        
        # Recent beliefs (last 7 days)
        recent_cutoff = datetime.now() - timedelta(days=7)
        recent_beliefs = [b for b in beliefs if b.timestamp > recent_cutoff]
        summary["recent_beliefs"] = [
            {"content": b.content, "type": b.belief_type.value, "confidence": b.confidence}
            for b in sorted(recent_beliefs, key=lambda x: x.timestamp, reverse=True)[:5]
        ]
        
        return summary
    
    def _save_beliefs(self):
        """Save beliefs to persistent storage"""
        try:
            # Convert beliefs to serializable format
            beliefs_data = {}
            for belief_id, belief in self.beliefs.items():
                beliefs_data[belief_id] = {
                    "id": belief.id,
                    "content": belief.content,
                    "belief_type": belief.belief_type.value,
                    "confidence": belief.confidence,
                    "source": belief.source,
                    "timestamp": belief.timestamp.isoformat(),
                    "user_id": belief.user_id,
                    "context": belief.context,
                    "contradictions": belief.contradictions
                }
            
            # Convert contradictions to serializable format
            contradictions_data = {}
            for cont_id, contradiction in self.contradictions.items():
                contradictions_data[cont_id] = {
                    "id": contradiction.id,
                    "belief1_id": contradiction.belief1_id,
                    "belief2_id": contradiction.belief2_id,
                    "severity": contradiction.severity.value,
                    "description": contradiction.description,
                    "timestamp": contradiction.timestamp.isoformat(),
                    "resolved": contradiction.resolved,
                    "resolution_strategy": contradiction.resolution_strategy
                }
            
            # Convert user profiles
            user_profiles_data = {}
            for user_id, belief_ids in self.user_belief_profiles.items():
                user_profiles_data[user_id] = list(belief_ids)
            
            # Save to file
            data = {
                "beliefs": beliefs_data,
                "contradictions": contradictions_data,
                "user_profiles": user_profiles_data,
                "last_saved": datetime.now().isoformat()
            }
            
            with open("belief_memory.json", "w") as f:
                json.dump(data, f, indent=2)
                
            print(f"[BeliefAnalyzer] 💾 Saved {len(self.beliefs)} beliefs and {len(self.contradictions)} contradictions")
            
        except Exception as e:
            print(f"[BeliefAnalyzer] ❌ Error saving beliefs: {e}")
    
    def _load_beliefs(self):
        """Load beliefs from persistent storage"""
        try:
            with open("belief_memory.json", "r") as f:
                data = json.load(f)
            
            # Load beliefs
            for belief_id, belief_data in data.get("beliefs", {}).items():
                belief = Belief(
                    id=belief_data["id"],
                    content=belief_data["content"],
                    belief_type=BeliefType(belief_data["belief_type"]),
                    confidence=belief_data["confidence"],
                    source=belief_data["source"],
                    timestamp=datetime.fromisoformat(belief_data["timestamp"]),
                    user_id=belief_data["user_id"],
                    context=belief_data["context"],
                    contradictions=belief_data.get("contradictions", [])
                )
                self.beliefs[belief_id] = belief
            
            # Load contradictions
            for cont_id, cont_data in data.get("contradictions", {}).items():
                contradiction = Contradiction(
                    id=cont_data["id"],
                    belief1_id=cont_data["belief1_id"],
                    belief2_id=cont_data["belief2_id"],
                    severity=ContradictionSeverity(cont_data["severity"]),
                    description=cont_data["description"],
                    timestamp=datetime.fromisoformat(cont_data["timestamp"]),
                    resolved=cont_data.get("resolved", False),
                    resolution_strategy=cont_data.get("resolution_strategy")
                )
                self.contradictions[cont_id] = contradiction
            
            # Load user profiles
            for user_id, belief_ids in data.get("user_profiles", {}).items():
                self.user_belief_profiles[user_id] = set(belief_ids)
            
            print(f"[BeliefAnalyzer] 📚 Loaded {len(self.beliefs)} beliefs and {len(self.contradictions)} contradictions")
            
        except FileNotFoundError:
            print("[BeliefAnalyzer] 📝 No existing belief memory found, starting fresh")
        except Exception as e:
            print(f"[BeliefAnalyzer] ❌ Error loading beliefs: {e}")

# Global analyzer instance
belief_analyzer = BeliefAnalyzer()

# Convenience functions for integration
def analyze_user_input(text: str, user_id: str) -> Dict[str, Any]:
    """Analyze user input for belief contradictions"""
    return belief_analyzer.analyze_memory_update(text, user_id)

def get_user_contradictions(user_id: str, severity: str = None) -> List[Dict[str, Any]]:
    """Get contradictions for a user"""
    severity_enum = ContradictionSeverity(severity) if severity else None
    contradictions = belief_analyzer.get_contradictions_for_user(user_id, severity_enum)
    
    return [
        {
            "id": c.id,
            "severity": c.severity.value,
            "description": c.description,
            "belief1": belief_analyzer.beliefs[c.belief1_id].content,
            "belief2": belief_analyzer.beliefs[c.belief2_id].content,
            "resolved": c.resolved
        }
        for c in contradictions
    ]

def resolve_user_contradiction(contradiction_id: str, strategy: str = "newer_wins") -> bool:
    """Resolve a specific contradiction"""
    return belief_analyzer.resolve_contradiction(contradiction_id, strategy)

def get_user_belief_summary(user_id: str) -> Dict[str, Any]:
    """Get belief summary for a user"""
    return belief_analyzer.get_belief_summary_for_user(user_id)

def save_belief_state():
    """Save current belief state to disk"""
    belief_analyzer._save_beliefs()