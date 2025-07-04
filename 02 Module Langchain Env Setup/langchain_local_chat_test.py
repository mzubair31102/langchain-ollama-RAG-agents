from langchain_ollama import ChatOllama

base_url = "http://localhost:11434"
model = "llama3.2:latest"  # Correct model name from your local list

llm = ChatOllama(base_url=base_url, model=model)

question = "Hi! How are you?"
response = llm.invoke(question)
print(response.content)
