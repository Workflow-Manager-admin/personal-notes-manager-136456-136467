from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import Base
from .db import engine
from .routes_auth import router as auth_router
from .routes_notes import router as notes_router

openapi_tags = [
    {
        "name": "Authentication",
        "description": "Register, login, and view user account endpoints.",
    },
    {
        "name": "Notes",
        "description": "CRUD and search endpoints for notes.",
    },
]

app = FastAPI(
    title="Personal Notes Manager API",
    description="A backend for securely managing user notes with authentication and full CRUD/search.",
    version="1.0.0",
    openapi_tags=openapi_tags,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create all DB tables at startup if not exist
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(notes_router)

@app.get("/", tags=["Utility"])
def health_check():
    """Check if the Notes Manager backend is healthy."""
    return {"message": "Healthy"}
