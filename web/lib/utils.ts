export function formatTimestamp(seconds: number): string {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);

  if (h > 0) {
    return `${h}:${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
  }
  return `${m}:${s.toString().padStart(2, "0")}`;
}

export function formatFileSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`; //Round off to 1 digit after decimal
  if (bytes < 1024 * 1024 * 1024) return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  return `${(bytes / (1024 * 1024 * 1024)).toFixed(2)} GB`;
}

export function categoryLabel(category: string): string {
  switch (category) {
    case "SINGLE_KILL":
      return "SINGLE KILL";
    case "MULTIPLE_KILLS":
      return "MULTI-KILL";
    default:
      return category.toUpperCase();
  }
}

export function categoryColor(category: string): string {
  switch (category) {
    case "MULTIPLE_KILLS":
      return "text-orange-500";
    case "SINGLE_KILL":
    default:
      return "text-zinc-400";
  }
}
