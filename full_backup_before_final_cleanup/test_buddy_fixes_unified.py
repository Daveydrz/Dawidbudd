#!/usr/bin/env python3
"""
Test Buddy Core Functionality - After Major Fixes
Tests the unified consciousness system, voice recognition, and memory
"""

import sys
import os

# Add the main directory to path
sys.path.insert(0, '/home/runner/work/Dawidbudd/Dawidbudd')

def test_imports():
    """Test that all core imports work"""
    print("=== Testing Core Imports ===")
    
    try:
        from ai.consciousness_manager import consciousness_manager, ConsciousnessMode
        print("✅ Consciousness manager imported")
        print(f"✅ Status: {consciousness_manager.get_status()}")
    except Exception as e:
        print(f"❌ Consciousness manager error: {e}")
    
    try:
        from ai.llm_handler import llm_handler
        print("✅ LLM handler imported")
    except Exception as e:
        print(f"❌ LLM handler error: {e}")
    
    try:
        from ai.extractor_client import extractor_client
        print("✅ Extractor client imported")
    except Exception as e:
        print(f"❌ Extractor client error: {e}")
    
    try:
        from voice.recognition import identify_speaker_with_confidence
        from voice.database import known_users, anonymous_clusters
        print("✅ Voice recognition imported")
        print(f"✅ Voice DB: {len(known_users)} users, {len(anonymous_clusters)} clusters")
    except Exception as e:
        print(f"❌ Voice recognition error: {e}")
    
    try:
        from ai.memory import add_to_conversation_history
        print("✅ Memory system imported")
    except Exception as e:
        print(f"❌ Memory system error: {e}")

def test_consciousness_system():
    """Test consciousness manager functionality"""
    print("\n=== Testing Consciousness System ===")
    
    try:
        from ai.consciousness_manager import consciousness_manager, ConsciousnessMode
        
        # Test mode setting
        consciousness_manager.set_mode(ConsciousnessMode.ACTIVE)
        print("✅ Mode setting works")
        
        # Test interaction update
        consciousness_manager.update_from_interaction("Hello, I'm David", "Hi David!")
        print("✅ Interaction update works")
        
        # Test consciousness context generation
        context = consciousness_manager.get_consciousness_context_for_llm()
        print(f"✅ Consciousness context generated: {len(context)} fields")
        
        # Test status
        status = consciousness_manager.get_status()
        print(f"✅ Status: Running={status['is_running']}, Mode={status['mode']}")
        
    except Exception as e:
        print(f"❌ Consciousness system error: {e}")
        import traceback
        traceback.print_exc()

def test_voice_recognition():
    """Test voice recognition system"""
    print("\n=== Testing Voice Recognition ===")
    
    try:
        from voice.database import load_known_users, known_users, anonymous_clusters
        load_known_users()
        
        print(f"✅ Database loaded: {len(known_users)} known users")
        print(f"✅ Anonymous clusters: {len(anonymous_clusters)}")
        
        # List current clusters/users
        if anonymous_clusters:
            print("🔍 Current anonymous clusters:")
            for cluster_id, data in list(anonymous_clusters.items())[:3]:
                print(f"  - {cluster_id}: {data.get('sample_count', 0)} samples")
        
        if known_users:
            print("👤 Known users:")
            for user_id in list(known_users.keys())[:3]:
                print(f"  - {user_id}")
    
    except Exception as e:
        print(f"❌ Voice recognition error: {e}")

def test_memory_system():
    """Test memory system"""
    print("\n=== Testing Memory System ===")
    
    try:
        from ai.memory import add_to_conversation_history
        
        # Test adding a conversation
        add_to_conversation_history("TestUser", "Hello, my name is Alice", "Nice to meet you Alice!")
        print("✅ Memory system can save conversations")
        
    except Exception as e:
        print(f"❌ Memory system error: {e}")

def test_extractor_client():
    """Test consciousness processing"""
    print("\n=== Testing Consciousness Processing ===")
    
    try:
        from ai.extractor_client import extractor_client, get_consciousness_for_prompt
        
        # Test consciousness processing (should use local fallback if port 5002 offline)
        result = extractor_client.process_full_consciousness("Hello, I'm David", "TestUser")
        print(f"✅ Consciousness processing works: {len(result)} sections")
        
        # Test prompt generation
        prompt_context = get_consciousness_for_prompt("TestUser")
        print(f"✅ Consciousness prompt generated: {len(prompt_context)} chars")
        
    except Exception as e:
        print(f"❌ Consciousness processing error: {e}")

def main():
    """Run all tests"""
    print("🧪 Testing Buddy Core Functionality After Major Fixes")
    print("=" * 60)
    
    test_imports()
    test_consciousness_system()
    test_voice_recognition()
    test_memory_system()
    test_extractor_client()
    
    print("\n" + "=" * 60)
    print("✅ Testing complete! Check for any ❌ errors above.")

if __name__ == "__main__":
    main()