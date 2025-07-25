#!/usr/bin/env python3
"""
Test Connection Fixes for WinError 10053
Tests both streaming and non-streaming requests to verify fixes
"""

import time
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_connection_fixes():
    """Test the connection fixes for WinError 10053"""
    print("🧪 Testing Connection Fixes for WinError 10053")
    print("=" * 60)
    
    try:
        # Import chat functions
        from ai.chat import ask_kobold, ask_kobold_streaming
        print("✅ Successfully imported chat functions")
        
        # Test non-streaming request (used by inner monologue)
        print("\n🔄 Testing non-streaming request...")
        test_messages = [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": "Hello, how are you today?"}
        ]
        
        start_time = time.time()
        try:
            response = ask_kobold(test_messages, max_tokens=50)
            duration = time.time() - start_time
            print(f"✅ Non-streaming request successful in {duration:.2f}s")
            print(f"📝 Response: {response[:100]}..." if len(response) > 100 else f"📝 Response: {response}")
        except Exception as e:
            print(f"❌ Non-streaming request failed: {e}")
            return False
        
        # Test streaming request (used by main responses)
        print("\n🌊 Testing streaming request...")
        start_time = time.time()
        response_chunks = []
        
        try:
            for chunk in ask_kobold_streaming(test_messages, max_tokens=50):
                response_chunks.append(chunk)
                print(f"📦 Chunk: {chunk}")
                
                # Break after reasonable number of chunks for testing
                if len(response_chunks) >= 5:
                    break
            
            duration = time.time() - start_time
            full_response = " ".join(response_chunks)
            print(f"✅ Streaming request successful in {duration:.2f}s")
            print(f"📝 Full response: {full_response}")
            
        except Exception as e:
            print(f"❌ Streaming request failed: {e}")
            return False
        
        print("\n🎉 All connection tests passed!")
        print("🔧 WinError 10053 fixes appear to be working correctly")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_session_handling():
    """Test the persistent session handling"""
    print("\n🔗 Testing Session Handling")
    print("-" * 30)
    
    try:
        from ai.chat import session
        print(f"✅ Session created: {session}")
        print(f"📋 Session headers: {dict(session.headers)}")
        
        # Test multiple requests with same session
        print("🔄 Testing multiple requests with persistent session...")
        
        from ai.chat import ask_kobold
        test_messages = [
            {"role": "system", "content": "Respond briefly."},
            {"role": "user", "content": "Test 1"}
        ]
        
        for i in range(3):
            try:
                response = ask_kobold(test_messages, max_tokens=20)
                print(f"✅ Request {i+1} successful: {response[:50]}...")
            except Exception as e:
                print(f"❌ Request {i+1} failed: {e}")
                return False
        
        print("✅ Session handling working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Session handling test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Connection Fix Tests")
    
    # Test connection fixes
    connection_test = test_connection_fixes()
    
    # Test session handling
    session_test = test_session_handling()
    
    if connection_test and session_test:
        print("\n🎉 ALL TESTS PASSED")
        print("🔧 WinError 10053 fixes are working correctly")
        sys.exit(0)
    else:
        print("\n❌ SOME TESTS FAILED")
        print("🔧 Connection fixes may need additional work")
        sys.exit(1)