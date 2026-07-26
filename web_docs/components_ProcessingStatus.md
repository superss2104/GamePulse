# `web/components/ProcessingStatus.tsx`

## File Overview

- Purpose: Live status display for a job.
- Why it exists: It shows progress while the backend processes the match.
- Architecture fit: It is the main status surface on the results page.

## Detailed Walkthrough

- Returns `null` when `status` is missing.
- `STATUS_CONFIG` maps each job state to a label and styles.
- Shows a pulsing indicator when queued or processing.
- Displays a terminal-like telemetry block.
- Shows an error box, success summary, or waiting state depending on the job.

## React / Frontend Concepts

- Pure prop-driven rendering
- Conditional UI
- State-to-view mapping

## Engineering Decisions

- The telemetry styling makes waiting feel intentional and product-specific.

## Dependencies

- `JobStatusResponse`
- CSS animation classes from `globals.css`

## Interview Questions

- Easy: Why use a config object for statuses?
- Medium: Why return `null` when there is no status?
- Deep: How would you make this accessible?
- Design: How would you handle a new backend status?
- Follow-up: Should the telemetry log be more structured?

## Resume Points

- Built a live asynchronous status panel with success, failure, and in-progress states.

## Improvements

- Add ARIA live regions.
- Add more detailed progress stages.

## Checklist

- Know the status mapping.
- Know how the component changes by job state.

