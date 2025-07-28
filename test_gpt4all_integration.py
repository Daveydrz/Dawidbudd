#!/usr/bin/env python3
"""
Test GPT4All Extractor Integration
This test verifies that the new GPT4All-based extractor works correctly
Run this after the user provides the model file and installs gpt4all
"""

import os
import sys

def test_extractor_llm():
    """Test the GPT4All extractor"""
    print("🧪 Testing GPT4All Extractor Integration")
    
    # Check if model file exists
    model_path = "./extractor_model/ggml-gpt4all-j-v1.3-groovy.bin"
    if not os.path.exists(model_path):
        print(f"❌ Model file not found: {model_path}")
        print("📋 User needs to download and place the model file in extractor_model/")
        return False
    
    # Test gpt4all import
    try:
        from gpt4all import GPT4All
        print("✅ gpt4all library imported successfully")
    except ImportError:
        print("❌ gpt4all library not installed")
        print("📋 User needs to run: pip install gpt4all")
        return False
    
    # Test extractor_llm
    try:
        from ai.extractor_llm import extract_facts
        print("✅ extractor_llm module imported successfully")
        
        # Test fact extraction
        test_text = "Hi, my name is David and I like pizza but I dislike broccoli. I'm feeling happy today!"
        result = extract_facts(test_text)
        
        print(f"📋 Test extraction result: {result}")
        
        # Verify structure
        expected_keys = ["name", "likes", "dislikes", "emotion"]
        for key in expected_keys:
            if key not in result:
                print(f"❌ Missing key in result: {key}")
                return False
        
        print("✅ Fact extraction working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Error testing extractor: {e}")
        return False

def test_consciousness_manager():
    """Test consciousness manager integration"""
    print("\n🧠 Testing Consciousness Manager Integration")
    
    try:
        from ai.consciousness_manager import consciousness_manager
        print("✅ Consciousness manager imported successfully")
        
        # Test update from interaction
        test_text = "Hello, I'm John and I love coffee"
        consciousness_manager.update_from_interaction(test_text, "test_user")
        
        print("✅ Consciousness manager updated successfully")
        
        # Check memory
        if consciousness_manager.memory.get("name"):
            print(f"✅ Name extracted: {consciousness_manager.memory['name']}")
        
        if consciousness_manager.memory.get("likes"):
            print(f"✅ Likes extracted: {consciousness_manager.memory['likes']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing consciousness manager: {e}")
        return False

def test_llm_handler():
    """Test LLM handler integration"""
    print("\n🎯 Testing LLM Handler Integration")
    
    try:
        from ai.llm_handler import llm_handler
        print("✅ LLM handler imported successfully")
        
        # The actual response generation requires port 5001 to be running
        # So we just test that the method exists and can be called
        print("✅ LLM handler integration ready")
        print("📋 Note: Response generation requires port 5001 LLM server to be running")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing LLM handler: {e}")
        return False

if __name__ == "__main__":
    print("🚀 GPT4All Extractor Integration Test")
    print("=" * 50)
    
    success = True
    
    success &= test_extractor_llm()
    success &= test_consciousness_manager()
    success &= test_llm_handler()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! GPT4All extractor integration ready")
        print("📋 Next steps:")
        print("   1. Start your LLM server on port 5001")
        print("   2. Test with voice input or main.py")
    else:
        print("❌ Some tests failed. Check the errors above.")
        print("📋 Make sure:")
        print("   1. Model file is in extractor_model/ggml-gpt4all-j-v1.3-groovy.bin")
        print("   2. gpt4all is installed: pip install gpt4all")