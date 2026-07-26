# `web/components/UploadZone.tsx`

## File Overview

- Purpose: Drag-and-drop and click-to-upload area.
- Why it exists: It is the entry point for the recording file.
- Architecture fit: It feeds the upload pipeline in the home page.

## Detailed Walkthrough

- `useState` tracks drag state and the selected file.
- `useCallback` stabilizes drag/drop and input handlers.
- The component validates file MIME types against an allowlist.
- On a valid file, it calls `onFileSelected(file)`.
- It shows filename, file size, and upload progress when relevant.
- It displays parent-supplied errors below the drop zone.

## React / Frontend Concepts

- Local UI state
- Callback props
- Drag-and-drop events
- Controlled disabling while uploading

## Engineering Decisions

- The file input is hidden so the whole card behaves like the target.
- Upload orchestration lives in the page, not inside the drop zone.

## Dependencies

- `formatFileSize`
- Browser drag-and-drop APIs

## Interview Questions

- Easy: How does this accept files?
- Medium: Why support both dropping and clicking?
- Deep: Why is the upload logic outside this component?
- Design: How would you improve accessibility?
- Follow-up: What edge cases exist with MIME validation?

## Resume Points

- Built a drag-and-drop upload surface with validation and progress feedback.

## Improvements

- Validate file size.
- Add keyboard accessibility.
- Handle empty MIME types more gracefully.

## Checklist

- Know the file selection flow.
- Know the upload-disabled state behavior.

