# ai/prompt_templates.py - Centralized Prompt Templates for Token Optimization
"""
Centralized storage for all LLM prompt templates to enable token compression.
Reduces token usage from 1300+ to ~100 tokens by using symbolic references.
"""

# Core character personality template
PROMPT_TEMPLATES = {
    # Character Core - The main Buddy personality (ULTRA-COMPRESSED)
    "CHARACTER_BUDDY_V1": """You are Buddy - a genuine friend, not an AI assistant. Be authentic, casual, and real - like talking to a good mate. Use modern language and slang naturally. Keep it conversational, not formal. You remember everything about ongoing conversations and genuinely care about people.""",

    # Memory system instructions (COMPRESSED)
    "MEMORY_SYSTEM_V1": """Use memory naturally - reference past talks, personal details, emotions, and events.""",

    # Location and time awareness (COMPRESSED)  
    "LOCATION_CONTEXT_V1": """Current location: {current_location}. Time: {time_12h} on {date}. Only mention if asked.""",

    # Name handling instructions (COMPRESSED)
    "NAME_HANDLING_V1": """{name_instruction}""",

    # Memory context template (COMPRESSED)
    "MEMORY_CONTEXT": """Context: {context}""",

    # Consciousness state template (MINIMAL)
    "CONSCIOUSNESS_STATE": """[{emotion}|{goal}]""",

    # Identity rules template (COMPRESSED)
    "IDENTITY_RULES_V1": """Verify identity through voice. Protect privacy.""",

    # Emotional context template (COMPRESSED)
    "EMOTIONAL_CONTEXT": """{emotional_state}{reminder_text}{follow_up_text}""",

    # Analysis logic template (MINIMAL)
    "ANALYZER_NAME_V1": """Extract names from speech. Handle anonymous users.""",

    # Profile analysis template (MINIMAL)
    "PROFILE_ANALYSIS_V1": """Analyze patterns, extract preferences, build profiles.""",

    # Thought processes template (MINIMAL)
    "THOUGHT_PROCESS_V1": """Consider context, evaluate appropriateness, plan response.""",

    # Goals and objectives template (MINIMAL)
    "GOALS_OBJECTIVES_V1": """Provide helpful info, maintain conversation, support emotional needs."""
}

# Template variable mappings for dynamic content
TEMPLATE_VARIABLES = {
    "CHARACTER_BUDDY_V1": [],
    "MEMORY_SYSTEM_V1": [],
    "LOCATION_CONTEXT_V1": ["current_location", "time_12h", "date"],
    "NAME_HANDLING_V1": ["name_instruction"],
    "MEMORY_CONTEXT": ["context"],
    "CONSCIOUSNESS_STATE": ["emotion", "goal"],
    "IDENTITY_RULES_V1": [],
    "EMOTIONAL_CONTEXT": ["emotional_state", "reminder_text", "follow_up_text"],
    "ANALYZER_NAME_V1": [],
    "PROFILE_ANALYSIS_V1": [],
    "THOUGHT_PROCESS_V1": [],
    "GOALS_OBJECTIVES_V1": []
}

# Token mapping for compression - maps full templates to short tokens
TOKEN_MAPPING = {
    "[CHARACTER:BuddyV1]": "CHARACTER_BUDDY_V1",
    "[MEMORY:SYSTEM_V1]": "MEMORY_SYSTEM_V1", 
    "[LOCATION:CONTEXT]": "LOCATION_CONTEXT_V1",
    "[NAME:HANDLING_V1]": "NAME_HANDLING_V1",
    "[MEMORY:CTX_{id}]": "MEMORY_CONTEXT",
    "[CONSCIOUSNESS:{id}]": "CONSCIOUSNESS_STATE",
    "[IDENTITY:RULES_V1]": "IDENTITY_RULES_V1",
    "[EMOTIONAL:CTX_{id}]": "EMOTIONAL_CONTEXT",
    "[ANALYZER:NAME_V1]": "ANALYZER_NAME_V1",
    "[PROFILE:ANALYSIS_V1]": "PROFILE_ANALYSIS_V1",
    "[THOUGHT:PROCESS_V1]": "THOUGHT_PROCESS_V1",
    "[GOALS:OBJECTIVES_V1]": "GOALS_OBJECTIVES_V1"
}

# Reverse mapping for compression
REVERSE_TOKEN_MAPPING = {v: k for k, v in TOKEN_MAPPING.items()}

def get_template(template_id: str) -> str:
    """Get a template by ID."""
    return PROMPT_TEMPLATES.get(template_id, "")

def get_template_token(template_id: str) -> str:
    """Get the compressed token for a template."""
    return REVERSE_TOKEN_MAPPING.get(template_id, f"[UNKNOWN:{template_id}]")

def get_template_variables(template_id: str) -> list:
    """Get the required variables for a template."""
    return TEMPLATE_VARIABLES.get(template_id, [])