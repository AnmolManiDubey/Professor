# app/services/image_search.py
from app.config import SERPAPI_KEY
from serpapi import GoogleSearch

def fetch_images(topic: str, max_results: int = 3) -> list[dict]:
    params = {
        "engine": "google",
        "q": topic,
        "tbm":"isch",     # tbm=isch is google images
        "ijn":"0",      # page index 0 for the first page
        "api_key": SERPAPI_KEY
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()
    
    images_results = results.get("images_results", [])
    images = []
    
    for img in images_results[:max_results]:
        images.append({
            "image_url" : img.get("original"),
            "thumbnail": img.get("thumbnail"),
            "title" : img.get("title"),
            "source": img.get("source"),
            "link":img.get("link")
        })
    return images    
    