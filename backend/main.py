from fastapi import FastAPI, Depends, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from database.database import get_db
from repository.protein_repository import ProteinRepository
from services.protein_service import ProteinService
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from exceptions import AppError
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
app = FastAPI(
    title = "Protein Visualisation API", 
    description = "API for visualizing protein features, isoforms, and interactions", 
    version = "1.0.0"
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ORIGIN", "http://localhost:5173")],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def unified_error_handler(request: Request, exc: Exception):
    if isinstance(exc, AppError):
        # Expected: we raised this deliberately, safe to expose detail/extra
        status_code = exc.status_code
        title = exc.title
        type_ = exc.type_
        detail = exc.detail
        extra = exc.extra
    else:
        # Unexpected: log the real thing server-side, don't leak internals to the client
        logger.exception("Unhandled exception on %s", request.url)
        status_code = 500
        title = "Internal Server Error"
        type_ = "about:blank"
        detail = "An unexpected error occurred."
        extra = {}

    return JSONResponse(
        status_code=status_code,
        content={
            "type": type_,
            "title": title,
            "status": status_code,
            "detail": detail,
            "instance": str(request.url),
            **extra,
        },
        media_type="application/problem+json",
    )
    
def get_protein_service(session: AsyncSession = Depends(get_db)):
    repo = ProteinRepository(session)
    return ProteinService(repo)

@app.get("/proteins")
async def get_proteins(
    query: str = Query(default="", description="Search query for protein name, gene symbol, or protein ID", max_length=100),
    limit: int = Query(default=10, description="Maximum number of results to return", le=100),
    protein_service: ProteinService = Depends(get_protein_service)
):  
    return await protein_service.get_proteins(query, limit)

@app.get("/proteins/{protein_id}/feature-map")
async def get_feature_map(
    protein_id: str,
    protein_service: ProteinService = Depends(get_protein_service)
):
    return await protein_service.get_feature_map(protein_id)

@app.get("/proteins/{protein_id}/protein-expressions")
async def get_protein_expressions(
    protein_id: str,
    protein_service: ProteinService = Depends(get_protein_service)
):
    return await protein_service.get_protein_expressions(protein_id)

@app.get("/proteins/{protein_id}/interactions")
async def get_protein_interactions(
    protein_id: str,
    protein_service: ProteinService = Depends(get_protein_service)
):
    return await protein_service.get_protein_interactions(protein_id)

@app.get("/proteins/{protein_id}/details")
async def get_protein(
    protein_id: str,
    protein_service: ProteinService = Depends(get_protein_service)
):
    return await protein_service.get_protein_details(protein_id)
