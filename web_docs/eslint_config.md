# `web/eslint.config.mjs`

## File Overview

- Purpose: ESLint configuration.
- Why it exists: It enforces React and Next.js best practices.
- Architecture fit: It keeps the frontend maintainable.

## Key Contents

- Uses `eslint-config-next/core-web-vitals`
- Uses `eslint-config-next/typescript`
- Ignores generated output

## Interview Questions

- Easy: What does ESLint catch?
- Ans - ESLint is a static code analysis tool for JavaScript and TypeScript. It analyzes the source code without executing it and reports potential bugs, code smells, and violations of coding standards, helping maintain consistent code quality.
- Medium: Why ignore `.next`?
- Ans - These directories contain generated build artifacts rather than source code. Linting them would produce unnecessary warnings, slow down the linting process, and analyze files that developers don't manually edit. We only lint the actual source code.
- Deep: Why use Next's config instead of custom rules first?\
- Ans - Next.js provides an officially maintained ESLint configuration that includes recommended rules for React, Next.js, and performance best practices such as Core Web Vitals. Starting with these defaults saves development time, reduces maintenance, and ensures the project follows framework-recommended practices. We can still override or extend the rules if the project requires additional coding standards.

