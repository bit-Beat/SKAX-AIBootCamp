### AI
import os
import configparser
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings

current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, "config.ini")
config = configparser.ConfigParser()
config.read(config_path)

llm = AzureChatOpenAI(
    openai_api_version="2024-02-01",
    azure_deployment=config['LLM']['AOAI_DEPLOY_GPT4O_MINI'],
    temperature=0.0,
    api_key=config['LLM']['AOAI_API_KEY'],
    azure_endpoint = config['LLM']['AOAI_ENDPOINT'],
)

embeddings = AzureOpenAIEmbeddings(
    model = config['LLM']['AOAI_DEPLOY_EMBED_3_SMALL'],
    openai_api_version='2024-02-01',
    api_key = config['LLM']['AOAI_API_KEY'],
    azure_endpoint = config['LLM']['AOAI_ENDPOINT']
)
