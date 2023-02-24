from db.models.jobs import Job
from fastapi import HTTPException
from fastapi import status
from schemas.jobs import JobCreate
from sqlalchemy.orm import Session


def create_new_job(job: JobCreate, db: Session, owner_id: int):
    job_object = Job(**job.dict(), owner_id=owner_id)
    db.add(job_object)
    db.commit()
    db.refresh(job_object)
    return job_object


def retreive_job(id: int, db: Session):
    return db.query(Job).filter(Job.id == id).first()


def list_jobs(db: Session):
    return db.query(Job).filter(Job.is_active == True).all()


def update_job_by_id(id: int, job: JobCreate, db: Session, owner_id):
    existing_job = db.query(Job).filter(Job.id == id)
    if not existing_job.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found"
        )
    job.__dict__.update(owner_id=owner_id)
    existing_job.update(job.__dict__)
    db.commit()
    return 1


def delete_job_by_id(id: int, db: Session, owner_id):
    existing_job = db.query(Job).filter(Job.id == id)
    if not existing_job.first():
        return 0
    existing_job.delete(synchronize_session=False)
    db.commit()
    return 1
