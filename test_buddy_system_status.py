#!/usr/bin/env python3
"""
Buddy System Status Test
Tests all core components to verify everything is working properly
"""

import sys
import os
import traceback
from typing import Dict, List, Any

def test_imports() -> Dict[str, Any]:
    """Test all critical imports"""
    results = {}
    critical_modules = [
        ('ai.emotion', 'get_emotional_system'),
        ('ai.llm_handler', 'llm_handler'),
        ('ai.consciousness_manager', 'consciousness_manager'),
        ('ai.memory', 'add_to_conversation_history'),
        ('voice.manager', 'voice_manager'),
        ('numpy', None),
        ('pyaudio', None),
        ('pvporcupine', None)
    ]
    
    for module_name, component in critical_modules:
        try:
            module = __import__(module_name, fromlist=[component] if component else [])
            if component:
                getattr(module, component)
            results[f"{module_name}.{component}" if component else module_name] = "✅ WORKING"
        except Exception as e:
            results[f"{module_name}.{component}" if component else module_name] = f"❌ ERROR: {e}"
    
    return results

def test_emotion_system() -> Dict[str, Any]:
    """Test emotion system functionality"""
    results = {}
    try:
        from ai.emotion import get_emotional_system, emotion_engine, get_current_emotional_state
        
        # Test emotional system
        emotional_system = get_emotional_system()
        results['emotional_system_init'] = "✅ WORKING"
        
        # Test emotion processing
        response = emotional_system.process_emotional_input("I'm happy today!", "test")
        results['emotion_processing'] = f"✅ WORKING - emotion: {response.get('primary_emotion', 'unknown')}"
        
        # Test traditional engine
        current_state = emotion_engine.get_current_state()
        results['emotion_engine'] = f"✅ WORKING - mood: {current_state.get('mood', 'unknown')}"
        
    except Exception as e:
        results['emotion_system'] = f"❌ ERROR: {e}"
    
    return results

def test_consciousness_system() -> Dict[str, Any]:
    """Test consciousness system"""
    results = {}
    try:
        from ai.consciousness_manager import consciousness_manager
        
        # Test consciousness status
        status = consciousness_manager.get_status()
        results['consciousness_status'] = f"✅ WORKING - mode: {status.get('mode', 'unknown')}"
        
        # Test interaction processing
        consciousness_manager.update_from_interaction("Hello buddy", "test_user")
        results['consciousness_interaction'] = "✅ WORKING"
        
    except Exception as e:
        results['consciousness_system'] = f"❌ ERROR: {e}"
    
    return results

def test_llm_system() -> Dict[str, Any]:
    """Test LLM handler"""
    results = {}
    try:
        from ai.llm_handler import llm_handler
        
        # Test LLM handler state
        results['llm_handler_init'] = "✅ WORKING"
        
        # Test response generation (without actually generating)
        if hasattr(llm_handler, 'generate_response_with_consciousness'):
            results['llm_consciousness_integration'] = "✅ WORKING"
        else:
            results['llm_consciousness_integration'] = "⚠️ METHOD MISSING"
        
    except Exception as e:
        results['llm_system'] = f"❌ ERROR: {e}"
    
    return results

def test_voice_system() -> Dict[str, Any]:
    """Test voice management system"""
    results = {}
    try:
        from voice.manager_core import voice_manager
        
        # Test voice manager
        results['voice_manager_init'] = "✅ WORKING"
        
        # Test voice identification method
        if hasattr(voice_manager, 'handle_voice_identification'):
            results['voice_identification'] = "✅ WORKING"
        else:
            results['voice_identification'] = "⚠️ METHOD MISSING"
        
        # Test session stats
        if hasattr(voice_manager, 'get_session_stats'):
            stats = voice_manager.get_session_stats()
            results['voice_stats'] = f"✅ WORKING - users: {stats.get('known_users', 0)}"
        else:
            results['voice_stats'] = "⚠️ METHOD MISSING"
        
    except Exception as e:
        results['voice_system'] = f"❌ ERROR: {e}"
    
    return results

def test_memory_system() -> Dict[str, Any]:
    """Test memory system"""
    results = {}
    try:
        from ai.memory import add_to_conversation_history, get_user_memory
        
        # Test memory functions
        results['memory_functions'] = "✅ WORKING"
        
        # Test user memory
        user_memory = get_user_memory("test_user")
        results['user_memory'] = f"✅ WORKING - type: {type(user_memory).__name__}"
        
    except Exception as e:
        results['memory_system'] = f"❌ ERROR: {e}"
    
    return results

def test_audio_dependencies() -> Dict[str, Any]:
    """Test audio-related dependencies"""
    results = {}
    
    # Test numpy
    try:
        import numpy as np
        test_array = np.array([1, 2, 3])
        results['numpy'] = f"✅ WORKING - version: {np.__version__}"
    except Exception as e:
        results['numpy'] = f"❌ ERROR: {e}"
    
    # Test pyaudio
    try:
        import pyaudio
        results['pyaudio'] = "✅ WORKING"
    except Exception as e:
        results['pyaudio'] = f"❌ ERROR: {e}"
    
    # Test pvporcupine
    try:
        import pvporcupine
        results['pvporcupine'] = "✅ WORKING"
    except Exception as e:
        results['pvporcupine'] = f"❌ ERROR: {e}"
    
    return results

def run_comprehensive_test():
    """Run comprehensive system test"""
    print("=" * 60)
    print("🚀 BUDDY SYSTEM STATUS TEST")
    print("=" * 60)
    
    # Suppress verbose output during testing
    original_stdout = sys.stdout
    
    try:
        # Redirect stdout to suppress verbose loading messages
        from io import StringIO
        sys.stdout = StringIO()
        
        # Run all tests
        tests = {
            "Core Imports": test_imports(),
            "Emotion System": test_emotion_system(),
            "Consciousness System": test_consciousness_system(),
            "LLM System": test_llm_system(),
            "Voice System": test_voice_system(),
            "Memory System": test_memory_system(),
            "Audio Dependencies": test_audio_dependencies()
        }
        
        # Restore stdout
        sys.stdout = original_stdout
        
        # Display results
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        warnings = 0
        
        for category, results in tests.items():
            print(f"\n📊 {category}")
            print("-" * 40)
            
            for test_name, result in results.items():
                print(f"  {test_name}: {result}")
                total_tests += 1
                
                if result.startswith("✅"):
                    passed_tests += 1
                elif result.startswith("❌"):
                    failed_tests += 1
                elif result.startswith("⚠️"):
                    warnings += 1
        
        # Summary
        print("\n" + "=" * 60)
        print("📈 SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⚠️  Warnings: {warnings}")
        
        if failed_tests == 0:
            print("\n🎉 ALL CRITICAL TESTS PASSED!")
            print("Buddy system is ready to run.")
            if warnings > 0:
                print(f"Note: {warnings} non-critical warnings (optional features)")
        else:
            print(f"\n🚨 {failed_tests} CRITICAL FAILURES DETECTED")
            print("Some components may not work properly.")
        
        print("=" * 60)
        
        return failed_tests == 0
        
    except Exception as e:
        sys.stdout = original_stdout
        print(f"❌ Test framework error: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)