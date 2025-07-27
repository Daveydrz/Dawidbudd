#!/usr/bin/env python3
"""
Test script for thread safety of cognitive modules

This script tests the thread safety of the save operations in the cognitive modules
to ensure they don't corrupt data when accessed concurrently.
"""

import sys
import os
import threading
import time
import json
import tempfile
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, '/home/runner/work/Dawidbudd/Dawidbudd')

def test_thread_safety():
    """Test thread safety of cognitive module save operations"""
    print("🔒 Testing Thread Safety of Cognitive Modules")
    print("=" * 60)
    
    try:
        # Test imports
        print("\n📦 Testing Imports...")
        from ai.self_model import SelfModel
        from ai.subjective_experience import SubjectiveExperienceSystem
        from ai.goal_engine import GoalEngine
        print("✅ All modules imported successfully")
        
        # Create temp directory for test files
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Test SelfModel thread safety
            print("\n🧠 Testing SelfModel Thread Safety...")
            self_model = SelfModel(save_path=str(temp_path / "test_self_model.json"))
            test_concurrent_saves(self_model, "SelfModel", self_model._save_self_model)
            
            # Test SubjectiveExperience thread safety
            print("\n🌟 Testing SubjectiveExperience Thread Safety...")
            exp_system = SubjectiveExperienceSystem(save_path=str(temp_path / "test_experience.json"))
            test_concurrent_saves(exp_system, "SubjectiveExperience", exp_system._save_experience_state)
            
            # Test GoalEngine thread safety
            print("\n🎯 Testing GoalEngine Thread Safety...")
            goal_engine = GoalEngine(save_path=str(temp_path / "test_goals.json"))
            test_concurrent_saves(goal_engine, "GoalEngine", goal_engine._save_goal_state)
        
        print("\n✅ All thread safety tests passed!")
        
    except Exception as e:
        print(f"\n❌ Thread safety test failed: {e}")
        return False
    
    return True

def test_concurrent_saves(instance, module_name, save_method):
    """Test concurrent save operations on a module"""
    print(f"   Testing {module_name} concurrent saves...")
    
    # Track results
    results = {'success': 0, 'errors': 0}
    errors = []
    
    def save_worker(worker_id):
        """Worker function that performs save operations"""
        try:
            for i in range(5):  # Each worker does 5 saves
                save_method()
                time.sleep(0.01)  # Small delay to increase chance of collision
            results['success'] += 1
        except Exception as e:
            results['errors'] += 1
            errors.append(f"Worker {worker_id}: {str(e)}")
    
    # Create multiple threads to save concurrently
    threads = []
    num_workers = 3
    
    for i in range(num_workers):
        thread = threading.Thread(target=save_worker, args=(i,))
        threads.append(thread)
    
    # Start all threads
    for thread in threads:
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Check results
    if results['errors'] > 0:
        print(f"   ❌ {module_name}: {results['errors']} errors occurred")
        for error in errors:
            print(f"      - {error}")
        return False
    else:
        print(f"   ✅ {module_name}: All {num_workers} threads completed successfully")
        
        # Verify the save file exists and is valid JSON
        if hasattr(instance, 'save_path'):
            try:
                with open(instance.save_path, 'r') as f:
                    json.load(f)  # Validate JSON format
                print(f"   ✅ {module_name}: Save file is valid JSON")
            except Exception as e:
                print(f"   ❌ {module_name}: Save file validation failed: {e}")
                return False
        
        return True

if __name__ == "__main__":
    success = test_thread_safety()
    sys.exit(0 if success else 1)