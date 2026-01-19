import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.user import router as user_router
from app.routers.item import router as item_router
from app.routers.vineyard import router as vineyard_router
from app.database.database import engine, Base

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Tables created via migrations or manually

app = FastAPI(title="FastAPI Scaffold", version="1.0.0")

from app.config import get_settings

settings = get_settings()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(",") if settings.allowed_origins != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_router)
app.include_router(item_router)
app.include_router(vineyard_router)

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI Scaffold"}