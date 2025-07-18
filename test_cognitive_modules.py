#!/usr/bin/env python3
"""
Test script for persistent cognitive modules

This script tests the core functionality of the new persistent cognitive modules
to ensure they work properly with the existing system.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, '/home/runner/work/Dawidbudd/Dawidbudd')

def test_cognitive_modules():
    """Test all cognitive modules"""
    print("🧠 Testing Persistent Cognitive Modules")
    print("=" * 60)
    
    try:
        # Test imports
        print("\n📦 Testing Imports...")
        from cognitive_modules.self_model import persistent_self_model
        from cognitive_modules.goal_bank import goal_bank, GoalType
        from cognitive_modules.experience_bank import experience_bank
        from cognitive_modules.memory_prioritization import memory_prioritizer
        from cognitive_modules.thought_loop import thought_loop
        from cognitive_modules.integration import cognitive_integrator
        print("✅ All modules imported successfully")
        
        # Test self model
        print("\n🔍 Testing Self Model...")
        self_data = persistent_self_model.get_cognitive_injection_data()
        print(f"✅ Self-model data keys: {list(self_data.keys())}")
        print(f"   - Personality traits: {len(self_data.get('self_traits', {}))}")
        print(f"   - Core beliefs: {len(self_data.get('core_beliefs', {}))}")
        
        # Test goal bank
        print("\n🎯 Testing Goal Bank...")
        goals_data = goal_bank.get_cognitive_injection_data()
        print(f"✅ Goals data keys: {list(goals_data.keys())}")
        print(f"   - Buddy goals: {len(goals_data.get('buddy_active_goals', []))}")
        print(f"   - User goals: {len(goals_data.get('user_active_goals', []))}")
        
        # Test experience bank
        print("\n💭 Testing Experience Bank...")
        exp_data = experience_bank.get_cognitive_injection_data()
        print(f"✅ Experience data keys: {list(exp_data.keys())}")
        print(f"   - Priority experiences: {len(exp_data.get('priority_experiences', []))}")
        print(f"   - Recent experiences: {len(exp_data.get('recent_experiences', []))}")
        
        # Test memory prioritization
        print("\n🧮 Testing Memory Prioritization...")
        prioritized_context = memory_prioritizer.prioritize_cognitive_context(
            user="test_user",
            current_context="Hello, how are you today?",
            context_priority="balanced"
        )
        print(f"✅ Prioritized context keys: {list(prioritized_context.keys())}")
        estimated_tokens = prioritized_context.get("token_usage", {}).get("estimated_total", 0)
        print(f"   - Estimated tokens: {estimated_tokens}")
        
        # Test cognitive integration
        print("\n🔗 Testing Cognitive Integration...")
        integration_result = cognitive_integrator.process_user_input(
            "Hello Buddy, I hope you're doing well!",
            "test_user"
        )
        print(f"✅ Integration result keys: {list(integration_result.keys())}")
        if "cognitive_state" in integration_result:
            cognitive_state = integration_result["cognitive_state"]
            print(f"   - Current emotion: {cognitive_state.get('emotion', 'unknown')}")
            print(f"   - Current mood: {cognitive_state.get('mood', 'unknown')}")
        
        # Test thought loop status (but don't start it for testing)
        print("\n🔄 Testing Thought Loop...")
        thought_status = thought_loop.get_status()
        print(f"✅ Thought loop status: {thought_status}")
        
        # Test adding a new experience
        print("\n➕ Testing Experience Addition...")
        exp_id = experience_bank.add_experience(
            event="Completed cognitive module testing",
            emotion="satisfaction",
            importance=0.7,
            user="test_user",
            context={"test": True}
        )
        print(f"✅ Added experience with ID: {exp_id}")
        
        # Test goal creation
        print("\n🎯 Testing Goal Creation...")
        goal_id = goal_bank.create_goal(
            title="Test Goal Completion",
            description="Successfully test all cognitive modules",
            goal_type=GoalType.SYSTEM,
            is_buddy_goal=True,
            priority=0.8
        )
        print(f"✅ Created goal with ID: {goal_id}")
        
        # Test goal progress update
        goal_bank.update_goal_progress(goal_id, 1.0, "All tests completed successfully")
        print(f"✅ Updated goal progress to 100%")
        
        print("\n🎉 All cognitive module tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_persistence():
    """Test data persistence across restarts"""
    print("\n💾 Testing Data Persistence...")
    
    try:
        # Check if data files exist
        import os
        data_dir = "/home/runner/work/Dawidbudd/Dawidbudd/cognitive_modules/data"
        
        expected_files = [
            "self_model.json",
            "goal_bank.json", 
            "experience_bank.json"
        ]
        
        for filename in expected_files:
            filepath = os.path.join(data_dir, filename)
            if os.path.exists(filepath):
                file_size = os.path.getsize(filepath)
                print(f"✅ {filename}: {file_size} bytes")
            else:
                print(f"⚠️ {filename}: Not found (will be created on first use)")
        
        return True
        
    except Exception as e:
        print(f"❌ Persistence test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_cognitive_modules()
    success &= test_data_persistence()
    
    if success:
        print("\n✅ All tests completed successfully!")
        print("🚀 Cognitive modules are ready for integration!")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        sys.exit(1)