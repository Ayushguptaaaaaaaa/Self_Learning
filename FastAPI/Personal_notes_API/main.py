from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import User, Note
from schemas import UserRegister, UserLogin, UserResponse, NoteCreate, NoteUpdate, NoteResponse, LoginResponse
from auth import hash_password, verify_password, create_access_token, get_current_user
import json

# Create FastAPI instance
app = FastAPI(title="Personal Notes API")

# Create tables on startup
Base.metadata.create_all(bind=engine)


@app.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserRegister, db: Session = Depends(get_db)):
    """Register a new user"""
    
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )
    
    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )
    
    # Hash password
    hashed_password = hash_password(user.password)
    
    # Create new user
    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )
    
    # Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@app.post("/auth/login", response_model=LoginResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """Login user and return JWT token"""
    
    # Find user by username
    db_user = db.query(User).filter(User.username == user.username).first()
    
    # Check if user exists
    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    
    # Verify password
    if not verify_password(user.password, db_user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    
    # Create JWT token
    access_token = create_access_token(data={"sub": db_user.username})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.post("/notes", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Create a new note"""
    
    # Convert tags list to JSON string
    tags_json = json.dumps(note.tags)
    
    # Create new note
    new_note = Note(
        user_id=current_user.id,
        title=note.title,
        content=note.content,
        tags=tags_json,
        is_favorite=note.is_favorite
    )
    
    # Save to database
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    
    # Convert tags back to list before returning
    new_note.tags = json.loads(new_note.tags)
    
    return new_note

@app.get("/notes", response_model=list[NoteResponse])
def get_notes(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db),
    search: str = None,
    tag: str = None,
    limit: int = 10,
    offset: int = 0
):
    """Get all notes for current user with optional filtering"""
    
    # Start query for current user's notes
    query = db.query(Note).filter(Note.user_id == current_user.id)
    
    # Filter by search term in title
    if search:
        query = query.filter(Note.title.contains(search))
    
    # Filter by tag
    if tag:
        query = query.filter(Note.tags.contains(f'"{tag}"'))
    
    # Get paginated results
    notes = query.limit(limit).offset(offset).all()
    
    # Convert tags from JSON string to list
    for note in notes:
        note.tags = json.loads(note.tags)
    
    return notes


@app.get("/notes/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: int, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Get a specific note"""
    
    # Find note by ID
    note = db.query(Note).filter(Note.id == note_id).first()
    
    # Check if note exists
    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )
    
    # Check if note belongs to current user (SECURITY!)
    if note.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to access this note"
        )
    
    # Convert tags from JSON to list
    note.tags = json.loads(note.tags)
    
    return note


@app.put("/notes/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int, 
    note_update: NoteUpdate,
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Update a note"""
    
    # Find note by ID
    note = db.query(Note).filter(Note.id == note_id).first()
    
    # Check if note exists
    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )
    
    # Check if note belongs to current user (SECURITY!)
    if note.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to update this note"
        )
    
    # Update fields
    note.title = note_update.title
    note.content = note_update.content
    note.tags = json.dumps(note_update.tags)  # Convert list to JSON
    note.is_favorite = note_update.is_favorite
    
    # Save to database
    db.commit()
    db.refresh(note)
    
    # Convert tags back to list
    note.tags = json.loads(note.tags)
    
    return note


@app.delete("/notes/{note_id}")
def delete_note(
    note_id: int, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Delete a note"""
    
    # Find note by ID
    note = db.query(Note).filter(Note.id == note_id).first()
    
    # Check if note exists
    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )
    
    # Check if note belongs to current user (SECURITY!)
    if note.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to delete this note"
        )
    
    # Delete from database
    db.delete(note)
    db.commit()
    
    return {"message": "Note deleted successfully"}