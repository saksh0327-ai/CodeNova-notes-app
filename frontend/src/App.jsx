import { useEffect, useState } from 'react'
import './App.css'

const API_URL = 'http://127.0.0.1:8000/notes'

function App() {
  const [notes, setNotes] = useState([])
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  useEffect(() => {
    fetch(API_URL)
      .then((response) => response.json())
      .then((data) => setNotes(data))
      .catch((error) => console.error('Error loading notes:', error))
  }, [])

  async function addNote(e) {
    e.preventDefault()

    if (!title.trim() || !content.trim()) {
      alert('Please enter both title and content.')
      return
    }

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: title.trim(),
          content: content.trim(),
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to save note')
      }

      const newNote = await response.json()
      setNotes((previousNotes) => [...previousNotes, newNote])
      setTitle('')
      setContent('')
    } catch (error) {
      console.error(error)
      alert('Could not save note. Check whether the backend is running.')
    }
  }
async function deleteNote(id) {
  try {
    const response = await fetch(`${API_URL}/${id}`, {
      method: 'DELETE',
    })

    if (!response.ok) {
      throw new Error('Failed to delete note')
    }

    setNotes((previousNotes) =>
      previousNotes.filter((note) => note.id !== id)
    )
  } catch (error) {
    console.error(error)
    alert('Could not delete note. Please try again.')
  }
}

async function updateNote(id, updatedTitle, updatedContent) {
  try {
    const response = await fetch(`${API_URL}/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        title: updatedTitle,
        content: updatedContent,
      }),
    })

    if (!response.ok) {
      throw new Error('Failed to update note')
    }

    const updatedNote = await response.json()

    setNotes((previousNotes) =>
      previousNotes.map((note) =>
        note.id === id ? updatedNote : note
      )
    )
  } catch (error) {
    console.error(error)
    alert('Could not update note. Please try again.')
  }
}

  return (
    <main className="app">
      <header className="header">
        <h1>My Notes</h1>
        <p>Write down your ideas and keep them organized.</p>
      </header>

      <form className="note-form" onSubmit={addNote}>
        <input
          type="text"
          placeholder="Note title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />

        <textarea
          placeholder="Write your note here..."
          value={content}
          onChange={(e) => setContent(e.target.value)}
          rows="4"
        />

        <button type="submit">Add Note</button>
      </form>

      <section className="notes-section">
        <h2>Your Notes ({notes.length})</h2>

        {notes.length === 0 ? (
          <p className="empty">No notes yet. Create your first note!</p>
        ) : (
          <div className="notes-grid">
            {notes.map((note) => (
              <article className="note-card" key={note.id}>
  <h3>{note.title}</h3>
  <p>{note.content}</p>

  <button
    onClick={() => {
      const updatedTitle = prompt('Enter the updated title:', note.title)
      if (updatedTitle === null) return

      const updatedContent = prompt('Enter the updated content:', note.content)
      if (updatedContent === null) return

      if (!updatedTitle.trim() || !updatedContent.trim()) {
        alert('Title and content cannot be empty.')
        return
      }

      updateNote(note.id, updatedTitle.trim(), updatedContent.trim())
    }}
  >
    Edit
  </button>

  <button
    className="delete-button"
    onClick={() => deleteNote(note.id)}
  >
    Delete
  </button>
</article>
            ))}
          </div>
        )}
      </section>
    </main>
  )
}

export default App