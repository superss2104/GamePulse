# `web/components/HowItWorks.tsx`

## File Overview

- Purpose: Static explanation of the pipeline.
- Why it exists: It helps the user understand how the app analyzes a match.
- Architecture fit: It mirrors the backend workflow in a readable format.

## Detailed Walkthrough

- Defines a static five-step array.
- Renders each step with `map()`.
- Each step describes a stage of the analysis pipeline.

## React / Frontend Concepts

- Static data rendering
- List rendering

## Engineering Decisions

- The section is descriptive rather than interactive because its job is to explain the product.

## Dependencies

- React
- Tailwind

## Interview Questions

- Easy: What does this section explain?
- Medium: Why is the content in an array?
- Deep: How does this match the backend design?
- Design: How would you make it live and status-driven?
- Follow-up: Should user-facing architecture docs be static?

## Resume Points

- Documented the detection pipeline directly in the frontend UI.

## Improvements

- Make it interactive as the backend progresses.

## Checklist

- Know the five stages.
- Know why this component exists at all.

