"""
Time and anaphora resolution helpers for memory processing.
"""
import re
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import calendar


def parse_australian_date(date_str: str, context_time: Optional[datetime] = None) -> Optional[datetime]:
    """
    Parse Australian date format where 5/10 means 5th October.
    
    Args:
        date_str: Date string to parse
        context_time: Context datetime for ambiguous dates
        
    Returns:
        Parsed datetime or None if parsing fails
    """
    if context_time is None:
        context_time = datetime.now()
    
    # AU format: DD/MM or DD/MM/YYYY
    au_patterns = [
        r'(\d{1,2})/(\d{1,2})/(\d{4})',  # DD/MM/YYYY
        r'(\d{1,2})/(\d{1,2})',  # DD/MM (assume current year)
    ]
    
    for pattern in au_patterns:
        match = re.search(pattern, date_str)
        if match:
            groups = match.groups()
            day = int(groups[0])
            month = int(groups[1])
            year = int(groups[2]) if len(groups) > 2 else context_time.year
            
            try:
                return datetime(year, month, day)
            except ValueError:
                continue
    
    return None


def parse_relative_time(text: str, context_time: Optional[datetime] = None) -> Optional[datetime]:
    """
    Parse relative time expressions like 'today', 'tomorrow', 'next week'.
    
    Args:
        text: Text containing relative time expression
        context_time: Context datetime for relative calculations
        
    Returns:
        Parsed datetime or None if parsing fails
    """
    if context_time is None:
        context_time = datetime.now()
    
    text_lower = text.lower().strip()
    
    # Today/Yesterday/Tomorrow
    if 'today' in text_lower:
        return context_time.replace(hour=12, minute=0, second=0, microsecond=0)
    elif 'yesterday' in text_lower:
        return (context_time - timedelta(days=1)).replace(hour=12, minute=0, second=0, microsecond=0)
    elif 'tomorrow' in text_lower:
        return (context_time + timedelta(days=1)).replace(hour=12, minute=0, second=0, microsecond=0)
    
    # This/Next/Last week
    if 'this week' in text_lower:
        return context_time
    elif 'next week' in text_lower:
        return context_time + timedelta(weeks=1)
    elif 'last week' in text_lower:
        return context_time - timedelta(weeks=1)
    
    # Days of the week
    weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    for i, day in enumerate(weekdays):
        if day in text_lower:
            current_weekday = context_time.weekday()
            days_ahead = i - current_weekday
            
            if 'next' in text_lower:
                days_ahead += 7
            elif 'last' in text_lower:
                days_ahead -= 7
            elif days_ahead <= 0:  # If the day has passed this week, assume next week
                days_ahead += 7
                
            return context_time + timedelta(days=days_ahead)
    
    # In N minutes/hours/days
    time_units = {
        'minute': 1, 'minutes': 1, 'min': 1, 'mins': 1,
        'hour': 60, 'hours': 60, 'hr': 60, 'hrs': 60,
        'day': 1440, 'days': 1440,
        'week': 10080, 'weeks': 10080,
        'month': 43200, 'months': 43200  # Approximate
    }
    
    for unit, minutes in time_units.items():
        pattern = rf'in\s+(\d+)\s+{unit}'
        match = re.search(pattern, text_lower)
        if match:
            count = int(match.group(1))
            return context_time + timedelta(minutes=count * minutes)
    
    return None


def parse_time_expression(time_str: str) -> Optional[tuple]:
    """
    Parse various time expressions.
    
    Args:
        time_str: Time string to parse
        
    Returns:
        Tuple of (hour, minute) or None if parsing fails
    """
    time_str = time_str.lower().strip()
    
    # Special times
    special_times = {
        'noon': (12, 0),
        'midnight': (0, 0),
        'midday': (12, 0),
    }
    
    for word, time_tuple in special_times.items():
        if word in time_str:
            return time_tuple
    
    # 24-hour format: 17:30, 09:15
    match = re.search(r'(\d{1,2}):(\d{2})', time_str)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2))
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            return (hour, minute)
    
    # 12-hour format: 5pm, 10am, 5:30pm
    match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)', time_str)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2) or 0)
        period = match.group(3)
        
        if period == 'pm' and hour != 12:
            hour += 12
        elif period == 'am' and hour == 12:
            hour = 0
            
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            return (hour, minute)
    
    # Expressions like "half past five", "quarter to three"
    match = re.search(r'(half past|quarter past|quarter to)\s+(\w+)', time_str)
    if match:
        expression = match.group(1)
        hour_word = match.group(2)
        
        # Convert word to number
        hour_map = {
            'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6,
            'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11, 'twelve': 12
        }
        
        hour = hour_map.get(hour_word)
        if hour:
            if expression == 'half past':
                return (hour, 30)
            elif expression == 'quarter past':
                return (hour, 15)
            elif expression == 'quarter to':
                return (hour - 1 if hour > 1 else 12, 45)
    
    return None


