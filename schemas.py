from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from models import EventStatus

class EventCreate(BaseModel):
    name: str
    description: str
    start_time: datetime
    end_time: datetime
    location: str
    max_attendees: int

class EventResponse(EventCreate):
    event_id: int
    status: EventStatus
    class Config:
        from_attributes = True

class AttendeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    event_id: int  # Added event_id field for registration

class AttendeeResponse(AttendeeCreate):
    attendee_id: int
    check_in_status: bool
    event_id: int
    class Config:
        from_attributes = True


class EventUpdate(BaseModel):
    event_id: int
    name: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    max_attendees: Optional[int] = None
    status: Optional[EventStatus] = None
    
    class Config:
        from_attributes = True
    