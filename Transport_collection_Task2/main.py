# from fastapi import FastAPI

# app = FastAPI(
#     title = "Transport Collection System",
#     version = "1.0.0" 
# )
# @app.get("/")
# def home():
#     return {
#         "message" : "Tranport Collection System" 
#     }


from fastapi import FastAPI

from router.transport_collection_router import (
    router as transport_router
)


app = FastAPI(
    title="Transport Collection System ",
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