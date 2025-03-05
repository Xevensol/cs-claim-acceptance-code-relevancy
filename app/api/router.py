from fastapi import APIRouter
# from app.api.endpoints.icd_codes_endpoint import router
from app.api.endpoints.relevance_endpoint import router

api_router = APIRouter()

api_router.include_router(router, tags=["check relevance of ICD and CPT codes"])