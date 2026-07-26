# `web/app/globals.css`

## File Overview

- Purpose: Global CSS and theme layer.
- Why it exists: It defines the app-wide look and a few animation utilities.
- Architecture fit: It is the baseline styling for all pages and components.

## Detailed Walkthrough

- Imports Tailwind with `@import "tailwindcss";`.
- Defines the font theme token.
- Sets `color-scheme: dark` globally.
- Styles the body with a dark background and subtle dot-grid texture.
- Defines `data-flow` and `scanline` keyframes.
- Exposes utility classes `animate-data-flow` and `animate-scanline`.

## React / Frontend Concepts

- Global styling
- Theme tokens
- Custom animation utilities

## Engineering Decisions

- A custom dark tactical theme matches the CS2 subject matter.
- The custom animations support the status UI without extra JavaScript.

## Dependencies

- Tailwind CSS

## Interview Questions

- Easy: What does this file control?
- Medium: Why use keyframes instead of inline animation styles?
- Deep: How do these styles support the product identity?
- Design: How would you organize theme tokens as the app grows?
- Follow-up: Why might the font token need attention?

## Resume Points

- Created a global dark theme and motion system for the frontend UI.

## Improvements

- Fix the font token wiring.
- Move repeated theme values into CSS variables.

## Checklist

- Know the background and animation setup.
- Know why `color-scheme: dark` matters.

