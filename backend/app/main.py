#This runs the FastAPI app and includes the /teach route.

from fastapi import FastAPI
from app.routes import teach

app = FastAPI(
    title= "ML Teacher API",
    version="1.0"
    
)
app.include_router(teach.router)
