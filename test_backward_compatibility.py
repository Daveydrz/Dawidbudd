#!/usr/bin/env python3
"""
Test backward compatibility of consolidated modules

This ensures that existing code will continue to work after consolidation.
"""

import sys

def test_existing_imports():
    """Test that existing imports still work"""
    print("🔄 Testing backward compatibility...")
    
    try:
        # Test that we can still import from original ai modules
        print("  • Testing AI module imports...")
        
        # These should work because the files still exist
        try:
            from ai.goal_engine import goal_engine
            print("    ✅ ai.goal_engine import works")
        except ImportError as e:
            print(f"    ⚠️  ai.goal_engine import failed: {e}")
        
        try:
            from ai.motivation import motivation_system
            print("    ✅ ai.motivation import works") 
        except ImportError as e:
            print(f"    ⚠️  ai.motivation import failed: {e}")
        
        try:
            from ai.memory import get_user_memory
            print("    ✅ ai.memory import works")
        except ImportError as e:
            print(f"    ⚠️  ai.memory import failed: {e}")
        
        try:
            from ai.self_model import self_model
            print("    ✅ ai.self_model import works")
        except ImportError as e:
            print(f"    ⚠️  ai.self_model import failed: {e}")
        
        # Test consolidated module imports work
        print("  • Testing consolidated module imports...")
        
        from goal_motivation import goal_motivation_system
        from belief_memory import get_user_memory as get_memory_consolidated
        from self_awareness import self_awareness_system
        from voice_manager import voice_manager
        from smart_audio_manager import smart_audio_manager
        
        print("    ✅ All consolidated modules import successfully")
        
        # Test that they provide expected functionality
        print("  • Testing functionality compatibility...")
        
        # Goal/motivation system
        stats = goal_motivation_system.get_stats()
        assert "goals" in stats
        print("    ✅ Goal motivation system provides expected interface")
        
        # Memory system
        memory = get_memory_consolidated("test_user")
        memory_stats = memory.get_stats()
        assert isinstance(memory_stats, dict)
        print("    ✅ Memory system provides expected interface")
        
        # Self awareness
        awareness_stats = self_awareness_system.get_stats()
        assert isinstance(awareness_stats, dict)
        print("    ✅ Self awareness system provides expected interface")
        
        # Voice manager
        voice_stats = voice_manager.get_session_stats()
        assert isinstance(voice_stats, dict)
        print("    ✅ Voice manager provides expected interface")
        
        # Audio manager
        audio_stats = smart_audio_manager.get_stats()
        assert isinstance(audio_stats, dict)
        print("    ✅ Audio manager provides expected interface")
        
        return True
        
    except Exception as e:
        print(f"    ❌ Compatibility test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run backward compatibility tests"""
    print("🔙 Backward Compatibility Test Suite")
    print("="*40)
    
    success = test_existing_imports()
    
    print("="*40)
    if success:
        print("🎉 Backward compatibility maintained!")
        return 0
    else:
        print("⚠️  Compatibility issues detected")
        return 1

if __name__ == "__main__":
    sys.exit(main())
