# CSpotlight Frontend

This is the Next.js frontend for the **CSpotlight** automated CS2 highlight detection pipeline. It provides a sleek, modern web interface for users to upload gameplay videos, tweak pipeline configuration weights, and view/download the generated highlight clips in real-time.

## 🛠️ Tech Stack

- **Framework:** Next.js (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Icons:** Lucide React
- **Data Fetching:** Standard `fetch` with polling

## 🚀 Getting Started Locally

1. Install dependencies:
```bash
npm install
# or
yarn install
```

2. Configure Environment Variables:
If you are running the FastAPI backend locally, the frontend will default to `http://localhost:8000`. 
If you are connecting to a remote deployed backend, create a `.env.local` file in this `web/` directory:
```env
NEXT_PUBLIC_API_URL=http://<YOUR_BACKEND_IP>:8000
```

3. Run the development server:
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the application.

## ☁️ Deployment on Vercel

The easiest way to deploy this frontend is via [Vercel](https://vercel.com).

1. Import your GitHub repository to Vercel.
2. **Critical Step:** In the Vercel project configuration, set the **Root Directory** to `web`.
3. Under Environment Variables, add `NEXT_PUBLIC_API_URL` pointing to your deployed FastAPI backend.
4. Click **Deploy**.

## 📁 Key Components

- `app/page.tsx`: The main landing page with the hero section, configuration panel, and drag-and-drop upload zone.
- `app/results/[jobId]/page.tsx`: The results dashboard that polls the backend for job status and displays the extracted video clips once processing is complete.
- `components/`: Reusable UI components including the `UploadZone`, `ConfigPanel`, `ProcessingStatus`, and `ClipViewer`.
- `lib/api.ts`: TypeScript API client that handles typed communication with the FastAPI backend, including `FormData` uploads and status polling.
