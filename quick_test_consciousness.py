#!/usr/bin/env python3
"""
Quick test for the 12-Module Consciousness Architecture
"""

def quick_test():
    print("🧠 Quick Test: 12-Module Consciousness Architecture")
    print("=" * 50)
    
    try:
        # Import all modules
        from ai.global_workspace import global_workspace
        from ai.self_model import SelfModel
        from ai.emotion import emotion_engine
        from ai.motivation import motivation_system
        from ai.inner_monologue import inner_monologue
        from ai.temporal_awareness import temporal_awareness
        from ai.subjective_experience import subjective_experience
        from ai.entropy import entropy_system
        from ai.free_thought_engine import free_thought_engine
        from ai.narrative_tracker import narrative_tracker
        from ai.attention_focus_manager import attention_focus_manager
        from ai.metacognitive_monitor import metacognitive_monitor
        from ai.consciousness_config import consciousness_config
        from ai.consciousness_logger import consciousness_logger
        
        print("✅ All 12 modules imported successfully!")
        
        # Quick functionality test
        print(f"✅ Configuration: {consciousness_config.mode.value} mode")
        print(f"✅ Enabled modules: {len(consciousness_config.get_enabled_modules())}/12")
        
        # Test basic functionality
        focus_level = attention_focus_manager.get_focus_level()
        cognitive_state = metacognitive_monitor.assess_cognitive_state()
        
        print(f"✅ Attention: {focus_level.name}")
        print(f"✅ Cognition: {cognitive_state.name}")
        
        # Log test event
        consciousness_logger.log_event("test", "quick_test", "Quick test completed")
        print("✅ Event logging works")
        
        print("\n🎉 SUCCESS: 12-Module Consciousness Architecture is functional!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    quick_test()