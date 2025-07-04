# app/routes/teach.py

from fastapi import APIRouter, HTTPException
from app.services.llm import call_groq_llm
from app.services.prompt_templates import teach_prompt_with_references
from app.services.image_search import fetch_images
from pydantic import BaseModel
from typing import List
import re

router = APIRouter()

# Define user/assistant/system message format
class Message(BaseModel):
    role: str
    content: str

# Define request body format
class Conversation(BaseModel):
    topic: str
    messages: List[Message]

# Extract markdown-style [title](url) reference links
def extract_reference_links(markdown_text: str):
    pattern = r"\[([^\]]+)\]\((https?://[^\)]+)\)"
    matches = re.findall(pattern, markdown_text)
    return [{"title": title, "url": url} for title, url in matches]

@router.post("/teach")
async def teach(conversation: Conversation):
    if not conversation.messages:
        raise HTTPException(status_code=400, detail="Conversation must include messages")

    try:
        # Add system prompt at the start of the message list
        system_prompt = {
            "role": "system",
            "content": teach_prompt_with_references(conversation.topic)
        }
        all_messages = [system_prompt] + [message.dict() for message in conversation.messages]

        # Get explanation from LLM
        explanation = await call_groq_llm(all_messages)

        # Extract markdown links (for Reference Links section)
        reference_links = extract_reference_links(explanation)

        # Run image search using topic + explanation context
        images = await fetch_images(conversation.topic, context=explanation)

        return {
            "topic": conversation.topic,
            "explanation": explanation,
            "images": images,
            "reference_links": reference_links
        }

    except Exception as e:
        print("Error in /teach:", e)
        raise HTTPException(status_code=500, detail="Internal server error")
