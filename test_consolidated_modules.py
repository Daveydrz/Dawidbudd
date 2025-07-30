#!/usr/bin/env python3
"""
Test script for consolidated modules - Phase 3 validation

This script tests:
1. All 5 consolidated modules can be imported
2. Basic functionality works
3. Backward compatibility is maintained
4. Integration between modules functions
"""

import sys
import traceback
from datetime import datetime

def test_goal_motivation():
    """Test goal_motivation.py module"""
    print("🎯 Testing goal_motivation.py...")
    try:
        from goal_motivation import (
            goal_motivation_system, 
            GoalType, 
            MotivationType,
            get_goal_engine,
            get_motivation_system
        )
        
        # Test basic functionality
        goal_id = goal_motivation_system.add_goal(
            "Test learning goal",
            MotivationType.CURIOSITY,
            GoalType.LEARNING,
            0.7
        )
        
        # Test backward compatibility
        goal_engine = get_goal_engine()
        motivation_sys = get_motivation_system()
        
        assert goal_id is not None
        assert len(goal_motivation_system.active_goals) > 0
        assert goal_engine is goal_motivation_system
        assert motivation_sys is goal_motivation_system
        
        print("  ✅ Goal motivation system working")
        return True
        
    except Exception as e:
        print(f"  ❌ Goal motivation test failed: {e}")
        traceback.print_exc()
        return False

def test_belief_memory():
    """Test belief_memory.py module"""
    print("🧠 Testing belief_memory.py...")
    try:
        from belief_memory import (
            get_user_memory,
            add_to_conversation_history,
            validate_ai_response_appropriateness,
            BeliefMemorySystem
        )
        
        # Test basic functionality
        memory_system = get_user_memory("test_user")
        
        # Test conversation history
        add_to_conversation_history("test_user", "Hello", "Hi there!")
        
        # Test response validation
        is_appropriate, response = validate_ai_response_appropriateness("test_user", "How are you?")
        
        assert isinstance(memory_system, BeliefMemorySystem)
        assert is_appropriate == True
        
        print("  ✅ Belief memory system working")
        return True
        
    except Exception as e:
        print(f"  ❌ Belief memory test failed: {e}")
        traceback.print_exc()
        return False

def test_self_awareness():
    """Test self_awareness.py module"""
    print("🔍 Testing self_awareness.py...")
    try:
        from self_awareness import (
            self_awareness_system,
            self_model,
            SelfAwarenessSystem,
            SelfModel
        )
        
        # Test basic functionality
        self_awareness_system.reflect_on_experience("Test reflection", {"test": True})
        
        # Test backward compatibility
        self_model.reflect_on_experience("Another reflection", {"test": True})
        
        stats = self_awareness_system.get_stats()
        
        assert isinstance(self_awareness_system, SelfAwarenessSystem)
        assert isinstance(self_model, SelfModel)
        assert stats["reflections"] > 0
        
        print("  ✅ Self awareness system working")
        return True
        
    except Exception as e:
        print(f"  ❌ Self awareness test failed: {e}")
        traceback.print_exc()
        return False

def test_voice_manager():
    """Test voice_manager.py module"""
    print("🎤 Testing voice_manager.py...")
    try:
        from voice_manager import (
            voice_manager,
            voice_database,
            VoiceManager,
            load_known_users,
            save_known_users
        )
        
        # Test basic functionality
        result = voice_manager.handle_voice_identification(None, "test")
        stats = voice_manager.get_session_stats()
        
        # Test database operations
        load_known_users()
        save_result = save_known_users()
        
        assert isinstance(voice_manager, VoiceManager)
        assert result[0] is not None  # Should return some user ID
        assert isinstance(stats, dict)
        
        print("  ✅ Voice manager system working")
        return True
        
    except Exception as e:
        print(f"  ❌ Voice manager test failed: {e}")
        traceback.print_exc()
        return False

def test_smart_audio_manager():
    """Test smart_audio_manager.py module"""
    print("🔊 Testing smart_audio_manager.py...")
    try:
        from smart_audio_manager import (
            smart_audio_manager,
            full_duplex_manager,
            SmartAudioManager,
            analyze_speech_detection,
            get_current_threshold
        )
        import numpy as np
        
        # Test basic functionality
        smart_audio_manager.start()
        stats = smart_audio_manager.get_stats()
        threshold = get_current_threshold()
        
        # Test audio processing
        test_audio = np.random.rand(1024).astype(np.float32)
        detection_result = analyze_speech_detection(test_audio)
        
        smart_audio_manager.stop()
        
        assert isinstance(smart_audio_manager, SmartAudioManager)
        assert isinstance(stats, dict)
        assert isinstance(threshold, float)
        assert "speech_detected" in detection_result
        
        print("  ✅ Smart audio manager system working")
        return True
        
    except Exception as e:
        print(f"  ❌ Smart audio manager test failed: {e}")
        traceback.print_exc()
        return False

def test_integration():
    """Test integration between modules"""
    print("🔗 Testing module integration...")
    try:
        # Test that modules can work together
        from goal_motivation import goal_motivation_system, MotivationType, GoalType
        from belief_memory import get_user_memory
        from self_awareness import self_awareness_system
        
        # Create a goal
        goal_id = goal_motivation_system.add_goal(
            "Integration test goal", 
            MotivationType.GROWTH, 
            GoalType.LEARNING
        )
        
        # Get memory system  
        memory = get_user_memory("integration_test")
        
        # Create self-awareness reflection
        self_awareness_system.reflect_on_experience(
            "Testing integration between systems", 
            {"goal_id": goal_id}
        )
        
        # Check that systems are working
        goal_stats = goal_motivation_system.get_stats()
        memory_stats = memory.get_stats()
        awareness_stats = self_awareness_system.get_stats()
        
        assert goal_stats["goals"]["total_active"] > 0
        assert isinstance(memory_stats, dict)
        assert awareness_stats["reflections"] > 0
        
        print("  ✅ Module integration working")
        return True
        
    except Exception as e:
        print(f"  ❌ Integration test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🧪 Phase 3 Consolidated Modules Test Suite")
    print("="*50)
    
    tests = [
        test_goal_motivation,
        test_belief_memory,
        test_self_awareness,
        test_voice_manager,
        test_smart_audio_manager,
        test_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"  ❌ Test crashed: {e}")
            print()
    
    print("="*50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Phase 3 consolidation successful!")
        return 0
    else:
        print(f"⚠️  {total - passed} tests failed - review needed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
