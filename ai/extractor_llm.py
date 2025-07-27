from gpt4all import GPT4All
import json

# Load GPT4All-J model (CPU only, no GPU required)
extractor = GPT4All("ggml-gpt4all-j-v1.3-groovy.bin", model_path="./extractor_model")

def extract_facts(text: str) -> dict:
    """Extract name, likes, dislikes, emotion using GPT4All-J"""
    prompt = f"""
You are an extractor. Your ONLY job is to return valid JSON.

Text: "{text}"

Extract:
- name (if user clearly says their OWN name)
- likes (things user says they like)
- dislikes (things user says they dislike)
- emotion (happy, sad, neutral)

Return ONLY JSON. No explanation.
"""

    output = extractor.generate(prompt, max_tokens=120)

    try:
        return json.loads(output.strip().split("```")[-1])
    except:
        return {"name": None, "likes": [], "dislikes": [], "emotion": "neutral"}