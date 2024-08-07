from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import v1_router
from app.core.logging_config import configure_logging
from app.core.settings import get_settings

# Env set up
load_dotenv()
settings = get_settings()
configure_logging()

# Initialize the app
app = FastAPI(openapi_url=settings.openapi_url)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add the routers
app.include_router(v1_router, prefix="/api/v1")
