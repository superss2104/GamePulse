# `web/lib/utils.ts`

## File Overview

- Purpose: Formatting and label helpers.
- Why it exists: It keeps display logic out of components.
- Architecture fit: It supports clean rendering for timestamps, file sizes, and categories.

## Detailed Walkthrough

- `formatTimestamp(seconds)` returns `mm:ss` or `hh:mm:ss`.
- `formatFileSize(bytes)` converts file sizes into human-readable units.
- `categoryLabel(category)` maps backend enum values to user-facing labels.
- `categoryColor(category)` maps categories to Tailwind text classes.

## React / Frontend Concepts

- Pure utility functions.
- No state.
- No effects.

## Engineering Decisions

- Shared helpers reduce duplication and keep presentational components focused on JSX.

## Dependencies

- TypeScript

## Interview Questions

- Easy: What does `formatTimestamp()` do?
- Medium: Why centralize these helpers?
- Deep: Why might `categoryColor()` be unused?
- Design: How would you support localization here?
- Follow-up: What edge cases should you test?

## Resume Points

- Built reusable formatting helpers for the frontend display layer.

## Improvements

- Add tests.
- Remove unused helpers if they stay dead.

## Checklist

- Know the output format of each helper.
- Know why these helpers exist at all.

