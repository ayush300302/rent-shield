import os
import json
import re
from dotenv import load_dotenv

# Load .env file from the root folder if it exists
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(ROOT_DIR, '.env')
load_dotenv(dotenv_path)

def get_env_var(key: str, default: str = None) -> str:
    """Get environment variable or fallback to default."""
    return os.getenv(key, default)

def parse_json_from_llm(text: str) -> dict:
    """Extract and parse JSON content from an LLM response string."""
    text = text.strip()
    # Try finding JSON block in markdown
    match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL | re.IGNORECASE)
    if match:
        text = match.group(1)
    else:
        # Fallback to finding first brace and last brace
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            text = text[start:end+1]
    
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON from response: {text}. Error: {str(e)}")
