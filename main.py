from fastapi import FastAPI
from auth import router as auth_router
from companies import router as company_router
from jobs import router as job_router
from candidates import router as candidate_router
from applications import router as application_router
from interview import router as interview_router

app = FastAPI(title="Recruitment Portal")

app.include_router(auth_router, prefix="/auth")
app.include_router(company_router, prefix="/companies")
app.include_router(job_router, prefix="/jobs")
app.include_router(candidate_router, prefix="/candidates")
app.include_router(application_router, prefix="/applications")
app.include_router(interview_router, prefix="/interviews")
