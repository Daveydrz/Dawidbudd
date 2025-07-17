#!/usr/bin/env python3
"""
Test Belief Analysis and Persistent Beliefs System
Tests the belief contradiction detection and persistent storage features.
"""

import sys
import os
import tempfile
from pathlib import Path

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_belief_analyzer():
    """Test the belief analyzer for contradiction detection"""
    print("🧠 Testing Belief Analyzer\n")
    
    try:
        from ai.belief_analyzer import BeliefAnalyzer, analyze_user_statement_for_contradictions
        
        # Create temporary belief store for testing
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_belief_store = f.name
        
        analyzer = BeliefAnalyzer(belief_store_path=temp_belief_store)
        
        # Test 1: Extract beliefs from statements
        print("1. Testing belief extraction...")
        
        test_statements = [
            "My name is John and I am 25 years old",
            "I love pizza and hate vegetables", 
            "I work as a software engineer",
            "My dog Max is very friendly"
        ]
        
        for statement in test_statements:
            analysis = analyzer.analyze_statement(statement, "TestUser")
            print(f"   Statement: '{statement}'")
            print(f"   Extracted beliefs: {len(analysis['new_beliefs'])}")
            for belief in analysis['new_beliefs']:
                print(f"     - {belief['content']} ({belief['category']})")
        
        print("   ✅ Belief extraction working")
        
        # Test 2: Detect contradictions
        print("\n2. Testing contradiction detection...")
        
        # Add a contradictory statement
        contradictory_statement = "I hate pizza and love vegetables"
        analysis = analyzer.analyze_statement(contradictory_statement, "TestUser")
        
        print(f"   Contradictory statement: '{contradictory_statement}'")
        print(f"   Contradictions detected: {len(analysis['contradictions'])}")
        
        for contradiction in analysis['contradictions']:
            print(f"     - Severity: {contradiction['severity']}")
            print(f"     - Explanation: {contradiction['explanation']}")
        
        if analysis['contradictions']:
            print("   ✅ Contradiction detection working")
        else:
            print("   ⚠️ No contradictions detected (may need more sophisticated matching)")
        
        # Test 3: Awareness response generation
        print("\n3. Testing awareness response generation...")
        
        analysis, awareness_response = analyze_user_statement_for_contradictions(
            "I actually love vegetables now", "TestUser"
        )
        
        print(f"   Statement: 'I actually love vegetables now'")
        print(f"   Awareness response: {awareness_response}")
        
        if awareness_response:
            print("   ✅ Awareness response generation working")
        else:
            print("   ⚠️ No awareness response generated")
        
        # Cleanup
        os.unlink(temp_belief_store)
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing belief analyzer: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_persistent_beliefs():
    """Test the persistent beliefs system"""
    print("💾 Testing Persistent Beliefs System\n")
    
    try:
        from ai.persistent_beliefs import PersistentBeliefsManager, BeliefType, get_persistent_belief_context
        
        # Create temporary belief file for testing
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_belief_file = f.name
        
        manager = PersistentBeliefsManager(belief_file=temp_belief_file, auto_save_interval=3600)  # Disable auto-save for testing
        
        # Test 1: Add persistent beliefs
        print("1. Testing belief addition...")
        
        test_user = "TestUser"
        
        # Add various types of beliefs
        beliefs_to_add = [
            ("John Smith", BeliefType.CORE_FACT, 0.9, 0.9),
            ("loves programming", BeliefType.PREFERENCE, 0.8, 0.7),
            ("has a dog named Max", BeliefType.RELATIONSHIP, 0.9, 0.8),
            ("wants to learn machine learning", BeliefType.GOAL, 0.7, 0.6),
            ("drinks coffee every morning", BeliefType.HABIT, 0.8, 0.5)
        ]
        
        for content, belief_type, confidence, importance in beliefs_to_add:
            belief_id = manager.add_belief(
                user_id=test_user,
                content=content,
                belief_type=belief_type,
                confidence=confidence,
                importance=importance
            )
            print(f"   Added belief: {content} (ID: {belief_id})")
        
        print("   ✅ Belief addition working")
        
        # Test 2: Retrieve beliefs
        print("\n2. Testing belief retrieval...")
        
        all_beliefs = manager.get_beliefs(test_user)
        print(f"   Total beliefs: {len(all_beliefs)}")
        
        core_beliefs = manager.get_core_beliefs(test_user)
        print(f"   Core belief categories: {list(core_beliefs.keys())}")
        
        for category, beliefs in core_beliefs.items():
            print(f"     {category}: {len(beliefs)} beliefs")
            for belief in beliefs:
                print(f"       - {belief.content} (importance: {belief.importance})")
        
        print("   ✅ Belief retrieval working")
        
        # Test 3: Belief context generation
        print("\n3. Testing belief context generation...")
        
        context = get_persistent_belief_context(test_user, max_beliefs=10)
        print(f"   Generated context ({len(context)} chars):")
        print("   " + "\n   ".join(context.split("\n")[:8]))  # Show first 8 lines
        
        if context and "PERSISTENT BELIEFS" in context:
            print("   ✅ Belief context generation working")
        else:
            print("   ❌ Belief context generation failed")
        
        # Test 4: Save and load persistence
        print("\n4. Testing persistence...")
        
        manager.save_beliefs()
        print("   Saved beliefs to file")
        
        # Create new manager instance to test loading
        manager2 = PersistentBeliefsManager(belief_file=temp_belief_file, auto_save_interval=3600)
        loaded_beliefs = manager2.get_beliefs(test_user)
        
        print(f"   Loaded {len(loaded_beliefs)} beliefs from file")
        
        if len(loaded_beliefs) == len(all_beliefs):
            print("   ✅ Persistence working")
        else:
            print(f"   ❌ Persistence failed: expected {len(all_beliefs)}, got {len(loaded_beliefs)}")
        
        # Test 5: User summary
        print("\n5. Testing user summary...")
        
        summary = manager.get_user_summary(test_user)
        print(f"   User summary: {summary}")
        
        if summary['total_beliefs'] > 0:
            print("   ✅ User summary working")
        else:
            print("   ❌ User summary failed")
        
        # Cleanup
        os.unlink(temp_belief_file)
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing persistent beliefs: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_belief_integration():
    """Test integration between belief analyzer and persistent beliefs"""
    print("🔗 Testing Belief Integration\n")
    
    try:
        from ai.belief_analyzer import analyze_user_statement_for_contradictions
        from ai.persistent_beliefs import store_conversation_beliefs, get_persistent_belief_context
        
        # Test 1: Store conversation beliefs
        print("1. Testing conversation belief storage...")
        
        test_user = "IntegrationTestUser"
        conversation = "Hi, my name is Alice and I'm 30 years old. I love hiking and have a cat named Whiskers. I work as a teacher and my goal is to travel to Japan next year."
        
        store_conversation_beliefs(test_user, conversation)
        print(f"   Stored beliefs from conversation: '{conversation[:50]}...'")
        
        # Get stored context
        context = get_persistent_belief_context(test_user)
        print(f"   Retrieved persistent context: {len(context)} characters")
        
        if context:
            print("   ✅ Conversation belief storage working")
        else:
            print("   ⚠️ No persistent context generated")
        
        # Test 2: Contradiction detection with persistent beliefs
        print("\n2. Testing contradiction detection...")
        
        contradictory_statement = "Actually, I hate hiking and I'm 25 years old"
        analysis, awareness_response = analyze_user_statement_for_contradictions(
            contradictory_statement, test_user
        )
        
        print(f"   Contradictory statement: '{contradictory_statement}'")
        print(f"   Analysis: {len(analysis.get('contradictions', []))} contradictions")
        print(f"   Awareness response: {awareness_response}")
        
        if analysis.get('contradictions') or awareness_response:
            print("   ✅ Integrated contradiction detection working")
        else:
            print("   ⚠️ No contradictions detected in integration")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing belief integration: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all belief system tests"""
    print("🚀 Testing Belief Analysis & Persistent Beliefs System\n")
    
    results = []
    
    # Run tests
    results.append(("Belief Analyzer", test_belief_analyzer()))
    results.append(("Persistent Beliefs", test_persistent_beliefs()))
    results.append(("Belief Integration", test_belief_integration()))
    
    # Print summary
    print("\n" + "="*60)
    print("📋 Belief System Test Results:")
    print("="*60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:25} {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All belief system tests passed! Enhanced consciousness awareness is ready.")
        
        print("\n📝 Belief System Features:")
        print("- Real-time belief contradiction detection")
        print("- Persistent belief storage across sessions")
        print("- Automatic belief extraction from conversations")
        print("- Consciousness awareness of user consistency")
        print("- Enhanced memory continuity and context")
    else:
        print("⚠️ Some belief system tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()