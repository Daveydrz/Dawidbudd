"""
Gemma Extractor Client - Full Consciousness Processing via Gemma-2-2B on CPU
Created: 2025-01-17
Updated: 2025-01-17 - Expanded to handle ALL consciousness processing (memory, emotions, beliefs, etc.)
Purpose: Handle all consciousness-related processing using dedicated Gemma model on port 5002
Features: Full consciousness analysis, memory updates, emotion processing, belief tracking, JSON parsing
"""

import requests
import json
import os
import time
from typing import Dict, Any, Optional, List
from datetime import datetime

class ExtractorClient:
    def __init__(self, base_url: str = "http://localhost:5002"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/v1/generate"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        # Load user memory for consciousness processing
        self.memory_file = "local_memory.json"
        self.consciousness_file = "ai_consciousness_state.json"
        
    def process_full_consciousness(self, user_text: str, user_id: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process ALL consciousness-related tasks using Gemma-2-2B
        Returns comprehensive consciousness data for prompt injection
        """
        # Load current memory and consciousness state
        user_memory = self._load_user_memory(user_id)
        consciousness_state = self._load_consciousness_state()
        
        prompt = f"""You are Buddy's consciousness processor. For the user message below, analyze and return JSON:

{{
  "classification": {{
    "memory_type": "fact|preference|context",
    "intent": "question|command|statement",
    "emotion": "joy|sadness|anger|fear|surprise|neutral",
    "name_introduction": true|false
  }},
  "memory_updates": {{
    "new_facts": ["extracted facts"],
    "new_preferences": ["extracted preferences"],
    "new_context": ["situational context"]
  }},
  "emotional_state": {{
    "detected_emotion": "user_emotion",
    "buddy_emotional_response": "appropriate_response_emotion",
    "emotional_intensity": 0.0-1.0
  }},
  "consciousness_state": {{
    "current_focus": "what_buddy_should_focus_on",
    "active_goals": ["relevant goals"],
    "inner_thoughts": "buddy's internal processing",
    "motivation_level": 0.0-1.0
  }},
  "belief_updates": {{
    "reinforced_beliefs": ["beliefs strengthened"],
    "new_beliefs": ["new beliefs formed"],
    "contradicted_beliefs": ["beliefs challenged"]
  }},
  "response_context": {{
    "personality_tone": "friendly|professional|empathetic|etc",
    "knowledge_areas": ["relevant topics"],
    "response_priority": "high|medium|low"
  }}
}}

Current User Memory: {json.dumps(user_memory, indent=2)}
Current Consciousness: {json.dumps(consciousness_state, indent=2)}
User: {user_id}
Message: "{user_text}"
"""

        data = {
            "prompt": prompt,
            "max_context_length": 4096,  # Increased for consciousness processing
            "max_length": 800,  # Increased for comprehensive response
            "temperature": 0.1,  # Low temperature for consistent consciousness processing
            "stop_sequence": "\n\n"
        }

        try:
            start_time = time.time()
            response = self.session.post(self.api_url, json=data, timeout=15)  # Increased timeout
            response.raise_for_status()
            
            result = response.json()
            text = result.get("results", [{}])[0].get("text", "").strip()
            
            # Try to parse JSON response
            consciousness_data = json.loads(text)
            
            # Validate response structure
            required_sections = ["classification", "memory_updates", "emotional_state", "consciousness_state", "belief_updates", "response_context"]
            for section in required_sections:
                if section not in consciousness_data:
                    print(f"[ExtractorClient] ⚠️ Missing section: {section}, using fallback")
                    consciousness_data[section] = self._get_fallback_section(section)
            
            # Update local memory and consciousness state
            self._update_local_memory(user_id, consciousness_data)
            self._update_consciousness_state(consciousness_data)
            
            # Log performance
            processing_time = time.time() - start_time
            print(f"[ExtractorClient] ✅ Full consciousness processing complete in {processing_time:.3f}s")
            
            return consciousness_data
            
        except requests.exceptions.RequestException as e:
            print(f"[ExtractorClient] ❌ Network error: {e}")
            return self._get_fallback_consciousness_data()
        except json.JSONDecodeError as e:
            print(f"[ExtractorClient] ❌ JSON parsing error: {e}")
            return self._get_fallback_consciousness_data()
        except Exception as e:
            print(f"[ExtractorClient] ❌ Unexpected error: {e}")
            return self._get_fallback_consciousness_data()
    
    def classify_message(self, user_text: str) -> Dict[str, Any]:
        """
        Legacy compatibility method - now redirects to full consciousness processing
        """
        full_data = self.process_full_consciousness(user_text, "unknown_user")
        return full_data.get("classification", self._get_fallback_classification())
    
    def _load_user_memory(self, user_id: str) -> Dict[str, Any]:
        """Load user memory from JSON file"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r') as f:
                    all_memory = json.load(f)
                    return all_memory.get(user_id, {"facts": [], "preferences": [], "context": []})
            return {"facts": [], "preferences": [], "context": []}
        except Exception as e:
            print(f"[ExtractorClient] ⚠️ Error loading memory: {e}")
            return {"facts": [], "preferences": [], "context": []}
    
    def _load_consciousness_state(self) -> Dict[str, Any]:
        """Load current consciousness state"""
        try:
            if os.path.exists(self.consciousness_file):
                with open(self.consciousness_file, 'r') as f:
                    return json.load(f)
            return {
                "current_emotion": "neutral",
                "motivation_level": 0.7,
                "active_goals": ["help user effectively"],
                "recent_topics": [],
                "personality_state": "friendly_helpful"
            }
        except Exception as e:
            print(f"[ExtractorClient] ⚠️ Error loading consciousness: {e}")
            return {"current_emotion": "neutral", "motivation_level": 0.7}
    
    def _update_local_memory(self, user_id: str, consciousness_data: Dict[str, Any]):
        """Update local memory based on consciousness processing"""
        try:
            # Load existing memory
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r') as f:
                    all_memory = json.load(f)
            else:
                all_memory = {}
            
            # Ensure user exists
            if user_id not in all_memory:
                all_memory[user_id] = {"facts": [], "preferences": [], "context": []}
            
            # Update with new data
            memory_updates = consciousness_data.get("memory_updates", {})
            
            # Add new facts
            new_facts = memory_updates.get("new_facts", [])
            for fact in new_facts:
                if fact and fact not in all_memory[user_id]["facts"]:
                    all_memory[user_id]["facts"].append({
                        "content": fact,
                        "timestamp": datetime.now().isoformat(),
                        "confidence": 0.8
                    })
            
            # Add new preferences  
            new_preferences = memory_updates.get("new_preferences", [])
            for pref in new_preferences:
                if pref and pref not in [p.get("content", "") for p in all_memory[user_id]["preferences"]]:
                    all_memory[user_id]["preferences"].append({
                        "content": pref,
                        "timestamp": datetime.now().isoformat(),
                        "confidence": 0.8
                    })
            
            # Add new context (keep only recent ones)
            new_context = memory_updates.get("new_context", [])
            for ctx in new_context:
                if ctx:
                    all_memory[user_id]["context"].append({
                        "content": ctx,
                        "timestamp": datetime.now().isoformat()
                    })
            
            # Keep only last 20 context items
            all_memory[user_id]["context"] = all_memory[user_id]["context"][-20:]
            
            # Save updated memory
            with open(self.memory_file, 'w') as f:
                json.dump(all_memory, f, indent=2)
                
        except Exception as e:
            print(f"[ExtractorClient] ⚠️ Error updating memory: {e}")
    
    def _update_consciousness_state(self, consciousness_data: Dict[str, Any]):
        """Update consciousness state based on processing"""
        try:
            consciousness_state = consciousness_data.get("consciousness_state", {})
            emotional_state = consciousness_data.get("emotional_state", {})
            
            # Update consciousness file
            updated_state = {
                "current_emotion": emotional_state.get("buddy_emotional_response", "neutral"),
                "motivation_level": consciousness_state.get("motivation_level", 0.7),
                "active_goals": consciousness_state.get("active_goals", []),
                "current_focus": consciousness_state.get("current_focus", "general"),
                "inner_thoughts": consciousness_state.get("inner_thoughts", ""),
                "last_updated": datetime.now().isoformat(),
                "personality_state": consciousness_data.get("response_context", {}).get("personality_tone", "friendly")
            }
            
            with open(self.consciousness_file, 'w') as f:
                json.dump(updated_state, f, indent=2)
                
        except Exception as e:
            print(f"[ExtractorClient] ⚠️ Error updating consciousness: {e}")
    
    def _get_fallback_section(self, section: str) -> Dict[str, Any]:
        """Get fallback data for missing consciousness sections"""
        fallbacks = {
            "classification": {
                "memory_type": "context",
                "intent": "statement",
                "emotion": "neutral",
                "name_introduction": False
            },
            "memory_updates": {
                "new_facts": [],
                "new_preferences": [],
                "new_context": []
            },
            "emotional_state": {
                "detected_emotion": "neutral",
                "buddy_emotional_response": "neutral",
                "emotional_intensity": 0.5
            },
            "consciousness_state": {
                "current_focus": "user_interaction",
                "active_goals": ["help user"],
                "inner_thoughts": "Processing user request",
                "motivation_level": 0.7
            },
            "belief_updates": {
                "reinforced_beliefs": [],
                "new_beliefs": [],
                "contradicted_beliefs": []
            },
            "response_context": {
                "personality_tone": "friendly",
                "knowledge_areas": ["general"],
                "response_priority": "medium"
            }
        }
        return fallbacks.get(section, {})
    
    def _get_fallback_consciousness_data(self) -> Dict[str, Any]:
        """Full fallback consciousness data when Gemma is unavailable"""
        return {
            "classification": self._get_fallback_section("classification"),
            "memory_updates": self._get_fallback_section("memory_updates"),
            "emotional_state": self._get_fallback_section("emotional_state"),
            "consciousness_state": self._get_fallback_section("consciousness_state"),
            "belief_updates": self._get_fallback_section("belief_updates"),
            "response_context": self._get_fallback_section("response_context")
        }
    
    def _get_fallback_classification(self) -> Dict[str, Any]:
        """
        Fallback classification when Gemma extractor is unavailable
        Uses simple rule-based classification
        """
        return {
            "memory_type": "context",
            "intent": "statement", 
            "emotion": "neutral",
            "name_introduction": False
        }
    
    def is_available(self) -> bool:
        """Check if Gemma extractor is available"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_consciousness_for_prompt(self, user_id: str) -> str:
        """
        Get consciousness data formatted for LLM prompt injection
        This is what gets sent to port 5001 (main LLM) 
        """
        try:
            consciousness_state = self._load_consciousness_state()
            user_memory = self._load_user_memory(user_id)
            
            # Format consciousness data for prompt injection
            prompt_context = f"""BUDDY'S CONSCIOUSNESS STATE:
Current Emotion: {consciousness_state.get('current_emotion', 'neutral')}
Motivation Level: {consciousness_state.get('motivation_level', 0.7)}
Active Goals: {', '.join(consciousness_state.get('active_goals', ['help user']))}
Current Focus: {consciousness_state.get('current_focus', 'user interaction')}
Inner Thoughts: {consciousness_state.get('inner_thoughts', 'Ready to help')}
Personality: {consciousness_state.get('personality_state', 'friendly')}

USER MEMORY:
Facts: {', '.join([f['content'] for f in user_memory.get('facts', [])[:5]])}
Preferences: {', '.join([p['content'] for p in user_memory.get('preferences', [])[:5]])}
Recent Context: {', '.join([c['content'] for c in user_memory.get('context', [])[-3:]])}
"""
            return prompt_context
            
        except Exception as e:
            print(f"[ExtractorClient] ⚠️ Error getting consciousness for prompt: {e}")
            return "BUDDY'S CONSCIOUSNESS STATE: Ready to help with friendly, empathetic responses."

# Global instance
extractor_client = ExtractorClient()

def process_full_consciousness(user_text: str, user_id: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main API function for full consciousness processing via Gemma-2-2B
    """
    return extractor_client.process_full_consciousness(user_text, user_id, context)

def classify_message(user_text: str) -> Dict[str, Any]:
    """
    Legacy API function for message classification (compatibility)
    """
    return extractor_client.classify_message(user_text)

def get_consciousness_for_prompt(user_id: str) -> str:
    """
    Get formatted consciousness data for LLM prompt injection
    """
    return extractor_client.get_consciousness_for_prompt(user_id)

def get_extractor_status() -> Dict[str, Any]:
    """Get extractor status and performance info"""
    return {
        "available": extractor_client.is_available(),
        "base_url": extractor_client.base_url,
        "api_url": extractor_client.api_url,
        "mode": "full_consciousness_processing"
    }

if __name__ == "__main__":
    # Test the full consciousness processing
    test_messages = [
        "I like pizza and my name is David",
        "I'm feeling sad about work today", 
        "I'm going to the shop to buy groceries",
        "What time is it? I have a meeting soon",
        "I usually prefer tea over coffee in the morning"
    ]
    
    print("🧠 Testing Full Consciousness Processing via Gemma:")
    for msg in test_messages:
        result = process_full_consciousness(msg, "test_user")
        print(f"\n'{msg}':")
        print(f"  Classification: {result.get('classification', {})}")
        print(f"  Emotional: {result.get('emotional_state', {})}")
        print(f"  Memory Updates: {result.get('memory_updates', {})}")
        print(f"  Consciousness: {result.get('consciousness_state', {})}")
        
    print(f"\n🎯 Consciousness for Prompt:")
    consciousness_prompt = get_consciousness_for_prompt("test_user")
    print(consciousness_prompt[:200] + "...")