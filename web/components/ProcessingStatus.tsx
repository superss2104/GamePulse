"use client";

import type { JobStatusResponse } from "@/types";

interface ProcessingStatusProps {
  status: JobStatusResponse | null;
}

const STATUS_CONFIG = {
  queued: {
    label: "IN QUEUE",
    color: "text-zinc-500",
    border: "border-zinc-800",
  },
  processing: {
    label: "ANALYSIS IN PROGRESS",
    color: "text-orange-500",
    border: "border-orange-500",
  },
  completed: {
    label: "ANALYSIS COMPLETE",
    color: "text-emerald-500",
    border: "border-emerald-500",
  },
  failed: {
    label: "PIPELINE FAILURE",
    color: "text-red-500",
    border: "border-red-500",
  },
};

export default function ProcessingStatus({ status }: ProcessingStatusProps) { //{status} unpacks the status prop from the ProccessingStatusProps
  if (!status) return null;

  const config = STATUS_CONFIG[status.status];
  const isProcessing = status.status === "processing" || status.status === "queued";

  return (
    <div className="w-full max-w-6xl mx-auto mb-8">
      <div className={`relative overflow-hidden border bg-zinc-950 rounded-sm transition-colors duration-500 ${config.border}`}>
        <div className={`border-b p-4 flex items-center justify-between ${config.border}`}>
          <div className="flex items-center gap-3">
            {isProcessing && (
              <span className="relative flex h-3 w-3">
                <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 bg-orange-500`}></span>
                <span className={`relative inline-flex rounded-full h-3 w-3 bg-orange-500`}></span>
              </span>
            )}
            <h2 className={`text-sm font-bold uppercase tracking-widest ${config.color}`}>
              {config.label}
            </h2>
          </div>
          <div className="text-xs font-mono text-zinc-500">
            ID: {status.job_id}
          </div>
        </div>

        {/* Body */}
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">

            {/* Left: Terminal Log */}
            <div>
              <h3 className="text-xs font-bold uppercase tracking-widest text-zinc-400 mb-3">
                PIPELINE TELEMETRY
              </h3>
              <div className="bg-zinc-950 border border-zinc-800 rounded-sm p-4 font-mono text-xs h-32 overflow-y-auto relative">

                <div className="text-zinc-500 mb-1">{`> INITIALIZING PIPELINE... OK`}</div>
                <div className="text-zinc-500 mb-1">{`> MOUNTING VIDEO SOUCE... OK`}</div>
                <div className={`${isProcessing ? 'text-orange-500' : 'text-zinc-500'} mb-1`}>
                  {`> ${status.progress?.toUpperCase() || "AWAITING INSTRUCTIONS..."}`}
                  {isProcessing && <span className="animate-pulse">_</span>}
                </div>

                {status.status === 'completed' && (
                  <div className="text-emerald-500 mt-2">{`> PROCESS TERMINATED SUCCESSFULLY. [${status.result?.clip_count} CLIPS GENERATED]`}</div>
                )}
              </div>
            </div>

            {/* Right: Summary / Error */}
            <div className="flex flex-col justify-center">
              {status.error ? (
                <div className="border border-red-500/50 bg-red-500/10 p-4 text-xs font-mono text-red-400 uppercase rounded-sm">
                  <span className="font-bold block mb-1">CRITICAL ERROR:</span>
                  {status.error}
                </div>
              ) : status.status === "completed" ? (
                <div className="text-center">
                  <div className="text-4xl font-black text-zinc-100 mb-2">
                    {status.result?.clip_count}
                  </div>
                  <div className="text-xs font-bold uppercase tracking-widest text-orange-500">
                    HIGHLIGHTS EXTRACTED
                  </div>
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center h-full gap-4">
                  <div className="relative flex items-center justify-center w-12 h-12">
                    <div className="absolute inset-0 border-2 border-zinc-800 rounded-full"></div>
                    <div className="absolute inset-0 border-2 border-orange-500 rounded-full border-t-transparent animate-spin"></div>
                    <div className="w-1.5 h-1.5 bg-orange-500 rounded-full animate-ping"></div>
                  </div>
                  <div className="text-center">
                    <div className="text-xs font-bold text-orange-500 uppercase tracking-widest mb-1">
                      ANALYZING MATCH...
                    </div>
                    <div className="text-[10px] font-mono text-zinc-500 uppercase">
                      Please Wait...
                    </div>
                  </div>
                </div>
              )}
            </div>

          </div>
        </div>

        {/* Scanline effect spanning entire card */}
        {isProcessing && (
          <div className="animate-scanline" style={{
            position: 'absolute',
            inset: 0,
            pointerEvents: 'none',
            zIndex: 50,
            background: 'linear-gradient(to bottom, transparent 0%, rgba(249,115,22,0.3) 40%, rgba(249,115,22,0.3) 60%, transparent 100%)',
            backgroundSize: '100% 20px',
            backgroundRepeat: 'no-repeat',
          }} />
        )}

      </div>
    </div>
  );
}
