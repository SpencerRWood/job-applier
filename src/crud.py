import os
from sqlalchemy.orm import Session
from datetime import datetime
from src.data_models import JobDescription, JobApplication
from src.schemas import JobApplicationCreate
from fastapi import HTTPException

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def create_job_application(db: Session, application_data: JobApplicationCreate, resume: bytes, resume_filename: str):
    # Fetch the latest application_id if any exists
    # last_application = db.query(JobApplication).order_by(JobApplication.application_id.desc()).first()
    # new_application_id = (last_application.application_id + 1) if last_application else 1
    
    # Save job description
    job_description = JobDescription(job_posting_link=application_data.job_posting_link)
    db.add(job_description)
    db.commit()
    db.refresh(job_description)

    application_id = job_description.description_id
    
    # Save resume file
    resume_path = None
    if resume:
        resume_path = os.path.join(UPLOAD_FOLDER, resume_filename)
        with open(resume_path, "wb") as f:
            f.write(resume)
    
    # Parse application_date
    application_date_parsed = None
    if application_data.application_date:
        application_date_parsed = datetime.strptime(application_data.application_date, "%Y-%m-%d")

    # Save job application
    job_application = JobApplication(
        application_id=application_id,
        company=application_data.company,
        job_title=application_data.job_title,
        # applied=application_data.applied,
        application_date=application_date_parsed,
        resume_used=resume_path,
        referred=application_data.referred,
        status=application_data.status,
        notes=application_data.notes,
        created_at = datetime.now(),
        current_indicator=True
    )

    db.add(job_application)
    db.commit()
    db.refresh(job_application)
    return job_application

def update_job_application_status(db: Session, application_id: int, new_status: str):
    # Set current_indicator to False for the existing current status record
    current_status = db.query(JobApplication).filter(
        JobApplication.application_id == application_id,
        JobApplication.current_indicator == True
    ).first()

    if current_status is None:
        raise HTTPException(status_code=404, detail="Job application not found or no current status found")

    current_status.current_indicator = False
    current_status.updated_at = datetime.now()
    db.commit()

    new_application_status = JobApplication(
        application_id = application_id,
        company=current_status.company,
        job_title=current_status.job_title,
        applied=current_status.applied,
        application_date=current_status.application_date,
        resume_used=current_status.resume_used,
        referred=current_status.referred,
        status=new_status,
        notes=current_status.notes,
        created_at=current_status.created_at,  # Keep original creation date
        updated_at=datetime.now(),
        current_indicator=True
    )

    db.add(new_application_status)
    db.commit()
    db.refresh(new_application_status)
    return new_application_status