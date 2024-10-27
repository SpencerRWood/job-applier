from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from src.database import Base, engine
from src.routers import applications

# Initialize FastAPI app
app = FastAPI()

templates = Jinja2Templates(directory="src/templates")

# Create tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(applications.router)

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("root.html", {"request": request})

@app.get("/form")
async def display_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.get("/update-form")
async def display_update_form(request: Request):
    return templates.TemplateResponse("update_form.html", {"request": request})
