from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import json
from pathlib import Path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model for creating a note
class Note(BaseModel):
    title: str
    content: str

# Model for updating a note
class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

# Permanent storage for notes
DATA_FILE = Path(__file__).parent / "notes.json"

def load_notes():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def save_notes():
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(notes, file, indent=4)

notes = load_notes()
next_id = max((note["id"] for note in notes), default=0) + 1


# Home route
@app.get("/")
def home():
    return {"message": "Notes Application API is running"}


# Get all notes or search notes
@app.get("/notes")
def get_notes(search: Optional[str] = None):
    if search:
        query = search.lower()
        return [
            note for note in notes
            if query in note["title"].lower()
            or query in note["content"].lower()
        ]

    return notes


# Create a new note
@app.post("/notes")
def create_note(note: Note):
    global next_id

    new_note = {
        "id": next_id,
        "title": note.title,
        "content": note.content
    }

    notes.append(new_note)
    save_notes()
    next_id += 1

    return new_note


# Update an existing note
@app.put("/notes/{note_id}")
def update_note(note_id: int, updated: NoteUpdate):
    for note in notes:
        if note["id"] == note_id:
            if updated.title is not None:
                note["title"] = updated.title

            if updated.content is not None:
                note["content"] = updated.content
            save_notes()
            return note

    raise HTTPException(
        status_code=404,
        detail="Note not found"
    )


# Delete a note
@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    for note in notes:
        if note["id"] == note_id:
            notes.remove(note)
            save_notes()
            return {"message": "Note deleted successfully"}

    raise HTTPException(
        status_code=404,
        detail="Note not found"
    )