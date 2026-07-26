import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.api.routes import router
from server.config import CORS_ORIGINS
from server.processing.worker import job_manager

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(name)s: %(message)s",
)

LOGGER = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI): #lifespan is called when the server starts and when the server stops by FastAPI
    LOGGER.info("CSpotlight API starting up")
    yield # do nothing
    LOGGER.info("CSpotlight API shutting down")
    job_manager.shutdown()


app = FastAPI( # this is creating the fast api app
    title="CSpotlight API",
    description="Automated CS2 highlight extraction backend",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware( #add middleware to the app
    CORSMiddleware, #Cross origin resource sharing 
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router) # include router (API endpoints) in the app

@app.get("/health", tags=["system"])  #map a GET request to the /health path
async def health_check(): 
    return {"status": "ok", "service": "cspotlight-api"}
