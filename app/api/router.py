from fastapi import APIRouter

from app.api.endpoints.relevance_endpoint import relevancy_router

api_router = APIRouter()

api_router.include_router(
    relevancy_router,
    tags=["Check Relevance of ICD and CPT codes"]
)
