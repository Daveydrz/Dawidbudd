# ai/human_memory_smart.py - Robust Human-Like Memory System with Provenance & Episode Stitching
import json
import os
import random
import threading
import time
import hashlib
import difflib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Set
import re
from ai.memory import get_user_memory, add_to_conversation_history

# Cross-conversation reference patterns (stdlib only)
EXPLICIT_REF_PATTERNS = [
    r"\bwhen i went to (?P<location>[^.,!?\n]+)",
    r"\bthat (?P<event>appointment|meeting|visit|party|dinner|lunch|trip) (?:i|we) (?:had|went to|did)",
    r"\bthe (?P<person>[A-Z][a-zA-Z]+)'s (?P<event>birthday|wedding|party|funeral)",
    r"\bremember when (?:i|we) (?P<activity>[^.,!?\n]+)",
    r"\blast (?P<timeframe>week|month|year) when (?:i|we) (?P<activity>[^.,!?\n]+)",
    r"\bthat time (?:i|we) (?P<activity>went to|visited|saw|met|had) (?P<target>[^.,!?\n]+)",
    r"\bafter (?:my|our|the) (?P<event>appointment|meeting|visit|trip) (?:to|at|with) (?P<target>[^.,!?\n]+)",
    r"\bbefore (?:my|our|the) (?P<event>appointment|meeting|visit|trip) (?:to|at|with) (?P<target>[^.,!?\n]+)",
    r"\bsince (?:i|we) (?P<activity>went to|visited|saw|met) (?P<target>[^.,!?\n]+)",
    r"\bwhen (?:i|we) were (?:at|in) (?P<location>[^.,!?\n]+)",
    r"\bthat (?P<place>restaurant|cafe|shop|store|mall|gym|park|hospital|clinic) (?:i|we) (?:went to|visited)"
]

# TTL policies (in seconds) for different event types
TTL_POLICIES = {
    'health_state': 7 * 24 * 3600,      # 7 days
    'mood_state': 3 * 24 * 3600,        # 3 days  
    'visit': 30 * 24 * 3600,            # 30 days
    'appointment': 365 * 24 * 3600,     # 1 year
    'life_event': -1,                   # Permanent (no expiry)
    'highlight': 14 * 24 * 3600,        # 14 days
    'default': 30 * 24 * 3600           # 30 days default
}

# Episode stitching window (in seconds)
EPISODE_WINDOW = 30 * 60  # 30 minutes

# Confidence decay rate per day
CONFIDENCE_DECAY_RATE = 0.02  # 2% per day

# Salience scoring weights
SALIENCE_WEIGHTS = {
    'emotion_intensity': 0.3,
    'goal_relevance': 0.25, 
    'novelty': 0.25,
    'social_significance': 0.2
}

