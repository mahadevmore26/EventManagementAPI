from fastapi import APIRouter, Depends, HTTPException, Body, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from crud import *
from schemas import *
from database import *
from fastapi import File, UploadFile
import csv
from io import StringIO

router = APIRouter(prefix="/attendees", tags=["attendees"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=AttendeeResponse)
def create_new_attendee(attendee: AttendeeCreate, db: Session = Depends(get_db)):
    try:
        # Check if event has reached max attendees
        event = get_events(db, attendee.event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
            
        current_attendees = len(get_event_attendees(db, attendee.event_id))
        if event.max_attendees and current_attendees >= event.max_attendees:
            raise HTTPException(
                status_code=400,
                detail="Event has reached maximum number of attendees"
            )
            
        return register_attendee(db, attendee)
    except IntegrityError as e:
        if "Duplicate entry" in str(e) and "email" in str(e):
            raise HTTPException(
                status_code=400,
                detail="An attendee with this email address is already registered"
            )
        raise HTTPException(status_code=400, detail="Database integrity error")

@router.put("/check-in", response_model=AttendeeResponse)
def check_in_attendee_endpoint(data: dict = Body(...), db: Session = Depends(get_db)):
    attendee = check_in_attendee(db, data["attendee_id"])
    if not attendee:
        raise HTTPException(
            status_code=404,
            detail="Attendee not found"
        )
    if attendee:
        raise HTTPException(
            status_code=400,
            detail="Attendee is already checked in"
        )
    return attendee

@router.post("/bulk-check-in")
def bulk_check_in(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    content = file.file.read()
    csv_string = content.decode()
    csv_reader = csv.DictReader(StringIO(csv_string))
    
    results = {
        "success": [],
        "errors": []
    }
    
    for row in csv_reader:
        try:
            attendee_id = int(row.get('attendee_id'))
            attendee = check_in_attendee(db, attendee_id)
            if attendee:
                results["success"].append(attendee_id)
        except Exception as e:
            results["errors"].append({
                "attendee_id": row.get('attendee_id'),
                "error": str(e)
            })
    
    return results

@router.post("/list", response_model=List[AttendeeResponse])
def list_event_attendees(
    data: dict = Body(...),
    checked_in: Optional[bool] = Query(None, description="Filter by check-in status"),
    search: Optional[str] = Query(None, description="Search in name or email"),
    db: Session = Depends(get_db)
):
    event_id = data["event_id"]
    attendees = get_event_attendees(db, event_id, checked_in, search)
    if not attendees:
        return []
    return attendees


