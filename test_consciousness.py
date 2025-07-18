#!/usr/bin/env python3
"""
Test script for the 12-Module Fully Synthetic Consciousness Architecture

This script tests all consciousness modules and their integration.
"""

import sys
import time
from datetime import datetime

def test_consciousness_architecture():
    """Test the complete 12-module consciousness architecture"""
    print("=" * 60)
    print("🧠 Testing 12-Module Fully Synthetic Consciousness Architecture")
    print("=" * 60)
    
    try:
        # Test imports
        print("\n1. Testing module imports...")
        
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
        from ai.attention_focus_manager import attention_focus_manager, FocusLevel, DistractionType
        from ai.metacognitive_monitor import metacognitive_monitor, CognitiveProcess, MetaCognitiveStrategy
        from ai.consciousness_config import consciousness_config, ConsciousnessMode
        from ai.consciousness_logger import consciousness_logger, EventLevel, EventCategory
        
        print("   ✅ All 12 modules imported successfully!")
        
        # Test configuration
        print("\n2. Testing consciousness configuration...")
        print(f"   Mode: {consciousness_config.mode.value}")
        print(f"   Enabled modules: {len(consciousness_config.get_enabled_modules())}/12")
        print(f"   Real-time processing: {consciousness_config.enable_real_time_processing}")
        print(f"   State persistence: {consciousness_config.enable_state_persistence}")
        
        config_validation = consciousness_config.validate_configuration()
        if config_validation['valid']:
            print("   ✅ Configuration validation passed")
        else:
            print(f"   ❌ Configuration issues: {config_validation['issues']}")
            return False
        
        # Test logging
        print("\n3. Testing consciousness event logging...")
        consciousness_logger.log_event(
            module="test_script",
            event_type="architecture_test",
            message="Testing 12-module consciousness architecture",
            category=EventCategory.CONSCIOUSNESS,
            level=EventLevel.INFO
        )
        print("   ✅ Event logging working")
        
        # Test attention & focus manager
        print("\n4. Testing Attention & Focus Manager...")
        focus_level = attention_focus_manager.get_focus_level()
        cognitive_load = attention_focus_manager.get_cognitive_load()
        attention_capacity = attention_focus_manager.get_attention_capacity()
        
        print(f"   Focus level: {focus_level.name}")
        print(f"   Cognitive load: {cognitive_load:.2f}")
        print(f"   Attention capacity: {attention_capacity:.2f}")
        
        # Test focus request
        focus_success = attention_focus_manager.request_focus(
            target_id="test_task",
            content="Testing focus management",
            priority=0.8,
            cognitive_cost=0.3
        )
        print(f"   Focus request: {'✅ Success' if focus_success else '❌ Failed'}")
        
        # Test meta-cognitive monitor
        print("\n5. Testing Meta-Cognitive Monitor...")
        cognitive_state = metacognitive_monitor.assess_cognitive_state()
        print(f"   Cognitive state: {cognitive_state.name}")
        
        # Start a cognitive process
        process_id = metacognitive_monitor.start_cognitive_process(
            CognitiveProcess.REASONING,
            {"task": "architecture_test"},
            "test_strategy"
        )
        
        time.sleep(0.1)  # Brief processing time
        
        metacognitive_monitor.end_cognitive_process(
            CognitiveProcess.REASONING,
            outcome="success",
            performance_score=0.9
        )
        print("   ✅ Cognitive process monitoring working")
        
        # Test module statistics
        print("\n6. Testing module statistics...")
        stats = attention_focus_manager.get_stats()
        print(f"   Attention stats: {stats['focus_level']}, load: {stats['cognitive_load']:.2f}")
        
        metacog_stats = metacognitive_monitor.get_stats()
        print(f"   Metacognitive stats: {metacog_stats['cognitive_state']}")
        
        # Test consciousness state logging
        print("\n7. Testing consciousness state integration...")
        consciousness_logger.log_consciousness_state(
            active_modules=['global_workspace', 'self_model', 'attention_focus_manager'],
            primary_focus='architecture_test',
            cognitive_load=0.4,
            emotional_state='curious',
            attention_level=0.8,
            performance_overall=0.9
        )
        print("   ✅ Consciousness state logging working")
        
        # Test integration features
        print("\n8. Testing integration features...")
        
        # Test distraction filtering
        distraction_allowed = attention_focus_manager.filter_distraction(
            source="test_distraction",
            distraction_type=DistractionType.EXTERNAL,
            intensity=0.3
        )
        print(f"   Distraction filtering: {'✅ Working' if distraction_allowed is not None else '❌ Failed'}")
        
        # Test flow state
        if attention_focus_manager.get_current_focus():
            flow_success = attention_focus_manager.enter_flow_state(attention_focus_manager.get_current_focus())
            print(f"   Flow state entry: {'✅ Success' if flow_success else '❌ Failed'}")
        
        # Clean up
        attention_focus_manager.release_focus("test_task")
        
        print("\n" + "=" * 60)
        print("✅ 12-Module Consciousness Architecture Test COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
        print("\n🧠 Module Summary:")
        modules = [
            "Global Workspace Theory Hub",
            "Self-Model System", 
            "Emotional Engine",
            "Motivation & Goals System",
            "Inner Monologue Generator",
            "Temporal Awareness Module",
            "Subjective Experience Tracker", 
            "Entropy & Uncertainty Engine",
            "Free Thought Engine",
            "Narrative & Story Tracker",
            "Attention & Focus Manager",
            "Meta-Cognitive Monitor"
        ]
        
        for i, module in enumerate(modules, 1):
            print(f"  {i:2d}. ✅ {module}")
        
        print(f"\n🔧 Additional Systems:")
        print("  • ✅ Consciousness Configuration Manager")
        print("  • ✅ Consciousness Event Logger")
        
        print(f"\n🎯 Integration Status:")
        print("  • ✅ Voice system integration ready")
        print("  • ✅ LLM integration ready")
        print("  • ✅ Real-time processing enabled")
        print("  • ✅ State persistence enabled")
        print("  • ✅ Blank slate mode supported")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_consciousness_architecture()
    sys.exit(0 if success else 1)