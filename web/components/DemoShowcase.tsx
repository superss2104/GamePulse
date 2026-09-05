"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { processDemoClip } from "@/lib/api";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface DemoClip {
  id: string;
  title: string;
  description: string;
  filename: string; // filename served from /demo-videos/ for preview
}

const DEMO_CLIPS: DemoClip[] = [
  {
    id: "test13",
    title: "AWP Gameplay Highlights",
    description:
      "A collection of AWP kills in a regular DM game. See how the pipline isolates the most impressive kills and the moments just before the kill.",
    filename: "test13.mp4",
  },
  {
    id: "test6",
    title: "3 Kills Highlight",
    description:
      "A longer match recording with 3 kills. Process this clip to see how the pipeline isolates decisive round moments from raw gameplay.",
    filename: "test6.mp4",
  },
];

function ProcessIcon({ className }: { className?: string }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={2}
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
    >
      <polygon points="5 3 19 12 5 21 5 3" />
    </svg>
  );
}

function SpinnerIcon({ className }: { className?: string }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={2}
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
    >
      <path d="M21 12a9 9 0 1 1-6.219-8.56" />
    </svg>
  );
}

function DemoCard({ clip }: { clip: DemoClip }) {
  const router = useRouter();
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [previewOpen, setPreviewOpen] = useState(false);
  const videoUrl = `${API_BASE}/demo-videos/${clip.filename}`;

  const handleProcess = async () => {
    try {
      setProcessing(true);
      setError(null);
      const res = await processDemoClip(clip.id);
      router.push(`/results/${res.job_id}`);
    } catch (err) {
      console.error(err);
      setError(
        err instanceof Error ? err.message : "Failed to start demo processing."
      );
      setProcessing(false);
    }
  };

  return (
    <div className="group relative flex flex-col overflow-hidden rounded-sm border border-zinc-800 bg-zinc-950 transition-all duration-300 hover:border-zinc-600 hover:shadow-[0_0_30px_rgba(249,115,22,0.08)]">
      {/* Video Preview Area */}
      <div className="relative aspect-video w-full overflow-hidden bg-zinc-900">
        {/* Gradient overlay */}
        {!previewOpen && (
          <div className="absolute inset-0 z-10 bg-gradient-to-b from-zinc-950/60 via-transparent to-zinc-950/80 pointer-events-none" />
        )}

        {previewOpen ? (
          <video
            src={videoUrl}
            controls
            autoPlay
            className="h-full w-full object-cover"
          />
        ) : (
          <button
            onClick={() => setPreviewOpen(true)}
            className="group/play relative flex h-full w-full cursor-pointer items-center justify-center bg-zinc-900 transition-colors hover:bg-zinc-800/80"
            aria-label={`Preview ${clip.title}`}
          >
            {/* Grid pattern background */}
            <div
              className="absolute inset-0 opacity-20"
              style={{
                backgroundImage:
                  "linear-gradient(rgba(249,115,22,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(249,115,22,0.1) 1px, transparent 1px)",
                backgroundSize: "20px 20px",
              }}
            />

            {/* Center play button */}
            <div className="relative z-20 flex h-16 w-16 items-center justify-center rounded-sm border-2 border-zinc-600 bg-zinc-950/80 shadow-lg transition-all duration-300 group-hover/play:scale-110 group-hover/play:border-zinc-400 group-hover/play:shadow-xl">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="currentColor"
                className="ml-1 h-7 w-7 text-zinc-400"
              >
                <path
                  fillRule="evenodd"
                  d="M4.5 5.653c0-1.427 1.529-2.33 2.779-1.643l11.54 6.347c1.295.712 1.295 2.573 0 3.286L7.28 19.99c-1.25.687-2.779-.217-2.779-1.643V5.653Z"
                  clipRule="evenodd"
                />
              </svg>
            </div>

            {/* Corner labels */}
            <span className="absolute left-3 top-3 z-20 text-[10px] font-mono font-bold uppercase tracking-widest text-zinc-500">
              ▶ Preview Original
            </span>
            <span className="absolute bottom-3 right-3 z-20 text-[10px] font-mono text-zinc-600">
              Click to preview
            </span>
          </button>
        )}
      </div>

      {/* Info + Action Bar */}
      <div className="flex flex-col gap-3 border-t border-zinc-800 p-5">
        <div className="flex items-center gap-3">
          <span className="flex h-6 w-6 shrink-0 items-center justify-center border border-orange-500 bg-zinc-950 text-[10px] font-black text-orange-500">
            {clip.id === "test3" ? "01" : "02"}
          </span>
          <h3 className="text-sm font-bold uppercase tracking-wider text-zinc-200">
            {clip.title}
          </h3>
        </div>
        <p className="text-xs font-mono leading-relaxed text-zinc-500">
          {clip.description}
        </p>

        {/* Error display */}
        {error && (
          <p className="text-xs font-mono text-red-400 bg-red-500/10 border border-red-500/20 px-3 py-2 rounded-sm">
            {error}
          </p>
        )}

        {/* Process button */}
        <button
          onClick={handleProcess}
          disabled={processing}
          className={`mt-1 flex items-center justify-center gap-2 w-full py-3 rounded-sm text-xs font-bold uppercase tracking-widest transition-all duration-200 ${
            processing
              ? "bg-zinc-800 text-zinc-500 cursor-not-allowed border border-zinc-700"
              : "bg-orange-500 text-zinc-950 shadow-[0_0_15px_rgba(249,115,22,0.4)] hover:bg-orange-400 hover:shadow-[0_0_25px_rgba(249,115,22,0.6)] active:scale-[0.98] border border-orange-500"
          }`}
        >
          {processing ? (
            <>
              <SpinnerIcon className="h-4 w-4 animate-spin" />
              Processing...
            </>
          ) : (
            <>
              <ProcessIcon className="h-4 w-4" />
              Process with Pipeline
            </>
          )}
        </button>
      </div>
    </div>
  );
}

export default function DemoShowcase() {
  return (
    <section
      id="demo-showcase"
      className="w-full max-w-4xl py-16 border-t border-zinc-800 mt-8"
    >
      {/* Section Header */}
      <div className="mb-10 text-center">
        <div className="mb-4 inline-flex items-center gap-3 border border-zinc-800 bg-zinc-900/50 px-4 py-1.5 rounded-sm">
          <span className="h-2 w-2 bg-orange-500 shadow-[0_0_8px_rgba(249,115,22,0.8)] animate-pulse" />
          <span className="text-xs font-mono font-semibold uppercase tracking-widest text-zinc-300">
            Try It Out
          </span>
        </div>
        <h2 className="text-2xl font-black uppercase tracking-widest text-zinc-100">
          Sample Clips
        </h2>
        <p className="mt-2 text-xs font-mono text-zinc-500 uppercase">
          Select a clip to run the full CSpotlight pipeline and see the results
        </p>
      </div>

      {/* Demo Cards Grid */}
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        {DEMO_CLIPS.map((clip) => (
          <DemoCard key={clip.id} clip={clip} />
        ))}
      </div>

      {/* Bottom accent */}
      <div className="mt-10 flex items-center justify-center gap-4">
        <div className="h-px flex-1 bg-gradient-to-r from-transparent to-zinc-800" />
        <span className="text-[10px] font-mono uppercase tracking-widest text-zinc-700">
          No upload required · Process instantly
        </span>
        <div className="h-px flex-1 bg-gradient-to-l from-transparent to-zinc-800" />
      </div>
    </section>
  );
}
