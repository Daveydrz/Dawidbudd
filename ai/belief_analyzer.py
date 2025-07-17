"""
Belief Contradiction Detection System

This module analyzes user statements against stored beliefs and facts to detect
contradictions and enhance consciousness awareness of user consistency.
"""

import json
import logging
import re
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path

class ContradictionType(Enum):
    """Types of belief contradictions"""
    DIRECT = "direct"           # Direct contradiction (X vs not X)
    TEMPORAL = "temporal"       # Time-based contradiction (then vs now)
    LOGICAL = "logical"         # Logical inconsistency
    PREFERENCE = "preference"   # Preference contradiction (like vs dislike)
    FACTUAL = "factual"        # Factual contradiction
    EMOTIONAL = "emotional"     # Emotional state contradiction

class ContradictionSeverity(Enum):
    """Severity levels for contradictions"""
    CRITICAL = 5    # Fundamental contradiction requiring attention
    HIGH = 4        # Significant contradiction worth discussing
    MEDIUM = 3      # Moderate contradiction, mention if relevant
    LOW = 2         # Minor contradiction, note but don't emphasize
    NEGLIGIBLE = 1  # Very minor, just track

@dataclass
class BeliefStatement:
    """A stored belief or fact statement"""
    content: str
    confidence: float           # 0.0 to 1.0
    date_established: datetime
    last_mentioned: datetime
    source_context: str
    category: str              # "fact", "preference", "belief", "memory"
    emotional_weight: float    # How emotionally significant this is
    supporting_evidence: List[str] = field(default_factory=list)
    contradicting_evidence: List[str] = field(default_factory=list)
    tags: Set[str] = field(default_factory=set)

@dataclass
class ContradictionEvent:
    """A detected contradiction"""
    original_belief: BeliefStatement
    new_statement: str
    contradiction_type: ContradictionType
    severity: ContradictionSeverity
    confidence: float          # How confident we are this is a contradiction
    detected_at: datetime
    context: str
    explanation: str
    suggested_response: str

