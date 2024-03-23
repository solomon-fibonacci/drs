import logging
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from apis.datastore.service.factory import get_datastore

logger = logging.getLogger(__name__)
all_origins = ["*"]

router = APIRouter()


class HealthResponse(BaseModel):
    status: str


@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="ok")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Merchmaker API",
        description="API for the Merchmaker service",
        version="0.1",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=all_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router, prefix="/api", tags=["api"])

    return app


app = create_app()
