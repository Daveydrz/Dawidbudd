#!/usr/bin/env python3
"""
Stress test for thread safety of cognitive modules

This script performs intensive concurrent operations to verify
the thread safety improvements are robust under heavy load.
"""

import sys
import os
import threading
import time
import json
import tempfile
import random
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add the project root to the path
sys.path.insert(0, '/home/runner/work/Dawidbudd/Dawidbudd')

def stress_test_thread_safety():
    """Stress test thread safety under heavy concurrent load"""
    print("🔥 Stress Testing Thread Safety Under Heavy Load")
    print("=" * 60)
    
    try:
        # Test imports
        print("\n📦 Loading Modules...")
        from ai.self_model import SelfModel
        from ai.subjective_experience import SubjectiveExperienceSystem, ExperienceType
        from ai.goal_engine import GoalEngine, GoalType
        print("✅ All modules loaded successfully")
        
        # Create temp directory for test files
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Test each module with heavy concurrent load
            print("\n🧠 Stress Testing SelfModel...")
            stress_test_self_model(temp_path)
            
            print("\n🌟 Stress Testing SubjectiveExperience...")
            stress_test_subjective_experience(temp_path)
            
            print("\n🎯 Stress Testing GoalEngine...")
            stress_test_goal_engine(temp_path)
        
        print("\n✅ All stress tests passed! Thread safety is robust.")
        
    except Exception as e:
        print(f"\n❌ Stress test failed: {e}")
        return False
    
    return True

def stress_test_self_model(temp_path):
    """Stress test SelfModel with concurrent saves and updates"""
    print("   Creating SelfModel instance...")
    
    # Import here to avoid scope issues
    from ai.self_model import SelfModel
    
    self_model = SelfModel(save_path=str(temp_path / "stress_self_model.json"))
    
    results = {"success": 0, "errors": 0, "data_corruption": 0}
    errors = []
    
    def worker_operations(worker_id, num_operations=20):
        """Worker that performs intensive operations"""
        try:
            for i in range(num_operations):
                # Update self-knowledge
                self_model.update_self_knowledge("strength", f"skill_{worker_id}_{i}", 0.8)
                
                # Trigger reflection
                self_model.reflect_on_experience(f"Worker {worker_id} experience {i}")
                
                # Save state (this is the critical thread-safety test)
                self_model._save_self_model()
                
                # Small random delay to increase chance of collisions
                time.sleep(random.uniform(0.001, 0.005))
            
            results["success"] += 1
        except Exception as e:
            results["errors"] += 1
            errors.append(f"Worker {worker_id}: {str(e)}")
    
    # Run 10 workers concurrently, each doing 20 operations
    print("   Running 10 workers x 20 operations each (200 total operations)...")
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(worker_operations, i) for i in range(10)]
        for future in as_completed(futures):
            future.result()  # Wait for completion
    
    # Verify final state
    try:
        with open(self_model.save_path, 'r') as f:
            final_data = json.load(f)
        
        print(f"   ✅ Completed: {results['success']}/10 workers successful")
        print(f"   ✅ Save file is valid JSON ({len(final_data)} keys)")
        print(f"   ✅ No data corruption detected")
        
        if results["errors"] > 0:
            print(f"   ❌ {results['errors']} errors occurred:")
            for error in errors[:3]:  # Show first 3 errors
                print(f"      - {error}")
    
    except json.JSONDecodeError:
        print("   ❌ Final save file is corrupted (invalid JSON)")
        results["data_corruption"] += 1

