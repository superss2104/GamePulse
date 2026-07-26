    # `server/services/pipeline.py`

## File Overview

- Purpose: Bridge between the API backend and the core ML/video pipeline.
- Why it exists: Wraps the core detection logic (`src/`) as a black box and formats its output for the API.
- Architecture fit: The integration layer separating the web server from the data science code.

## Detailed Walkthrough

- Modifies `sys.path` dynamically to import the `src/` modules natively.
- `process_video()`: The main entry point.
- Maps `ProcessingSettings` to the pipeline's expected parameters.
- Invokes `detect_highlights()` to get raw clip segments.
- Calls `cut_clips()` to generate physical MP4 files via FFmpeg.
- Maps the pipeline output into structured `ClipResult` and `ProcessingResult` schemas.

## Backend Concepts

- Adapter pattern (adapting internal representations to API representations).
- Dynamic module loading (`sys.path.insert`).
- Defensive programming (gracefully handling missing dependencies if run in a minimal environment).

## Data Flow

1. Receives video path + settings.
2. Runs OpenCV highlight detection -> Returns timestamps.
3. Passes timestamps to FFmpeg wrapper -> Writes MP4s to disk.
4. Packages metadata and download URLs -> Returns to worker.

## Engineering Decisions

- Imports from `src/` are placed *inside* the function. This ensures the server can start up and register routes even if heavy dependencies (OpenCV) fail to load immediately, failing only when a job runs.
- Strict isolation: The API knows nothing about how detection works, and the pipeline knows nothing about HTTP or JSON.

## Dependencies

- `src.highlight.pipeline`
- `src.video.clips`
- `models.schemas`
- `services.storage`

## Interview Questions

### Easy: Why does this file map the internal clip category to a new Enum for the result?

The pipeline's internal `ClipCategory` (in `src/highlight/categories.py`) uses `auto()` for its values — meaning the values are arbitrary integers assigned by Python, not stable or human-readable. The API's `ClipCategoryEnum` (in `server/models/schemas.py`) is a `str, Enum` with explicit string values like `"SINGLE_KILL"`. The mapping on line 67 (`ClipCategoryEnum(clip.category.name)`) converts from one to the other.

This matters for two reasons:
1. **Serialization** — The API returns JSON. Pydantic serializes `ClipCategoryEnum` to clean strings (`"SINGLE_KILL"`), whereas the internal enum would serialize to meaningless integers.
2. **Decoupling** — The `src/` pipeline is treated as a black box. If someone renames or refactors the internal enum, the API contract doesn't break — only this one mapping line needs to change.

### Medium: Why are the `src/` imports nested inside the `process_video` function?

The imports on lines 31-33 (`detect_highlights`, `cut_clips`, `ClipCategory`) are placed inside the function body instead of at the top of the file. This is a **lazy-loading** strategy:

- The `src/` modules pull in heavy dependencies like OpenCV and NumPy. If these imports were at the top level, importing `pipeline.py` would immediately try to load all of them.
- This means the FastAPI server **could not even start** if those dependencies were missing or broken — every route would fail, not just the processing route.
- By nesting them inside `process_video()`, the server boots up fine and serves routes like `/upload` and `/results` even if OpenCV isn't installed. The import failure only happens when a job actually tries to run, which is a much more graceful failure mode.
- This is especially useful during frontend-only development, where you want the API skeleton running without needing the entire ML stack.

### Deep: How does modifying `sys.path` work, and what are its dangers in a larger application?

**How it works** (lines 16-18): `sys.path` is a list of directory paths that Python's import system searches through, left to right, when resolving an `import` statement. `sys.path.insert(0, _src_path)` puts the `src/` directory at the **front** of this list, so `import highlight.pipeline` resolves to `src/highlight/pipeline.py` before Python looks anywhere else.

**Dangers in a larger application:**
1. **Name collisions** — If `src/` contains a module with the same name as a standard library or third-party package (e.g., `logging`, `json`, `video`), the `src/` version silently wins because it's searched first. This can cause extremely confusing bugs.
2. **Global mutation** — `sys.path` is process-wide. Modifying it in one module affects every subsequent import in the entire application, including unrelated code. There's no scoping or isolation.
3. **Non-determinism** — If multiple modules insert different paths at position 0, the final import resolution depends on the order those modules happen to load, which can change between runs.
4. **Testing difficulty** — Tests may behave differently depending on whether `sys.path` was modified before or after test setup, making failures hard to reproduce.
5. **Alternatives** — In production, a cleaner approach would be to make `src/` a proper installable package (with a `pyproject.toml`/`setup.py`) and `pip install -e .` it, so it's on the path naturally without runtime hacks.

## Resume Points

- Architected a clean integration layer connecting an asynchronous web backend with a synchronous computer vision pipeline.

## Improvements

- Stream progress updates (e.g., % complete) from the pipeline back to the worker.

## Checklist

- Understand the Adapter pattern role this file plays.
