import os
import atexit
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine

from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory

# -------------------------------
# → LOAD ENVIRONMENT VARIABLES
# -------------------------------

# → Load environment variables from the .env file
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# → Fetch Azure OpenAI credentials
api_key    = os.getenv("AZURE_OPENAI_API_KEY")
api_ver    = os.getenv("AZURE_OPENAI_API_VERSION")
endpoint   = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# → Check if all required values are present
if not all([api_key, api_ver, endpoint, deployment]):
    print("Missing Azure credentials.")
    exit(1)

# -------------------------------
# → PROMPT TEMPLATE: Assistant Behavior
# -------------------------------

# → System-level prompt to guide assistant behavior
system_prompt = SystemMessagePromptTemplate.from_template(
    "You are a helpful assistant. Ask for the user's name and email, and remember them."
)

# → User message template
human_prompt = HumanMessagePromptTemplate.from_template("{input}")

# → Message chain with memory placeholder
messages = [system_prompt, MessagesPlaceholder("history"), human_prompt]
prompt = ChatPromptTemplate.from_messages(messages)

# -------------------------------
# → INITIALIZE LLM AND CHAIN
# -------------------------------

# → Set up AzureChatOpenAI model
llm = AzureChatOpenAI(
    api_key=api_key,
    api_version=api_ver,
    azure_endpoint=endpoint,
    deployment_name=deployment,
    temperature=0.5  # → Controls randomness of output
)

# → Chain: Prompt → LLM → OutputParser
chain = prompt | llm | StrOutputParser()

# -------------------------------
# → SQLITE-BASED MESSAGE HISTORY
# -------------------------------

# → Initialize database connection using SQLAlchemy
engine = create_engine("sqlite:///chat_history.db", future=True)

# → Function to return SQL-based chat history per session
def get_history(session_id: str):
    return SQLChatMessageHistory(session_id=session_id, connection=engine)

# → Wrap the LLM chain with session-aware message history
with_history = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=get_history,
    input_messages_key="input",
    history_messages_key="history"
)

# -------------------------------
# → FUNCTION: CHAT HANDLER
# -------------------------------

# → Handles user input with persistent message memory per session
def chat(session_id: str, user_input: str):
    return with_history.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": session_id}}
    )

# -------------------------------
# → CLEANUP HOOK (OPTIONAL)
# -------------------------------

# → This is optional because SQLChatMessageHistory saves instantly
def cleanup():
    print("→ Cleanup executed. No in-memory buffer to flush due to SQL-based persistence.")

atexit.register(cleanup)

# -------------------------------
# → SAMPLE USAGE
# -------------------------------

if __name__ == "__main__":
    sid = "user_1283"

    # → Simulate conversation with assistant
    print("→", chat(sid, "Hi"))
    print("→", chat(sid, "My name is Zubair and my email is zubair@example.com"))
    print("→", chat(sid, "What's my name?"))
    print("→", chat(sid, "What's my email?"))
