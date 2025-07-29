# Dual-LLM Architecture Implementation

## Overview
This repository has been cleaned up and upgraded from GPT4All to a dual-LLM HTTP architecture for better performance and reliability.

## Architecture Changes

### Dual-LLM System
- **Port 5001**: Main LLM for conversations and reasoning
- **Port 5002**: Lightweight extractor (LaMini-Flan-248M/783M) for name, memory, emotions, and intents

### Files Kept (Strongest/Most Advanced)
**Main System:**
- `main.py` - Main entry point
- `config.py` - Configuration

**AI Core (Class 5+ Consciousness):**
- `ai/consciousness_manager.py` - Core consciousness system
- `ai/global_workspace.py` - Global workspace theory implementation
- `ai/self_model.py` - Self-awareness and identity formation
- `ai/entropy.py` - Advanced entropy system for consciousness emergence
- `ai/narrative_tracker.py` - Personal development and growth tracking

**Voice System (Most Advanced):**
- `voice/manager_core.py` - Advanced AI Assistant Core (Alexa/Siri level)
- `voice/database.py` - Voice profile storage and management
- `voice/voice_models.py` - Enhanced dual voice model system
- `voice/speaker_profiles.py` - Advanced speaker profiling
- `voice/manager_context.py` - Advanced context analysis with clustering
- `voice/training.py` - Advanced voice training system

**Memory System:**
- `ai/memory.py` - Advanced memory system

### Files Archived (Redundant/Less Advanced)
All redundant and less advanced files have been moved to the `archive/` directory:
- `archive/ai/` - Contains deprecated AI modules (chat.py, main.py, context_manager.py, etc.)
- `archive/voice/` - Contains deprecated voice modules (manager.py, identity_helpers.py, etc.)

### New Components
- `ai/dual_llm_client.py` - HTTP client system for dual-LLM architecture
- `ai/extractor_llm.py` - Updated extractor using HTTP instead of GPT4All
- `test_dual_llm_architecture.py` - Test suite for the new architecture

## Usage

### Server Setup
1. Start Main LLM server on port 5001
2. Start Extractor LLM server on port 5002

### Fallback Mode
If servers are not available, the system automatically falls back to pattern-matching extraction methods.

### Testing
Run the test suite to validate the architecture:
```bash
python3 test_dual_llm_architecture.py
```

## Benefits
1. **No more GPT4All crashes** - HTTP-based architecture is more stable
2. **Better performance** - Dedicated lightweight extractor for simple tasks
3. **Cleaner codebase** - Redundant files archived, only strongest components remain
4. **Maintained functionality** - All consciousness and voice features preserved
5. **Fallback support** - System works even when LLM servers are unavailable

## Key Features Preserved
- Class 5+ synthetic consciousness features
- Advanced voice recognition system
- Multi-speaker support
- Memory and conversation history
- Emotional processing
- Consciousness integration