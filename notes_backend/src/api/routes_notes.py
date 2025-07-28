from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from . import models, schemas, db, auth

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)

# PUBLIC_INTERFACE
@router.post("/", response_model=schemas.NoteRead, status_code=201, summary="Create a Note", description="Create a new note for the authenticated user.")
def create_note(note_in: schemas.NoteCreate, db: Session = Depends(db.get_db), current_user: models.User = Depends(auth.get_current_user)):
    """Create a new note for the current user."""
    note = models.Note(**note_in.dict(), owner_id=current_user.id)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

# PUBLIC_INTERFACE
@router.get("/", response_model=List[schemas.NoteRead], summary="List Notes", description="List all notes for the current user.")
def list_notes(skip: int = 0, limit: int = 20, db: Session = Depends(db.get_db), current_user: models.User = Depends(auth.get_current_user)):
    """List notes for the current user."""
    return db.query(models.Note).filter(models.Note.owner_id == current_user.id).order_by(models.Note.updated_at.desc()).offset(skip).limit(limit).all()

# PUBLIC_INTERFACE
@router.get("/{note_id}", response_model=schemas.NoteRead, summary="Get a Note", description="Get a single note by ID (must be owned by the current user).")
def read_note(note_id: int, db: Session = Depends(db.get_db), current_user: models.User = Depends(auth.get_current_user)):
    """Read a single note belonging to the current user."""
    note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.owner_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

# PUBLIC_INTERFACE
@router.put("/{note_id}", response_model=schemas.NoteRead, summary="Update a Note", description="Update a note (title/content) for the current user.")
def update_note(note_id: int, note_in: schemas.NoteUpdate, db: Session = Depends(db.get_db), current_user: models.User = Depends(auth.get_current_user)):
    """Update the contents of a note."""
    note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.owner_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    update_data = note_in.dict(exclude_unset=True)
    for var, value in update_data.items():
        setattr(note, var, value)
    db.commit()
    db.refresh(note)
    return note

# PUBLIC_INTERFACE
@router.delete("/{note_id}", status_code=204, summary="Delete a Note", description="Delete a note owned by the current user.")
def delete_note(note_id: int, db: Session = Depends(db.get_db), current_user: models.User = Depends(auth.get_current_user)):
    """Delete a note."""
    note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.owner_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return

# PUBLIC_INTERFACE
@router.get("/search/", response_model=List[schemas.NoteRead], summary="Search Notes", description="Full text search notes by keyword in title/content.")
def search_notes(q: str = Query(..., description="Search query for title/content."), db: Session = Depends(db.get_db), current_user: models.User = Depends(auth.get_current_user)):
    """Simple case-insensitive search for notes in title or content."""
    search = f"%{q}%"
    notes = db.query(models.Note).filter(
        models.Note.owner_id == current_user.id,
        (models.Note.title.ilike(search)) | (models.Note.content.ilike(search))
    ).order_by(models.Note.updated_at.desc()).all()
    return notes
