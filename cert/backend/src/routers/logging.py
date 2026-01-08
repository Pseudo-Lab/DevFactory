from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from ..utils.access_log import log_page_view


logging_router = APIRouter(prefix="/log", tags=["log"])


class PageViewRequest(BaseModel):
    path: str


@logging_router.post("/pageview")
async def track_page_view(payload: PageViewRequest, request: Request):
    path = payload.path.strip()
    if not path.startswith("/"):
        raise HTTPException(status_code=400, detail="path must start with '/'")

    await log_page_view(request, path)
    return {"status": "ok"}
