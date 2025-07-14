# ollama_chat_local.py

"""
→ This script connects to a locally running Ollama instance and sends a prompt
  using the LLaMA 3.2 model to generate a response.
"""

from langchain_ollama import ChatOllama

# -------------------------------
# → STEP 1: CONFIGURE OLLAMA CONNECTION
# -------------------------------

# → Base URL where Ollama server is running locally
base_url = "http://localhost:11434"

# → Model name as listed in your local Ollama models
model = "llama3.2:latest"  # → Ensure this matches output of `ollama list`

# -------------------------------
# → STEP 2: INITIALIZE LLM INSTANCE
# -------------------------------

# → Create ChatOllama LLM object
llm = ChatOllama(
    base_url=base_url,
    model=model
)

# -------------------------------
# → STEP 3: SEND PROMPT AND GET RESPONSE
# -------------------------------

# → User input / prompt
question = "Hi! How are you?"

# → Call the LLM with the prompt
response = llm.invoke(question)

# -------------------------------
# → STEP 4: DISPLAY RESPONSE
# -------------------------------

# → Output the response content
print("→ Response from LLaMA:\n", response.content)
