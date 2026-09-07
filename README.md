# VihokAI Global Library Gateway V1

Python เป็นแกนกลาง เชื่อม 4 แหล่งแรก: Open Library + Library of Congress + Crossref + NASA
พร้อมต่อยอด WorldCat, Europeana, HathiTrust, ESA ใน V2/V3 โดยเพิ่มไฟล์ใน providers/

## Architecture
Next.js -> FastAPI /library/search -> LibraryRouter (parallel search) -> normalizer -> deduplicator -> ranking -> PostgreSQL + Qdrant -> RAG Engine -> LLM -> Answer + Citations

## Run
```bash
cp .env.example .env
docker-compose up --build
# API: http://localhost:8000/docs
# Frontend: cd frontend && npm install && npm run dev
```

## Endpoints
- POST /library/search {query, limit, sources[]}
- GET /library/search?q=...
- POST /library/ingest -> Celery task embed to Qdrant
- POST /chat {message, use_library}
- GET /health

## Adding new provider (V2)
1. สร้างไฟล์ `backend/library/providers/worldcat.py` extends LibraryProvider
2. implement `search()` และ `normalize()`
3. ใน `router.py` register: self.providers_map['worldcat'] = WorldCatProvider()

License check: full-text download ต้องเช็ค license ก่อน ingest (ดู field license, full_text_available)
