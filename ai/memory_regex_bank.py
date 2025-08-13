"""
Regex-based memory extraction patterns.
"""
import re
from typing import List, Tuple, Dict, Any


# Pattern groups for memory extraction
PATTERN_GROUPS = {
    'shopping_brands': {
        'patterns': [
            r'\b(?:bought|purchased|got|picked up|ordered)\s+([^.!?]+?)\s+(?:from|at)\s+(woolworths|coles|aldi|target|kmart|bunnings|jb hi-fi|harvey norman|big w|ikea)\b',
            r'\b(?:shopping at|went to)\s+(woolworths|coles|aldi|target|kmart|bunnings|jb hi-fi|harvey norman|big w|ikea)(?:\s+(?:for|to get)\s+([^.!?]+))?\b',
            r'\b(apple|samsung|sony|nintendo|microsoft|google|amazon)\s+([^.!?]+?)\b',
            r'\bneed to (?:buy|get|pick up)\s+([^.!?]+?)(?:\s+(?:from|at|today|tomorrow|yesterday))?\b',
        ],
        'confidence': 0.85,
        'type': 'shopping'
    },
    
    'decisions': {
        'patterns': [
            r'\b(?:decided|chose|will|going to|planning to)\s+([^.!?]+?)(?:\s+(?:today|tomorrow|yesterday|next|last))?\b',
            r'\bmade a decision to\s+([^.!?]+?)\b',
            r'\bchanged my mind about\s+([^.!?]+?)\b',
            r'\bthinking about\s+([^.!?]+?)\b',
        ],
        'confidence': 0.75,
        'type': 'decision'
    },
    
    'travel_plan': {
        'patterns': [
            r'\b(?:going to|visiting|traveling to|trip to)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b',
            r'\bbooked?\s+(?:a\s+)?(?:flight|hotel|accommodation|ticket)\s+(?:to|for)\s+(.+?)\b',
            r'\bplanning a (?:trip|holiday|vacation)\s+to\s+(.+?)\b',
            r'\bleaving for\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b',
        ],
        'confidence': 0.90,
        'type': 'travel_plan'
    },
    
    'travel_completion': {
        'patterns': [
            r'\b(?:just got back|returned|came back)\s+from\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b',
            r'\bfinished (?:my\s+)?(?:trip|holiday|vacation)\s+(?:to|in)\s+(.+?)\b',
            r'\b(?:was|been) (?:in|at)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b',
        ],
        'confidence': 0.85,
        'type': 'travel_completion'
    },
    
    'recurring_schedules': {
        'patterns': [
            r'\bevery\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday|weekday|weekend)\s+([^.!?]+?)\b',
            r'\b(?:weekly|daily|monthly)\s+([^.!?]+?)\b',
            r'\bscheduled\s+([^.!?]+?)\s+every\s+([^.!?]+?)\b',
            r'\bregular\s+([^.!?]+?)\s+(?:on|at)\s+([^.!?]+?)\b',
        ],
        'confidence': 0.80,
        'type': 'schedule'
    },
    
    'family_possessives': {
        'patterns': [
            r'\b(?:my|our)\s+(mum|dad|mother|father|mom|parent|sister|brother|wife|husband|son|daughter|child|family)(?:\'s)?\s+(.+?)\b',
            r'\b(mum|dad|mother|father|mom|parent|sister|brother|wife|husband|son|daughter|child)(?:\'s)?\s+(.+?)\b',
            r'\bfamily\s+(.+?)\b',
        ],
        'confidence': 0.70,
        'type': 'family'
    },
    
    'media_anaphora': {
        'patterns': [
            r'\b(?:watched|watching|saw)\s+(.*?)\s+(?:movie|film|show|series|documentary)\b',
            r'\b(?:listened to|hearing|heard)\s+(.*?)\s+(?:song|music|album|podcast)\b',
            r'\b(?:reading|read)\s+(.*?)\s+(?:book|novel|article)\b',
            r'\b(?:the|that)\s+(movie|film|show|series|book|song|album)\s+(?:about|with|featuring)\s+(.+?)\b',
        ],
        'confidence': 0.75,
        'type': 'media'
    },
    
    'meals': {
        'patterns': [
            r'\b(?:had|ate|eating|having)\s+(breakfast|lunch|dinner|brunch|snack)\s+(?:at|with)\s+(.+?)\b',
            r'\b(?:cooked|made|prepared)\s+(.+?)\s+for\s+(breakfast|lunch|dinner)\b',
            r'\b(?:breakfast|lunch|dinner|meal)\s+(?:was|is)\s+(.+?)\b',
            r'\border(?:ed)?\s+(.+?)\s+(?:for|from)\s+(.+?)\b',
        ],
        'confidence': 0.65,
        'type': 'meal'
    },
    
    'distances': {
        'patterns': [
            r'\b(\d+(?:\.\d+)?)\s*(?:km|kilometres|kilometers|miles)\s+(?:to|from|away from)\s+([^.!?]+?)\b',
            r'\b(?:about|around|roughly)\s+(\d+(?:\.\d+)?)\s*(?:km|kilometres|kilometers|miles)(?:\s+(?:to|from|away from)\s+([^.!?]+?))?\b',
            r'\b(\d+(?:\.\d+)?)\s*(?:minute|minutes|hour|hours)\s+(?:drive|walk|trip)\s+(?:to|from)\s+([^.!?]+?)\b',
        ],
        'confidence': 0.80,
        'type': 'distance'
    },
    
    'appointments_completion': {
        'patterns': [
            r'\b(?:finished|completed|done with)\s+(?:my\s+)?(?:appointment|meeting|session)\s+(?:with|at)\s+(.+?)\b',
            r'\b(?:saw|met with|visited)\s+(?:the\s+)?(doctor|dentist|therapist|counselor|specialist)\b',
            r'\b(?:appointment|meeting|session)\s+(?:with|at)\s+(.+?)\s+(?:was|is)\s+(?:done|finished|over)\b',
        ],
        'confidence': 0.85,
        'type': 'appointment_done'
    },
    
    'dreams': {
        'patterns': [
            r'\b(?:dreamed|dreamt|had a dream)\s+(?:about|that)\s+(.+?)\b',
            r'\b(?:nightmare|bad dream)\s+(?:about|involving)\s+(.+?)\b',
            r'\bin my dream\s+(.+?)\b',
            r'\bdream(?:ed|t)?\s+(?:of|about)\s+(.+?)\b',
        ],
        'confidence': 0.60,
        'type': 'dream'
    }
}


