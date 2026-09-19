# Australian Job Intelligence Dashboard

[![Tests](https://github.com/Billalhossainshishir/australian-job-intelligence-dashboard/actions/workflows/tests.yml/badge.svg)](https://github.com/Billalhossainshishir/australian-job-intelligence-dashboard/actions/workflows/tests.yml)
[![GitHub Pages](https://github.com/Billalhossainshishir/australian-job-intelligence-dashboard/actions/workflows/pages.yml/badge.svg)](https://github.com/Billalhossainshishir/australian-job-intelligence-dashboard/actions/workflows/pages.yml)

A dashboard for exploring a generated sample of Australian technology roles and comparing the technical skills in a CV with a role description. The browser dashboard and Python API implement separate demonstrations using synthetic data, not current vacancies.

Read the [reviewer guide](docs/REVIEWER_GUIDE.md) for execution modes, reproducible setup, architecture, verification steps and known limitations.

## Quick recruiter view

| Explore | Link |
| --- | --- |
| **Live demo** | https://billalhossainshishir.github.io/australian-job-intelligence-dashboard/ |
| **Reviewer guide** | [docs/REVIEWER_GUIDE.md](docs/REVIEWER_GUIDE.md) |
| **Architecture** | [docs/architecture.md](docs/architecture.md) |
| **Case study** | [docs/case-study.md](docs/case-study.md) |
| **Data notes** | [docs/data-notes.md](docs/data-notes.md) |

**60-second demo:** Filter technology roles → inspect skill demand → select a role → load/paste a CV → review transparent technical-skill coverage.

> **Public-demo honesty:** the GitHub Pages site uses curated sample data and browser-side analytics because GitHub Pages cannot run FastAPI/PostgreSQL. The complete backend implementation is included in this repository. The sample records are not live vacancies.


## Project preview

![Australian Job Intelligence Dashboard live demo overview](screenshots/job-intelligence-overview.jpg)

## Live demo flow

**Open dashboard → filter jobs → explore skill demand → select a job → load/paste a CV → compare technical skills**

**Technical Skill Coverage** describes dictionary-based skill overlap, not a probability of getting hired.

## What it demonstrates

- Python + FastAPI API design
- SQLAlchemy + PostgreSQL data modelling
- Transparent NLP-style skill extraction and normalisation
- Job-market analytics and interactive Chart.js dashboards
- Explainable CV-to-role technical skill comparison
- Docker Compose
- Pytest + GitHub Actions CI
- GitHub Pages deployment with an honest static-demo architecture
- Responsive recruiter-facing frontend

## Project structure

```text
australian-job-intelligence-dashboard/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── seed.py
│   │   └── services/skill_extractor.py
│   └── Dockerfile
├── frontend/
│   ├── index.html
│   ├── css/styles.css
│   ├── js/app.js
│   └── data/
├── tests/
├── docs/
├── data/
├── .github/workflows/
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Service health |
| GET | `/jobs` | Filter jobs by city, state, role, level or skill |
| GET | `/skills` | Canonical tracked skills |
| GET | `/locations` | Normalised city/state values |
| GET | `/analytics/top-skills` | Most frequent tracked skills |
| GET | `/analytics/cities` | Jobs by city |
| GET | `/analytics/cloud` | AWS/Azure/GCP demand |
| GET | `/analytics/languages` | Programming/data language demand |
| POST | `/compare` | CV vs job technical skill coverage |

FastAPI also exposes interactive API documentation at `/docs` when the backend is running.

## Run the API database and static frontend with Docker

```bash
docker compose up --build
```

Then open:

- Frontend: `http://localhost:8080`
- API: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`

The API container seeds PostgreSQL automatically from generated demonstration records. The served frontend still uses its own JavaScript data; it is not connected to this API. Inspect the backend through `/docs`.

## Run without Docker

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m backend.app.seed
uvicorn backend.app.main:app --reload
```

Serve the static frontend separately:

```bash
python -m http.server 8080 --directory frontend
```

## Run tests

```bash
pytest -q
```

## GitHub Pages deployment

The included `pages.yml` publishes only the `frontend/` directory. After pushing to GitHub:

1. Open **Settings → Pages**.
2. Under **Build and deployment**, choose **GitHub Actions**.
3. Push to `main` or run the Pages workflow manually.
4. Your demo should become available at:
   `https://billalhossainshishir.github.io/australian-job-intelligence-dashboard/`

## Skill extraction

Version 1 uses a deterministic canonical dictionary. Examples:

- `python3` → **Python**
- `PowerBI` → **Power BI**
- `k8s` → **Kubernetes**
- `Amazon Web Services` → **AWS**
- `GitHub` → **Git**

This keeps the result auditable and easy to test. More advanced NLP/embeddings can be added later without changing the metric definition.

## Technical Skill Coverage

```text
coverage = matched tracked skills / tracked skills requested by selected role × 100
```

It deliberately does **not** estimate interview probability, employability or hiring likelihood.

## Dataset and collection policy

The repository ships with 240 curated demo records so the project is reproducible and safe to publish. They are not current job advertisements. Real-world ingestion should use only public APIs, open datasets, licensed feeds or manually prepared data that permits reuse. Avoid scraping websites that prohibit automated collection.

## Portfolio summary

> Built an Australian technology-job intelligence platform using Python, FastAPI, PostgreSQL and explainable NLP-style skill extraction, with interactive market analytics and transparent CV-to-role technical skill coverage. Published a GitHub Pages recruiter demo while keeping the complete backend, database model, Docker setup and automated tests in the repository.

## Author

**Billal Hossain Shishir**  
Portfolio: `https://billalhossain.com.au`

## Limitations and scope

- The repository ships with curated synthetic demonstration records, not current Australian vacancies.
- Technical Skill Coverage is deterministic dictionary-based overlap; it is not an employability score, interview probability or hiring prediction.
- The GitHub Pages dashboard uses browser-side sample data and is not connected to the FastAPI/PostgreSQL backend.
- The current skill extractor is intentionally transparent and dictionary-based; it does not attempt semantic equivalence beyond configured normalisation.
- Real-world ingestion should use public APIs, open datasets, licensed feeds or manually prepared data that permits reuse.