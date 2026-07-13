---
name: website_review
description: Review a website for issues, tech stack, AI-generated content, security, and SEO. Outputs a structured analysis.
---
# Website Review Skill

Perform a comprehensive review of a website. Outputs a structured analysis covering tech stack, content quality, security, and SEO.

## Usage
Provide a URL to review:
```
Review https://example.com for issues and AI-generated content
```

## Review Checklist

### 1. Tech Stack Detection
- Check HTTP headers (Server, X-Powered-By, framework signatures)
- Inspect HTML source for framework markers (React `div#root`, Vue `div#app`, Next.js `__next`)
- Check CSS framework (Tailwind, Bootstrap, custom)
- Identify build tool (Vite, Webpack, Parcel)
- Check deployment platform (Cloudflare, Vercel, Netlify, AWS)

### 2. Content Quality
- **Placeholder detection**: Look for `#` links, Lorem ipsum, "Coming soon", mockup data (₫0, $0)
- **AI-generated indicators**: 
  - Perfect SaaS template structure
  - Polished marketing copy with specific unverifiable metrics
  - Uniform FAQ format
  - Generic testimonial names (John, Sarah, etc.)
  - Stock photo usage patterns
- **Real content verification**: Check if testimonials, case studies, pricing are verifiable

### 3. Security Audit
- **HTTP headers**: Check for security headers (X-Frame-Options, CSP, HSTS, X-Content-Type-Options)
- **CORS config**: Look for overly permissive origins (especially local IPs in production)
- **Cookie flags**: HttpOnly, Secure, SameSite
- **TLS/SSL**: Certificate validity, protocol version
- **Input handling**: Forms, search fields, URL parameters
- **API exposure**: Check for unprotected endpoints, data leakage

### 4. SEO Analysis
- **Meta tags**: title, description, og:*, twitter:*
- **Sitemap**: Check /sitemap.xml
- **Robots.txt**: Check /robots.txt
- **SSR/SSG**: Is content rendered server-side or client-only?
- **Structured data**: JSON-LD, schema.org
- **Performance**: JS bundle size, number of chunks loaded

### 5. Functionality Check
- **Navigation**: Do all links work? Any broken routes?
- **Forms**: Do they submit? Any validation?
- **Dashboard/App**: Is it real data or mockup?
- **Mobile responsiveness**: Check viewport meta, responsive classes

## Output Format

```
## Website Review: [URL]

### Tech Stack
- Framework: [detected]
- CSS: [detected]
- Deployment: [detected]

### Issues Found
1. [issue] — [severity: high/medium/low]
2. [issue] — [severity]

### AI-Generated Content Assessment
- Confidence: [X%]
- Indicators: [list]

### Security Concerns
1. [concern] — [severity]
2. [concern] — [severity]

### SEO Limitations
1. [limitation]
2. [limitation]

### Recommendations
1. [recommendation]
2. [recommendation]
```

## Notes
- This skill is for analysis only — do not modify the target website
- Use webfetch for initial content, then analyze HTML/headers
- For security testing, only perform passive analysis (no active attacks)
