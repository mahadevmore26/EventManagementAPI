from fastapi import FastAPI
from routers import events, attendees, auth
from database import create_tables, engine
from models import Base

app = FastAPI()

# Create database tables
create_tables()

app.include_router(events.router)
app.include_router(attendees.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Welcome to Event Management API"}