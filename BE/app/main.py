from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine

import app.models.role
import app.models.user

from app.router.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TransitOps API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "message": "TransitOps Backend Running 🚚"
    }