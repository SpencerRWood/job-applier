from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.schemas import JobApplicationCreate, StatusOptions
from src.crud import create_job_application, update_job_application_status

from typing import Optional

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/applications/")
async def add_job_application(
    company: str = Form(...),
    job_title: str = Form(...),
    job_posting_link: str = Form(...),
    applied: bool = Form(False),
    application_date: Optional[str] = Form(None),
    referred: bool = Form(False),
    status: str = Form(""),
    notes: str = Form(""),
    resume: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    application_data = JobApplicationCreate(
        company=company,
        job_title=job_title,
        job_posting_link=job_posting_link,
        applied=applied,
        application_date=application_date,
        referred=referred,
        status=status,
        notes=notes
    )

    # Handle resume upload if present
    resume_data = await resume.read() if resume else None
    resume_filename = resume.filename if resume else ""

    # Create job application
    try:
        job_application = create_job_application(db, application_data, resume_data, resume_filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"message": "Job application created successfully", "application_id": job_application.application_id}

@router.post("/applications/update")
async def change_job_application_status(
    application_id: int = Form(...),
    new_status: StatusOptions = Form(...),
    db: Session = Depends(get_db)
):
    updated_application = update_job_application_status(db, application_id, new_status)
    if updated_application is None:
        raise HTTPException(status_code=404, detail="Job application not found")
    
    return {"message": "Job application status updated", "application_id": application_id, "new_status": new_status}