"""
Mock Entropy Engine for testing purposes
"""
from enum import Enum
from typing import Any, List, Dict

class EntropyLevel(Enum):
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"

class MockEntropyEngine:
    """Mock entropy engine for testing"""
    
    def __init__(self):
        self.entropy_level = EntropyLevel.MEDIUM
    
    def get_current_entropy(self) -> EntropyLevel:
        return self.entropy_level

def get_entropy_engine() -> MockEntropyEngine:
    """Get mock entropy engine instance"""
    return MockEntropyEngine()

def probabilistic_select(items: List[Any], entropy_level: EntropyLevel = EntropyLevel.MEDIUM) -> Any:
    """Mock probabilistic selection"""
    if not items:
        return None
    return items[0]  # Just return first item for testing

def inject_consciousness_entropy(context: Dict[str, Any], entropy_level: EntropyLevel = EntropyLevel.MEDIUM) -> Dict[str, Any]:
    """Mock consciousness entropy injection"""
    context["entropy_level"] = entropy_level.value
    return context