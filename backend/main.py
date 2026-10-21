from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Notes Application")

# Model for creating a note
class Note(BaseModel):
    title: str
    content: str

# Model for updating a note
class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

# Temporary storage for notes
notes = []
next_id = 1


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
            return {"message": "Note deleted successfully"}

    raise HTTPException(
        status_code=404,
        detail="Note not found"
    )