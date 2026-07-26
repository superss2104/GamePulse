# `server/models/schemas.py`

## File Overview

- Purpose: Defines Pydantic data validation schemas and Enums.
- Why it exists: Guarantees strict type safety for API requests and responses.
- Architecture fit: Acts as the contract between the frontend and the backend.

## Detailed Walkthrough

- `JobStatus`: Enum defining lifecycle states (`queued`, `processing`, `completed`, `failed`).
- `ProcessingSettings`: Optional user parameters like weights and category toggles.
- `ProcessRequest/Response`: Schemas for the `/process` endpoint.
- `ClipResult`: Metadata for a single highlight clip (start, end, category, URL).
- `ProcessingResult`: Full summary of a completed job containing an array of `ClipResult`s.
- `JobStatusResponse`: Schema returned by the polling endpoint.

## Backend Concepts

- Data validation and parsing using Pydantic.
- Strong typing with Enums.
- OpenAPI schema generation (FastAPI auto-generates Swagger docs from these).

## Data Flow

1. Request hits FastAPI -> Body is parsed and validated against schema.
2. If invalid -> 422 Unprocessable Entity is automatically returned.
3. If valid -> Route handler receives a typed Pydantic object.
4. Route returns Pydantic object -> FastAPI serializes it to JSON.

## Engineering Decisions

- Centralizing schemas ensures the API contract is explicit and consistent.
- `ClipCategoryEnum` mirrors the internal pipeline enum to decouple the API layer from internal data science code.

## Dependencies

- `pydantic`
- `enum`
- `datetime`

## Interview Questions

- Easy: What happens if the frontend sends a `ProcessRequest` missing a required field?
- Medium: Why mirror the `ClipCategoryEnum` instead of importing it directly from the pipeline?
- Deep: How does Pydantic optimize validation performance in version 2?

## Resume Points

- Enforced strict API contracts and type safety using Pydantic, enabling auto-generated OpenAPI documentation.

## Improvements

- Add `Field(..., description="...")` for richer Swagger documentation.
- Add custom validators for settings bounds (e.g., ensuring weights are between 0 and 1).

## Checklist

- Ensure fields match the frontend TypeScript interfaces in `types/index.ts`.
