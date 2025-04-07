from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database, auth

router = APIRouter(prefix="/events", tags=["events"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.EventResponse)
def create_event(
    event: schemas.EventCreate, 
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    return crud.create_event(db, event)

@router.get("/", response_model=list[schemas.EventResponse])
def list_events(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    return crud.get_events(db)









# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app import crud, schemas, database

# router = APIRouter(prefix="/events", tags=["events"])

# def get_db():
#     db = database.SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @router.post("/", response_model=schemas.EventResponse)
# def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
#     return crud.create_event(db, event)

# @router.get("/", response_model=list[schemas.EventResponse])
# def list_events(db: Session = Depends(get_db)):
#     return crud.get_events(db)

