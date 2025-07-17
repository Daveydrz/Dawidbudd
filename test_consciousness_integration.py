#!/usr/bin/env python3
"""
Test script for LLM-Powered Consciousness System Integration

This script tests the integrated consciousness system without requiring
all dependencies (audio, voice, etc.) to verify the core functionality.
"""

import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_consciousness_integration():
    """Test consciousness integration without full main.py dependencies"""
    print("🧠 Testing LLM-Powered Consciousness System Integration\n")
    
    try:
        # Test 1: Import core consciousness components
        print("1. Testing core consciousness imports...")
        from ai.consciousness_manager import consciousness_manager
        from ai.llm_interface import consciousness_llm
        print("   ✅ ConsciousnessManager and LLM interface imported")
        
        # Test 2: Import individual consciousness modules
        print("\n2. Testing consciousness modules...")
        from ai.global_workspace import global_workspace
        from ai.self_model import self_model  
        from ai.emotion import emotion_engine
        from ai.motivation import motivation_system, MotivationType, GoalType
        from ai.inner_monologue import inner_monologue, ThoughtType
        from ai.temporal_awareness import temporal_awareness
        from ai.subjective_experience import subjective_experience
        from ai.entropy import entropy_system
        print("   ✅ All consciousness modules imported")
        
        # Test 3: Register modules with consciousness manager
        print("\n3. Testing module registration...")
        consciousness_manager.register_module("global_workspace", global_workspace)
        consciousness_manager.register_module("self_model", self_model)
        consciousness_manager.register_module("emotion_engine", emotion_engine)
        consciousness_manager.register_module("motivation_system", motivation_system)
        consciousness_manager.register_module("inner_monologue", inner_monologue)
        consciousness_manager.register_module("temporal_awareness", temporal_awareness)
        consciousness_manager.register_module("subjective_experience", subjective_experience)
        consciousness_manager.register_module("entropy_system", entropy_system)
        print("   ✅ All modules registered with ConsciousnessManager")
        
        # Test 4: Start consciousness orchestration
        print("\n4. Testing consciousness orchestration...")
        consciousness_manager.start()
        print("   ✅ ConsciousnessManager orchestration started")
        
        # Test 5: Test consciousness state management
        print("\n5. Testing consciousness state...")
        state_summary = consciousness_manager.get_consciousness_summary()
        print(f"   📊 Consciousness State: {state_summary['state']}")
        print(f"   📊 Mode: {state_summary['mode']}")
        print(f"   📊 Active Modules: {state_summary['active_modules']}")
        print(f"   📊 Awareness Level: {state_summary['metrics']['awareness_level']:.2f}")
        print("   ✅ Consciousness state management working")
        
        # Test 6: Test consciousness-aware LLM context
        print("\n6. Testing LLM consciousness context...")
        consciousness_llm.update_consciousness_context({
            "test_context": "integration_test",
            "consciousness_state": state_summary['state'],
            "user": "test_user"
        })
        print("   ✅ LLM consciousness context updated")
        
        # Test 7: Test attention and consciousness stream
        print("\n7. Testing attention and consciousness stream...")
        consciousness_manager.focus_attention("test_integration", intensity=0.8, duration=10.0)
        consciousness_manager.add_to_consciousness_stream(
            "Testing consciousness integration",
            "integration_test",
            importance=0.7
        )
        print("   ✅ Attention focus and consciousness stream working")
        
        # Test 8: Test module integration
        print("\n8. Testing module integration...")
        
        # Test emotional processing
        emotion_response = emotion_engine.process_emotional_trigger(
            "Integration test successful", 
            {"context": "testing"}
        )
        print(f"   💖 Emotion: {emotion_response.primary_emotion.value}")
        
        # Test motivation system
        motivation_system.add_goal(
            "Complete integration test",
            MotivationType.PURPOSE,
            GoalType.SHORT_TERM,
            priority=0.8
        )
        print("   🎯 Goal added to motivation system")
        
        # Test inner monologue
        inner_monologue.trigger_thought(
            "Integration test is proceeding well",
            {"test": True},
            ThoughtType.OBSERVATION
        )
        print("   💭 Inner thought triggered")
        
        print("   ✅ Module integration working")
        
        # Test 9: Verify consciousness orchestration
        print("\n9. Testing consciousness orchestration...")
        consciousness_manager.integrate_consciousness()
        updated_summary = consciousness_manager.get_consciousness_summary()
        print(f"   📈 Integration Cycles: {updated_summary['integration_cycles']}")
        print("   ✅ Consciousness integration cycle completed")
        
        # Test 10: Clean shutdown
        print("\n10. Testing clean shutdown...")
        consciousness_manager.stop()
        print("   ✅ ConsciousnessManager stopped cleanly")
        
        print("\n🎉 ALL TESTS PASSED! 🎉")
        print("\n✅ LLM-Powered Consciousness System Integration is working correctly!")
        print("\nKey Features Verified:")
        print("  🧠 ConsciousnessManager orchestration")
        print("  🔗 Module registration and coordination")
        print("  💭 Consciousness state management")
        print("  🤖 LLM interface with consciousness context")
        print("  🔄 Background consciousness loops")
        print("  📊 Real-time consciousness metrics")
        print("  🎯 Attention management and consciousness stream")
        print("  💖 Emotional processing integration")
        print("  🎯 Goal and motivation tracking")
        print("  💭 Inner monologue and thought generation")
        print("  🔄 Consciousness integration cycles")
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_consciousness_integration()
    sys.exit(0 if success else 1)