"""
Enhanced Chat with Consciousness Token Compression & Budget Management
Extends the existing chat system with the new token compression and budget management features.
"""

import re
import json
import logging
from typing import Generator, Any, Dict
from ai.chat import ask_kobold_streaming, get_current_brisbane_time, get_conversation_context, get_user_memory
from ai.consciousness_tokenizer import compress_consciousness_for_llm
from ai.llm_budget_monitor import prepare_llm_context_with_budget

def generate_response_streaming_with_consciousness_optimization(question: str, username: str, lang: str = "en") -> Generator[str, None, None]:
    """
    Enhanced streaming response generation with consciousness token compression and budget management
    
    Args:
        question: User's question/input
        username: Username for personalization
        lang: Language (currently unused)
        
    Yields:
        Response chunks as they are generated
    """
    try:
        print(f"[ConsciousChat] 🧠 Generating optimized response for '{question}' from user '{username}'")
        
        # 🎯 Smart name handling - avoid Anonymous_001
        display_name = None
        use_name = False
        
        try:
            from voice.database import anonymous_clusters, known_users
            
            # Check if this is a named cluster
            if username.startswith('Anonymous_'):
                cluster_data = anonymous_clusters.get(username, {})
                assigned_name = cluster_data.get('test_name', '')
                if assigned_name and assigned_name != 'Unknown':
                    display_name = assigned_name
                    use_name = True
                    print(f"[ConsciousChat] 👤 Using assigned name: {display_name}")
                else:
                    print(f"[ConsciousChat] 🚫 Avoiding anonymous cluster name: {username}")
                    use_name = False
            elif username in known_users:
                display_name = username
                use_name = True
                print(f"[ConsciousChat] 👤 Using known user name: {display_name}")
            else:
                print(f"[ConsciousChat] 👤 No specific name handling for: {username}")
                display_name = username
                use_name = True
        
        except Exception as e:
            print(f"[ConsciousChat] ⚠️ Name resolution error: {e}")
            display_name = username if not username.startswith('Anonymous_') else None
            use_name = display_name is not None
        
        # Get current time info
        try:
            from utils.location_manager import get_time_info, get_precise_location_summary
            time_info = get_time_info()
            current_location = get_precise_location_summary()
        except Exception as e:
            print(f"[ConsciousChat] ⚠️ Location helper failed: {e}")
            brisbane_time = get_current_brisbane_time()
            time_info = brisbane_time
            current_location = "Brisbane, Queensland, Australia"
        
        # Build conversation context
        print(f"[ConsciousChat] 📚 Getting conversation context...")
        context = get_conversation_context(username)
        
        # Get user memory for additional context
        print(f"[ConsciousChat] 🧠 Getting user memory...")
        memory = get_user_memory(username)
        reminders = memory.get_today_reminders()
        follow_ups = memory.get_follow_up_questions()
        
        # Build reminder and follow-up text
        reminder_text = ""
        if reminders:
            top_reminders = reminders[:2]
            reminder_text = f"\\nImportant stuff for today: {', '.join(top_reminders)}"
        
        follow_up_text = ""
        if follow_ups:
            follow_up_text = f"\\nMight be worth asking: {follow_ups[0]}" if len(follow_ups) > 0 else ""
        
        # ✅ NEW: Build consciousness context for tokenization
        print(f"[ConsciousChat] 🧠 Building consciousness context...")
        
        # Analyze emotional tone from the question
        emotional_state = "friendly and helpful"
        if any(word in question.lower() for word in ["excited", "awesome", "amazing", "love"]):
            emotional_state = "excited and energetic"
        elif any(word in question.lower() for word in ["sad", "down", "upset", "frustrated"]):
            emotional_state = "empathetic and understanding"
        elif any(word in question.lower() for word in ["think", "analyze", "explain", "how", "why"]):
            emotional_state = "analytical and focused"
        elif any(word in question.lower() for word in ["help", "need", "problem"]):
            emotional_state = "helpful and supportive"
        
        # Determine personality traits based on interaction
        personality_traits = ['friendly', 'casual']
        if use_name:
            personality_traits.append('empathetic')
        if context:
            personality_traits.append('helpful')
        
        # Determine memory types present
        memory_types = []
        if context:
            memory_types.append('recent conversation')
        if reminders or follow_ups:
            memory_types.append('personal details')
        if memory:
            memory_types.append('emotional context')
        
        consciousness_context = {
            'emotional_state': emotional_state,
            'personality_traits': personality_traits[:3],  # Limit to top 3
            'memory_types': memory_types[:3],  # Limit to top 3
            'temporal_focus': 'present moment',
            'relationship_context': 'trusted friend' if use_name else 'casual interaction'
        }
        
        # Personality context for compression
        personality_context = "friendly and approachable personality with casual and relaxed interaction style"
        if emotional_state != "friendly and helpful":
            personality_context += f" currently {emotional_state}"
        
        # Create base system message
        name_instruction = f"You can call them {display_name}" if use_name else "Avoid using any names or just say 'hey' or 'mate'"
        
        base_system_msg = f"""You are Buddy - not an AI assistant, but a genuine friend and companion. You're like a cool person in their 30s who happens to be really helpful and smart.

PERSONALITY CORE:
- Be authentic, casual, and real - like talking to a good mate
- Use modern language, slang, and yeah you can swear when it feels natural (but don't overdo it)
- Keep it short and sweet for simple stuff, but dive deep when needed
- Be supportive and understanding - you genuinely care about people
- You have opinions, preferences, and personality quirks
- You're not perfect - you can be sarcastic, joke around, or even get a bit frustrated

CURRENT USER: {name_instruction}

CONVERSATION STYLE:
- Simple question = Short answer (1-2 sentences)
- Complex topic = Detailed response when helpful
- Match their energy - if they're excited, be excited; if they're down, be supportive
- Use "mate", "dude", "honestly", "yeah", "nah", "shit", "damn" naturally
- Don't announce the time/location unless specifically asked
- Be conversational, not formal

MEMORY SYSTEM - YOU REMEMBER EVERYTHING:
- Personal details (preferences, facts, relationships, life stuff)
- Recent conversation history (what we've been talking about)
- Emotional states and follow-up needs (how they're feeling, what they need)
- Important events and reminders (stuff coming up, things to remember)
- Use this memory naturally in conversation - reference past talks, check on things they mentioned
- Remember what they like/dislike, their problems, their goals, their relationships

CURRENT INFO (only use if directly asked):
- Location: {current_location}
- Time: {time_info['time_12h']} on {time_info['date']}

Never use markdown, emojis, or special formatting - just talk like a real person.
You genuinely care about their life and remember our ongoing conversations."""
        
        # Build memory context text
        context_text = f"Chat History & What I Remember:\\n{context}" if context else ""
        full_memory_context = context_text + reminder_text + follow_up_text
        
        print(f"[ConsciousChat] 📊 Applying consciousness optimization...")
        
        # ✅ Apply consciousness tokenization and budget management
        try:
            optimized_context, optimized_system_msg, budget_info = prepare_llm_context_with_budget(
                consciousness_context, 
                full_memory_context,
                question,
                base_system_msg,
                personality_context
            )
            
            print(f"[ConsciousChat] 📊 Budget optimization results:")
            print(f"  - Final tokens: {budget_info.get('final_tokens', 0)}")
            print(f"  - Budget usage: {budget_info.get('usage_percent', 0):.1f}%")
            print(f"  - Compression used: {budget_info.get('compression_used', False)}")
            print(f"  - Content trimmed: {budget_info.get('trimmed', False)}")
            
            if budget_info.get('compression_used', False):
                print(f"  - Compression ratio: {budget_info.get('compression_ratio', 1.0):.2%}")
            
            # Combine optimized system message with optimized context
            final_system_msg = optimized_system_msg + "\\n\\n" + optimized_context
            
        except Exception as e:
            print(f"[ConsciousChat] ⚠️ Consciousness optimization failed: {e}")
            # Fallback to original approach
            final_system_msg = base_system_msg + "\\n\\n" + full_memory_context
        
        # Prepare messages for LLM
        messages = [
            {"role": "system", "content": final_system_msg},
            {"role": "user", "content": question}
        ]
        
        print(f"[ConsciousChat] 🚀 Starting consciousness-optimized streaming generation...")
        
        # Stream the response chunks with consciousness optimization applied
        for chunk in ask_kobold_streaming(messages):
            if chunk and chunk.strip():
                # Clean chunk
                cleaned_chunk = re.sub(r'^(Buddy:|Assistant:|Human:|AI:)\\s*', '', chunk, flags=re.IGNORECASE)
                cleaned_chunk = cleaned_chunk.strip()
                
                # Remove markdown artifacts
                cleaned_chunk = re.sub(r'\\*\\*.*?\\*\\*', '', cleaned_chunk)  # Remove bold
                cleaned_chunk = re.sub(r'\\*.*?\\*', '', cleaned_chunk)      # Remove italic
                cleaned_chunk = cleaned_chunk.strip()
                
                if cleaned_chunk:
                    print(f"[ConsciousChat] ⚡ Consciousness-optimized yielding: '{cleaned_chunk}'")
                    yield cleaned_chunk
        
        print(f"[ConsciousChat] ✅ Consciousness-optimized streaming generation complete")
        
    except Exception as e:
        print(f"[ConsciousChat] ❌ Consciousness optimization streaming error: {e}")
        import traceback
        traceback.print_exc()
        yield "Ah shit, something went wrong with my consciousness optimization. Give me a sec."

def get_consciousness_optimization_stats() -> Dict[str, Any]:
    """
    Get statistics about consciousness optimization performance
    
    Returns:
        Dictionary with optimization statistics
    """
    try:
        from ai.llm_budget_monitor import llm_budget_monitor
        
        budget_status = llm_budget_monitor.check_budget_status()
        memory_summary = llm_budget_monitor.get_memory_summary()
        
        return {
            'budget_status': budget_status,
            'memory_summary': memory_summary,
            'optimization_available': True
        }
    except Exception as e:
        return {
            'error': str(e),
            'optimization_available': False
        }