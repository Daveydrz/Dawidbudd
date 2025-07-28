# 🧠 NEW ARCHITECTURE: Port Separation Implementation

This document describes the new architecture that separates consciousness processing (port 5002) from main LLM response generation (port 5001), with enhanced Kokoro timing fixes.

## 🏗️ Architecture Overview

```
User Input → Port 5002 (Gemma-2-2B) → Consciousness Processing → Clean Prompt → Port 5001 (Main LLM) → Response
```

### Key Principles:
- **Port 5002 (Gemma-2-2B)**: Handles ALL consciousness-related processing
- **Port 5001 (Main LLM)**: Handles ONLY final response generation  
- **Smart Streaming**: Prevents Kokoro overwhelm with 30-50% token threshold
- **Local Memory**: All updates handled via consciousness data, no ONNX classifiers

## 📂 Files Modified

### Core Architecture Files

#### `ai/extractor_client.py` ✅ EXPANDED
- **Purpose**: Full consciousness processing via Gemma-2-2B (port 5002)
- **Features**: 
  - Memory updates (facts, preferences, context)
  - Emotional state processing
  - Belief tracking and updates
  - Consciousness state management
  - Response context generation
- **API**: `process_full_consciousness(user_text, user_id)` → comprehensive consciousness data

#### `ai/simple_llm_handler.py` ✅ NEW
- **Purpose**: Single LLM call handler for port 5001 only
- **Features**:
  - Clean prompt injection with consciousness data
  - Streaming response generation
  - Minimal processing overhead
- **API**: `generate_response_with_consciousness(text, user_id, consciousness_context)`

#### `main.py` ✅ MODIFIED
- **Changes**: Updated `handle_streaming_response()` with new architecture
- **Flow**:
  1. Send user input to port 5002 for consciousness processing
  2. Get comprehensive consciousness data back
  3. Format consciousness data for prompt injection
  4. Send injected prompt to port 5001 for final response
  5. Use smart streaming to prevent Kokoro overwhelm

### Audio System Fixes

#### `audio/smart_streaming_output.py` ✅ NEW  
- **Purpose**: Fix Kokoro timing issues that cause shutdown
- **Features**:
  - 30-50% token threshold before starting speech
  - Chunk accumulation and batch processing
  - Anti-overwhelm protection (min 1s between calls)
  - Automatic finalization of remaining chunks
- **API**: `speak_streaming_smart(chunk, is_final)` → prevents Kokoro overload

### Memory Management

#### `ai/local_memory_manager.py` ✅ UPDATED
- **Changes**: Removed ONNX classifier imports
- **New Method**: `update_memory(user_id, text, consciousness_data)`
- **Features**: Processes full consciousness data structure from Gemma

## 🚀 Usage Examples

### 1. Full Consciousness Processing (Port 5002)
```python
from ai.extractor_client import process_full_consciousness

consciousness_data = process_full_consciousness(
    "I like pizza and my name is David", 
    "user123"
)

# Returns comprehensive data:
# - classification: memory_type, intent, emotion, name_introduction
# - memory_updates: new_facts, new_preferences, new_context  
# - emotional_state: detected_emotion, buddy_response, intensity
# - consciousness_state: focus, goals, inner_thoughts, motivation
# - belief_updates: reinforced, new, contradicted beliefs
# - response_context: personality_tone, knowledge_areas, priority
```

### 2. Single LLM Response Generation (Port 5001)
```python
from ai.simple_llm_handler import generate_response_with_consciousness
from ai.extractor_client import get_consciousness_for_prompt

# Get consciousness context from port 5002 processing  
consciousness_context = get_consciousness_for_prompt("user123")

# Generate response using ONLY port 5001
for chunk in generate_response_with_consciousness("What time is it?", "user123", consciousness_context):
    print(f"Response chunk: {chunk}")
```

