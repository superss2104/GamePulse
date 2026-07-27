"use client";

import { useState } from "react";
import { formatFileSize } from "@/lib/utils";

interface UploadZoneProps {
  onFileSelected: (file: File) => void;
  uploading: boolean;
  uploadProgress: number;
  error: string | null;
}

const ACCEPTED_TYPES = [
  "video/mp4",
  "video/x-msvideo",
  "video/x-matroska",
  "video/quicktime",
  "video/webm",
];

export default function UploadZone({
  onFileSelected,
  uploading,
  uploadProgress,
  error,
}: UploadZoneProps) {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault(); //Prevent the video from opening in the browser
    e.stopPropagation(); //Prevents the event from bubbling up to parent components
    setDragActive(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const file = e.dataTransfer.files?.[0]; //If file exists in dropzone, get the first file
    if (file && ACCEPTED_TYPES.includes(file.type)) {
      setSelectedFile(file);
      onFileSelected(file);
    }
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => { //e is the event object containing the files selected for the input
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      onFileSelected(file);
    }
  };

  return (
    <div className="w-full max-w-4xl pt-8">
      <div className="flex items-center justify-between border-b border-zinc-800 pb-2 mb-4">
        <span className="text-xs font-mono text-orange-500">
          STATUS: {uploading ? "UPLOADING" : "AWAITING FILE"}
        </span>
      </div>
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`
          relative flex flex-col items-center justify-center border border-dashed
          p-12 transition-all duration-200 cursor-pointer rounded-sm
          ${
            dragActive
              ? "border-orange-500 bg-orange-500/5"
              : "border-zinc-700 bg-zinc-900 hover:border-zinc-500"
          }
          ${uploading ? "pointer-events-none opacity-70" : ""}
        `}
      >
        <input
          id="file-upload"
          type="file"
          accept=".mp4,.avi,.mkv,.mov,.webm"
          onChange={handleFileInput}
          className="absolute inset-0 cursor-pointer opacity-0" //covering the whole dropzone area
          disabled={uploading}
        />
        <div
          className={`mb-6 flex h-16 w-16 items-center justify-center border transition-colors rounded-sm ${
            dragActive ? "border-orange-500 text-orange-500 bg-orange-500/10" : "border-zinc-800 text-zinc-600 bg-zinc-950"
          }`}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
            className="h-8 w-8"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5"
            />
          </svg>
        </div>

        {selectedFile && !uploading ? (
          <div className="text-center font-mono">
            <p className="text-lg font-bold text-zinc-100">
              {selectedFile.name}
            </p>
            <p className="mt-1 text-xs text-orange-500">
              SIZE: {formatFileSize(selectedFile.size)}
            </p>
          </div>
        ) : (
          <div className="text-center font-mono">
            <p className="text-base font-bold text-zinc-100 uppercase">
              {dragActive ? "INITIATE TRANSFER" : "SELECT OR DROP MATCH RECORDING"}
            </p>
            <p className="mt-2 text-xs text-zinc-500 uppercase tracking-widest">
              SUPPORTED: MP4, AVI, MKV, MOV, WEBM
            </p>
            <p className="mt-1 text-xs text-zinc-600">
              MAX SIZE: 2000 MB
            </p>
          </div>
        )}

        {uploading && (
          <div className="mt-8 w-full max-w-md font-mono">
            <div className="flex items-center justify-between text-xs mb-2">
              <span className="text-zinc-400">TRANSFERRING...</span>
              <span className="text-orange-500 font-bold">[{uploadProgress}%]</span>
            </div>
            <div className="h-2 w-full bg-zinc-950 border border-zinc-800 rounded-sm overflow-hidden">
              <div
                className="h-full bg-orange-500 transition-all duration-300"
                style={{ width: `${uploadProgress}%` }}
              />
            </div>
          </div>
        )}
      </div>

      {error && (
        <div className="mt-4 border border-red-500/50 bg-red-500/10 p-4 text-xs font-mono text-red-400 uppercase rounded-sm">
          [ERROR] {error}
        </div>
      )}
    </div>
  );
}
