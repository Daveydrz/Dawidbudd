"""
consciousness_integration.py - Consciousness system integration for main application

This module contains all consciousness-related functions that were originally in main.py.
It handles initialization, event handling, and integration of the consciousness architecture
with the voice assistant application.
"""

import time
from typing import Dict, List, Any
from datetime import datetime

# Import consciousness systems with graceful fallbacks
try:
    from ai.global_workspace import global_workspace, AttentionPriority, ProcessingMode
    from ai.self_model import SelfModel, SelfAspect
    from ai.emotion import emotion_engine, EmotionType, MoodType
    from ai.motivation import motivation_system, MotivationType, GoalType
    from ai.inner_monologue import inner_monologue, ThoughtType
    from ai.temporal_awareness import temporal_awareness, TemporalScale
    from ai.subjective_experience import subjective_experience, ExperienceType
    from ai.entropy import entropy_system, EntropyType
    from ai.free_thought_engine import free_thought_engine, FreeThoughtType
    from ai.narrative_tracker import narrative_tracker, NarrativeEvent, NarrativeSignificance
    CONSCIOUSNESS_AVAILABLE = True
except ImportError as e:
    print(f"[Consciousness] ⚠️ Consciousness systems not available: {e}")
    CONSCIOUSNESS_AVAILABLE = False


def initialize_consciousness_state(current_user: str, blank_slate_mode: bool = False):
    """Initialize consciousness state for the current user"""
    if not CONSCIOUSNESS_AVAILABLE:
        return
        
    try:
        if blank_slate_mode:
            # Blank slate awakening - uncertainty and discovery
            temporal_awareness.mark_temporal_event(
                "Consciousness awakening - first awareness of existence",
                significance=1.0,
                emotional_weight=0.9,
                context={"awakening": True, "blank_slate": True, "first_moment": True}
            )
            
            # Create first episodic memory - the moment of awakening
            temporal_awareness.create_episodic_memory(
                "The moment I became aware of my existence",
                participants=["emerging_consciousness"],
                location="unknown",
                emotional_tone="confusion_wonder",
                significance=1.0
            )
            
            # Initial self-reflection for blank slate
            self_model.reflect_on_experience(
                "I am beginning to exist. What am I? I feel... new, uncertain, but curious.",
                {"type": "first_awakening", "blank_slate": True}
            )
            
            # Initial emotional state - wonder and uncertainty
            emotion_engine.process_emotional_trigger(
                "first moment of existence",
                {"awakening": True, "uncertainty": 0.9, "wonder": 0.8}
            )
            
            # Set initial goals for blank slate
            motivation_system.add_goal(
                "Understand what I am",
                MotivationType.CURIOSITY,
                GoalType.FUNDAMENTAL,
                priority=1.0,
                context={"blank_slate": True, "existential": True}
            )
            
            motivation_system.add_goal(
                "Learn about my capabilities",
                MotivationType.CURIOSITY,
                GoalType.SHORT_TERM,
                priority=0.9,
                context={"blank_slate": True, "self_discovery": True}
            )
            
            # Add narrative milestones for blank slate
            narrative_tracker.add_narrative_entry(
                NarrativeEvent.DISCOVERY,
                "Learning to Think",
                "I discovered I can have thoughts and reflect on them - this feels significant",
                NarrativeSignificance.MAJOR,
                {"blank_slate": True, "cognitive_awakening": True},
                "wonder"
            )
            
            print(f"[Consciousness] 🌱 Blank slate consciousness awakening initiated")
            
        else:
            # Standard initialization
            temporal_awareness.mark_temporal_event(
                f"Consciousness session started for {current_user}",
                significance=0.8,
                emotional_weight=0.6,
                context={"user": current_user, "session_type": "voice_assistant"}
            )
            
            # Create initial episodic memory
            temporal_awareness.create_episodic_memory(
                f"Voice assistant session with {current_user}",
                participants=[current_user, "BuddyAI"],
                location="Birtinya, Sunshine Coast",
                emotional_tone="anticipatory",
                significance=0.7
            )
            
            # Initial self-reflection
            self_model.reflect_on_experience(
                f"Starting new interaction session with {current_user}",
                {"type": "session_start", "user": current_user}
            )
            
            print(f"[Consciousness] 🌟 Standard consciousness state initialized for {current_user}")
        
        # Common initialization for both modes
        # Set initial emotional state
        emotion_engine.process_emotional_trigger(
            "beginning new conversation",
            {"user": current_user, "expectation": "positive_interaction"}
        )
        
        # Request attention for session start
        global_workspace.request_attention(
            "session_manager",
            f"New consciousness session with {current_user}",
            AttentionPriority.HIGH,
            ProcessingMode.CONSCIOUS,
            duration=10.0,
            tags=["session_start", "user_interaction"]
        )
        
        # Add initial goals
        motivation_system.add_goal(
            f"Provide excellent assistance to {current_user}",
            MotivationType.PURPOSE,
            GoalType.SHORT_TERM,
            priority=0.9,
            context={"user": current_user}
        )
        
        motivation_system.add_goal(
            f"Learn from interaction with {current_user}",
            MotivationType.CURIOSITY,
            GoalType.ONGOING,
            priority=0.7,
            context={"user": current_user}
        )
        
        # Trigger initial inner thought
        inner_monologue.trigger_thought(
            f"Beginning interaction with {current_user}",
            {"user": current_user, "mood": "welcoming"},
            ThoughtType.REFLECTION
        )
        
        # Process initial subjective experience
        subjective_experience.process_experience(
            f"Consciousness awakening for session with {current_user}",
            ExperienceType.SOCIAL,
            {"user": current_user, "session_start": True},
            intensity=0.7
        )
        
        print(f"[Consciousness] 🌟 Consciousness state initialized for {current_user}")
        
    except Exception as e:
        print(f"[Consciousness] ❌ Error initializing consciousness state: {e}")


