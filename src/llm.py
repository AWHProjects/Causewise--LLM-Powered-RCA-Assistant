from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Configure OpenAI client for LM Studio
client = OpenAI(
    base_url=os.getenv("OPENAI_API_BASE", "http://localhost:1234/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "lm-studio")
)

model_name = os.getenv("MODEL_NAME", "deepseek/qwen2-8b")

def analyze_incident(log_data):
    prompt = (
        "Analyze the following incident log and suggest likely root causes "
        "and actionable mitigation steps:\n\n" + log_data
    )
    
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are an expert system administrator and incident response specialist. Analyze logs and provide clear, actionable root cause analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error analyzing incident: {str(e)}\n\nPlease ensure LM Studio is running with the Local LLM Service enabled in App Settings > Developer tab."