class SmartHumanLikeMemory:
    """🧠 Smart human-like memory using LLM for event detection"""
    
    _lock = threading.Lock()  # class-level lock
    
    def __init__(self, username: str):
        self.username = username
        self.memory_dir = f"memory/{username}"
        os.makedirs(self.memory_dir, exist_ok=True)
        
        # Get the existing MEGA-INTELLIGENT memory system
        self.mega_memory = get_user_memory(username)
        
        # Smart memory storage with enhanced structure
        self.appointments = self.load_memory('smart_appointments.json')
        self.life_events = self.load_memory('smart_life_events.json') 
        self.conversation_highlights = self.load_memory('smart_highlights.json')
        self.health_states = self.load_memory('smart_health_states.json')
        self.mood_states = self.load_memory('smart_mood_states.json')
        self.visits = self.load_memory('smart_visits.json')
        
        # Episode tracking for cross-conversation linking
        self.episodes = self.load_memory('episodes.json')
        self.episode_index = self.load_memory('episode_index.json')  # Fast lookup
        
        # Hypothesis memories for uncertain events
        self.hypothesis_memories = self.load_memory('hypothesis_memories.json')
        
        # Personal knowledge graph
        self.knowledge_graph = self.load_memory('knowledge_graph.json')
        if not self.knowledge_graph:
            self.knowledge_graph = {
                'entities': {},      # person/place/thing -> properties  
                'relationships': [], # entity1 -> relation -> entity2
                'concepts': {}       # abstract concepts and associations
            }
        
        # Audit log for provenance (append-only)
        self.audit_log_file = os.path.join(self.memory_dir, 'audit_log.jsonl')
        
        # Session tracking
        self.context_used_this_session = set()
        self.current_episode_id = self._generate_episode_id()
        
        # Throttle marker (epoch seconds)
        self._last_tier3 = 0.0
        
        print(f"[SmartMemory] 🧠 Robust human-like memory initialized for {username}")
        print(f"[SmartMemory] 📊 Episodes: {len(self.episodes)}, Current episode: {self.current_episode_id}")
        
        # Clean up expired memories on startup
        self._cleanup_expired_memories()
        
        # Edge-case hardening: low-confidence clarifications and corrections
        self.pending_clarifications = self.load_memory('pending_clarifications.json')
        self.correction_history = self.load_memory('correction_history.json')
        self.alias_mappings = self.load_memory('alias_mappings.json')
        if not self.alias_mappings:
            self.alias_mappings = {'people': {}, 'places': {}, 'activities': {}}
    
    
    def _generate_episode_id(self) -> str:
        """Generate stable episode ID based on current time window"""
        now = datetime.now()
        # Create 2-hour time windows for episode grouping
        window_start = now.replace(minute=0, second=0, microsecond=0)
        if now.hour % 2 == 1:
            window_start = window_start.replace(hour=now.hour - 1)
        
        timestamp = int(window_start.timestamp())
        return f"ep_{self.username}_{timestamp}"
    
    def _generate_fingerprint(self, text: str, event_type: str = "") -> str:
        """Generate fingerprint for deduplication and similarity detection"""
        # Normalize text for consistent fingerprinting
        normalized = re.sub(r'[^\w\s]', '', text.lower().strip())
        normalized = re.sub(r'\s+', ' ', normalized)
        
        # Include event type in fingerprint for better differentiation
        content = f"{event_type}:{normalized}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def _pattern_based_detection(self, text: str) -> List[Dict]:
        """Pass 1: Pattern-based extraction using regex and heuristics"""
        candidates = []
        text_lower = text.lower()
        
        # Health state patterns
        health_patterns = [
            (r'\b(?:i\s*am|i\'m|feeling|feel)\s+(sick|unwell|ill|better|fine|good|bad)', 'health_state'),
            (r'\b(?:have|got)\s+(headache|fever|cold|flu|cough|pain)', 'health_state'),
            (r'\b(?:doctor|medicine|medication|hospital|clinic)', 'appointment')
        ]
        
        for pattern, event_type in health_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                candidate = {
                    'type': event_type,
                    'topic': match.group(0),
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'source': 'pattern',
                    'field_confidence': {'type': 0.8, 'topic': 0.7, 'date': 0.9}
                }
                
                if event_type == 'health_state':
                    state = 'unwell' if match.group(1) in ['sick', 'unwell', 'ill', 'bad'] else 'well'
                    candidate['state'] = state
                    candidate['field_confidence']['state'] = 0.8
                
                candidates.append(candidate)
        
        # Mood state patterns
        mood_patterns = [
            (r'\b(?:i\s*am|i\'m|feeling|feel)\s+(happy|sad|angry|excited|tired|stressed|worried|calm)', 'mood_state'),
        ]
        
        for pattern, event_type in mood_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                candidate = {
                    'type': event_type,
                    'topic': f"Feeling {match.group(1)}",
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'mood': match.group(1),
                    'source': 'pattern',
                    'field_confidence': {'type': 0.8, 'topic': 0.7, 'date': 0.9, 'mood': 0.8}
                }
                candidates.append(candidate)
        
        # Visit patterns
        visit_patterns = [
            (r'\b(?:went to|going to|visited|at)\s+(?:the\s+)?([a-zA-Z\s]+)', 'visit'),
        ]
        
        for pattern, event_type in visit_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                location = match.group(1).strip()
                if len(location) > 2:  # Filter out very short matches
                    candidate = {
                        'type': event_type,
                        'topic': f"Visit to {location}",
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'location': location.title(),
                        'source': 'pattern',
                        'field_confidence': {'type': 0.7, 'topic': 0.6, 'date': 0.9, 'location': 0.7}
                    }
                    candidates.append(candidate)
        
        return candidates
    
    def _heuristic_detection(self, text: str) -> List[Dict]:
        """Pass 2: Heuristic-based extraction using keywords and rules"""
        candidates = []
        text_lower = text.lower()
        
        # Health keywords
        if self._contains_health_state(text):
            candidate = {
                'type': 'health_state',
                'topic': 'Health state mentioned',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'heuristic',
                'field_confidence': {'type': 0.6, 'topic': 0.5, 'date': 0.9}
            }
            
            # Determine state
            negative_health = ['sick', 'unwell', 'ill', 'pain', 'hurt', 'bad', 'worse']
            positive_health = ['better', 'fine', 'good', 'recovered', 'healthy']
            
            if any(word in text_lower for word in negative_health):
                candidate['state'] = 'unwell'
                candidate['field_confidence']['state'] = 0.6
            elif any(word in text_lower for word in positive_health):
                candidate['state'] = 'well'
                candidate['field_confidence']['state'] = 0.6
            
            candidates.append(candidate)
        
        # Mood keywords
        if self._contains_mood_state(text):
            candidate = {
                'type': 'mood_state',
                'topic': 'Mood state mentioned',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'heuristic',
                'field_confidence': {'type': 0.6, 'topic': 0.5, 'date': 0.9}
            }
            candidates.append(candidate)
        
        # Visit keywords  
        if self._contains_visit_or_activity(text):
            candidate = {
                'type': 'visit',
                'topic': 'Activity or visit mentioned',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'heuristic',
                'field_confidence': {'type': 0.6, 'topic': 0.5, 'date': 0.9}
            }
            candidates.append(candidate)
        
        return candidates
    
    def _fuse_candidates(self, candidates: List[Dict], text: str) -> List[Dict]:
        """Fuse multiple candidates per field with highest confidence wins"""
        if not candidates:
            return []
        
        # Group candidates by type and similarity
        grouped_candidates = {}
        
        for candidate in candidates:
            event_type = candidate.get('type', 'highlight')
            topic_key = candidate.get('topic', 'unknown')
            
            # Create grouping key based on type and topic similarity
            group_key = f"{event_type}:{self._norm(topic_key)[:20]}"
            
            if group_key not in grouped_candidates:
                grouped_candidates[group_key] = []
            grouped_candidates[group_key].append(candidate)
        
        # Fuse each group
        fused_events = []
        
        for group_key, group_candidates in grouped_candidates.items():
            if len(group_candidates) == 1:
                # Single candidate - just add consensus metadata
                event = group_candidates[0].copy()
                event['confidence'] = self._calculate_overall_confidence(event.get('field_confidence', {}))
                event['source'] = event.get('source', 'single')
                event['evidence'] = [{'method': event.get('source'), 'confidence': event['confidence']}]
                fused_events.append(event)
            else:
                # Multiple candidates - perform field-level fusion
                fused_event = self._fuse_field_level(group_candidates, text)
                fused_events.append(fused_event)
        
        return fused_events
    
    def _fuse_field_level(self, candidates: List[Dict], text: str) -> Dict:
        """Fuse candidates at field level, choosing highest confidence for each field"""
        # Get all possible fields
        all_fields = set()
        for candidate in candidates:
            all_fields.update(candidate.keys())
            if 'field_confidence' in candidate:
                all_fields.update(candidate['field_confidence'].keys())
        
        # Remove meta fields
        all_fields.discard('field_confidence')
        all_fields.discard('source')
        all_fields.discard('evidence')
        
        fused_event = {}
        field_confidences = {}
        evidence = []
        critical_conflicts = []
        
        # For each field, pick the value with highest confidence
        for field in all_fields:
            best_value = None
            best_confidence = 0.0
            field_sources = []
            
            for candidate in candidates:
                if field in candidate and candidate[field] is not None:
                    candidate_confidence = candidate.get('field_confidence', {}).get(field, 0.5)
                    if candidate_confidence > best_confidence:
                        best_confidence = candidate_confidence
                        best_value = candidate[field]
                    
                    field_sources.append({
                        'method': candidate.get('source', 'unknown'),
                        'value': candidate[field],
                        'confidence': candidate_confidence
                    })
            
            if best_value is not None:
                fused_event[field] = best_value
                field_confidences[field] = best_confidence
                
                # Check for critical conflicts
                if field in ['date', 'location', 'state'] and len(field_sources) > 1:
                    values = [s['value'] for s in field_sources]
                    if len(set(values)) > 1 and best_confidence < 0.6:
                        critical_conflicts.append(field)
        
        # Calculate overall confidence
        overall_confidence = self._calculate_overall_confidence(field_confidences)
        
        # Stealth confirmation policy: Set internal flags without user prompts
        if critical_conflicts and overall_confidence < 0.6:
            fused_event['_needs_confirmation'] = True
            fused_event['_conflict_fields'] = critical_conflicts
            fused_event['_stealth_hint'] = self._build_stealth_hint(fused_event, critical_conflicts, text)
        
        # Add metadata
        fused_event['confidence'] = overall_confidence
        fused_event['source'] = 'consensus'
        fused_event['field_confidence'] = field_confidences
        
        # Build evidence trail
        for candidate in candidates:
            evidence.append({
                'method': candidate.get('source', 'unknown'),
                'confidence': self._calculate_overall_confidence(candidate.get('field_confidence', {})),
                'fields_contributed': [f for f in candidate.keys() if f not in ['field_confidence', 'source']]
            })
        
        fused_event['evidence'] = evidence
        
        return fused_event
    
    def _build_stealth_hint(self, event: Dict, conflicts: List[str], text: str) -> str:
        """Build stealth hint for uncertain events without user prompts"""
        hints = []
        
        if 'date' in conflicts:
            hints.append("unclear when this happened")
        if 'location' in conflicts:
            hints.append("uncertain about the location")
        if 'state' in conflicts:
            hints.append("ambiguous health/mood state")
        
        event_type = event.get('type', 'event')
        topic = event.get('topic', 'something')
        
        if hints:
            hint_text = f"Remember {topic} but {' and '.join(hints)}"
        else:
            hint_text = f"Low confidence about {topic} details"
        
        return hint_text
    
    def _calculate_overall_confidence(self, field_confidences: Dict[str, float]) -> float:
        """Calculate overall confidence from field confidences"""
        if not field_confidences:
            return 0.5
        
        # Weight important fields more heavily
        field_weights = {
            'type': 0.2,
            'topic': 0.15,
            'date': 0.15,
            'location': 0.1,
            'state': 0.1,
            'mood': 0.1,
            'people': 0.1,
            'time': 0.1
        }
        
        weighted_sum = 0.0
        total_weight = 0.0
        
        for field, confidence in field_confidences.items():
            weight = field_weights.get(field, 0.05)  # Default weight for other fields
            weighted_sum += confidence * weight
            total_weight += weight
        
        if total_weight == 0:
            return 0.5
        
        return min(1.0, weighted_sum / total_weight)
    
    def _store_hypothesis_memory(self, event: Dict, text: str):
        """Store uncertain event as hypothesis for later confirmation"""
        hypothesis = {
            'id': f"hyp_{int(time.time()*1000)}",
            'event': event,
            'original_text': text,
            'created': datetime.now().isoformat(),
            'status': 'pending',  # pending, confirmed, rejected
            'confidence': event.get('confidence', 0.5),
            'conflict_fields': event.get('_conflict_fields', []),
            'confirmation_attempts': 0,
            'evidence_for': [],
            'evidence_against': []
        }
        
        self.hypothesis_memories.append(hypothesis)
        
        # Log hypothesis creation
        self._add_to_audit_log('hypothesis_create', hypothesis)
        
        print(f"[SmartMemory] 🤔 Hypothesis stored: {event.get('topic', 'unknown')}")
    
    def _update_knowledge_graph(self, event: Dict):
        """Update personal knowledge graph with event information"""
        try:
            # Extract entities from event
            entities = []
            
            # People
            if event.get('people'):
                for person in event['people']:
                    entities.append({'name': person, 'type': 'person'})
            
            # Locations
            if event.get('location'):
                entities.append({'name': event['location'], 'type': 'place'})
            
            # Activities/concepts
            if event.get('type') in ['visit', 'appointment', 'life_event']:
                entities.append({'name': event.get('topic', ''), 'type': 'activity'})
            
            # Update entities in knowledge graph
            for entity in entities:
                name = entity['name'].strip()
                if not name:
                    continue
                    
                entity_id = f"{entity['type']}:{name.lower()}"
                
                if entity_id not in self.knowledge_graph['entities']:
                    self.knowledge_graph['entities'][entity_id] = {
                        'name': name,
                        'type': entity['type'],
                        'first_seen': datetime.now().isoformat(),
                        'mention_count': 0,
                        'associated_events': [],
                        'properties': {}
                    }
                
                # Update mention count and events
                kg_entity = self.knowledge_graph['entities'][entity_id]
                kg_entity['mention_count'] += 1
                kg_entity['last_seen'] = datetime.now().isoformat()
                
                if event.get('id'):
                    if event['id'] not in kg_entity['associated_events']:
                        kg_entity['associated_events'].append(event['id'])
            
            # Create relationships between entities in the same event
            if len(entities) > 1:
                for i, entity1 in enumerate(entities):
                    for entity2 in entities[i+1:]:
                        relationship = {
                            'from': f"{entity1['type']}:{entity1['name'].lower()}",
                            'to': f"{entity2['type']}:{entity2['name'].lower()}",
                            'relation': 'co_occurs_with',
                            'strength': 1,
                            'event_id': event.get('id'),
                            'created': datetime.now().isoformat()
                        }
                        
                        # Check if relationship already exists
                        existing = None
                        for rel in self.knowledge_graph['relationships']:
                            if (rel['from'] == relationship['from'] and 
                                rel['to'] == relationship['to'] and 
                                rel['relation'] == relationship['relation']):
                                existing = rel
                                break
                        
                        if existing:
                            existing['strength'] += 1
                        else:
                            self.knowledge_graph['relationships'].append(relationship)
            
        except Exception as e:
            print(f"[SmartMemory] ⚠️ Knowledge graph update error: {e}")
    
    def _add_to_audit_log(self, action: str, event: Dict, metadata: Dict = None):
        """Add entry to append-only audit log"""
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'action': action,
                'event_id': event.get('id'),
                'event_type': event.get('type'),
                'username': self.username,
                'metadata': metadata or {}
            }
            
            # Append to audit log file
            with open(self.audit_log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
                
        except Exception as e:
            print(f"[SmartMemory] ⚠️ Audit log error: {e}")
    
    def _calculate_confidence(self, text: str, detection_method: str, field_data: Dict) -> Dict[str, float]:
        """Calculate per-field confidence scores"""
        base_confidence = {
            'llm': 0.85,
            'regex': 0.75, 
            'fallback': 0.60,
            'manual': 0.95
        }.get(detection_method, 0.50)
        
        # Adjust confidence based on text quality and completeness
        text_length_factor = min(1.0, len(text.split()) / 10.0)  # Favor longer texts
        completeness_factor = len([v for v in field_data.values() if v]) / max(1, len(field_data))
        
        adjusted_confidence = base_confidence * text_length_factor * completeness_factor
        
        # Per-field confidence (all fields get same base confidence for now)
        field_confidence = {}
        for field in ['type', 'topic', 'date', 'time', 'emotion', 'priority', 'location', 'people']:
            if field in field_data and field_data[field]:
                field_confidence[field] = min(0.95, adjusted_confidence + 0.05)  # Slight boost for present fields
            else:
                field_confidence[field] = max(0.1, adjusted_confidence - 0.2)   # Penalty for missing fields
        
        return field_confidence
    
    def _calculate_salience(self, event: Dict, text: str) -> float:
        """Calculate salience (importance) score based on novelty, emotion, and goals"""
        score = 0.0
        
        # Emotion intensity contribution
        emotion = event.get('emotion', 'neutral').lower()
        emotion_scores = {
            'excited': 0.9, 'happy': 0.8, 'stressed': 0.7, 'worried': 0.7,
            'angry': 0.8, 'sad': 0.7, 'frustrated': 0.6, 'neutral': 0.3
        }
        score += emotion_scores.get(emotion, 0.3) * SALIENCE_WEIGHTS['emotion_intensity']
        
        # Novelty - check against recent similar events
        novelty_score = self._calculate_novelty(event, text)
        score += novelty_score * SALIENCE_WEIGHTS['novelty']
        
        # Goal relevance - health, appointments, social events score higher
        goal_score = self._calculate_goal_relevance(event)
        score += goal_score * SALIENCE_WEIGHTS['goal_relevance']
        
        # Social significance - events involving people score higher
        social_score = 0.8 if event.get('people') and len(event['people']) > 0 else 0.2
        score += social_score * SALIENCE_WEIGHTS['social_significance']
        
        return min(1.0, score)
    
    def _calculate_novelty(self, event: Dict, text: str) -> float:
        """Calculate novelty score by comparing with recent similar events"""
        event_type = event.get('type', 'highlight')
        fingerprint = self._generate_fingerprint(text, event_type)
        
        # Check similarity to recent events of same type
        recent_cutoff = datetime.now() - timedelta(days=7)
        similar_events = []
        
        event_lists = {
            'appointment': self.appointments,
            'life_event': self.life_events, 
            'highlight': self.conversation_highlights,
            'health_state': self.health_states,
            'mood_state': self.mood_states,
            'visit': self.visits
        }
        
        if event_type in event_lists:
            for existing_event in event_lists[event_type]:
                created = datetime.fromisoformat(existing_event.get('created', '2000-01-01T00:00:00'))
                if created >= recent_cutoff:
                    existing_fp = existing_event.get('fingerprint', '')
                    if existing_fp:
                        similarity = difflib.SequenceMatcher(None, fingerprint, existing_fp).ratio()
                        if similarity > 0.7:  # High similarity threshold
                            similar_events.append((similarity, existing_event))
        
        # Higher novelty score for fewer similar events
        if not similar_events:
            return 1.0
        elif len(similar_events) == 1:
            return 0.6
        else:
            return 0.3
    
    def _calculate_goal_relevance(self, event: Dict) -> float:
        """Calculate how relevant event is to user goals/needs"""
        event_type = event.get('type', 'highlight')
        priority = event.get('priority', 'medium')
        
        # Type-based relevance
        type_scores = {
            'appointment': 0.9,     # High relevance - future commitments
            'health_state': 0.8,    # High relevance - wellbeing tracking  
            'life_event': 0.7,      # Medium-high - social/emotional events
            'mood_state': 0.6,      # Medium - emotional tracking
            'visit': 0.5,           # Medium - activity tracking
            'highlight': 0.4        # Lower - general thoughts
        }
        
        base_score = type_scores.get(event_type, 0.4)
        
        # Priority adjustment
        priority_multipliers = {'high': 1.2, 'medium': 1.0, 'low': 0.8}
        multiplier = priority_multipliers.get(priority, 1.0)
        
        return min(1.0, base_score * multiplier)
    
    def _append_audit_log(self, action: str, event_data: Dict, metadata: Dict = None):
        """Append entry to audit log for provenance tracking"""
        audit_entry = {
            'timestamp': datetime.now().isoformat(),
            'episode_id': self.current_episode_id,
            'action': action,  # 'create', 'update', 'merge', 'expire', 'pin'
            'event_id': event_data.get('id'),
            'event_type': event_data.get('type'),
            'user': self.username,
            'metadata': metadata or {}
        }
        
        # Include fingerprint and key fields for provenance
        audit_entry['provenance'] = {
            'fingerprint': event_data.get('fingerprint'),
            'source': event_data.get('source'),
            'original_text': event_data.get('original_text', '')[:100],  # Truncate for log
            'confidence_avg': sum(event_data.get('field_confidence', {}).values()) / max(1, len(event_data.get('field_confidence', {})))
        }
        
        try:
            with open(self.audit_log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(audit_entry, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"[SmartMemory] ⚠️ Audit log error: {e}")
    
    def _cleanup_expired_memories(self):
        """Clean up expired memories based on TTL policies"""
        now = datetime.now()
        expired_count = 0
        
        for event_type, event_list in [
            ('health_state', self.health_states),
            ('mood_state', self.mood_states), 
            ('visit', self.visits),
            ('appointment', self.appointments),
            ('highlight', self.conversation_highlights)
        ]:
            ttl_seconds = TTL_POLICIES.get(event_type, TTL_POLICIES['default'])
            if ttl_seconds == -1:  # Permanent events
                continue
            
            expired_events = []
            for event in event_list[:]:  # Copy to avoid modification during iteration
                created = datetime.fromisoformat(event.get('created', '2000-01-01T00:00:00'))
                
                # Check if event is pinned (never expires)
                if event.get('pinned', False):
                    continue
                
                # Check if expired
                age_seconds = (now - created).total_seconds()
                if age_seconds > ttl_seconds:
                    expired_events.append(event)
                    event_list.remove(event)
                    expired_count += 1
                    
                    # Log expiration
                    self._append_audit_log('expire', event, {'age_days': age_seconds / (24 * 3600)})
        
        if expired_count > 0:
            print(f"[SmartMemory] 🗑️ Cleaned up {expired_count} expired memories")
            self._atomic_save_memories()
    
    def _apply_confidence_decay(self, event: Dict, created_time: datetime) -> Dict:
        """Apply confidence decay over time"""
        if 'field_confidence' not in event:
            return event
        
        days_old = (datetime.now() - created_time).days
        if days_old <= 0:
            return event
        
        # Apply exponential decay
        decay_factor = (1 - CONFIDENCE_DECAY_RATE) ** days_old
        
        decayed_confidence = {}
        for field, confidence in event['field_confidence'].items():
            decayed_confidence[field] = max(0.1, confidence * decay_factor)  # Minimum 10% confidence
        
        event['field_confidence'] = decayed_confidence
        return event
    
    def extract_and_store_human_memories(self, text: str):
        """Extract and store events/memories with consensus extraction and provenance"""
        if not text or not text.strip():
            return
            
        print(f"[SmartMemory] 🧠 Processing: '{text}'")
        
        # Edge-case hardening: Multi-event splitting
        try:
            from utils.time_helper import _split_multi_events
            text_parts = _split_multi_events(text)
            if len(text_parts) > 1:
                print(f"[SmartMemory] ✂️ Split into {len(text_parts)} events")
                for i, part in enumerate(text_parts):
                    print(f"[SmartMemory] 📝 Processing part {i+1}: '{part}'")
                    # Process each part separately
                    self._extract_single_text_memory(part)
                return
        except ImportError:
            pass  # Fallback if time_helper not available
        
        # Process as single event
        self._extract_single_text_memory(text)
    
    def _extract_single_text_memory(self, text: str):
        """Extract memory from a single text fragment"""
        # Also use the existing MEGA-INTELLIGENT extraction
        self.mega_memory.extract_memories_from_text(text)
        
        try:
            # Check for cross-conversation references first
            resolved_events = self._resolve_cross_conversation_references(text)
            
            # Process high-confidence cross-conversation merges
            cross_conv_merged = False
            if resolved_events:
                print(f"[SmartMemory] 🔗 Resolved {len(resolved_events)} cross-conversation references")
                cross_conv_merged = self._process_cross_conversation_merges(resolved_events, text)
            
            # Tier-3 throttle + lock around heavy processing
            now = time.time()
            
            # Tier-3 throttle: skip heavy path if we ran it very recently
            if (now - self._last_tier3) < 8.0:  # 8s guard, adjust if needed
                print("[SmartMemory] ⏳ Throttled Tier-3 extraction")
                return
                
            # Skip creating new events if cross-conversation merge already occurred
            if cross_conv_merged:
                print("[SmartMemory] ✅ Cross-conversation merge completed - skipping new event creation")
                return
                
            with self._lock:
                self._last_tier3 = now
                
                # Normalize text for consistent processing
                normalized_text = self._normalize_text_for_memory(text)
                
                # CONSENSUS EXTRACTION: Multiple passes with field-level confidence fusion
                candidates = []
                
                # Pass 1: Pattern-based detection (regex/heuristics)
                pattern_candidates = self._pattern_based_detection(normalized_text)
                candidates.extend(pattern_candidates)
                
                # Pass 2: Heuristic detection (keywords + rules)
                heuristic_candidates = self._heuristic_detection(normalized_text)
                candidates.extend(heuristic_candidates)
                
                # Pass 3: LLM-based smart detection
                llm_candidates = self._smart_detect_events(normalized_text)
                # Add source and field confidence to LLM candidates
                for candidate in llm_candidates:
                    if 'source' not in candidate:
                        candidate['source'] = 'llm'
                    if 'field_confidence' not in candidate:
                        # Estimate field confidences for LLM results
                        candidate['field_confidence'] = self._calculate_confidence(
                            text, 'llm', candidate)
                
                candidates.extend(llm_candidates)
                
                if not candidates:
                    print(f"[SmartMemory] 💬 No significant events detected in: '{text}'")
                    return
                
                # CONSENSUS FUSION: Combine candidates with field-level confidence
                fused_events = self._fuse_candidates(candidates, text)
                
                print(f"[SmartMemory] 📝 Consensus fusion: {len(candidates)} candidates → {len(fused_events)} events")
                
                # Process and store each fused event
                for raw_event in fused_events:
                    if not isinstance(raw_event, dict) or not raw_event.get('topic'):
                        print(f"[SmartMemory] ⚠️ Skipping invalid event: {raw_event}")
                        continue
                    
                    # Store as hypothesis if confidence too low
                    if raw_event.get('_needs_confirmation'):
                        self._store_hypothesis_memory(raw_event, text)
                        continue
                    
                    # Ensure proper JSON encoding
                    raw_event = self._ensure_json_encodable(raw_event)
                    
                    # Enhance with normalization, confidence, provenance
                    enhanced_event = self._enhance_event(raw_event, text=text, detection_method=raw_event.get('source', 'consensus'))
                    
                    # Find episode candidates for stitching
                    episode_candidates = self._find_episode_candidates(enhanced_event, text)
                    
                    # Perform episode stitching (merge or link)
                    stitched_event = self._stitch_episode(enhanced_event, episode_candidates)
                    
                    # Log creation/update to audit trail
                    if stitched_event.get('merge_count', 0) > 1:
                        action = 'update'
                    else:
                        action = 'create'
                    self._add_to_audit_log(action, stitched_event, {'original_text': text})
                    
                    # Store in appropriate collection based on type
                    event_type = stitched_event['type']
                    if event_type == 'appointment':
                        self._store_event_with_dedup(self.appointments, stitched_event, 'appointment')
                    elif event_type == 'life_event':
                        self._store_event_with_dedup(self.life_events, stitched_event, 'life_event')
                    elif event_type == 'highlight':
                        self._store_event_with_dedup(self.conversation_highlights, stitched_event, 'highlight')
                    elif event_type == 'health_state':
                        self._store_event_with_dedup(self.health_states, stitched_event, 'health_state')
                    elif event_type == 'mood_state':
                        self._store_event_with_dedup(self.mood_states, stitched_event, 'mood_state')
                    elif event_type == 'visit':
                        self._store_event_with_dedup(self.visits, stitched_event, 'visit')
                    
                    # Update knowledge graph
                    self._update_knowledge_graph(stitched_event)
                    
                    print(f"[SmartMemory] ✅ Stored {stitched_event['type']}: {stitched_event['topic']}")
                
                # Save memories with atomic write
                if fused_events or resolved_events:  # Save if we found events OR references
                    self._atomic_save_memories()
                
        except Exception as e:
            print(f"[SmartMemory] ❌ Error processing memories: {e}")
            import traceback
            traceback.print_exc()
    
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
            self.save_memory(self.episodes, 'episodes.json')
            self.save_memory(self.episode_index, 'episode_index.json')
            self.save_memory(self.hypothesis_memories, 'hypothesis_memories.json')
            self.save_memory(self.knowledge_graph, 'knowledge_graph.json')
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
                
                # Validate and enhance events with LLM detection method
                validated_events = []
                for event in events:
                    if self._validate_event(event):
                        enhanced_event = self._enhance_event(event, text=text, detection_method="llm")
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
    
    def _enhance_event(self, event: Dict, *, text: str = "", detection_method: str = "llm") -> Dict:
        """🔧 COMPREHENSIVE NORMALIZATION - Single normalizer for ALL events with confidence, source, salience, provenance"""
        now = datetime.now()
        now_iso = now.isoformat()
        etype = event.get('type', 'highlight')
        
        # Generate unique ID and fingerprint
        event_id = event.get('id') or f"{etype}_{int(time.time()*1000)}_{random.randint(100,999)}"
        fingerprint = self._generate_fingerprint(text or event.get('original_text', ''), etype)
        
        # UNIFIED FIELD STRUCTURE - Every event gets ALL these fields
        enhanced = {
            # === CORE IDENTIFICATION ===
            'id': event_id,
            'type': etype,
            'topic': event.get('topic', 'unknown'),
            'category': event.get('category') or self._determine_category(etype),
            'fingerprint': fingerprint,
            
            # === TEMPORAL FIELDS ===
            'date': event.get('date', now.strftime('%Y-%m-%d')),
            'time': event.get('time'),
            'created': now_iso,
            'last_updated': now_iso,
            
            # === CONTEXTUAL FIELDS ===
            'location': event.get('location'),
            'people': self._normalize_people_list(event.get('people', [])),
            'details': event.get('details'),
            'original_text': event.get('original_text', text),
            
            # === EMOTIONAL/PRIORITY FIELDS ===
            'emotion': event.get('emotion', 'neutral'),
            'priority': event.get('priority', 'medium'), 
            'status': event.get('status', 'pending'),
            
            # === MICRO-EVENT SPECIFIC FIELDS ===
            'state': event.get('state'),          # health_state/mood_state
            'severity': event.get('severity'),    # health_state
            'symptoms': event.get('symptoms', []), # health_state
            'mood': event.get('mood'),            # mood_state
            'intensity': event.get('intensity'),  # mood_state
            'items': event.get('items', []),      # visits/purchases
            
            # === CONFIDENCE & SALIENCE ===
            'field_confidence': self._calculate_confidence(text, detection_method, event),
            'salience': self._calculate_salience(event, text),
            
            # === SOURCE & PROVENANCE ===
            'source': detection_method,  # llm, regex, fallback, manual
            'detected_by': event.get('detected_by', detection_method),
            'episode_id': self.current_episode_id,
            
            # === META FIELDS ===
            'user': self.username,
            'pinned': event.get('pinned', False),  # For durable facts that don't expire
            'ttl_override': event.get('ttl_override'),  # Custom TTL in seconds
            'version': 1  # For future schema evolution
        }
        
        # Apply confidence decay for existing events
        if 'created' in event and event['created'] != now_iso:
            created_time = datetime.fromisoformat(event['created'])
            enhanced = self._apply_confidence_decay(enhanced, created_time)
        
        # Add stable fingerprint for long-range similarity detection
        enhanced['stable_fingerprint'] = self._stable_fingerprint(enhanced)
        
        return enhanced
    
    def _normalize_people_list(self, people: List[Any]) -> List[str]:
        """Normalize people list to consistent string format"""
        if not people:
            return []
        
        normalized = []
        for person in people:
            if isinstance(person, str) and person.strip():
                # Clean and title-case names
                clean_name = person.strip().title()
                if clean_name not in normalized:
                    normalized.append(clean_name)
        
        return normalized
    
    def _find_episode_candidates(self, event: Dict, text: str) -> List[Dict]:
        """Find candidate events for episode stitching based on similarity and time proximity"""
        candidates = []
        event_fingerprint = event.get('fingerprint', '')
        event_stable_fingerprint = event.get('stable_fingerprint', '')
        event_type = event.get('type', 'highlight')
        created_time = datetime.fromisoformat(event.get('created', datetime.now().isoformat()))
        
        # Define time window for episode stitching (reduced to 30 minutes as requested)
        episode_window = 30 * 60  # 30 minutes in seconds  
        window_start = created_time - timedelta(seconds=episode_window)
        window_end = created_time + timedelta(seconds=episode_window)
        
        # Get relevant event list
        event_lists = {
            'appointment': self.appointments,
            'life_event': self.life_events,
            'highlight': self.conversation_highlights, 
            'health_state': self.health_states,
            'mood_state': self.mood_states,
            'visit': self.visits
        }
        
        all_events = []
        for event_list in event_lists.values():
            all_events.extend(event_list)
        
        # Check all events for candidates
        for existing_event in all_events:
            try:
                existing_created = datetime.fromisoformat(existing_event.get('created', '2000-01-01T00:00:00'))
                
                # Check short-window similarity (original fingerprint)
                within_window = window_start <= existing_created <= window_end
                
                if within_window:
                    # Check fingerprint similarity for short window
                    existing_fingerprint = existing_event.get('fingerprint', '')
                    if existing_fingerprint and event_fingerprint:
                        similarity = difflib.SequenceMatcher(None, event_fingerprint, existing_fingerprint).ratio()
                        
                        # High similarity suggests potential merge
                        if similarity > 0.8:
                            candidates.append({
                                'event': existing_event,
                                'similarity': similarity,
                                'time_diff': abs((created_time - existing_created).total_seconds()),
                                'merge_type': 'duplicate'
                            })
                        # Medium similarity suggests episode linking
                        elif similarity > 0.5:
                            candidates.append({
                                'event': existing_event,
                                'similarity': similarity,
                                'time_diff': abs((created_time - existing_created).total_seconds()),
                                'merge_type': 'episode_link'
                            })
                
                # Check stable fingerprint for cross-day similarity
                existing_stable_fingerprint = existing_event.get('stable_fingerprint', '')
                if existing_stable_fingerprint and event_stable_fingerprint:
                    stable_similarity = difflib.SequenceMatcher(None, event_stable_fingerprint, existing_stable_fingerprint).ratio()
                    
                    # Cross-day thematic similarity
                    if stable_similarity > 0.7:
                        candidates.append({
                            'event': existing_event,
                            'similarity': stable_similarity * 0.9,  # Slightly lower weight for cross-day
                            'time_diff': abs((created_time - existing_created).total_seconds()),
                            'merge_type': 'cross_day_link'
                        })
                
                # Check for thematic/contextual similarity
                if self._events_are_thematically_related(event, existing_event):
                    candidates.append({
                        'event': existing_event,
                        'similarity': 0.6,  # Medium similarity for thematic
                        'time_diff': abs((created_time - existing_created).total_seconds()),
                        'merge_type': 'thematic_link'
                    })
                        
            except Exception as e:
                continue  # Skip problematic events
        
        # Sort by similarity and time proximity
        candidates.sort(key=lambda x: (x['similarity'], -x['time_diff']), reverse=True)
        return candidates[:3]  # Top 3 candidates
    
    def _events_are_thematically_related(self, event1: Dict, event2: Dict) -> bool:
        """Check if two events are thematically related"""
        # Same type events are related
        if event1.get('type') == event2.get('type'):
            return True
        
        # Health and mood states are related
        health_mood_types = {'health_state', 'mood_state'}
        if event1.get('type') in health_mood_types and event2.get('type') in health_mood_types:
            return True
        
        # Events with overlapping people are related
        people1 = set(event1.get('people', []))
        people2 = set(event2.get('people', []))
        if people1 and people2 and people1.intersection(people2):
            return True
        
        # Events at same location are related
        loc1 = event1.get('location', '').lower()
        loc2 = event2.get('location', '').lower()
        if loc1 and loc2 and loc1 == loc2:
            return True
        
        return False
    
    def _resolve_cross_conversation_references(self, text: str) -> List[Dict]:
        """🔗 Resolve cross-conversation references using explicit patterns (stdlib only)"""
        references = []
        text_lower = text.lower().strip()
        
        # Search for explicit reference patterns
        for pattern in EXPLICIT_REF_PATTERNS:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                ref_data = match.groupdict()
                ref_text = match.group(0)
                
                # Find candidate events that match this reference
                candidates = self._find_reference_candidates(ref_data, ref_text, text)
                
                for candidate in candidates:
                    references.append({
                        'reference_text': ref_text,
                        'reference_data': ref_data,
                        'matched_event': candidate['event'],
                        'confidence': candidate['confidence'],
                        'match_type': candidate['match_type'],
                        'original_text': text
                    })
        
        return references
    
    def _find_reference_candidates(self, ref_data: Dict, ref_text: str, full_text: str) -> List[Dict]:
        """Find events that match the reference data"""
        candidates = []
        
        # Get all events from all lists
        all_events = []
        event_lists = [
            ('appointment', self.appointments),
            ('life_event', self.life_events),
            ('highlight', self.conversation_highlights),
            ('health_state', self.health_states),
            ('mood_state', self.mood_states),
            ('visit', self.visits)
        ]
        
        for event_type, event_list in event_lists:
            for event in event_list:
                all_events.append((event_type, event))
        
        # Match against different reference types
        for event_type, event in all_events:
            confidence = 0.0
            match_type = 'none'
            
            # Location-based matching
            if 'location' in ref_data:
                ref_location = ref_data['location'].strip().lower()
                event_location = event.get('location', '').lower()
                event_topic = event.get('topic', '').lower()
                
                if event_location and ref_location in event_location:
                    confidence = 0.9
                    match_type = 'location_exact'
                elif event_location and difflib.SequenceMatcher(None, ref_location, event_location).ratio() > 0.7:
                    confidence = 0.7
                    match_type = 'location_similar'
                elif ref_location in event_topic:
                    confidence = 0.6
                    match_type = 'location_in_topic'
            
            # Person-based matching
            elif 'person' in ref_data:
                ref_person = ref_data['person'].strip().lower()
                event_people = [p.lower() for p in event.get('people', [])]
                event_topic = event.get('topic', '').lower()
                
                if any(ref_person in person for person in event_people):
                    confidence = 0.9
                    match_type = 'person_exact'
                elif ref_person in event_topic:
                    confidence = 0.7
                    match_type = 'person_in_topic'
            
            # Event-based matching
            elif 'event' in ref_data:
                ref_event = ref_data['event'].strip().lower()
                event_topic = event.get('topic', '').lower()
                event_category = event.get('category', '').lower()
                
                if ref_event in event_topic or ref_event in event_category:
                    confidence = 0.8
                    match_type = 'event_type_match'
                elif event_type == 'appointment' and ref_event in ['appointment', 'meeting']:
                    confidence = 0.7
                    match_type = 'event_category_match'
                elif event_type == 'visit' and ref_event in ['visit', 'trip']:
                    confidence = 0.7
                    match_type = 'event_category_match'
            
            # Activity-based matching
            elif 'activity' in ref_data:
                ref_activity = ref_data['activity'].strip().lower()
                event_topic = event.get('topic', '').lower()
                event_details = event.get('details', '').lower()
                
                # Use difflib for fuzzy matching of activities
                topic_similarity = difflib.SequenceMatcher(None, ref_activity, event_topic).ratio()
                details_similarity = difflib.SequenceMatcher(None, ref_activity, event_details).ratio() if event_details else 0
                
                max_similarity = max(topic_similarity, details_similarity)
                if max_similarity > 0.6:
                    confidence = max_similarity
                    match_type = 'activity_similar'
            
            # Place-based matching (restaurant, cafe, etc.)
            elif 'place' in ref_data:
                ref_place = ref_data['place'].strip().lower()
                event_location = event.get('location', '').lower()
                event_topic = event.get('topic', '').lower()
                
                if ref_place in event_location or ref_place in event_topic:
                    confidence = 0.8
                    match_type = 'place_match'
            
            # Add candidate if confidence is high enough
            if confidence > 0.5:
                candidates.append({
                    'event': event,
                    'confidence': confidence,
                    'match_type': match_type,
                    'event_type': event_type
                })
        
        # Sort by confidence and return top candidates
        candidates.sort(key=lambda x: x['confidence'], reverse=True)
        return candidates[:5]  # Top 5 candidates
    
    def _create_cross_reference_links(self, references: List[Dict]) -> Dict[str, List[Dict]]:
        """Create cross-reference links between current conversation and past events"""
        links_by_event = {}
        
        for ref in references:
            matched_event = ref['matched_event']
            event_id = matched_event.get('id')
            
            if event_id:
                if event_id not in links_by_event:
                    links_by_event[event_id] = []
                
                link_info = {
                    'reference_text': ref['reference_text'],
                    'reference_context': ref['original_text'][:200],  # Truncate for storage
                    'confidence': ref['confidence'],
                    'match_type': ref['match_type'],
                    'linked_at': datetime.now().isoformat(),
                    'episode_id': self.current_episode_id
                }
                
                links_by_event[event_id].append(link_info)
        
    def _update_events_with_references(self, reference_links: Dict[str, List[Dict]]):
        """Update existing events with cross-reference links"""
        all_event_lists = [
            self.appointments,
            self.life_events,
            self.conversation_highlights,
            self.health_states,
            self.mood_states,
            self.visits
        ]
        
        updated_count = 0
        for event_list in all_event_lists:
            for event in event_list:
                event_id = event.get('id')
                if event_id in reference_links:
                    # Add cross-reference links to existing event
                    if 'cross_references' not in event:
                        event['cross_references'] = []
                    
                    # Add new references
                    new_refs = reference_links[event_id]
                    event['cross_references'].extend(new_refs)
                    
                    # Update metadata
                    event['last_updated'] = datetime.now().isoformat()
                    event['reference_count'] = len(event['cross_references'])
                    
                    updated_count += 1
        
        if updated_count > 0:
            print(f"[SmartMemory] 🔗 Updated {updated_count} events with cross-references")
        
        return updated_count
    
    def _process_cross_conversation_merges(self, resolved_events: List[Dict], text: str) -> bool:
        """Process cross-conversation references and merge with existing events if confidence ≥ 0.65"""
        merged_any = False
        
        for reference in resolved_events:
            confidence = reference.get('confidence', 0.0)
            if confidence < 0.65:
                continue  # Skip low confidence references
            
            matched_event = reference['matched_event']
            event_id = matched_event.get('id')
            if not event_id:
                continue
            
            # Determine which category file this event belongs to
            event_lists_and_files = [
                (self.appointments, 'smart_appointments.json', 'appointment'),
                (self.life_events, 'smart_life_events.json', 'life_event'),
                (self.conversation_highlights, 'smart_highlights.json', 'highlight'),
                (self.health_states, 'smart_health_states.json', 'health_state'),
                (self.mood_states, 'smart_mood_states.json', 'mood_state'),
                (self.visits, 'smart_visits.json', 'visit')
            ]
            
            # Find the event in the appropriate list
            target_list = None
            target_file = None
            target_index = None
            
            for event_list, filename, category in event_lists_and_files:
                for i, event in enumerate(event_list):
                    if event.get('id') == event_id:
                        target_list = event_list
                        target_file = filename
                        target_index = i
                        break
                if target_list:
                    break
            
            if target_list is None or target_index is None:
                continue  # Event not found
            
            # Create a new event from the reference to merge
            new_event = {
                'type': matched_event.get('type', 'highlight'),
                'topic': f"Referenced: {reference['reference_text']}",
                'date': datetime.now().strftime('%Y-%m-%d'),
                'time': datetime.now().strftime('%H:%M'),
                'original_text': text,
                'detected_by': 'cross_reference'
            }
            
            # Merge the new event with the matched event
            merged_event = self._merge_duplicate_events(new_event, matched_event)
            
            # Preserve episode_id and update metadata
            merged_event['episode_id'] = matched_event.get('episode_id', self.current_episode_id)
            merged_event['last_updated'] = datetime.now().isoformat()
            
            # Extend evidence with cross-reference information
            if 'evidence' not in merged_event:
                merged_event['evidence'] = []
            merged_event['evidence'].append({
                'type': 'cross_reference',
                'reference_text': reference['reference_text'],
                'confidence': confidence,
                'linked_at': datetime.now().isoformat(),
                'context': text[:200]  # Truncate for storage
            })
            
            # Replace the event in the list
            target_list[target_index] = merged_event
            
            # Write back atomically
            self.save_memory(target_list, target_file)
            
            # Audit log
            self._append_audit_log('merge', merged_event, {
                'link': 'reference',
                'reference_text': reference['reference_text'],
                'confidence': confidence,
                'merged_with': event_id
            })
            
            merged_any = True
            print(f"[SmartMemory] 🔗 Cross-conversation merge: {reference['reference_text']} → {event_id}")
        
        return merged_any
    
    def _perform_episode_stitching(self, new_event: Dict, candidates: List[Dict]) -> Dict:
        if not candidates:
            return new_event
        
        best_candidate = candidates[0]
        merge_type = best_candidate['merge_type']
        existing_event = best_candidate['event']
        
        if merge_type == 'duplicate' and best_candidate['similarity'] > 0.9:
            # High confidence duplicate - merge events
            merged_event = self._merge_duplicate_events(new_event, existing_event)
            self._append_audit_log('merge', merged_event, {
                'merged_with': existing_event.get('id'),
                'similarity': best_candidate['similarity'],
                'merge_type': 'duplicate'
            })
            return merged_event
        
        else:
            # Create cross-reference links for episode continuity
            episode_links = new_event.get('episode_links', [])
            
            for candidate in candidates[:2]:  # Link to top 2 candidates
                link_event = candidate['event']
                link_id = link_event.get('id')
                
                if link_id and link_id not in episode_links:
                    episode_links.append({
                        'event_id': link_id,
                        'link_type': candidate['merge_type'],
                        'similarity': candidate['similarity'],
                        'created': datetime.now().isoformat()
                    })
            
            new_event['episode_links'] = episode_links
            self._append_audit_log('link', new_event, {
                'linked_events': [link['event_id'] for link in episode_links[-len(candidates[:2]):]],
                'link_types': [candidate['merge_type'] for candidate in candidates[:2]]
            })
            
            return new_event
    
    def _merge_duplicate_events(self, new_event: Dict, existing_event: Dict) -> Dict:
        """Merge two duplicate events, combining information and updating confidence"""
        # Start with existing event as base
        merged = existing_event.copy()
        
        # Update timestamps
        merged['last_updated'] = datetime.now().isoformat()
        
        # Merge field confidence (take maximum confidence per field)
        existing_conf = existing_event.get('field_confidence', {})
        new_conf = new_event.get('field_confidence', {})
        
        merged_conf = {}
        all_fields = set(existing_conf.keys()) | set(new_conf.keys())
        for field in all_fields:
            existing_val = existing_conf.get(field, 0.0)
            new_val = new_conf.get(field, 0.0)
            merged_conf[field] = max(existing_val, new_val)
        
        merged['field_confidence'] = merged_conf
        
        # Combine people lists
        existing_people = set(existing_event.get('people', []))
        new_people = set(new_event.get('people', []))
        merged['people'] = list(existing_people | new_people)
        
        # Combine items lists  
        existing_items = set(existing_event.get('items', []))
        new_items = set(new_event.get('items', []))
        merged['items'] = list(existing_items | new_items)
        
        # Update with better details if new event has more information
        if len(new_event.get('details', '')) > len(existing_event.get('details', '')):
            merged['details'] = new_event.get('details')
        
        # Take higher salience score
        merged['salience'] = max(
            existing_event.get('salience', 0.0),
            new_event.get('salience', 0.0)
        )
        
        # Increment merge counter
        merged['merge_count'] = merged.get('merge_count', 1) + 1
        merged['merged_sources'] = merged.get('merged_sources', [existing_event.get('source', 'unknown')])
        merged['merged_sources'].append(new_event.get('source', 'unknown'))
        
        return merged
    
    def _store_event_with_dedup(self, event_list: List[Dict], event: Dict, event_type: str):
        """Store event in list with deduplication based on merge results"""
        event_id = event.get('id')
        
        # Check if this is a merged event (already exists in list)
        if event.get('merge_count', 0) > 1:
            # Find and update existing event
            for i, existing in enumerate(event_list):
                if existing.get('id') == event_id:
                    event_list[i] = event
                    print(f"[SmartMemory] 🔄 Updated {event_type}: {event['topic']} (merged)")
                    return
        
        # New event - append to list
        event_list.append(event)
        
        # Print appropriate message
        event_info = self._format_event_info(event)
        print(f"[SmartMemory] ✅ New {event_type}: {event_info}")
    
    def _format_event_info(self, event: Dict) -> str:
        """Format event information for logging"""
        topic = event.get('topic', 'unknown')
        date = event.get('date', '')
        emotion = event.get('emotion', '')
        location = event.get('location', '')
        salience = event.get('salience', 0.0)
        
        info_parts = [topic]
        
        if date:
            info_parts.append(f"on {date}")
        if location:
            info_parts.append(f"at {location}")
        if emotion:
            info_parts.append(f"({emotion})")
        
        # Add confidence/salience indicator
        avg_conf = sum(event.get('field_confidence', {}).values()) / max(1, len(event.get('field_confidence', {})))
        info_parts.append(f"[conf:{avg_conf:.2f} sal:{salience:.2f}]")
        
        return " ".join(info_parts)
    
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
            events.append(self._enhance_event(base_event, text=text, detection_method="fallback"))
        
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
            events.append(self._enhance_event(base_event, text=text, detection_method="fallback"))
        
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
            events.append(self._enhance_event(base_event, text=text, detection_method="fallback"))
        
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
            events.append(self._enhance_event(base_event, text=text, detection_method="fallback"))
        
        return events
    
    def _week_start(self, ymd: str) -> str:
        """Get Monday of the week for a given date"""
        d = datetime.strptime(ymd, '%Y-%m-%d')
        monday = d - timedelta(days=d.weekday())
        return monday.strftime('%Y-%m-%d')
    
    def _norm(self, s: str) -> str:
        """Normalize string for consistent comparison"""
        return re.sub(r'\s+', ' ', (s or '').strip().lower())
    
    def _stable_fingerprint(self, ev: dict) -> str:
        """Create stable fingerprint using category|key|week_bucket"""
        bucket = self._week_start(ev.get('date') or datetime.now().strftime('%Y-%m-%d'))
        key = self._norm(ev.get('location') or ev.get('topic'))
        return f"{ev.get('category','highlight')}|{key}|{bucket}"
    
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
    
    def _atomic_write_json(self, path: str, data):
        """Atomic JSON write using tempfile + os.replace"""
        import tempfile
        import os
        
        d = os.path.dirname(path)
        os.makedirs(d, exist_ok=True)
        
        fd, tmp = tempfile.mkstemp(prefix='.tmp_', dir=d)
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            os.replace(tmp, path)
        finally:
            try:
                if os.path.exists(tmp):
                    os.remove(tmp)
            except:
                pass
    
    def save_memory(self, data: List[Dict], filename: str):
        """Save memory file using atomic writes"""
        file_path = os.path.join(self.memory_dir, filename)
        try:
            self._atomic_write_json(file_path, data)
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
    
    # Edge-case hardening methods
    def ask_for_clarification(self, event: Dict, uncertainty_reason: str) -> str:
        """Generate clarification question for low-confidence events"""
        questions = []
        
        if 'date' in event.get('_conflict_fields', []):
            questions.extend([
                f"When exactly did {event.get('topic', 'this')} happen?",
                f"Was {event.get('topic', 'this')} today or another day?"
            ])
        
        if 'location' in event.get('_conflict_fields', []):
            questions.extend([
                f"Where did {event.get('topic', 'this')} take place?",
                f"Which location was {event.get('topic', 'this')} at?"
            ])
        
        if 'state' in event.get('_conflict_fields', []) and event.get('type') == 'health_state':
            questions.extend([
                f"How are you feeling exactly?",
                f"Are you feeling better or worse than before?"
            ])
        
        # Store pending clarification
        clarification = {
            'id': f"clarif_{int(time.time()*1000)}",
            'event': event,
            'question': questions[0] if questions else f"Can you tell me more about {event.get('topic', 'this')}?",
            'created': datetime.now().isoformat(),
            'status': 'pending',
            'reason': uncertainty_reason
        }
        
        self.pending_clarifications.append(clarification)
        self.save_memory(self.pending_clarifications, 'pending_clarifications.json')
        
        return questions[0] if questions else f"Can you tell me more about {event.get('topic', 'this')}?"
    
    def process_correction(self, original_text: str, correction_text: str) -> bool:
        """Process user correction with enhanced history tracking"""
        try:
            # Find events from recent memory that might match the correction context
            recent_events = []
            for category in [self.appointments, self.life_events, self.conversation_highlights, 
                           self.health_states, self.mood_states, self.visits]:
                # Look at events from last 48 hours (extended window)
                cutoff_date = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
                
                for event in category:
                    if event.get('date') >= cutoff_date:
                        recent_events.append((event, category))
            
            # Try to match correction to a specific event
            best_match = None
            best_similarity = 0.0
            
            for event, category in recent_events:
                similarity = self._calculate_text_similarity(original_text, event.get('original_text', ''))
                if similarity > best_similarity and similarity > 0.6:  # Higher threshold for corrections
                    best_similarity = similarity
                    best_match = (event, category)
            
            if best_match:
                event, category = best_match
                # Enhanced correction processing with full audit trail
                old_event = event.copy()
                
                # Create correction record
                correction_record = {
                    'id': f"corr_{int(time.time()*1000)}",
                    'event_id': event.get('id'),
                    'original_text': original_text,
                    'correction_text': correction_text,
                    'corrected_at': datetime.now().isoformat(),
                    'similarity_score': best_similarity,
                    'field_changes': {},
                    'confidence_changes': {}
                }
                
                # Re-extract with correction text
                self._extract_single_text_memory(correction_text)
                corrected_events = self.mega_memory.memory_entries  # Get last extracted events
                
                if corrected_events:
                    corrected_event = corrected_events[-1]  # Get most recent
                    
                    # Track field-level changes
                    for key, new_value in corrected_event.items():
                        if key not in ['id', 'created', 'episode_id', 'timestamp']:
                            old_value = event.get(key)
                            if old_value != new_value:
                                correction_record['field_changes'][key] = {
                                    'old': old_value,
                                    'new': new_value
                                }
                                event[key] = new_value
                    
                    # Update confidence scores
                    event['confidence'] = min(1.0, event.get('confidence', 0.5) + 0.1)  # Boost confidence after correction
                    event['corrected'] = True
                    event['last_updated'] = datetime.now().isoformat()
                    
                    # Enhanced correction history
                    if 'correction_history' not in event:
                        event['correction_history'] = []
                    
                    event['correction_history'].append(correction_record)
                    
                    # Log to audit trail
                    self._add_to_audit_log('correction', correction_record)
                    
                    # Save updated memory
                    self._save_all_categories()
                    
                    print(f"[SmartMemory] ✏️ Enhanced correction applied: {event.get('topic')} ({len(correction_record['field_changes'])} fields changed)")
                    return True
            else:
                print(f"[SmartMemory] ❓ No matching event found for correction (best similarity: {best_similarity:.2f})")
            
            return False
            
        except Exception as e:
            print(f"[SmartMemory] ❌ Error processing correction: {e}")
            return False
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two text strings"""
        if not text1 or not text2:
            return 0.0
        
        # Use difflib for text similarity
        return difflib.SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def learn_alias(self, entity: str, alias: str, entity_type: str = 'auto') -> bool:
        """Enhanced alias learning with better bidirectional mappings"""
        try:
            if entity_type == 'auto':
                # Enhanced entity type detection
                entity_lower = entity.lower()
                alias_lower = alias.lower()
                
                # People detection (names, titles)
                if (entity.title() == entity and len(entity.split()) <= 3 and 
                    not any(word in entity_lower for word in ['the', 'a', 'an', 'my', 'our'])):
                    entity_type = 'people'
                # Places detection (more comprehensive)
                elif any(word in entity_lower for word in [
                    'restaurant', 'cafe', 'shop', 'park', 'hospital', 'clinic', 'gym', 'mall',
                    'store', 'office', 'school', 'university', 'library', 'museum', 'theater',
                    'bank', 'hotel', 'airport', 'station', 'beach', 'mountain'
                ]):
                    entity_type = 'places'
                # Activities detection
                elif any(word in entity_lower for word in [
                    'meeting', 'appointment', 'workout', 'class', 'session', 'practice',
                    'game', 'match', 'event', 'party', 'dinner', 'lunch', 'breakfast'
                ]):
                    entity_type = 'activities'
                else:
                    # Default to people for single/double words, activities for longer
                    entity_type = 'people' if len(entity.split()) <= 2 else 'activities'
            
            if entity_type not in self.alias_mappings:
                self.alias_mappings[entity_type] = {}
            
            # Normalize for consistency
            entity_norm = entity.lower().strip()
            alias_norm = alias.lower().strip()
            
            # Enhanced bidirectional mapping with conflict detection
            mapping_entry = {
                'aliases': [],
                'primary': entity,
                'learned_at': datetime.now().isoformat(),
                'usage_count': 0,
                'confidence': 0.8
            }
            
            # Update existing mapping or create new one
            if entity_norm in self.alias_mappings[entity_type]:
                existing = self.alias_mappings[entity_type][entity_norm]
                if isinstance(existing, list):
                    # Convert old format to new format
                    mapping_entry['aliases'] = existing.copy()
                    mapping_entry['usage_count'] = len(existing)
                else:
                    mapping_entry = existing
                    
                if alias_norm not in mapping_entry['aliases']:
                    mapping_entry['aliases'].append(alias_norm)
            else:
                mapping_entry['aliases'] = [alias_norm]
            
            self.alias_mappings[entity_type][entity_norm] = mapping_entry
            
            # Create reverse mapping for quick lookup
            reverse_mapping = {
                'primary': entity,
                'type': entity_type,
                'learned_at': datetime.now().isoformat()
            }
            self.alias_mappings[entity_type][alias_norm] = reverse_mapping
            
            # Update usage statistics
            mapping_entry['usage_count'] += 1
            mapping_entry['last_used'] = datetime.now().isoformat()
            
            # Save enhanced alias mappings  
            self.save_memory(self.alias_mappings, 'alias_mappings.json')
            
            print(f"[SmartMemory] 🔗 Enhanced alias learned: '{alias}' ↔ '{entity}' ({entity_type})")
            return True
            
        except Exception as e:
            print(f"[SmartMemory] ❌ Error learning alias: {e}")
            return False
    
    def resolve_alias(self, text: str, entity_type: str = None) -> str:
        """Resolve alias to primary entity name"""
        try:
            text_norm = text.lower().strip()
            
            types_to_check = [entity_type] if entity_type else ['people', 'places', 'activities']
            
            for e_type in types_to_check:
                if e_type in self.alias_mappings:
                    for primary, mapping in self.alias_mappings[e_type].items():
                        if isinstance(mapping, dict):
                            # Check if text matches an alias
                            if text_norm in mapping.get('aliases', []):
                                # Update usage count
                                mapping['usage_count'] = mapping.get('usage_count', 0) + 1
                                mapping['last_used'] = datetime.now().isoformat()
                                self.save_memory(self.alias_mappings, 'alias_mappings.json')
                                return mapping['primary']
                            
                            # Check reverse mapping
                            if text_norm == primary:
                                return mapping['primary']
            
            return text  # Return original if no alias found
            
        except Exception as e:
            print(f"[SmartMemory] ❌ Error resolving alias: {e}")
            return text
    
    def _events_similar(self, text1: str, text2: str, threshold: float = 0.6) -> bool:
        """Check if two text fragments describe similar events"""
        try:
            # Normalize both texts
            norm1 = re.sub(r'[^\w\s]', '', text1.lower()).strip()
            norm2 = re.sub(r'[^\w\s]', '', text2.lower()).strip()
            
            # Use difflib for similarity
            similarity = difflib.SequenceMatcher(None, norm1, norm2).ratio()
            return similarity >= threshold
            
        except:
            return False
    
    def _save_all_categories(self):
        """Save all memory categories"""
        self.save_memory(self.appointments, 'smart_appointments.json')
        self.save_memory(self.life_events, 'smart_life_events.json')
        self.save_memory(self.conversation_highlights, 'smart_highlights.json')
        self.save_memory(self.health_states, 'smart_health_states.json')
        self.save_memory(self.mood_states, 'smart_mood_states.json')
        self.save_memory(self.visits, 'smart_visits.json')
        self.save_memory(self.episodes, 'episodes.json')
        self.save_memory(self.hypothesis_memories, 'hypothesis_memories.json')
        self.save_memory(self.knowledge_graph, 'knowledge_graph.json')
