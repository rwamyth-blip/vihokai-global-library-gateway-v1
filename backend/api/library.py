from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from backend.library.router import LibraryRouter
from backend.library.normalizer import normalize_results
from backend.library.deduplicator import deduplicate
from backend.library.ranking import rank_results
from backend.database.repository import SearchLogRepository

router = APIRouter(prefix="/library", tags=["Library"])
library_router = LibraryRouter()

class SearchRequest(BaseModel):
    query: str = Field(..., examples=["artificial intelligence"])
    limit: int = Field(10, ge=1, le=50)
    sources: Optional[List[str]] = Field(
        None,
        description="searxng, local, openlibrary, loc, crossref, nasa, google_books, wikipedia, internet_archive, firecrawl",
    )
    enable_rerank: bool = True
    enable_dedup: bool = True

class IngestRequest(BaseModel):
    query: str
    limit: int = 10

@router.post("/search")
async def search_library(req: SearchRequest):
    raw = await library_router.search(req.query, limit=req.limit, sources=req.sources)
    norm = normalize_results(raw)
    if req.enable_dedup:
        norm = deduplicate(norm)
    if req.enable_rerank:
        norm = rank_results(norm, req.query)
    # log
    try:
        SearchLogRepository().log(req.query, len(norm))
    except: pass
    return {"query": req.query, "count": len(norm), "results": norm}

@router.get("/search")
async def search_library_get(q: str = Query(...), limit: int = 10):
    return await search_library(SearchRequest(query=q, limit=limit))

@router.post("/ingest")
async def ingest_to_rag(req: IngestRequest):
    """Search + ingest to vector DB for RAG"""
    from backend.workers.library_tasks import ingest_task
    task = ingest_task.delay(req.query, req.limit)
    return {"task_id": task.id, "status": "queued", "query": req.query}

@router.get("/providers")
def list_providers():
    return {
        "mesh": {
            "01_web": ["searxng"],
            "02_local": ["local (Qdrant index ตัวเอง)"],
            "03_library": [
                "openlibrary", "loc", "crossref", "nasa",
                "google_books", "wikipedia", "internet_archive",
            ],
            "04_ai": ["firecrawl", "exa/serper/brave (ผ่าน chat_service)"],
            "05_llm": ["groq", "gemini", "openai", "deepseek", "kimi", "claude", "meta_llama"],
            "06_rag_agents": ["research_agent", "judge_agent", "image_agent", "multi_ai_rag"],
        },
        "v1": [
            "local", "searxng", "openlibrary", "loc", "crossref", "nasa",
            "google_books", "wikipedia", "internet_archive", "firecrawl",
        ],
        "v2_planned": ["worldcat", "europeana", "hathitrust", "dpla", "openalex", "pubmed", "arxiv"],
        "v3_planned": ["esa", "semantic_scholar"],
    }
