from langchain_community.llms import Ollama
import os
from dotenv import load_dotenv

load_dotenv()

ollama_model = os.getenv("OLLAMA_MODEL")
ollama_url = os.getenv("OLLAMA_BASE_URL")

llm = Ollama(model=ollama_model, base_url=ollama_url)

def analyze_incident(log_data):
    prompt = (
        "Analyze the following incident log and suggest likely root causes "
        "and actionable mitigation steps:\n\n" + log_data
    )
    response = llm.invoke(prompt)
    return response