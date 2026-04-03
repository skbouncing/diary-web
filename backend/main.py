from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models, schemas, database
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="My Diary API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/entries", response_model=List[schemas.DiaryEntryResponse])
def get_entries(db: Session = Depends(get_db)):
    return db.query(models.DiaryEntry).order_by(models.DiaryEntry.created_at.desc()).all()

@app.get("/entries/{entry_id}", response_model=schemas.DiaryEntryResponse)
def get_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.DiaryEntry).filter(models.DiaryEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="일기를 찾을 수 없습니다")
    return entry

@app.post("/entries", response_model=schemas.DiaryEntryResponse, status_code=201)
def create_entry(entry: schemas.DiaryEntryCreate, db: Session = Depends(get_db)):
    db_entry = models.DiaryEntry(**entry.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@app.put("/entries/{entry_id}", response_model=schemas.DiaryEntryResponse)
def update_entry(entry_id: int, entry: schemas.DiaryEntryUpdate, db: Session = Depends(get_db)):
    db_entry = db.query(models.DiaryEntry).filter(models.DiaryEntry.id == entry_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="일기를 찾을 수 없습니다")
    for field, value in entry.dict(exclude_unset=True).items():
        setattr(db_entry, field, value)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@app.delete("/entries/{entry_id}", status_code=204)
def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    db_entry = db.query(models.DiaryEntry).filter(models.DiaryEntry.id == entry_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="일기를 찾을 수 없습니다")
    db.delete(db_entry)
    db.commit()