export default function HowItWorks() {
  const steps = [
    {
      number: "01",
      title: "Data Extraction",
      description: "Visual motion scores, audio intensity, and killfeed events are extracted from the raw match recording.",
    },
    {
      number: "02",
      title: "Signal Fusion",
      description: "Motion, audio, and killfeed signals are combined into a unified highlight score, using the killfeed as a hard gate to filter out non-combat action.",
    },
    {
      number: "03",
      title: "Windowing & Thresholding",
      description: "The pipeline applies a sliding window across the scores, keeping only the segments that breach the top percentile of match intensity.",
    },
    {
      number: "04",
      title: "Motion Expansion",
      description: "Because killfeeds are lagging indicators, windows are expanded backward into preceding motion activity to capture the full setup and aiming phase.",
    },
    {
      number: "05",
      title: "Categorization & Export",
      description: "Events are merged, categorized (e.g., Single Kill vs Multi-Kill), converted into precise timestamps, and exported via FFmpeg.",
    },
  ];

  return (
    <section className="w-full max-w-4xl py-16 border-t border-zinc-800 mt-16">
      <div className="mb-10 text-center">
        <h2 className="text-2xl font-black uppercase tracking-widest text-zinc-100">
          Pipeline Architecture
        </h2>
        <p className="mt-2 text-xs font-mono text-zinc-500 uppercase">
          How CSpotlight analyzes your match
        </p>
      </div>

      <div className="space-y-4">
        {steps.map((step, index) => (
          <div key={index} className="flex flex-col sm:flex-row items-start sm:items-center gap-4 bg-zinc-900/50 border border-zinc-800 p-6 rounded-sm hover:border-zinc-700 transition-colors">
            <div className="flex-shrink-0 flex items-center justify-center w-12 h-12 bg-zinc-950 border border-orange-500 text-orange-500 font-black text-xl rounded-sm">
              {step.number}
            </div>
            <div>
              <h3 className="text-sm font-bold uppercase tracking-wider text-zinc-200">
                {step.title}
              </h3>
              <p className="mt-1 text-xs font-mono text-zinc-400">
                {step.description}
              </p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
