# ollama_api_test.py

"""
→ OLLAMA API TESTING GUIDE

Before running this script:

→ 1. Install and start Ollama on your machine:
       https://ollama.com/download

→ 2. Pull the desired model (e.g., llama3.2):
       ollama pull llama3.2

→ 3. Confirm your local models:
       ollama list

→ 4. Update the "model" field below if using a different name

→ 5. Install the required Python package:
       pip install requests
"""

import requests

# -------------------------------
# → BASE CONFIGURATION
# -------------------------------

# → URL where local Ollama server is running
BASE_URL = "http://localhost:11434"

# -------------------------------
# → FUNCTION: TEST /api/generate ENDPOINT
# -------------------------------

def test_generate():
    print("\n" + "=" * 40)
    print("→ TESTING: /api/generate".center(40))
    print("=" * 40)
    
    url = f"{BASE_URL}/api/generate"
    payload = {
        "model": "llama3.2:latest",  # → Ensure this matches your local model name
        "prompt": "Hi, how are you?",
        "stream": False
    }

    # → Send request
    response = requests.post(url, json=payload)

    # → Print response
    print("→ Response:\n", response.json().get("response", "No response returned."))

# -------------------------------
# → FUNCTION: TEST /api/chat ENDPOINT
# -------------------------------

def test_chat():
    print("\n" + "=" * 40)
    print("→ TESTING: /api/chat".center(40))
    print("=" * 40)

    url = f"{BASE_URL}/api/chat"
    payload = {
        "model": "llama3.2:latest",  # → Ensure this matches your local model name
        "messages": [
            {
                "role": "user",
                "content": "Hi, how are you?"
            }
        ],
        "stream": False
    }

    # → Send request
    response = requests.post(url, json=payload)

    # → Print response
    print("→ Response:\n", response.json().get("message", {}).get("content", "No response returned."))

# -------------------------------
# → MAIN ENTRY POINT
# -------------------------------

if __name__ == "__main__":
    test_generate()
    test_chat()
