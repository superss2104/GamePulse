# `web/app/results/[jobId]/page.tsx`

## File Overview

- Purpose: Dynamic results page for one job.
- Why it exists: It shows live backend status and generated clips.
- Architecture fit: It is the second half of the workflow after upload.

## Detailed Walkthrough

- `use client` is required because the page uses `useEffect`, `useState`, and route params.
- `useParams()` reads `jobId` from the dynamic route.
- `status` stores the latest `JobStatusResponse`.
- `useEffect()` starts polling when the page mounts.
- `pollUntilDone()` repeatedly fetches job status until completion or failure.
- The cleanup flag prevents stale updates after unmount.
- On polling failure, the page sets a failed status with a clear error string.
- When complete, the page renders the clip list through `ClipCard`.

## React / Frontend Concepts

- Route params
- Effects
- Cleanup
- Conditional rendering
- Mapping arrays to components

## Data Flow

1. Route param `jobId` is read.
2. The page polls `/results/:jobId`.
3. Each poll updates local `status`.
4. UI changes when status becomes completed or failed.
5. Clips are rendered from `status.result.clips`.

## Engineering Decisions

- Polling is simpler than websockets and sufficient for a long-running background job.
- The page does not cache results because it wants the latest job state.

## Dependencies

- `useParams`
- `useEffect`
- `pollUntilDone`
- `ProcessingStatus`
- `ClipCard`

# app/results/[jobId]/page.tsx – Interview Questions

## 1. Why is this a Client Component?

### Answer

This page uses browser-only React hooks:

- `useState()` for storing the latest processing status.
- `useEffect()` for starting the polling process.
- `useParams()` for reading the dynamic `jobId` from the URL.

Since the page continuously updates while the backend processes the video, it must run in the browser and therefore requires `"use client"`.

---

## 2. What does `useParams()` do?

### Answer

The page is a dynamic route:

```
/results/[jobId]
```

For example:

```
/results/abc123
```

`useParams()` extracts the dynamic part of the URL:

```tsx
const params = useParams();
const jobId = params.jobId;
```

which returns:

```ts
{
    jobId: "abc123"
}
```

This `jobId` is then used to poll the backend for the correct processing job.

---

## 3. Why is polling started inside `useEffect`?

### Answer

`useEffect()` runs after the component is mounted.

Starting polling inside `useEffect` ensures that only one polling loop is created when the page loads.

If `pollUntilDone()` were called directly inside the component body, a new polling loop would be created every time React re-rendered the component.

---

## 4. Why is `jobId` included in the dependency array?

```tsx
useEffect(() => {
    ...
}, [jobId]);
```

### Answer

React reruns the effect whenever any dependency changes.

If the user navigates from

```
/results/job1
```

to

```
/results/job2
```

the page should stop polling the old job and begin polling the new one.

Using `[jobId]` ensures the polling always corresponds to the currently displayed job.

---

## 5. Why does `useEffect` return a cleanup function?

```tsx
return () => {
    isMounted = false;
};
```

### Answer

React automatically calls this function when:

- the component unmounts, or
- `jobId` changes.

This prevents the polling callback from attempting to update state after the page has already been removed, avoiding unnecessary updates and React warnings.

---

## 6. Why use polling instead of WebSockets?

### Answer

Video processing is a relatively slow background task.

Polling every 1–2 seconds provides responsive updates while keeping the implementation simple.

WebSockets are more appropriate for applications requiring real-time updates, such as chat systems or multiplayer games.

---

## 7. Why is `status` stored in React state?

```tsx
const [status, setStatus] = useState(...);
```

### Answer

Every polling response updates the current processing status.

Updating the React state automatically causes the component to re-render, allowing the UI to reflect:

- processing progress,
- completion,
- failures,
- generated highlight clips.

Without React state, the page would never update when new data arrived.

---

## 8. Why use optional chaining?

```tsx
status?.status
```

### Answer

Initially, `status` is `null` because no polling response has been received.

Without optional chaining:

```tsx
status.status
```

would throw:

```
Cannot read properties of null
```

Optional chaining safely returns `undefined` until `status` exists.

---

## 9. Explain this conditional rendering.

```tsx
{status?.status === "completed" && (
    ...
)}
```

### Answer

React renders the JSX only if the condition is true.

If:

```ts
status.status === "completed"
```

the highlight list is displayed.

Otherwise, React renders nothing.

This prevents incomplete results from appearing while processing is still ongoing.

---

## 10. Why use a ternary operator here?

```tsx
status.result.clip_count === 0 ? (...) : (...)
```

### Answer

The UI has two possible states after processing completes:

- No highlights were found.
- Highlights were found.

The ternary operator cleanly renders one of these two interfaces based on the backend response.

---

## 11. Why use `map()` to render clips?

```tsx
status.result.clips.map((clip) => (
    <ClipCard ... />
))
```

### Answer

The backend returns an array of clips.

`map()` transforms each clip object into a `ClipCard` component.

Conceptually:

```
clip1
    ↓
ClipCard

clip2
    ↓
ClipCard

clip3
    ↓
ClipCard
```

React then renders the resulting list of components.

---

## 12. Why is the `key` prop required?

```tsx
<ClipCard
    key={clip.name}
    ...
/>
```

### Answer

React uses the `key` to uniquely identify each list item.

This allows React to efficiently determine which clips were added, removed, or updated without rebuilding the entire list.

---

## 13. Why use Next.js `<Link>` instead of `<a>`?

### Answer

`<Link>` enables client-side navigation.

Benefits include:

- prefetching pages,
- faster navigation,
- preserving application state,
- avoiding full page reloads.

This results in a smoother user experience.

---

## 14. Why split the UI into components like `ProcessingStatus` and `ClipCard`?

### Answer

Breaking the page into reusable components improves:

- readability,
- maintainability,
- reusability,
- separation of concerns.

`ResultsPage` manages the page logic, while each child component is responsible for rendering a specific part of the UI.

---

## 15. What happens if the backend connection fails while polling?

### Answer

The Promise returned by `pollUntilDone()` is rejected.

The `.catch()` block updates the page state to:

```ts
status: "failed"
```

allowing the UI to display an error message instead of leaving the user waiting indefinitely.t if the backend returns an unknown status?

## Resume Points

- Built a live polling results page for asynchronous job processing.
- Rendered downloadable and previewable highlight clips from backend metadata.

## Improvements

- Add retry and timeout handling.
- Add a cancel/stop polling action.
- Make the empty state more explicit.

## Checklist

- Know the polling loop.
- Know how the page reacts to success and failure.
- Know how clip data becomes UI.

