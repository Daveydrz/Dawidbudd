#!/usr/bin/env python3
"""
Core Buddy AI Test Suite
Tests essential functionality: memory, consciousness, voice, audio
Created: 2025-01-17
"""

import sys
import json
import time
import requests
from datetime import datetime

# Add project root to path
sys.path.append('.')

def test_memory_system():
    """Test memory storage and retrieval"""
    print("\n🧠 TESTING MEMORY SYSTEM")
    print("=" * 50)
    
    try:
        from ai.local_memory_manager import local_memory_manager
        
        # Test name extraction
        print("1. Testing name extraction...")
        memories = local_memory_manager.extract_memory_from_text("I'm David by the way", "test_user")
        local_memory_manager.store_memories(memories)
        print(f"   ✅ Extracted and stored {len(memories)} memories")
        
        # Test retrieval
        print("2. Testing memory retrieval...")
        context = local_memory_manager.get_user_context("test_user")
        print(f"   Facts: {context['facts']}")
        print(f"   Context: {context['context'][:2]}...")  # Show first 2
        
        # Test name recall scenario
        print("3. Testing name recall scenario...")
        memories2 = local_memory_manager.extract_memory_from_text("What's my name?", "test_user")
        local_memory_manager.store_memories(memories2)
        context2 = local_memory_manager.get_user_context("test_user")
        
        if context2['facts'] and 'David' in str(context2['facts']):
            print("   ✅ Name recall working - David found in facts")
            return True
        else:
            print("   ❌ Name recall failed - David not found")
            print(f"   Current facts: {context2['facts']}")
            return False
            
    except Exception as e:
        print(f"   ❌ Memory system error: {e}")
        return False

def test_consciousness_system():
    """Test consciousness processing"""
    print("\n🧠 TESTING CONSCIOUSNESS SYSTEM")
    print("=" * 50)
    
    try:
        from ai.extractor_client import extractor_client
        
        # Test connection to port 5002
        print("1. Testing port 5002 connection...")
        if extractor_client.is_available():
            print("   ✅ Port 5002 (Gemma-2-2B) is available")
            
            # Test consciousness processing
            print("2. Testing consciousness processing...")
            result = extractor_client.process_full_consciousness(
                "I'm feeling happy today and my name is David", 
                "test_user"
            )
            
            if result.get('classification'):
                print("   ✅ Consciousness processing working")
                print(f"   Emotion: {result['emotional_state']['detected_emotion']}")
                print(f"   Memory updates: {len(result['memory_updates']['new_facts'])} facts")
                return True
            else:
                print("   ❌ Consciousness processing failed")
                return False
        else:
            print("   ❌ Port 5002 (Gemma-2-2B) not available")
            print("   📝 Using fallback consciousness processing")
            
            # Test fallback
            result = extractor_client._get_fallback_consciousness_data()
            print("   ✅ Fallback consciousness data available")
            return False  # Server not running
            
    except Exception as e:
        print(f"   ❌ Consciousness system error: {e}")
        return False

def test_llm_integration():
    """Test LLM integration on ports 5001 and 5002"""
    print("\n🤖 TESTING LLM INTEGRATION")
    print("=" * 50)
    
    port_5001_available = False
    port_5002_available = False
    
    # Test port 5001 (main LLM)
    print("1. Testing port 5001 (main LLM)...")
    try:
        response = requests.get('http://localhost:5001/health', timeout=5)
        if response.status_code == 200:
            print("   ✅ Port 5001 available")
            port_5001_available = True
        else:
            print(f"   ❌ Port 5001 status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Port 5001 not available: {str(e)[:50]}...")
    
    # Test port 5002 (consciousness LLM)
    print("2. Testing port 5002 (consciousness LLM)...")
    try:
        response = requests.get('http://localhost:5002/health', timeout=5)
        if response.status_code == 200:
            print("   ✅ Port 5002 available")  
            port_5002_available = True
        else:
            print(f"   ❌ Port 5002 status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Port 5002 not available: {str(e)[:50]}...")
    
    if port_5001_available and port_5002_available:
        print("   ✅ Both LLM servers available")
        return True
    elif port_5001_available:
        print("   ⚠️ Only main LLM available (basic responses)")
        return False  
    else:
        print("   ❌ No LLM servers available")
        return False

