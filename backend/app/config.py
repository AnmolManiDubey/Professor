# loads api keys from .env

import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_BASE_URL = os.getenv("GROQ_BASE_URL")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")