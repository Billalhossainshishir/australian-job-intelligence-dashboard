from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    job_id = Column(String(40), unique=True, nullable=False, index=True)
    title = Column(String(180), nullable=False, index=True)
    company = Column(String(180), nullable=False)
    city = Column(String(80), nullable=False, index=True)
    state = Column(String(10), nullable=False, index=True)
    description = Column(Text, nullable=False)
    salary = Column(String(100), nullable=True)
    employment_type = Column(String(60), nullable=False)
    role_type = Column(String(80), nullable=False, index=True)
    experience_level = Column(String(30), nullable=False, index=True)
    date_posted = Column(Date, nullable=False, index=True)
    source = Column(String(120), nullable=False)

    skills = relationship("JobSkill", back_populates="job", cascade="all, delete-orphan")


class JobSkill(Base):
    __tablename__ = "job_skills"
    __table_args__ = (UniqueConstraint("job_id", "skill", name="uq_job_skill"),)

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True)
    skill = Column(String(80), nullable=False, index=True)

    job = relationship("Job", back_populates="skills")
