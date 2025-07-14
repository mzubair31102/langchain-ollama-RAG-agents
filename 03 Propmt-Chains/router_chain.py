# department_router.py

"""
→ HIGH-LEVEL FLOW (USER INPUT TO OUTPUT)

User inputs a query:
    e.g., "Why was my salary deducted this month?"

→ [User Query]
    ↓
→ [Router Chain]
    ↓
→ [Classify Department: HR / Finance / Helpdesk / Dev]
    ↓
→ [Send Query to That Department's Assistant]
    ↓
→ [Response from Assistant]
    ↓
→ [Print the Output]
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Literal, TypedDict
from operator import itemgetter

from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# -------------------------------
# → STEP 1: LOAD ENVIRONMENT AND INIT MODEL
# -------------------------------

# → Load environment variables from .env file
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

# → Initialize Azure OpenAI Chat model
llm = AzureChatOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    temperature=0.3
)

# -------------------------------
# → STEP 2: DEFINE DEPARTMENT ASSISTANT CHAINS
# -------------------------------

# → Department descriptions
dept_defs = {
    "hr": "Questions about leave, benefits, or HR policies",
    "finance": "Questions about salary, reimbursements, deductions, budgets",
    "helpdesk": "Technical support questions or system issues",
    "dev": "Development and coding-related queries"
}

# → Create individual assistant chains per department
chains = {}
for name, desc in dept_defs.items():
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"You are the {name.upper()} Assistant: {desc}."),
        ("human", "{query}")
    ])
    chains[name] = prompt | llm | StrOutputParser()

# -------------------------------
# → STEP 3: CREATE ROUTER CHAIN TO CLASSIFY QUERY
# -------------------------------

# → Prompt to classify user query into a department
route_prompt = ChatPromptTemplate.from_messages([
    ("system", "Given a user's query, pick the best department: hr, finance, helpdesk, or dev."),
    ("human", "{query}")
])

# → Output schema
class RouteResult(TypedDict):
    destination: Literal["hr", "finance", "helpdesk", "dev"]

# → Chain that returns the department (destination)
route_chain = route_prompt | llm.with_structured_output(RouteResult) | itemgetter("destination")

# -------------------------------
# → STEP 4: BUILD ROUTER + DEPARTMENT HANDLER
# -------------------------------

# → Router extracts destination and passes original query forward
router = {
    "destination": route_chain,
    "query": RunnablePassthrough(input_key="query")
}

# → Use router to forward query to appropriate assistant chain
full_chain = router | RunnableLambda(lambda ctx: chains[ctx["destination"]])

# -------------------------------
# → STEP 5: TEST INPUTS
# -------------------------------

if __name__ == "__main__":
    test_queries = [
        "How many paid leaves am I entitled to each year?",
        "Why was my salary deducted this month?",
        "My Outlook keeps crashing, can you help?"
    ]

    for q in test_queries:
        result = full_chain.invoke({"query": q})
        print(f"\n→ {q}\n→ {result}")
