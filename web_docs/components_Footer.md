# `web/components/Footer.tsx`

## File Overview

- Purpose: Global footer.
- Why it exists: It closes the shell and reinforces branding.
- Architecture fit: It is the counterpart to the navbar.

## Detailed Walkthrough

- Displays the logo and product name.
- Shows a short product description.
- Includes a GitHub link.
- Shows the stack/version label.

## React / Frontend Concepts

- Presentational shell component

## Engineering Decisions

- The footer is informational and lightweight.

## Dependencies

- Static image asset

## Interview Questions

- Easy: Why have a footer?
- Medium: Why show version information?
- Deep: Why is this likely a server component candidate?
- Design: What would you put here in production?
- Follow-up: Should footer content be interactive?

## Resume Points

- Added consistent branding and product metadata to the app shell.

## Improvements

- Use `next/image`.
- Keep the repository link current.

## Checklist

- Know what shell content belongs here.

