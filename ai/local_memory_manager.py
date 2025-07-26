"""
Local Memory Manager - Handle memory updates without LLM calls
Created: 2025-01-17
Updated: 2025-01-17 - Integrated ONNX-like memory classifier
Purpose: Fast, local memory storage with intelligent categorization
Features: JSON-based storage, ONNX classifier, multi-language support
"""

import json
import os
import time
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict

# Note: Memory classification now handled by Gemma-2-2B on port 5002
# This file provides local pattern-based fallback only

@dataclass
class MemoryEntry:
    """Simple memory entry structure"""
    timestamp: str
    user_id: str
    text: str
    memory_type: str  # 'fact', 'action', 'preference', 'context'
    extracted_info: Dict[str, Any]
    confidence: float

class LocalMemoryManager:
    """Local memory manager for fast, LLM-free memory operations"""
    
    def __init__(self, memory_file: str = "local_memory.json"):
        self.memory_file = memory_file
        self.memory_data = self._load_memory()
        
        # Simple patterns for fact extraction (no LLM needed)
        self.action_patterns = [
            r"i'?m going to (.+)",
            r"i'?m at (.+)",
            r"i went to (.+)",
            r"i'?m back from (.+)",
            r"i just (.+)",
            r"i'?m (.+ing .+)",
            r"i am going to (.+)",
            r"i am at (.+)",
            r"i am (.+ing .+)",
        ]
        
        self.preference_patterns = [
            r"i (like|love|prefer|enjoy) (.+)",
            r"i (hate|dislike) (.+)",
            r"my favorite (.+) is (.+)",
            r"i usually (.+)",
        ]
        
        self.fact_patterns = [
            r"my name is (.+)",
            r"i'?m (.+) years old",
            r"i work (.+)",
            r"i live (.+)",
            r"my (.+) is (.+)",
        ]
    
    def _load_memory(self) -> Dict[str, List[Dict]]:
        """Load memory from JSON file"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            return {"users": {}}
        except Exception as e:
            print(f"[LocalMemory] ⚠️ Error loading memory: {e}")
            return {"users": {}}
    
    def _save_memory(self):
        """Save memory to JSON file"""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.memory_data, f, indent=2)
        except Exception as e:
            print(f"[LocalMemory] ⚠️ Error saving memory: {e}")
    
    def extract_memory_from_text(self, text: str, user_id: str) -> List[MemoryEntry]:
        """
        Extract memory information using pattern-based classification
        NOTE: Full memory classification now handled by Gemma-2-2B on port 5002
        This method provides local fallback only
        """
        memories = []
        text_stripped = text.strip()
        timestamp = datetime.now().isoformat()
        
        if not text_stripped:
            return memories
        
        print(f"[LocalMemory] ℹ️ Using pattern-based fallback - Full classification on port 5002")
        
        # Use pattern-based extraction as fallback
        return self._extract_memory_with_patterns(text, user_id)
    
    def _extract_classified_metadata(self, text: str, memory_type: str) -> Dict[str, Any]:
        """Extract additional metadata based on classification type"""
        text_lower = text.lower().strip()
        
        if memory_type == "preference":
            return self._extract_preference_metadata(text_lower)
        elif memory_type == "fact":
            return self._extract_fact_metadata(text_lower) 
        elif memory_type == "context":
            return self._extract_context_metadata(text_lower)
        else:
            return {"classified_type": memory_type, "source": "onnx_classifier"}
    
    def _extract_preference_metadata(self, text_lower: str) -> Dict[str, Any]:
        """Extract preference-specific metadata"""
        # Sentiment analysis
        sentiment = "neutral"
        if any(word in text_lower for word in ["love", "adore", "favorite", "like", "enjoy", "prefer"]):
            sentiment = "positive"
        elif any(word in text_lower for word in ["hate", "dislike", "can't stand", "despise", "avoid"]):
            sentiment = "negative"
        
        # Extract subject (what they like/dislike)
        subject = "unknown"
        
        # Common preference patterns
        preference_patterns = [
            r"(?:i|my)\s+(?:really\s+)?(?:love|like|enjoy|prefer|adore)\s+(.+?)(?:\.|!|$)",
            r"(?:i|my)\s+(?:really\s+)?(?:hate|dislike|can't\s+stand|despise)\s+(.+?)(?:\.|!|$)", 
            r"(?:i|my)\s+(?:favorite|favourite)\s+(.+?)\s+is\s+(.+?)(?:\.|!|$)",
            r"(.+?)\s+(?:is|are)\s+(?:my\s+)?(?:favorite|favourite)(?:\.|!|$)",
        ]
        
        for pattern in preference_patterns:
            match = re.search(pattern, text_lower)
            if match:
                if len(match.groups()) == 1:
                    subject = match.group(1).strip()
                elif len(match.groups()) == 2:
                    subject = match.group(2).strip()  # For "favorite X is Y" patterns
                break
        
        return {
            "sentiment": sentiment,
            "subject": subject,
            "preference_type": "like_dislike",
            "intensity": "high" if any(word in text_lower for word in ["love", "adore", "hate", "despise"]) else "medium",
            "source": "onnx_classifier"
        }
    
    def _extract_fact_metadata(self, text_lower: str) -> Dict[str, Any]:
        """Extract fact-specific metadata"""
        # Determine fact category
        fact_category = "personal_info"
        
        if any(word in text_lower for word in ["name", "called"]):
            fact_category = "identity"
        elif any(word in text_lower for word in ["age", "years old", "born"]):
            fact_category = "age_birth"
        elif any(word in text_lower for word in ["live", "address", "from"]):
            fact_category = "location"
        elif any(word in text_lower for word in ["work", "job", "career", "profession"]):
            fact_category = "occupation"
        elif any(word in text_lower for word in ["family", "wife", "husband", "child", "parent", "mom", "dad"]):
            fact_category = "family"
        elif any(word in text_lower for word in ["allergic", "condition", "medical", "health"]):
            fact_category = "medical"
        elif any(word in text_lower for word in ["height", "weight", "hair", "eyes", "tall", "short"]):
            fact_category = "physical"
        
        # Extract the actual fact value
        fact_value = "unknown"
        
        # Common fact extraction patterns
        fact_patterns = [
            r"my\s+name\s+is\s+(.+?)(?:\.|!|$)",
            r"i\s+am\s+(.+?)\s+years?\s+old(?:\.|!|$)",
            r"i\s+live\s+(?:in|at)\s+(.+?)(?:\.|!|$)",
            r"i\s+work\s+(?:as|at|for)\s+(.+?)(?:\.|!|$)",
            r"my\s+(.+?)\s+is\s+(.+?)(?:\.|!|$)",
        ]
        
        for pattern in fact_patterns:
            match = re.search(pattern, text_lower)
            if match:
                if len(match.groups()) == 1:
                    fact_value = match.group(1).strip()
                elif len(match.groups()) == 2:
                    fact_value = match.group(2).strip()  # For "my X is Y" patterns
                break
        
        return {
            "fact_category": fact_category,
            "fact_value": fact_value,
            "permanence": "permanent" if fact_category in ["identity", "age_birth"] else "semi_permanent",
            "verified": False,
            "source": "onnx_classifier"
        }
    
    def _extract_context_metadata(self, text_lower: str) -> Dict[str, Any]:
        """Extract context-specific metadata"""
        # Determine context type
        context_type = "general"
        
        if any(word in text_lower for word in ["going", "went", "at", "from", "to"]):
            context_type = "location_activity"
        elif any(word in text_lower for word in ["doing", "making", "working", "playing"]):
            context_type = "current_activity"
        elif any(word in text_lower for word in ["feel", "feeling", "tired", "happy", "sad"]):
            context_type = "emotional_state"
        elif any(word in text_lower for word in ["just", "finished", "completed", "done"]):
            context_type = "recent_completion"
        elif any(word in text_lower for word in ["about to", "going to", "will", "planning"]):
            context_type = "future_intention"
        
        # Extract activity or location
        activity = "unknown"
        
        # Context extraction patterns
        context_patterns = [
            r"i'?m\s+(?:going\s+to|at|in)\s+(?:the\s+)?(.+?)(?:\.|!|$)",
            r"i\s+(?:just|recently)\s+(.+?)(?:\.|!|$)",
            r"i'?m\s+(?:currently\s+)?(.+?)(?:\.|!|$)",
            r"i\s+(?:feel|am\s+feeling)\s+(.+?)(?:\.|!|$)",
        ]
        
        for pattern in context_patterns:
            match = re.search(pattern, text_lower)
            if match:
                activity = match.group(1).strip()
                break
        
        return {
            "context_type": context_type,
            "activity": activity,
            "temporal": "current" if any(word in text_lower for word in ["now", "currently", "right now"]) else "general",
            "duration": "temporary",
            "source": "onnx_classifier"
        }
    
    def _extract_memory_with_patterns(self, text: str, user_id: str) -> List[MemoryEntry]:
        """Fallback pattern-based extraction (original method)"""
        memories = []
        text_lower = text.lower().strip()
        timestamp = datetime.now().isoformat()
        
        # Extract actions (fallback)
        for pattern in self.action_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                memory = MemoryEntry(
                    timestamp=timestamp,
                    user_id=user_id,
                    text=text,
                    memory_type="context",  # Actions are now classified as context
                    extracted_info={
                        "action": match.strip(),
                        "pattern": pattern,
                        "context": "user_reported_action",
                        "source": "pattern_fallback"
                    },
                    confidence=0.7  # Lower confidence for fallback
                )
                memories.append(memory)
        
        # Extract preferences (fallback)
        for pattern in self.preference_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                if isinstance(match, tuple):
                    sentiment, subject = match
                else:
                    sentiment, subject = "neutral", match
                
                memory = MemoryEntry(
                    timestamp=timestamp,
                    user_id=user_id,
                    text=text,
                    memory_type="preference",
                    extracted_info={
                        "sentiment": sentiment,
                        "subject": subject.strip(),
                        "pattern": pattern,
                        "source": "pattern_fallback"
                    },
                    confidence=0.6  # Lower confidence for fallback
                )
                memories.append(memory)
        
        # Extract facts (fallback)
        for pattern in self.fact_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                memory = MemoryEntry(
                    timestamp=timestamp,
                    user_id=user_id,
                    text=text,
                    memory_type="fact",
                    extracted_info={
                        "fact": match.strip(),
                        "pattern": pattern,
                        "category": "personal_info",
                        "source": "pattern_fallback"
                    },
                    confidence=0.6  # Lower confidence for fallback
                )
                memories.append(memory)
        
        # Store general context if no specific patterns matched
        if not memories:
            memory = MemoryEntry(
                timestamp=timestamp,
                user_id=user_id,
                text=text,
                memory_type="context",
                extracted_info={
                    "topic": self._extract_simple_topic(text),
                    "length": len(text.split()),
                    "question": "?" in text,
                    "source": "general_fallback"
                },
                confidence=0.5
            )
            memories.append(memory)
        
        return memories
    
    def _extract_simple_topic(self, text: str) -> str:
        """Extract simple topic without LLM"""
        # Simple keyword-based topic extraction
        topics = {
            "weather": ["weather", "rain", "sunny", "cold", "hot", "temperature"],
            "food": ["eat", "food", "hungry", "restaurant", "cooking", "meal"],
            "work": ["work", "job", "office", "meeting", "project", "boss"],
            "family": ["family", "mom", "dad", "sister", "brother", "kids"],
            "travel": ["travel", "trip", "vacation", "plane", "hotel", "visit"],
            "technology": ["computer", "internet", "phone", "app", "software"],
            "health": ["health", "doctor", "medicine", "sick", "hospital"],
            "entertainment": ["movie", "music", "game", "book", "tv", "show"]
        }
        
        text_lower = text.lower()
        for topic, keywords in topics.items():
            if any(keyword in text_lower for keyword in keywords):
                return topic
        
        return "general"
    
    def store_memories(self, memories: List[MemoryEntry]):
        """Store memories locally with enhanced categorization"""
        for memory in memories:
            user_id = memory.user_id
            
            # Initialize user if not exists
            if user_id not in self.memory_data["users"]:
                self.memory_data["users"][user_id] = {
                    "actions": [],      # Deprecated - keeping for backward compatibility
                    "preferences": [],
                    "facts": [],
                    "context": [],
                    "last_activity": memory.timestamp
                }
            
            # Ensure all categories exist
            user_data = self.memory_data["users"][user_id]
            for category in ["actions", "preferences", "facts", "context"]:
                if category not in user_data:
                    user_data[category] = []
            
            # Map memory type appropriately
            memory_type = memory.memory_type
            
            # Actions are now stored as context events
            if memory_type == "action":
                memory_type = "context"
                # Update memory type in the object too
                memory.memory_type = "context"
            
            # Map singular to plural forms for storage
            type_mapping = {
                "preference": "preferences",
                "fact": "facts",
                "context": "context"
            }
            
            storage_type = type_mapping.get(memory_type, "context")
            
            # Validate storage type 
            if storage_type not in ["preferences", "facts", "context"]:
                print(f"[LocalMemory] ⚠️ Unknown storage type '{storage_type}', defaulting to context")
                storage_type = "context"
            
            # Store in appropriate category
            memory_dict = asdict(memory)
            user_data[storage_type].append(memory_dict)
            user_data["last_activity"] = memory.timestamp
            
            # Keep only recent memories (last 100 per category)
            for category in ["actions", "preferences", "facts", "context"]:
                if len(user_data[category]) > 100:
                    user_data[category] = user_data[category][-100:]
        
        self._save_memory()
    
    def get_memory_summary_by_type(self, user_id: str) -> Dict[str, int]:
        """Get count of memories by type for a user"""
        if user_id not in self.memory_data["users"]:
            return {"preferences": 0, "facts": 0, "context": 0}
        
        user_data = self.memory_data["users"][user_id]
        return {
            "preferences": len(user_data.get("preferences", [])),
            "facts": len(user_data.get("facts", [])),
            "context": len(user_data.get("context", [])),
            "total": (len(user_data.get("preferences", [])) + 
                     len(user_data.get("facts", [])) + 
                     len(user_data.get("context", [])))
        }
    
    def get_classifier_performance_stats(self) -> Dict[str, Any]:
        """Get memory classifier performance statistics"""
        if MEMORY_CLASSIFIER_AVAILABLE:
            return get_classifier_stats()
        else:
            return {
                "model_loaded": False,
                "error": "Memory classifier not available"
            }
    
    def get_recent_memories(self, user_id: str, limit: int = 10) -> Dict[str, Any]:
        """Get recent memories for a user"""
        if user_id not in self.memory_data["users"]:
            return {"actions": [], "preferences": [], "facts": [], "context": []}
        
        user_memories = self.memory_data["users"][user_id]
        return {
            "actions": user_memories.get("actions", [])[-limit:],
            "preferences": user_memories.get("preferences", [])[-limit:],
            "facts": user_memories.get("facts", [])[-limit:],
            "context": user_memories.get("context", [])[-limit:],
            "last_activity": user_memories.get("last_activity", "")
        }
    
    def get_last_action(self, user_id: str) -> Optional[str]:
        """Get user's last action quickly"""
        memories = self.get_recent_memories(user_id, 1)
        actions = memories.get("actions", [])
        if actions:
            return actions[-1]["extracted_info"]["action"]
        return None
    
    def process_user_input(self, text: str, user_id: str) -> Dict[str, Any]:
        """Process user input and update memory locally with all ONNX classifiers"""
        start_time = time.time()
        
        # Run all ONNX classifiers (local, no LLM calls)
        classification_results = self._classify_user_input_all(text)
        
        # Extract memories using ONNX memory classifier
        memories = self.extract_memory_from_text(text, user_id)
        
        # Store memories
        if memories:
            self.store_memories(memories)
        
        # Get context for response
        recent_memories = self.get_recent_memories(user_id, 5)
        memory_summary = self.get_memory_summary_by_type(user_id)
        
        processing_time = time.time() - start_time
        
        # Enhanced reporting with all classifier results
        result = {
            "memories_extracted": len(memories),
            "processing_time": processing_time,
            "recent_memories": recent_memories,
            "last_action": self.get_last_action(user_id),
            "memory_summary": memory_summary,
            "classifiers_used": {
                "memory": MEMORY_CLASSIFIER_AVAILABLE,
                "intent": INTENT_CLASSIFIER_AVAILABLE,
                "emotion": EMOTION_CLASSIFIER_AVAILABLE,
                "name": NAME_CLASSIFIER_AVAILABLE
            },
            "classifications": classification_results
        }
        
        # Add memory type breakdown if memories were extracted
        if memories:
            memory_types = {}
            for memory in memories:
                mem_type = memory.memory_type
                if mem_type in memory_types:
                    memory_types[mem_type] += 1
                else:
                    memory_types[mem_type] = 1
            result["memory_types_extracted"] = memory_types
        
        return result
    
    def process_user_input_with_onnx(self, text: str, user_id: str):
        """
        DEPRECATED: This method is replaced by Gemma-2-2B processing on port 5002
        All classification now handled via ai.extractor_client.process_full_consciousness()
        """
        print(f"[LocalMemory] ⚠️ process_user_input_with_onnx is deprecated - use port 5002 instead")
        
        # Extract memories using pattern-based fallback
        memories = self.extract_memory_from_text(text, user_id)
        self.store_memories(memories)
        
        print(f"[LocalMemory] ℹ️ Stored {len(memories)} memories using pattern fallback")
        
    def _classify_user_input_all(self, text: str) -> Dict[str, Any]:
        """
        DEPRECATED: All classification now handled by Gemma-2-2B on port 5002
        Use ai.extractor_client.process_full_consciousness() instead
        """
        print(f"[LocalMemory] ⚠️ ONNX classification is deprecated - using port 5002 Gemma instead")
        
        # Return basic fallback results
        return {
            "memory": {"type": "context", "confidence": 0.5},
            "intent": {"type": "casual_chat", "confidence": 0.5},
            "emotion": {"type": "neutral", "confidence": 0.5, "intensity": "low"},
            "name": {"type": "no_name", "confidence": 0.5, "extracted_names": []}
        }
    
    def get_all_classifier_stats(self) -> Dict[str, Any]:
        """Get performance statistics for all ONNX classifiers"""
        stats = {}
        
        if MEMORY_CLASSIFIER_AVAILABLE:
            try:
                stats["memory"] = get_classifier_stats()
            except Exception as e:
                stats["memory"] = {"error": str(e)}
        
        if INTENT_CLASSIFIER_AVAILABLE:
            try:
                stats["intent"] = get_intent_classifier_stats()
            except Exception as e:
                stats["intent"] = {"error": str(e)}
        
        if EMOTION_CLASSIFIER_AVAILABLE:
            try:
                stats["emotion"] = get_emotion_classifier_stats()
            except Exception as e:
                stats["emotion"] = {"error": str(e)}
        
        if NAME_CLASSIFIER_AVAILABLE:
            try:
                stats["name"] = get_name_classifier_stats()
            except Exception as e:
                stats["name"] = {"error": str(e)}
        
        return stats

    def get_memory_context_for_llm(self, user_id: str, include_classifications: bool = True) -> str:
        """Get memory context string for LLM prompt with enhanced categorization"""
        memories = self.get_recent_memories(user_id, 5)
        context_parts = []
        
        # Add recent facts (most important for understanding user)
        if memories["facts"]:
            recent_facts = []
            for fact_memory in memories["facts"][-3:]:  # Last 3 facts
                extracted_info = fact_memory.get("extracted_info", {})
                if extracted_info.get("source") == "onnx_classifier":
                    # Enhanced fact formatting
                    fact_category = extracted_info.get("fact_category", "personal")
                    fact_value = extracted_info.get("fact_value", "unknown")
                    recent_facts.append(f"{fact_category}: {fact_value}")
                else:
                    # Fallback formatting
                    fact = extracted_info.get("fact", "unknown")
                    recent_facts.append(fact)
            
            if recent_facts:
                context_parts.append(f"Facts: {', '.join(recent_facts)}")
        
        # Add preferences (important for personality)
        if memories["preferences"]:
            recent_prefs = []
            for pref_memory in memories["preferences"][-2:]:  # Last 2 preferences
                extracted_info = pref_memory.get("extracted_info", {})
                if extracted_info.get("source") == "onnx_classifier":
                    # Enhanced preference formatting
                    sentiment = extracted_info.get("sentiment", "neutral")
                    subject = extracted_info.get("subject", "unknown")
                    intensity = extracted_info.get("intensity", "medium")
                    
                    if sentiment == "positive":
                        pref_text = f"likes {subject}" + (" (strongly)" if intensity == "high" else "")
                    elif sentiment == "negative":
                        pref_text = f"dislikes {subject}" + (" (strongly)" if intensity == "high" else "")
                    else:
                        pref_text = f"feels neutral about {subject}"
                    
                    recent_prefs.append(pref_text)
                else:
                    # Fallback formatting
                    sentiment = extracted_info.get("sentiment", "neutral")
                    subject = extracted_info.get("subject", "unknown")
                    recent_prefs.append(f"{sentiment} {subject}")
            
            if recent_prefs:
                context_parts.append(f"Preferences: {', '.join(recent_prefs)}")
        
        # Add recent context/actions (for immediate relevance)
        if memories["context"]:
            recent_contexts = []
            for context_memory in memories["context"][-3:]:  # Last 3 context items
                extracted_info = context_memory.get("extracted_info", {})
                if extracted_info.get("source") == "onnx_classifier":
                    # Enhanced context formatting
                    context_type = extracted_info.get("context_type", "general")
                    activity = extracted_info.get("activity", "unknown")
                    
                    if context_type == "location_activity":
                        recent_contexts.append(f"location: {activity}")
                    elif context_type == "current_activity":
                        recent_contexts.append(f"doing: {activity}")
                    elif context_type == "recent_completion":
                        recent_contexts.append(f"completed: {activity}")
                    else:
                        recent_contexts.append(activity)
                else:
                    # Fallback formatting
                    action = extracted_info.get("action", extracted_info.get("topic", "unknown"))
                    recent_contexts.append(action)
            
            if recent_contexts:
                context_parts.append(f"Recent: {', '.join(recent_contexts)}")
        
        result = " | ".join(context_parts) if context_parts else ""
        
        # Add classifier performance note if available
        if MEMORY_CLASSIFIER_AVAILABLE and context_parts:
            stats = get_classifier_stats()
            if stats.get("performance_target_met", False):
                result += " [AI-classified]"
        
        return result
    
    def cleanup_old_memories(self, days: int = 30):
        """Clean up old memories"""
        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_iso = cutoff_date.isoformat()
        
        for user_id in self.memory_data["users"]:
            for category in ["actions", "preferences", "facts", "context"]:
                self.memory_data["users"][user_id][category] = [
                    memory for memory in self.memory_data["users"][user_id][category]
                    if memory.get("timestamp", "") > cutoff_iso
                ]
        
        self._save_memory()

    def get_user_facts(self, user_id: str) -> List[str]:
        """Get user facts for LLM prompt"""
        if user_id not in self.memory_data["users"]:
            return []
        
        facts = []
        user_facts = self.memory_data["users"][user_id].get("facts", [])
        for fact_memory in user_facts[-5:]:  # Last 5 facts
            extracted_info = fact_memory.get("extracted_info", {})
            if extracted_info.get("source") == "onnx_classifier":
                fact_value = extracted_info.get("fact_value", "unknown")
                if fact_value != "unknown":
                    facts.append(fact_value)
            else:
                fact = extracted_info.get("fact", "")
                if fact:
                    facts.append(fact)
        return facts
    
    def get_user_preferences(self, user_id: str) -> List[str]:
        """Get user preferences for LLM prompt"""
        if user_id not in self.memory_data["users"]:
            return []
        
        preferences = []
        user_prefs = self.memory_data["users"][user_id].get("preferences", [])
        for pref_memory in user_prefs[-3:]:  # Last 3 preferences
            extracted_info = pref_memory.get("extracted_info", {})
            if extracted_info.get("source") == "onnx_classifier":
                sentiment = extracted_info.get("sentiment", "neutral")
                subject = extracted_info.get("subject", "unknown")
                if subject != "unknown":
                    if sentiment == "positive":
                        preferences.append(f"likes {subject}")
                    elif sentiment == "negative":
                        preferences.append(f"dislikes {subject}")
                    else:
                        preferences.append(f"neutral about {subject}")
            else:
                sentiment = extracted_info.get("sentiment", "")
                subject = extracted_info.get("subject", "")
                if subject:
                    preferences.append(f"{sentiment} {subject}")
        return preferences
    
    def get_recent_context(self, user_id: str, limit: int = 3) -> List[str]:
        """Get recent context/actions for LLM prompt"""
        if user_id not in self.memory_data["users"]:
            return []
        
        contexts = []
        user_contexts = self.memory_data["users"][user_id].get("context", [])
        for context_memory in user_contexts[-limit:]:  # Last N contexts
            extracted_info = context_memory.get("extracted_info", {})
            if extracted_info.get("source") == "onnx_classifier":
                activity = extracted_info.get("activity", "unknown")
                context_type = extracted_info.get("context_type", "general")
                if activity != "unknown":
                    if context_type == "location_activity":
                        contexts.append(f"at {activity}")
                    elif context_type == "current_activity":
                        contexts.append(f"doing {activity}")
                    else:
                        contexts.append(activity)
            else:
                action = extracted_info.get("action", "")
                if action:
                    contexts.append(action)
        return contexts
    
    def process_user_input_with_onnx(self, text: str, user_id: str):
        """Process user input using only ONNX classifiers - no LLM calls"""
        # Use the existing process_user_input method which already uses ONNX
        result = self.process_user_input(text, user_id)
        print(f"[LocalMemory] ONNX processing: {result['memories_extracted']} memories extracted")
        return result
    
    def update_memory(self, user_id: str, text: str, consciousness_data: Dict[str, Any]):
        """Update memory using full consciousness data from Gemma extractor (port 5002)"""
        start_time = time.time()
        
        if not consciousness_data:
            print("[LocalMemory] ⚠️ No consciousness data provided")
            return
        
        # Extract classification from consciousness data
        classification = consciousness_data.get("classification", {})
        memory_type = classification.get("memory_type", "context")
        intent = classification.get("intent", "statement")
        emotion = classification.get("emotion", "neutral") 
        name_introduction = classification.get("name_introduction", False)
        
        # Extract memory updates from consciousness processing
        memory_updates = consciousness_data.get("memory_updates", {})
        
        print(f"[LocalMemory] 🧠 Processing full consciousness data: {memory_type}/{intent}/{emotion}")
        
        # Process specific memory updates from Gemma
        stored_memories = []
        timestamp = datetime.now().isoformat()
        
        # Store new facts
        new_facts = memory_updates.get("new_facts", [])
        for fact in new_facts:
            if fact and fact.strip():
                fact_memory = MemoryEntry(
                    timestamp=timestamp,
                    user_id=user_id,
                    text=fact,
                    memory_type="fact",
                    extracted_info={
                        "fact_category": "general",
                        "fact_value": fact,
                        "source": "gemma_consciousness_processor",
                        "confidence": 0.85
                    },
                    confidence=0.85
                )
                stored_memories.append(fact_memory)
        
        # Store new preferences
        new_preferences = memory_updates.get("new_preferences", [])
        for pref in new_preferences:
            if pref and pref.strip():
                pref_memory = MemoryEntry(
                    timestamp=timestamp,
                    user_id=user_id,
                    text=pref,
                    memory_type="preference",
                    extracted_info={
                        "preference_type": "general",
                        "preference_value": pref,
                        "source": "gemma_consciousness_processor",
                        "confidence": 0.85
                    },
                    confidence=0.85
                )
                stored_memories.append(pref_memory)
        
        # Store new context
        new_context = memory_updates.get("new_context", [])
        for ctx in new_context:
            if ctx and ctx.strip():
                ctx_memory = MemoryEntry(
                    timestamp=timestamp,
                    user_id=user_id,
                    text=ctx,
                    memory_type="context",
                    extracted_info={
                        "context_type": "general",
                        "context_value": ctx,
                        "source": "gemma_consciousness_processor",
                        "confidence": 0.80
                    },
                    confidence=0.80
                )
                stored_memories.append(ctx_memory)
        
        # Store the main interaction as context if no specific updates
        if not stored_memories:
            main_memory = MemoryEntry(
                timestamp=timestamp,
                user_id=user_id,
                text=text,
                memory_type=memory_type,
                extracted_info={
                    "classification_source": "gemma_consciousness_processor",
                    "intent": intent,
                    "emotion": emotion,
                    "name_introduction": name_introduction,
                    "consciousness_data": consciousness_data,
                    "processing_time": time.time() - start_time
                },
                confidence=0.90
            )
            stored_memories.append(main_memory)
        
        # Store all memories
        if stored_memories:
            self.store_memories(stored_memories)
            print(f"[LocalMemory] 💾 Stored {len(stored_memories)} memory entries from consciousness processing")
        
        # Handle name introduction if detected
        if name_introduction or self._extract_names_from_text(text):
            names = self._extract_names_from_text(text)
            if names:
                print(f"[LocalMemory] 👤 Name introduction detected: {names}")
                
                # Store each name as a separate fact
                for name in names:
                    name_memory = MemoryEntry(
                        timestamp=timestamp,
                        user_id=user_id,
                        text=f"User's name is {name}",
                        memory_type="fact",
                        extracted_info={
                            "fact_category": "identity",
                            "fact_value": name,
                            "name_introduction": True,
                            "source": "name_extraction",
                            "confidence": 0.95
                        },
                        confidence=0.95
                    )
                    self.store_memories([name_memory])
                    print(f"[LocalMemory] ✅ Name '{name}' stored as fact")
        
        processing_time = time.time() - start_time
        print(f"[LocalMemory] ✅ Gemma memory update complete in {processing_time:.3f}s")
        
        return {
            "memory_type": memory_type,
            "intent": intent,
            "emotion": emotion,
            "name_introduction": name_introduction,
            "memories_stored": len(stored_memories),
            "processing_time": processing_time
        }
    
    def _extract_names_from_text(self, text: str) -> List[str]:
        """Simple name extraction from text"""
        # Look for patterns like "I'm [Name]", "My name is [Name]", "Call me [Name]"
        name_patterns = [
            r"my name is (\w+)",
            r"i'?m (\w+)",
            r"call me (\w+)",
            r"i'?m called (\w+)"
        ]
        
        names = []
        text_lower = text.lower()
        
        for pattern in name_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                # Capitalize first letter and add to names
                if len(match) > 1 and match.isalpha():
                    names.append(match.capitalize())
        
        return list(set(names))  # Remove duplicates
    
    def add_interaction(self, user_id: str, user_input: str, ai_response: str):
        """Add interaction to memory"""
        timestamp = datetime.now().isoformat()
        
        # Store the interaction as context
        interaction_memory = MemoryEntry(
            timestamp=timestamp,
            user_id=user_id,
            text=f"User said: {user_input}. Buddy replied: {ai_response[:100]}...",
            memory_type="context",
            extracted_info={
                "context_type": "interaction",
                "user_input": user_input,
                "ai_response": ai_response,
                "interaction_timestamp": timestamp,
                "source": "local_memory_manager"
            },
            confidence=1.0
        )
        
        self.store_memories([interaction_memory])
        print(f"[LocalMemory] Interaction stored for {user_id}")
        
    def get_user_facts(self, user_id: str) -> List[str]:
        """Get user facts for prompt injection"""
        try:
            if user_id not in self.memory_data["users"]:
                return []
            
            facts = self.memory_data["users"][user_id].get("facts", [])
            # Return just the content strings
            if facts and isinstance(facts[0], dict):
                return [fact.get("content", str(fact)) for fact in facts[-5:]]  # Last 5 facts
            else:
                return facts[-5:]  # Last 5 facts
        except Exception as e:
            print(f"[LocalMemory] ⚠️ Error getting facts: {e}")
            return []
    
    def get_user_preferences(self, user_id: str) -> List[str]:
        """Get user preferences for prompt injection"""
        try:
            if user_id not in self.memory_data["users"]:
                return []
            
            preferences = self.memory_data["users"][user_id].get("preferences", [])
            # Return just the content strings
            if preferences and isinstance(preferences[0], dict):
                return [pref.get("content", str(pref)) for pref in preferences[-5:]]  # Last 5 preferences
            else:
                return preferences[-5:]  # Last 5 preferences
        except Exception as e:
            print(f"[LocalMemory] ⚠️ Error getting preferences: {e}")
            return []
    
    def get_recent_context(self, user_id: str, limit: int = 3) -> List[str]:
        """Get recent context for prompt injection"""
        try:
            if user_id not in self.memory_data["users"]:
                return []
            
            context = self.memory_data["users"][user_id].get("context", [])
            # Return just the content strings
            if context and isinstance(context[0], dict):
                return [ctx.get("content", str(ctx)) for ctx in context[-limit:]]  # Last N context items
            else:
                return context[-limit:]  # Last N context items
        except Exception as e:
            print(f"[LocalMemory] ⚠️ Error getting context: {e}")
            return []
    
    def add_interaction(self, user_id: str, user_input: str, response: str):
        """Add interaction to memory"""
        try:
            # Extract memories from user input
            memories = self.extract_memory_from_text(user_input, user_id)
            if memories:
                self.store_memories(memories)
            
            # Store the interaction as context
            context_memory = MemoryEntry(
                timestamp=datetime.now().isoformat(),
                user_id=user_id,
                text=f"User: {user_input} | Buddy: {response}",
                memory_type="context",
                extracted_info={
                    "interaction": True,
                    "user_input": user_input,
                    "buddy_response": response,
                    "source": "interaction_log"
                },
                confidence=1.0
            )
            self.store_memories([context_memory])
            
            print(f"[LocalMemory] 💾 Stored interaction for {user_id}")
            
        except Exception as e:
            print(f"[LocalMemory] ⚠️ Error adding interaction: {e}")
            # Try a simpler approach if the above fails
            try:
                simple_context = MemoryEntry(
                    timestamp=datetime.now().isoformat(),
                    user_id=user_id,
                    text=f"Interaction: {user_input[:50]}...",
                    memory_type="context",
                    extracted_info={
                        "simple_interaction": True,
                        "source": "fallback_interaction_log"
                    },
                    confidence=0.8
                )
                self.store_memories([simple_context])
                print(f"[LocalMemory] 💾 Stored simple interaction for {user_id}")
            except Exception as e2:
                print(f"[LocalMemory] ❌ Failed to store interaction: {e2}")

    def get_user_context(self, user_id: str) -> Dict[str, List[str]]:
        """Get user context for immediate responses (no LLM delay)"""
        try:
            if "users" not in self.memory_data or user_id not in self.memory_data["users"]:
                return {"facts": [], "preferences": [], "context": []}
            
            user_memories = self.memory_data["users"][user_id]
            context = {"facts": [], "preferences": [], "context": []}
            
            # Extract recent facts (last 10) - check memory format
            facts = user_memories.get("facts", [])
            if facts:
                recent_facts = []
                for fact_entry in facts[-10:]:  # Last 10 facts
                    if isinstance(fact_entry, dict):
                        # New format with extracted_info
                        if "extracted_info" in fact_entry:
                            fact_text = fact_entry["extracted_info"].get("fact", fact_entry.get("text", ""))
                            if fact_text:
                                recent_facts.append(fact_text)
                        # Content format
                        elif "content" in fact_entry:
                            recent_facts.append(fact_entry["content"])
                        # Text format
                        elif "text" in fact_entry:
                            recent_facts.append(fact_entry["text"])
                    else:
                        # Simple string format
                        recent_facts.append(str(fact_entry))
                context["facts"] = recent_facts
            
            # Extract preferences (last 5)
            preferences = user_memories.get("preferences", [])
            if preferences:
                recent_preferences = []
                for pref_entry in preferences[-5:]:  # Last 5 preferences
                    if isinstance(pref_entry, dict):
                        # New format with extracted_info
                        if "extracted_info" in pref_entry:
                            sentiment = pref_entry["extracted_info"].get("sentiment", "likes")
                            subject = pref_entry["extracted_info"].get("subject", "")
                            if subject:
                                recent_preferences.append(f"{sentiment} {subject}")
                        # Content format
                        elif "content" in pref_entry:
                            recent_preferences.append(pref_entry["content"])
                        # Text format  
                        elif "text" in pref_entry:
                            recent_preferences.append(pref_entry["text"])
                    else:
                        # Simple string format
                        recent_preferences.append(str(pref_entry))
                context["preferences"] = recent_preferences
            
            # Extract recent context (last 5)
            contexts = user_memories.get("context", [])
            if contexts:
                recent_context = []
                for ctx_entry in contexts[-5:]:  # Last 5 context items
                    if isinstance(ctx_entry, dict):
                        # New format with extracted_info
                        if "extracted_info" in ctx_entry:
                            action = ctx_entry["extracted_info"].get("action", ctx_entry.get("text", ""))
                            if action:
                                recent_context.append(action)
                        # Content format
                        elif "content" in ctx_entry:
                            recent_context.append(ctx_entry["content"])
                        # Text format
                        elif "text" in ctx_entry:
                            recent_context.append(ctx_entry["text"])
                    else:
                        # Simple string format
                        recent_context.append(str(ctx_entry))
                context["context"] = recent_context
            
            print(f"[LocalMemory] 📋 Retrieved context for {user_id}: {len(context['facts'])} facts, {len(context['preferences'])} prefs, {len(context['context'])} context")
            return context
            
        except Exception as e:
            print(f"[LocalMemory] ⚠️ Error getting user context: {e}")
            return {"facts": [], "preferences": [], "context": []}


# Global instance
local_memory_manager = LocalMemoryManager()

def get_user_context(user_id: str) -> Dict[str, List[str]]:
    """API function to get user context"""
    return local_memory_manager.get_user_context(user_id)