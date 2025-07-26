"""
Local Memory Manager - Handle memory updates without LLM calls
Created: 2025-01-17
Purpose: Fast, local memory storage for immediate responses
Features: JSON-based storage, pattern recognition, simple fact extraction
"""

import json
import os
import time
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict

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
        """Extract memory information from text without LLM calls"""
        memories = []
        text_lower = text.lower().strip()
        timestamp = datetime.now().isoformat()
        
        # Extract actions
        for pattern in self.action_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                memory = MemoryEntry(
                    timestamp=timestamp,
                    user_id=user_id,
                    text=text,
                    memory_type="action",
                    extracted_info={
                        "action": match.strip(),
                        "pattern": pattern,
                        "context": "user_reported_action"
                    },
                    confidence=0.9
                )
                memories.append(memory)
        
        # Extract preferences
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
                        "pattern": pattern
                    },
                    confidence=0.8
                )
                memories.append(memory)
        
        # Extract facts
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
                        "category": "personal_info"
                    },
                    confidence=0.9
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
                    "question": "?" in text
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
        """Store memories locally"""
        for memory in memories:
            user_id = memory.user_id
            
            # Initialize user if not exists
            if user_id not in self.memory_data["users"]:
                self.memory_data["users"][user_id] = {
                    "actions": [],
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
            
            # Map memory type to category (in case of mismatch)
            memory_type = memory.memory_type
            if memory_type not in ["actions", "preferences", "facts", "context"]:
                # Default to context if unknown type
                memory_type = "context"
            
            # Store in appropriate category
            memory_dict = asdict(memory)
            user_data[memory_type].append(memory_dict)
            user_data["last_activity"] = memory.timestamp
            
            # Keep only recent memories (last 100 per category)
            for category in ["actions", "preferences", "facts", "context"]:
                if len(user_data[category]) > 100:
                    user_data[category] = user_data[category][-100:]
        
        self._save_memory()
    
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
        """Process user input and update memory locally"""
        start_time = time.time()
        
        # Extract memories
        memories = self.extract_memory_from_text(text, user_id)
        
        # Store memories
        if memories:
            self.store_memories(memories)
        
        # Get context for response
        recent_memories = self.get_recent_memories(user_id, 5)
        
        processing_time = time.time() - start_time
        
        return {
            "memories_extracted": len(memories),
            "processing_time": processing_time,
            "recent_memories": recent_memories,
            "last_action": self.get_last_action(user_id)
        }
    
    def get_memory_context_for_llm(self, user_id: str) -> str:
        """Get memory context string for LLM prompt"""
        memories = self.get_recent_memories(user_id, 5)
        context_parts = []
        
        # Add recent actions
        if memories["actions"]:
            recent_actions = [m["extracted_info"]["action"] for m in memories["actions"][-3:]]
            context_parts.append(f"Recent actions: {', '.join(recent_actions)}")
        
        # Add preferences
        if memories["preferences"]:
            recent_prefs = [
                f"{m['extracted_info']['sentiment']} {m['extracted_info']['subject']}" 
                for m in memories["preferences"][-2:]
            ]
            context_parts.append(f"Preferences: {', '.join(recent_prefs)}")
        
        # Add facts
        if memories["facts"]:
            recent_facts = [m["extracted_info"]["fact"] for m in memories["facts"][-2:]]
            context_parts.append(f"Facts: {', '.join(recent_facts)}")
        
        return " | ".join(context_parts) if context_parts else ""
    
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

# Global instance
local_memory_manager = LocalMemoryManager()