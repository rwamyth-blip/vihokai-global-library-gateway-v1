import pytest, asyncio
from backend.library.router import LibraryRouter

@pytest.mark.asyncio
async def test_search():
    router = LibraryRouter()
    res = await router.search("ai", limit=2)
    assert isinstance(res, list)