class BeliefAnalyzer:
    """
    Analyzes user statements for contradictions with stored beliefs and facts.
    Enhances consciousness awareness of user consistency and changes.
    """
    
    def __init__(self, belief_store_path: str = "belief_store.json"):
        self.belief_store_path = Path(belief_store_path)
        self.beliefs: Dict[str, BeliefStatement] = {}
        self.contradiction_history: List[ContradictionEvent] = []
        
        # Analysis patterns for different types of statements
        self.belief_patterns = {
            'factual': [
                r"my name is (\w+)",
                r"i am (\d+) years old",
                r"i live in ([^.]+)",
                r"i work (?:as|at) ([^.]+)",
                r"i am from ([^.]+)",
                r"i have (\d+) (?:child|children|kids)",
                r"i am (married|single|divorced|widowed)",
                r"my (\w+) is (\w+)"  # my job is X, my car is Y
            ],
            'preferences': [
                r"i (love|hate|like|dislike|enjoy|can't stand) ([^.]+)",
                r"i prefer ([^.]+) to ([^.]+)",
                r"my favorite ([^.]+) is ([^.]+)",
                r"i really (love|hate|like|dislike) ([^.]+)",
                r"i (always|never|usually|rarely) ([^.]+)"
            ],
            'beliefs': [
                r"i believe (?:that )?([^.]+)",
                r"i think (?:that )?([^.]+)",
                r"in my opinion[,]? ([^.]+)",
                r"i feel (?:that )?([^.]+) is ([^.]+)"
            ],
            'temporal': [
                r"i used to ([^.]+) but now i ([^.]+)",
                r"i no longer ([^.]+)",
                r"i stopped ([^.]+)",
                r"i started ([^.]+)",
                r"before i ([^.]+) but now i ([^.]+)"
            ],
            'emotional': [
                r"i feel ([^.]+) about ([^.]+)",
                r"([^.]+) makes? me (happy|sad|angry|excited|nervous|anxious)",
                r"i am (worried|excited|nervous|happy|sad) about ([^.]+)"
            ]
        }
        
        self.contradiction_indicators = {
            'direct_opposites': [
                ('love', 'hate'), ('like', 'dislike'), ('enjoy', "can't stand"),
                ('always', 'never'), ('yes', 'no'), ('true', 'false'),
                ('married', 'single'), ('have', "don't have")
            ],
            'temporal_markers': [
                'used to', 'no longer', 'stopped', 'started', 'before', 'now',
                'previously', 'currently', 'nowadays', 'these days'
            ],
            'uncertainty_words': [
                'maybe', 'perhaps', 'possibly', 'might', 'could', 'unsure',
                'not sure', 'don\'t know', 'uncertain'
            ]
        }
        
        self.load_beliefs()
        logging.info(f"[BeliefAnalyzer] 🧠 Belief analyzer initialized with {len(self.beliefs)} beliefs")
    
    def analyze_statement(self, statement: str, context: str = "") -> List[ContradictionEvent]:
        """
        Analyze a statement for contradictions with stored beliefs
        
        Args:
            statement: User's statement to analyze
            context: Additional context for the statement
            
        Returns:
            List of detected contradictions
        """
        contradictions = []
        statement_lower = statement.lower().strip()
        
        # Extract new beliefs/facts from the statement
        new_beliefs = self._extract_beliefs_from_statement(statement, context)
        
        # Check each new belief against existing beliefs
        for new_belief in new_beliefs:
            potential_contradictions = self._find_contradictions(new_belief, statement_lower)
            contradictions.extend(potential_contradictions)
        
        # Store new beliefs (even if they contradict existing ones)
        for new_belief in new_beliefs:
            self._store_belief(new_belief)
        
        # Record contradiction events
        for contradiction in contradictions:
            self.contradiction_history.append(contradiction)
        
        if contradictions:
            logging.info(f"[BeliefAnalyzer] ⚠️ Found {len(contradictions)} contradictions")
        
        return contradictions
    
    def _extract_beliefs_from_statement(self, statement: str, context: str) -> List[BeliefStatement]:
        """Extract belief statements from user input"""
        beliefs = []
        statement_lower = statement.lower().strip()
        
        # Check each pattern category
        for category, patterns in self.belief_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, statement_lower)
                for match in matches:
                    belief_content = match.group(0)
                    
                    # Determine confidence based on certainty markers
                    confidence = self._assess_statement_confidence(statement_lower)
                    
                    # Determine emotional weight
                    emotional_weight = self._assess_emotional_weight(belief_content, category)
                    
                    belief = BeliefStatement(
                        content=belief_content,
                        confidence=confidence,
                        date_established=datetime.now(),
                        last_mentioned=datetime.now(),
                        source_context=context or statement,
                        category=category,
                        emotional_weight=emotional_weight,
                        tags=self._extract_tags(belief_content, category)
                    )
                    
                    beliefs.append(belief)
        
        return beliefs
    
    def _find_contradictions(self, new_belief: BeliefStatement, full_statement: str) -> List[ContradictionEvent]:
        """Find contradictions between new belief and existing beliefs"""
        contradictions = []
        
        for belief_id, existing_belief in self.beliefs.items():
            contradiction = self._check_belief_contradiction(new_belief, existing_belief, full_statement)
            if contradiction:
                contradictions.append(contradiction)
        
        return contradictions
    
    def _check_belief_contradiction(self, new_belief: BeliefStatement, 
                                  existing_belief: BeliefStatement,
                                  full_statement: str) -> Optional[ContradictionEvent]:
        """Check if two beliefs contradict each other"""
        
        # Skip if beliefs are too different in category or subject
        if not self._beliefs_are_comparable(new_belief, existing_belief):
            return None
        
        # Check for direct contradictions
        direct_contradiction = self._check_direct_contradiction(new_belief, existing_belief)
        if direct_contradiction:
            return self._create_contradiction_event(
                new_belief, existing_belief, full_statement,
                ContradictionType.DIRECT, direct_contradiction
            )
        
        # Check for temporal contradictions (change over time)
        temporal_contradiction = self._check_temporal_contradiction(new_belief, existing_belief)
        if temporal_contradiction:
            # Temporal changes are usually not contradictions, but worth noting
            severity = ContradictionSeverity.LOW
            return self._create_contradiction_event(
                new_belief, existing_belief, full_statement,
                ContradictionType.TEMPORAL, temporal_contradiction, severity
            )
        
        # Check for preference contradictions
        preference_contradiction = self._check_preference_contradiction(new_belief, existing_belief)
        if preference_contradiction:
            return self._create_contradiction_event(
                new_belief, existing_belief, full_statement,
                ContradictionType.PREFERENCE, preference_contradiction
            )
        
        # Check for logical contradictions
        logical_contradiction = self._check_logical_contradiction(new_belief, existing_belief)
        if logical_contradiction:
            return self._create_contradiction_event(
                new_belief, existing_belief, full_statement,
                ContradictionType.LOGICAL, logical_contradiction
            )
        
        return None
    
    def _beliefs_are_comparable(self, belief1: BeliefStatement, belief2: BeliefStatement) -> bool:
        """Check if two beliefs are comparable (same subject area)"""
        # Extract key subjects from both beliefs
        subjects1 = self._extract_subjects(belief1.content)
        subjects2 = self._extract_subjects(belief2.content)
        
        # Check for overlap in subjects
        return bool(subjects1.intersection(subjects2))
    
    def _extract_subjects(self, belief_content: str) -> Set[str]:
        """Extract key subjects from belief content"""
        # Simple subject extraction - could be enhanced with NLP
        words = belief_content.lower().split()
        
        # Remove common words
        stop_words = {'i', 'am', 'is', 'are', 'the', 'a', 'an', 'and', 'or', 'but', 'my', 'have', 'like', 'love', 'hate'}
        subjects = {word for word in words if word not in stop_words and len(word) > 2}
        
        return subjects
    
    def _check_direct_contradiction(self, new_belief: BeliefStatement, 
                                  existing_belief: BeliefStatement) -> Optional[str]:
        """Check for direct contradictions between beliefs"""
        new_content = new_belief.content.lower()
        existing_content = existing_belief.content.lower()
        
        # Check for direct opposite words
        for positive, negative in self.contradiction_indicators['direct_opposites']:
            if ((positive in new_content and negative in existing_content) or
                (negative in new_content and positive in existing_content)):
                return f"Direct opposition: '{positive}' vs '{negative}'"
        
        # Check for specific contradictory patterns
        if self._contains_negation_contradiction(new_content, existing_content):
            return "Negation contradiction detected"
        
        return None
    
    def _contains_negation_contradiction(self, text1: str, text2: str) -> bool:
        """Check if one text negates the other"""
        # Simple negation check - could be enhanced
        negation_words = ["not", "don't", "doesn't", "won't", "can't", "never", "no"]
        
        # Remove negations from both texts and see if they're similar
        text1_positive = text1
        text2_positive = text2
        
        for neg in negation_words:
            text1_positive = text1_positive.replace(neg, "").strip()
            text2_positive = text2_positive.replace(neg, "").strip()
        
        # If the texts are similar after removing negations, and one originally had negations
        has_negation_1 = any(neg in text1 for neg in negation_words)
        has_negation_2 = any(neg in text2 for neg in negation_words)
        
        if has_negation_1 != has_negation_2:  # One has negation, other doesn't
            # Check similarity of positive forms
            similarity = self._text_similarity(text1_positive, text2_positive)
            return similarity > 0.6
        
        return False
    
    def _check_temporal_contradiction(self, new_belief: BeliefStatement, 
                                    existing_belief: BeliefStatement) -> Optional[str]:
        """Check for temporal contradictions (changes over time)"""
        new_content = new_belief.content.lower()
        existing_content = existing_belief.content.lower()
        
        # Check for temporal markers indicating change
        temporal_markers = self.contradiction_indicators['temporal_markers']
        
        has_temporal_new = any(marker in new_content for marker in temporal_markers)
        has_temporal_existing = any(marker in existing_content for marker in temporal_markers)
        
        if has_temporal_new or has_temporal_existing:
            # This might be a legitimate change over time
            time_diff = new_belief.date_established - existing_belief.date_established
            if time_diff.days > 7:  # More than a week apart
                return f"Temporal change detected (change over {time_diff.days} days)"
        
        return None
    
    def _check_preference_contradiction(self, new_belief: BeliefStatement, 
                                      existing_belief: BeliefStatement) -> Optional[str]:
        """Check for preference contradictions"""
        if new_belief.category != "preferences" or existing_belief.category != "preferences":
            return None
        
        new_content = new_belief.content.lower()
        existing_content = existing_belief.content.lower()
        
        # Extract the subject being evaluated
        subject_new = self._extract_preference_subject(new_content)
        subject_existing = self._extract_preference_subject(existing_content)
        
        if subject_new and subject_existing and subject_new == subject_existing:
            # Same subject, check for contradictory preferences
            new_sentiment = self._extract_preference_sentiment(new_content)
            existing_sentiment = self._extract_preference_sentiment(existing_content)
            
            if new_sentiment and existing_sentiment and new_sentiment != existing_sentiment:
                return f"Preference contradiction: {subject_new} ({existing_sentiment} → {new_sentiment})"
        
        return None
    
    def _extract_preference_subject(self, preference_text: str) -> Optional[str]:
        """Extract the subject of a preference statement"""
        # Simple extraction - could be enhanced
        patterns = [
            r"(?:love|hate|like|dislike|enjoy|can't stand) (.+?)(?:\s|$)",
            r"my favorite (.+?) is",
            r"(.+?) (?:makes? me|is) (?:happy|sad|angry)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, preference_text)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extract_preference_sentiment(self, preference_text: str) -> Optional[str]:
        """Extract the sentiment of a preference statement"""
        positive_words = ['love', 'like', 'enjoy', 'favorite', 'happy', 'great']
        negative_words = ['hate', 'dislike', "can't stand", 'angry', 'sad', 'terrible']
        
        if any(word in preference_text for word in positive_words):
            return "positive"
        elif any(word in preference_text for word in negative_words):
            return "negative"
        
        return None
    
    def _check_logical_contradiction(self, new_belief: BeliefStatement, 
                                   existing_belief: BeliefStatement) -> Optional[str]:
        """Check for logical contradictions"""
        # This would be enhanced with more sophisticated logical reasoning
        # For now, just check for obvious logical inconsistencies
        
        new_content = new_belief.content.lower()
        existing_content = existing_belief.content.lower()
        
        # Example: "I am single" vs "I am married"
        if ("single" in new_content and "married" in existing_content) or \
           ("married" in new_content and "single" in existing_content):
            return "Logical contradiction: marital status"
        
        # Example: "I have no children" vs "I have 2 children"
        if ("no children" in new_content or "don't have children" in new_content) and \
           any(word in existing_content for word in ["child", "children", "kids"]):
            return "Logical contradiction: children status"
        
        return None
    
    def _create_contradiction_event(self, new_belief: BeliefStatement, 
                                  existing_belief: BeliefStatement,
                                  full_statement: str,
                                  contradiction_type: ContradictionType,
                                  explanation: str,
                                  severity: ContradictionSeverity = None) -> ContradictionEvent:
        """Create a contradiction event"""
        if severity is None:
            severity = self._assess_contradiction_severity(contradiction_type, new_belief, existing_belief)
        
        confidence = self._assess_contradiction_confidence(new_belief, existing_belief, contradiction_type)
        
        suggested_response = self._generate_contradiction_response(
            new_belief, existing_belief, contradiction_type, severity
        )
        
        return ContradictionEvent(
            original_belief=existing_belief,
            new_statement=new_belief.content,
            contradiction_type=contradiction_type,
            severity=severity,
            confidence=confidence,
            detected_at=datetime.now(),
            context=full_statement,
            explanation=explanation,
            suggested_response=suggested_response
        )
    
    def _assess_contradiction_severity(self, contradiction_type: ContradictionType,
                                     new_belief: BeliefStatement,
                                     existing_belief: BeliefStatement) -> ContradictionSeverity:
        """Assess the severity of a contradiction"""
        # Consider emotional weight and confidence
        avg_emotional_weight = (new_belief.emotional_weight + existing_belief.emotional_weight) / 2
        avg_confidence = (new_belief.confidence + existing_belief.confidence) / 2
        
        if contradiction_type == ContradictionType.DIRECT:
            if avg_emotional_weight > 0.7 and avg_confidence > 0.8:
                return ContradictionSeverity.CRITICAL
            elif avg_emotional_weight > 0.5:
                return ContradictionSeverity.HIGH
            else:
                return ContradictionSeverity.MEDIUM
        
        elif contradiction_type == ContradictionType.TEMPORAL:
            return ContradictionSeverity.LOW  # Changes over time are usually okay
        
        elif contradiction_type == ContradictionType.PREFERENCE:
            if avg_emotional_weight > 0.6:
                return ContradictionSeverity.MEDIUM
            else:
                return ContradictionSeverity.LOW
        
        else:
            return ContradictionSeverity.MEDIUM
    
    def _assess_contradiction_confidence(self, new_belief: BeliefStatement,
                                       existing_belief: BeliefStatement,
                                       contradiction_type: ContradictionType) -> float:
        """Assess confidence in the contradiction detection"""
        base_confidence = 0.7
        
        # Higher confidence for direct contradictions
        if contradiction_type == ContradictionType.DIRECT:
            base_confidence = 0.9
        
        # Adjust based on belief confidence
        avg_belief_confidence = (new_belief.confidence + existing_belief.confidence) / 2
        adjusted_confidence = (base_confidence + avg_belief_confidence) / 2
        
        return min(0.95, adjusted_confidence)  # Cap at 95%
    
    def _generate_contradiction_response(self, new_belief: BeliefStatement,
                                       existing_belief: BeliefStatement,
                                       contradiction_type: ContradictionType,
                                       severity: ContradictionSeverity) -> str:
        """Generate a suggested response for the contradiction"""
        if severity == ContradictionSeverity.CRITICAL:
            return f"I notice you mentioned '{new_belief.content}', but I remember you saying '{existing_belief.content}' before. Has something changed?"
        
        elif severity == ContradictionSeverity.HIGH:
            return f"That's interesting - you mentioned '{new_belief.content}', which seems different from what you told me before about '{existing_belief.content}'. Could you help me understand?"
        
        elif severity == ContradictionSeverity.MEDIUM:
            return f"I noticed you said '{new_belief.content}'. I also remember you mentioning '{existing_belief.content}'. Are both things true?"
        
        elif severity == ContradictionSeverity.LOW:
            if contradiction_type == ContradictionType.TEMPORAL:
                return f"I see your perspective on this has evolved since we last talked about it."
            else:
                return f"I'm noting some different information about this topic."
        
        else:
            return "I'm keeping track of what you've shared with me."
    
    def _assess_statement_confidence(self, statement: str) -> float:
        """Assess confidence level of a statement"""
        confidence = 0.8  # Default confidence
        
        # Lower confidence for uncertain words
        uncertainty_words = self.contradiction_indicators['uncertainty_words']
        if any(word in statement for word in uncertainty_words):
            confidence -= 0.3
        
        # Higher confidence for definitive statements
        definitive_words = ['definitely', 'absolutely', 'certainly', 'always', 'never']
        if any(word in statement for word in definitive_words):
            confidence += 0.1
        
        return max(0.1, min(1.0, confidence))
    
    def _assess_emotional_weight(self, content: str, category: str) -> float:
        """Assess emotional weight of a belief"""
        emotional_weight = 0.3  # Default
        
        # Higher weight for emotional categories
        if category == 'emotional':
            emotional_weight = 0.8
        elif category == 'preferences':
            emotional_weight = 0.5
        elif category == 'factual':
            emotional_weight = 0.3
        
        # Adjust based on emotional words in content
        emotional_words = ['love', 'hate', 'fear', 'anxiety', 'joy', 'depression', 'anger', 'happiness']
        if any(word in content.lower() for word in emotional_words):
            emotional_weight += 0.2
        
        return min(1.0, emotional_weight)
    
    def _extract_tags(self, content: str, category: str) -> Set[str]:
        """Extract tags from belief content"""
        tags = {category}
        
        # Add semantic tags based on content
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['family', 'parent', 'child', 'spouse']):
            tags.add('family')
        if any(word in content_lower for word in ['work', 'job', 'career', 'office']):
            tags.add('work')
        if any(word in content_lower for word in ['health', 'medical', 'doctor', 'sick']):
            tags.add('health')
        if any(word in content_lower for word in ['food', 'eat', 'cooking', 'restaurant']):
            tags.add('food')
        
        return tags
    
    def _text_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple text similarity"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _store_belief(self, belief: BeliefStatement):
        """Store a belief in the belief store"""
        # Generate a unique ID for the belief
        belief_id = f"{belief.category}_{len(self.beliefs)}_{int(belief.date_established.timestamp())}"
        
        # Check if similar belief already exists
        similar_belief_id = self._find_similar_belief(belief)
        if similar_belief_id:
            # Update existing belief instead of creating new one
            existing_belief = self.beliefs[similar_belief_id]
            existing_belief.last_mentioned = belief.date_established
            existing_belief.confidence = (existing_belief.confidence + belief.confidence) / 2
            existing_belief.supporting_evidence.append(belief.content)
        else:
            # Store as new belief
            self.beliefs[belief_id] = belief
        
        self.save_beliefs()
    
    def _find_similar_belief(self, belief: BeliefStatement) -> Optional[str]:
        """Find similar existing belief"""
        for belief_id, existing_belief in self.beliefs.items():
            if (existing_belief.category == belief.category and
                self._text_similarity(existing_belief.content, belief.content) > 0.8):
                return belief_id
        return None
    
    def save_beliefs(self):
        """Save beliefs to persistent storage"""
        try:
            beliefs_data = {}
            for belief_id, belief in self.beliefs.items():
                beliefs_data[belief_id] = {
                    'content': belief.content,
                    'confidence': belief.confidence,
                    'date_established': belief.date_established.isoformat(),
                    'last_mentioned': belief.last_mentioned.isoformat(),
                    'source_context': belief.source_context,
                    'category': belief.category,
                    'emotional_weight': belief.emotional_weight,
                    'supporting_evidence': belief.supporting_evidence,
                    'contradicting_evidence': belief.contradicting_evidence,
                    'tags': list(belief.tags)
                }
            
            with open(self.belief_store_path, 'w') as f:
                json.dump(beliefs_data, f, indent=2)
            
            logging.debug(f"[BeliefAnalyzer] 💾 Saved {len(self.beliefs)} beliefs")
            
        except Exception as e:
            logging.error(f"[BeliefAnalyzer] ❌ Failed to save beliefs: {e}")
    
    def load_beliefs(self):
        """Load beliefs from persistent storage"""
        try:
            if self.belief_store_path.exists():
                with open(self.belief_store_path, 'r') as f:
                    beliefs_data = json.load(f)
                
                for belief_id, data in beliefs_data.items():
                    belief = BeliefStatement(
                        content=data['content'],
                        confidence=data['confidence'],
                        date_established=datetime.fromisoformat(data['date_established']),
                        last_mentioned=datetime.fromisoformat(data['last_mentioned']),
                        source_context=data['source_context'],
                        category=data['category'],
                        emotional_weight=data['emotional_weight'],
                        supporting_evidence=data.get('supporting_evidence', []),
                        contradicting_evidence=data.get('contradicting_evidence', []),
                        tags=set(data.get('tags', []))
                    )
                    self.beliefs[belief_id] = belief
                
                logging.info(f"[BeliefAnalyzer] 📂 Loaded {len(self.beliefs)} beliefs")
        
        except Exception as e:
            logging.error(f"[BeliefAnalyzer] ❌ Failed to load beliefs: {e}")
            self.beliefs = {}
    
    def get_contradiction_summary(self) -> Dict[str, Any]:
        """Get summary of recent contradictions"""
        recent_contradictions = [
            c for c in self.contradiction_history
            if datetime.now() - c.detected_at < timedelta(days=7)
        ]
        
        return {
            'total_beliefs': len(self.beliefs),
            'recent_contradictions': len(recent_contradictions),
            'contradiction_types': {
                ctype.value: len([c for c in recent_contradictions if c.contradiction_type == ctype])
                for ctype in ContradictionType
            },
            'severity_distribution': {
                severity.value: len([c for c in recent_contradictions if c.severity == severity])
                for severity in ContradictionSeverity
            }
        }

# Global belief analyzer instance
belief_analyzer = BeliefAnalyzer()

def analyze_for_contradictions(statement: str, context: str = "") -> Tuple[List[ContradictionEvent], Dict[str, Any]]:
    """
    Convenience function to analyze a statement for contradictions
    
    Args:
        statement: User's statement to analyze
        context: Additional context
        
    Returns:
        Tuple of (contradictions, analysis_summary)
    """
    contradictions = belief_analyzer.analyze_statement(statement, context)
    summary = belief_analyzer.get_contradiction_summary()
    
    return contradictions, summary

def get_belief_stats() -> Dict[str, Any]:
    """Get belief analyzer statistics"""
    return belief_analyzer.get_contradiction_summary()

logging.info("[BeliefAnalyzer] 🧠 Belief contradiction analyzer module loaded")
print("[BeliefAnalyzer] ✅ Real Belief Contradiction Detection: LOADED")
print("[BeliefAnalyzer] 🎯 Enhanced consciousness awareness of user consistency")
print("[BeliefAnalyzer] 🔍 Detects contradictions and generates awareness responses")