"""
Memory recall and context building for questions.
"""
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import re
import random
import time
import sqlite3
import os
import config
from .text_embedder import embed_text_batch
from .memory_store import neighbors_by_vector, find_by_ids, DB_PATH
from .memory_logs import log_recall_decision
from .memory_normalize import parse_australian_date, parse_relative_time


def parse_question_constraints(question: str) -> Dict[str, Any]:
    """
    Parse question for temporal constraints, role synonyms, and anaphora.
    
    Args:
        question: The question text
        
    Returns:
        Dictionary with parsed constraints
    """
    constraints = {
        'before_date': None,
        'after_date': None,
        'roles': [],
        'media_anaphora': [],
        'keywords': []
    }
    
    question_lower = question.lower()
    
    # Parse temporal constraints
    before_patterns = [
        r'before (\d{1,2}/\d{1,2}(?:/\d{4})?)',
        r'before (yesterday|today|tomorrow)',
        r'before (last|this|next) (week|month|year)'
    ]
    
    after_patterns = [
        r'after (\d{1,2}/\d{1,2}(?:/\d{4})?)',
        r'after (yesterday|today|tomorrow)',
        r'after (last|this|next) (week|month|year)',
        r'since (\d{1,2}/\d{1,2}(?:/\d{4})?)',
        r'since (yesterday|today|tomorrow)'
    ]
    
    for pattern in before_patterns:
        match = re.search(pattern, question_lower)
        if match:
            date_str = match.group(1)
            if '/' in date_str:
                constraints['before_date'] = parse_australian_date(date_str)
            else:
                constraints['before_date'] = parse_relative_time(date_str)
    
    for pattern in after_patterns:
        match = re.search(pattern, question_lower)
        if match:
            date_str = match.group(1)
            if '/' in date_str:
                constraints['after_date'] = parse_australian_date(date_str)
            else:
                constraints['after_date'] = parse_relative_time(date_str)
    
    # Parse role synonyms
    role_patterns = {
        'family': r'\b(family|relatives?|parents?|siblings?|brother|sister|mum|dad|mother|father)\b',
        'friends': r'\b(friends?|mates?|buddies?)\b',
        'work': r'\b(work|colleagues?|boss|manager|team)\b',
        'partner': r'\b(partner|girlfriend|boyfriend|wife|husband|spouse)\b'
    }
    
    for role, pattern in role_patterns.items():
        if re.search(pattern, question_lower):
            constraints['roles'].append(role)
    
    # Parse media anaphora
    media_patterns = [
        r'\b(?:the|that) (movie|film|book|show|series|song|album)\b',
        r'\bwhat (?:was|is) (?:the name of )?(?:the|that) (movie|film|book|show|series|song|album)\b'
    ]
    
    for pattern in media_patterns:
        matches = re.findall(pattern, question_lower)
        constraints['media_anaphora'].extend(matches)
    
    # Extract key terms for keyword search
    # Remove common words and extract meaningful terms
    stop_words = {'what', 'when', 'where', 'who', 'how', 'why', 'did', 'do', 'does', 
                  'is', 'was', 'were', 'are', 'the', 'a', 'an', 'and', 'or', 'but', 
                  'i', 'you', 'we', 'they', 'he', 'she', 'it', 'my', 'your', 'our',
                  'say', 'said', 'tell', 'told', 'about', 'me'}
    
    words = re.findall(r'\b\w+\b', question_lower)
    keywords = [word for word in words if len(word) > 2 and word not in stop_words]
    constraints['keywords'] = keywords[:10]  # Limit to top 10 keywords
    
    return constraints


def build_query_text(question: str, dialog_summary: Optional[str] = None) -> str:
    """
    Build enhanced query text from question and optional dialog summary.
    
    Args:
        question: The question being asked
        dialog_summary: Optional short dialog summary for context
        
    Returns:
        Enhanced query text for embedding
    """
    # Start with the question
    query_parts = [question.strip()]
    
    # Add dialog summary if provided
    if dialog_summary and dialog_summary.strip():
        query_parts.append(f"Context: {dialog_summary.strip()}")
    
    # Combine and return
    return " | ".join(query_parts)


