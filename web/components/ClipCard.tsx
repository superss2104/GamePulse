"use client";

import { useState } from "react";
import type { ClipResult } from "@/types";
import { categoryLabel, formatTimestamp } from "@/lib/utils";
import { getDownloadUrl } from "@/lib/api";

interface ClipCardProps {
  clip: ClipResult;
  jobId: string;
}

export default function ClipCard({ clip, jobId }: ClipCardProps) {
  const [previewOpen, setPreviewOpen] = useState(false);
  const isMultiKill = clip.category === "MULTIPLE_KILLS";
  const videoUrl = getDownloadUrl(jobId, clip.name);

  return (
    <div className="flex flex-col border border-zinc-800 bg-zinc-950 transition-colors hover:border-zinc-600 rounded-sm overflow-hidden mb-2 group">
      {/* Row content */}
      <div className="flex flex-col sm:flex-row items-stretch">
        {/* Left: Metadata / Rank */}
        <div className={`flex flex-col justify-center items-center p-4 sm:w-24 border-r border-zinc-800 ${isMultiKill ? 'bg-orange-500/10' : 'bg-zinc-900/50'}`}>
          <span className="text-xs font-mono text-zinc-500 mb-1">LEN</span>
          <span className={`text-lg font-black font-mono ${isMultiKill ? 'text-orange-500' : 'text-zinc-300'}`}>
            {formatTimestamp(clip.duration)}
          </span>
        </div>

        {/* Middle: Info */}
        <div className="flex-1 p-4 flex flex-col justify-center">
          <div className="flex items-center gap-3 mb-2">
            <span className={`text-[10px] font-bold uppercase tracking-widest px-2 py-0.5 rounded-sm border ${isMultiKill
                ? 'border-orange-500 text-orange-500 bg-orange-500/10'
                : 'border-zinc-600 text-zinc-400 bg-zinc-800/50'
              }`}>
              {categoryLabel(clip.category)}
            </span>
            <span className="text-xs font-mono text-zinc-500">
              {formatTimestamp(clip.start)} — {formatTimestamp(clip.end)}
            </span>
          </div>
          <h4 className="font-bold text-zinc-100 uppercase tracking-wide truncate">
            {clip.name.replace('.mp4', '')}
          </h4>
        </div>

        {/* Right: Actions */}
        <div className="flex items-center justify-center p-4 sm:border-l border-zinc-800 bg-zinc-900/30 gap-3">
          <button
            onClick={() => setPreviewOpen(!previewOpen)}
            className={`flex items-center justify-center h-10 px-4 font-bold uppercase tracking-widest text-xs transition-colors rounded-sm border ${previewOpen
                ? 'bg-orange-500 text-zinc-950 border-orange-500'
                : 'bg-zinc-950 text-orange-500 border-orange-500/50 hover:bg-orange-500 hover:text-zinc-950'
              }`}
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2.5} stroke="currentColor" className="h-4 w-4 sm:mr-0 md:mr-2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" d="M15.91 11.672a.375.375 0 010 .656l-5.603 3.113a.375.375 0 01-.557-.328V8.887c0-.286.307-.466.557-.327l5.603 3.112z" />
            </svg>
            <span className="hidden md:inline">PREVIEW</span>
          </button>

          <a
            href={videoUrl}
            download={clip.name}
            className="flex items-center justify-center h-10 px-4 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 font-bold uppercase tracking-widest text-xs transition-colors rounded-sm"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={2.5}
              stroke="currentColor"
              className="h-4 w-4 sm:mr-0 md:mr-2"
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
            </svg>
            <span className="hidden md:inline">DOWNLOAD</span>
          </a>
        </div>
      </div>

      {/* Expandable Preview Section */}
      {previewOpen && (
        <div className="w-full bg-zinc-950 border-t border-zinc-800 p-4 flex flex-col items-center">
          <div className="w-full max-w-3xl">
            <video
              controls
              autoPlay
              src={videoUrl}
              className="w-full h-auto border border-zinc-800 rounded-sm shadow-2xl"
            />
          </div>
        </div>
      )}
    </div>
  );
}
