from openai import OpenAI
import os
import time
from dotenv import load_dotenv

load_dotenv()

# Configure OpenAI client for LM Studio
client = OpenAI(
    base_url=os.getenv("OPENAI_API_BASE", "http://localhost:1234/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "lm-studio")
)

model_name = os.getenv("MODEL_NAME", "deepseek/deepseek-r1-0528-qwen3-8b")

def validate_llm_connection():
    """Test LLM connectivity and basic functionality"""
    try:
        start_time = time.time()
        
        # Test basic connectivity
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Respond with exactly: 'LLM validation successful'"}
            ],
            temperature=0.1,
            max_tokens=50
        )
        
        end_time = time.time()
        response_time = round((end_time - start_time) * 1000, 2)  # Convert to milliseconds
        
        response_text = response.choices[0].message.content
        if response_text:
            response_text = response_text.strip()
        else:
            response_text = ""
        
        return {
            'status': 'success',
            'response_time_ms': response_time,
            'model': model_name,
            'response': response_text,
            'validation_passed': 'LLM validation successful' in response_text,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'model': model_name,
            'validation_passed': False,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }

def analyze_incident(log_data, progress_callback=None):
    """Analyze incident logs with optional progress tracking"""
    if progress_callback:
        progress_callback(10, "Initializing analysis...")
    
    prompt = (
        "Analyze the following incident log and suggest likely root causes "
        "and actionable mitigation steps:\n\n" + log_data
    )
    
    try:
        if progress_callback:
            progress_callback(30, "Sending request to LLM...")
        
        start_time = time.time()
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are an expert system administrator and incident response specialist. Analyze logs and provide clear, actionable root cause analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        if progress_callback:
            progress_callback(80, "Processing LLM response...")
        
        end_time = time.time()
        analysis_time = round(end_time - start_time, 2)
        
        result = response.choices[0].message.content or "No response received from LLM"
        
        if progress_callback:
            progress_callback(100, "Analysis complete!")
        
        # Add metadata to the response
        result += f"\n\n--- ANALYSIS METADATA ---\n"
        result += f"Model: {model_name}\n"
        result += f"Analysis Time: {analysis_time}s\n"
        result += f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}"
        
        return result
        
    except Exception as e:
        if progress_callback:
            progress_callback(100, f"Error: {str(e)}")
        
        return f"Error analyzing incident: {str(e)}\n\nPlease ensure LM Studio is running with the Local LLM Service enabled in App Settings > Developer tab."