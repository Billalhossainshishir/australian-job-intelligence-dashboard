# Architecture

```mermaid
flowchart LR
  A[Deterministic lawful demo-data generator] --> B[Normalisation + skill extraction]
  B --> C[(PostgreSQL)]
  C --> D[FastAPI]
  D --> E[Jobs API]
  D --> F[Analytics API]
  D --> G[CV technical skill comparison]
  H[GitHub Pages demo] --> I[Browser-side 240-record demo market]
  I --> J[Filters + Chart.js]
  I --> K[Technical Skill Coverage]
```

## Full-stack path

The repository contains FastAPI, SQLAlchemy and PostgreSQL. `docker compose up --build` starts PostgreSQL, seeds 240 deterministic demo records, starts the API and serves the frontend locally.

## GitHub Pages path

GitHub Pages is static hosting, so the public recruiter demo generates the same reproducible sample market in browser JavaScript. The page clearly labels the records as portfolio demo data and does not claim the Python backend is running on GitHub Pages.



## Current execution boundary

The current frontend does not call the API, including when served by Docker. Browser-generated data and comparison remain separate from Python/database results. The two paths in the diagram are independent, not an integrated full-stack user journey. See [the reviewer guide](REVIEWER_GUIDE.md).