def calculate_confidence(pattern_group: str, match_quality: float = 1.0) -> float:
    """
    Calculate confidence score based on pattern group and match quality.
    
    Args:
        pattern_group: The pattern group that matched
        match_quality: Quality of the match (0.0-1.0)
        
    Returns:
        Confidence score (0.0-1.0)
    """
    base_confidence = PATTERN_GROUPS.get(pattern_group, {}).get('confidence', 0.5)
    return min(base_confidence * match_quality, 1.0)


def extract_candidates(text: str) -> Tuple[List[Dict[str, Any]], float, List[str]]:
    """
    Extract memory candidates from text using regex patterns.
    
    Args:
        text: Input text to analyze for memory candidates
        
    Returns:
        Tuple containing:
        - List of extracted memory items (dicts with 'content', 'type', etc.)
        - Maximum confidence score among all matches
        - List of pattern IDs that matched
    """
    items = []
    max_confidence = 0.0
    pattern_ids = []
    
    text_lower = text.lower()
    
    for group_name, group_data in PATTERN_GROUPS.items():
        patterns = group_data['patterns']
        item_type = group_data['type']
        
        for i, pattern in enumerate(patterns):
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            
            for match in matches:
                # Extract matched content
                groups = match.groups()
                if groups:
                    content = ' '.join(filter(None, groups)).strip()
                else:
                    content = match.group(0).strip()
                
                # Calculate match quality based on content length and specificity
                match_quality = min(len(content) / 50.0, 1.0)  # Longer content = higher quality
                if len(content) < 3:  # Too short
                    match_quality *= 0.5
                
                confidence = calculate_confidence(group_name, match_quality)
                
                # Create memory item
                item = {
                    'content': content,
                    'type': item_type,
                    'confidence': confidence,
                    'pattern_group': group_name,
                    'pattern_index': i,
                    'original_text': match.group(0),
                    'start': match.start(),
                    'end': match.end()
                }
                
                items.append(item)
                max_confidence = max(max_confidence, confidence)
                
                pattern_id = f"{group_name}_{i}"
                if pattern_id not in pattern_ids:
                    pattern_ids.append(pattern_id)
    
    # Sort items by confidence (highest first)
    items.sort(key=lambda x: x['confidence'], reverse=True)
    
    return items, max_confidence, pattern_ids


# Self-test function
def test_regex_patterns():
    """Test the regex patterns with sample utterances."""
    test_cases = [
        "I bought milk from Woolworths yesterday",
        "Going to Brisbane next week for a holiday",
        "Had dinner at that Italian restaurant",
        "Every Monday I have a meeting with the team",
        "My mum's birthday is coming up",
        "Watched the new Marvel movie last night",
        "The appointment with the doctor is finished",
        "Dreamed about flying over the ocean",
        "It's about 5km to the shopping center",
        "Decided to change jobs next month"
    ]
    
    print("Testing regex patterns:")
    for test_text in test_cases:
        items, max_conf, pattern_ids = extract_candidates(test_text)
        print(f"\nText: '{test_text}'")
        print(f"Max confidence: {max_conf:.2f}")
        print(f"Pattern IDs: {pattern_ids}")
        for item in items[:2]:  # Show top 2 matches
            print(f"  - {item['type']}: '{item['content']}' (conf: {item['confidence']:.2f})")


if __name__ == "__main__":
    test_regex_patterns()