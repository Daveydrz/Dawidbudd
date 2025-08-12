# utils/time_helper.py - Time helper functions for Buddy (July 2025)
"""
Time and location helper functions for consistent time handling
"""
from datetime import datetime, timedelta
import pytz
import re
from config import USER_TIMEZONE, USER_LOCATION, USER_STATE, USER_COUNTRY

def get_buddy_current_time() -> str:
    """Get Buddy's current local time (July 2025)"""
    try:
        tz = pytz.timezone(USER_TIMEZONE)
        current_time = datetime.now(tz)
        return current_time.strftime("%Y-%m-%d %H:%M:%S")
    except:
        # Fallback to Brisbane time
        brisbane_tz = pytz.timezone("Australia/Brisbane")
        current_time = datetime.now(brisbane_tz)
        return current_time.strftime("%Y-%m-%d %H:%M:%S")

def get_buddy_time_12h() -> str:
    """Get Buddy's current time in 12-hour format"""
    try:
        tz = pytz.timezone(USER_TIMEZONE)
        current_time = datetime.now(tz)
        return current_time.strftime("%I:%M %p")
    except:
        brisbane_tz = pytz.timezone("Australia/Brisbane")
        current_time = datetime.now(brisbane_tz)
        return current_time.strftime("%I:%M %p")

def get_buddy_date() -> str:
    """Get Buddy's current date (July 2025)"""
    try:
        tz = pytz.timezone(USER_TIMEZONE)
        current_time = datetime.now(tz)
        return current_time.strftime("%A, %B %d, %Y")
    except:
        brisbane_tz = pytz.timezone("Australia/Brisbane")
        current_time = datetime.now(brisbane_tz)
        return current_time.strftime("%A, %B %d, %Y")

def get_buddy_location() -> str:
    """Get Buddy's location summary"""
    parts = []
    if USER_LOCATION:
        parts.append(USER_LOCATION)
    if USER_STATE:
        parts.append(USER_STATE)
    if USER_COUNTRY:
        parts.append(USER_COUNTRY)
    
    return ", ".join(parts) if parts else "Brisbane, Queensland, Australia"

def get_time_info_for_buddy() -> dict:
    """Get comprehensive time info for Buddy to use in responses (July 2025)"""
    try:
        tz = pytz.timezone(USER_TIMEZONE)
        now = datetime.now(tz)
        
        return {
            'current_time_24h': now.strftime("%H:%M"),
            'current_time_12h': now.strftime("%I:%M %p"),
            'current_date': now.strftime("%A, %B %d, %Y"),
            'day_name': now.strftime("%A"),
            'month_name': now.strftime("%B"),
            'year': str(now.year),
            'timezone': USER_TIMEZONE,
            'location': get_buddy_location()
        }
    except Exception as e:
        # Fallback to Brisbane time
        try:
            brisbane_tz = pytz.timezone("Australia/Brisbane")
            now = datetime.now(brisbane_tz)
            return {
                'current_time_24h': now.strftime("%H:%M"),
                'current_time_12h': now.strftime("%I:%M %p"),
                'current_date': now.strftime("%A, %B %d, %Y"),
                'day_name': now.strftime("%A"),
                'month_name': now.strftime("%B"),
                'year': str(now.year),
                'timezone': 'Australia/Brisbane',
                'location': 'Brisbane, Queensland, Australia'
            }
        except:
            # Final fallback
            now = datetime.now()
            return {
                'current_time_24h': now.strftime("%H:%M"),
                'current_time_12h': now.strftime("%I:%M %p"),
                'current_date': now.strftime("%A, %B %d, %Y"),
                'day_name': now.strftime("%A"),
                'month_name': now.strftime("%B"),
                'year': str(now.year),
                'timezone': 'Australia/Brisbane',
                'location': 'Brisbane, Queensland, Australia'
            }

# ================================================================================
# 🕒 INTERNAL HELPERS for Memory System (Private - No Public API Changes)  
# ================================================================================

