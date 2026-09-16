from sqlalchemy import delete
from .database import Base, SessionLocal, engine
from .models import Job, JobSkill
from .demo_data import build_demo_jobs

def seed():
    Base.metadata.create_all(bind=engine)
    db=SessionLocal()
    try:
        db.execute(delete(JobSkill)); db.execute(delete(Job))
        rows=build_demo_jobs()
        for row in rows:
            skills=row.pop("skills")
            job=Job(**row)
            job.skills=[JobSkill(skill=s) for s in skills]
            db.add(job)
        db.commit()
        print(f"Seeded {len(rows)} deterministic demo jobs")
    finally:
        db.close()

if __name__=="__main__":
    seed()
