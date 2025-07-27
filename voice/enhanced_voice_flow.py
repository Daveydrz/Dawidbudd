"""
Enhanced Voice Flow Manager
Following user's specified flow exactly:
1. Voice recognition → Match to cluster or create anonymous_01, anonymous_02, etc.
2. Name extraction from text → Link to voice profile
3. Multi-user support with separate memories/histories
4. Context preservation during token limits
"""

import json
import os
import time
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import re

from voice.database import known_users, anonymous_clusters, save_known_users
from voice.recognition import identify_speaker_with_confidence, generate_voice_embedding


class EnhancedVoiceFlow:
    """Enhanced voice flow following user's exact specifications"""
    
    def __init__(self):
        self.user_profiles = {}  # Track user profiles {voice_id: profile_data}
        self.anonymous_counter = 1
        self.current_user = None
        
        # Load existing profiles
        self._load_profiles()
        
    def _load_profiles(self):
        """Load existing voice profiles and anonymous clusters"""
        try:
            # Sync with existing database
            from voice.database import load_known_users
            load_known_users()
            
            # Count existing anonymous clusters to continue numbering
            anonymous_count = 0
            for user_id in known_users.keys():
                if user_id.startswith('Anonymous_'):
                    try:
                        num = int(user_id.split('_')[1])
                        anonymous_count = max(anonymous_count, num)
                    except:
                        pass
            
            self.anonymous_counter = anonymous_count + 1
            print(f"[EnhancedVoiceFlow] 📊 Loaded profiles - will start new anonymous at #{self.anonymous_counter}")
            
        except Exception as e:
            print(f"[EnhancedVoiceFlow] ⚠️ Error loading profiles: {e}")
    
    def process_voice_input(self, audio_data: Any, text: str) -> Tuple[str, str]:
        """
        Process voice input following user's exact flow:
        1. Voice recognition → Match or create anonymous cluster
        2. Check for name introduction in text
        3. Link name to voice profile if introduced
        """
        
        # Step 1: Voice Recognition
        voice_user_id, voice_status = self._identify_voice(audio_data)
        
        # Step 2: Check for name introduction
        extracted_name = self._extract_name_from_text(text)
        
        # Step 3: Handle name introduction
        if extracted_name and voice_user_id.startswith('Anonymous_'):
            # User is introducing themselves - link name to anonymous cluster
            print(f"[EnhancedVoiceFlow] 🎭 Name introduction detected: {extracted_name}")
            print(f"[EnhancedVoiceFlow] 🔗 Linking {extracted_name} to {voice_user_id}")
            
            linked_user_id = self._link_name_to_voice(extracted_name, voice_user_id, audio_data)
            
            # Update memory system
            self._update_user_identity(linked_user_id, extracted_name)
            
            return linked_user_id, "NAME_LINKED_TO_VOICE"
            
        elif extracted_name and not voice_user_id.startswith('Anonymous_'):
            # Known user introducing different name - potential conflict or update
            existing_name = self._get_stored_name(voice_user_id)
            if existing_name and existing_name.lower() != extracted_name.lower():
                print(f"[EnhancedVoiceFlow] ⚠️ Name conflict: Voice={voice_user_id} has stored name '{existing_name}' but said '{extracted_name}'")
                # For now, trust the voice recognition
                return voice_user_id, "NAME_CONFLICT_VOICE_TRUSTED"
            else:
                # Update or confirm name
                self._update_user_identity(voice_user_id, extracted_name)
                return voice_user_id, "NAME_CONFIRMED"
        
        # Step 4: Return voice identification result
        return voice_user_id, voice_status
    
    def _identify_voice(self, audio_data: Any) -> Tuple[str, str]:
        """Identify voice and return user_id and status"""
        try:
            # Generate voice embedding
            embedding = generate_voice_embedding(audio_data)
            if embedding is None:
                return "Daveydrz", "NO_EMBEDDING"
            
            # Try to match against existing profiles
            identified_user, confidence = identify_speaker_with_confidence(audio_data)
            
            if identified_user != "UNKNOWN" and confidence > 0.7:
                print(f"[EnhancedVoiceFlow] ✅ Voice matched: {identified_user} (confidence: {confidence:.3f})")
                return identified_user, "VOICE_RECOGNIZED"
            
            # No match - create new anonymous cluster
            anonymous_id = f"Anonymous_{self.anonymous_counter:02d}"
            self.anonymous_counter += 1
            
            print(f"[EnhancedVoiceFlow] 🆕 Creating new anonymous cluster: {anonymous_id}")
            
            # Create anonymous profile
            self._create_anonymous_profile(anonymous_id, embedding)
            
            return anonymous_id, "NEW_ANONYMOUS_CLUSTER"
            
        except Exception as e:
            print(f"[EnhancedVoiceFlow] ❌ Voice identification error: {e}")
            return "Daveydrz", "VOICE_ERROR"
    
    def _extract_name_from_text(self, text: str) -> Optional[str]:
        """Extract name from text using multiple patterns"""
        if not text:
            return None
            
        text_lower = text.lower().strip()
        
        # Name introduction patterns
        patterns = [
            r"my name is (\w+)",
            r"i'?m (\w+)(?:\s|$|[,.])",
            r"i am (\w+)(?:\s|$|[,.])",
            r"call me (\w+)",
            r"name'?s (\w+)",
            r"this is (\w+)",
            r"it'?s (\w+)(?:\s|$|[,.])",
            r"i am called (\w+)",
            r"you can call me (\w+)",
            r"the name is (\w+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                name = match.group(1).strip()
                # Validate name (basic checks)
                if len(name) >= 2 and name.isalpha() and name.lower() not in ['the', 'is', 'am', 'me', 'my']:
                    return name.capitalize()
        
        return None
    
    def _create_anonymous_profile(self, anonymous_id: str, embedding: np.ndarray):
        """Create a new anonymous voice profile"""
        try:
            timestamp = datetime.now().isoformat()
            
            # Add to known_users database
            known_users[anonymous_id] = {
                'username': anonymous_id,
                'status': 'anonymous',
                'voice_embeddings': [embedding.tolist()],
                'created_at': timestamp,
                'last_updated': timestamp,
                'is_anonymous': True,
                'embedding_count': 1,
                'voice_samples': 1,
                'confidence_threshold': 0.6,
                'real_name': None,
                'linked_from_anonymous': False
            }
            
            # Add to anonymous_clusters database
            anonymous_clusters[anonymous_id] = {
                'cluster_id': anonymous_id,
                'embeddings': [embedding.tolist()],
                'created_at': timestamp,
                'last_updated': timestamp,
                'status': 'anonymous',
                'sample_count': 1,
                'real_name': None,
                'linked_to_named': False
            }
            
            # Save to database
            save_known_users()
            
            print(f"[EnhancedVoiceFlow] ✅ Created anonymous profile: {anonymous_id}")
            
        except Exception as e:
            print(f"[EnhancedVoiceFlow] ❌ Error creating anonymous profile: {e}")
    
    def _link_name_to_voice(self, name: str, anonymous_id: str, audio_data: Any) -> str:
        """Link a real name to an anonymous voice cluster"""
        try:
            # Create new named profile from anonymous cluster
            named_id = name
            
            # Check if name already exists
            counter = 1
            original_name = name
            while named_id in known_users and not known_users[named_id].get('is_anonymous', False):
                named_id = f"{original_name}_{counter:02d}"
                counter += 1
            
            # Copy data from anonymous cluster
            if anonymous_id in known_users:
                anonymous_data = known_users[anonymous_id].copy()
                
                # Create named profile
                known_users[named_id] = {
                    'username': named_id,
                    'real_name': original_name,
                    'status': 'named',
                    'voice_embeddings': anonymous_data.get('voice_embeddings', []),
                    'created_at': anonymous_data.get('created_at'),
                    'last_updated': datetime.now().isoformat(),
                    'is_anonymous': False,
                    'embedding_count': anonymous_data.get('embedding_count', 1),
                    'voice_samples': anonymous_data.get('voice_samples', 1),
                    'confidence_threshold': 0.7,
                    'linked_from_anonymous': True,
                    'previous_anonymous_id': anonymous_id
                }
                
                # Update anonymous cluster to show it's been linked
                if anonymous_id in anonymous_clusters:
                    anonymous_clusters[anonymous_id]['linked_to_named'] = True
                    anonymous_clusters[anonymous_id]['linked_name'] = named_id
                    anonymous_clusters[anonymous_id]['real_name'] = original_name
                
                # Save changes
                save_known_users()
                
                print(f"[EnhancedVoiceFlow] ✅ Linked name '{original_name}' to voice cluster")
                print(f"[EnhancedVoiceFlow] 🔗 Anonymous {anonymous_id} → Named {named_id}")
                
                return named_id
            
            else:
                print(f"[EnhancedVoiceFlow] ⚠️ Anonymous cluster {anonymous_id} not found for linking")
                return anonymous_id
                
        except Exception as e:
            print(f"[EnhancedVoiceFlow] ❌ Error linking name to voice: {e}")
            return anonymous_id
    
    def _update_user_identity(self, user_id: str, name: str):
        """Update user identity in memory system"""
        try:
            # Update local memory with the name
            from ai.local_memory_manager import local_memory_manager
            
            # Store the name as a fact
            memory_entry = {
                'type': 'fact',
                'content': f"User's name is {name}",
                'confidence': 0.9,
                'source': 'voice_introduction'
            }
            
            local_memory_manager.store_memories([memory_entry], user_id)
            
            print(f"[EnhancedVoiceFlow] 💾 Updated identity: {user_id} = {name}")
            
        except Exception as e:
            print(f"[EnhancedVoiceFlow] ⚠️ Error updating user identity: {e}")
    
    def _get_stored_name(self, user_id: str) -> Optional[str]:
        """Get stored name for a user"""
        try:
            if user_id in known_users:
                profile = known_users[user_id]
                return profile.get('real_name') or profile.get('display_name')
            return None
        except Exception as e:
            print(f"[EnhancedVoiceFlow] ⚠️ Error getting stored name: {e}")
            return None
    
    def get_user_display_name(self, user_id: str) -> str:
        """Get display name for user"""
        try:
            stored_name = self._get_stored_name(user_id)
            if stored_name:
                return stored_name
            elif user_id.startswith('Anonymous_'):
                return f"Speaker {user_id.split('_')[1]}"
            else:
                return user_id
        except Exception as e:
            print(f"[EnhancedVoiceFlow] ⚠️ Error getting display name: {e}")
            return user_id or "friend"
    
    def get_user_context_for_llm(self, user_id: str) -> str:
        """Get user context for LLM injection"""
        try:
            from ai.local_memory_manager import local_memory_manager
            
            # Get user's memory context
            user_context = local_memory_manager.get_user_context(user_id)
            
            # Get display name
            display_name = self.get_user_display_name(user_id)
            
            # Build context string
            facts = user_context.get('facts', [])
            preferences = user_context.get('preferences', [])
            recent_context = user_context.get('context', [])
            
            context = f"""CURRENT USER: {user_id} (known as: {display_name})
VOICE PROFILE: {"Anonymous speaker" if user_id.startswith('Anonymous_') else "Recognized voice"}

USER MEMORY:
Facts: {', '.join(facts[-5:]) if facts else 'Learning about user'}
Preferences: {', '.join(preferences[-3:]) if preferences else 'Discovering preferences'}
Recent Context: {', '.join(recent_context[-3:]) if recent_context else 'Fresh conversation'}

INTERACTION CONTEXT:
- Remember this is {display_name} speaking
- Maintain continuity with their previous conversations
- Show awareness of their specific identity and history"""

            return context
            
        except Exception as e:
            print(f"[EnhancedVoiceFlow] ⚠️ Error getting user context: {e}")
            return f"CURRENT USER: {user_id}"
    
    def handle_context_limit(self, user_id: str, current_context: str) -> str:
        """Handle context window limits by preserving consciousness data"""
        try:
            print(f"[EnhancedVoiceFlow] 🔄 Handling context limit for {user_id}")
            
            # Get essential user data that must be preserved
            display_name = self.get_user_display_name(user_id)
            
            from ai.local_memory_manager import local_memory_manager
            user_context = local_memory_manager.get_user_context(user_id)
            
            # Create compressed context with only essential information
            essential_facts = user_context.get('facts', [])[-3:]  # Last 3 facts
            essential_preferences = user_context.get('preferences', [])[-2:]  # Last 2 preferences
            essential_context = user_context.get('context', [])[-2:]  # Last 2 context items
            
            compressed_context = f"""ESSENTIAL USER DATA for {display_name} ({user_id}):
Key Facts: {', '.join(essential_facts) if essential_facts else 'None'}
Preferences: {', '.join(essential_preferences) if essential_preferences else 'None'}
Recent: {', '.join(essential_context) if essential_context else 'New conversation'}

CONSCIOUSNESS STATE: Maintaining awareness of {display_name}'s identity and continuing conversation naturally."""
            
            print(f"[EnhancedVoiceFlow] ✅ Context compressed from {len(current_context)} to {len(compressed_context)} characters")
            
            return compressed_context
            
        except Exception as e:
            print(f"[EnhancedVoiceFlow] ❌ Error handling context limit: {e}")
            return f"USER: {user_id} - Continuing conversation"


# Global instance
enhanced_voice_flow = EnhancedVoiceFlow()


def process_voice_input(audio_data: Any, text: str) -> Tuple[str, str]:
    """Main API function for processing voice input"""
    return enhanced_voice_flow.process_voice_input(audio_data, text)


def get_user_display_name(user_id: str) -> str:
    """Get display name for user"""  
    return enhanced_voice_flow.get_user_display_name(user_id)


def get_user_context_for_llm(user_id: str) -> str:
    """Get user context for LLM injection"""
    return enhanced_voice_flow.get_user_context_for_llm(user_id)


def handle_context_limit(user_id: str, current_context: str) -> str:
    """Handle context window limits"""
    return enhanced_voice_flow.handle_context_limit(user_id, current_context)