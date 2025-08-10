# ai/chat_enhanced_smart_with_fusion.py - Enhanced chat with intelligent memory fusion
from ai.human_memory_smart import SmartHumanLikeMemory
from ai.chat import generate_response_streaming
from ai.memory_fusion_intelligent import get_intelligent_unified_username
import random

# ✅ ENTROPY SYSTEM: Import consciousness emergence components
try:
    from ai.entropy_engine import get_entropy_engine, probabilistic_select, inject_consciousness_entropy, EntropyLevel
    from ai.emotion import get_emotional_system, process_emotional_context
    print("[ChatFusion] 🌀 Entropy system integrated for consciousness emergence")
    ENTROPY_AVAILABLE = True
except ImportError as e:
    print(f"[ChatFusion] ⚠️ Entropy system not available: {e}")
    ENTROPY_AVAILABLE = False

# Global memory instances
smart_memories = {}

def get_smart_memory(username: str) -> SmartHumanLikeMemory:
    """Get or create smart memory for user"""
    if username not in smart_memories:
        smart_memories[username] = SmartHumanLikeMemory(username)
    return smart_memories[username]

def generate_response_streaming_with_intelligent_fusion(question: str, username: str, lang="en"):
    """🧠 Generate response with intelligent memory fusion, smart memory + CONSCIOUSNESS ENTROPY + TOKEN OPTIMIZATION"""
    
    # ✅ TOKEN OPTIMIZATION: Initialize optimization settings
    try:
        from ai.llm_budget_monitor import get_budget_status
        from ai.consciousness_tokenizer import get_consciousness_summary_for_llm
        
        budget_status = get_budget_status()
        usage_percentage = budget_status.get("daily_usage_percentage", 0.0)
        
        # Determine optimization level based on usage
        if usage_percentage > 0.8:
            optimization_level = "ultra"  # 85% token reduction
            print(f"[ChatFusion] 🏷️ ULTRA token optimization enabled (usage: {usage_percentage*100:.1f}%)")
        elif usage_percentage > 0.6:
            optimization_level = "high"   # 70% token reduction
            print(f"[ChatFusion] 🏷️ HIGH token optimization enabled (usage: {usage_percentage*100:.1f}%)")
        elif usage_percentage > 0.4:
            optimization_level = "medium" # 55% token reduction
            print(f"[ChatFusion] 🏷️ MEDIUM token optimization enabled (usage: {usage_percentage*100:.1f}%)")
        else:
            optimization_level = "standard" # 40% token reduction
            print(f"[ChatFusion] 🏷️ STANDARD token optimization enabled (usage: {usage_percentage*100:.1f}%)")
            
    except Exception as budget_error:
        print(f"[ChatFusion] ⚠️ Budget check error: {budget_error}")
        optimization_level = "standard"
    
    # ✅ ENTROPY SYSTEM: Process emotional and uncertainty context
    emotional_context = {}
    consciousness_summary = ""
    if ENTROPY_AVAILABLE:
        try:
            emotional_context = process_emotional_context(question, f"fusion_{username}")
            entropy_engine = get_entropy_engine()
            consciousness_score = entropy_engine.get_consciousness_metrics()['consciousness_score']
            print(f"[ChatFusion] 🎭 Emotional state: {emotional_context.get('primary_emotion', 'neutral')}")
            print(f"[ChatFusion] 🌀 Consciousness score: {consciousness_score:.2f}")
            
            # ✅ TOKEN OPTIMIZATION: Create compressed consciousness summary
            if optimization_level in ["high", "ultra"]:
                # Ultra-compressed consciousness for high optimization
                emotion = emotional_context.get('primary_emotion', 'neutral')[:4]  # Abbreviate
                consciousness_summary = f"[C:{emotion}|s:{consciousness_score:.1f}]"
            else:
                # Standard consciousness summary
                consciousness_summary = get_consciousness_summary_for_llm({
                    'emotion_engine': {'primary_emotion': emotional_context.get('primary_emotion', 'neutral')},
                    'entropy_level': consciousness_score
                })
            
            print(f"[ChatFusion] 🏷️ Consciousness summary: {consciousness_summary}")
            
        except Exception as entropy_error:
            print(f"[ChatFusion] ⚠️ Entropy processing error: {entropy_error}")
            consciousness_summary = "[C:engaged]" if optimization_level in ["high", "ultra"] else "[CONSCIOUSNESS:engaged]"
    
    # 🔧 FIX: Check for unified username from memory fusion
    print(f"[ChatFusion] 🔍 Checking memory fusion for user: {username}")
    try:
        unified_username = get_intelligent_unified_username(username)
        
        if unified_username != username:
            print(f"[ChatFusion] 🎯 MEMORY FUSION: {username} → {unified_username}")
            print(f"[ChatFusion] 🧠 Using unified memory for response generation")
        else:
            print(f"[ChatFusion] ✅ No fusion needed for {username}")
        
        # 🔧 CRITICAL: Use unified username for ALL subsequent operations
        username = unified_username
        
    except ImportError:
        print(f"[ChatFusion] ⚠️ Memory fusion not available, using original username: {username}")
    except Exception as e:
        print(f"[ChatFusion] ❌ Memory fusion error: {e}, using original username: {username}")
    
    # Step 2: Use unified username for all memory operations
    smart_memory = get_smart_memory(username)
    
    # Step 3: Extract and store memories from current message
    smart_memory.extract_and_store_human_memories(question)
    
    # Step 4: Check for natural context responses (reminders, follow-ups)
    context_response = smart_memory.check_for_natural_context_response()
    
    if context_response:
        print(f"[ChatFusion] 🎯 Context response triggered: {context_response}")
        
        # ✅ ENTROPY SYSTEM: Probabilistic transition selection with consciousness
        if ENTROPY_AVAILABLE:
            casual_transitions = [
                "Oh hey, before I forget - ", 
                "Actually, ", 
                "By the way, ",
                "Quick thing - ",
                "Um, wait - ",  # Added uncertainty
                "Hmm, I should mention - ",  # Added hesitation
                ""
            ]
            transition = probabilistic_select(casual_transitions)
        else:
            casual_transitions = [
                "Oh hey, before I forget - ", 
                "Actually, ", 
                "By the way, ",
                "Quick thing - ",
                ""
            ]
            transition = random.choice(casual_transitions)
        
        if transition:
            # ✅ ENTROPY SYSTEM: Inject consciousness into transition
            if ENTROPY_AVAILABLE:
                transition = inject_consciousness_entropy("response", transition)
            yield transition
        
        # Make context response more casual with entropy
        casual_context = context_response.replace("I wanted to", "I was gonna")
        casual_context = casual_context.replace("remind you", "remind ya")
        casual_context = casual_context.replace("follow up", "check in")
        
        # ✅ ENTROPY SYSTEM: Add uncertainty to context delivery
        if ENTROPY_AVAILABLE and emotional_context.get('uncertainty_level', 0) > 0.4:
            uncertainty_modifiers = ["I think ", "maybe ", "I believe "]
            uncertainty_mod = probabilistic_select(uncertainty_modifiers + [""])
            if uncertainty_mod:
                casual_context = uncertainty_mod + casual_context
        
        for word in casual_context.split():
            yield word + " "
        
        # Add transition to main response with entropy
        if ENTROPY_AVAILABLE:
            casual_connectors = [
                "Anyway, ", "So, ", "But yeah, ", "And ", "Um, ", "Well, ", ""
            ]
            connector = probabilistic_select(casual_connectors)
        else:
            casual_connectors = [
                "Anyway, ", "So, ", "But yeah, ", "And ", ""
            ]
            connector = random.choice(casual_connectors)
        
        if connector:
            if ENTROPY_AVAILABLE:
                connector = inject_consciousness_entropy("response", connector)
            yield connector
    
    # ✅ ENHANCED ENTROPY SYSTEM: Multiple response pathway generation for consciousness emergence
    response_pathways = []
    optimized_question = question
    
    if ENTROPY_AVAILABLE:
        try:
            # ✅ TOKEN OPTIMIZATION: Create optimized question with consciousness context
            if optimization_level in ["high", "ultra"]:
                # Ultra-compressed prompt optimization
                optimized_question = f"{question} {consciousness_summary}"
                print(f"[ChatFusion] 🏷️ Ultra-optimized prompt: +{len(consciousness_summary)} chars")
            elif optimization_level == "medium":
                # Medium optimization with abbreviated consciousness
                consciousness_abbreviated = consciousness_summary[:50] + "..." if len(consciousness_summary) > 50 else consciousness_summary
                optimized_question = f"{question} {consciousness_abbreviated}"
                print(f"[ChatFusion] 🏷️ Medium-optimized prompt: +{len(consciousness_abbreviated)} chars")
            else:
                # Standard optimization
                optimized_question = f"{question} {consciousness_summary}"
                print(f"[ChatFusion] 🏷️ Standard-optimized prompt: +{len(consciousness_summary)} chars")
            
            print(f"[ChatFusion] 🌀 Generating multiple consciousness pathways...")
            
            # Primary pathway (main response) with optimized prompt
            response_pathways.append(("primary", generate_response_streaming(optimized_question, username, lang)))
            
            # Check for alternative pathways based on uncertainty (only if not ultra-optimized)
            if optimization_level != "ultra":
                uncertainty_state = get_entropy_engine().get_uncertainty_state()
                if uncertainty_state.value in ["uncertain", "confused"]:
                    # Generate uncertainty-flavored response with optimization
                    if optimization_level == "high":
                        uncertain_question = f"Uncertain: '{question}' {consciousness_summary[:30]}"
                    else:
                        uncertain_question = f"I'm not entirely sure, but regarding '{question}' {consciousness_summary}"
                    response_pathways.append(("uncertain", generate_response_streaming(uncertain_question, username, lang)))
            
            # Probabilistic pathway selection
            if len(response_pathways) > 1:
                weights = [0.7, 0.3]  # Favor primary but allow uncertainty
                selected_pathway = probabilistic_select(response_pathways, weights)
                chosen_generator = selected_pathway[1]
                print(f"[ChatFusion] 🎯 Selected {selected_pathway[0]} response pathway")
            else:
                chosen_generator = response_pathways[0][1]
                
        except Exception as pathway_error:
            print(f"[ChatFusion] ⚠️ Pathway generation error: {pathway_error}")
            # Fallback with basic optimization
            fallback_question = f"{question} {consciousness_summary}" if consciousness_summary else question
            chosen_generator = generate_response_streaming(fallback_question, username, lang)
    else:
        # No entropy system available - use basic consciousness optimization
        if consciousness_summary:
            optimized_question = f"{question} {consciousness_summary}"
        chosen_generator = generate_response_streaming(optimized_question, username, lang)
    
    # Step 5: Generate main response with unified memory context + CONSCIOUSNESS ENTROPY + TOKEN OPTIMIZATION
    print(f"[ChatFusion] 💭 Generating CONSCIOUSNESS response with unified memory for {username}")
    print(f"[ChatFusion] 🏷️ Token optimization level: {optimization_level}")
    
    chunk_count = 0
    total_chars = 0
    
    for chunk in chosen_generator:
        # ✅ ENTROPY SYSTEM: Inject consciousness into each chunk
        if ENTROPY_AVAILABLE:
            try:
                chunk = inject_consciousness_entropy("response", chunk, EntropyLevel.MEDIUM)
            except Exception as chunk_error:
                print(f"[ChatFusion] ⚠️ Chunk entropy error: {chunk_error}")
        
        # ✅ TOKEN OPTIMIZATION: Track optimization metrics
        if chunk:
            chunk_count += 1
            total_chars += len(chunk)
            
            # For ultra optimization, log every 5th chunk
            if optimization_level == "ultra" and chunk_count % 5 == 0:
                print(f"[ChatFusion] 🏷️ Ultra-optimized chunk {chunk_count}: {total_chars} chars")
            
        yield chunk
    
    # ✅ TOKEN OPTIMIZATION: Final optimization metrics
    if chunk_count > 0:
        avg_chunk_size = total_chars / chunk_count
        print(f"[ChatFusion] ✅ Response complete: {chunk_count} chunks, {total_chars} chars")
        print(f"[ChatFusion] 📊 Optimization: {optimization_level} level, avg chunk: {avg_chunk_size:.1f} chars")
        
        # Log significant optimizations
        if optimization_level in ["high", "ultra"]:
            estimated_original_size = total_chars * (2.0 if optimization_level == "high" else 3.0)
            estimated_reduction = (estimated_original_size - total_chars) / estimated_original_size
            print(f"[ChatFusion] 🎯 Estimated token reduction: {estimated_reduction*100:.1f}%")

# Export for main.py
__all__ = ['generate_response_streaming_with_intelligent_fusion']