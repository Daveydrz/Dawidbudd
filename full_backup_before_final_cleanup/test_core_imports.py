#!/usr/bin/env python3
"""
Test core imports without audio dependencies
"""

print("Testing core imports...")

try:
    from ai.emotion import reset_session_for_user_smart
    print("✅ reset_session_for_user_smart imported successfully")
except Exception as e:
    print(f"❌ reset_session_for_user_smart import failed: {e}")

try:
    from ai.extractor_llm import extract_facts
    result = extract_facts("My name is John and I like pizza")
    print(f"✅ extract_facts works: {result}")
except Exception as e:
    print(f"❌ extract_facts failed: {e}")

try:
    from ai.consciousness_manager import consciousness_manager
    print("✅ consciousness_manager imported successfully")
except Exception as e:
    print(f"❌ consciousness_manager import failed: {e}")

try:
    from ai.llm_handler import llm_handler
    print("✅ llm_handler imported successfully")
except Exception as e:
    print(f"❌ llm_handler import failed: {e}")

print("Core imports test completed.")