import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationChain

# → Load environment variables from the .env file
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# → Fetch Azure OpenAI credentials from environment
api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

if not all([api_key, api_version, endpoint, deployment]):
    print("❌ Missing Azure OpenAI environment variables.")
    exit(1)

print("✅ Azure OpenAI credentials loaded successfully.")

# → Initialize LLM
llm = AzureChatOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=endpoint,
    deployment_name=deployment,
    temperature=0.5
)

# → Setup summarization memory
memory = ConversationSummaryMemory(llm=llm, return_messages=True)

# → Conversation chain using summarization-based memory
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=False
)

# → Terminal Chatbot Loop
print("\n🤖 Chatbot Initialized with Summarization Memory")
print("Type 'exit' or 'quit' to end the chat.\n")

while True:
    user_input = input("👤 You: ")
    
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Exiting the chat. Goodbye!")
        break

    response = conversation.invoke(user_input)
    
    print("\n🧠 Summary So Far:")
    print(memory.buffer)
    
    print("\n🤖 Assistant:", response['response'])
    print("-" * 60)
