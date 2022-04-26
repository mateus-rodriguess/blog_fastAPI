import os 
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from app.models import user_models
from app.views.user_views import user_router

from .database import SessionLocal, engine

load_dotenv()
# create tables
user_models.Base.metadata.create_all(bind=engine)

app = FastAPI(openapi_url="/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.router.prefix = "/api/v1"

app.include_router(user_router, prefix="/users")


@app.get("/")
async def main():
    """
    redirect / for docs api
    """
    return RedirectResponse(url="/docs/")
