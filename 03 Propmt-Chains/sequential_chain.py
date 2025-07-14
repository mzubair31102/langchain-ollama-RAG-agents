from pathlib import Path
import os
from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import ChatPromptTemplate

# -------------------------------
# → LOAD ENVIRONMENT VARIABLES
# -------------------------------

# → Define path to .env file and load it
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# → Fetch Azure OpenAI credentials from environment
api_key     = os.getenv("AZURE_OPENAI_API_KEY")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")
endpoint    = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment  = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# -------------------------------
# → INITIALIZE AZURE OPENAI MODEL
# -------------------------------

# → Create an instance of AzureChatOpenAI
llm = AzureChatOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=endpoint,
    deployment_name=deployment
)

# -------------------------------
# → USER'S PROFESSIONAL BIO
# -------------------------------

# → This is the input bio used in all prompt chains
bio = (
    "I'm a cloud engineer with 5 years of experience working with Azure, Kubernetes, and serverless functions. "
    "I’ve built scalable APIs and automated infrastructure for multiple SaaS platforms. "
    "I’m certified in Azure DevOps and specialize in CI/CD pipelines and security monitoring."
)

# -------------------------------
# → STEP 1: CREATE LINKEDIN HEADLINE
# -------------------------------

# → Prompt to generate a catchy LinkedIn-style headline
headline_prompt = ChatPromptTemplate.from_template(
    "Create a short, catchy LinkedIn-style professional headline for this bio:\n\n{bio}"
)

# → Chain to process headline
chain_one = LLMChain(
    llm=llm,
    prompt=headline_prompt,
    output_key="headline"
)

# -------------------------------
# → STEP 2: GENERATE ONE-PARAGRAPH PITCH
# -------------------------------

# → Prompt to summarize bio into a strong one-paragraph pitch
pitch_prompt = ChatPromptTemplate.from_template(
    "Summarize this professional bio into a compelling 1-paragraph pitch:\n\n{bio}"
)

# → Chain to process pitch
chain_two = LLMChain(
    llm=llm,
    prompt=pitch_prompt,
    output_key="pitch"
)

# -------------------------------
# → STEP 3: JOB APPLICATION MESSAGE
# -------------------------------

# → Prompt to convert the pitch into a job application message
job_message_prompt = ChatPromptTemplate.from_template(
    "Use the following pitch to write a short job application message:\n\n{pitch}"
)

# → Chain to generate job message
chain_three = LLMChain(
    llm=llm,
    prompt=job_message_prompt,
    output_key="job_message"
)

# -------------------------------
# → COMBINE ALL CHAINS SEQUENTIALLY
# -------------------------------

# → Create a sequential pipeline with data dependency between chains
chain = SequentialChain(
    chains=[chain_one, chain_two, chain_three],
    input_variables=["bio"],
    output_variables=["headline", "pitch", "job_message"],
    verbose=True
)

# -------------------------------
# → RUN THE CHAIN
# -------------------------------

# → Run the full workflow using the professional bio
result = chain({"bio": bio})

# -------------------------------
# → DISPLAY FINAL OUTPUT
# -------------------------------

print("\n→ Final Output")
print("→ LinkedIn Headline:", result["headline"])
print("\n→ 1-Paragraph Pitch:\n", result["pitch"])
print("\n→ Job Application Message:\n", result["job_message"])
