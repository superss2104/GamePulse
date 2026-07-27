"use client";

import Link from "next/link";
import Image from "next/image";

export default function Navbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 border-b border-zinc-800 bg-zinc-950/40 backdrop-blur-md">
      <div className="mx-auto flex h-14 max-w-7xl items-center justify-between px-1">
        <Link href="/" className="flex items-center gap-3 group">
          <Image
            src="/logo.png"
            alt="CSpotlight Logo"
            width={240}
            height={80}
            className="h-30 w-auto object-contain transition-transform group-hover:scale-110"
          />
        </Link>

        <div className="flex items-center gap-6">
          <a
            href="https://github.com/superss2104/CSpotlight"
            target="_blank"
            rel="noopener noreferrer"
            className="text-xs font-semibold uppercase tracking-wider text-zinc-500 transition-colors hover:text-zinc-300"
          >
            GitHub
          </a>
          <Link
            href="/"
            className="rounded-sm bg-orange-500 px-5 py-2 text-xs font-bold uppercase tracking-wider text-zinc-900 shadow-[0_0_15px_rgba(249,115,22,0.6)] transition-all hover:bg-orange-400 hover:shadow-[0_0_20px_rgba(249,115,22,0.6)] active:scale-95"
          >
            Upload Match
          </Link>
        </div>
      </div>
    </nav>
  );
}
