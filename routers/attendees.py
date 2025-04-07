from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter(prefix="/attendees", tags=["attendees"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=schemas.AttendeeResponse)
def register_attendee(attendee: schemas.AttendeeCreate, db: Session = Depends(get_db)):
    return crud.register_attendee(db, attendee)