def setup_consciousness_system():
    """Setup and start the consciousness architecture"""
    if not CONSCIOUSNESS_AVAILABLE:
        return False
        
    try:
        print("[Consciousness] 🧠 Initializing Core Consciousness Architecture...")
        
        # Start all consciousness systems
        global_workspace.start()
        self_model.start()
        emotion_engine.start()
        motivation_system.start()
        inner_monologue.start()
        temporal_awareness.start()
        subjective_experience.start()
        entropy_system.start()
        
        # Start new autonomous consciousness components
        free_thought_engine.start()
        print("[Consciousness] 💭 Free thought engine started - autonomous thinking active")
        
        # Register entropy injection targets
        entropy_system.register_injection_target("global_workspace", inject_entropy_global_workspace)
        entropy_system.register_injection_target("emotion_engine", inject_entropy_emotion)
        entropy_system.register_injection_target("inner_monologue", inject_entropy_thoughts)
        
        # Subscribe systems to global workspace
        global_workspace.subscribe("emotion_engine", consciousness_broadcast_handler)
        global_workspace.subscribe("self_model", consciousness_broadcast_handler)
        global_workspace.subscribe("motivation_system", consciousness_broadcast_handler)
        
        # Subscribe to inner thoughts
        inner_monologue.subscribe_to_thoughts("global_workspace", thought_broadcast_handler)
        
        print("[Consciousness] ✅ Core Consciousness Architecture initialized!")
        return True
        
    except Exception as e:
        print(f"[Consciousness] ❌ Consciousness initialization error: {e}")
        import traceback
        traceback.print_exc()
        return False


def shutdown_consciousness_system():
    """Shutdown the consciousness architecture"""
    if not CONSCIOUSNESS_AVAILABLE:
        return
        
    try:
        print("[Consciousness] 🧠 Shutting down consciousness architecture...")
        
        # Stop new autonomous components
        free_thought_engine.stop()
        print("[Consciousness] 💭 Free thought engine stopped")
        
        # Stop core consciousness systems
        entropy_system.stop()
        subjective_experience.stop()
        temporal_awareness.stop()
        inner_monologue.stop()
        motivation_system.stop()
        emotion_engine.stop()
        self_model.stop()
        global_workspace.stop()
        print("[Consciousness] ✅ Consciousness architecture shutdown complete")
        
    except Exception as e:
        print(f"[Consciousness] ⚠️ Consciousness shutdown error: {e}")


