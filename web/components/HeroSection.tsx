export default function HeroSection() {
  return (
    <section className="relative flex flex-col items-center pt-24 pb-16 text-center border-b border-zinc-800 w-full max-w-7xl">
      {/* Decoration*/}
      <div className="absolute top-0 left-0 w-full h-120 px bg-gradient-to-r from-transparent via-orange-500/30 to-transparent opacity-50" />
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-px h-16 bg-gradient-to-b from-orange-500/50 to-transparent opacity-50" />

      {/* Badge */}
      <div className="relative mb-8 inline-flex items-center gap-3 border border-zinc-800 bg-zinc-900/50 px-4 py-1.5 rounded-sm">
        <span className="h-2 w-2 bg-orange-500 shadow-[0_0_8px_rgba(249,115,22,0.8)]" />
        <span className="text-xs font-mono font-semibold uppercase tracking-widest text-zinc-300">
          Powered by Computer Vision
        </span>
      </div>

      {/* Title */}
      <h1 className="relative text-4xl font-black uppercase tracking-tight text-zinc-100 sm:text-5xl lg:text-6xl">
        Automated CS2
        <br />
        <span className="text-orange-500">Match Highlights</span>
      </h1>

      {/* Subtitle */}
      <p className="relative mt-6 max-w-2xl text-sm font-mono text-zinc-400 leading-relaxed uppercase tracking-wide">
        Upload your CS2 gameplay recordings. Our algorithmic pipeline parses the killfeed, tracks motion, and isolates multi-kill events for immediate post-match analysis.
      </p>

      {/* Feature Data Points */}
      <div className="relative mt-12 grid grid-cols-2 sm:grid-cols-4 gap-px bg-zinc-800 border border-zinc-800 rounded-sm overflow-hidden shadow-2xl">
        {[
          { stat: "01", label: "Killfeed Parsing" },
          { stat: "02", label: "Multi-Kill Tracking" },
          { stat: "03", label: "Motion Telemetry" },
          { stat: "04", label: "Audio Scoring" },
        ].map((feature) => (
          <div
            key={feature.stat} //set the unique key for each feature 
            className="flex flex-col items-center justify-center bg-zinc-950 p-6 transition-colors hover:bg-zinc-900"
          >
            <span className="text-2xl font-black text-zinc-700">{feature.stat}</span>
            <span className="mt-2 text-xs font-bold uppercase tracking-wider text-orange-500 text-center">
              {feature.label}
            </span>
          </div>
        ))}
      </div>
    </section>
  );
}
