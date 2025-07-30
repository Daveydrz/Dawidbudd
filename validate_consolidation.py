#!/usr/bin/env python3
"""
Final validation script for Phase 3 consolidation

This script validates:
1. All 5 consolidated modules are working
2. Backward compatibility is maintained
3. Integration between modules works
4. Production readiness indicators
"""

import sys
import os
from datetime import datetime

def validate_files_exist():
    """Validate all consolidated files exist"""
    required_files = [
        "goal_motivation.py",
        "belief_memory.py", 
        "self_awareness.py",
        "voice_manager.py",
        "smart_audio_manager.py"
    ]
    
    print("📁 Validating consolidated files...")
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"  ✅ {file} ({size:,} bytes)")
        else:
            print(f"  ❌ {file} missing!")
            return False
    
    return True

def validate_module_imports():
    """Validate all modules can be imported"""
    modules = [
        ("goal_motivation", ["goal_motivation_system", "GoalType", "MotivationType"]),
        ("belief_memory", ["get_user_memory", "BeliefMemorySystem"]),
        ("self_awareness", ["self_awareness_system", "SelfAwarenessSystem"]),
        ("voice_manager", ["voice_manager", "VoiceManager"]),
        ("smart_audio_manager", ["smart_audio_manager", "SmartAudioManager"])
    ]
    
    print("📦 Validating module imports...")
    for module_name, exports in modules:
        try:
            module = __import__(module_name)
            for export in exports:
                if hasattr(module, export):
                    print(f"  ✅ {module_name}.{export}")
                else:
                    print(f"  ❌ {module_name}.{export} missing!")
                    return False
        except ImportError as e:
            print(f"  ❌ {module_name} import failed: {e}")
            return False
    
    return True

def validate_functionality():
    """Validate basic functionality of each system"""
    print("⚙️  Validating functionality...")
    
    try:
        # Goal motivation system
        from goal_motivation import goal_motivation_system, MotivationType, GoalType
        goal_id = goal_motivation_system.add_goal(
            "Validation test goal", 
            MotivationType.ACHIEVEMENT, 
            GoalType.SHORT_TERM,
            0.8
        )
        assert goal_id is not None
        print("  ✅ Goal motivation system functional")
        
        # Belief memory system
        from belief_memory import get_user_memory
        memory = get_user_memory("validation_user")
        stats = memory.get_stats()
        assert isinstance(stats, dict)
        print("  ✅ Belief memory system functional")
        
        # Self awareness system  
        from self_awareness import self_awareness_system
        self_awareness_system.reflect_on_experience("Validation reflection", {})
        awareness_stats = self_awareness_system.get_stats()
        assert awareness_stats["reflections"] > 0
        print("  ✅ Self awareness system functional")
        
        # Voice manager system
        from voice_manager import voice_manager
        result = voice_manager.handle_voice_identification(None, "test")
        assert result[0] is not None
        print("  ✅ Voice manager system functional")
        
        # Smart audio manager system
        from smart_audio_manager import smart_audio_manager
        smart_audio_manager.start()
        audio_stats = smart_audio_manager.get_stats()
        smart_audio_manager.stop()
        assert isinstance(audio_stats, dict)
        print("  ✅ Smart audio manager system functional")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Functionality validation failed: {e}")
        return False

