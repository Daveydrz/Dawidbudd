"""
Mock Kyutai Coordinator for testing purposes
"""
import numpy as np
from dataclasses import dataclass
from typing import Optional, Generator

@dataclass
class StreamingChunk:
    """Mock streaming chunk for testing"""
    audio_data: np.ndarray
    sample_rate: int = 16000
    chunk_id: str = "test_chunk"
    text: str = ""

class MockKyutaiCoordinator:
    """Mock coordinator for testing"""
    
    def __init__(self):
        self.active = False
    
    def generate_audio_chunks(self, text: str) -> Generator[StreamingChunk, None, None]:
        """Mock audio chunk generation"""
        # Generate simple mock audio data
        mock_audio = np.random.rand(1024).astype(np.float32)
        yield StreamingChunk(
            audio_data=mock_audio,
            sample_rate=16000,
            chunk_id="mock_chunk_1",
            text=text
        )

def get_kyutai_coordinator() -> MockKyutaiCoordinator:
    """Get mock coordinator instance"""
    return MockKyutaiCoordinator()