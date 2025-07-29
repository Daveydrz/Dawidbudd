"""
Emergency Fast Response System
Created: 2025-01-17
Purpose: Provide immediate user responses by bypassing consciousness processing
         and moving all consciousness operations to background processing
"""

import time
from typing import Dict, Any, Generator, Optional

def generate_immediate_response(user_input: str, user_id: str) -> Generator[str, None, None]:
    """
    Generate immediate response bypassing all consciousness processing
    Target: <2 seconds response time
    """
    start_time = time.time()
    
    try:
        # ✅ EMERGENCY FAST PATH: Use simplest possible LLM call
        print("[FastResponse] ⚡ EMERGENCY FAST RESPONSE - bypassing all consciousness processing")
        
        # Try to use the most basic LLM system available
        try:
            from ai.chat import generate_response
            response = generate_response(
                f"You are Buddy. Respond naturally and helpfully to: {user_input}",
                user_id,
                "en"
            )
            
            # Split response into chunks for streaming
            words = response.split()
            chunk_size = 10  # 10 words per chunk
            
            for i in range(0, len(words), chunk_size):
                chunk = " ".join(words[i:i + chunk_size])
                yield chunk
                
        except ImportError:
            # Ultimate fallback if no LLM available
            yield f"I hear you asking: {user_input}. Let me help you with that."
            
        response_time = time.time() - start_time
        print(f"[FastResponse] ✅ Emergency response completed in {response_time:.3f}s")
        
    except Exception as e:
        print(f"[FastResponse] ❌ Emergency response error: {e}")
        yield f"I apologize, I'm having technical difficulties. You asked: {user_input}"

def schedule_background_consciousness_processing(user_input: str, user_id: str, context: Dict[str, Any] = None):
    """
    Schedule all consciousness processing for background execution
    This preserves Class 5+ consciousness without blocking user response
    """
    try:
        # Import background processor
        from ai.background_consciousness_processor import background_processor, BackgroundTask
        
        # Schedule all consciousness operations that were previously blocking
        tasks = [
            {
                "task_id": f"consciousness_{int(time.time())}",
                "task_type": "full_consciousness_integration", 
                "user_input": user_input,
                "user_id": user_id,
                "data": context or {},
                "priority": 2,  # Lower priority than immediate response
                "delay_seconds": 1.0  # 1 second delay to ensure response finishes first
            }
        ]
        
        # Add individual consciousness module tasks
        consciousness_tasks = [
            "emotion_processing",
            "motivation_evaluation", 
            "inner_monologue_generation",
            "subjective_experience_processing",
            "temporal_awareness_marking",
            "self_reflection",
            "entropy_processing",
            "global_workspace_attention"
        ]
        
        for task_type in consciousness_tasks:
            task = BackgroundTask(
                task_id=f"{task_type}_{int(time.time())}",
                task_type=task_type,
                user_input=user_input,
                user_id=user_id,
                data=context or {},
                priority=3,  # Background priority
                delay_seconds=2.0  # 2 second delay
            )
            background_processor.schedule_background_task(task)
            
        print(f"[FastResponse] 📋 Scheduled {len(consciousness_tasks)} background consciousness tasks")
        
    except Exception as e:
        print(f"[FastResponse] ⚠️ Error scheduling background consciousness: {e}")

def is_emergency_fast_mode_needed() -> bool:
    """
    Determine if emergency fast response mode should be used
    Always return True for now to fix the latency crisis
    """
    return True  # Emergency mode always enabled

def get_minimal_context_for_response(user_input: str, user_id: str) -> Dict[str, Any]:
    """
    Get absolutely minimal context needed for immediate response
    No LLM calls or heavy processing allowed
    """
    try:
        # Only basic static context that doesn't require processing
        return {
            "user_id": user_id,
            "input_length": len(user_input),
            "timestamp": time.time(),
            "mode": "emergency_fast"
        }
    except Exception as e:
        print(f"[FastResponse] ⚠️ Error getting minimal context: {e}")
        return {"mode": "emergency_fast"}