from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from app.models import EventStatus

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
        orm_mode = True

class AttendeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str

class AttendeeResponse(AttendeeCreate):
    attendee_id: int
    check_in_status: bool
    event_id: int
    class Config:
        orm_mode = True