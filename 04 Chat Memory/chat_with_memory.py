import os
import json
from pathlib import Path
from dotenv import load_dotenv

from sqlalchemy import create_engine, MetaData, Table, select, distinct
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate, SystemMessagePromptTemplate,
    HumanMessagePromptTemplate, MessagesPlaceholder
)
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory

# → Load environment variables from .env file
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

# → Fetch required Azure OpenAI credentials
api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# → Validate credentials
if not all([api_key, api_version, endpoint, deployment]):
    print("Missing Azure credentials.")
    exit(1)

print("Azure credentials ready.")

# → Initialize the AzureChatOpenAI model
llm = AzureChatOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=endpoint,
    deployment_name=deployment,
    temperature=0.5,  # Adjusts randomness of response
)

# → Construct the system and human prompt templates
system_prompt = SystemMessagePromptTemplate.from_template(
    "You are a helpful assistant. Ask user name & email and remember them."
)
human_prompt = HumanMessagePromptTemplate.from_template("{input}")

# → Define the full chat prompt, including prior message history
prompt = ChatPromptTemplate.from_messages([
    system_prompt,
    MessagesPlaceholder(variable_name="history"),
    human_prompt,
])

# → Create the final processing chain (Prompt → LLM → OutputParser)
chain = prompt | llm | StrOutputParser()

# → Define SQLite DB path and create SQLAlchemy engine
db_path = Path(__file__).resolve().parent / "chat_history.db"
engine = create_engine(f"sqlite:///{db_path}")

# → Function to fetch chat history for a given session
def get_history(session_id: str):
    return SQLChatMessageHistory(session_id=session_id, connection=engine)

# → Wrap chain with message history tracking
with_history = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=get_history,     # Custom history retriever
    input_messages_key="input",          # Key in input dict for current user message
    history_messages_key="history",      # Key for where to inject message history
)

# → Main chat function that accepts user input and session ID
def chat(user_input: str, session_id: str = "default"):
    return with_history.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": session_id}}  # Session-based memory
    )

# → Utility function to fetch and print all session histories in JSON format
def print_all_sessions_json():
    meta = MetaData()
    meta.reflect(bind=engine, only=["message_store"])  # Reflect only the required table
    tbl = Table("message_store", meta, autoload_with=engine)

    with engine.connect() as conn:
        # → Fetch all distinct session IDs
        session_ids = [row[0] for row in conn.execute(select(distinct(tbl.c.session_id)))]
        for sid in session_ids:
            hist = SQLChatMessageHistory(session_id=sid, connection=engine)
            msgs = hist.get_messages()
            # → Format messages into a simple JSON list
            messages_json = [{"role": m.type, "content": m.content} for m in msgs]
            print(f"\n→ Session '{sid}' history:")
            print(json.dumps(messages_json, indent=2))

# → Sample usage and testing
if __name__ == "__main__":
    sess1 = "session_A"
    sess2 = "session_B"

    # → Simulate user interaction in session A
    print("→", chat("Hi there", session_id=sess1))
    print("→", chat("My name is Alice", session_id=sess1))

    # → Simulate user interaction in session B
    print("→", chat("Hello", session_id=sess2))
    print("→", chat("What's your name?", session_id=sess2))

    # → Continue chatting in session A
    print("→", chat("What's my name?", session_id=sess1))

    # → Output all session histories
    print_all_sessions_json()