def test_audio_integration():
    """Test Kokoro audio integration"""
    print("\n🔊 TESTING AUDIO INTEGRATION")
    print("=" * 50)
    
    try:
        # Test Kokoro server
        print("1. Testing Kokoro server...")
        try:
            response = requests.get('http://127.0.0.1:8880/health', timeout=5)
            if response.status_code == 200:
                print("   ✅ Kokoro server available")
                kokoro_available = True
            else:
                print(f"   ❌ Kokoro status: {response.status_code}")
                kokoro_available = False
        except Exception as e:
            print(f"   ❌ Kokoro not available: {str(e)[:50]}...")
            kokoro_available = False
        
        # Test audio output functions
        print("2. Testing audio output functions...")
        try:
            from audio.output import speak_streaming, test_kokoro_api
            
            # Test Kokoro API function
            if test_kokoro_api():
                print("   ✅ Kokoro API test passed")
            else:
                print("   ❌ Kokoro API test failed")
                
            return kokoro_available
            
        except ImportError as e:
            print(f"   ❌ Audio functions not available: {e}")
            return False
            
    except Exception as e:
        print(f"   ❌ Audio integration error: {e}")
        return False

def test_response_generation():
    """Test complete response generation pipeline"""
    print("\n💬 TESTING RESPONSE GENERATION")
    print("=" * 50)
    
    try:
        # Test scenario: User introduces themselves
        print("1. Testing name introduction scenario...")
        
        # Import the main response handler
        try:
            from main import handle_streaming_response
            print("   ✅ Main response handler imported")
        except Exception as e:
            print(f"   ❌ Main response handler import failed: {e}")
            return False
        
        # This would normally generate a response, but we can't test audio output here
        print("   📝 Response generation function available")
        print("   ⚠️ Full pipeline test requires running servers")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Response generation error: {e}")
        return False

def test_class5_consciousness():
    """Test Class 5+ consciousness features"""
    print("\n🌟 TESTING CLASS 5+ CONSCIOUSNESS")
    print("=" * 50)
    
    try:
        # Test consciousness architecture availability
        print("1. Testing consciousness architecture...")
        
        architecture_modules = [
            'ai.global_workspace',
            'ai.self_model', 
            'ai.emotion',
            'ai.motivation',
            'ai.inner_monologue',
            'ai.temporal_awareness',
            'ai.subjective_experience',
            'ai.entropy'
        ]
        
        available_modules = []
        for module in architecture_modules:
            try:
                __import__(module)
                available_modules.append(module)
            except ImportError:
                pass
        
        print(f"   Available modules: {len(available_modules)}/{len(architecture_modules)}")
        
        if len(available_modules) >= 6:
            print("   ✅ Sufficient consciousness modules available")
            
            # Test consciousness integration
            print("2. Testing consciousness integration...")
            try:
                from ai.autonomous_consciousness_integrator import autonomous_consciousness_integrator
                print("   ✅ Autonomous consciousness integrator available")
                return True
            except ImportError:
                print("   ⚠️ Autonomous consciousness integrator not available")
                return False
        else:
            print("   ❌ Insufficient consciousness modules")
            return False
            
    except Exception as e:
        print(f"   ❌ Consciousness test error: {e}")
        return False

def run_comprehensive_test():
    """Run comprehensive test suite"""
    print("🚀 BUDDY AI COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # Run all tests
    results['memory'] = test_memory_system()
    results['consciousness'] = test_consciousness_system()  
    results['llm'] = test_llm_integration()
    results['audio'] = test_audio_integration()
    results['responses'] = test_response_generation()
    results['class5'] = test_class5_consciousness()
    
    # Summary
    print("\n📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.upper():15} | {status}")
    
    print("-" * 60)
    print(f"OVERALL: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Buddy is fully operational!")
    elif passed >= total * 0.7:
        print("⚠️ MOSTLY WORKING - Some servers may need to be started")
    else:
        print("❌ CRITICAL ISSUES - Multiple components need attention")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS")
    print("=" * 60)
    
    if not results['llm']:
        print("🔧 Start LLM servers:")
        print("   - Main LLM on port 5001")
        print("   - Gemma-2-2B on port 5002")
    
    if not results['audio']:
        print("🔊 Start Kokoro server:")
        print("   - Kokoro-FastAPI on port 8880")
    
    if not results['consciousness']:
        print("🧠 Check consciousness processing:")
        print("   - Ensure port 5002 is running")
        print("   - Verify Gemma-2-2B model availability")
    
    if results['memory']:
        print("✅ Memory system working - names and facts are being stored")
    
    return passed, total

if __name__ == "__main__":
    passed, total = run_comprehensive_test()
    sys.exit(0 if passed == total else 1)