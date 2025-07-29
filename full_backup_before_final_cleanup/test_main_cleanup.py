#!/usr/bin/env python3
"""
Test script to verify main.py cleanup is complete and imports work
"""

import sys
import importlib.util

def test_main_imports():
    """Test that main.py can import without errors"""
    print("🧪 Testing main.py imports...")
    
    try:
        # Test direct import of main components
        from ai.llm_handler import llm_handler
        from ai.memory import add_to_conversation_history, get_user_memory
        from ai.consciousness_manager import consciousness_manager, ConsciousnessMode
        
        print("✅ Core imports successful:")
        print(f"  - llm_handler: {type(llm_handler)}")
        print(f"  - add_to_conversation_history: {type(add_to_conversation_history)}")
        print(f"  - get_user_memory: {type(get_user_memory)}")
        print(f"  - consciousness_manager: {type(consciousness_manager)}")
        print(f"  - ConsciousnessMode: {ConsciousnessMode}")
        
        # Test consciousness manager functionality
        status = consciousness_manager.get_status()
        print(f"  - Consciousness manager status: {status['is_running']}")
        print(f"  - Current mode: {status['mode']}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_no_old_consciousness_modules():
    """Test that old consciousness modules are not accessible"""
    print("\n🧪 Testing old consciousness modules are removed...")
    
    old_modules = [
        'ai.inner_monologue',
        'ai.free_thought_engine', 
        'ai.entropy_engine',
        'ai.self_model',
        'ai.subjective_experience',
        'ai.narrative_tracker',
        'ai.consciousness_tokenizer',
        'ai.global_workspace',
        'ai.emotion',
        'ai.motivation',
        'ai.temporal_awareness',
        'ai.entropy'
    ]
    
    removed_count = 0
    for module_name in old_modules:
        try:
            importlib.import_module(module_name)
            print(f"⚠️  {module_name} is still accessible (should be archived)")
        except ImportError:
            print(f"✅ {module_name} properly removed")
            removed_count += 1
        except Exception as e:
            print(f"❓ {module_name} - unexpected error: {e}")
    
    print(f"\n📊 Summary: {removed_count}/{len(old_modules)} modules properly removed")
    return removed_count == len(old_modules)

def main():
    """Run all tests"""
    print("🚀 Running Buddy cleanup verification tests...\n")
    
    import_test = test_main_imports()
    removal_test = test_no_old_consciousness_modules()
    
    print(f"\n🎯 Test Results:")
    print(f"  ✅ Core imports working: {import_test}")
    print(f"  ✅ Old modules removed: {removal_test}")
    
    if import_test and removal_test:
        print(f"\n🎉 ALL TESTS PASSED - Buddy cleanup successful!")
        print(f"   - Only consciousness_manager handles consciousness")
        print(f"   - No conflicting consciousness modules")
        print(f"   - Clean import structure")
        return True
    else:
        print(f"\n❌ SOME TESTS FAILED - Cleanup needs attention")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)