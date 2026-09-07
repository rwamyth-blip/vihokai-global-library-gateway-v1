from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import library as library_api
from backend.api import health as health_api
from backend.api import chat as chat_api
from backend.database.database import init_db
from backend.vector_db.client import get_qdrant_client
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        init_db()
        print("✓ DB initialized")
    except Exception as e:
        print(f"DB init skip: {e}")
    try:
        client = get_qdrant_client()
        from backend.vector_db.collections import ensure_collections
        ensure_collections(client)
        print("✓ Qdrant ready")
    except Exception as e:
        print(f"Qdrant init skip: {e}")
    yield

app = FastAPI(
    title="VihokAI Global Library Gateway",
    version="1.0.0",
    description="Global Library Search + RAG Gateway - Open Library, LOC, Crossref, NASA",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_api.router)
app.include_router(library_api.router)
app.include_router(chat_api.router)

@app.get("/")
def root():
    return {
        "service": "VihokAI Global Library Gateway",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "library": "/library/search",
        "chat": "/chat"
    }
