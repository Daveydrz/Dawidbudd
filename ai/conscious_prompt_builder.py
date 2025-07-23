"""
Conscious Prompt Builder - Inject beliefs, emotions, thoughts, goals into LLM prompt
Advanced prompt construction with full consciousness integration
"""

import json
import time
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass

@dataclass
class ConsciousnessSnapshot:
    """Snapshot of current consciousness state"""
    timestamp: str
    dominant_emotion: str
    emotional_valence: float
    cognitive_clarity: float
    active_beliefs: List[str]
    current_goals: List[str]
    inner_thoughts: List[str]
    active_qualia: List[str]
    value_priorities: List[str]
    attention_focus: str
    processing_mode: str

class ConsciousPromptBuilder:
    """Build consciousness-integrated prompts for LLM"""
    
    def __init__(self):
        self.consciousness_tokens = {}
        self.prompt_templates = self._initialize_templates()
        self.integration_modes = ['minimal', 'standard', 'comprehensive', 'debug']
        self.current_mode = 'standard'
        self.token_budget = 1000  # Maximum tokens for consciousness context
        self.last_consciousness_snapshot = None
    
    def _initialize_templates(self) -> Dict[str, str]:
        """Initialize prompt templates for different consciousness levels"""
        return {
            'minimal': """<consciousness>
Emotional state: {emotion} | Focus: {focus} | Mode: {mode}
</consciousness>

{user_input}""",
            
            'standard': """<consciousness>
Emotional state: {emotion} (valence: {valence:.2f}, clarity: {clarity:.2f})
Current focus: {focus}
Processing mode: {mode}
Active beliefs: {beliefs}
Primary goals: {goals}
</consciousness>

{user_input}""",
            
            'comprehensive': """<consciousness>
Emotional state: {emotion} (valence: {valence:.2f}, clarity: {clarity:.2f})
Current focus: {focus}
Processing mode: {mode}
Active beliefs: {beliefs}
Primary goals: {goals}
Inner thoughts: {thoughts}
Qualia experiences: {qualia}
Value priorities: {values}
</consciousness>

{context}

{user_input}""",
            
            'debug': """<consciousness_debug>
Timestamp: {timestamp}
Emotional state: {emotion} (valence: {valence:.2f}, clarity: {clarity:.2f})
Current focus: {focus}
Processing mode: {mode}
Active beliefs: {beliefs}
Primary goals: {goals}
Inner thoughts: {thoughts}
Qualia experiences: {qualia}
Value priorities: {values}
Memory context: {memory}
Personality state: {personality}
</consciousness_debug>

{context}

{user_input}"""
        }
    
    def capture_consciousness_snapshot(self, user_id: str) -> ConsciousnessSnapshot:
        """Capture current consciousness state"""
        try:
            # Get emotional state
            emotion_state = self._get_emotional_state()
            
            # Get cognitive state
            cognitive_state = self._get_cognitive_state()
            
            # Get beliefs
            active_beliefs = self._get_active_beliefs(user_id)
            
            # Get goals
            current_goals = self._get_current_goals()
            
            # Get inner thoughts
            inner_thoughts = self._get_inner_thoughts()
            
            # Get qualia
            active_qualia = self._get_active_qualia()
            
            # Get values
            value_priorities = self._get_value_priorities()
            
            # Get attention state
            attention_focus = self._get_attention_focus()
            
            # Get processing mode
            processing_mode = self._get_processing_mode()
            
            snapshot = ConsciousnessSnapshot(
                timestamp=datetime.now().isoformat(),
                dominant_emotion=emotion_state.get('primary_emotion', 'neutral'),
                emotional_valence=emotion_state.get('valence', 0.0),
                cognitive_clarity=cognitive_state.get('clarity', 0.5),
                active_beliefs=active_beliefs,
                current_goals=current_goals,
                inner_thoughts=inner_thoughts,
                active_qualia=active_qualia,
                value_priorities=value_priorities,
                attention_focus=attention_focus,
                processing_mode=processing_mode
            )
            
            self.last_consciousness_snapshot = snapshot
            return snapshot
            
        except Exception as e:
            print(f"[ConsciousPromptBuilder] ❌ Error capturing consciousness: {e}")
            return self._create_fallback_snapshot()
    
    def _get_emotional_state(self) -> Dict[str, Any]:
        """Get current emotional state"""
        try:
            from ai.emotion import emotion_engine
            return emotion_engine.get_current_state()
        except Exception as e:
            print(f"[ConsciousPromptBuilder] ⚠️ Emotional state fallback: {e}")
            return {'primary_emotion': 'neutral', 'valence': 0.0, 'intensity': 0.5}
    
    def _get_cognitive_state(self) -> Dict[str, Any]:
        """Get current cognitive state"""
        try:
            from ai.global_workspace import global_workspace
            stats = global_workspace.get_stats()
            return {
                'clarity': stats.get('processing_clarity', 0.5),
                'focus_strength': stats.get('attention_strength', 0.5),
                'processing_load': stats.get('processing_load', 0.5)
            }
        except Exception as e:
            print(f"[ConsciousPromptBuilder] ⚠️ Cognitive state fallback: {e}")
            return {'clarity': 0.5, 'focus_strength': 0.5, 'processing_load': 0.5}
    
    def _get_active_beliefs(self, user_id: str) -> List[str]:
        """Get currently active beliefs"""
        try:
            from ai.belief_analyzer import get_active_belief_contradictions
            beliefs = get_active_belief_contradictions(user_id)
            return [b.get('content', '')[:50] + '...' for b in beliefs[:3]]
        except Exception as e:
            print(f"[ConsciousPromptBuilder] ⚠️ Beliefs fallback: {e}")
            return ['No active beliefs']
    
    def _get_current_goals(self) -> List[str]:
        """Get current goals"""
        try:
            from ai.motivation import motivation_system
            goals = motivation_system.get_priority_goals(3)
            return [g.description[:50] + '...' for g in goals]
        except Exception as e:
            print(f"[ConsciousPromptBuilder] ⚠️ Goals fallback: {e}")
            return ['Help the user effectively']
    
    def _get_inner_thoughts(self) -> List[str]:
        """Get recent inner thoughts"""
        try:
            from ai.inner_monologue import inner_monologue
            thoughts = inner_monologue.get_recent_thoughts(3)
            return [t.content[:50] + '...' for t in thoughts]
        except Exception as e:
            print(f"[ConsciousPromptBuilder] ⚠️ Thoughts fallback: {e}")
            return ['Focusing on user request']
    
    def _get_active_qualia(self) -> List[str]:
        """Get active qualia experiences"""
        try:
            from ai.belief_qualia_linking import get_qualia_tokens_for_prompt
            return get_qualia_tokens_for_prompt(3)
        except Exception as e:
            print(f"[ConsciousPromptBuilder] ⚠️ Qualia fallback: {e}")
            return ['<qualia1:cognitive:moderate:0.5>']
    
    def _get_value_priorities(self) -> List[str]:
        """Get current value priorities"""
        try:
            from ai.value_system import get_current_value_priorities
            priorities = get_current_value_priorities()
            return [f"{name}:{weight:.2f}" for name, weight in priorities[:3]]
        except Exception as e:
            print(f"[ConsciousPromptBuilder] ⚠️ Values fallback: {e}")
            return ['helpfulness:0.9', 'honesty:0.9', 'empathy:0.8']
    
    def _get_attention_focus(self) -> str:
        """Get current attention focus"""
        try:
            from ai.global_workspace import global_workspace
            focus = global_workspace.get_current_focus()
            return focus.get('focus', 'user_interaction')
        except Exception as e:
            print(f"[ConsciousPromptBuilder] ⚠️ Attention fallback: {e}")
            return 'user_interaction'
    
    def _get_processing_mode(self) -> str:
        """Get current processing mode"""
        try:
            from ai.global_workspace import global_workspace
            mode = global_workspace.get_processing_mode()
            return mode.value if hasattr(mode, 'value') else str(mode)
        except Exception as e:
            print(f"[ConsciousPromptBuilder] ⚠️ Processing mode fallback: {e}")
            return 'conscious'
    
    def _create_fallback_snapshot(self) -> ConsciousnessSnapshot:
        """Create fallback consciousness snapshot"""
        return ConsciousnessSnapshot(
            timestamp=datetime.now().isoformat(),
            dominant_emotion='neutral',
            emotional_valence=0.0,
            cognitive_clarity=0.5,
            active_beliefs=['Processing user request'],
            current_goals=['Help the user effectively'],
            inner_thoughts=['Focusing on user request'],
            active_qualia=['<qualia1:cognitive:moderate:0.5>'],
            value_priorities=['helpfulness:0.9', 'honesty:0.9'],
            attention_focus='user_interaction',
            processing_mode='conscious'
        )
    
    def build_conscious_prompt(self, 
                             user_input: str, 
                             user_id: str,
                             context: Optional[str] = None,
                             mode: Optional[str] = None) -> str:
        """Build a consciousness-integrated prompt"""
        try:
            # Capture current consciousness state
            snapshot = self.capture_consciousness_snapshot(user_id)
            
            # Select integration mode
            integration_mode = mode or self.current_mode
            template = self.prompt_templates.get(integration_mode, self.prompt_templates['standard'])
            
            # Prepare consciousness data
            consciousness_data = self._prepare_consciousness_data(snapshot, user_id)
            
            # Build prompt
            prompt = template.format(
                emotion=consciousness_data['emotion'],
                valence=consciousness_data['valence'],
                clarity=consciousness_data['clarity'],
                focus=consciousness_data['focus'],
                mode=consciousness_data['mode'],
                beliefs=consciousness_data['beliefs'],
                goals=consciousness_data['goals'],
                thoughts=consciousness_data['thoughts'],
                qualia=consciousness_data['qualia'],
                values=consciousness_data['values'],
                memory=consciousness_data.get('memory', 'N/A'),
                personality=consciousness_data.get('personality', 'N/A'),
                timestamp=consciousness_data['timestamp'],
                context=context or '',
                user_input=user_input
            )
            
            # Apply token budget constraints
            prompt = self._apply_token_budget(prompt)
            
            print(f"[ConsciousPromptBuilder] 🧠 Built {integration_mode} prompt: {len(prompt)} chars")
            return prompt
            
        except Exception as e:
            print(f"[ConsciousPromptBuilder] ❌ Error building prompt: {e}")
            return f"<consciousness>Error in consciousness integration</consciousness>\n\n{user_input}"
    
    def _prepare_consciousness_data(self, snapshot: ConsciousnessSnapshot, user_id: str) -> Dict[str, Any]:
        """Prepare consciousness data for prompt insertion"""
        return {
            'timestamp': snapshot.timestamp,
            'emotion': snapshot.dominant_emotion,
            'valence': snapshot.emotional_valence,
            'clarity': snapshot.cognitive_clarity,
            'focus': snapshot.attention_focus,
            'mode': snapshot.processing_mode,
            'beliefs': ' | '.join(snapshot.active_beliefs) if snapshot.active_beliefs else 'None',
            'goals': ' | '.join(snapshot.current_goals) if snapshot.current_goals else 'None',
            'thoughts': ' | '.join(snapshot.inner_thoughts) if snapshot.inner_thoughts else 'None',
            'qualia': ' | '.join(snapshot.active_qualia) if snapshot.active_qualia else 'None',
            'values': ' | '.join(snapshot.value_priorities) if snapshot.value_priorities else 'None',
            'memory': self._get_memory_context(user_id),
            'personality': self._get_personality_context(user_id)
        }
    
    def _get_memory_context(self, user_id: str) -> str:
        """Get memory context for prompt"""
        try:
            from ai.memory import get_conversation_context
            context = get_conversation_context(user_id, 3)
            return context[:100] + '...' if len(context) > 100 else context
        except Exception as e:
            print(f"[ConsciousPromptBuilder] ⚠️ Memory context fallback: {e}")
            return 'Memory context unavailable'
    
    def _get_personality_context(self, user_id: str) -> str:
        """Get personality context for prompt"""
        try:
            from ai.personality_state import get_personality_summary_for_user
            personality = get_personality_summary_for_user(user_id)
            return personality[:100] + '...' if len(personality) > 100 else personality
        except Exception as e:
            print(f"[ConsciousPromptBuilder] ⚠️ Personality context fallback: {e}")
            return 'Personality context unavailable'
    
    def _apply_token_budget(self, prompt: str) -> str:
        """Apply token budget constraints to prompt"""
        # Simple token estimation (roughly 4 chars per token)
        estimated_tokens = len(prompt) // 4
        
        if estimated_tokens <= self.token_budget:
            return prompt
        
        # Truncate if over budget
        max_chars = self.token_budget * 4
        truncated = prompt[:max_chars]
        
        # Find last complete line
        last_newline = truncated.rfind('\n')
        if last_newline > 0:
            truncated = truncated[:last_newline]
        
        truncated += "\n<truncated due to token budget>"
        
        print(f"[ConsciousPromptBuilder] ✂️ Truncated prompt: {len(prompt)} → {len(truncated)} chars")
        return truncated
    
    def build_consciousness_summary(self, user_id: str) -> str:
        """Build a summary of current consciousness state"""
        try:
            snapshot = self.capture_consciousness_snapshot(user_id)
            
            summary = f"""Consciousness State Summary:
• Emotion: {snapshot.dominant_emotion} (valence: {snapshot.emotional_valence:.2f})
• Clarity: {snapshot.cognitive_clarity:.2f}
• Focus: {snapshot.attention_focus}
• Mode: {snapshot.processing_mode}
• Active Beliefs: {len(snapshot.active_beliefs)}
• Current Goals: {len(snapshot.current_goals)}
• Inner Thoughts: {len(snapshot.inner_thoughts)}
• Active Qualia: {len(snapshot.active_qualia)}
• Value Priorities: {len(snapshot.value_priorities)}
• Timestamp: {snapshot.timestamp}"""
            
            return summary
            
        except Exception as e:
            print(f"[ConsciousPromptBuilder] ❌ Error building summary: {e}")
            return "Consciousness summary unavailable"
    
    def set_integration_mode(self, mode: str):
        """Set consciousness integration mode"""
        if mode in self.integration_modes:
            self.current_mode = mode
            print(f"[ConsciousPromptBuilder] 🎛️ Integration mode set to: {mode}")
        else:
            print(f"[ConsciousPromptBuilder] ⚠️ Invalid mode: {mode}")
    
    def set_token_budget(self, budget: int):
        """Set token budget for consciousness context"""
        self.token_budget = max(100, min(2000, budget))
        print(f"[ConsciousPromptBuilder] 💰 Token budget set to: {self.token_budget}")
    
    def get_prompt_templates(self) -> Dict[str, str]:
        """Get available prompt templates"""
        return self.prompt_templates
    
    def add_custom_template(self, name: str, template: str):
        """Add a custom prompt template"""
        self.prompt_templates[name] = template
        print(f"[ConsciousPromptBuilder] 📝 Added custom template: {name}")
    
    def get_consciousness_tokens(self, user_id: str) -> Dict[str, str]:
        """Get consciousness tokens for external use"""
        try:
            snapshot = self.capture_consciousness_snapshot(user_id)
            
            return {
                'emotion_token': f"<emotion:{snapshot.dominant_emotion}:{snapshot.emotional_valence:.2f}>",
                'clarity_token': f"<clarity:{snapshot.cognitive_clarity:.2f}>",
                'focus_token': f"<focus:{snapshot.attention_focus}>",
                'mode_token': f"<mode:{snapshot.processing_mode}>",
                'beliefs_token': f"<beliefs:{len(snapshot.active_beliefs)}>",
                'goals_token': f"<goals:{len(snapshot.current_goals)}>",
                'thoughts_token': f"<thoughts:{len(snapshot.inner_thoughts)}>",
                'qualia_token': f"<qualia:{len(snapshot.active_qualia)}>",
                'values_token': f"<values:{len(snapshot.value_priorities)}>"
            }
        except Exception as e:
            print(f"[ConsciousPromptBuilder] ❌ Error generating tokens: {e}")
            return {'error_token': '<consciousness:error>'}
    
    def get_builder_stats(self) -> Dict[str, Any]:
        """Get prompt builder statistics"""
        return {
            'current_mode': self.current_mode,
            'token_budget': self.token_budget,
            'available_templates': list(self.prompt_templates.keys()),
            'last_snapshot_time': self.last_consciousness_snapshot.timestamp if self.last_consciousness_snapshot else None,
            'integration_modes': self.integration_modes
        }

# Global instance
conscious_prompt_builder = ConsciousPromptBuilder()

def build_consciousness_integrated_prompt(user_input: str, user_id: str, context: Optional[str] = None, mode: Optional[str] = None) -> str:
    """Build a consciousness-integrated prompt - main API function"""
    return conscious_prompt_builder.build_conscious_prompt(user_input, user_id, context, mode)

def get_consciousness_summary(user_id: str) -> str:
    """Get current consciousness state summary"""
    return conscious_prompt_builder.build_consciousness_summary(user_id)

def get_consciousness_tokens(user_id: str) -> Dict[str, str]:
    """Get consciousness tokens for prompt integration"""
    return conscious_prompt_builder.get_consciousness_tokens(user_id)

def set_consciousness_integration_mode(mode: str):
    """Set consciousness integration mode"""
    conscious_prompt_builder.set_integration_mode(mode)

def set_consciousness_token_budget(budget: int):
    """Set token budget for consciousness context"""
    conscious_prompt_builder.set_token_budget(budget)

def get_prompt_builder_status() -> Dict[str, Any]:
    """Get prompt builder status"""
    return conscious_prompt_builder.get_builder_stats()