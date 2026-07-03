export default function Footer() {
  return (
    <footer className="border-t border-zinc-800 bg-zinc-950">
      <div className="mx-auto flex max-w-7xl flex-col items-center gap-4 px-6 py-8 sm:flex-row sm:justify-between"> 
        {/*If screen width is at least 640px, then apply justify-between and flex-row*/}
        <div className="flex items-center gap-3">
          <span className="text-xs font-bold uppercase tracking-widest text-zinc-300">
            CSpotlight
          </span>
          <span className="text-xs text-zinc-600 inline-block">|</span>
          <span className="text-xs uppercase tracking-wider text-zinc-600">
            Automated CS2 Highlight Extraction
          </span>
        </div>

        <div className="flex items-center gap-6">
          <a
            href="https://github.com/superss2104/CSpotlight"
            target="_blank"
            rel="noopener noreferrer"
            className="text-xs font-semibold uppercase tracking-wider text-zinc-500 transition-colors hover:text-zinc-300"
          > 
            GitHub
          </a>
          <span className="text-xs font-mono text-zinc-700">
            v1.0.0 // NEXT.JS + FASTAPI
          </span>
        </div>
      </div>
    </footer>
  );
}
