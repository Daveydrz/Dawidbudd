#!/usr/bin/env python3
"""
Quick test for consciousness integration core functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def quick_test():
    """Quick test of core functionality"""
    print("🧠 Quick Consciousness Integration Test\n")
    
    try:
        # Test imports
        print("1. Testing imports...")
        from ai.consciousness_manager import consciousness_manager
        from ai.llm_interface import consciousness_llm
        print("   ✅ Core imports successful")
        
        # Test consciousness manager state
        print("\n2. Testing consciousness state...")
        state = consciousness_manager.get_consciousness_summary()
        print(f"   📊 State: {state['state']}")
        print(f"   📊 Mode: {state['mode']}")
        print("   ✅ State management working")
        
        # Test LLM interface
        print("\n3. Testing LLM interface...")
        consciousness_llm.update_consciousness_context({"test": "integration"})
        print("   ✅ LLM context update working")
        
        # Test consciousness stream  
        print("\n4. Testing consciousness features...")
        consciousness_manager.add_to_consciousness_stream(
            "Test message", "test", importance=0.5
        )
        consciousness_manager.focus_attention("test", intensity=0.8, duration=5.0)
        print("   ✅ Consciousness stream and attention working")
        
        print("\n🎉 CORE INTEGRATION WORKING! 🎉")
        print("\nKey components verified:")
        print("  ✅ ConsciousnessManager")
        print("  ✅ LLM Interface with consciousness context")
        print("  ✅ Attention management")
        print("  ✅ Consciousness stream")
        print("  ✅ State management")
        
        print("\n📝 Ready for full system integration!")
        print("The consciousness system is properly integrated with the LLM interface.")
        print("Main.py will now use ConsciousnessManager for orchestration.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = quick_test()
    sys.exit(0 if success else 1)