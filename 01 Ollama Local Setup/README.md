
# Ollama Setup and Usage Guide

This guide provides step-by-step instructions to install Ollama on Windows or macOS, start the server, pull a model, and interact with it using API requests.

---

## 1. Install Ollama on Windows or macOS

### Windows

1. Open your browser and navigate to:  
   https://ollama.com/download

2. Download and run the Windows installer (.exe).

3. After installation, open Command Prompt or PowerShell and verify the installation:

   ```bash
   ollama --version
   ```

### macOS

1. Open Terminal.

2. Run the following command to install via Homebrew:

   ```bash
   brew install ollama
   ```

3. Once installed, verify the installation:

   ```bash
   ollama --version
   ```

---

## 2. Start the Ollama Server

Start the Ollama server locally. Keep this terminal session running:

```bash
ollama serve
```

---

## 3. Pull a Model

Download a model locally for use (e.g., `llama3.2:1b`):

```bash
ollama pull llama3.2:1b
```

---

## 4. Test the Generate API

Send a text generation request using the `/api/generate` endpoint:

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:1b",
  "prompt": "Why is the sky blue?",
  "stream": false
}'
```

---

## 5. Test the Chat Completion API

Interact with the model using chat format via the `/api/chat` endpoint:

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llama3.2:1b",
  "messages": [
    {
      "role": "user",
      "content": "Why is the sky blue?"
    }
  ],
  "stream": false
}'
```

---

## 6. List Downloaded Models

To view all locally downloaded models:

```bash
ollama list
```

---

## 7. Remove a Model

To delete an installed model:

```bash
ollama rm llama3.2:1b
```

---

## Notes

- The Ollama API runs on `http://localhost:11434` by default.
- Replace `llama3.2:1b` with any other supported model name as needed.
- Ensure `ollama serve` is running when sending API requests.

## Ollama Model Command Reference

- /set – Set session variables

- /show – Show current model info

- /load – Load a model or session

- /save – Save current session

- /clear – Clear session context

- /bye – Exit session

- /? or /help – Show command help

- /? shortcuts – Show keyboard shortcuts

---

More Info:  
Visit the official site for updates and full documentation: https://ollama.com
