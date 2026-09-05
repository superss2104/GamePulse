import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from server.api.routes import router
from server.config import CORS_ORIGINS
from server.processing.worker import job_manager

DEMO_VIDEOS_DIR = Path(__file__).resolve().parent / "demo_videos"
DEMO_VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(name)s: %(message)s",
)

LOGGER = logging.getLogger(__name__)


import asyncio

async def cleanup_task():
    while True:
        try:
            # Run the synchronous cleanup function in a thread to prevent blocking
            cleaned = await asyncio.to_thread(job_manager.cleanup_expired)
            if cleaned > 0:
                LOGGER.info("Swept and cleaned up %d expired jobs from the server", cleaned)
        except asyncio.CancelledError:
            break
        except Exception as e:
            LOGGER.error("Error in cleanup task: %s", e)
        await asyncio.sleep(900)  # 15 minutes


@asynccontextmanager
async def lifespan(app: FastAPI): #lifespan is called when the server starts and when the server stops by FastAPI
    LOGGER.info("CSpotlight API starting up")
    # Start the background cleanup task
    cleaner = asyncio.create_task(cleanup_task())
    yield # do nothing
    LOGGER.info("CSpotlight API shutting down")
    cleaner.cancel()
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

# Mount demo video assets as a static directory.
# Videos placed in server/demo_videos/ are served at /demo-videos/<filename>.
app.mount("/demo-videos", StaticFiles(directory=str(DEMO_VIDEOS_DIR)), name="demo-videos")

@app.get("/health", tags=["system"])  #map a GET request to the /health path
async def health_check(): 
    return {"status": "ok", "service": "cspotlight-api"}
