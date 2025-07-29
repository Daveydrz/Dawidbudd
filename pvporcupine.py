# Mock pvporcupine module for testing
class Porcupine:
    def __init__(self, keywords=['buddy']):
        self.keywords = keywords
    
    def process(self, data):
        return -1  # No keyword detected
    
    def delete(self):
        pass

def create(**kwargs):
    return Porcupine()