import os
from dotenv import load_dotenv
load_dotenv()

# Ollama
from langchain_ollama import ChatOllama

# Azure OpenAI
from langchain_community.chat_models import AzureChatOpenAI


def get_llm_ollama():
    """
    Returns an instance of ChatOllama using local Ollama LLM.
    """
    base_url = "http://localhost:11434"
    model_name = "llama3.2:latest"
    return ChatOllama(base_url=base_url, model=model_name)


def get_llm_azure():
    """
    Returns an instance of AzureChatOpenAI using environment variables.
    """
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

    return AzureChatOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=endpoint,
        deployment_name=deployment,
    )