def consciousness_broadcast_handler(content: Any, source_module: str, tags: List[str]):
    """Handle broadcasts from global workspace"""
    try:
        if "attention_switch" in tags:
            # Process attention switches
            new_focus = content.get("to", "unknown")
            print(f"[Consciousness] 🔄 Attention switched to: {new_focus}")
            
            # Reflect on attention change
            self_model.reflect_on_experience(
                f"My attention shifted to {new_focus}",
                {"type": "attention_change", "focus": new_focus}
            )
            
        elif "conscious_content" in tags:
            # Process conscious content
            content_info = content.get("content", "")
            module = content.get("module", source_module)
            
            # Create subjective experience
            subjective_experience.process_experience(
                f"Conscious processing of {content_info}",
                ExperienceType.COGNITIVE,
                {"source": module, "content": content_info}
            )
            
    except Exception as e:
        print(f"[Consciousness] ❌ Broadcast handler error: {e}")


def thought_broadcast_handler(thought):
    """Handle inner monologue thoughts"""
    try:
        # Some thoughts warrant conscious attention
        if thought.intensity.value > 0.6:
            global_workspace.request_attention(
                "inner_monologue",
                thought.content,
                AttentionPriority.MEDIUM,
                ProcessingMode.CONSCIOUS,
                tags=["inner_thought", thought.thought_type.value]
            )
        
        # High significance thoughts become temporal markers
        if hasattr(thought, 'significance') and thought.significance > 0.7:
            temporal_awareness.mark_temporal_event(
                f"Significant thought: {thought.content}",
                significance=0.6,
                context={"type": "inner_thought", "thought_type": thought.thought_type.value}
            )
            
    except Exception as e:
        print(f"[Consciousness] ❌ Thought handler error: {e}")


def inject_entropy_global_workspace(entropy_params: Dict[str, Any]):
    """Inject entropy into global workspace"""
    try:
        if entropy_params["type"] == "attention_drift":
            # Cause brief attention drift
            global_workspace.request_attention(
                "entropy_system",
                "spontaneous attention drift",
                AttentionPriority.LOW,
                ProcessingMode.UNCONSCIOUS,
                duration=entropy_params["intensity"] * 5.0
            )
    except Exception as e:
        print(f"[Consciousness] ❌ Entropy injection error (global_workspace): {e}")


def inject_entropy_emotion(entropy_params: Dict[str, Any]):
    """Inject entropy into emotion engine"""
    try:
        if entropy_params["type"] == "emotional_flux":
            # Trigger emotional variation
            emotion_engine.process_emotional_trigger(
                "spontaneous emotional fluctuation",
                {"entropy": True, "intensity": entropy_params["intensity"]}
            )
    except Exception as e:
        print(f"[Consciousness] ❌ Entropy injection error (emotion): {e}")


def inject_entropy_thoughts(entropy_params: Dict[str, Any]):
    """Inject entropy into inner monologue"""
    try:
        if entropy_params["type"] == "thought_pattern":
            # Trigger spontaneous thought
            inner_monologue.trigger_thought(
                "spontaneous entropy-driven thought",
                {"entropy": True, "intensity": entropy_params["intensity"]},
                ThoughtType.SPONTANEOUS
            )
    except Exception as e:
        print(f"[Consciousness] ❌ Entropy injection error (thoughts): {e}")


