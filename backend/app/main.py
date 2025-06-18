#This runs the FastAPI app and includes the /teach route.

from fastapi import FastAPI
from app.routes import teach
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(
    title= "ML Teacher API",
    version="1.0"
    
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev; restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(teach.router)
