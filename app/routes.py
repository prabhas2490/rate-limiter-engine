from fastapi import APIRouter
from pydantic import BaseModel
from app.algorithms import token_bucket

router = APIRouter()

class RateLimitRequest(BaseModel):
    client_id: str
    limit: int
    window: int
# POST /check - returns allowed/blocked decision for incoming request
@router.post("/check")
def check_rate_limit(request: RateLimitRequest):
    result = token_bucket(
        client_id=request.client_id,
        limit=request.limit,
        window=request.window
    )
    if not result["allowed"]:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    return result
