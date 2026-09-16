from collections import Counter
from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import select

from .database import Base, engine, get_db
from .models import Job
from .schemas import JobOut, SkillCoverageRequest, SkillCoverageResponse
from .services.skill_extractor import SKILL_VARIANTS, compare_skills

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Australian Job Intelligence API",
    version="1.0.0",
    description="Portfolio API for technology job analytics and transparent technical-skill comparison.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def serialize_job(job: Job) -> JobOut:
    return JobOut(
        job_id=job.job_id,
        title=job.title,
        company=job.company,
        city=job.city,
        state=job.state,
        description=job.description,
        salary=job.salary,
        employment_type=job.employment_type,
        role_type=job.role_type,
        experience_level=job.experience_level,
        date_posted=job.date_posted,
        source=job.source,
        skills=sorted(js.skill for js in job.skills),
    )


@app.get("/health")
def health():
    return {"status": "ok", "service": "australian-job-intelligence-api"}


@app.get("/skills")
def skills():
    return {"skills": sorted(SKILL_VARIANTS.keys())}


@app.get("/locations")
def locations(db: Session = Depends(get_db)):
    rows = db.execute(select(Job.city, Job.state).distinct()).all()
    return {"locations": [{"city": city, "state": state} for city, state in sorted(rows)]}


@app.get("/jobs", response_model=list[JobOut])
def jobs(
    city: str | None = None,
    state: str | None = None,
    role_type: str | None = None,
    experience_level: str | None = None,
    skill: str | None = None,
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    query = select(Job)
    if city:
        query = query.where(Job.city == city)
    if state:
        query = query.where(Job.state == state)
    if role_type:
        query = query.where(Job.role_type == role_type)
    if experience_level:
        query = query.where(Job.experience_level == experience_level)
    results = db.scalars(query.order_by(Job.date_posted.desc()).limit(limit)).unique().all()
    if skill:
        results = [job for job in results if skill in {s.skill for s in job.skills}]
    return [serialize_job(job) for job in results]


@app.get("/analytics/top-skills")
def top_skills(limit: int = Query(10, ge=1, le=50), db: Session = Depends(get_db)):
    jobs = db.scalars(select(Job)).unique().all()
    counts = Counter(skill.skill for job in jobs for skill in job.skills)
    return {"items": [{"skill": k, "count": v} for k, v in counts.most_common(limit)]}


@app.get("/analytics/cities")
def cities(db: Session = Depends(get_db)):
    jobs = db.scalars(select(Job)).unique().all()
    counts = Counter(f"{job.city}, {job.state}" for job in jobs)
    return {"items": [{"location": k, "count": v} for k, v in counts.most_common()]}


@app.get("/analytics/cloud")
def cloud(db: Session = Depends(get_db)):
    jobs = db.scalars(select(Job)).unique().all()
    cloud_skills = {"AWS", "Azure", "GCP"}
    counts = Counter(s.skill for job in jobs for s in job.skills if s.skill in cloud_skills)
    return {"items": [{"skill": k, "count": counts.get(k, 0)} for k in ["AWS", "Azure", "GCP"]]}


@app.get("/analytics/languages")
def languages(db: Session = Depends(get_db)):
    jobs = db.scalars(select(Job)).unique().all()
    language_skills = {"Python", "Java", "JavaScript", "TypeScript", "C#", "C++", "SQL"}
    counts = Counter(s.skill for job in jobs for s in job.skills if s.skill in language_skills)
    return {"items": [{"skill": k, "count": v} for k, v in counts.most_common()]}


@app.post("/compare", response_model=SkillCoverageResponse)
def compare(payload: SkillCoverageRequest):
    return compare_skills(payload.cv_text, payload.job_description)