def normalize_time_references(text: str, context_time: Optional[datetime] = None) -> str:
    """
    Normalize time references in text (e.g., 'yesterday', 'next week').
    
    Args:
        text: Input text with potential time references
        context_time: Context datetime for relative time resolution
        
    Returns:
        Text with normalized absolute time references
    """
    if context_time is None:
        context_time = datetime.now()
    
    normalized_text = text
    
    # First try to parse Australian dates
    au_date_pattern = r'\b(\d{1,2}/\d{1,2}(?:/\d{4})?)\b'
    for match in re.finditer(au_date_pattern, text):
        date_str = match.group(1)
        parsed_date = parse_australian_date(date_str, context_time)
        if parsed_date:
            iso_date = parsed_date.strftime("%Y-%m-%d")
            normalized_text = normalized_text.replace(date_str, iso_date)
    
    # Parse relative time expressions
    relative_patterns = [
        r'\b(today|tomorrow|yesterday)\b',
        r'\b(this|next|last)\s+(week|month|year)\b',
        r'\b(next|last)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b',
        r'\bin\s+\d+\s+(minutes?|hours?|days?|weeks?|months?)\b'
    ]
    
    for pattern in relative_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            relative_expr = match.group(0)
            parsed_time = parse_relative_time(relative_expr, context_time)
            if parsed_time:
                iso_datetime = parsed_time.strftime("%Y-%m-%d %H:%M")
                normalized_text = normalized_text.replace(relative_expr, iso_datetime)
    
    # Parse time expressions
    time_patterns = [
        r'\b(\d{1,2}:\d{2})\b',
        r'\b(\d{1,2}(?::\d{2})?\s*(?:am|pm))\b',
        r'\b(noon|midnight|midday)\b',
        r'\b(half past|quarter past|quarter to)\s+\w+\b'
    ]
    
    for pattern in time_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            time_expr = match.group(0)
            parsed_time = parse_time_expression(time_expr)
            if parsed_time:
                hour, minute = parsed_time
                time_str = f"{hour:02d}:{minute:02d}"
                normalized_text = normalized_text.replace(time_expr, time_str)
    
    return normalized_text


def resolve_anaphora(kind: str, lookback: int, context_history: List[Dict[str, Any]]) -> Optional[str]:
    """
    Resolve anaphoric references by scanning last N episodes by category.
    
    Args:
        kind: Type of anaphora to resolve (e.g., 'person', 'place', 'media')
        lookback: Number of previous items to consider for resolution
        context_history: Recent conversation/memory context
        
    Returns:
        Resolved reference or None if not found
    """
    if not context_history:
        return None
    
    # Scan the last N items for the specified kind
    recent_items = context_history[-lookback:] if lookback > 0 else context_history
    
    # Define what we're looking for based on kind
    search_patterns = {
        'person': ['PERSON', 'family', 'speaker'],
        'place': ['LOCATION', 'travel_plan', 'travel_completion'],
        'media': ['media', 'movie', 'book', 'song'],
        'event': ['appointment', 'meeting', 'schedule'],
        'food': ['meal', 'restaurant', 'food'],
        'object': ['shopping', 'item', 'product']
    }
    
    target_types = search_patterns.get(kind, [kind])
    
    # Search for most recent mention of this type
    for item in reversed(recent_items):
        item_type = item.get('type', '').lower()
        item_kind = item.get('kind', '').lower()
        
        if any(target in item_type or target in item_kind for target in target_types):
            # Extract the most relevant content
            content = item.get('text', '') or item.get('content', '') or item.get('items', '')
            if content:
                return content
    
    return None


def extract_when_iso(text: str, context_time: Optional[datetime] = None) -> Optional[str]:
    """
    Extract and normalize time information to ISO format.
    
    Args:
        text: Input text
        context_time: Context datetime
        
    Returns:
        ISO formatted datetime string or None
    """
    if context_time is None:
        context_time = datetime.now()
    
    # Try Australian date parsing first
    au_date_pattern = r'\b(\d{1,2}/\d{1,2}(?:/\d{4})?)\b'
    match = re.search(au_date_pattern, text)
    if match:
        parsed_date = parse_australian_date(match.group(1), context_time)
        if parsed_date:
            return parsed_date.strftime("%Y-%m-%dT%H:%M:%S")
    
    # Try relative time parsing
    relative_time = parse_relative_time(text, context_time)
    if relative_time:
        return relative_time.strftime("%Y-%m-%dT%H:%M:%S")
    
    return None


def extract_anaphora_key(text: str, context_history: List[Dict[str, Any]]) -> Optional[str]:
    """
    Extract anaphora key from text for later resolution.
    
    Args:
        text: Input text
        context_history: Context for resolution
        
    Returns:
        Anaphora key or None
    """
    text_lower = text.lower()
    
    # Common anaphoric patterns
    anaphora_patterns = {
        'the_place': r'\b(?:the place|there|that place)\b',
        'the_person': r'\b(?:he|she|they|that person|the guy|the woman)\b',
        'the_thing': r'\b(?:it|that|this|the thing)\b',
        'the_event': r'\b(?:the meeting|the appointment|that event)\b',
        'the_media': r'\b(?:the movie|the book|the show|that film)\b'
    }
    
    for key, pattern in anaphora_patterns.items():
        if re.search(pattern, text_lower):
            kind = key.split('_')[1]  # Extract 'place', 'person', etc.
            resolved = resolve_anaphora(kind, 10, context_history)
            if resolved:
                return f"{key}:{resolved}"
    
    return None


# Self-test function
def test_normalization():
    """Test the normalization functions with sample inputs."""
    test_cases = [
        "Meeting on 5/10 at 2:30pm",
        "I'll see you tomorrow at noon",
        "Had lunch yesterday at half past twelve",
        "Next Monday we're going to Brisbane",
        "The appointment is in 2 hours",
        "5/10/2024 at midnight"
    ]
    
    print("Testing time normalization:")
    context = datetime(2024, 9, 15, 10, 30, 0)  # September 15, 2024, 10:30 AM
    
    for test_text in test_cases:
        normalized = normalize_time_references(test_text, context)
        when_iso = extract_when_iso(test_text, context)
        print(f"\nOriginal: '{test_text}'")
        print(f"Normalized: '{normalized}'")
        print(f"ISO: {when_iso}")


if __name__ == "__main__":
    test_normalization()