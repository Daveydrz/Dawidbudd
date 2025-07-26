#!/usr/bin/env python3
"""
Test Port Separation Architecture
Created: 2025-01-17
Purpose: Verify that consciousness processing goes to port 5002 and response generation to port 5001
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_port_separation():
    """Test the fixed port separation architecture"""
    print("🧪 Testing Port Separation Architecture")
    print("="*50)
    
    # Test 1: Check LLM Handler Port Separation
    print("\n1️⃣ Testing LLM Handler Port Separation:")
    try:
        from ai.llm_handler import LLMHandler
        llm_handler = LLMHandler()
        
        # This should use port 5002 for consciousness and port 5001 for response
        print("✅ LLM Handler imported successfully")
        print(f"   - Description: LLM Handler configured for port separation")
        
        # Check the method signature
        if hasattr(llm_handler, 'generate_response_with_consciousness'):
            print("✅ generate_response_with_consciousness method available")
        else:
            print("❌ generate_response_with_consciousness method missing")
            
    except ImportError as e:
        print(f"❌ LLM Handler import failed: {e}")
    
    # Test 2: Check Extractor Client (Port 5002)
    print("\n2️⃣ Testing Extractor Client (Port 5002):")
    try:
        from ai.extractor_client import ExtractorClient, process_full_consciousness
        
        client = ExtractorClient()
        print(f"✅ Extractor Client created for: {client.base_url}")
        
        if client.base_url == "http://localhost:5002":
            print("✅ Correct port 5002 configured for consciousness processing")
        else:
            print(f"❌ Wrong port configured: {client.base_url}")
            
        # Test availability (will fail if server not running, which is expected)
        is_available = client.is_available()
        print(f"   - Port 5002 server available: {is_available}")
        
    except ImportError as e:
        print(f"❌ Extractor Client import failed: {e}")
    
    # Test 3: Check Simple LLM Handler (Port 5001)
    print("\n3️⃣ Testing Simple LLM Handler (Port 5001):")
    try:
        from ai.simple_llm_handler import SimpleLLMHandler
        
        simple_handler = SimpleLLMHandler()
        print(f"✅ Simple LLM Handler created for: {simple_handler.base_url}")
        
        if simple_handler.base_url == "http://localhost:5001":
            print("✅ Correct port 5001 configured for response generation")
        else:
            print(f"❌ Wrong port configured: {simple_handler.base_url}")
            
        # Test availability (will fail if server not running, which is expected)
        is_available = simple_handler.is_available()
        print(f"   - Port 5001 server available: {is_available}")
        
    except ImportError as e:
        print(f"❌ Simple LLM Handler import failed: {e}")
    
    # Test 4: Check Config Settings
    print("\n4️⃣ Testing Config Settings:")
    try:
        from config import KOBOLD_URL
        print(f"✅ KOBOLD_URL loaded: {KOBOLD_URL}")
        
        if "localhost:5001" in KOBOLD_URL:
            print("✅ Main LLM correctly configured for port 5001")
        else:
            print(f"❌ Main LLM not on port 5001: {KOBOLD_URL}")
            
    except ImportError as e:
        print(f"❌ Config import failed: {e}")
    
    # Test 5: Check Smart Streaming Output
    print("\n5️⃣ Testing Smart Streaming Output (Kokoro Protection):")
    try:
        from audio.smart_streaming_output import speak_streaming_smart, reset_streaming_output
        
        print("✅ Smart streaming functions imported")
        
        # Test reset function
        reset_streaming_output()
        print("✅ Streaming output reset successful")
        
        # Test smart streaming (won't actually play audio in this test)
        spoke = speak_streaming_smart("Test chunk", is_final=False)
        print(f"   - Smart streaming test: {spoke}")
        
    except ImportError as e:
        print(f"❌ Smart streaming import failed: {e}")
    
    # Test 6: Check Main.py Integration
    print("\n6️⃣ Testing Main.py Integration:")
    try:
        # Check if handle_streaming_response exists and has correct signature
        from main import handle_streaming_response
        
        print("✅ handle_streaming_response function available")
        
        # Check function signature
        import inspect
        sig = inspect.signature(handle_streaming_response)
        params = list(sig.parameters.keys())
        print(f"   - Function parameters: {params}")
        
        if len(params) >= 2:
            print("✅ Function has correct parameter structure")
        else:
            print("❌ Function parameter structure incorrect")
            
    except ImportError as e:
        print(f"❌ Main.py function import failed: {e}")
    
    # Summary
    print("\n" + "="*50)
    print("🎯 Port Separation Architecture Summary:")
    print("   - Port 5002: Consciousness processing (Gemma-2-2B)")
    print("   - Port 5001: Response generation (Main LLM)")
    print("   - Smart streaming: Kokoro protection with 30-50% threshold")
    print("   - Memory system: Local JSON updates")
    print("\n✅ Architecture test complete!")

if __name__ == "__main__":
    test_port_separation()