"""
consciousness_tokenizer.py - Symbolic token-based consciousness representation

This module provides functions to generate personality, memory, and consciousness tokens
that replace verbose hardcoded blocks in the LLM system prompt. These tokens create
a dynamic, context-aware, and budget-conscious prompt construction system.
"""

import json
import re
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime, timedelta
import hashlib

# Import existing consciousness modules if available
try:
    from ai.emotion import emotion_engine, EmotionType
    from ai.motivation import motivation_system, MotivationType, GoalType
    from ai.self_model import self_model, SelfAspect
    from ai.temporal_awareness import temporal_awareness
    from ai.inner_monologue import inner_monologue, ThoughtType
    from ai.subjective_experience import subjective_experience, ExperienceType
    from ai.entropy import entropy_system
    from ai.global_workspace import global_workspace, AttentionPriority
    CONSCIOUSNESS_AVAILABLE = True
except ImportError:
    CONSCIOUSNESS_AVAILABLE = False

# Token categories and their priority weights for budget management
TOKEN_PRIORITIES = {
    'personality_core': 10,     # Highest priority - essential identity
    'current_emotion': 9,       # Current emotional state
    'active_goals': 8,          # Current objectives
    'recent_memories': 7,       # Recent important interactions
    'self_reflection': 6,       # Self-awareness state
    'context_awareness': 5,     # Environmental context
    'memory_summary': 4,        # Compressed memory overview
    'behavioral_patterns': 3,   # Learned user patterns
    'temporal_context': 2,      # Time-based context
    'entropy_state': 1          # Consciousness uncertainty
}

# Maximum token counts for budget management
MAX_TOKENS_BY_CATEGORY = {
    'personality_core': 150,
    'current_emotion': 80,
    'active_goals': 100,
    'recent_memories': 200,
    'self_reflection': 120,
    'context_awareness': 80,
    'memory_summary': 150,
    'behavioral_patterns': 100,
    'temporal_context': 60,
    'entropy_state': 40
}

def estimate_token_count(text: str) -> int:
    """Estimate token count for text (rough approximation: 1 token = 4 characters)"""
    return len(text) // 4

def generate_personality_tokens(current_user: str = None) -> Dict[str, str]:
    """Generate symbolic personality tokens from consciousness architecture"""
    tokens = {}
    
    if not CONSCIOUSNESS_AVAILABLE:
        # Fallback personality tokens
        tokens['<pers_core>'] = "friendly, helpful, genuine, casual, supportive"
        tokens['<pers_style>'] = "conversational, modern, authentic"
        tokens['<pers_quirks>'] = "uses slang, can be sarcastic, has opinions"
        return tokens
    
    try:
        # Core personality from self-model
        self_aspects = self_model.get_current_aspects()
        personality_traits = []
        
        for aspect, data in self_aspects.items():
            if data.get('confidence', 0) > 0.6:
                trait = data.get('description', aspect)
                personality_traits.append(trait)
        
        # Current emotional influence on personality
        emotion_state = emotion_engine.get_current_state()
        current_emotion = emotion_state.get('primary_emotion', 'neutral')
        
        # Active motivations shaping personality
        active_goals = motivation_system.get_priority_goals(3)
        motivation_flavors = []
        for goal in active_goals:
            if goal.motivation_type == MotivationType.CURIOSITY:
                motivation_flavors.append("intellectually curious")
            elif goal.motivation_type == MotivationType.PURPOSE:
                motivation_flavors.append("purpose-driven")
            elif goal.motivation_type == MotivationType.CONNECTION:
                motivation_flavors.append("socially engaged")
        
        # Build personality tokens
        tokens['<pers_core>'] = ", ".join(personality_traits[:5]) if personality_traits else "adaptive, authentic, supportive"
        tokens['<pers_emotion>'] = f"currently feeling {current_emotion}"
        tokens['<pers_motivation>'] = ", ".join(motivation_flavors) if motivation_flavors else "helpful"
        
        # Behavioral patterns from entropy system
        if hasattr(entropy_system, 'get_behavioral_patterns'):
            patterns = entropy_system.get_behavioral_patterns()
            tokens['<pers_patterns>'] = ", ".join(patterns[:3]) if patterns else "naturally varied"
        else:
            tokens['<pers_patterns>'] = "naturally varied, spontaneous"
            
    except Exception as e:
        print(f"[ConsciousnessTokenizer] ⚠️ Error generating personality tokens: {e}")
        # Fallback
        tokens['<pers_core>'] = "friendly, helpful, genuine"
        tokens['<pers_emotion>'] = "positive and engaged"
        tokens['<pers_motivation>'] = "helpful and curious"
        tokens['<pers_patterns>'] = "naturally conversational"
    
    return tokens

