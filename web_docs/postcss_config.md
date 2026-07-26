# `web/postcss.config.mjs`

## File Overview

- Purpose: PostCSS setup for Tailwind.
- Why it exists: It wires the CSS pipeline.
- Architecture fit: It enables the styling system.

## Key Contents

- Registers `@tailwindcss/postcss`

## Interview Questions

- Easy: What is PostCSS? 
- Ans - PostCSS is a CSS processing tool that transforms CSS during the build process using plugins. It allows tools like Tailwind CSS and Autoprefixer to generate and modify CSS before it's served to the browser.. It's like a compiler but for CSS


- Medium: Why is Tailwind configured here? Because Tailwind itself is a PostCSS plugin
- Ans - Tailwind is implemented as a PostCSS plugin. During the build process, PostCSS invokes the Tailwind plugin, which scans the project's source files for utility classes and generates only the CSS that's actually used. This keeps the final CSS bundle much smaller.


- Deep: What breaks if this plugin is removed? 
- Ans - Tailwind is implemented as a PostCSS plugin. During the build process, PostCSS invokes the Tailwind plugin to scan the project's source files for utility classes, generate only the required CSS, and transform Tailwind-specific directives like @apply into standard CSS. Without this plugin, Tailwind utility classes would not be generated, so the application would render without its intended styling