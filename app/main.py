import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.routers.user import router as user_router
from app.routers.item import router as item_router
from app.routers.vineyard import router as vineyard_router
from app.routers.terreno import router as terreno_router
from app.database.database import engine, Base

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Tables created via migrations or manually

limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

app = FastAPI(title="FastAPI Scaffold", version="1.0.0")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

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
app.include_router(terreno_router)

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI Scaffold"}