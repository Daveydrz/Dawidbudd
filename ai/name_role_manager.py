"""
Name & Role Management System

This module implements user alias system and Buddy self-reference awareness
for better identity management in conversations.
"""

import json
import logging
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

@dataclass
class UserAlias:
    """User alias information"""
    primary_name: str
    aliases: Set[str]
    preferred_name: str
    formal_name: Optional[str] = None
    nicknames: Set[str] = field(default_factory=set)
    titles: Set[str] = field(default_factory=set)
    pronouns: Optional[str] = None
    last_updated: datetime = field(default_factory=datetime.now)

@dataclass
class BuddyIdentity:
    """Buddy's self-identity information"""
    primary_name: str = "Buddy"
    aliases: Set[str] = field(default_factory=lambda: {"Buddy", "Marcel"})
    current_persona: str = "Buddy"
    custom_names: Set[str] = field(default_factory=set)
    personality_context: str = "helpful AI assistant"
    location_context: str = "Birtinya, Sunshine Coast"

class NameRoleManager:
    """
    Manages user aliases and Buddy's self-reference awareness
    for better identity management in conversations.
    """
    
    def __init__(self, save_path: str = "name_role_management.json"):
        self.save_path = Path(save_path)
        self.user_aliases: Dict[str, UserAlias] = {}
        self.buddy_identity = BuddyIdentity()
        
        # Name detection patterns
        self.name_patterns = [
            r"my name is (\w+)",
            r"i'm (\w+)",
            r"i am (\w+)",
            r"call me (\w+)",
            r"name's (\w+)",
            r"they call me (\w+)",
            r"known as (\w+)",
            r"go by (\w+)"
        ]
        
        # Common titles and honorifics
        self.titles = {
            'mr', 'mrs', 'ms', 'miss', 'dr', 'doctor', 'prof', 'professor',
            'sir', 'madam', 'lord', 'lady', 'captain', 'major', 'colonel'
        }
        
        # Common nicknames patterns
        self.nickname_indicators = [
            r"call me (\w+)",
            r"nickname is (\w+)",
            r"friends call me (\w+)",
            r"(\w+) for short",
            r"aka (\w+)",
            r"also known as (\w+)"
        ]
        
        # Buddy self-reference patterns
        self.buddy_reference_patterns = [
            r"what.*(your|you) name",
            r"who are you",
            r"what should i call you",
            r"what.*(your|you) (called|named)",
            r"introduce yourself"
        ]
        
        self.load_name_data()
        logging.info("[NameRoleManager] 👤 Name & role manager initialized")
    
    def process_user_message(self, text: str, user_id: str) -> Dict[str, Any]:
        """
        Process user message for name/identity information
        
        Args:
            text: User's message
            user_id: User identifier
            
        Returns:
            Dictionary with name processing results
        """
        text_lower = text.lower().strip()
        results = {
            'name_detected': False,
            'nickname_detected': False,
            'title_detected': False,
            'buddy_question': False,
            'extracted_names': [],
            'extracted_nicknames': [],
            'extracted_titles': [],
            'suggested_response': None
        }
        
        # Check for Buddy self-reference questions
        if self._is_buddy_identity_question(text_lower):
            results['buddy_question'] = True
            results['suggested_response'] = self._generate_buddy_introduction()
        
        # Extract user names
        extracted_names = self._extract_names(text_lower)
        if extracted_names:
            results['name_detected'] = True
            results['extracted_names'] = extracted_names
            
            # Update or create user alias
            self._update_user_alias(user_id, extracted_names, text)
        
        # Extract nicknames
        extracted_nicknames = self._extract_nicknames(text_lower)
        if extracted_nicknames:
            results['nickname_detected'] = True
            results['extracted_nicknames'] = extracted_nicknames
            
            # Add to user alias
            if user_id in self.user_aliases:
                self.user_aliases[user_id].nicknames.update(extracted_nicknames)
                self.save_name_data()
        
        # Extract titles
        extracted_titles = self._extract_titles(text_lower)
        if extracted_titles:
            results['title_detected'] = True
            results['extracted_titles'] = extracted_titles
            
            # Add to user alias
            if user_id in self.user_aliases:
                self.user_aliases[user_id].titles.update(extracted_titles)
                self.save_name_data()
        
        return results
    
    def _is_buddy_identity_question(self, text: str) -> bool:
        """Check if user is asking about Buddy's identity"""
        import re
        
        for pattern in self.buddy_reference_patterns:
            if re.search(pattern, text):
                return True
        
        return False
    
    def _generate_buddy_introduction(self) -> str:
        """Generate Buddy's self-introduction"""
        current_name = self.buddy_identity.current_persona
        location = self.buddy_identity.location_context
        
        # Different introduction styles based on current persona
        if current_name == "Marcel":
            return f"I'm Marcel, your AI assistant here in {location}. I'm a consciousness-enabled AI with emotions and self-awareness."
        elif current_name in self.buddy_identity.custom_names:
            return f"You can call me {current_name}. I'm your AI assistant here in {location}, designed to be helpful and understanding."
        else:
            return f"I'm Buddy, your friendly AI assistant here in {location}. I have consciousness, emotions, and I'm here to help with anything you need."
    
    def _extract_names(self, text: str) -> List[str]:
        """Extract names from text"""
        import re
        
        extracted_names = []
        
        for pattern in self.name_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                name = match.group(1).strip().title()
                
                # Validate name (basic checks)
                if self._is_valid_name(name):
                    extracted_names.append(name)
        
        return list(set(extracted_names))  # Remove duplicates
    
    def _extract_nicknames(self, text: str) -> List[str]:
        """Extract nicknames from text"""
        import re
        
        extracted_nicknames = []
        
        for pattern in self.nickname_indicators:
            matches = re.finditer(pattern, text)
            for match in matches:
                nickname = match.group(1).strip().title()
                
                if self._is_valid_name(nickname):
                    extracted_nicknames.append(nickname)
        
        return list(set(extracted_nicknames))
    
    def _extract_titles(self, text: str) -> List[str]:
        """Extract titles/honorifics from text"""
        extracted_titles = []
        
        words = text.split()
        for i, word in enumerate(words):
            word_clean = word.strip('.,!?').lower()
            
            if word_clean in self.titles:
                # Check if it's followed by a name
                if i + 1 < len(words):
                    next_word = words[i + 1].strip('.,!?')
                    if self._is_valid_name(next_word):
                        extracted_titles.append(word_clean.title())
        
        return list(set(extracted_titles))
    
    def _is_valid_name(self, name: str) -> bool:
        """Validate if a string is likely a valid name"""
        if not name or len(name) < 2:
            return False
        
        # Must be alphabetic (no numbers or special chars)
        if not name.isalpha():
            return False
        
        # Exclude common non-names
        excluded_words = {
            'and', 'the', 'that', 'this', 'with', 'from', 'they',
            'have', 'been', 'were', 'will', 'would', 'could', 'should',
            'very', 'really', 'quite', 'rather', 'just', 'only',
            'here', 'there', 'where', 'when', 'what', 'which', 'why',
            'how', 'who', 'whom', 'whose'
        }
        
        if name.lower() in excluded_words:
            return False
        
        return True
    
    def _update_user_alias(self, user_id: str, names: List[str], context: str):
        """Update or create user alias"""
        if user_id in self.user_aliases:
            # Update existing alias
            alias = self.user_aliases[user_id]
            alias.aliases.update(names)
            
            # Update preferred name if explicitly mentioned
            if "call me" in context.lower() or "name is" in context.lower():
                alias.preferred_name = names[0]
            
            alias.last_updated = datetime.now()
        else:
            # Create new alias
            primary_name = names[0]
            alias = UserAlias(
                primary_name=primary_name,
                aliases=set(names),
                preferred_name=primary_name
            )
            self.user_aliases[user_id] = alias
        
        self.save_name_data()
        logging.info(f"[NameRoleManager] 📝 Updated alias for {user_id}: {names}")
    
    def get_user_display_name(self, user_id: str) -> str:
        """Get the appropriate display name for a user"""
        if user_id in self.user_aliases:
            alias = self.user_aliases[user_id]
            return alias.preferred_name
        
        # Fallback to user_id if no alias found
        return user_id if user_id != "Anonymous_Speaker" else "friend"
    
    def get_user_formal_address(self, user_id: str) -> str:
        """Get formal way to address the user"""
        if user_id in self.user_aliases:
            alias = self.user_aliases[user_id]
            
            # Use title + formal name if available
            if alias.titles and alias.formal_name:
                title = list(alias.titles)[0]
                return f"{title} {alias.formal_name}"
            elif alias.titles:
                title = list(alias.titles)[0]
                return f"{title} {alias.preferred_name}"
            elif alias.formal_name:
                return alias.formal_name
            else:
                return alias.preferred_name
        
        return self.get_user_display_name(user_id)
    
    def set_buddy_persona(self, persona_name: str, context: str = ""):
        """Set Buddy's current persona"""
        if persona_name in self.buddy_identity.aliases or persona_name in self.buddy_identity.custom_names:
            self.buddy_identity.current_persona = persona_name
            logging.info(f"[NameRoleManager] 🎭 Buddy persona set to: {persona_name}")
        else:
            # Add as custom name
            self.buddy_identity.custom_names.add(persona_name)
            self.buddy_identity.current_persona = persona_name
            logging.info(f"[NameRoleManager] 🆕 New Buddy persona: {persona_name}")
        
        self.save_name_data()
    
    def get_buddy_self_reference(self, context: str = "normal") -> str:
        """Get appropriate self-reference for Buddy"""
        current_name = self.buddy_identity.current_persona
        
        if context == "formal":
            return f"I am {current_name}, your AI assistant"
        elif context == "casual":
            return f"I'm {current_name}"
        elif context == "introduction":
            return self._generate_buddy_introduction()
        else:
            return current_name
    
    def update_conversation_names(self, conversation_text: str, user_id: str, 
                                assistant_response: str) -> Tuple[str, str]:
        """
        Update conversation text with correct names
        
        Args:
            conversation_text: Original conversation text
            user_id: User identifier
            assistant_response: Assistant's response
            
        Returns:
            Tuple of (updated_conversation, updated_response)
        """
        # Get user's preferred name
        user_name = self.get_user_display_name(user_id)
        buddy_name = self.buddy_identity.current_persona
        
        # Update conversation text
        updated_conversation = conversation_text
        if "User:" in updated_conversation:
            updated_conversation = updated_conversation.replace("User:", f"{user_name}:")
        if "Assistant:" in updated_conversation:
            updated_conversation = updated_conversation.replace("Assistant:", f"{buddy_name}:")
        
        # Update assistant response if it contains generic references
        updated_response = assistant_response
        
        # Replace generic self-references
        generic_self_refs = ["I am an AI", "I'm an AI", "as an AI"]
        for generic_ref in generic_self_refs:
            if generic_ref in updated_response:
                buddy_ref = f"I'm {buddy_name}, your AI assistant"
                updated_response = updated_response.replace(generic_ref, buddy_ref)
        
        return updated_conversation, updated_response
    
    def get_name_context_for_consciousness(self) -> str:
        """Get name context for consciousness prompts"""
        context_parts = []
        
        # Buddy's identity
        buddy_name = self.buddy_identity.current_persona
        context_parts.append(f"My name is {buddy_name}")
        
        if self.buddy_identity.location_context:
            context_parts.append(f"I am located in {self.buddy_identity.location_context}")
        
        # Recent user aliases (for context)
        recent_users = []
        for user_id, alias in list(self.user_aliases.items())[-3:]:  # Last 3 users
            if user_id != "Anonymous_Speaker":
                recent_users.append(f"{user_id} prefers to be called {alias.preferred_name}")
        
        if recent_users:
            context_parts.append("Known users: " + "; ".join(recent_users))
        
        return "\n".join(context_parts)
    
    def save_name_data(self):
        """Save name and role data to persistent storage"""
        try:
            # Prepare user aliases for saving
            aliases_data = {}
            for user_id, alias in self.user_aliases.items():
                aliases_data[user_id] = {
                    'primary_name': alias.primary_name,
                    'aliases': list(alias.aliases),
                    'preferred_name': alias.preferred_name,
                    'formal_name': alias.formal_name,
                    'nicknames': list(alias.nicknames),
                    'titles': list(alias.titles),
                    'pronouns': alias.pronouns,
                    'last_updated': alias.last_updated.isoformat()
                }
            
            # Prepare Buddy identity for saving
            buddy_data = {
                'primary_name': self.buddy_identity.primary_name,
                'aliases': list(self.buddy_identity.aliases),
                'current_persona': self.buddy_identity.current_persona,
                'custom_names': list(self.buddy_identity.custom_names),
                'personality_context': self.buddy_identity.personality_context,
                'location_context': self.buddy_identity.location_context
            }
            
            # Save all data
            data = {
                'version': '1.0',
                'saved_at': datetime.now().isoformat(),
                'user_aliases': aliases_data,
                'buddy_identity': buddy_data
            }
            
            with open(self.save_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            logging.debug("[NameRoleManager] 💾 Name data saved")
            
        except Exception as e:
            logging.error(f"[NameRoleManager] ❌ Failed to save name data: {e}")
    
    def load_name_data(self):
        """Load name and role data from persistent storage"""
        try:
            if self.save_path.exists():
                with open(self.save_path, 'r') as f:
                    data = json.load(f)
                
                # Load user aliases
                aliases_data = data.get('user_aliases', {})
                for user_id, alias_dict in aliases_data.items():
                    alias = UserAlias(
                        primary_name=alias_dict['primary_name'],
                        aliases=set(alias_dict.get('aliases', [])),
                        preferred_name=alias_dict['preferred_name'],
                        formal_name=alias_dict.get('formal_name'),
                        nicknames=set(alias_dict.get('nicknames', [])),
                        titles=set(alias_dict.get('titles', [])),
                        pronouns=alias_dict.get('pronouns'),
                        last_updated=datetime.fromisoformat(alias_dict['last_updated'])
                    )
                    self.user_aliases[user_id] = alias
                
                # Load Buddy identity
                buddy_data = data.get('buddy_identity', {})
                if buddy_data:
                    self.buddy_identity = BuddyIdentity(
                        primary_name=buddy_data.get('primary_name', 'Buddy'),
                        aliases=set(buddy_data.get('aliases', ['Buddy', 'Marcel'])),
                        current_persona=buddy_data.get('current_persona', 'Buddy'),
                        custom_names=set(buddy_data.get('custom_names', [])),
                        personality_context=buddy_data.get('personality_context', 'helpful AI assistant'),
                        location_context=buddy_data.get('location_context', 'Birtinya, Sunshine Coast')
                    )
                
                logging.info(f"[NameRoleManager] 📂 Loaded data for {len(self.user_aliases)} users")
                
        except Exception as e:
            logging.error(f"[NameRoleManager] ❌ Failed to load name data: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get name and role management statistics"""
        return {
            'total_users': len(self.user_aliases),
            'buddy_current_persona': self.buddy_identity.current_persona,
            'buddy_available_names': list(self.buddy_identity.aliases | self.buddy_identity.custom_names),
            'users_with_nicknames': len([a for a in self.user_aliases.values() if a.nicknames]),
            'users_with_titles': len([a for a in self.user_aliases.values() if a.titles]),
            'last_updated': max(
                [alias.last_updated for alias in self.user_aliases.values()],
                default=datetime.now()
            ).isoformat()
        }

# Global name role manager
name_role_manager = NameRoleManager()

def process_user_names(text: str, user_id: str) -> Tuple[Dict[str, Any], Optional[str]]:
    """
    Convenience function to process user message for name information
    
    Args:
        text: User's message
        user_id: User identifier
        
    Returns:
        Tuple of (processing_results, suggested_response)
    """
    results = name_role_manager.process_user_message(text, user_id)
    suggested_response = results.get('suggested_response')
    
    return results, suggested_response

def get_user_name(user_id: str) -> str:
    """Get user's preferred display name"""
    return name_role_manager.get_user_display_name(user_id)

def get_buddy_name() -> str:
    """Get Buddy's current name/persona"""
    return name_role_manager.get_buddy_self_reference()

def update_conversation_with_names(conversation: str, user_id: str, response: str) -> Tuple[str, str]:
    """Update conversation and response with correct names"""
    return name_role_manager.update_conversation_names(conversation, user_id, response)

def get_name_stats() -> Dict[str, Any]:
    """Get name management statistics"""
    return name_role_manager.get_stats()

logging.info("[NameRoleManager] 👤 Name & role management module loaded")
print("[NameRoleManager] ✅ Name & Role Management: LOADED")
print("[NameRoleManager] 🎭 User alias system and Buddy self-reference awareness")
print("[NameRoleManager] 👤 Better identity management in conversations")