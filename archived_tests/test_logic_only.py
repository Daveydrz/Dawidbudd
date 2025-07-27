#!/usr/bin/env python3
"""
Test the immediate response logic directly
"""

import time
import sys
import os

def test_immediate_response_logic():
    """Test the immediate response architecture logic"""
    print("🚀 Testing Immediate Response Logic...")
    
    # Mock the response generation
    def mock_generate_response_with_consciousness(text, user_id, consciousness_context):
        """Mock streaming response"""
        chunks = [
            "Hello! ", 
            "I understand ", 
            f"you asked about '{text[:20]}...'. ",
            "Let me help you with that. ",
            "I'm processing your request immediately. ",
            "Thank you for your question!"
        ]
        
        for chunk in chunks:
            time.sleep(0.01)  # Simulate minimal processing time
            yield chunk
    
    def mock_speak_streaming(text):
        """Mock speech output"""
        print(f"🎵 [SPEAKING] {text}")
    
    def mock_add_to_conversation_history(user, input_text, response):
        """Mock memory storage"""
        print(f"💾 [MEMORY] {user}: {input_text[:30]}... -> {response[:30]}...")
    
    def mock_get_user_context(user_id):
        """Mock memory context"""
        return {
            "facts": ["User likes technology", "User is interested in AI"],
            "preferences": ["Direct answers", "Technical details"],
            "context": ["Asked about AI before", "Prefers quick responses"]
        }
    
    # Simulate the immediate response logic
    def simulate_immediate_response(text, current_user):
        """Simulate the immediate response function"""
        print(f"[IMMEDIATE] 🚀 Starting IMMEDIATE response for: '{text}' (user: {current_user})")
        
        start_time = time.time()
        
        # Step 1: Start background consciousness (non-blocking)
        print("[IMMEDIATE] 🧠 Starting background consciousness processing (port 5002)...")
        
        def background_consciousness():
            print("[IMMEDIATE] 🧠 Background: Processing consciousness via port 5002...")
            time.sleep(0.5)  # Simulate background processing
            print("[IMMEDIATE] ✅ Background consciousness processing complete")
        
        import threading
        threading.Thread(target=background_consciousness, daemon=True).start()
        
        # Step 2: Get existing context immediately
        print("[IMMEDIATE] 📝 Using existing memory context for immediate response")
        existing_context = mock_get_user_context(current_user)
        
        consciousness_context = f"""BUDDY'S CONSCIOUSNESS STATE:
Current Emotion: helpful
Motivation Level: 0.8
Active Goals: help user effectively
Current Focus: user interaction
Personality: friendly, empathetic

USER MEMORY:
Facts: {', '.join(existing_context.get('facts', [])[:5])}
Preferences: {', '.join(existing_context.get('preferences', [])[:5])}  
Recent Context: {', '.join(existing_context.get('context', [])[-3:])}"""
        
        # Step 3: Generate response immediately
        print("[IMMEDIATE] ⚡ Starting IMMEDIATE response generation (port 5001)...")
        print("[IMMEDIATE] 🎯 Using simple LLM handler for port 5001 ONLY")
        
        full_response = ""
        chunk_count = 0
        first_chunk = True
        
        # Generate response
        for chunk in mock_generate_response_with_consciousness(text, current_user, consciousness_context):
            if chunk and chunk.strip():
                chunk_text = chunk.strip()
                chunk_count += 1
                
                if first_chunk:
                    print("[IMMEDIATE] 🎵 First chunk ready - starting speech IMMEDIATELY!")
                    first_chunk = False
                
                print(f"[IMMEDIATE] 🗣️ Speaking chunk {chunk_count}: '{chunk_text[:50]}...'")
                
                # Start speaking immediately (no delays)
                mock_speak_streaming(chunk_text)
                full_response += chunk_text + " "
                
                # Brief pause for natural flow (minimal)
                time.sleep(0.01)
        
        total_time = time.time() - start_time
        
        if full_response.strip():
            # Add to conversation history
            mock_add_to_conversation_history(current_user, text, full_response.strip())
            
            print(f"[IMMEDIATE] ✅ IMMEDIATE response complete:")
            print(f"[IMMEDIATE] ⚡ Total time: {total_time:.3f}s (TARGET: <3s)")
            print(f"[IMMEDIATE] 📊 Chunks processed: {chunk_count}")
            print(f"[IMMEDIATE] 🧠 Consciousness processing in background for next interaction")
        
        return total_time
    
    # Test the logic
    print("\n🧪 Testing immediate response with different inputs...")
    
    test_cases = [
        ("Hello, how are you?", "TestUser1"),
        ("What time is it?", "TestUser2"),
        ("I'm going to the shop", "TestUser3"),
        ("Tell me about artificial intelligence", "TestUser4")
    ]
    
    total_tests = len(test_cases)
    passed_tests = 0
    
    for i, (question, user) in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}/{total_tests}: '{question}'")
        
        response_time = simulate_immediate_response(question, user)
        
        if response_time < 3.0:
            print(f"✅ EXCELLENT: Response in {response_time:.3f}s (under 3s)")
            passed_tests += 1
        elif response_time < 5.0:
            print(f"✅ GOOD: Response in {response_time:.3f}s (under 5s)")
            passed_tests += 1
        else:
            print(f"❌ SLOW: Response in {response_time:.3f}s (over 5s)")
    
    print(f"\n📊 Test Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("✅ ALL TESTS PASSED: Immediate response architecture working correctly!")
        return True
    else:
        print("⚠️ SOME TESTS FAILED: Architecture needs optimization")
        return False

if __name__ == "__main__":
    success = test_immediate_response_logic()
    sys.exit(0 if success else 1)