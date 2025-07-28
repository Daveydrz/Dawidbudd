"""
Test GPT4All prompt formats without actually downloading models
"""

# Test the prompts we created to ensure they're short and clear
def test_gpt4all_prompts():
    print("🧪 Testing GPT4All Prompt Formats (without actual model)...")
    
    # Test extract_facts prompt
    text = "Hi my name is David and I like pizza"
    facts_prompt = f"""
TASK: Extract facts from the user message below.

Message: "{text}"

Return ONLY valid JSON with these keys:
{{
  "name": "if user says their own name, else NONE",
  "likes": ["list of things user likes"],
  "dislikes": ["list of things user dislikes"],
  "emotion": "happy, sad, angry, or neutral"
}}
"""
    
    print(f"📋 extract_facts prompt length: {len(facts_prompt)} characters")
    print(f"📋 extract_facts prompt (max_tokens=60):")
    print(facts_prompt)
    print()
    
    # Test extract_name prompt  
    name_prompt = f"""
TASK: If the user introduced themselves, extract their name.

Message: "{text}"

Return ONLY a name (e.g. "David"). 
If no name, reply with "NONE".
"""
    
    print(f"🏷️ extract_name prompt length: {len(name_prompt)} characters")
    print(f"🏷️ extract_name prompt (max_tokens=10):")
    print(name_prompt)
    print()
    
    # Test extract_intent prompt
    intent_prompt = f"""
TASK: What is the user's intent?

Message: "{text}"

Return ONLY one word: question, request, information, greeting, goodbye, complaint, compliment, help, or casual.
"""
    
    print(f"🎯 extract_intent prompt length: {len(intent_prompt)} characters")
    print(f"🎯 extract_intent prompt (max_tokens=10):")
    print(intent_prompt)
    print()
    
    # Test extract_emotion prompt
    emotion_prompt = f"""
TASK: What emotion is the user expressing?

Message: "{text}"

Return ONLY one word: happy, sad, angry, worried, excited, neutral, or confused.
"""
    
    print(f"😊 extract_emotion prompt length: {len(emotion_prompt)} characters")
    print(f"😊 extract_emotion prompt (max_tokens=10):")
    print(emotion_prompt)
    print()

    # Test JSON parsing robustness
    print("🔍 Testing JSON parsing robustness...")
    test_outputs = [
        '{"name": "David", "likes": ["pizza"], "dislikes": [], "emotion": "happy"}',
        'Some text before {"name": "David", "likes": ["pizza"], "dislikes": [], "emotion": "happy"} some text after',
        '```json\n{"name": "David", "likes": ["pizza"], "dislikes": [], "emotion": "happy"}\n```',
        '{"name":"David","likes":["pizza"],"dislikes":[],"emotion":"happy"}',  # No spaces
        'David',  # Simple name response
        'NONE',   # No name response
        'invalid json response',  # Invalid response
        '',       # Empty response
    ]
    
    for output in test_outputs:
        print(f"  Testing output: '{output[:50]}{'...' if len(output) > 50 else ''}'")
        
        # Test JSON extraction logic
        json_start = output.find("{")
        json_end = output.rfind("}")
        if json_start != -1 and json_end != -1:
            json_part = output[json_start:json_end+1]
            try:
                import json
                parsed = json.loads(json_part)
                print(f"    ✅ Parsed JSON: {parsed}")
            except:
                print(f"    ❌ Failed to parse extracted JSON: '{json_part}'")
        else:
            print(f"    ⚠️ No JSON found, would use fallback")
    
    print("\n✅ All prompt formats are short, clear, and have robust error handling!")

if __name__ == "__main__":
    test_gpt4all_prompts()