from fastapi import FastAPI
from app.routers import events, attendees
# from .routers import events, attendees
# from routers import events, attendees

app = FastAPI()

app.include_router(events.router)
app.include_router(attendees.router)

@app.get("/")
def root():
    return {"message": "Welcome to Event Management API"}