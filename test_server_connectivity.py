#!/usr/bin/env python3
"""
LLM Server Connectivity Test
Tests both port 5001 (Main LLM) and port 5002 (Gemma Consciousness)
"""

import requests
import json
import time

def test_port_5001():
    """Test main LLM on port 5001"""
    print("🎯 Testing Main LLM (Port 5001)...")
    
    try:
        url = "http://localhost:5001/api/v1/generate"
        data = {
            "prompt": "Hello, respond with just 'Working'",
            "max_length": 50,
            "temperature": 0.0
        }
        
        response = requests.post(url, json=data, timeout=10)
        if response.status_code == 200:
            print("✅ Port 5001: Main LLM is running")
            return True
        else:
            print(f"❌ Port 5001: HTTP {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Port 5001: Connection refused - LLM server not running")
        return False
    except Exception as e:
        print(f"❌ Port 5001: {e}")
        return False

def test_port_5002():
    """Test Gemma consciousness on port 5002"""
    print("🧠 Testing Gemma Consciousness (Port 5002)...")
    
    try:
        url = "http://localhost:5002/api/v1/generate"
        data = {
            "prompt": "Respond with just 'Consciousness Active'",
            "max_length": 50,
            "temperature": 0.0
        }
        
        response = requests.post(url, json=data, timeout=10)
        if response.status_code == 200:
            print("✅ Port 5002: Gemma Consciousness is running")
            return True
        else:
            print(f"❌ Port 5002: HTTP {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Port 5002: Connection refused - Gemma server not running")
        return False
    except Exception as e:
        print(f"❌ Port 5002: {e}")
        return False

def test_kokoro_api():
    """Test Kokoro TTS API"""
    print("🎵 Testing Kokoro TTS (Port 8880)...")
    
    try:
        url = "http://127.0.0.1:8880/api/tts"
        data = {
            "text": "Test",
            "voice": "af_heart"
        }
        
        response = requests.post(url, json=data, timeout=5)
        if response.status_code == 200:
            print("✅ Port 8880: Kokoro TTS is running")
            return True
        else:
            print(f"❌ Port 8880: HTTP {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Port 8880: Connection refused - Kokoro server not running")
        return False
    except Exception as e:
        print(f"❌ Port 8880: {e}")
        return False

def main():
    print("🚀 BUDDY LLM SERVER CONNECTIVITY TEST")
    print("="*50)
    
    results = {
        "main_llm": test_port_5001(),
        "gemma_consciousness": test_port_5002(),
        "kokoro_tts": test_kokoro_api()
    }
    
    print("\n📊 CONNECTIVITY RESULTS:")
    print("="*30)
    
    for service, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {service.replace('_', ' ').title()}: {'ONLINE' if status else 'OFFLINE'}")
    
    online_count = sum(results.values())
    total_count = len(results)
    
    print(f"\n🎯 Overall: {online_count}/{total_count} services online")
    
    if online_count == total_count:
        print("🎉 ALL SERVICES ONLINE - Buddy is ready!")
    elif results["main_llm"] and results["gemma_consciousness"]:
        print("👍 CORE SERVICES ONLINE - Buddy will work (voice may be silent)")
    elif results["main_llm"]:
        print("⚠️  MAIN LLM ONLY - Limited consciousness features")
    else:
        print("🚨 CRITICAL SERVICES OFFLINE - Buddy will not work properly")
        
        print("\n🔧 TO START SERVERS:")
        if not results["main_llm"]:
            print("  Main LLM (Port 5001): Start your LLM server (e.g., Ollama, KoboldCPP, etc.)")
        if not results["gemma_consciousness"]:
            print("  Gemma (Port 5002): Start Gemma-2-2B server for consciousness processing")
        if not results["kokoro_tts"]:
            print("  Kokoro (Port 8880): Start Kokoro-FastAPI TTS server")

if __name__ == "__main__":
    main()