def _parse_relative_date(date_str: str, reference_date: datetime = None) -> datetime:
    """INTERNAL: Parse relative date strings with robust fallbacks"""
    if reference_date is None:
        reference_date = datetime.now()
    
    date_str = date_str.lower().strip()
    
    # Handle common patterns
    if date_str in ['today', 'now', 'right now', 'just now']:
        return reference_date
    elif date_str in ['yesterday', 'last night']:
        return reference_date - timedelta(days=1)
    elif date_str in ['tomorrow', 'later today', 'tonight']:
        return reference_date + timedelta(days=1)
    elif date_str in ['last week', 'a week ago', 'week ago']:
        return reference_date - timedelta(weeks=1)
    elif date_str in ['this week', 'earlier this week']:
        # Start of this week (Monday)
        days_since_monday = reference_date.weekday()
        return reference_date - timedelta(days=days_since_monday)
    elif date_str in ['next week', 'a week from now']:
        return reference_date + timedelta(weeks=1)
    elif date_str in ['last month', 'a month ago']:
        return reference_date - timedelta(days=30)
    elif date_str in ['this month', 'earlier this month']:
        return reference_date.replace(day=1)
    elif date_str in ['next month', 'a month from now']:
        return reference_date + timedelta(days=30)
    
    # Enhanced pattern matching with safe fallbacks
    try:
        # Days ago pattern
        match = re.search(r'(\d+)\s+days?\s+ago', date_str)
        if match:
            days = min(int(match.group(1)), 365)  # Cap at 365 days
            return reference_date - timedelta(days=days)
        
        # Weeks ago pattern
        match = re.search(r'(\d+)\s+weeks?\s+ago', date_str)
        if match:
            weeks = min(int(match.group(1)), 52)  # Cap at 52 weeks
            return reference_date - timedelta(weeks=weeks)
        
        # Hours ago pattern
        match = re.search(r'(\d+)\s+hours?\s+ago', date_str)
        if match:
            hours = min(int(match.group(1)), 168)  # Cap at 1 week
            return reference_date - timedelta(hours=hours)
        
        # Days from now pattern
        match = re.search(r'(\d+)\s+days?\s+from\s+now', date_str)
        if match:
            days = min(int(match.group(1)), 365)
            return reference_date + timedelta(days=days)
            
        # Day names (Monday, Tuesday, etc.)
        days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        for i, day in enumerate(days_of_week):
            if day in date_str:
                current_weekday = reference_date.weekday()
                days_until = (i - current_weekday) % 7
                if days_until == 0 and 'next' in date_str:
                    days_until = 7
                elif days_until == 0 and 'last' in date_str:
                    days_until = -7
                elif days_until > 0 and 'last' in date_str:
                    days_until -= 7
                return reference_date + timedelta(days=days_until)
                
    except (ValueError, AttributeError) as e:
        print(f"[TimeHelper] ⚠️ Error parsing date '{date_str}': {e}")
    
    # Safe fallback - return reference date
    print(f"[TimeHelper] 🔄 Using fallback date for: '{date_str}'")
    return reference_date

def _calculate_days_between(start_date: str, end_date: str = None) -> int:
    """INTERNAL: Calculate days between two date strings (YYYY-MM-DD format)"""
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date:
            end = datetime.strptime(end_date, '%Y-%m-%d')
        else:
            end = datetime.now()
        
        return abs((end - start).days)
    except Exception:
        return 0

def _is_date_in_range(date_str: str, days_back: int) -> bool:
    """INTERNAL: Check if date is within specified range"""
    try:
        event_date = datetime.strptime(date_str, '%Y-%m-%d')
        cutoff = datetime.now() - timedelta(days=days_back)
        return event_date >= cutoff
    except Exception:
        return False

def _get_week_boundaries(date_str: str = None) -> tuple:
    """INTERNAL: Get start and end dates of the week containing the given date"""
    try:
        if date_str:
            target_date = datetime.strptime(date_str, '%Y-%m-%d')
        else:
            target_date = datetime.now()
        
        # Find Monday of the week
        monday = target_date - timedelta(days=target_date.weekday())
        sunday = monday + timedelta(days=6)
        
        return monday.strftime('%Y-%m-%d'), sunday.strftime('%Y-%m-%d')
    except Exception:
        # Fallback to current week
        now = datetime.now()
        monday = now - timedelta(days=now.weekday())
        sunday = monday + timedelta(days=6)
        return monday.strftime('%Y-%m-%d'), sunday.strftime('%Y-%m-%d')