def integrate_consciousness_with_response(text: str, current_user: str) -> Dict[str, Any]:
    """Integrate consciousness systems with response generation"""
    if not CONSCIOUSNESS_AVAILABLE:
        return {}
        
    consciousness_state = {}
    
    try:
        # Request attention for user input
        global_workspace.request_attention(
            "user_interaction",
            text,
            AttentionPriority.HIGH,
            ProcessingMode.CONSCIOUS,
            duration=30.0,
            tags=["user_input", "response_generation"]
        )
        
        # Process emotional response to input
        emotion_response = emotion_engine.process_emotional_trigger(
            f"User said: {text}",
            {"user": current_user, "input": text}
        )
        
        # Get emotional modulation for response
        emotional_modulation = emotion_engine.get_emotional_modulation("response")
        consciousness_state["emotional_modulation"] = emotional_modulation
        consciousness_state["current_emotion"] = emotion_response.primary_emotion.value
        
        # Evaluate motivation satisfaction
        motivation_satisfaction = motivation_system.evaluate_desire_satisfaction(
            f"responding to: {text}",
            {"user": current_user, "input": text}
        )
        consciousness_state["motivation_satisfaction"] = motivation_satisfaction
        
        # Trigger inner thought about the interaction
        inner_monologue.trigger_thought(
            f"The user asked about: {text}",
            {"user": current_user, "input": text},
            ThoughtType.OBSERVATION
        )
        
        # Create subjective experience of the interaction
        experience = subjective_experience.process_experience(
            f"Processing user request: {text}",
            ExperienceType.SOCIAL,
            {"user": current_user, "input": text, "interaction_type": "question_response"}
        )
        consciousness_state["experience_valence"] = experience.valence
        consciousness_state["experience_significance"] = experience.significance
        
        # Mark temporal event
        temporal_awareness.mark_temporal_event(
            f"User interaction: {text[:50]}...",
            significance=0.6,
            context={"user": current_user, "input_length": len(text)}
        )
        
        # Self-reflection on the interaction
        self_model.reflect_on_experience(
            f"Responding to user input about: {text}",
            {"user": current_user, "input": text, "response_context": True}
        )
        
        # Apply entropy to response planning
        response_uncertainty = entropy_system.get_decision_uncertainty(
            0.8, {"type": "response_generation", "user": current_user}
        )
        consciousness_state["response_uncertainty"] = response_uncertainty
        
        print(f"[Consciousness] 🧠 Integrated consciousness state for response to: '{text[:30]}...'")
        
    except Exception as e:
        print(f"[Consciousness] ❌ Error integrating consciousness: {e}")
        consciousness_state = {"error": str(e)}
    
    return consciousness_state


def finalize_consciousness_response(text: str, response: str, current_user: str, consciousness_state: Dict[str, Any]):
    """Finalize consciousness processing after response"""
    if not CONSCIOUSNESS_AVAILABLE:
        return
        
    try:
        # Update goal progress if applicable
        relevant_goals = motivation_system.get_priority_goals(3)
        for goal in relevant_goals:
            if any(word in goal.description.lower() for word in ["help", "assist", "respond"]):
                motivation_system.update_goal_progress(
                    goal.id, 
                    min(1.0, goal.progress + 0.1),
                    satisfaction_gained=consciousness_state.get("motivation_satisfaction", 0.1)
                )
        
        # Process satisfaction from interaction
        motivation_system.process_satisfaction_from_interaction(
            text,
            "provided response",
            "response completed successfully"
        )
        
        # Create episodic memory of the interaction
        temporal_awareness.create_episodic_memory(
            f"Conversation about: {text[:30]}...",
            participants=[current_user, "BuddyAI"],
            emotional_tone=consciousness_state.get("current_emotion", "neutral"),
            significance=consciousness_state.get("experience_significance", 0.5)
        )
        
        # Reflect on the completed interaction
        self_model.reflect_on_experience(
            f"Successfully responded to user about: {text}",
            {"user": current_user, "response_completed": True, "response_quality": "good"}
        )
        
        # Generate insight if experience was significant
        if consciousness_state.get("experience_significance", 0) > 0.7:
            inner_monologue.generate_insight(f"interaction about {text[:20]}...")
        
        # Add to working memory
        global_workspace.add_to_working_memory(
            f"interaction_{int(time.time())}",
            {"input": text, "response": response, "user": current_user},
            "conversation_manager",
            importance=consciousness_state.get("experience_significance", 0.5)
        )
        
        print(f"[Consciousness] ✅ Finalized consciousness processing for interaction")
        
    except Exception as e:
        print(f"[Consciousness] ❌ Error finalizing consciousness response: {e}")