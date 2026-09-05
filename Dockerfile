FROM python:3.12-slim

# Install system dependencies
# ffmpeg is needed for audio extraction and video clipping
# libgl1 and libglib2.0-0 are required by OpenCV
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install backend requirements
COPY server/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend and pipeline source code
COPY server/ ./server/
COPY src/ ./src/

# Copy demo video assets for the showcase section
COPY server/demo_videos/ ./server/demo_videos/

# Expose backend API port
EXPOSE 8000

# Run the FastAPI server using the PORT environment variable provided by Render
CMD python -m uvicorn server.app:app --host 0.0.0.0 --port ${PORT:-8000}
