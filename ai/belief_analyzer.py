"""
Belief Analyzer - Real Belief Contradiction Detection
Compares new user statements to stored beliefs/facts and flags contradictions.
"""

import json
import logging
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum

class ContradictionSeverity(Enum):
    """Severity levels for belief contradictions"""
    MINOR = "minor"           # Small inconsistencies, preferences changed
    MODERATE = "moderate"     # Conflicting facts, changed circumstances  
    MAJOR = "major"          # Direct contradictions, major life changes
    CRITICAL = "critical"    # Safety concerns, serious contradictions

@dataclass
class Belief:
    """A stored belief or fact about the user"""
    content: str
    category: str  # "personal", "preference", "fact", "relationship", "goal"
    confidence: float  # 0.0 to 1.0
    source: str  # Where this belief came from
    timestamp: str
    last_confirmed: str
    confirmation_count: int = 1
    contradicted_count: int = 0

@dataclass
class Contradiction:
    """A detected contradiction between beliefs"""
    original_belief: Belief
    new_statement: str
    severity: ContradictionSeverity
    confidence: float  # How confident we are this is a contradiction
    explanation: str
    detected_at: str
    resolved: bool = False

class BeliefAnalyzer:
    """
    Real Belief Contradiction Detection System
    
    Analyzes new user statements against stored beliefs to detect contradictions
    and maintain awareness of user consistency and changes over time.
    """
    
    def __init__(self, belief_store_path: str = "belief_store.json"):
        self.belief_store_path = Path(belief_store_path)
        self.beliefs: Dict[str, List[Belief]] = {}
        self.contradictions: List[Contradiction] = []
        self.load_belief_store()
        
        logging.info(f"[BeliefAnalyzer] 🧠 Belief analyzer initialized with {len(self.beliefs)} belief categories")
    
    def load_belief_store(self):
        """Load beliefs from persistent storage"""
        try:
            if self.belief_store_path.exists():
                with open(self.belief_store_path, 'r') as f:
                    data = json.load(f)
                
                # Convert dictionaries back to Belief objects
                for category, belief_list in data.get('beliefs', {}).items():
                    self.beliefs[category] = [
                        Belief(**belief_data) for belief_data in belief_list
                    ]
                
                # Load contradictions
                contradiction_data = data.get('contradictions', [])
                self.contradictions = [
                    Contradiction(
                        original_belief=Belief(**c['original_belief']),
                        new_statement=c['new_statement'],
                        severity=ContradictionSeverity(c['severity']),
                        confidence=c['confidence'],
                        explanation=c['explanation'],
                        detected_at=c['detected_at'],
                        resolved=c.get('resolved', False)
                    ) for c in contradiction_data
                ]
                
                logging.info(f"[BeliefAnalyzer] 📚 Loaded {sum(len(beliefs) for beliefs in self.beliefs.values())} beliefs and {len(self.contradictions)} contradictions")
            else:
                logging.info(f"[BeliefAnalyzer] 🆕 Creating new belief store")
        
        except Exception as e:
            logging.error(f"[BeliefAnalyzer] ❌ Error loading belief store: {e}")
            self.beliefs = {}
            self.contradictions = []
    
    def save_belief_store(self):
        """Save beliefs to persistent storage"""
        try:
            # Convert Belief objects to dictionaries
            beliefs_data = {}
            for category, belief_list in self.beliefs.items():
                beliefs_data[category] = [asdict(belief) for belief in belief_list]
            
            # Convert Contradiction objects to dictionaries
            contradictions_data = []
            for contradiction in self.contradictions:
                contradictions_data.append({
                    'original_belief': asdict(contradiction.original_belief),
                    'new_statement': contradiction.new_statement,
                    'severity': contradiction.severity.value,
                    'confidence': contradiction.confidence,
                    'explanation': contradiction.explanation,
                    'detected_at': contradiction.detected_at,
                    'resolved': contradiction.resolved
                })
            
            data = {
                'beliefs': beliefs_data,
                'contradictions': contradictions_data,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.belief_store_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            logging.debug(f"[BeliefAnalyzer] 💾 Belief store saved")
        
        except Exception as e:
            logging.error(f"[BeliefAnalyzer] ❌ Error saving belief store: {e}")
    
    def extract_beliefs_from_statement(self, statement: str, username: str) -> List[Belief]:
        """
        Extract potential beliefs from a user statement
        
        Args:
            statement: User's statement to analyze
            username: Username for context
            
        Returns:
            List of extracted beliefs
        """
        beliefs = []
        current_time = datetime.now().isoformat()
        
        # Personal information patterns
        personal_patterns = [
            (r"my name is (\w+)", "personal", "name"),
            (r"i am (\d+) years old", "personal", "age"),
            (r"i live in ([^,.]+)", "personal", "location"),
            (r"i work as a? ([^,.]+)", "personal", "occupation"),
            (r"i have a? ([^,.]+)", "personal", "possession"),
            (r"my (\w+) is ([^,.]+)", "personal", "attribute")
        ]
        
        # Preference patterns
        preference_patterns = [
            (r"i (love|like|enjoy|prefer) ([^,.]+)", "preference", "positive"),
            (r"i (hate|dislike|avoid) ([^,.]+)", "preference", "negative"),
            (r"my favorite ([^,.]+) is ([^,.]+)", "preference", "favorite"),
            (r"i usually ([^,.]+)", "preference", "habit"),
            (r"i always ([^,.]+)", "preference", "habit"),
            (r"i never ([^,.]+)", "preference", "habit")
        ]
        
        # Relationship patterns
        relationship_patterns = [
            (r"my (\w+) is ([^,.]+)", "relationship", "family"),
            (r"i'm (married|single|divorced|engaged)", "relationship", "status"),
            (r"i have a? (\w+) named ([^,.]+)", "relationship", "named_relationship"),
            (r"(\w+) and i ([^,.]+)", "relationship", "interaction")
        ]
        
        # Goal patterns
        goal_patterns = [
            (r"i want to ([^,.]+)", "goal", "desire"),
            (r"i'm planning to ([^,.]+)", "goal", "plan"),
            (r"my goal is to ([^,.]+)", "goal", "explicit"),
            (r"i hope to ([^,.]+)", "goal", "aspiration")
        ]
        
        # Fact patterns
        fact_patterns = [
            (r"i am ([^,.]+)", "fact", "state"),
            (r"i have ([^,.]+)", "fact", "possession"),
            (r"i can ([^,.]+)", "fact", "ability"),
            (r"i graduated from ([^,.]+)", "fact", "education"),
            (r"i studied ([^,.]+)", "fact", "education")
        ]
        
        all_patterns = [
            ("personal", personal_patterns),
            ("preference", preference_patterns),
            ("relationship", relationship_patterns),
            ("goal", goal_patterns),
            ("fact", fact_patterns)
        ]
        
        statement_lower = statement.lower()
        
        for category, patterns in all_patterns:
            for pattern, belief_category, subcategory in patterns:
                matches = re.finditer(pattern, statement_lower)
                for match in matches:
                    # Extract the matched content
                    matched_text = match.group(0)
                    
                    # Create belief
                    belief = Belief(
                        content=matched_text,
                        category=belief_category,
                        confidence=0.8,  # Default confidence
                        source=f"user_statement_{username}",
                        timestamp=current_time,
                        last_confirmed=current_time
                    )
                    
                    beliefs.append(belief)
        
        return beliefs
    
    def check_for_contradictions(self, new_statement: str, username: str) -> List[Contradiction]:
        """
        Check if a new statement contradicts existing beliefs
        
        Args:
            new_statement: New user statement to check
            username: Username for context
            
        Returns:
            List of detected contradictions
        """
        contradictions = []
        new_beliefs = self.extract_beliefs_from_statement(new_statement, username)
        
        for new_belief in new_beliefs:
            # Check against existing beliefs in the same category
            existing_beliefs = self.beliefs.get(new_belief.category, [])
            
            for existing_belief in existing_beliefs:
                contradiction = self._analyze_belief_contradiction(existing_belief, new_belief, new_statement)
                if contradiction:
                    contradictions.append(contradiction)
        
        return contradictions
    
    def _analyze_belief_contradiction(self, existing_belief: Belief, new_belief: Belief, full_statement: str) -> Optional[Contradiction]:
        """
        Analyze if two beliefs contradict each other
        
        Args:
            existing_belief: Previously stored belief
            new_belief: Newly extracted belief
            full_statement: Full user statement for context
            
        Returns:
            Contradiction object if contradiction detected, None otherwise
        """
        # Simple contradiction detection based on content analysis
        existing_content = existing_belief.content.lower()
        new_content = new_belief.content.lower()
        
        # Direct contradiction patterns
        contradiction_patterns = [
            # Positive vs negative preferences
            (r"i (love|like|enjoy)", r"i (hate|dislike|avoid)", ContradictionSeverity.MODERATE),
            (r"i always", r"i never", ContradictionSeverity.MAJOR),
            (r"i have", r"i don't have", ContradictionSeverity.MODERATE),
            (r"i am", r"i am not", ContradictionSeverity.MODERATE),
            (r"my .+ is", r"my .+ is", ContradictionSeverity.MINOR),  # Same attribute, different value
        ]
        
        # Check for obvious contradictions
        for pos_pattern, neg_pattern, severity in contradiction_patterns:
            if re.search(pos_pattern, existing_content) and re.search(neg_pattern, new_content):
                return self._create_contradiction(existing_belief, full_statement, severity, 0.8, "Direct positive/negative contradiction")
            if re.search(neg_pattern, existing_content) and re.search(pos_pattern, new_content):
                return self._create_contradiction(existing_belief, full_statement, severity, 0.8, "Direct negative/positive contradiction")
        
        # Check for semantic contradictions (simplified)
        if existing_belief.category == new_belief.category:
            # Extract key terms for comparison
            existing_terms = set(re.findall(r'\b\w+\b', existing_content))
            new_terms = set(re.findall(r'\b\w+\b', new_content))
            
            # Check for contradictory terms
            contradictory_pairs = [
                ("love", "hate"), ("like", "dislike"), ("enjoy", "avoid"),
                ("always", "never"), ("married", "single"), ("have", "don't"),
                ("am", "not"), ("can", "can't"), ("will", "won't")
            ]
            
            for term1, term2 in contradictory_pairs:
                if term1 in existing_terms and term2 in new_terms:
                    return self._create_contradiction(
                        existing_belief, 
                        full_statement, 
                        ContradictionSeverity.MODERATE, 
                        0.7, 
                        f"Contradictory terms: '{term1}' vs '{term2}'"
                    )
        
        # Check for changed values (e.g., age, location)
        if existing_belief.category == "personal":
            # Extract numbers or specific values
            existing_values = re.findall(r'\b(?:\d+|\w+)\b', existing_content)
            new_values = re.findall(r'\b(?:\d+|\w+)\b', new_content)
            
            # If same type of information but different values
            if len(existing_values) > 0 and len(new_values) > 0:
                if existing_values != new_values and any(v in existing_content.split() for v in new_content.split()):
                    return self._create_contradiction(
                        existing_belief,
                        full_statement,
                        ContradictionSeverity.MINOR,
                        0.6,
                        f"Changed personal information: {existing_values} → {new_values}"
                    )
        
        return None
    
    def _create_contradiction(self, original_belief: Belief, new_statement: str, 
                            severity: ContradictionSeverity, confidence: float, explanation: str) -> Contradiction:
        """Create a contradiction object"""
        return Contradiction(
            original_belief=original_belief,
            new_statement=new_statement,
            severity=severity,
            confidence=confidence,
            explanation=explanation,
            detected_at=datetime.now().isoformat()
        )
    
    def add_belief(self, belief: Belief):
        """Add a new belief to the store"""
        category = belief.category
        if category not in self.beliefs:
            self.beliefs[category] = []
        
        # Check if similar belief already exists
        existing_belief = self._find_similar_belief(belief)
        if existing_belief:
            # Update confirmation count
            existing_belief.confirmation_count += 1
            existing_belief.last_confirmed = belief.timestamp
            logging.debug(f"[BeliefAnalyzer] ✅ Confirmed existing belief: {belief.content}")
        else:
            # Add new belief
            self.beliefs[category].append(belief)
            logging.debug(f"[BeliefAnalyzer] 🆕 Added new belief: {belief.content}")
        
        self.save_belief_store()
    
    def _find_similar_belief(self, new_belief: Belief) -> Optional[Belief]:
        """Find a similar existing belief"""
        category_beliefs = self.beliefs.get(new_belief.category, [])
        
        for existing_belief in category_beliefs:
            # Simple similarity check based on content overlap
            existing_words = set(existing_belief.content.lower().split())
            new_words = set(new_belief.content.lower().split())
            
            overlap = len(existing_words.intersection(new_words))
            total_words = len(existing_words.union(new_words))
            
            if total_words > 0 and overlap / total_words > 0.6:  # 60% similarity threshold
                return existing_belief
        
        return None
    
    def analyze_statement(self, statement: str, username: str) -> Dict[str, Any]:
        """
        Complete analysis of a user statement
        
        Args:
            statement: User statement to analyze
            username: Username for context
            
        Returns:
            Dictionary with analysis results
        """
        # Extract new beliefs
        new_beliefs = self.extract_beliefs_from_statement(statement, username)
        
        # Check for contradictions
        contradictions = self.check_for_contradictions(statement, username)
        
        # Add new beliefs to store
        for belief in new_beliefs:
            self.add_belief(belief)
        
        # Store detected contradictions
        for contradiction in contradictions:
            self.contradictions.append(contradiction)
        
        # Save updates
        if contradictions:
            self.save_belief_store()
        
        return {
            'new_beliefs': [asdict(belief) for belief in new_beliefs],
            'contradictions': [asdict(contradiction) for contradiction in contradictions],
            'total_beliefs': sum(len(beliefs) for beliefs in self.beliefs.values()),
            'total_contradictions': len([c for c in self.contradictions if not c.resolved])
        }
    
    def get_contradiction_awareness_response(self, contradictions: List[Contradiction]) -> Optional[str]:
        """
        Generate an awareness response for detected contradictions
        
        Args:
            contradictions: List of detected contradictions
            
        Returns:
            Awareness response string or None
        """
        if not contradictions:
            return None
        
        # Sort by severity
        critical_contradictions = [c for c in contradictions if c.severity == ContradictionSeverity.CRITICAL]
        major_contradictions = [c for c in contradictions if c.severity == ContradictionSeverity.MAJOR]
        moderate_contradictions = [c for c in contradictions if c.severity == ContradictionSeverity.MODERATE]
        
        if critical_contradictions:
            return "Wait, I noticed something important might have changed - want to clarify that for me?"
        elif major_contradictions:
            return "Hm, that sounds different from what you mentioned before. Did something change?"
        elif moderate_contradictions:
            return "I think you might have mentioned something different about that earlier, but maybe I'm misremembering?"
        else:
            return "Just checking - I think you said something slightly different about that before?"
    
    def get_belief_summary(self) -> Dict[str, Any]:
        """Get a summary of stored beliefs"""
        summary = {
            'total_beliefs': sum(len(beliefs) for beliefs in self.beliefs.values()),
            'categories': {},
            'recent_contradictions': len([c for c in self.contradictions if not c.resolved and 
                                        (datetime.now() - datetime.fromisoformat(c.detected_at)).days < 7])
        }
        
        for category, beliefs in self.beliefs.items():
            summary['categories'][category] = len(beliefs)
        
        return summary

# Global belief analyzer instance
belief_analyzer = BeliefAnalyzer()

def analyze_user_statement_for_contradictions(statement: str, username: str) -> Tuple[Dict[str, Any], Optional[str]]:
    """
    Analyze user statement for belief contradictions
    
    Args:
        statement: User statement to analyze
        username: Username for context
        
    Returns:
        Tuple of (analysis_results, awareness_response)
    """
    analysis = belief_analyzer.analyze_statement(statement, username)
    
    # Generate awareness response if contradictions found
    contradictions = [
        Contradiction(
            original_belief=Belief(**c['original_belief']),
            new_statement=c['new_statement'],
            severity=ContradictionSeverity(c['severity']),
            confidence=c['confidence'],
            explanation=c['explanation'],
            detected_at=c['detected_at'],
            resolved=c.get('resolved', False)
        ) for c in analysis['contradictions']
    ]
    
    awareness_response = belief_analyzer.get_contradiction_awareness_response(contradictions)
    
    return analysis, awareness_response