def _format_time_ago(timestamp_str: str) -> str:
    """INTERNAL: Format how long ago something happened"""
    try:
        event_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        now = datetime.now()
        
        # Handle timezone-aware vs naive datetime
        if event_time.tzinfo is not None and now.tzinfo is None:
            import pytz
            now = pytz.UTC.localize(now)
        elif event_time.tzinfo is None and now.tzinfo is not None:
            now = now.replace(tzinfo=None)
        
        diff = now - event_time
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        else:
            return "just now"
            
    except Exception:
        return "unknown time"

def _resolve_relative_date_safe(text: str, now=None, tz_offset_minutes=None) -> tuple:
    """Return (YYYY-MM-DD, note). Handle today/yesterday/tomorrow, last/next weekday; capture tz offset."""
    if now is None:
        try:
            tz = pytz.timezone(USER_TIMEZONE)
            now = datetime.now(tz).replace(tzinfo=None)
        except:
            now = datetime.now()
    
    text = text.lower().strip()
    note = "parsed successfully"
    
    # Handle timezone offset if provided
    if tz_offset_minutes is not None:
        now = now + timedelta(minutes=tz_offset_minutes)
        note = f"adjusted for timezone offset: {tz_offset_minutes} minutes"
    
    # Basic patterns
    if text in ['today', 'now', 'right now', 'just now']:
        return now.strftime('%Y-%m-%d'), f"{note} (today)"
    elif text in ['yesterday', 'last night']:
        result_date = now - timedelta(days=1)
        return result_date.strftime('%Y-%m-%d'), f"{note} (yesterday)"
    elif text in ['tomorrow', 'later today', 'tonight']:
        result_date = now + timedelta(days=1)
        return result_date.strftime('%Y-%m-%d'), f"{note} (tomorrow)"
    
    # Weekday patterns
    days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    for i, day in enumerate(days_of_week):
        if day in text:
            current_weekday = now.weekday()
            days_until = (i - current_weekday) % 7
            
            if 'next' in text and days_until == 0:
                days_until = 7
            elif 'last' in text:
                if days_until == 0:
                    days_until = -7
                else:
                    days_until = days_until - 7
            elif days_until == 0:
                days_until = 0  # This weekday (today)
                
            result_date = now + timedelta(days=days_until)
            direction = "next" if days_until > 0 else "last" if days_until < 0 else "this"
            return result_date.strftime('%Y-%m-%d'), f"{note} ({direction} {day})"
    
    # Relative day patterns with safety caps
    try:
        # N days ago
        match = re.search(r'(\d+)\s+days?\s+ago', text)
        if match:
            days = min(int(match.group(1)), 365)  # Cap at 365 days
            result_date = now - timedelta(days=days)
            return result_date.strftime('%Y-%m-%d'), f"{note} ({days} days ago, capped at 365)"
        
        # N days from now
        match = re.search(r'(\d+)\s+days?\s+from\s+now', text)
        if match:
            days = min(int(match.group(1)), 365)
            result_date = now + timedelta(days=days)
            return result_date.strftime('%Y-%m-%d'), f"{note} ({days} days from now, capped at 365)"
        
        # N weeks ago
        match = re.search(r'(\d+)\s+weeks?\s+ago', text)
        if match:
            weeks = min(int(match.group(1)), 52)  # Cap at 52 weeks
            result_date = now - timedelta(weeks=weeks)
            return result_date.strftime('%Y-%m-%d'), f"{note} ({weeks} weeks ago, capped at 52)"
        
        # N hours ago
        match = re.search(r'(\d+)\s+hours?\s+ago', text)
        if match:
            hours = min(int(match.group(1)), 168)  # Cap at 1 week
            result_date = now - timedelta(hours=hours)
            return result_date.strftime('%Y-%m-%d'), f"{note} ({hours} hours ago, capped at 168)"
            
    except (ValueError, AttributeError) as e:
        note = f"error parsing numeric pattern: {e}"
    
    # Week-based patterns
    if 'last week' in text or 'a week ago' in text:
        result_date = now - timedelta(weeks=1)
        return result_date.strftime('%Y-%m-%d'), f"{note} (last week)"
    elif 'next week' in text:
        result_date = now + timedelta(weeks=1)
        return result_date.strftime('%Y-%m-%d'), f"{note} (next week)"
    elif 'this week' in text:
        # Start of this week (Monday)
        days_since_monday = now.weekday()
        result_date = now - timedelta(days=days_since_monday)
        return result_date.strftime('%Y-%m-%d'), f"{note} (start of this week)"
    
    # Month-based patterns
    if 'last month' in text:
        result_date = now - timedelta(days=30)
        return result_date.strftime('%Y-%m-%d'), f"{note} (last month, approx)"
    elif 'next month' in text:
        result_date = now + timedelta(days=30)
        return result_date.strftime('%Y-%m-%d'), f"{note} (next month, approx)"
    elif 'this month' in text:
        result_date = now.replace(day=1)
        return result_date.strftime('%Y-%m-%d'), f"{note} (start of this month)"
    
    # Safe fallback
    return now.strftime('%Y-%m-%d'), f"fallback to today - could not parse: '{text}'"

