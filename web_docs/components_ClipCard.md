# `web/components/ClipCard.tsx`

## File Overview

- Purpose: One generated clip row.
- Why it exists: It gives the user preview and download actions for each highlight.
- Architecture fit: It is the final consumer-facing output of the pipeline.

## Detailed Walkthrough

- Accepts `clip` and `jobId`.
- Computes `isMultiKill` from the category.
- Builds a download URL with `getDownloadUrl()`.
- Uses local `previewOpen` state to show or hide the inline video.
- Renders duration, category, timestamps, and a cleaned clip title.
- Preview toggles an inline `<video>` element.
- Download points directly to the backend endpoint.

## React / Frontend Concepts

- Local state
- Conditional rendering
- List-item composition

## Engineering Decisions

- The preview is loaded only when requested so the page does not fetch every video immediately.

## Dependencies

- `ClipResult`
- `useState`
- `categoryLabel`
- `formatTimestamp`
- `getDownloadUrl`

## Interview Questions

- Easy: What can the user do here?
- Medium: Why build the URL in the client?
- Deep: What cross-origin issues could happen here?
- Design: How would you handle a long list of clips?
- Follow-up: What if clip names are not unique?

## Resume Points

- Rendered clip metadata into previewable and downloadable highlight cards.

## Improvements

- Use safer filename handling.
- Handle duplicate keys more defensively.

## Checklist

- Know preview state behavior.
- Know how the download URL is formed.