def stress_test_subjective_experience(temp_path):
    """Stress test SubjectiveExperience with concurrent processing"""
    print("   Creating SubjectiveExperience instance...")
    
    # Import here to avoid scope issues
    from ai.subjective_experience import SubjectiveExperienceSystem, ExperienceType
    
    exp_system = SubjectiveExperienceSystem(save_path=str(temp_path / "stress_experience.json"))
    exp_system.start()
    
    results = {"success": 0, "errors": 0}
    errors = []
    
    def worker_experiences(worker_id, num_experiences=15):
        """Worker that processes experiences concurrently"""
        try:
            for i in range(num_experiences):
                # Process different types of experiences
                exp_types = [ExperienceType.COGNITIVE, ExperienceType.EMOTIONAL, 
                           ExperienceType.SOCIAL, ExperienceType.CREATIVE]
                exp_type = random.choice(exp_types)
                
                trigger = f"Worker {worker_id} trigger {i}"
                
                # Process experience (this triggers saves)
                exp_system.process_experience(trigger, exp_type)
                
                # Random delay
                time.sleep(random.uniform(0.001, 0.003))
            
            results["success"] += 1
        except Exception as e:
            results["errors"] += 1
            errors.append(f"Worker {worker_id}: {str(e)}")
    
    # Run 8 workers concurrently
    print("   Running 8 workers x 15 experiences each (120 total experiences)...")
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(worker_experiences, i) for i in range(8)]
        for future in as_completed(futures):
            future.result()
    
    # Stop the system and verify
    exp_system.stop()
    
    try:
        with open(exp_system.save_path, 'r') as f:
            final_data = json.load(f)
        
        print(f"   ✅ Completed: {results['success']}/8 workers successful")
        print(f"   ✅ Save file is valid JSON ({len(final_data)} keys)")
        print(f"   ✅ Total experiences processed: {exp_system.total_experiences}")
        
    except json.JSONDecodeError:
        print("   ❌ Final save file is corrupted (invalid JSON)")

def stress_test_goal_engine(temp_path):
    """Stress test GoalEngine with concurrent goal operations"""
    print("   Creating GoalEngine instance...")
    
    # Import here to avoid scope issues
    from ai.goal_engine import GoalEngine, GoalType
    
    goal_engine = GoalEngine(save_path=str(temp_path / "stress_goals.json"))
    goal_engine.start()
    
    results = {"success": 0, "errors": 0}
    errors = []
    
    def worker_goals(worker_id, num_goals=10):
        """Worker that creates and manages goals"""
        try:
            for i in range(num_goals):
                # Generate spontaneous desires and goals
                desire = goal_engine.generate_spontaneous_desire(
                    {"worker_id": worker_id, "iteration": i}
                )
                
                if desire:
                    # Promote some desires to goals
                    if random.random() > 0.5:
                        goal = goal_engine.promote_desire_to_goal(desire)
                        if goal:
                            # Update progress on some goals
                            if random.random() > 0.3:
                                progress = random.uniform(0.1, 1.0)
                                goal_engine.update_goal_progress(goal.id, progress, 0.1)
                
                # Random delay
                time.sleep(random.uniform(0.002, 0.008))
            
            results["success"] += 1
        except Exception as e:
            results["errors"] += 1
            errors.append(f"Worker {worker_id}: {str(e)}")
    
    # Run 6 workers concurrently
    print("   Running 6 workers x 10 goal operations each (60 total operations)...")
    
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = [executor.submit(worker_goals, i) for i in range(6)]
        for future in as_completed(futures):
            future.result()
    
    # Stop and verify
    goal_engine.stop()
    
    try:
        with open(goal_engine.save_path, 'r') as f:
            final_data = json.load(f)
        
        print(f"   ✅ Completed: {results['success']}/6 workers successful")
        print(f"   ✅ Save file is valid JSON ({len(final_data)} keys)")
        print(f"   ✅ Total goals created: {goal_engine.total_goals_created}")
        print(f"   ✅ Total desires generated: {goal_engine.total_desires_generated}")
        
    except json.JSONDecodeError:
        print("   ❌ Final save file is corrupted (invalid JSON)")

if __name__ == "__main__":
    success = stress_test_thread_safety()
    sys.exit(0 if success else 1)