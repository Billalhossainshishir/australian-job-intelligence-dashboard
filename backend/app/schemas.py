from datetime import date
from pydantic import BaseModel, Field


class SkillCoverageRequest(BaseModel):
    cv_text: str = Field(min_length=1, max_length=20000)
    job_description: str = Field(min_length=1, max_length=20000)


class SkillCoverageResponse(BaseModel):
    cv_skills: list[str]
    job_skills: list[str]
    matched_skills: list[str]
    missing_skills: list[str]
    technical_skill_coverage: float


class JobOut(BaseModel):
    job_id: str
    title: str
    company: str
    city: str
    state: str
    description: str
    salary: str | None
    employment_type: str
    role_type: str
    experience_level: str
    date_posted: date
    source: str
    skills: list[str]
