from fastapi import APIRouter

router = APIRouter(prefix="/interview", tags=["Interview"])

@router.get("/health")
def health():
    return {"status": "interview engine ready"}