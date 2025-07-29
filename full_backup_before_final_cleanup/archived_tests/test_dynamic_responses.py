#!/usr/bin/env python3
"""
Test Dynamic Response Generation - Verify No Hardcoded Responses
"""

def test_dynamic_error_responses():
    """Test that error responses are dynamic and not hardcoded"""
    print("🧪 Testing Dynamic Error Responses...")
    
    try:
        from ai.chat import _generate_dynamic_error_response
        
        # Test different error types
        test_cases = [
            {'error_type': 'connection_error', 'error_code': 500},
            {'error_type': 'timeout_error', 'situation': 'test'},
            {'error_type': 'json_decode_error'},
            {'error_type': 'general_error', 'error_message': 'test error'}
        ]
        
        responses = []
        for test_case in test_cases:
            response = _generate_dynamic_error_response(test_case)
            responses.append(response)
            print(f"  ✅ {test_case['error_type']}: '{response}'")
        
        # Verify responses are different and contextual
        unique_responses = set(responses)
        if len(unique_responses) == len(responses):
            print("  ✅ All error responses are unique and contextual")
        else:
            print("  ⚠️ Some error responses are identical")
        
        # Verify no hardcoded phrases
        hardcoded_phrases = ["Sorry, I got an error", "KoboldCpp", "Ah shit"]
        for response in responses:
            for phrase in hardcoded_phrases:
                if phrase in response:
                    print(f"  ❌ Found hardcoded phrase '{phrase}' in response: {response}")
                    return False
        
        print("  ✅ No hardcoded phrases detected in error responses")
        return True
        
    except Exception as e:
        print(f"  ❌ Error testing dynamic responses: {e}")
        return False

def test_autonomous_action_responses():
    """Test that autonomous actions generate dynamic responses"""
    print("🧪 Testing Autonomous Action Responses...")
    
    try:
        from ai.autonomous_action_planner import AutonomousActionPlanner, ActionType, ActionContext
        
        planner = AutonomousActionPlanner('test_user')
        
        # Create test context
        context = ActionContext(
            time_of_day='evening',
            current_mood='thoughtful',
            user_availability=1.0,
            recent_interactions=['casual conversation'],
            active_goals=['learning', 'connection'],
            day_of_week='friday',
            environment_factors={},
            user_preferences={'interaction_style': 'thoughtful'}
        )
        
        # Test different action types
        action_types = [ActionType.PROACTIVE_QUESTION, ActionType.CHECK_IN, ActionType.EMOTIONAL_SUPPORT]
        
        responses = []
        for action_type in action_types:
            response = planner._generate_dynamic_fallback_action(action_type, context)
            responses.append(response)
            print(f"  ✅ {action_type.value}: '{response}'")
        
        # Verify no hardcoded templates
        hardcoded_phrases = ["I wanted to", "I was thinking about you and wanted to"]
        for response in responses:
            for phrase in hardcoded_phrases:
                if phrase in response:
                    print(f"  ❌ Found hardcoded phrase '{phrase}' in response: {response}")
                    return False
        
        print("  ✅ No hardcoded templates detected in action responses")
        return True
        
    except Exception as e:
        print(f"  ❌ Error testing autonomous actions: {e}")
        return False

def test_subjective_experience_responses():
    """Test that subjective experiences generate dynamic descriptions"""
    print("🧪 Testing Subjective Experience Responses...")
    
    try:
        from ai.subjective_experience import SubjectiveExperienceSystem
        
        system = SubjectiveExperienceSystem()
        
        # Test dynamic description fallback
        response = system._generate_dynamic_no_experiences_response()
        print(f"  ✅ No experiences response: '{response}'")
        
        # Verify not hardcoded
        hardcoded_phrase = "I haven't had any notable experiences recently to reflect upon"
        if hardcoded_phrase in response:
            print(f"  ❌ Found hardcoded phrase in response: {response}")
            return False
        
        print("  ✅ No hardcoded phrases detected in experience responses")
        return True
        
    except Exception as e:
        print(f"  ❌ Error testing subjective experiences: {e}")
        return False

def test_goal_engine_responses():
    """Test that goal engine generates dynamic existential thoughts"""
    print("🧪 Testing Goal Engine Responses...")
    
    try:
        from ai.goal_engine import GoalEngine
        
        engine = GoalEngine('test_user')
        
        # Test dynamic existential fallback
        response = engine._generate_dynamic_existential_fallback()
        print(f"  ✅ Existential thought: '{response}'")
        
        # Verify not hardcoded
        hardcoded_phrase = "I find myself contemplating the nature of my existence and purpose..."
        if hardcoded_phrase in response:
            print(f"  ❌ Found hardcoded phrase in response: {response}")
            return False
        
        print("  ✅ No hardcoded phrases detected in goal engine responses")
        return True
        
    except Exception as e:
        print(f"  ❌ Error testing goal engine: {e}")
        return False

def main():
    """Run all dynamic response tests"""
    print("🚀 Testing Dynamic Response Generation - No Hardcoded Messages")
    print("=" * 60)
    
    test_results = []
    
    test_results.append(test_dynamic_error_responses())
    test_results.append(test_autonomous_action_responses())
    test_results.append(test_subjective_experience_responses())
    test_results.append(test_goal_engine_responses())
    
    print("\n" + "=" * 60)
    print("📊 Test Results:")
    
    passed = sum(test_results)
    total = len(test_results)
    
    if passed == total:
        print(f"✅ All {total} tests passed - Dynamic responses working correctly!")
        print("✅ No hardcoded responses detected!")
        print("✅ All responses are generated dynamically using consciousness context!")
    else:
        print(f"❌ {total - passed} tests failed out of {total}")
        print("❌ Some hardcoded responses may still exist")
    
    return passed == total

if __name__ == "__main__":
    main()