from fastapi import FastAPI

from router.transport_collection_router import (
    router as transport_router
)


app = FastAPI(
    title="Transport Collection System Updated",
    description=(
        "FastAPI + PostgreSQL "
        "Transport Collection Management System"
    ),
    version="1.0.0"
)


app.include_router( transport_router )

@app.get("/")
async def home():
    return {
        "message":
        "Transport Collection API is running"
    }