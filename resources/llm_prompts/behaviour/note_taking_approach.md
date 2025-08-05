## Three Note-Taking Approaches

### 1. AI Work-Along Notes (*_(ai_workalong).md)
- Verbose AI explanations are FORBIDDEN in all files except those with `_(ai_workalong)` suffix
- Examples: `brainstorm_features_(ai_workalong).md`, `analysis_auth_system_(ai_workalong).md`,
  `debugging_cronicle_(ai_workalong).md`
- Use for detailed reasoning, context, technical deep-dives, lengthy explanations
- Throwaway documentation for AI processing only
- **This is the ONLY location where verbose AI explanations are permitted**

### 2. Literal Capture Mode (Default)
- When user says "write something down" - use their exact words
- Structure better with subpoints and lists
- Keep original phrasing for features, ideas, descriptions
- Break single lines into structured, shorter sentences
- **NO verbose explanations or long-form text allowed**

### 3. Content Generation Mode
- Maximum simplicity and conciseness
- Small sentences, short and to-the-point
- Format: "Feature A: point 1, point 2, point 3"
- Use established names, precise language
- **STRICTLY no lengthy explanations or verbose content**

## Formatting Rules

**Default Structure:**
```
Group name (no heading)
- item 1
- item 2
  - subitem A
  - subitem B
- item 3
```

**Depth Limits:**
- Maximum 3-5 points per level
- Maximum 2 levels of nesting
- For deeper structure: create new group with name (no heading)

**Examples:**

*Literal Capture:*
```
Authentication system
- user login via email/password
- session management with JWT tokens
  - 24-hour expiration
  - refresh token support
- password reset flow
```

*Content Generation:*
```
Core Features
- Auth: JWT sessions, email login, password reset
- API: REST endpoints, rate limiting, error handling  
- Storage: PostgreSQL, Redis cache, S3 assets
```