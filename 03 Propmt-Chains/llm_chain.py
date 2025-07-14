import os
from pathlib import Path
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI

# -------------------------------
# → STEP 1: LOAD ENVIRONMENT VARIABLES
# -------------------------------

# → Define path to .env file and load it
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# → Fetch Azure OpenAI credentials
api_key     = os.getenv("AZURE_OPENAI_API_KEY")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")
endpoint    = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment  = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# → Validate credentials
if not all([api_key, api_version, endpoint, deployment]):
    print("→ Missing Azure OpenAI environment variables.")
    exit(1)

print("→ Azure OpenAI credentials loaded successfully.")

# -------------------------------
# → STEP 2: INITIALIZE AZURE OPENAI CHAT MODEL
# -------------------------------

# → Create instance of AzureChatOpenAI with moderate creativity
llm = AzureChatOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=endpoint,
    deployment_name=deployment,
    temperature=0.3  # → Adds slight randomness for creativity
)

print("→ Azure OpenAI Chat Model initialized.")

# -------------------------------
# → STEP 3: DEFINE PROMPT TEMPLATE
# -------------------------------

# → Create prompt template for product description generation
prompt = PromptTemplate(
    input_variables=["product"],
    template=(
        "Write a short, engaging e-commerce product description for a {product} in bullets. "
        "Keep it under 50 words."
    )
)

print("→ PromptTemplate created.")

# -------------------------------
# → STEP 4: COMBINE PROMPT AND MODEL
# -------------------------------

# → Combine prompt and LLM into a LangChain pipeline
chain = prompt | llm

print("→ LangChain pipeline (prompt → LLM) is ready.")

# -------------------------------
# → STEP 5: RUN EXAMPLE INPUT THROUGH CHAIN
# -------------------------------

# → Example product to describe
product_name = "wireless noise-canceling headphones"

# → Format the prompt to see what will be sent
formatted_prompt = prompt.format(product=product_name)
print("\n→ Full Prompt Sent to LLM:\n", formatted_prompt)

# → Invoke the chain to generate output
print("\n→ Generating product description...\n")
result = chain.invoke({"product": product_name})

# -------------------------------
# → STEP 6: DISPLAY GENERATED OUTPUT
# -------------------------------

# → Show result depending on object type
if hasattr(result, 'content'):
    print("→ Generated Product Description:\n", result.content)
else:
    print("→ Generated Product Description:\n", result)