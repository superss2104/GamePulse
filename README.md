# CSpotlight

CSpotlight is an automated highlight-detection pipeline and web application for Counter-Strike 2 (CS2) gameplay footage. It fuses motion, audio, and killfeed signals to automatically identify and cut the most exciting moments from a recording, with zero manual intervention.

## 🚀 Features

- **Full-Stack Web Interface** — Drag-and-drop video upload, real-time job polling, and in-browser clip preview/download.
- **Multi-signal Scoring** — Combines motion (OpenCV optical flow), audio energy, and CS2 killfeed detection into a single fused score stream.
- **Killfeed Detection** — Locates red-outlined kill entries in the HUD using contour analysis, rejecting false positives via inner-fill heuristics.
- **Multikill Tracking** — Groups kill events within a sliding 5-second time window (with 1-second debounce) to accurately categorize single, double, triple, and quad kills.
- **Configurable Weights** — Fine-tune the pipeline (e.g., 0.25 motion / 0.25 audio / 0.50 killfeed) via the web UI settings panel.
- **Automatic Cleanup** — An `asyncio` background task automatically sweeps expired job data to prevent unbounded disk growth in production.

## 🛠️ Tech Stack

- **Frontend:** Next.js, React, TypeScript, TailwindCSS
- **Backend:** FastAPI, Python, Pydantic
- **Computer Vision:** OpenCV, NumPy
- **Media Processing:** FFmpeg
- **Infrastructure:** Docker, Oracle Cloud (ARM), Vercel

## 📦 Project Structure

```text
CSpotlight/
├── web/                   # Next.js Frontend
├── server/                # FastAPI Backend Server
├── src/                   # Core Python Computer Vision Pipeline
│   ├── audio/             # Audio energy extraction
│   ├── cs2/               # Killfeed and multikill detection
│   ├── highlight/         # Score fusion, windowing, and categorization
│   └── video/             # Optical-flow motion analysis
├── tests/                 # 62 unit tests across 7 modules
├── Dockerfile             # Backend containerization
└── launch.bat             # Windows local development launcher
```

## 🚀 Quick Start (Local Development)

### Prerequisites
- Node.js 18+
- Python 3.10+
- FFmpeg installed and available on PATH

### 1. Start the FastAPI Backend
```powershell
# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r server/requirements.txt

# Start the backend server
python -m uvicorn server.app:app --port 8000 --reload
```

### 2. Start the Next.js Frontend
In a new terminal window:
```powershell
cd web
npm install
npm run dev
```

Open `http://localhost:3000` in your browser.

*(Note for Windows users: You can just double-click `launch.bat` in the root directory to start both servers simultaneously!)*

## ☁️ Deployment

### Backend (Docker / Oracle Cloud)
The backend is fully containerized and optimized for deployment on cloud instances (e.g., Oracle Cloud ARM).
```bash
docker build -t cspotlight-backend .
docker run -d --name cspotlight-backend --restart always -p 8000:8000 cspotlight-backend
```

### Frontend (Vercel)
Deploy the `web/` directory to Vercel and set the following environment variable:
`NEXT_PUBLIC_API_URL=http://<YOUR_BACKEND_IP>:8000`

## 💻 CLI Usage (Headless Mode)

You can still run the core pipeline directly from the command line without the web server.

```powershell
python src/main.py --input "data/videos/match.mp4" --output "clips/match"
```

**CLI Options:**
- `--input PATH` : Path to input video file
- `--output PATH` : Directory for output clips
- `--motion-weight FLOAT` : Weight for motion signal
- `--audio-weight FLOAT` : Weight for audio signal
- `--killfeed-weight FLOAT` : Weight for killfeed signal
- `--disable-single-kills` : Exclude single-kill clips
- `--disable-multi-kills` : Exclude multi-kill clips

## 🧪 Testing

The pipeline is validated by 62 unit tests covering all core detection and scoring stages using synthetic frame data and edge-case fixtures.

```powershell
python -m pytest tests/
```

## 📄 License
MIT License.