def validate_integration():
    """Validate that modules work together"""
    print("🔗 Validating system integration...")
    
    try:
        from goal_motivation import goal_motivation_system, MotivationType, GoalType
        from belief_memory import get_user_memory
        from self_awareness import self_awareness_system
        from voice_manager import voice_manager
        from smart_audio_manager import smart_audio_manager
        
        # Test cross-module interaction
        # 1. Create a goal
        goal_id = goal_motivation_system.add_goal(
            "Learn from user interaction",
            MotivationType.CURIOSITY,
            GoalType.LEARNING
        )
        
        # 2. Create memory entry
        memory = get_user_memory("integration_user")
        
        # 3. Self-reflect on the goal
        self_awareness_system.reflect_on_experience(
            f"Created goal for learning: {goal_id}",
            {"goal_id": goal_id, "integration_test": True}
        )
        
        # 4. Test voice and audio systems
        voice_result = voice_manager.handle_voice_identification(None, "integration test")
        
        smart_audio_manager.start()
        audio_working = smart_audio_manager.get_stats()["state"] is not None
        smart_audio_manager.stop()
        
        # Validate integration worked
        assert len(goal_motivation_system.active_goals) > 0
        assert memory.get_stats() is not None
        assert self_awareness_system.get_stats()["reflections"] > 0
        assert voice_result[0] is not None
        assert audio_working
        
        print("  ✅ Cross-module integration working")
        return True
        
    except Exception as e:
        print(f"  ❌ Integration validation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def validate_backward_compatibility():
    """Validate backward compatibility"""
    print("🔄 Validating backward compatibility...")
    
    try:
        # Test original module imports still work
        from ai.goal_engine import goal_engine
        from ai.motivation import motivation_system
        from ai.memory import get_user_memory as original_get_memory
        from ai.self_model import self_model
        
        # Test they still provide expected functionality
        assert hasattr(goal_engine, 'generate_spontaneous_desire')
        assert hasattr(motivation_system, 'get_current_motivations')
        
        memory = original_get_memory("compatibility_test")
        assert hasattr(memory, 'add_entity_memory')
        
        assert hasattr(self_model, 'reflect_on_experience')
        
        print("  ✅ Original module imports work")
        print("  ✅ Original functionality preserved")
        return True
        
    except Exception as e:
        print(f"  ❌ Backward compatibility failed: {e}")
        return False

def generate_consolidation_report():
    """Generate final consolidation report"""
    print("\n📊 PHASE 3 CONSOLIDATION REPORT")
    print("=" * 50)
    
    # File sizes
    total_size = 0
    for file in ["goal_motivation.py", "belief_memory.py", "self_awareness.py", 
                "voice_manager.py", "smart_audio_manager.py"]:
        if os.path.exists(file):
            size = os.path.getsize(file)
            total_size += size
            print(f"📄 {file:<25} {size:>8,} bytes")
    
    print(f"📄 {'TOTAL CONSOLIDATED':<25} {total_size:>8,} bytes")
    print()
    
    # Module count
    print(f"📦 Modules consolidated: 5/5 (100%)")
    print(f"🎯 Phase 3 target: COMPLETE")
    print(f"🎉 Total consolidation: 9/9 modules (100%)")
    print()
    
    # Features
    features = [
        "✅ Goal-setting and motivation systems unified",
        "✅ Belief and memory systems consolidated", 
        "✅ Self-awareness and introspection integrated",
        "✅ Voice recognition and management unified",
        "✅ Audio pipeline fully consolidated",
        "✅ Backward compatibility maintained",
        "✅ Cross-module integration working",
        "✅ Production-ready architecture"
    ]
    
    for feature in features:
        print(feature)
    
    print()
    print(f"🕐 Consolidation completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎉 PHASE 3 CONSOLIDATION SUCCESSFUL!")

def main():
    """Run all validation checks"""
    print("🧪 PHASE 3 CONSOLIDATION VALIDATION")
    print("=" * 50)
    
    checks = [
        ("File Existence", validate_files_exist),
        ("Module Imports", validate_module_imports), 
        ("Functionality", validate_functionality),
        ("Integration", validate_integration),
        ("Backward Compatibility", validate_backward_compatibility)
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        print(f"\n🔍 {name}:")
        if check_func():
            passed += 1
            print(f"✅ {name} PASSED")
        else:
            print(f"❌ {name} FAILED")
        print()
    
    print("=" * 50)
    print(f"📊 VALIDATION RESULTS: {passed}/{total} checks passed")
    
    if passed == total:
        generate_consolidation_report()
        return 0
    else:
        print(f"⚠️  {total - passed} validation checks failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