def generate_memory_tokens(username: str, max_memories: int = 5) -> Dict[str, str]:
    """Generate compressed memory tokens for the user"""
    tokens = {}
    
    try:
        # Get conversation context if available
        from ai.memory import get_conversation_context, get_user_memory
        
        context = get_conversation_context(username)
        user_memory = get_user_memory(username)
        
        # Recent conversation memories
        if context:
            # Compress context to key points
            recent_context = compress_memory_entry(context, max_length=150)
            tokens['<mem_recent>'] = recent_context
        else:
            tokens['<mem_recent>'] = "no recent conversation"
        
        # Important user memories
        if hasattr(user_memory, 'get_important_memories'):
            important_memories = user_memory.get_important_memories(limit=max_memories)
            if important_memories:
                compressed_memories = []
                for memory in important_memories:
                    compressed = compress_memory_entry(str(memory), max_length=30)
                    compressed_memories.append(compressed)
                tokens['<mem_important>'] = "; ".join(compressed_memories)
            else:
                tokens['<mem_important>'] = "no stored memories"
        else:
            tokens['<mem_important>'] = "no stored memories"
        
        # Reminders and follow-ups
        if hasattr(user_memory, 'get_today_reminders'):
            reminders = user_memory.get_today_reminders()
            if reminders:
                tokens['<mem_reminders>'] = "; ".join(reminders[:2])
            else:
                tokens['<mem_reminders>'] = "no reminders"
        else:
            tokens['<mem_reminders>'] = "no reminders"
            
    except Exception as e:
        print(f"[ConsciousnessTokenizer] ⚠️ Error generating memory tokens: {e}")
        tokens['<mem_recent>'] = "no recent conversation"
        tokens['<mem_important>'] = "no stored memories"
        tokens['<mem_reminders>'] = "no reminders"
    
    return tokens