def get_episodic_memories_recent(days: int = 7) -> List[Dict[str, Any]]:
    """
    Get recent episodic memories for context.
    
    Args:
        days: Number of days to look back
        
    Returns:
        List of recent episodic memory dictionaries
    """
    if not os.path.exists(DB_PATH):
        return []
    
    cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM episodic_raw 
        WHERE created_at > ? 
        ORDER BY created_at DESC 
        LIMIT 50
    ''', (cutoff_date,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def search_memories_by_keywords(keywords: List[str], limit: int = 20) -> List[str]:
    """
    Search memories by keyword matching in text content.
    
    Args:
        keywords: List of keywords to search for
        limit: Maximum number of memory IDs to return
        
    Returns:
        List of memory IDs matching keywords
    """
    if not keywords or not os.path.exists(DB_PATH):
        return []
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Build query with OR conditions for keywords
    keyword_conditions = []
    params = []
    
    for keyword in keywords:
        keyword_conditions.append('(text LIKE ? OR kind LIKE ? OR participants LIKE ? OR items LIKE ?)')
        keyword_pattern = f'%{keyword}%'
        params.extend([keyword_pattern, keyword_pattern, keyword_pattern, keyword_pattern])
    
    if not keyword_conditions:
        return []
    
    query = f'''
        SELECT id FROM memories 
        WHERE deleted = 0 AND ({' OR '.join(keyword_conditions)})
        ORDER BY created_at DESC
        LIMIT ?
    '''
    params.append(limit)
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    return [row[0] for row in rows]


def calculate_memory_decay(created_time: datetime, current_time: datetime, half_life_days: float = 21.0) -> float:
    """
    Calculate memory strength decay over time.
    
    Args:
        created_time: When the memory was created
        current_time: Current time
        half_life_days: Half-life for memory decay in days
        
    Returns:
        Decay factor (0.0 to 1.0)
    """
    if isinstance(created_time, str):
        created_time = datetime.fromisoformat(created_time.replace('Z', '+00:00'))
    
    days_elapsed = (current_time - created_time).total_seconds() / (24 * 3600)
    decay_factor = 0.5 ** (days_elapsed / half_life_days)
    return min(1.0, max(0.0, decay_factor))


def calculate_recency_boost(created_time: datetime, current_time: datetime, near_future_days: int = 14) -> float:
    """
    Calculate recency boost for memories.
    
    Args:
        created_time: When the memory was created
        current_time: Current time
        near_future_days: Days to consider as "recent" for boosting
        
    Returns:
        Recency boost factor (0.0 to 1.0)
    """
    if isinstance(created_time, str):
        created_time = datetime.fromisoformat(created_time.replace('Z', '+00:00'))
    
    days_elapsed = (current_time - created_time).total_seconds() / (24 * 3600)
    
    if days_elapsed < 0:  # Future memory
        return 1.0
    elif days_elapsed < near_future_days:
        # Linear decay from 1.0 to 0.1 over near_future_days
        return 1.0 - (days_elapsed / near_future_days) * 0.9
    else:
        return 0.1


def score_memory(memory: Dict[str, Any], similarity: float, current_time: datetime) -> float:
    """
    Score a memory using the weighted formula.
    
    Args:
        memory: Memory dictionary
        similarity: Vector similarity score
        current_time: Current time for recency calculations
        
    Returns:
        Combined score
    """
    # Get memory attributes with defaults
    importance = float(memory.get('importance', 1.0))
    strength = float(memory.get('strength', 1.0))
    created_at = memory.get('created_at', current_time.isoformat())
    
    if isinstance(created_at, str):
        try:
            created_time = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        except:
            created_time = current_time
    else:
        created_time = created_at
    
    # Calculate components
    recency_boost = calculate_recency_boost(created_time, current_time, 
                                          getattr(config, 'RECALL_NEAR_FUTURE_DAYS', 14))
    
    # Weighted scoring: 0.6*similarity + 0.2*importance + 0.1*recency_boost + 0.1*strength
    score = (0.6 * similarity + 
             0.2 * (importance / 4.0) + 
             0.1 * recency_boost + 
             0.1 * (strength / getattr(config, 'MAX_STRENGTH', 4.0)))
    
    return min(1.0, max(0.0, score))


def format_known_facts(memories: List[Dict[str, Any]]) -> str:
    """
    Format memories as a "Known Facts" bullet list with ID tags.
    
    Args:
        memories: List of memory dictionaries
        
    Returns:
        Formatted string with bullet points and ID tags
    """
    if not memories:
        return "Known Facts: None available."
    
    facts = ["Known Facts:"]
    
    for memory in memories:
        text = memory.get('text', '').strip()
        memory_id = memory.get('id', 'unknown')
        kind = memory.get('kind', 'general')
        created_at = memory.get('created_at', '')
        
        # Truncate very long text
        if len(text) > 120:
            text = text[:117] + "..."
        
        # Format created time
        time_str = ""
        if created_at:
            try:
                dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                time_str = f" ({dt.strftime('%d/%m/%Y')})"
            except:
                pass
        
        # Create bullet point
        bullet = f"• {text}{time_str} #{memory_id}"
        facts.append(bullet)
    
    return "\n".join(facts)


def build_memory_context_for_question(
    question: str,
    user_id: Optional[str] = None,
    max_items: int = 6,
    near_future_days: int = 14,
    boost_factor: float = 0.35,
    dialog_summary: Optional[str] = None
) -> Dict[str, Any]:
    """
    Build relevant memory context for answering a question.
    
    Args:
        question: The question being asked
        user_id: ID of the user asking the question  
        max_items: Maximum number of memory items to include
        near_future_days: Days in near future to boost relevance
        boost_factor: Boost factor for recent/relevant memories
        dialog_summary: Optional dialog summary for enhanced context
        
    Returns:
        Dictionary containing:
        - 'memories': List of relevant memory items
        - 'confidence': Overall confidence in the context
        - 'sources': List of source IDs used
        - 'recall_strategy': Strategy used for recall
        - 'known_facts': Formatted bullet list string
    """
    start_time = time.time()
    current_time = datetime.now()
    
    # Parse question for constraints
    constraints = parse_question_constraints(question)
    
    # Build enhanced query text
    query_text = build_query_text(question, dialog_summary)
    
    # Get config values
    vector_recall_enabled = getattr(config, 'VECTOR_RECALL_ENABLED', True)
    recall_max_items = getattr(config, 'RECALL_MAX_ITEMS', max_items)
    recall_jitter = getattr(config, 'RECALL_RANDOM_JITTER', 0.02)
    
    all_candidate_ids = set()
    vector_results = []
    keyword_results = []
    
    # Vector similarity search
    if vector_recall_enabled:
        try:
            # Embed query
            query_embedding = embed_text_batch([query_text])[0]
            
            # Search vector store
            vector_candidates = neighbors_by_vector(query_embedding, k=30)
            vector_results = [(memory_id, similarity) for memory_id, similarity in vector_candidates]
            all_candidate_ids.update([memory_id for memory_id, _ in vector_candidates])
            
        except Exception as e:
            print(f"[MemoryRecall] ⚠️ Vector search failed: {e}")
            vector_results = []
    
    # Keyword/metadata search as fallback/supplement
    keyword_candidates = search_memories_by_keywords(constraints['keywords'], limit=20)
    keyword_results = keyword_candidates
    all_candidate_ids.update(keyword_candidates)
    
    # Retrieve all candidate memories
    all_memories = find_by_ids(list(all_candidate_ids)) if all_candidate_ids else []
    
    # Apply temporal constraints
    filtered_memories = []
    for memory in all_memories:
        created_at = memory.get('created_at')
        if created_at:
            try:
                memory_time = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                
                # Check before constraint
                if constraints['before_date'] and memory_time >= constraints['before_date']:
                    continue
                
                # Check after constraint  
                if constraints['after_date'] and memory_time <= constraints['after_date']:
                    continue
                    
            except:
                pass  # Keep memory if date parsing fails
        
        filtered_memories.append(memory)
    
    # Score memories
    scored_memories = []
    for memory in filtered_memories:
        memory_id = memory.get('id')
        
        # Get similarity score from vector search
        similarity = 0.0
        for vid, vsim in vector_results:
            if vid == memory_id:
                similarity = vsim
                break
        
        # Boost similarity for keyword matches
        if memory_id in keyword_results:
            similarity = max(similarity, 0.3)  # Minimum similarity for keyword matches
        
        # Calculate combined score
        score = score_memory(memory, similarity, current_time)
        scored_memories.append((memory, score))
    
    # Sort by score descending
    scored_memories.sort(key=lambda x: x[1], reverse=True)
    
    # Apply limits and jitter
    limit = min(recall_max_items, len(scored_memories))
    
    # Add small random jitter to break ties
    if recall_jitter > 0:
        for i in range(len(scored_memories)):
            memory, score = scored_memories[i]
            jitter = random.uniform(-recall_jitter, recall_jitter)
            scored_memories[i] = (memory, score + jitter)
        
        # Re-sort after jitter
        scored_memories.sort(key=lambda x: x[1], reverse=True)
    
    # Take top memories
    top_memories = [memory for memory, score in scored_memories[:limit]]
    
    # Calculate overall confidence
    if scored_memories:
        avg_score = sum(score for _, score in scored_memories[:limit]) / len(scored_memories[:limit])
        confidence = min(1.0, avg_score)
    else:
        confidence = 0.0
    
    # Determine recall strategy
    strategy_parts = []
    if vector_results:
        strategy_parts.append("vector")
    if keyword_results:
        strategy_parts.append("keyword")
    recall_strategy = "+".join(strategy_parts) if strategy_parts else "none"
    
    # Format known facts
    known_facts = format_known_facts(top_memories)
    
    # Log recall decision
    processing_time_ms = (time.time() - start_time) * 1000
    metadata = {
        'constraints': constraints,
        'vector_candidates': len(vector_results),
        'keyword_candidates': len(keyword_results),
        'total_candidates': len(all_candidate_ids),
        'filtered_count': len(filtered_memories)
    }
    
    log_recall_decision(
        question=question,
        recalled_memories=top_memories,
        recall_strategy=recall_strategy,
        confidence=confidence,
        processing_time_ms=processing_time_ms,
        metadata=metadata
    )
    
    return {
        'memories': top_memories,
        'confidence': confidence,
        'sources': [mem.get('id', 'unknown') for mem in top_memories],
        'recall_strategy': recall_strategy,
        'known_facts': known_facts
    }


def get_episodic_memories(
    query: str,
    time_range: Optional[tuple] = None,
    max_results: int = 10
) -> List[Dict[str, Any]]:
    """
    Retrieve episodic memories matching query and time constraints.
    
    Args:
        query: Search query for episodic memories
        time_range: Optional (start_time, end_time) tuple
        max_results: Maximum number of results to return
        
    Returns:
        List of episodic memory dictionaries
    """
    if not os.path.exists(DB_PATH):
        return []
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Build query with time constraints
    base_query = "SELECT * FROM episodic_raw WHERE utterance LIKE ?"
    params = [f'%{query}%']
    
    if time_range:
        start_time, end_time = time_range
        base_query += " AND created_at BETWEEN ? AND ?"
        params.extend([start_time.isoformat(), end_time.isoformat()])
    
    base_query += " ORDER BY created_at DESC LIMIT ?"
    params.append(max_results)
    
    cursor.execute(base_query, params)
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def get_semantic_memories(
    query: str,
    similarity_threshold: float = 0.80,
    max_results: int = 10
) -> List[Dict[str, Any]]:
    """
    Retrieve semantic memories by similarity to query.
    
    Args:
        query: Search query for semantic memories
        similarity_threshold: Minimum similarity threshold
        max_results: Maximum number of results to return
        
    Returns:
        List of semantic memory dictionaries
    """
    try:
        # Embed query
        query_embedding = embed_text_batch([query])[0]
        
        # Search for similar memories
        candidates = neighbors_by_vector(query_embedding, k=max_results * 2)
        
        # Filter by similarity threshold
        filtered_candidates = [(memory_id, sim) for memory_id, sim in candidates 
                             if sim >= similarity_threshold]
        
        # Get memory details
        memory_ids = [memory_id for memory_id, _ in filtered_candidates[:max_results]]
        memories = find_by_ids(memory_ids)
        
        # Add similarity scores
        for memory in memories:
            for memory_id, sim in filtered_candidates:
                if memory.get('id') == memory_id:
                    memory['similarity'] = sim
                    break
        
        return memories
        
    except Exception as e:
        print(f"[MemoryRecall] ⚠️ Semantic memory search failed: {e}")
        return []