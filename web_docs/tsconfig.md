# `web/tsconfig.json`

## File Overview

- Purpose: TypeScript compiler configuration.
- Why it exists: It provides strict typing and import aliases.
- Architecture fit: It supports the typed frontend architecture.

## Key Contents

- `strict: true`
- `moduleResolution: "bundler"`
- `isolatedModules: true`
- `paths["@/*"] = ["./*"]`

## Interview Questions

- Easy: What does `paths` do?
- Medium: Why use strict mode?
- Deep: Why is `isolatedModules` useful in Next.js?