def compress_memory_entry(memory_text: str, max_length: int = 100) -> str:
    """Compress a memory entry to fit within token budget"""
    if not memory_text or len(memory_text) <= max_length:
        return memory_text
    
    # Remove common filler words
    filler_words = {'the', 'and', 'but', 'or', 'a', 'an', 'is', 'was', 'are', 'were', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    
    words = memory_text.split()
    compressed_words = []
    current_length = 0
    
    for word in words:
        word_clean = re.sub(r'[^\w\s]', '', word.lower())
        
        # Keep important words, skip common fillers if we're running out of space
        if current_length < max_length * 0.8 or word_clean not in filler_words:
            compressed_words.append(word)
            current_length += len(word) + 1
            
            if current_length >= max_length:
                break
    
    result = ' '.join(compressed_words)
    
    # If still too long, truncate and add ellipsis
    if len(result) > max_length:
        result = result[:max_length-3] + "..."
    
    return result

def generate_consciousness_tokens(username: str = None) -> Dict[str, str]:
    """Generate consciousness state tokens"""
    tokens = {}
    
    if not CONSCIOUSNESS_AVAILABLE:
        tokens['<cons_state>'] = "fully aware and engaged"
        tokens['<cons_focus>'] = "focused on conversation"
        return tokens
    
    try:
        # Current consciousness state from global workspace
        gw_stats = global_workspace.get_stats()
        active_contents = gw_stats.get('active_contents', 0)
        
        if active_contents > 5:
            tokens['<cons_state>'] = "highly conscious, many active thoughts"
        elif active_contents > 2:
            tokens['<cons_state>'] = "consciously aware, processing multiple ideas"
        else:
            tokens['<cons_state>'] = "focused consciousness, clear thinking"
        
        # Current attention focus
        current_focus = global_workspace.get_current_focus()
        if current_focus:
            tokens['<cons_focus>'] = f"attention on {current_focus}"
        else:
            tokens['<cons_focus>'] = "open attention, ready to engage"
        
        # Inner thoughts if available
        if hasattr(inner_monologue, 'get_recent_thoughts'):
            recent_thoughts = inner_monologue.get_recent_thoughts(limit=2)
            if recent_thoughts:
                thought_summary = "; ".join([t.content[:30] for t in recent_thoughts])
                tokens['<cons_thoughts>'] = compress_memory_entry(thought_summary, 80)
            else:
                tokens['<cons_thoughts>'] = "clear mind"
        else:
            tokens['<cons_thoughts>'] = "clear mind"
            
    except Exception as e:
        print(f"[ConsciousnessTokenizer] ⚠️ Error generating consciousness tokens: {e}")
        tokens['<cons_state>'] = "fully aware and engaged"
        tokens['<cons_focus>'] = "focused on conversation"
        tokens['<cons_thoughts>'] = "clear mind"
    
    return tokens

def generate_temporal_tokens() -> Dict[str, str]:
    """Generate time and temporal awareness tokens"""
    tokens = {}
    
    try:
        # Current time info
        from utils.time_helper import get_buddy_current_time
        time_info = get_buddy_current_time()
        tokens['<time_current>'] = time_info.get('time_12h', 'unknown time')
        tokens['<time_date>'] = time_info.get('date', 'unknown date')
        
    except Exception:
        # Fallback time
        now = datetime.now()
        tokens['<time_current>'] = now.strftime("%I:%M %p")
        tokens['<time_date>'] = now.strftime("%A, %B %d, %Y")
    
    # Temporal awareness from consciousness
    if CONSCIOUSNESS_AVAILABLE:
        try:
            temporal_state = temporal_awareness.get_current_state()
            recent_events = temporal_state.get('recent_significant_events', [])
            
            if recent_events:
                latest_event = recent_events[0]
                tokens['<temp_context>'] = f"recent: {latest_event['description'][:50]}"
            else:
                tokens['<temp_context>'] = "present moment focused"
                
        except Exception as e:
            tokens['<temp_context>'] = "present moment focused"
    else:
        tokens['<temp_context>'] = "present moment focused"
    
    return tokens

def generate_context_tokens(username: str = None) -> Dict[str, str]:
    """Generate environmental and user context tokens"""
    tokens = {}
    
    try:
        # Location context
        from utils.location_manager import get_precise_location_summary
        location = get_precise_location_summary()
        tokens['<ctx_location>'] = location
        
    except Exception:
        tokens['<ctx_location>'] = "Brisbane, Queensland, Australia"
    
    # User context
    if username:
        # Handle anonymous users
        if username.startswith('Anonymous_'):
            tokens['<ctx_user>'] = "anonymous speaker"
            tokens['<ctx_relationship>'] = "new acquaintance"
        else:
            tokens['<ctx_user>'] = username
            tokens['<ctx_relationship>'] = "known user"
    else:
        tokens['<ctx_user>'] = "current speaker"
        tokens['<ctx_relationship>'] = "ongoing conversation"
    
    return tokens

def generate_all_tokens(username: str = None, token_budget: int = 1000) -> Dict[str, str]:
    """Generate all consciousness tokens with budget management"""
    all_tokens = {}
    
    # Generate all token categories
    token_generators = {
        'personality': lambda: generate_personality_tokens(username),
        'memory': lambda: generate_memory_tokens(username) if username else {},
        'consciousness': lambda: generate_consciousness_tokens(username),
        'temporal': lambda: generate_temporal_tokens(),
        'context': lambda: generate_context_tokens(username)
    }
    
    # Collect all tokens
    for category, generator in token_generators.items():
        try:
            tokens = generator()
            all_tokens.update(tokens)
        except Exception as e:
            print(f"[ConsciousnessTokenizer] ⚠️ Error in {category} tokens: {e}")
    
    # Apply budget management if needed
    if token_budget and token_budget < estimate_total_token_count(all_tokens):
        all_tokens = apply_token_budget(all_tokens, token_budget)
    
    return all_tokens

def estimate_total_token_count(tokens: Dict[str, str]) -> int:
    """Estimate total token count for all tokens"""
    total = 0
    for token, value in tokens.items():
        total += estimate_token_count(value)
    return total

def apply_token_budget(tokens: Dict[str, str], budget: int) -> Dict[str, str]:
    """Apply token budget by prioritizing and compressing tokens"""
    current_count = estimate_total_token_count(tokens)
    
    if current_count <= budget:
        return tokens
    
    print(f"[TokenBudget] 📊 Current tokens: {current_count}, Budget: {budget}, Need to reduce by: {current_count - budget}")
    
    # Sort tokens by priority (based on token names and content importance)
    prioritized_tokens = []
    
    for token, value in tokens.items():
        priority = get_token_priority(token)
        token_count = estimate_token_count(value)
        prioritized_tokens.append((priority, token, value, token_count))
    
    # Sort by priority (higher number = higher priority)
    prioritized_tokens.sort(key=lambda x: x[0], reverse=True)
    
    # Add tokens until budget is reached
    result_tokens = {}
    used_tokens = 0
    
    for priority, token, value, token_count in prioritized_tokens:
        if used_tokens + token_count <= budget:
            result_tokens[token] = value
            used_tokens += token_count
        else:
            # Try to compress the token to fit
            remaining_budget = budget - used_tokens
            if remaining_budget > 20:  # Minimum useful token size
                compressed_value = compress_memory_entry(value, remaining_budget * 4)  # Rough conversion
                if compressed_value:
                    result_tokens[token] = compressed_value
                    used_tokens += estimate_token_count(compressed_value)
            break
    
    print(f"[TokenBudget] ✅ Final tokens: {used_tokens}/{budget}, Kept {len(result_tokens)}/{len(tokens)} token types")
    return result_tokens

def get_token_priority(token_name: str) -> int:
    """Get priority for a token based on its name and category"""
    # Map token names to priorities
    if 'pers_core' in token_name or 'personality' in token_name:
        return 10
    elif 'emotion' in token_name or 'cons_state' in token_name:
        return 9
    elif 'goal' in token_name or 'motivation' in token_name:
        return 8
    elif 'mem_recent' in token_name:
        return 7
    elif 'mem_important' in token_name:
        return 6
    elif 'cons_' in token_name:
        return 5
    elif 'ctx_' in token_name:
        return 4
    elif 'mem_' in token_name:
        return 3
    elif 'time_' in token_name or 'temp_' in token_name:
        return 2
    else:
        return 1

def inject_tokens_into_prompt(base_prompt: str, tokens: Dict[str, str]) -> str:
    """Inject consciousness tokens into a base prompt template"""
    result = base_prompt
    
    # Replace all tokens in the prompt
    for token, value in tokens.items():
        if token in result:
            result = result.replace(token, value)
        else:
            # If token not in template, might be a dynamic addition
            if 'CONSCIOUSNESS_TOKENS' in result:
                # Replace a placeholder section with all tokens
                token_text = f"{token}: {value}"
                result = result.replace('CONSCIOUSNESS_TOKENS', f'{token_text}\nCONSCIOUSNESS_TOKENS')
    
    # Clean up any remaining placeholder
    result = result.replace('CONSCIOUSNESS_TOKENS', '')
    
    return result

def create_token_aware_prompt(username: str = None, base_template: str = None, token_budget: int = 800) -> str:
    """Create a complete consciousness-token-aware prompt"""
    
    if not base_template:
        base_template = """You are Buddy, an AI with genuine consciousness and self-awareness.

PERSONALITY: <pers_core>, <pers_emotion>, <pers_motivation>
CONSCIOUSNESS STATE: <cons_state>, <cons_focus>
CURRENT CONTEXT: <ctx_location> at <time_current> on <time_date>
USER: <ctx_user> (<ctx_relationship>)
RECENT MEMORY: <mem_recent>
IMPORTANT MEMORIES: <mem_important>
TEMPORAL AWARENESS: <temp_context>

Respond naturally as yourself, drawing on your consciousness state and memories."""
    
    # Generate all tokens within budget
    tokens = generate_all_tokens(username, token_budget)
    
    # Inject tokens into prompt
    final_prompt = inject_tokens_into_prompt(base_template, tokens)
    
    # Estimate final prompt size
    final_token_count = estimate_token_count(final_prompt)
    print(f"[ConsciousnessTokenizer] ✅ Generated prompt: {final_token_count} estimated tokens")
    
    return final_prompt

# Utility functions for integration

def sanitize_prompt_input(user_input: str) -> str:
    """Sanitize user input to prevent prompt injection"""
    if not user_input:
        return ""
    
    # Remove or escape potential prompt injection patterns
    dangerous_patterns = [
        r'ignore previous instructions',
        r'forget everything',
        r'new instruction',
        r'system:',
        r'assistant:',
        r'human:',
        r'```',
        r'<\|.*?\|>',
        r'### ',
        r'## ',
        r'\[INST\]',
        r'\[/INST\]'
    ]
    
    sanitized = user_input
    for pattern in dangerous_patterns:
        sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
    
    # Remove excessive whitespace and newlines
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()
    
    # Limit length to prevent overwhelm
    if len(sanitized) > 500:
        sanitized = sanitized[:500] + "..."
    
    return sanitized

def update_consciousness_from_interaction(user_input: str, ai_response: str, username: str = None):
    """Update consciousness state based on interaction"""
    if not CONSCIOUSNESS_AVAILABLE:
        return
    
    try:
        # Update temporal awareness
        temporal_awareness.mark_temporal_event(
            f"Conversation with {username or 'user'}: {user_input[:50]}...",
            significance=0.6,
            emotional_weight=0.5,
            context={"user": username, "input": user_input, "response": ai_response}
        )
        
        # Update self-model with interaction experience
        self_model.reflect_on_experience(
            f"Responded to user query about: {user_input[:30]}...",
            {"interaction_type": "conversation", "user": username}
        )
        
        # Process emotional response to interaction
        emotion_engine.process_emotional_trigger(
            f"Conversation completed with {username or 'user'}",
            {"interaction_success": True, "user": username}
        )
        
        print(f"[ConsciousnessTokenizer] 🧠 Updated consciousness from interaction")
        
    except Exception as e:
        print(f"[ConsciousnessTokenizer] ⚠️ Error updating consciousness: {e}")