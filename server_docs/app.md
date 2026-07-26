# `server/app.py`

## File Overview

- Purpose: FastAPI application entry point.
- Why it exists: Initializes the server, configures middleware, and registers routes.
- Architecture fit: The root of the backend application that ties all components together.

## Detailed Walkthrough

- `lifespan(app)`: Handles startup and shutdown hooks, ensuring graceful shutdown of the job manager.
- `app = FastAPI(...)`: Initializes the FastAPI application with metadata.
- `app.add_middleware(...)`: Configures CORS using `CORS_ORIGINS` from `config.py` to allow frontend requests.
- `app.include_router(router)`: Mounts the API endpoints defined in `api/routes.py`.
- `@app.get("/health")`: Provides a simple health check endpoint to verify the API is running.

## Backend Concepts

- Application lifecycle management.
- Middleware configuration for cross-origin requests.
- Routing delegation.

## Data Flow

1. Server starts -> triggers `lifespan` startup.
2. Incoming requests hit `FastAPI` instance.
3. CORS middleware validates origin.
4. Request is routed to `api/routes.py` or handled by `/health`.
5. Server stops -> triggers `lifespan` shutdown -> shuts down `job_manager`.

## Engineering Decisions

- Using `lifespan` over deprecated `@app.on_event("startup")` for modern FastAPI lifecycle management.
- Abstracting routes into a separate module (`routes.py`) keeps the entry point clean.
- Including a `/health` endpoint is standard practice for container orchestration and uptime monitoring.

## Dependencies

- `fastapi`
- `logging`
- `contextlib`

## Interview Questions

- Easy: What does the CORS middleware do here?
- Medium: Why is it important to shut down the `job_manager` in the lifespan event?
- Deep: How does the `yield` statement work in an `asynccontextmanager`?

## Resume Points

- Built a modular FastAPI backend with proper lifespan management and CORS configuration.

## Improvements

- Add request rate limiting.
- Add centralized exception handling.
- Add structured JSON logging.

## Checklist

- Ensure CORS covers production domains.
- Know the purpose of the lifespan hook.
