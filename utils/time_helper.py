# utils/time_helper.py - Time helper functions for Buddy (July 2025)
"""
Time and location helper functions for consistent time handling
"""
from datetime import datetime
import pytz
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
    """INTERNAL: Parse relative date strings like 'yesterday', 'last week'"""
    if reference_date is None:
        reference_date = datetime.now()
    
    date_str = date_str.lower().strip()
    
    if date_str in ['today', 'now']:
        return reference_date
    elif date_str == 'yesterday':
        return reference_date - timedelta(days=1)
    elif date_str == 'tomorrow':
        return reference_date + timedelta(days=1)
    elif date_str in ['last week', 'a week ago']:
        return reference_date - timedelta(weeks=1)
    elif date_str in ['this week']:
        # Start of this week (Monday)
        days_since_monday = reference_date.weekday()
        return reference_date - timedelta(days=days_since_monday)
    elif 'days ago' in date_str:
        import re
        match = re.search(r'(\d+)\s+days?\s+ago', date_str)
        if match:
            days = int(match.group(1))
            return reference_date - timedelta(days=days)
    
    # Fallback - return reference date
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