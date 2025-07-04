import httpx
from app.config import GROQ_API_KEY, GROQ_BASE_URL

async def call_groq_llm(
    messages: list, 
    model: str = "llama3-70b-8192"
) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    # Prepend system message if not present
    if not messages or messages[0].get("role") != "system":
        messages = [{"role": "system", "content": "You are a helpful ML assistant."}] + messages

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.4,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{GROQ_BASE_URL}/chat/completions", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
