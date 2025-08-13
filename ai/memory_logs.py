"""
Logging utilities for memory extraction and recall decisions.
"""
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
import os


def log_extraction_decision(
    text: str,
    extracted_items: List[Dict[str, Any]],
    confidence: float,
    pattern_ids: List[str],
    llm_fallback_used: bool = False,
    metadata: Optional[Dict[str, Any]] = None
) -> None:
    """
    Log a memory extraction decision for debugging and analysis.
    
    Args:
        text: Original text that was analyzed
        extracted_items: Items extracted from the text
        confidence: Confidence score of the extraction
        pattern_ids: Pattern IDs that matched
        llm_fallback_used: Whether LLM fallback was used
        metadata: Additional metadata to log
    """
    # Ensure logs directory exists
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'type': 'extraction',
        'text': text,
        'extracted_items': extracted_items,
        'confidence': confidence,
        'pattern_ids': pattern_ids,
        'llm_fallback_used': llm_fallback_used,
        'metadata': metadata or {}
    }
    
    # Write to daily log file
    log_date = datetime.now().strftime('%Y-%m-%d')
    log_file = os.path.join(logs_dir, f"memory_extraction_{log_date}.jsonl")
    
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        # Also print summary for debugging
        print(f"[MemoryLog] 📊 Extraction: {len(extracted_items)} items, conf={confidence:.3f}, "
              f"LLM={'YES' if llm_fallback_used else 'NO'}, patterns={len(pattern_ids)}")
    except Exception as e:
        print(f"[MemoryLog] ⚠️ Failed to write log: {e}")


def log_recall_decision(
    question: str,
    recalled_memories: List[Dict[str, Any]],
    recall_strategy: str,
    confidence: float,
    processing_time_ms: float,
    metadata: Optional[Dict[str, Any]] = None
) -> None:
    """
    Log a memory recall decision for debugging and analysis.
    
    Args:
        question: Question that triggered recall
        recalled_memories: Memories that were recalled
        recall_strategy: Strategy used for recall
        confidence: Overall confidence in recall
        processing_time_ms: Time taken for recall in milliseconds
        metadata: Additional metadata to log
    """
    # Ensure logs directory exists
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'type': 'recall',
        'question': question,
        'recalled_count': len(recalled_memories),
        'recall_strategy': recall_strategy,
        'confidence': confidence,
        'processing_time_ms': processing_time_ms,
        'memory_ids': [mem.get('id', 'unknown') for mem in recalled_memories],
        'metadata': metadata or {}
    }
    
    # Write to daily log file
    log_date = datetime.now().strftime('%Y-%m-%d')
    log_file = os.path.join(logs_dir, f"memory_recall_{log_date}.jsonl")
    
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        # Also print summary for debugging
        print(f"[MemoryLog] 🧠 Recall: {len(recalled_memories)} memories, conf={confidence:.3f}, "
              f"strategy={recall_strategy}, time={processing_time_ms:.1f}ms")
    except Exception as e:
        print(f"[MemoryLog] ⚠️ Failed to write recall log: {e}")


def get_log_file_path(log_type: str) -> str:
    """
    Get the appropriate log file path for a given log type.
    
    Args:
        log_type: Type of log ('extraction', 'recall', etc.)
        
    Returns:
        Path to the log file
    """
    # TODO: Implement log file path generation
    # Should create dated log files in logs/ directory
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    return os.path.join('logs', f'memory_{log_type}_{date_str}.jsonl')