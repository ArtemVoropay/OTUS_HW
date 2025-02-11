from fastapi import APIRouter

router = APIRouter()

@router.get("/health/", tags = ["health"], description='Check health')
async def health():
   return {'status': "OK"}
