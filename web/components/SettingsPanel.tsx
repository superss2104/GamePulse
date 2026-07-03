"use client";

import type { ProcessingSettings } from "@/types";
import { DEFAULT_SETTINGS } from "@/types";

interface SettingsPanelProps {
  settings: ProcessingSettings;
  onSettingsChange: (settings: ProcessingSettings) => void;
  disabled?: boolean;
}

export default function SettingsPanel({
  settings,
  onSettingsChange,
  disabled = false,
}: SettingsPanelProps) {
  const toggle = (key: keyof ProcessingSettings) => {
    onSettingsChange({
      ...settings, //create a new copy of previous object using ... (spread operator), this is just for immutable updates, So that react knows that the state has changed. 
      [key]: !settings[key], //Instead of directly modifying the variable of the exisitng object, we create a new object and pass that to the onSettingsChange callback, because of this react will know that the state has changed and will re-render the component. and it will update the UI.
    }); //We use key so that we can dynamically update the value of the key that is passed to the function.
  };

  return (
    <div className="w-full max-w-4xl mt-8">
      <div className="border border-zinc-800 bg-zinc-950 p-6 rounded-sm">
        <div className="mb-4 pb-2 border-b border-zinc-800">
          <h3 className="text-sm font-bold uppercase tracking-widest text-zinc-300">
            Analysis Parameters
          </h3>
          <p className="mt-1 text-xs font-mono text-zinc-500 uppercase">
            Configure highlight detection filters
          </p>
        </div>

        <div className="flex flex-col gap-3 sm:flex-row sm:gap-4">
          {/* Single Kills Toggle */}
          <button
            onClick={() => toggle("disable_single_kills")}
            disabled={disabled}
            className={`
              relative flex flex-1 items-center gap-4 border px-5 py-4 text-left transition-all rounded-sm
              ${!settings.disable_single_kills
                ? "border-orange-500 bg-orange-500/5 text-zinc-100"
                : "border-zinc-800 bg-zinc-900/50 text-zinc-500"
              }
              ${disabled ? "cursor-not-allowed opacity-50" : "cursor-pointer hover:bg-zinc-800"}
            `}
          >
            {/* Active accent bar */}
            {!settings.disable_single_kills && (
              <div className="absolute left-0 top-0 bottom-0 w-1 bg-orange-500" />
            )}

            <div
              className={`flex h-4 w-4 items-center justify-center border transition-colors rounded-sm ${!settings.disable_single_kills
                  ? "border-orange-500 bg-orange-500"
                  : "border-zinc-700 bg-zinc-950"
                }`}
            >
              {!settings.disable_single_kills && (
                <svg className="h-3 w-3 text-zinc-950" fill="none" viewBox="0 0 24 24" strokeWidth={4} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                </svg>
              )}
            </div>
            <div>
              <span className="block text-sm font-bold uppercase tracking-wider">Single Kills</span>
              <span className="block text-xs font-mono text-zinc-500 mt-0.5">Detect individual eliminations</span>
            </div>
          </button>

          {/* Multi Kills Toggle */}
          <button
            onClick={() => toggle("disable_multi_kills")}
            disabled={disabled}
            className={`
              relative flex flex-1 items-center gap-4 border px-5 py-4 text-left transition-all rounded-sm
              ${!settings.disable_multi_kills
                ? "border-orange-500 bg-orange-500/5 text-zinc-100"
                : "border-zinc-800 bg-zinc-900/50 text-zinc-500"
              }
              ${disabled ? "cursor-not-allowed opacity-50" : "cursor-pointer hover:bg-zinc-800"}
            `}
          >
            {/* Active accent bar */}
            {!settings.disable_multi_kills && (
              <div className="absolute left-0 top-0 bottom-0 w-1 bg-orange-500" />
            )}

            <div
              className={`flex h-4 w-4 items-center justify-center border transition-colors rounded-sm ${!settings.disable_multi_kills
                  ? "border-orange-500 bg-orange-500"
                  : "border-zinc-700 bg-zinc-950"
                }`}
            >
              {!settings.disable_multi_kills && (
                <svg className="h-3 w-3 text-zinc-950" fill="none" viewBox="0 0 24 24" strokeWidth={4} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                </svg>
              )}
            </div>
            <div>
              <span className="block text-sm font-bold uppercase tracking-wider">Multi Kills</span>
              <span className="block text-xs font-mono text-zinc-500 mt-0.5">Detect rapid succession eliminations</span>
            </div>
          </button>
        </div>
      </div>
    </div>
  );
}
