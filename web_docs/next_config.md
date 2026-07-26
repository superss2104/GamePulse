# `web/next.config.ts`

## File Overview

- Purpose: Next.js config entry point.
- Why it exists: It is where rewrites, headers, and image config would go.
- Architecture fit: Currently minimal and intentionally empty.

## Key Contents

- Exports an empty `nextConfig` object

## Interview Questions

- Easy: What is this file for?
- Ans - next.config.ts is the framework-level configuration file for Next.js. It allows us to customize how Next.js behaves, including routing, image optimization, redirects, rewrites, headers, environment settings, and experimental features.


- Medium: Why might it stay empty?
- Ans - Next.js provides sensible defaults for most applications, so many projects don't require any additional configuration. If the default behavior satisfies the application's requirements, the configuration object can remain empty. 


- Deep: When would you add rewrites or headers?
- Ans - I'd use rewrites when the frontend and backend are hosted on different servers. Rewrites allow the frontend to call endpoints like /api/upload while Next.js transparently forwards the request to the actual backend service. This avoids hardcoding backend URLs throughout the application.
- I'd configure headers to improve security and performance. For example, adding security headers like Content-Security-Policy or X-Frame-Options, enabling caching through Cache-Control, or configuring CORS headers when necessary.

