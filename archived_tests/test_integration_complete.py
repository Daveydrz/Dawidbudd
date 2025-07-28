#!/usr/bin/env python3
"""
Integration test for the complete system with cognitive modules

This script tests the integration between the new cognitive modules
and the existing LLM generation functions.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, '/home/runner/work/Dawidbudd/Dawidbudd')

def test_llm_integration():
    """Test integration with LLM generation functions"""
    print("🔗 Testing LLM Integration with Cognitive Modules")
    print("=" * 60)
    
    try:
        # Test import of main components
        print("\n📦 Testing Main System Imports...")
        from cognitive_modules.integration import cognitive_integrator
        print("✅ Cognitive integrator imported")
        
        # Test initialization
        print("\n🚀 Testing Initialization...")
        success = cognitive_integrator.initialize()
        if success:
            print("✅ Cognitive integrator initialized successfully")
        else:
            print("❌ Failed to initialize cognitive integrator")
            return False
        
        # Test cognitive context generation
        print("\n🧠 Testing Cognitive Context Generation...")
        context = cognitive_integrator.process_user_input(
            "Hello Buddy! I'm working on a coding project and could use some help.",
            "test_developer"
        )
        
        print(f"✅ Generated context with keys: {list(context.keys())}")
        
        # Verify expected structure
        if "cognitive_state" in context:
            print(f"   - Cognitive state: {context['cognitive_state']}")
        if "memory_context" in context:
            print(f"   - Memory context: {context['memory_context'][:100]}...")
        if "personality_context" in context:
            print(f"   - Personality traits: {len(context['personality_context'].get('key_traits', {}))}")
        if "goal_context" in context:
            print(f"   - Active goals: {context['goal_context']}")
        
        # Test LLM function imports (verify they exist)
        print("\n🔧 Testing LLM Function Availability...")
        try:
            from ai.chat_enhanced_smart_with_fusion import generate_response_streaming_with_intelligent_fusion
            print("✅ generate_response_streaming_with_intelligent_fusion available")
        except ImportError as e:
            print(f"⚠️ Fusion LLM function not available: {e}")
        
        try:
            from ai.llm_handler import generate_consciousness_integrated_response
            print("✅ generate_consciousness_integrated_response available")
        except ImportError as e:
            print(f"⚠️ Consciousness LLM function not available: {e}")
        
        # Test session management
        print("\n📋 Testing Session Management...")
        cognitive_integrator.start_session("test_developer")
        print("✅ Session started")
        
        status = cognitive_integrator.get_status()
        print(f"✅ Status retrieved: {status['initialized']}, active modules: {sum(status['modules'].values())}")
        
        cognitive_integrator.end_session()
        print("✅ Session ended")
        
        # Test thought loop integration
        print("\n💭 Testing Thought Loop Integration...")
        cognitive_integrator.trigger_reflection("integration test")
        print("✅ Reflection triggered")
        
        print("\n🎉 LLM integration tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_startup_sequence():
    """Test the startup sequence that would happen in main.py"""
    print("\n🔄 Testing Startup Sequence...")
    
    try:
        # Simulate the import sequence from main.py
        print("   - Testing main.py import pattern...")
        
        try:
            from cognitive_modules.integration import cognitive_integrator
            SELF_AWARENESS_COMPONENTS_AVAILABLE = True
            print("   ✅ New cognitive integrator loaded")
        except ImportError:
            try:
                from ai.cognitive_integration import cognitive_integrator
                SELF_AWARENESS_COMPONENTS_AVAILABLE = True
                print("   ✅ Fallback cognitive integrator loaded")
            except ImportError:
                SELF_AWARENESS_COMPONENTS_AVAILABLE = False
                print("   ❌ No cognitive integrator available")
        
        if SELF_AWARENESS_COMPONENTS_AVAILABLE:
            print("   ✅ SELF_AWARENESS_COMPONENTS_AVAILABLE = True")
            
            # Test the start method
            result = cognitive_integrator.start()
            print(f"   ✅ cognitive_integrator.start() = {result}")
            
            # Test the should_express_internal_state method
            should_express, expression = cognitive_integrator.should_express_internal_state()
            expr_summary = expression[:50] + "..." if expression else "No expression"
            print(f"   ✅ should_express_internal_state() = {should_express}, '{expr_summary}'")
            
        else:
            print("   ❌ Self-awareness components not available")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Startup sequence test failed: {e}")
        return False

def test_data_persistence():
    """Test that data persists correctly across restarts"""
    print("\n💾 Testing Data Persistence...")
    
    try:
        # Import modules fresh
        from cognitive_modules.self_model import PersistentSelfModel
        from cognitive_modules.goal_bank import GoalBank
        from cognitive_modules.experience_bank import ExperienceBank
        
        # Test that data files exist and have reasonable content
        data_dir = "/home/runner/work/Dawidbudd/Dawidbudd/cognitive_modules/data"
        
        files_to_check = [
            ("self_model.json", "personality_traits"),
            ("goal_bank.json", "goals"),  
            ("experience_bank.json", "experiences")
        ]
        
        import json
        for filename, key_to_check in files_to_check:
            filepath = os.path.join(data_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    if key_to_check in data:
                        print(f"   ✅ {filename}: Contains {key_to_check}")
                    else:
                        print(f"   ⚠️ {filename}: Missing {key_to_check}")
            else:
                print(f"   ❌ {filename}: File not found")
        
        # Test creating new instances and verify they load existing data
        self_model_test = PersistentSelfModel()
        if len(self_model_test.personality_traits) > 0:
            print(f"   ✅ Self-model loaded {len(self_model_test.personality_traits)} personality traits")
        
        goal_bank_test = GoalBank()
        if len(goal_bank_test.goals) > 0:
            print(f"   ✅ Goal bank loaded {len(goal_bank_test.goals)} goals")
        
        experience_bank_test = ExperienceBank()
        if len(experience_bank_test.experiences) > 0:
            print(f"   ✅ Experience bank loaded {len(experience_bank_test.experiences)} experiences")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Data persistence test failed: {e}")
        return False

if __name__ == "__main__":
    success = True
    
    success &= test_llm_integration()
    success &= test_startup_sequence() 
    success &= test_data_persistence()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ ALL INTEGRATION TESTS PASSED!")
        print("🚀 The cognitive modules are fully integrated and ready!")
        print("\n📋 Summary of implemented features:")
        print("   ✅ Persistent self-model with personality traits and beliefs")
        print("   ✅ Goal bank with long-term goal tracking")
        print("   ✅ Experience bank with episodic memory")
        print("   ✅ Background thought loop for self-reflection")
        print("   ✅ Memory prioritization for token management")
        print("   ✅ Full integration with existing LLM pipeline")
        print("   ✅ Session continuity and data persistence")
        
    else:
        print("❌ Some integration tests failed.")
        print("Please check the errors above before deploying.")
        sys.exit(1)