# Additional internal helpers for robust time parsing (edge-case hardening)
def _parse_time_range_robust(query: str) -> tuple:
    """Internal helper: Parse time range from query with robust handling"""
    try:
        tz = pytz.timezone(USER_TIMEZONE)
        base_date = datetime.now(tz).replace(tzinfo=None)
    except:
        base_date = datetime.now()
    
    query_lower = query.lower().strip()
    
    # Today
    if re.search(r'\btoday\b', query_lower):
        today = base_date.strftime('%Y-%m-%d')
        return (today, today)
    
    # Yesterday  
    if re.search(r'\byesterday\b', query_lower):
        yesterday = (base_date - timedelta(days=1)).strftime('%Y-%m-%d')
        return (yesterday, yesterday)
    
    # This week
    if re.search(r'\bthis week\b', query_lower):
        monday = base_date - timedelta(days=base_date.weekday())
        sunday = monday + timedelta(days=6)
        return (monday.strftime('%Y-%m-%d'), sunday.strftime('%Y-%m-%d'))
    
    # Last week
    if re.search(r'\blast week\b', query_lower):
        last_monday = base_date - timedelta(days=base_date.weekday() + 7)
        last_sunday = last_monday + timedelta(days=6)
        return (last_monday.strftime('%Y-%m-%d'), last_sunday.strftime('%Y-%m-%d'))
    
    # Last N days
    days_match = re.search(r'\blast\s+(\d+)\s+days?\b', query_lower)
    if days_match:
        days = int(days_match.group(1))
        start_date = base_date - timedelta(days=days-1)
        return (start_date.strftime('%Y-%m-%d'), base_date.strftime('%Y-%m-%d'))
    
    # Default to today if no range found
    today = base_date.strftime('%Y-%m-%d')
    return (today, today)

def _split_multi_events(text: str) -> list:
    """Internal helper: Split text that contains multiple events"""
    # Split on conjunctions that indicate separate events
    separators = [
        r'\band\s+then\b',
        r'\bafter\s+that\b', 
        r'\bthen\s+i\b',
        r'\balso\s+i\b',
        r'\.\s*i\s+also\b',
        r'\.\s*then\s+i\b',
        r'\band\s+i\s+also\b'
    ]
    
    parts = [text]
    for separator in separators:
        new_parts = []
        for part in parts:
            split_parts = re.split(separator, part, flags=re.IGNORECASE)
            new_parts.extend([p.strip() for p in split_parts if p.strip()])
        parts = new_parts
    
    # Filter out parts that are too short to be meaningful events
    meaningful_parts = [p for p in parts if len(p.split()) >= 3]
    
    return meaningful_parts if len(meaningful_parts) > 1 else [text]