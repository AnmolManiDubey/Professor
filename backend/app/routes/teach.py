#This creates the /teach endpoint.

from fastapi import APIRouter, Query, HTTPException
from app.services.llm import call_groq_llm
from app.services.prompt_templates import teach_prompt_with_references
from app.services.image_search import fetch_images


router = APIRouter()

@router.get("/teach")
async def teach(topic: str = Query(..., min_length=3)):
    prompt = teach_prompt_with_references(topic)
    
    if not prompt:
        raise HTTPException(status_code = 400, detail="Prompt must not be empty")
    
    explanation = await call_groq_llm(prompt)
    images = fetch_images(topic)
    
    # references = get_reference_links(topic)
    return {
        "topic":topic,
        "explanation":explanation,
        "images": images
        # "reference_links": references
    }
    