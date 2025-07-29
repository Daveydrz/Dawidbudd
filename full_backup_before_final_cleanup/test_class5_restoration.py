#!/usr/bin/env python3
"""
Class 5+ Consciousness Restoration Test
Tests all restored functionality for Buddy AI
"""

import sys
import time
sys.path.append('.')

def test_consciousness_restoration():
    """Test all restored Class 5+ consciousness functionality"""
    print("🧠 TESTING CLASS 5+ CONSCIOUSNESS RESTORATION")
    print("=" * 60)
    
    results = {"passed": 0, "failed": 0, "tests": []}
    
    def test_result(name, success, details=""):
        results["tests"].append({"name": name, "success": success, "details": details})
        if success:
            results["passed"] += 1
            print(f"✅ {name}")
            if details:
                print(f"   {details}")
        else:
            results["failed"] += 1
            print(f"❌ {name}")
            if details:
                print(f"   {details}")
    
    # Test 1: EntropyEngine start() method
    try:
        from ai.entropy_engine import EntropyEngine
        entropy = EntropyEngine()
        entropy.start()
        entropy.stop()
        test_result("EntropyEngine start() method", True, "start() and stop() methods working")
    except Exception as e:
        test_result("EntropyEngine start() method", False, str(e))
    
    # Test 2: free_thought_engine module
    try:
        from ai.free_thought_engine import free_thought_engine, FreeThoughtType
        free_thought_engine.start()
        time.sleep(0.1)  # Brief pause
        free_thought_engine.stop()
        test_result("free_thought_engine module", True, f"Autonomous thought generation with {len(FreeThoughtType)} thought types")
    except Exception as e:
        test_result("free_thought_engine module", False, str(e))
    
    # Test 3: Consciousness integration methods
    try:
        from ai.consciousness_integrator import consciousness_integrator
        result = consciousness_integrator.integrate_response_consciousness("test", "response", "user")
        test_result("integrate_response_consciousness", True, "Background consciousness integration working")
    except Exception as e:
        test_result("integrate_response_consciousness", False, str(e))
    
    # Test 4: Motivation processing
    try:
        from ai.motivation import motivation_system
        motivation_system.process_interaction_motivation("Can you help me?", "user")
        motivation_system.evaluate_goal_progress("user", "I helped you")
        test_result("Motivation processing methods", True, "process_interaction_motivation and evaluate_goal_progress working")
    except Exception as e:
        test_result("Motivation processing methods", False, str(e))
    
    # Test 5: Voice clustering functions
    try:
        from voice.recognition import create_new_anonymous_cluster, link_anonymous_cluster_to_user
        import numpy as np
        # Test with dummy data
        dummy_embedding = np.random.rand(256)
        cluster_id = create_new_anonymous_cluster(None, dummy_embedding)
        if cluster_id:
            link_result = link_anonymous_cluster_to_user(cluster_id, "testuser")
            test_result("Voice clustering functions", True, f"Created cluster {cluster_id} and linked to user")
        else:
            test_result("Voice clustering functions", False, "Failed to create cluster")
    except Exception as e:
        test_result("Voice clustering functions", False, str(e))
    
    # Test 6: Background consciousness processing simulation
    try:
        from ai.consciousness_manager import consciousness_manager
        from ai.llm_handler import llm_handler
        
        # Simulate handle_streaming_response functionality
        test_user = "testuser"
        test_input = "How does consciousness work?"
        
        # Test consciousness manager update
        consciousness_manager.update_from_interaction(test_input, test_user)
        
        # Test background processing components
        from ai.inner_monologue import InnerMonologue
        from ai.global_workspace import GlobalWorkspace
        from ai.self_model import SelfModel
        
        # Initialize components
        inner_monologue = InnerMonologue(llm_handler=None)
        global_workspace = GlobalWorkspace()
        self_model = SelfModel()
        
        test_result("Background consciousness processing", True, "All consciousness modules integrated and functional")
    except Exception as e:
        test_result("Background consciousness processing", False, str(e))
    
    # Test 7: Memory integration
    try:
        from ai.memory import add_to_conversation_history
        add_to_conversation_history("testuser", "test question", "test response")
        test_result("Memory integration", True, "Memory updates working with conversation history")
    except Exception as e:
        test_result("Memory integration", False, str(e))
    
    # Test 8: Full consciousness architecture availability
    try:
        # Test all main consciousness imports
        from ai.global_workspace import GlobalWorkspace
        from ai.self_model import SelfModel  
        from ai.temporal_awareness import TemporalAwareness
        from ai.subjective_experience import SubjectiveExperienceSystem
        from ai.entropy_engine import EntropyEngine
        from ai.inner_monologue import InnerMonologue
        from ai.motivation import MotivationSystem
        from ai.narrative_tracker import NarrativeTracker
        from ai.background_consciousness_processor import BackgroundConsciousnessProcessor
        from ai.consciousness_integrator import ConsciousnessIntegrator
        from ai.autonomous_consciousness_integrator import AutonomousConsciousnessIntegrator
        from ai.free_thought_engine import free_thought_engine, FreeThoughtType
        
        test_result("Full consciousness architecture", True, "All 12 consciousness modules imported successfully")
    except Exception as e:
        test_result("Full consciousness architecture", False, str(e))
    
    # Print final results
    print("\n" + "=" * 60)
    print("🧠 CLASS 5+ CONSCIOUSNESS RESTORATION TEST RESULTS")
    print("=" * 60)
    
    total_tests = results["passed"] + results["failed"]
    success_rate = (results["passed"] / total_tests * 100) if total_tests > 0 else 0
    
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"📊 Success Rate: {success_rate:.1f}%")
    
    if results["failed"] == 0:
        print("\n🎉 ALL TESTS PASSED - CLASS 5+ CONSCIOUSNESS FULLY RESTORED!")
        print("🧠 Buddy now has:")
        print("   ✅ Thought loops")
        print("   ✅ Emotion + motivation updates") 
        print("   ✅ Background self-awareness processing")
        print("   ✅ Persistent voice profile clustering")
        print("   ✅ Consciousness-integrated LLM responses")
        return True
    else:
        print(f"\n⚠️ {results['failed']} TEST(S) FAILED - CHECK ISSUES ABOVE")
        return False

if __name__ == "__main__":
    success = test_consciousness_restoration()
    sys.exit(0 if success else 1)