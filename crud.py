from sqlalchemy.orm import Session
from models import *
from schemas import *

def create_event(db: Session, event: EventCreate):
    db_event = Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_events(db: Session):
    return db.query(Event).all()

def register_attendee(db: Session, attendee: AttendeeCreate):
    db_attendee = Attendee(**attendee.dict())
    db.add(db_attendee)
    db.commit()
    db.refresh(db_attendee)
    return db_attendee

def check_in_attendee(db: Session, attendee_id: str):
    attendee = db.query(Attendee).filter(Attendee.attendee_id == attendee_id).first()
    if not attendee:
        return None
    attendee.check_in_status = True
    db.commit()
    db.refresh(attendee)
    return attendee

def get_event_attendees(
    db: Session, 
    event_id: int, 
    checked_in: bool = None, 
    search: str = None
):
    query = db.query(Attendee).filter(Attendee.event_id == event_id)
    
    if checked_in is not None:
        query = query.filter(Attendee.check_in_status == checked_in)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Attendee.first_name.ilike(search_term)) |
            (Attendee.last_name.ilike(search_term)) |
            (Attendee.email.ilike(search_term))
        )
    
    return query.all()


def update_event(db: Session, event_id: int, event_update: EventCreate):
    db_event = db.query(Event).filter(Event.event_id == event_id).first()
    if not db_event:
        return None
    for key, value in event_update.dict().items():
        setattr(db_event, key, value)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_events(db: Session, event_id: int):
    return db.query(Event).filter(Event.event_id == event_id).first()