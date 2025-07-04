# LangChain Module 02


## Overview of LangChain

LangChain is an open-source framework designed to make it easier to build applications powered by large language models. It offers support for prompt management, model integrations, chaining logic, memory management, and tracing.

LangChain is modular and extensible. It supports several popular model providers including OpenAI, Google, Hugging Face, Cohere, and others. It allows you to use models either through chat-style messaging or traditional completion prompts.

---

## Overview of LangGraph

LangGraph extends LangChain with capabilities to build stateful applications using graph-based workflows. It is particularly useful when developing multi-agent systems, decision-making pipelines, and control flow logic involving conditional branches and loops.

LangGraph works seamlessly with LangChain components, offering more structure and control for complex use cases.

---

## Objective of This Module

The goal of this module is to help you understand how to:

- Use chat models through LangChain
- Define and apply prompt templates
- Structure inputs and outputs as messages
- Enable observability using LangSmith

By the end of this module, you will have a working LLM-powered translation application that demonstrates the core principles of prompt engineering and chat model invocation.

---

## Environment Setup Using Visual Studio Code (VS Code)

Follow these steps to prepare your development environment:

### 1. Install Visual Studio Code

If you do not already have VS Code installed, download and install it from the official website:

https://code.visualstudio.com/

### 2. Install Python

Ensure Python 3.8 or higher is installed on your system. You can verify this by running the following command in the terminal:

```bash
python --version
```
### 3. Create a Virtual Environment

Create a virtual environment for your project using the following command:

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

Activate the virtual environment by running the following command:

```bash
For Windows 
venv\Scripts\activate

For macOS
source venv/bin/activate
```
### 5.Create a requirements.txt file

Create a requirements.txt file to specify the required Python packages for your project.

```bash
pip freeze > requirements.txt
```
### 6.Add the following to requirements.txt

```bash
langchain
LangSmith
python-dotenv
```
### 7. Install Dependencies

Install the required dependencies by running the following command:

```bash
pip install -r requirements.txt
```
### 8. Dependency Version Control
Initially, the requirements.txt file includes all required Python packages without specifying exact versions. This allows for flexibility during development and ensures compatibility with the latest releases.

If you wish to lock your environment to the exact versions you used after installation, follow these steps:

Open your terminal within the activated virtual environment.

Run the following command:

```bash
pip freeze > requirements.txt
```

This will generate a new requirements.txt file that contains the exact package versions used during installation. You can commit this file to your version control system for future reference.

Once you have locked the dependencies, you can use the requirements.txt file to install the exact versions specified in the file.

### 9. Create a .env File
EVN file is used to store the API keys and other sensitive information that should not be committed to version control.
.env is ignored by Git and is not tracked in version control. It is a good practice to keep your API keys and other sensitive information in a separate file that is not committed to version control.

Create .env file 

### 11. Create .gitignore and Add:
.gitignore
 
In File Add the following:

```
# Ignore virtual environment
venv/

# Ignore environment variables
.env
```


### 10.Installation
The LangChain Ollama integration lives in the langchain-ollama package:
```bash
pip install -qU langchain-ollama
```
Make sure you're using the latest Ollama version for structured outputs. Update by running:

```bash
pip install -U ollama
```
Run the following command:

Update Package versions in requirements.txt

```bash
pip freeze > requirements.txt
```
### 11. Run the Python Script
```bash
langchain_local_chat_test.py
```
### What’s Happening?

- ChatOllama(...): Connects your Python code to the locally running Ollama server.
- llm.invoke(...): Sends your question to the AI model.
- response.content: Contains the AI's reply (just like ChatGPT's response).
- print(...): Displays the reply in the terminal.