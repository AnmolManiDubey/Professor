#This file handles Groq’s LLaMA 3 call using httpx.

import httpx
from app.config import GROQ_API_KEY, GROQ_BASE_URL

async def call_groq_llm(prompt: str, model: str = "llama3-70b-8192") -> str:
    headers = {
        "Authorization" : f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload ={
        "model" : model,
        "messages": [
            {"role": "system","content": "You are a helpful ML assistant."},
            {"role": "user", "content": prompt}
            ],
        "temperature":0.7
    }
        
    
    
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{GROQ_BASE_URL}/chat/completions", json = payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    