# ai/human_memory_smart.py - Smart LLM-based life event detection
import json
import os
import random
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import re
from ai.memory import get_user_memory, add_to_conversation_history

class SmartHumanLikeMemory:
    """🧠 Smart human-like memory using LLM for event detection"""
    
    _lock = threading.Lock()  # class-level lock
    
    def __init__(self, username: str):
        self.username = username
        self.memory_dir = f"memory/{username}"
        os.makedirs(self.memory_dir, exist_ok=True)
        
        # Get the existing MEGA-INTELLIGENT memory system
        self.mega_memory = get_user_memory(username)
        
        # Smart memory storage
        self.appointments = self.load_memory('smart_appointments.json')
        self.life_events = self.load_memory('smart_life_events.json') 
        self.conversation_highlights = self.load_memory('smart_highlights.json')
        self.health_states = self.load_memory('smart_health_states.json')
        self.mood_states = self.load_memory('smart_mood_states.json')
        self.visits = self.load_memory('smart_visits.json')
        
        # Session tracking
        self.context_used_this_session = set()
        
        # Throttle marker (epoch seconds)
        self._last_tier3 = 0.0
        
        print(f"[SmartMemory] 🧠 Smart LLM-based memory initialized for {username}")
    
    def extract_and_store_human_memories(self, text: str):
        """🎯 Smart LLM-based memory extraction with BULLETPROOF filtering"""
        
        # Also use the existing MEGA-INTELLIGENT extraction
        self.mega_memory.extract_memories_from_text(text)
        
        # Tier-3 throttle + lock around heavy LLM path
        now = time.time()
        
        # Tier-3 throttle: skip heavy path if we ran it very recently
        if (now - self._last_tier3) < 8.0:  # 8s guard, adjust if needed
            print("[SmartMemory] ⏳ Throttled Tier-3 extraction")
            return
            
        with self._lock:
            self._last_tier3 = now
            
            # Normalize text for consistent processing
            normalized_text = self._normalize_text_for_memory(text)
            
            # Use LLM to intelligently detect events (only if passes all filters)
            detected_events = self._smart_detect_events(normalized_text)
            
            # Store detected events with JSON encoding safeguards
            for event in detected_events:
                try:
                    # Ensure proper JSON encoding
                    event = self._ensure_json_encodable(event)
                    
                    if event['type'] == 'appointment':
                        self.appointments.append(event)
                        print(f"[SmartMemory] 📅 Smart appointment: {event['topic']} on {event['date']}")
                    elif event['type'] == 'life_event':
                        self.life_events.append(event)
                        print(f"[SmartMemory] 📝 Smart life event: {event['topic']} on {event['date']} ({event['emotion']})")
                    elif event['type'] == 'highlight':
                        self.conversation_highlights.append(event)
                        print(f"[SmartMemory] 💬 Smart highlight: {event['topic']}")
                    elif event['type'] == 'health_state':
                        self.health_states.append(event)
                        print(f"[SmartMemory] 🏥 Health state: {event['topic']} - {event.get('state', 'unknown')} ({event.get('severity', 'N/A')})")
                    elif event['type'] == 'mood_state':
                        self.mood_states.append(event)
                        print(f"[SmartMemory] 😊 Mood state: {event['topic']} - {event.get('mood', 'unknown')} ({event.get('intensity', 'N/A')})")
                    elif event['type'] == 'visit':
                        self.visits.append(event)
                        print(f"[SmartMemory] 🏪 Visit: {event['topic']} at {event.get('location', 'unknown location')}")
                except Exception as e:
                    print(f"[SmartMemory] ❌ Event encoding error: {e}")
                    continue
            
            # Save memories with atomic write
            if detected_events:  # Only save if we actually found events
                self._atomic_save_memories()
    
    def _normalize_text_for_memory(self, text: str) -> str:
        """🔄 Normalize text for consistent memory processing"""
        if not text or not isinstance(text, str):
            return ""
            
        # Strip excessive whitespace
        normalized = ' '.join(text.strip().split())
        
        # Normalize common contractions for consistent processing
        contractions = {
            "i'm": "i am",
            "don't": "do not",
            "won't": "will not",
            "can't": "cannot",
            "it's": "it is",
            "that's": "that is",
            "we're": "we are",
            "they're": "they are"
        }
        
        normalized_lower = normalized.lower()
        for contraction, expansion in contractions.items():
            normalized_lower = normalized_lower.replace(contraction, expansion)
            
        return normalized_lower
    
    def _ensure_json_encodable(self, event: Dict) -> Dict:
        """🔒 Ensure event is JSON encodable"""
        encodable_event = {}
        
        for key, value in event.items():
            if isinstance(value, (str, int, float, bool, type(None))):
                encodable_event[key] = value
            elif isinstance(value, (list, tuple)):
                encodable_event[key] = [str(item) for item in value]
            elif isinstance(value, dict):
                encodable_event[key] = {str(k): str(v) for k, v in value.items()}
            else:
                encodable_event[key] = str(value)
                
        return encodable_event
    
    def _atomic_save_memories(self):
        """💾 Atomic save with backup recovery"""
        try:
            self.save_memory(self.appointments, 'smart_appointments.json')
            self.save_memory(self.life_events, 'smart_life_events.json') 
            self.save_memory(self.conversation_highlights, 'smart_highlights.json')
            self.save_memory(self.health_states, 'smart_health_states.json')
            self.save_memory(self.mood_states, 'smart_mood_states.json')
            self.save_memory(self.visits, 'smart_visits.json')
        except Exception as e:
            print(f"[SmartMemory] ❌ Atomic save error: {e}")
            # Could add backup recovery here if needed
    
    def _is_casual_conversation(self, text: str) -> bool:
        """🛡️ BULLETPROOF filter to block casual conversation from LLM"""
        text_lower = text.lower().strip()
        
        # Block ALL questions TO Buddy
        question_to_buddy_patterns = [
            r'how.+are.+you',           # "How are you today?"
            r'how.+you.+doing',         # "How you doing?"
            r'what.+about.+you',        # "What about you?"
            r'how.+your.+day',          # "How was your day?"
            r'what.+your.+plan',        # "What's your plan?"
            r'what.+you.+think',        # "What do you think?"
            r'do.+you.+know',           # "Do you know..."
            r'can.+you.+help',          # "Can you help me?"
            r'can.+you.+tell',          # "Can you tell me?"
            r'what.+is.+your',          # "What is your..."
            r'where.+are.+you',         # "Where are you?"
            r'what.+time.+is.+it',      # "What time is it?"
            r'tell.+me.+about',         # "Tell me about..."
            r'explain.+to.+me',         # "Explain to me..."
            r'how.+does.+this',         # "How does this work?"
            r'why.+is.+this',           # "Why is this..."
            r'what.+does.+this',        # "What does this mean?"
        ]
        
        # Block ALL greetings and pleasantries
        greeting_patterns = [
            r'^thanks?\s+buddy',        # "Thanks buddy"
            r'^thank\s+you',            # "Thank you"
            r'^hello\b',                # "Hello"
            r'^hi\b',                   # "Hi"
            r'^hey\b',                  # "Hey"
            r'^good\s+morning',         # "Good morning"
            r'^good\s+afternoon',       # "Good afternoon" 
            r'^good\s+evening',         # "Good evening"
            r'^good\s+night',           # "Good night"
            r'nice.+talking',           # "Nice talking to you"
            r'see.+you.+later',         # "See you later"
            r'goodbye',                 # "Goodbye"
            r'bye',                     # "Bye"
            r'talk.+to.+you.+later',    # "Talk to you later"
            r'catch.+you.+later',       # "Catch you later"
        ]
        
        # Block ALL casual responses
        casual_response_patterns = [
            r'i.+m.+(fine|good|okay|great|alright)',  # "I'm fine/good/okay/great"
            r'nothing.+much',           # "Nothing much"
            r'same.+here',              # "Same here"
            r'just.+(chatting|talking|chilling)',  # "Just chatting"
            r'not.+much',               # "Not much"
            r'pretty.+good',            # "Pretty good"
            r'doing.+(well|fine|good)', # "Doing well/fine/good"
            r'that.+s.+(cool|nice|great)', # "That's cool/nice/great"
            r'sounds.+(good|great|nice)', # "Sounds good/great/nice"
            r'i.+see',                  # "I see"
            r'oh.+(okay|ok|cool)',      # "Oh okay/ok/cool"
            r'gotcha',                  # "Gotcha"
            r'makes.+sense',            # "Makes sense"
        ]
        
        # Check ALL patterns
        all_patterns = question_to_buddy_patterns + greeting_patterns + casual_response_patterns
        
        for pattern in all_patterns:
            if re.search(pattern, text_lower):
                print(f"[SmartMemory] 🛡️ BLOCKED casual pattern '{pattern}' in: '{text}'")
                return True
        
        # Block if too short (less than 6 words for events)
        if len(text.split()) < 6:
            print(f"[SmartMemory] 🛡️ BLOCKED too short ({len(text.split())} words): '{text}'")
            return True
        
        # Block if it's a question (contains ?)
        if '?' in text:
            print(f"[SmartMemory] 🛡️ BLOCKED question mark detected: '{text}'")
            return True
        
        return False
    
    def _likely_contains_events(self, text: str) -> bool:
        """🎯 STRICT check - only allow if it DEFINITELY contains events"""
        text_lower = text.lower()
        
        # MUST contain time indicators
        time_indicators = [
            'tomorrow', 'today', 'tonight', 'this week', 'next week', 'this weekend',
            'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
            'this morning', 'this afternoon', 'this evening', 'later today',
            'in an hour', 'in a few hours', 'at ', 'o\'clock'
        ]
        
        has_time = any(indicator in text_lower for indicator in time_indicators)
        
        if not has_time:
            print(f"[SmartMemory] 🛡️ BLOCKED no time indicators: '{text}'")
            return False
        
        # MUST contain event keywords
        event_keywords = [
            # Appointments (specific)
            'appointment', 'meeting', 'dentist', 'doctor', 'surgery', 'hospital',
            'interview', 'class', 'lesson', 'session', 'therapy', 'vet',
            'haircut', 'massage', 'nail', 'beauty', 'spa',
            
            # Social events (specific)
            'birthday', 'party', 'wedding', 'funeral', 'visit', 'visiting',
            'going to', 'seeing', 'dinner', 'lunch', 'coffee', 'movie',
            'concert', 'date', 'sleepover', 'hang out', 'play date',
            
            # Work/school (specific)
            'work', 'job', 'school', 'exam', 'test', 'presentation', 
            'conference', 'training', 'orientation', 'review',
            
            # Travel (specific)
            'vacation', 'trip', 'flying', 'traveling', 'flight', 'train',
            'bus', 'driving to', 'pick up', 'drop off',
            
            # Actions with commitment
            'have to', 'need to', 'going for', 'scheduled', 'planned',
            'supposed to', 'meeting with', 'seeing', 'picking up'
        ]
        
        has_event = any(keyword in text_lower for keyword in event_keywords)
        
        if not has_event:
            print(f"[SmartMemory] 🛡️ BLOCKED no event keywords: '{text}'")
            return False
        
        # Additional validation - check for action verbs
        action_verbs = [
            'have', 'going', 'seeing', 'visiting', 'meeting', 'picking', 
            'dropping', 'starting', 'finishing', 'attending', 'scheduled'
        ]
        
        has_action = any(verb in text_lower for verb in action_verbs)
        
        if not has_action:
            print(f"[SmartMemory] 🛡️ BLOCKED no action verbs: '{text}'")
            return False
        
        print(f"[SmartMemory] ✅ PASSED all event filters: '{text}'")
        return True
    
    def _contains_emotional_state(self, text: str) -> bool:
        """🎯 Check for emotional states worth remembering"""
        text_lower = text.lower()
        
        emotion_keywords = [
            'stressed', 'worried', 'anxious', 'nervous', 'scared', 'upset',
            'excited', 'thrilled', 'happy', 'glad', 'pleased', 'proud',
            'sad', 'depressed', 'down', 'frustrated', 'angry', 'annoyed',
            'tired', 'exhausted', 'overwhelmed', 'confused', 'lost',
            'hopeful', 'optimistic', 'confident', 'motivated', 'inspired'
        ]
        
        return any(emotion in text_lower for emotion in emotion_keywords)
    
    def _contains_health_state(self, text: str) -> bool:
        """🏥 Check for health states worth remembering"""
        text_lower = text.lower()
        
        health_keywords = [
            'sick', 'unwell', 'ill', 'feel sick', 'not well', 'feeling bad',
            'headache', 'fever', 'cold', 'flu', 'cough', 'sore throat',
            'stomach ache', 'pain', 'hurt', 'aching', 'dizzy', 'nauseous',
            'feel better', 'feeling good', 'feel fine', 'recovered', 'healthy',
            'getting better', 'feeling worse', 'doctor', 'medicine', 'medication'
        ]
        
        return any(keyword in text_lower for keyword in health_keywords)
    
    def _contains_mood_state(self, text: str) -> bool:
        """😊 Check for mood states worth remembering"""
        text_lower = text.lower()
        
        # Look for "I'm/I am/feeling" followed by mood words
        mood_patterns = [
            r'\b(?:i\s?am|i\'m|feeling|feel)\s+(?:really\s+|very\s+|quite\s+|pretty\s+|so\s+|extremely\s+)?(happy|sad|angry|excited|tired|stressed|worried|calm|peaceful|frustrated|annoyed|content|proud|disappointed|anxious|nervous|confident|motivated|inspired|depressed|overwhelmed|confused|lost|hopeful|optimistic)',
            r'\b(?:today|right now|currently)\s+i\s+(?:am|feel)\s+(?:really\s+|very\s+)?(good|bad|great|terrible|awful|amazing|fantastic|horrible)'
        ]
        
        for pattern in mood_patterns:
            if re.search(pattern, text_lower):
                return True
        
        return False
    
    def _contains_visit_or_activity(self, text: str) -> bool:
        """🏪 Check for visits or activities worth remembering"""
        text_lower = text.lower()
        
        # Visit patterns
        visit_patterns = [
            r'\b(?:went to|going to|visited|at)\s+(?:the\s+)?([a-zA-Z\s]+?)(?:\s+(?:today|yesterday|tomorrow|this morning|this afternoon|tonight))?',
            r'\b(?:had|got|bought)\s+(?:some\s+|a\s+)?([a-zA-Z\s]+?)\s+(?:at|from)\s+([a-zA-Z\s]+)',
        ]
        
        for pattern in visit_patterns:
            if re.search(pattern, text_lower):
                return True
        
        # Activity keywords
        activity_keywords = [
            'mcdonalds', 'restaurant', 'cafe', 'coffee shop', 'store', 'shop',
            'mall', 'market', 'supermarket', 'gym', 'park', 'library',
            'went out', 'had lunch', 'had dinner', 'had coffee', 'went shopping'
        ]
        
        return any(keyword in text_lower for keyword in activity_keywords)
    
    def _smart_detect_events(self, text: str) -> List[Dict]:
        """🧠 Use Hermes 3 Pro Mistral to intelligently detect events - BULLETPROOF FILTERED"""
        
        # ✅ TRIPLE FILTERING SYSTEM - BULLETPROOF!
        
        # Filter 1: Block casual conversation
        if self._is_casual_conversation(text):
            return []
        
        # Filter 2: Must contain events OR emotions OR health OR mood OR visits
        has_events = self._likely_contains_events(text)
        has_emotions = self._contains_emotional_state(text)
        has_health = self._contains_health_state(text)
        has_mood = self._contains_mood_state(text)
        has_visits = self._contains_visit_or_activity(text)
        
        if not (has_events or has_emotions or has_health or has_mood or has_visits):
            print(f"[SmartMemory] 🛡️ BLOCKED no events, emotions, health, mood, or visits: '{text}'")
            return []
        
        # Filter 3: Final validation - must be substantial OR micro-event
        has_micro_events = has_health or has_mood or has_visits
        
        if not has_micro_events and len(text.split()) < 5:
            print(f"[SmartMemory] 🛡️ BLOCKED too short for events: '{text}'")
            return []
        
        # If we get here, it's worth LLM processing
        print(f"[SmartMemory] 🎯 APPROVED for LLM processing: '{text}'")
        
        current_date = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now().strftime('%H:%M')
        
        # Smart prompt for event detection
        detection_prompt = f"""You are a smart memory assistant. Analyze this user message and extract any events, appointments, life situations, health states, mood changes, or activities that should be remembered.

Current date: {current_date}
Current time: {current_time}
User message: "{text}"

Extract events in this exact JSON format (return empty array if no events):
[
  {{
    "type": "appointment|life_event|highlight|health_state|mood_state|visit",
    "topic": "brief_description",
    "date": "YYYY-MM-DD",
    "time": "HH:MM" or null,
    "emotion": "happy|excited|stressful|sensitive|casual|supportive|neutral",
    "priority": "high|medium|low",
    "state": "unwell|well|happy|sad|stressed|tired|calm" (for health_state/mood_state),
    "severity": "mild|moderate|severe" (for health_state only),
    "symptoms": ["headache", "fever"] (for health_state only),
    "mood": "happy|sad|angry|excited|tired|stressed|calm" (for mood_state only),
    "intensity": "mild|moderate|intense" (for mood_state only),
    "location": "place_name" (for visits),
    "people": ["person1", "person2"] (who was involved),
    "items": ["item1", "item2"] (for visits/purchases),
    "original_text": "{text}"
  }}
]

Event Types:
- "appointment": Time-specific events (dentist, meeting, class)
- "life_event": Emotional/social events (birthdays, visits, funerals)  
- "highlight": General feelings/thoughts to remember
- "health_state": Health conditions ("I'm sick", "feeling better", "have a headache")
- "mood_state": Mood/emotional states ("I'm happy", "feeling stressed", "really tired today")
- "visit": Places visited or activities ("went to McDonald's", "had coffee at cafe")

Guidelines:
- Calculate dates: tomorrow = {(datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')}
- Be smart about natural language: "going to Emily's tomorrow, it's her birthday" = birthday visit
- For health_state: include symptoms array and severity if mentioned
- For mood_state: include intensity if mentioned (very happy = intense)
- For visits: include location and any people/items mentioned
- Priority: high=urgent/sensitive, medium=social/fun, low=routine
- ONLY extract if it's a REAL event, state, or activity worth remembering
- DO NOT extract casual conversation, greetings, or questions

Examples:
"I have dentist tomorrow at 2PM" → appointment, dentist, tomorrow, 14:00, stressful, medium
"Going to Emily's tomorrow, it's her birthday" → life_event, Emily's birthday visit, tomorrow, happy, medium
"I'm really stressed about work" → highlight, work stress, today, supportive, low
"I'm feeling sick today, have a headache" → health_state, feeling sick, today, state=unwell, severity=mild, symptoms=[headache]
"I'm so happy right now!" → mood_state, happy mood, today, mood=happy, intensity=intense
"Went to McDonald's for lunch" → visit, McDonald's visit, today, location=McDonald's

Return only valid JSON array:"""

        try:
            # Local import to avoid future cycles
            from ai.chat import ask_kobold
            
            # Get LLM response
            messages = [
                {"role": "system", "content": "You are a precise JSON extraction assistant. Return only valid JSON arrays. Extract ONLY real events, appointments, or emotional states worth remembering."},
                {"role": "user", "content": detection_prompt}
            ]
            
            llm_response = ask_kobold(messages, max_tokens=300)
            
            # Clean and parse JSON response
            json_text = self._extract_json_from_response(llm_response)
            
            if json_text:
                events = json.loads(json_text)
                
                # Validate and enhance events
                validated_events = []
                for event in events:
                    if self._validate_event(event):
                        enhanced_event = self._enhance_event(event, text=text)
                        validated_events.append(enhanced_event)
                
                print(f"[SmartMemory] 🧠 LLM detected {len(validated_events)} events from: '{text}'")
                return validated_events
            
        except Exception as e:
            print(f"[SmartMemory] ⚠️ LLM detection error: {e}")
            # Fallback to simple regex for critical patterns
            return self._fallback_detection(text)
        
        return []
    
    def _extract_json_from_response(self, response: str) -> Optional[str]:
        """Extract JSON array from LLM response"""
        try:
            # Look for JSON array in response
            import re
            
            # Find JSON array pattern
            json_match = re.search(r'\[.*?\]', response, re.DOTALL)
            if json_match:
                return json_match.group(0)
            
            # Look for individual JSON objects and wrap in array
            obj_matches = re.findall(r'\{.*?\}', response, re.DOTALL)
            if obj_matches:
                return '[' + ','.join(obj_matches) + ']'
            
        except Exception as e:
            print(f"[SmartMemory] JSON extraction error: {e}")
        
        return None
    
    def _validate_event(self, event: Dict) -> bool:
        """Validate event has required fields"""
        required_fields = ['type', 'topic', 'date', 'emotion']
        return all(field in event for field in required_fields)
    
    def _enhance_event(self, event: Dict, *, text: str = "") -> Dict:
        """🔧 Enhanced normalization ensuring unified field structure for ALL events"""
        now_iso = datetime.now().isoformat()
        etype = event.get('type', 'highlight')
        
        # Base unified structure - EVERY event gets ALL these fields
        enhanced = {
            # Core identification
            'id': event.get('id') or f"{etype}_{int(time.time()*1000)}",
            'type': etype,
            'topic': event.get('topic', 'unknown'),
            'category': event.get('category') or self._determine_category(etype),
            
            # Temporal fields
            'date': event.get('date', datetime.now().strftime('%Y-%m-%d')),
            'time': event.get('time'),
            'created': now_iso,
            'last_updated': now_iso,
            
            # Contextual fields
            'location': event.get('location'),
            'people': event.get('people') or [],
            'details': event.get('details'),
            'original_text': event.get('original_text', text),
            
            # Emotional/priority fields
            'emotion': event.get('emotion', 'neutral'),
            'priority': event.get('priority', 'medium'),
            'status': event.get('status', 'pending'),
            
            # Micro-event specific fields
            'state': event.get('state'),  # for health_state/mood_state
            'severity': event.get('severity'),  # for health_state
            'symptoms': event.get('symptoms') or [],  # for health_state
            'mood': event.get('mood'),  # for mood_state
            'intensity': event.get('intensity'),  # for mood_state
            'items': event.get('items') or [],  # for visits/purchases
            
            # Meta fields
            'detected_by': event.get('detected_by', 'llm'),
            'user': self.username,
        }
        
        return enhanced
    
    def _determine_category(self, event_type: str) -> str:
        """🏷️ Determine appropriate category based on event type"""
        category_mapping = {
            'appointment': 'appointment',
            'life_event': 'life_event', 
            'highlight': 'highlight',
            'health_state': 'health',
            'mood_state': 'mood',
            'visit': 'activity'
        }
        return category_mapping.get(event_type, 'highlight')
    
    def _fallback_detection(self, text: str) -> List[Dict]:
        """Simple fallback detection for critical patterns"""
        events = []
        text_lower = text.lower()
        current_date = datetime.now().strftime('%Y-%m-%d')
        tomorrow_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Only critical patterns with time
        if re.search(r'(?:dentist|doctor|appointment|meeting).+(?:tomorrow|today).+(?:\d{1,2}(?::\d{2})?(?:\s?(?:am|pm|AM|PM))?|\d{1,2}\s?(?:am|pm|AM|PM))', text_lower):
            base_event = {
                'type': 'appointment',
                'topic': 'appointment',
                'date': tomorrow_date if 'tomorrow' in text_lower else current_date,
                'emotion': 'casual',
                'original_text': text,
                'detected_by': 'fallback'
            }
            events.append(self._enhance_event(base_event, text=text))
        
        # Only birthday with specific person
        birthday_match = re.search(r'(\w+)(?:\'s)?\s+birthday.+(?:tomorrow|today)', text_lower)
        if birthday_match:
            person = birthday_match.group(1)
            base_event = {
                'type': 'life_event',
                'topic': f'{person}_birthday',
                'date': tomorrow_date if 'tomorrow' in text_lower else current_date,
                'emotion': 'happy',
                'original_text': text,
                'detected_by': 'fallback'
            }
            events.append(self._enhance_event(base_event, text=text))
        
        # Simple health state detection
        if re.search(r'\b(?:i\s?am|i\'m|feeling)\s+(?:really\s+|very\s+)?(?:sick|unwell|ill|not well)', text_lower):
            base_event = {
                'type': 'health_state',
                'topic': 'feeling unwell',
                'date': current_date,
                'state': 'unwell',
                'emotion': 'supportive',
                'original_text': text,
                'detected_by': 'fallback'
            }
            events.append(self._enhance_event(base_event, text=text))
        
        # Simple mood state detection
        mood_match = re.search(r'\b(?:i\s?am|i\'m|feeling)\s+(?:really\s+|very\s+|quite\s+|so\s+)?(happy|sad|stressed|tired|excited|angry|frustrated|worried)', text_lower)
        if mood_match:
            mood = mood_match.group(1)
            base_event = {
                'type': 'mood_state',
                'topic': f'feeling {mood}',
                'date': current_date,
                'mood': mood,
                'emotion': 'supportive',
                'original_text': text,
                'detected_by': 'fallback'
            }
            events.append(self._enhance_event(base_event, text=text))
        
        return events
    
    def load_memory(self, filename: str) -> List[Dict]:
        """Load memory file"""
        file_path = os.path.join(self.memory_dir, filename)
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"[SmartMemory] ⚠️ Error loading {filename}: {e}")
            return []
    
    def save_memory(self, data: List[Dict], filename: str):
        """Save memory file"""
        file_path = os.path.join(self.memory_dir, filename)
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[SmartMemory] ❌ Error saving {filename}: {e}")
    
    def check_for_natural_context_response(self) -> Optional[str]:
        """🎯 Check if we should naturally bring up memories"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Check appointments first (time-sensitive)
        response = self._check_smart_appointments(today)
        if response:
            return response
        
        # Check life events 
        response = self._check_smart_life_events(today)
        if response:
            return response
        
        # Check health states
        response = self._check_health_states()
        if response:
            return response
        
        # Check mood states
        response = self._check_mood_states()
        if response:
            return response
        
        # Check visits
        response = self._check_visits()
        if response:
            return response
        
        # Check conversation highlights (occasionally)
        if random.random() < 0.2:  # 20% chance
            response = self._check_smart_highlights()
            if response:
                return response
        
        return None
    
    def _check_smart_appointments(self, today: str) -> Optional[str]:
        """📅 Check smart appointments"""
        for appointment in self.appointments:
            if appointment['date'] == today and appointment['status'] == 'pending':
                topic = appointment['topic']
                time_str = appointment.get('time', '')
                
                context_key = f"appointment_{appointment['date']}_{topic}"
                if context_key in self.context_used_this_session:
                    continue
                
                self.context_used_this_session.add(context_key)
                
                if time_str:
                    if 'dentist' in topic.lower():
                        responses = [
                            f"Yo! Just a heads up — {topic} at {time_str}. You ready for the drill?",
                            f"Hey, don't forget your {topic} at {time_str}! Try not to chicken out"
                        ]
                    else:
                        responses = [
                            f"Heads up — {topic} at {time_str} today. You got this!",
                            f"Don't forget your {topic} at {time_str}!"
                        ]
                else:
                    responses = [
                        f"Hey, you've got {topic} today. How you feeling about it?",
                        f"Don't forget about {topic} today!"
                    ]
                
                appointment['status'] = 'reminded'
                self.save_memory(self.appointments, 'smart_appointments.json')
                
                return random.choice(responses)
        
        return None
    
    def _check_smart_life_events(self, today: str) -> Optional[str]:
        """📝 Check smart life events"""
        for event in self.life_events:
            if event['date'] == today and event['status'] == 'pending':
                topic = event['topic']
                emotion = event['emotion']
                
                context_key = f"life_event_{event['date']}_{topic}"
                if context_key in self.context_used_this_session:
                    continue
                
                self.context_used_this_session.add(context_key)
                
                if emotion == 'sensitive':
                    responses = [
                        f"Hey, how'd the {topic} go? You alright?",
                        f"Just checking — how was the {topic}? You doing okay?"
                    ]
                elif emotion in ['happy', 'excited']:
                    responses = [
                        f"Yooo! How was the {topic}? Tell me everything!",
                        f"How'd the {topic} go?! Was it awesome?"
                    ]
                elif emotion == 'stressful':
                    responses = [
                        f"So how'd the {topic} go? You survive?",
                        f"How was the {topic}? Hope it went better than expected!"
                    ]
                else:
                    responses = [
                        f"How'd the {topic} go?",
                        f"So, how was your {topic}?"
                    ]
                
                event['status'] = 'followed_up'
                self.save_memory(self.life_events, 'smart_life_events.json')
                
                return random.choice(responses)
        
        return None
    
    def _check_smart_highlights(self) -> Optional[str]:
        """💬 Check smart conversation highlights"""
        recent_highlights = []
        cutoff_date = datetime.now() - timedelta(days=3)
        
        for highlight in self.conversation_highlights:
            created = datetime.fromisoformat(highlight['created'])
            if created >= cutoff_date and highlight['status'] == 'pending':
                context_key = f"highlight_{highlight['topic']}_{highlight['created'][:10]}"
                if context_key not in self.context_used_this_session:
                    recent_highlights.append(highlight)
        
        if recent_highlights:
            highlight = random.choice(recent_highlights)
            topic = highlight['topic']
            
            context_key = f"highlight_{topic}_{highlight['created'][:10]}"
            self.context_used_this_session.add(context_key)
            
            responses = [
                f"Hey, how's that {topic} situation going?",
                f"Any updates on {topic}?"
            ]
            
            highlight['status'] = 'followed_up'
            self.save_memory(self.conversation_highlights, 'smart_highlights.json')
            
            return random.choice(responses)
        
        return None
    
    def reset_session_context(self):
        """Reset session context"""
        self.context_used_this_session.clear()
        print(f"[SmartMemory] 🔄 Session context reset for {self.username}")
    
    def _check_health_states(self) -> Optional[str]:
        """🏥 Check recent health states for follow-up"""
        recent_health = []
        cutoff_date = datetime.now() - timedelta(days=2)  # Check last 2 days
        
        for health in self.health_states:
            created = datetime.fromisoformat(health['created'])
            if created >= cutoff_date and health['status'] == 'pending':
                context_key = f"health_{health['topic']}_{health['created'][:10]}"
                if context_key not in self.context_used_this_session:
                    recent_health.append(health)
        
        if recent_health and random.random() < 0.3:  # 30% chance
            health = random.choice(recent_health)
            topic = health['topic']
            state = health.get('state', 'unknown')
            
            context_key = f"health_{topic}_{health['created'][:10]}"
            self.context_used_this_session.add(context_key)
            
            if state == 'unwell':
                responses = [
                    f"Hey, how are you feeling? Still {topic.replace('feeling ', '')}?",
                    f"Are you feeling any better today? You mentioned {topic}.",
                ]
            else:
                responses = [
                    f"Good to hear you're {topic}! How are you doing today?",
                ]
            
            health['status'] = 'followed_up'
            self.save_memory(self.health_states, 'smart_health_states.json')
            
            return random.choice(responses)
        
        return None
    
    def _check_mood_states(self) -> Optional[str]:
        """😊 Check recent mood states for follow-up"""
        recent_moods = []
        cutoff_date = datetime.now() - timedelta(days=1)  # Check last day
        
        for mood_state in self.mood_states:
            created = datetime.fromisoformat(mood_state['created'])
            if created >= cutoff_date and mood_state['status'] == 'pending':
                context_key = f"mood_{mood_state['topic']}_{mood_state['created'][:10]}"
                if context_key not in self.context_used_this_session:
                    recent_moods.append(mood_state)
        
        if recent_moods and random.random() < 0.2:  # 20% chance
            mood_state = random.choice(recent_moods)
            topic = mood_state['topic']
            mood = mood_state.get('mood', 'unknown')
            
            context_key = f"mood_{topic}_{mood_state['created'][:10]}"
            self.context_used_this_session.add(context_key)
            
            if mood in ['sad', 'stressed', 'angry', 'frustrated', 'worried']:
                responses = [
                    f"How are you feeling now? You seemed {mood} earlier.",
                    f"Hope you're feeling better than when you were {mood}.",
                ]
            else:
                responses = [
                    f"Still {mood}? That's awesome!",
                    f"How's your mood today? You seemed {mood} before.",
                ]
            
            mood_state['status'] = 'followed_up'
            self.save_memory(self.mood_states, 'smart_mood_states.json')
            
            return random.choice(responses)
        
        return None
    
    def _check_visits(self) -> Optional[str]:
        """🏪 Check recent visits for follow-up"""
        recent_visits = []
        cutoff_date = datetime.now() - timedelta(days=3)  # Check last 3 days
        
        for visit in self.visits:
            created = datetime.fromisoformat(visit['created'])
            if created >= cutoff_date and visit['status'] == 'pending':
                context_key = f"visit_{visit['topic']}_{visit['created'][:10]}"
                if context_key not in self.context_used_this_session:
                    recent_visits.append(visit)
        
        if recent_visits and random.random() < 0.15:  # 15% chance
            visit = random.choice(recent_visits)
            topic = visit['topic']
            location = visit.get('location', 'somewhere')
            
            context_key = f"visit_{topic}_{visit['created'][:10]}"
            self.context_used_this_session.add(context_key)
            
            responses = [
                f"How was your visit to {location}?",
                f"Did you enjoy {topic}?",
                f"Any interesting finds at {location}?",
            ]
            
            visit['status'] = 'followed_up'
            self.save_memory(self.visits, 'smart_visits.json')
            
            return random.choice(responses)
        
        return None