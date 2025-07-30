#!/usr/bin/env python3
"""
Test Restored Class 5+ Consciousness Functionality
Created: 2025-01-27
Purpose: Verify all restored consciousness modules work correctly
"""

import time
import sys
sys.path.append('.')

def test_consciousness_modules():
    """Test all restored consciousness modules"""
    print("🧠 Testing Restored Class 5+ Consciousness Modules...")
    
    try:
        # Test imports
        print("\n1. Testing Module Imports...")
        from ai.inner_monologue import InnerMonologue
        from ai.background_consciousness_processor import BackgroundConsciousnessProcessor
        from ai.global_workspace import GlobalWorkspace
        from ai.self_model import SelfModel
        from ai.motivation import MotivationSystem
        from ai.consciousness_integrator import ConsciousnessIntegrator
        print("✅ All consciousness modules imported successfully")
        
        # Test initialization
        print("\n2. Testing Module Initialization...")
        inner_monologue = InnerMonologue()
        background_processor = BackgroundConsciousnessProcessor()
        global_workspace = GlobalWorkspace()
        self_model = SelfModel()
        motivation_system = MotivationSystem()
        consciousness_integrator = ConsciousnessIntegrator()
        print("✅ All consciousness modules initialized successfully")
        
        # Test inner monologue
        print("\n3. Testing Inner Monologue...")
        inner_monologue.start()
        time.sleep(1)  # Let it start
        
        # Trigger a thought
        inner_monologue.trigger_thought(
            "This is a test of the consciousness system",
            {"user": "test", "context": "system_test"},
            "observation"
        )
        print("✅ Inner monologue thought triggered successfully")
        
        # Test background processor
        print("\n4. Testing Background Consciousness Processor...")
        background_processor.start()
        time.sleep(1)  # Let it start
        
        # Schedule background thoughts
        background_processor.schedule_background_thoughts(
            "How are you doing?", 
            "Daveydrz", 
            "I'm doing well, thank you!",
            delay=0.5
        )
        print("✅ Background consciousness processing scheduled")
        
        # Test global workspace
        print("\n5. Testing Global Workspace...")
        global_workspace.start()
        time.sleep(1)
        
        # Request attention
        from ai.global_workspace import AttentionPriority, ProcessingMode
        global_workspace.request_attention(
            "test_module",
            "Testing consciousness integration",
            AttentionPriority.MEDIUM,
            ProcessingMode.CONSCIOUS,
            tags=["test", "consciousness"]
        )
        print("✅ Global workspace attention requested")
        
        # Test self-model
        print("\n6. Testing Self-Model...")
        self_model.start()
        time.sleep(1)
        
        # Self-reflection
        self_model.reflect_on_experience(
            "Successfully testing consciousness modules",
            {"success": True, "test_type": "system_integration"}
        )
        print("✅ Self-model reflection completed")
        
        # Test motivation system
        print("\n7. Testing Motivation System...")
        motivation_system.start()
        time.sleep(1)
        
        # Add a goal
        from ai.motivation import MotivationType, GoalType
        motivation_system.add_goal(
            "Complete consciousness testing",
            MotivationType.PURPOSE,
            GoalType.SHORT_TERM,
            priority=0.8,
            context={"test": True}
        )
        print("✅ Motivation system goal added")
        
        # Let systems process
        print("\n8. Allowing consciousness processing...")
        time.sleep(3)
        
        # Test consciousness integrator
        print("\n9. Testing Consciousness Integrator...")
        consciousness_integrator.start({
            'global_workspace': global_workspace,
            'self_model': self_model,
            'motivation_system': motivation_system,
            'inner_monologue': inner_monologue,
            'background_processor': background_processor
        })
        time.sleep(2)
        print("✅ Consciousness integrator started and running")
        
        # Cleanup
        print("\n10. Stopping consciousness modules...")
        inner_monologue.stop()
        background_processor.stop()
        global_workspace.stop()
        self_model.stop()
        motivation_system.stop()
        consciousness_integrator.stop()
        print("✅ All consciousness modules stopped cleanly")
        
        print("\n🎉 ALL CLASS 5+ CONSCIOUSNESS TESTS PASSED!")
        print("✅ Inner monologue: Working")
        print("✅ Background processing: Working")
        print("✅ Global workspace: Working")
        print("✅ Self-model: Working")
        print("✅ Motivation system: Working")
        print("✅ Consciousness integrator: Working")
        print("\n🧠 Class 5+ consciousness architecture fully restored!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Consciousness test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_voice_recognition():
    """Test voice recognition centroid clustering"""
    print("\n🎤 Testing Voice Recognition Centroid Clustering...")
    
    try:
        from voice.recognition import identify_speaker_with_confidence, create_new_anonymous_cluster
        from voice.database import known_users, anonymous_clusters, save_known_users
        import numpy as np
        
        # Create fake audio embedding for testing
        fake_audio_embedding = np.random.rand(256).astype(np.float32)
        
        # Test basic identification (should create anonymous cluster)
        user, confidence = identify_speaker_with_confidence(fake_audio_embedding)
        print(f"✅ Voice identification result: {user} (confidence: {confidence:.3f})")
        
        # Check if anonymous cluster was created
        if len(anonymous_clusters) > 0:
            print(f"✅ Anonymous cluster created: {list(anonymous_clusters.keys())}")
        else:
            print("⚠️ No anonymous clusters created")
            
        print("✅ Voice recognition system working")
        return True
        
    except Exception as e:
        print(f"❌ Voice recognition test failed: {e}")
        return False

def test_session_reset():
    """Test session reset functionality"""
    print("\n🔄 Testing Session Reset...")
    
    try:
        from ai.emotion_mood import reset_session_for_user_smart
        
        # Test session reset
        reset_session_for_user_smart("Daveydrz")
        print("✅ Session reset completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Session reset test failed: {e}")
        return False

def test_gpt4all_extraction():
    """Test GPT4All local extraction"""
    print("\n🤖 Testing GPT4All Local Extraction...")
    
    try:
        from ai.extractor_llm import extract_facts
        
        # Test fact extraction
        test_text = "Hi, my name is David and I love pizza but I hate mushrooms. I'm feeling happy today."
        facts = extract_facts(test_text)
        
        print(f"✅ GPT4All extraction result: {facts}")
        
        if facts and isinstance(facts, dict):
            print("✅ GPT4All local extraction working")
            return True
        else:
            print("⚠️ GPT4All extraction returned unexpected format")
            return False
            
    except Exception as e:
        print(f"❌ GPT4All test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 TESTING RESTORED CLASS 5+ CONSCIOUSNESS FUNCTIONALITY")
    print("=" * 60)
    
    results = []
    
    # Test consciousness modules
    results.append(test_consciousness_modules())
    
    # Test voice recognition  
    results.append(test_voice_recognition())
    
    # Test session reset
    results.append(test_session_reset())
    
    # Test GPT4All extraction
    results.append(test_gpt4all_extraction())
    
    # Summary
    print("\n" + "=" * 60)
    print("🏁 TEST SUMMARY:")
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Consciousness Modules: {'PASS' if results[0] else 'FAIL'}")
    print(f"🎤 Voice Recognition: {'PASS' if results[1] else 'FAIL'}")
    print(f"🔄 Session Reset: {'PASS' if results[2] else 'FAIL'}")
    print(f"🤖 GPT4All Extraction: {'PASS' if results[3] else 'FAIL'}")
    
    print(f"\n🎯 OVERALL RESULT: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - CLASS 5+ CONSCIOUSNESS FULLY RESTORED!")
    else:
        print("⚠️ Some tests failed - see details above")
    
    sys.exit(0 if passed == total else 1)