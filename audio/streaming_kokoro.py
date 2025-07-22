# audio/streaming_kokoro.py - UPDATED: Direct Kokoro library integration
"""
Streaming wrapper for Kokoro TTS using direct library integration
"""
import threading
import queue
import time
import numpy as np
from typing import Optional, Generator, List
from concurrent.futures import ThreadPoolExecutor, Future
from dataclasses import dataclass
from audio.kyutai_coordinator import StreamingChunk, get_kyutai_coordinator
from config import *

@dataclass
class AudioChunk:
    """Audio chunk with metadata"""
    audio_data: np.ndarray
    sample_rate: int
    chunk_id: str
    text: str
    start_time: float
    generation_time: float

class StreamingKokoroWrapper:
    """UPDATED: Streaming wrapper that uses direct Kokoro library"""
    
    def __init__(self):
        self.thread_pool = ThreadPoolExecutor(max_workers=STREAMING_THREAD_POOL_SIZE)
        self.audio_queue = queue.Queue(maxsize=STREAMING_BUFFER_SIZE)
        self.generation_futures = {}
        self.is_streaming = False
        self.current_voice = "af_heart"  # Default voice
        self.current_lang = "en-us"
        
    def set_voice_settings(self, lang: str):
        """Set voice and language for Kokoro"""
        if lang in KOKORO_VOICES:
            self.current_voice = KOKORO_VOICES[lang]
            self.current_lang = KOKORO_LANGS.get(lang, lang)
            if DEBUG:
                print(f"[StreamingKokoro] 🎭 Voice set to {self.current_voice} ({self.current_lang})")
    
    def generate_audio_chunk_sync(self, text: str, chunk_id: str) -> Optional[AudioChunk]:
        """Generate audio for a single chunk using direct Kokoro library"""
        try:
            start_time = time.time()
            
            # ✅ UPDATED: Use direct Kokoro library via audio.output
            from audio.output import generate_tts
            
            if DEBUG:
                print(f"[StreamingKokoro] 🎵 Generating chunk {chunk_id}: '{text[:30]}...'")
            
            # Use the updated generate_tts with direct library
            audio_data, sample_rate = generate_tts(text, self.current_lang.split('-')[0])
            
            generation_time = time.time() - start_time
            
            if audio_data is not None:
                audio_chunk = AudioChunk(
                    audio_data=audio_data,
                    sample_rate=sample_rate,
                    chunk_id=chunk_id,
                    text=text,
                    start_time=start_time,
                    generation_time=generation_time
                )
                
                if DEBUG:
                    print(f"[StreamingKokoro] ✅ Generated chunk {chunk_id} in {generation_time:.2f}s")
                
                return audio_chunk
            else:
                print(f"[StreamingKokoro] ❌ No audio generated for chunk {chunk_id}")
                return None
            
        except Exception as e:
            print(f"[StreamingKokoro] ❌ Error generating audio for chunk {chunk_id}: {e}")
            return None
    
    def stream_text_chunks(self, text_chunks: List[str], lang: str = "en") -> Generator[AudioChunk, None, None]:
        """Stream audio generation for text chunks"""
        self.set_voice_settings(lang)
        self.is_streaming = True
        
        try:
            # Create Kyutai coordinator chunks
            coordinator = get_kyutai_coordinator()
            all_chunks = []
            
            for text in text_chunks:
                chunks = coordinator.smart_chunk_text(text)
                optimized_chunks = coordinator.optimize_for_kokoro(chunks)
                all_chunks.extend(optimized_chunks)
            
            if DEBUG:
                print(f"[StreamingKokoro] 🎵 Streaming {len(all_chunks)} chunks")
            
            # Process chunks with timing
            for i, chunk in enumerate(all_chunks):
                chunk_id = f"chunk_{i}"
                
                # Generate and play audio
                audio_chunk = self.generate_audio_chunk_sync(chunk.text, chunk_id)
                
                if audio_chunk:
                    yield audio_chunk
                
                # Apply Kyutai prosody timing
                if KYUTAI_PROSODY_OVERLAP > 0 and i < len(all_chunks) - 1:
                    time.sleep(KYUTAI_PROSODY_OVERLAP)
        
        finally:
            self.is_streaming = False
    
    def get_streaming_stats(self) -> dict:
        """Get streaming performance statistics"""
        return {
            "is_streaming": self.is_streaming,
            "current_voice": self.current_voice,
            "current_lang": self.current_lang,
            "buffer_size": STREAMING_BUFFER_SIZE,
            "thread_pool_size": STREAMING_THREAD_POOL_SIZE
        }

# Global streaming Kokoro instance
streaming_kokoro = StreamingKokoroWrapper()

def stream_speak_chunks(text_chunks: List[str], lang: str = "en"):
    """UPDATED: High-level function to stream speak text chunks using direct library"""
    kokoro = streaming_kokoro
    
    if DEBUG:
        print(f"[StreamSpeak] 🌊 Starting to stream {len(text_chunks)} text chunks")
    
    chunk_count = 0
    for audio_chunk in kokoro.stream_text_chunks(text_chunks, lang):
        chunk_count += 1
        if DEBUG:
            print(f"[StreamSpeak] 🎵 Completed chunk {chunk_count}: '{audio_chunk.text[:30]}...'")
    
    if DEBUG:
        print(f"[StreamSpeak] ✅ Completed streaming {chunk_count} chunks")