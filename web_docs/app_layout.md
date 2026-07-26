# `web/app/layout.tsx`

## File Overview

- Purpose: Root layout for the frontend shell.
- Why it exists: It defines shared structure, metadata, and persistent chrome.
- Architecture fit: Every route is rendered inside this layout.

## Detailed Walkthrough

- Imports `Metadata`, `Inter`, `Navbar`, `Footer`, and global CSS.
- Exports app-wide metadata: title, description, and manifest.
- Wraps the app in `<html lang="en" className="dark scroll-smooth">`.
- Applies the Inter font class to the body.
- Adds a fixed background image layer behind the content.
- Renders `Navbar`, `main`, and `Footer` around `children`.

## React / Frontend Concepts

- App Router layout
- Server component by default
- Shared shell composition
- Metadata
- Font optimization

## Data Flow

1. Route content arrives as `children`.
2. Layout wraps it with the shared shell.
3. Navbar and footer remain visible across routes.

## Engineering Decisions

- Centralizing shell content avoids repetition.
- The background image and dark theme establish the brand identity.

## Dependencies

- `next/font/google`
- `next/metadata`
- `Navbar`
- `Footer`
- `globals.css`

## Interview Questions

- Easy: What is a root layout?
- Medium: Why put the background here instead of in a page?
- Deep: Why is this a good place for metadata?
- Design: How would you add theme variants here?
- Follow-up: What is wrong with the current public asset path?

## Resume Points

- Built a shared Next.js app shell with metadata and optimized font loading.

## Improvements

- Fix the wallpaper URL path.
- Consider making the shell components server components if they stay static.

## Checklist

- Know how App Router layouts work.
- Know why this file affects every route.

