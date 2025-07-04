"""
Ollama API Testing

Before running this script, follow these steps:

1. Ensure you have installed and started Ollama on your machine.
   You can download it from: https://ollama.com/download

2. Pull the required model (e.g., llama3.2) using:
       ollama pull llama3.2

3. Check your installed models with:
       ollama list

4. Replace the "model" field below with the correct model name from your list if different.

5. Make sure the required Python package is installed:
       pip install requests
"""
import requests

BASE_URL = "http://localhost:11434"

# Test /api/generate
def test_generate():
    print("\n" + "=" * 40)
    print("TESTING: /api/generate".center(40))
    print("=" * 40)
    
    url = f"{BASE_URL}/api/generate"
    payload = {
        "model": "llama3.2:latest",
        "prompt": "Hi, how are you?",
        "stream": False
    }
    response = requests.post(url, json=payload)
    print(response.json().get("response", "No response"))

# Test /api/chat
def test_chat():
    print("\n" + "=" * 40)
    print("TESTING: /api/chat".center(40))
    print("=" * 40)

    url = f"{BASE_URL}/api/chat"
    payload = {
        "model": "llama3.2:latest",
        "messages": [
            {
                "role": "user",
                "content": "Hi, how are you?"
            }
        ],
        "stream": False
    }
    response = requests.post(url, json=payload)
    print(response.json().get("message", {}).get("content", "No response"))

if __name__ == "__main__":
    test_generate()
    test_chat()
