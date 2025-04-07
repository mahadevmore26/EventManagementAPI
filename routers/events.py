from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import *
from schemas import *
from database import *
from auth import *

router = APIRouter(prefix="/events", tags=["events"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create_event", response_model=EventResponse)
def create_event_handler(
    event: EventCreate, 
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user)
):
    return create_event(db, event)

@router.get("/list_events", response_model=list[EventResponse])
def list_events(
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user)
):
    return get_events(db)



@router.put("/update_event", response_model=EventResponse)
def update_event_handler(
    event: EventUpdate,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user)
):
    updated_event = update_event(db, event.event_id, event)
    if not updated_event:
        raise HTTPException(status_code=404, detail="Event not found")
    return updated_event


