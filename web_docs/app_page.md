# `web/app/page.tsx`

## File Overview

- Purpose: Main upload and configuration page.
- Why it exists: It is the start of the product workflow.
- Architecture fit: Orchestrates upload, processing, and route transition.

## Detailed Walkthrough

- `use client` is required because the page uses hooks and client-side navigation.
- `useRouter()` is used to push the user to the results page after processing starts.
- `settings` is local state initialized from `DEFAULT_SETTINGS`.
- `uploading`, `uploadProgress`, and `error` model the upload lifecycle.
- `handleFileSelected(file)` is the main workflow:
  - sets loading state
  - uploads the file through `uploadVideo()`
  - updates progress through the callback
  - starts backend processing through `startProcessing()`
  - navigates to `/results/${job_id}`
- The JSX composes `HeroSection`, `UploadZone`, `SettingsPanel`, and `HowItWorks`.

## React / Frontend Concepts

- Local state
- Controlled child props
- Client routing
- Async event handling

## Data Flow

1. User picks a file in `UploadZone`.
2. The file is passed to `handleFileSelected`.
3. The file is uploaded to the backend.
4. The backend returns `job_id`.
5. The page starts processing for that job.
6. The page navigates to the results route.

## Engineering Decisions

- Upload and processing are split into two backend calls so progress feedback can happen before the job starts.
- State lives in the page instead of a global store because this workflow is small and linear.

## Dependencies

- `useRouter`
- `uploadVideo`
- `startProcessing`
- `DEFAULT_SETTINGS`
- Child components

# app/page.tsx – Interview Questions

## 1. Why is this a Client Component?

### Answer

This page is marked with `"use client"` because it relies on browser-only features:

- `useState()` for managing UI state.
- `useRouter()` for client-side navigation.
- File upload through the browser.
- Event handlers (`onFileSelected`).

Server Components cannot handle user interactions or browser APIs, so this page must execute on the client.

---

## 2. Why is `settings` stored in the Home component instead of `SettingsPanel`?

### Answer

`settings` is required by multiple components.

```
Home
│
├── UploadZone
│
└── SettingsPanel
```

`SettingsPanel` modifies the settings, while `UploadZone` indirectly needs them when the upload starts.

If the state lived inside `SettingsPanel`, the Home component would not have access to the latest values when calling:

```ts
startProcessing(uploadRes.job_id, settings);
```

Therefore the state is lifted to the parent component.

---

## 3. Why use React state instead of normal variables?

### Answer

Variables do not trigger UI updates.

For example,

```ts
let uploading = false;
```

Changing it to

```ts
uploading = true;
```

would not update the page.

Using

```ts
const [uploading, setUploading] = useState(false);
```

causes React to automatically re-render whenever the upload state changes.

---

## 4. Why keep separate state variables instead of one big object?

### Answer

Each piece of state changes independently.

```ts
uploading
uploadProgress
error
settings
```

For example:

- upload progress changes many times per second.
- error changes only on failure.
- settings change only when the user edits them.

Keeping them separate makes updates simpler and avoids unnecessary object copying.

---

## 5. Why is `handleFileSelected` asynchronous?

### Answer

Uploading a video and starting backend processing are asynchronous operations.

```ts
const uploadRes = await uploadVideo(...);

await startProcessing(...);
```

Using `async/await` keeps the code readable while waiting for network requests to finish without freezing the browser.

---

## 6. Why split upload and processing into two API calls?

### Answer

Instead of

```
POST /process
```

the application performs

```
Upload Video
      ↓
Receive Job ID
      ↓
Start Processing
```

Advantages:

- upload completes immediately,
- processing can run in the background,
- failed processing does not require re-uploading the video,
- upload and processing services can scale independently.

---

## 7. Why is upload progress updated through a callback?

```ts
uploadVideo(file, (percent) => {
    setUploadProgress(percent);
});
```

### Answer

The upload library continuously reports progress.

Each progress update invokes the callback.

Example:

```
5%

↓

18%

↓

43%

↓

81%

↓

100%
```

Each callback updates React state, causing the progress bar to animate smoothly.

---

## 8. Why navigate only after `startProcessing()` succeeds?

```ts
await startProcessing(...);

router.push(...);
```

### Answer

The Results page immediately begins polling.

If navigation occurred before processing had successfully started, the Results page could begin polling for a job that doesn't exist yet.

Waiting ensures the backend has successfully created the processing job before redirecting.

---

## 9. Why use `router.push()` instead of `window.location`?

### Answer

`router.push()` performs client-side navigation.

Benefits:

- no full page refresh,
- faster navigation,
- preserves application state,
- Next.js prefetching support.

Using

```ts
window.location
```

would reload the entire application.

---

## 10. Why reset the error before every upload?

```ts
setError(null);
```

### Answer

Suppose a previous upload failed.

The error message should disappear when the user starts another upload.

Otherwise, the old error would remain visible during the next upload.

---

## 11. Why disable the SettingsPanel while uploading?

```tsx
disabled={uploading}
```

### Answer

Changing processing parameters while the upload is already in progress could create inconsistent behavior.

Disabling the controls ensures the uploaded job always uses the exact settings selected when the upload began.

---

## 12. Why store the upload progress in React state?

### Answer

The progress bar is part of the UI.

Each progress update:

```ts
setUploadProgress(percent);
```

causes React to re-render the progress bar.

Without React state, the progress indicator would never visually update.

---

## 13. What happens if upload succeeds but processing fails?

### Answer

The upload is already complete.

The `catch` block displays the error message:

```ts
setError(...)
```

and resets the upload state.

Since the video is already uploaded, the backend could later support retrying processing without requiring another upload.

---

## 14. Why split the page into components?

```
Home
│
├── HeroSection
├── UploadZone
├── SettingsPanel
└── HowItWorks
```

### Answer

Each component has a single responsibility.

- `HeroSection` displays the landing content.
- `UploadZone` handles uploads.
- `SettingsPanel` edits processing parameters.
- `HowItWorks` explains the pipeline.

This keeps the page small, reusable, and easier to maintain.

---

## 15. If you wanted to support multiple simultaneous uploads, what would you change?

### Answer

Instead of storing:

```ts
uploading
uploadProgress
error
```

store an array of upload jobs:

```ts
jobs = [
    {
        file,
        progress,
        status,
        error
    }
]
```

Each upload would manage its own state independently, allowing multiple videos to be uploaded and processed concurrently.

---

## 16. Why use TypeScript interfaces like `ProcessingSettings`?

### Answer

The interface guarantees that every processing request contains the expected fields.

It provides:

- compile-time type checking,
- editor autocompletion,
- easier maintenance,
- fewer runtime bugs.

---

## 17. Why keep the API logic (`uploadVideo`, `startProcessing`) outside the component?

### Answer

Separating API calls from UI logic follows separation of concerns.

The page only describes **what** should happen.

The API module handles **how** HTTP requests are made.

Benefits include:

- cleaner components,
- reusable API functions,
- easier testing,
- simpler maintenance.

## Resume Points

- Orchestrated the full upload-to-results workflow in a Next.js app.
- Added user-visible upload progress and route handoff to live job polling.

## Improvements

- Add pre-upload file validation.
- Add cancel support.
- Reset state after success or failure.

## Checklist

- Know the upload sequence end to end.
- Know why this page must be client-side.
- Know how child components communicate with it.

