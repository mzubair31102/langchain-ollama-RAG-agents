import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain_core.output_parsers import StrOutputParser

# → Load environment variables from the .env file
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# → Fetch Azure OpenAI credentials from environment
api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# → Check if all credentials are available
if not all([api_key, api_version, endpoint, deployment]):
    print("Missing Azure OpenAI environment variables.")
    exit(1)

print("Azure OpenAI credentials loaded successfully.")

# → Initialize Azure Chat Model using LangChain
llm = AzureChatOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=endpoint,
    deployment_name=deployment,
    temperature=0.5  # Controls randomness of output
)

# -------------------------------
# → PROMPT TEMPLATE: Define assistant's behavior
# -------------------------------

# → System prompt to guide the assistant's initial behavior
system_prompt = SystemMessagePromptTemplate.from_template(
    "You are a helpful assistant. Start every conversation by greeting the user and asking for their name and email."
)

# → Human prompt will hold dynamic user input
human_prompt = HumanMessagePromptTemplate.from_template("{user_input}")

# → Combine system and human prompts into a single chat prompt
chat_prompt = ChatPromptTemplate.from_messages([
    system_prompt,
    human_prompt
])

# → Create the final chain: Prompt → LLM → Output Parser
chain = chat_prompt | llm | StrOutputParser()

# -------------------------------
# → TEST CASES: Run test conversations
# -------------------------------

print("\n→ TEST 1: Start conversation")
response1 = chain.invoke({"user_input": "Hi"})
print("→", response1)

print("\n→ TEST 2: Provide name and email")
response2 = chain.invoke({"user_input": "My name is Zubair and my email is zubair@example.com"})
print("→", response2)

print("\n→ TEST 3: Ask what is my name and email?")
response3 = chain.invoke({"user_input": "What is my name and email?"})
print("→", response3)