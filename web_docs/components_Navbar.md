# `web/components/Navbar.tsx`

## File Overview

- Purpose: Fixed top navigation bar.
- Why it exists: It provides branding, navigation, and a CTA.
- Architecture fit: It is part of the global shell.

## Detailed Walkthrough

- Renders a fixed dark nav at the top of the page.
- The logo links back to `/`.
- The GitHub link opens externally in a new tab.
- The `Upload Match` CTA routes to the home page.

## React / Frontend Concepts

- Presentational component
- Internal navigation via `Link`
- External navigation via `<a>`

## Engineering Decisions

- The nav stays visible across pages so the CTA is always accessible.

## Dependencies

- `next/link`
- Static image asset

## Interview Questions

- Easy: What is the navbar for?
- Medium: Why use `Link` for internal navigation?
- Deep: Why might this not need `use client`?
- Design: How would you adapt it for logged-in users?
- Follow-up: Why is the CTA so prominent?

## Resume Points

- Built a persistent navigation shell with a branded CTA.

## Improvements

- Remove `use client` if it remains static.
- Use `next/image`.

## Checklist

- Know the difference between internal and external links.
- Know what belongs in shell navigation.

