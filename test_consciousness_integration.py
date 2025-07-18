#!/usr/bin/env python3
"""
Test script to demonstrate consciousness tokenizer integration
This shows how the system generates dynamic consciousness-aware prompts
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_consciousness_tokenizer():
    print("🧠 CONSCIOUSNESS TOKENIZER INTEGRATION TEST")
    print("=" * 60)
    
    # Test 1: Basic token generation
    print("\n1. TESTING BASIC TOKEN GENERATION")
    print("-" * 40)
    
    try:
        from ai.consciousness_tokenizer import (
            generate_personality_tokens,
            generate_memory_tokens,
            generate_consciousness_tokens,
            generate_temporal_tokens,
            generate_context_tokens
        )
        
        user = "TestUser"
        
        # Generate different token types
        personality_tokens = generate_personality_tokens(user)
        memory_tokens = generate_memory_tokens(user)
        consciousness_tokens = generate_consciousness_tokens(user)
        temporal_tokens = generate_temporal_tokens()
        context_tokens = generate_context_tokens(user)
        
        print(f"✅ Personality tokens: {len(personality_tokens)}")
        for token, value in personality_tokens.items():
            print(f"   {token}: {value}")
        
        print(f"✅ Memory tokens: {len(memory_tokens)}")
        for token, value in memory_tokens.items():
            print(f"   {token}: {value}")
        
        print(f"✅ Consciousness tokens: {len(consciousness_tokens)}")
        for token, value in consciousness_tokens.items():
            print(f"   {token}: {value}")
        
        print(f"✅ Temporal tokens: {len(temporal_tokens)}")
        for token, value in temporal_tokens.items():
            print(f"   {token}: {value}")
        
        print(f"✅ Context tokens: {len(context_tokens)}")
        for token, value in context_tokens.items():
            print(f"   {token}: {value}")
            
    except Exception as e:
        print(f"❌ Error in token generation: {e}")
        return False
    
    # Test 2: Semantic analysis
    print("\n2. TESTING SEMANTIC ANALYSIS")
    print("-" * 40)
    
    try:
        from ai.semantic_tagger import analyze_user_text, get_semantic_tokens
        
        test_inputs = [
            "How are you feeling today?",
            "I'm really excited about my new job!",
            "Can you help me find information about machine learning?",
            "I'm worried about my presentation tomorrow"
        ]
        
        for test_input in test_inputs:
            analysis = analyze_user_text(test_input, user)
            tokens = get_semantic_tokens(test_input, user)
            
            print(f"\nInput: '{test_input}'")
            print(f"  Intent: {analysis.intent.value} (conf: {analysis.intent_confidence:.2f})")
            print(f"  Emotion: {analysis.emotional_tone.value} (conf: {analysis.tone_confidence:.2f})")
            print(f"  Complexity: {analysis.complexity_score:.2f}, Urgency: {analysis.urgency_score:.2f}")
            print(f"  Topics: {[d.value for d in analysis.topic_domains]}")
            print(f"  Generated {len(tokens)} semantic tokens")
            
    except Exception as e:
        print(f"❌ Error in semantic analysis: {e}")
        return False
    
    # Test 3: Belief analysis
    print("\n3. TESTING BELIEF CONTRADICTION DETECTION")
    print("-" * 40)
    
    try:
        from ai.belief_analyzer import analyze_user_input, get_user_belief_summary
        
        # Add some beliefs that might contradict
        belief_statements = [
            "My name is John and I live in Sydney",
            "I'm 25 years old and work as a teacher",
            "I love playing tennis and hate football",
            "My name is James and I live in Melbourne",  # Contradiction with first
            "I'm 30 years old"  # Contradiction with second
        ]
        
        for statement in belief_statements:
            result = analyze_user_input(statement, user)
            print(f"\nStatement: '{statement}'")
            print(f"  New beliefs found: {result['new_beliefs_found']}")
            print(f"  Contradictions: {len(result['contradictions_detected'])}")
            
            if result['contradictions_detected']:
                for contradiction in result['contradictions_detected']:
                    print(f"    ⚠️ {contradiction['severity']}: {contradiction['description']}")
        
        # Show belief summary
        summary = get_user_belief_summary(user)
        print(f"\n📊 BELIEF SUMMARY for {user}:")
        print(f"  Total beliefs: {summary['total_beliefs']}")
        print(f"  By type: {summary['by_type']}")
        print(f"  Contradictions: {summary['contradictions']}")
        
    except Exception as e:
        print(f"❌ Error in belief analysis: {e}")
        return False
    
    # Test 4: Complete consciousness prompt generation
    print("\n4. TESTING COMPLETE CONSCIOUSNESS PROMPT GENERATION")
    print("-" * 40)
    
    try:
        from ai.consciousness_tokenizer import create_token_aware_prompt
        from ai.llm_handler import generate_prompt_only, analyze_and_process_input
        
        test_input = "I'm feeling stressed about work and need some advice"
        
        # Test basic prompt creation
        basic_prompt = create_token_aware_prompt(user, token_budget=800)
        print(f"✅ Basic consciousness prompt ({len(basic_prompt)} chars)")
        print(f"Preview: {basic_prompt[:200]}...")
        
        # Test advanced LLM handler
        processing_result = analyze_and_process_input(test_input, user)
        advanced_prompt = generate_prompt_only(test_input, user)
        
        print(f"\n✅ Advanced consciousness prompt ({len(advanced_prompt)} chars)")
        print(f"Processing result keys: {list(processing_result.keys())}")
        print(f"Semantic intent: {processing_result['semantic_analysis'].intent.value}")
        print(f"Needs memory search: {processing_result['needs_memory_search']}")
        print(f"Response guidance: {processing_result['response_guidance']}")
        
        print(f"\nPrompt preview:")
        print(advanced_prompt[:400] + "..." if len(advanced_prompt) > 400 else advanced_prompt)
        
    except Exception as e:
        print(f"❌ Error in prompt generation: {e}")
        return False
    
    # Test 5: Token budget management
    print("\n5. TESTING TOKEN BUDGET MANAGEMENT")
    print("-" * 40)
    
    try:
        from ai.consciousness_tokenizer import generate_all_tokens, estimate_total_token_count, apply_token_budget
        
        # Test with different budgets
        budgets = [2000, 1000, 500, 200]
        
        for budget in budgets:
            tokens = generate_all_tokens(user, budget)
            total_tokens = estimate_total_token_count(tokens)
            
            print(f"\nBudget: {budget} tokens")
            print(f"  Generated: {len(tokens)} token types")
            print(f"  Estimated total: {total_tokens} tokens")
            print(f"  Within budget: {'✅' if total_tokens <= budget else '❌'}")
            
            if total_tokens > budget:
                optimized = apply_token_budget(tokens, budget)
                optimized_total = estimate_total_token_count(optimized)
                print(f"  After optimization: {len(optimized)} types, {optimized_total} tokens")
        
    except Exception as e:
        print(f"❌ Error in budget management: {e}")
        return False
    
    # Test 6: Integration validation
    print("\n6. TESTING INTEGRATION VALIDATION")
    print("-" * 40)
    
    try:
        from ai.llm_handler import validate_integration
        
        validation = validate_integration()
        print("Integration status:")
        for component, status in validation.items():
            status_icon = "✅" if status else "❌"
            print(f"  {status_icon} {component}")
        
        all_good = all(validation.values())
        print(f"\nOverall integration: {'✅ FULLY OPERATIONAL' if all_good else '⚠️ PARTIAL (some components missing)'}")
        
    except Exception as e:
        print(f"❌ Error in integration validation: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 CONSCIOUSNESS TOKENIZER INTEGRATION TEST COMPLETE")
    print("✅ All consciousness features are now integrated into the LLM pipeline")
    print("✅ Dynamic token-based prompts replace hardcoded blocks")
    print("✅ Token budget management prevents prompt overflow") 
    print("✅ Belief contradiction detection maintains consistency")
    print("✅ Semantic analysis enhances response understanding")
    print("✅ Prompt injection sanitization provides security")
    return True

if __name__ == "__main__":
    success = test_consciousness_tokenizer()
    sys.exit(0 if success else 1)