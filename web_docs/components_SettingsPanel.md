# `web/components/SettingsPanel.tsx`

## File Overview

- Purpose: Toggle panel for highlight filters.
- Why it exists: It gives the user basic control over what gets detected.
- Architecture fit: It is the only user-facing config surface before processing starts.

## Detailed Walkthrough

- Receives `settings`, `onSettingsChange`, and `disabled`.
- `toggle(key)` flips a boolean setting and emits a new object.
- One button controls `disable_single_kills`.
- One button controls `disable_multi_kills`.
- Visual state changes based on whether each category is enabled.

## React / Frontend Concepts

- Controlled component
- Prop drilling
- Derived visual state

## Engineering Decisions

- The UI is intentionally simple because the backend only exposes a small set of toggles right now.

## Dependencies

- `ProcessingSettings`
- `DEFAULT_SETTINGS` is imported but currently unused

## Interview Questions

- Easy: What does this panel do?
- Medium: Why is it controlled by the parent?
- Deep: What is risky about a generic toggle helper?
- Design: How would you expose the weight fields in the UI?
- Follow-up: Why is the UI limited to booleans today?

## Resume Points

- Built a controlled settings panel for pre-processing highlight filters.

## Improvements

- Remove the unused import.
- Narrow the helper to boolean keys only.

## Checklist

- Know how settings propagate upward.
- Know what each toggle means.