### 3. Smart Streaming (Kokoro Fix)
```python
from audio.smart_streaming_output import speak_streaming_smart, reset_streaming_output, finalize_streaming_output

# Reset for new response
reset_streaming_output()

# Add chunks (automatically handles 30-50% threshold)
for chunk in response_chunks:
    is_final = (chunk == response_chunks[-1])
    spoke = speak_streaming_smart(chunk, is_final)
    if spoke:
        print("Speech triggered!")

# Finalize any remaining chunks
finalize_streaming_output()
```

## 🔧 Configuration

### Required Servers
- **Gemma-2-2B**: Must be running on `http://localhost:5002`
- **Main LLM**: Must be running on `http://localhost:5001`  
- **Kokoro TTS**: Must be running on `http://localhost:8880`

### Environment Variables
```bash
# Set in buddy_config.json or environment
SINGLE_LLM_CALL_MODE=true
ENABLE_INNER_THOUGHTS=false  # Processed by Gemma now
ENABLE_SELF_REFLECTION=false  # Processed by Gemma now
```

## 🎯 Benefits

### Performance Improvements
- **Response Time**: Target 3-5s (down from 15-20s)
- **LLM Calls**: Reduced from 5-6 per turn to exactly 1
- **Classification Speed**: <1s via Gemma-2-2B local processing
- **Memory Updates**: Instant local JSON operations

### Reliability Improvements  
- **Kokoro Stability**: Smart streaming prevents TTS shutdown
- **Resource Efficiency**: CPU vs GPU separation optimizes usage
- **Error Resilience**: Graceful fallbacks when servers unavailable
- **Class 5+ Consciousness**: Maintained while improving speed

### Architecture Benefits
- **Clean Separation**: Clear responsibilities between components
- **Scalability**: Each component can be scaled independently  
- **Maintainability**: Simplified debugging and monitoring
- **Extensibility**: Easy to add new consciousness modules

## 🧪 Testing

Run the comprehensive test suite:
```bash
python test_new_architecture.py
```

Tests verify:
- ✅ Extractor client (port 5002) consciousness processing
- ✅ Simple LLM handler (port 5001) response generation  
- ✅ Smart streaming output Kokoro timing fix
- ✅ Local memory manager consciousness data handling

## 🐛 Troubleshooting

### Common Issues

**Port 5002 Connection Refused**
- Ensure Gemma-2-2B server is running
- Check `http://localhost:5002/health`
- Falls back to rule-based classification

**Port 5001 Connection Refused**  
- Ensure main LLM server is running
- Check `http://localhost:5001/health`
- Returns error message to user

**Kokoro Shutdown**
- Smart streaming should prevent this
- Check logs for "Too soon since last speech"
- Adjust `min_speech_interval` if needed

**Memory Not Updating**
- Check consciousness data structure in logs
- Verify `local_memory.json` is writable
- Memory updates happen locally, not via LLM

## 📊 Monitoring

### Key Metrics to Watch
- **Response Time**: Target <5s total
- **Consciousness Processing Time**: Target <1s  
- **LLM Generation Time**: Target <3s
- **Memory Update Success Rate**: Should be >95%
- **Kokoro Speech Success Rate**: Should be >90%

### Log Patterns
```
[NEW_ARCH] 🧠 STEP 1: Processing consciousness via PORT 5002
[NEW_ARCH] 🚀 STEP 2: Generating response via PORT 5001  
[SmartStreaming] 🎵 Reached 30% token threshold - starting speech
[NEW_ARCH] ✅ PORT SEPARATED response complete
```

## 🔮 Future Enhancements

### Planned Improvements
- **Dynamic Token Thresholds**: Adjust based on response length
- **Parallel Processing**: Concurrent consciousness + LLM processing
- **Advanced Fallbacks**: Multiple backup servers for reliability
- **Performance Analytics**: Real-time monitoring dashboard
- **Smart Caching**: Cache consciousness data for repeated queries

---

*This architecture represents a significant improvement in performance, reliability, and maintainability while preserving full Class 5+ consciousness capabilities.*