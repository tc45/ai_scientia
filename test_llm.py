import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = os.getenv("OPENROUTER_API_URL")
OPENROUTER_LLM = os.getenv("OPENROUTER_LLM")

response = requests.post(
  url=f"{OPENROUTER_API_URL}chat/completions",
  headers={
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "HTTP-Referer": "https://www.example.com", # Optional. Site URL for rankings on openrouter.ai.
    "X-Title": "Example Site", # Optional. Site title for rankings on openrouter.ai.
  },
  data=json.dumps({
    "model": OPENROUTER_LLM, # Optional
    "messages": [
      {
        "role": "user",
        "content": "What is the meaning of life?"
      }
    ]
    
  })
)

print(response.json())

