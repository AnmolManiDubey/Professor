# app/services/image_search.py

import re
import asyncio
from functools import partial
from app.config import SERPAPI_KEY
from serpapi import GoogleSearch


def _get_images_sync(params):
    search = GoogleSearch(params)
    return search.get_dict()


def get_context_summary(text: str, max_chars: int = 150) -> str:
    """
    Extract a short summary from LLM explanation.
    Tries to get the first line under **Summary** or **Definition**.
    """
    # Look for **Summary** section
    match = re.search(r"\*\*Summary\*\*[\s\S]*?\n(.+?)(?:\n|$)", text)
    if not match:
        # Fallback: **Definition**
        match = re.search(r"\*\*Definition\*\*[\s\S]*?\n(.+?)(?:\n|$)", text)
    summary = match.group(1) if match else ""

    return summary.strip()[:max_chars] if summary else ""


async def fetch_images(topic: str, context: str = "", max_results: int = 3) -> list[dict]:
    """
    Perform a context-aware Google image search using SerpAPI.
    Combines topic with summary from LLM explanation.
    """
    # Extract context-aware keywords
    context_summary = get_context_summary(context)
    fallback_context = "machine learning" if "machine learning" not in topic.lower() else ""
    final_query = f"{topic} {fallback_context} {context_summary}".strip()

    # Prepare query params
    params = {
        "engine": "google",
        "q": final_query,
        "tbm": "isch",      # Image search
        "ijn": "0",         # First page
        "api_key": SERPAPI_KEY,
    }

    # Run sync call in background thread
    loop = asyncio.get_event_loop()
    try:
        results = await loop.run_in_executor(None, partial(_get_images_sync, params))
        images_results = results.get("images_results", [])
    except Exception as e:
        print("Image search error:", e)
        return []

    # Extract and format top N images
    images = []
    for img in images_results[:max_results]:
        if not img.get("original"):
            continue
        images.append({
            "image_url": img.get("original"),
            "thumbnail": img.get("thumbnail"),
            "title": img.get("title"),
            "source": img.get("source"),
            "link": img.get("link"),
        })

    return images


#How this works:
# get_context_summary() extracts a short meaningful summary from the LLM output (either from Summary or Definition).

# fetch_images() uses that summary plus the topic plus "machine learning" keyword to form a targeted Google image search query.

# The search runs asynchronously to avoid blocking your FastAPI event loop.