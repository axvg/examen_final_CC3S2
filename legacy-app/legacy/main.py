from fastapi import FastAPI
from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from contextlib import contextmanager
import sqlite3
from pathlib import Path
import uvicorn

class NoteRequest(BaseModel):
    name: str = Field(..., example="sample note", description="Nombre único de la nota")
    description: Optional[str] = Field(
        None, example="optional description", description="Descripción opcional de la nota"
    )


class NoteResponse(NoteRequest):
    id: int = Field(..., description="Identificador único de la nota")


DB_PATH = Path("app.db")


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()


def add_note(name: str, description: Optional[str] = None) -> int:
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO notes (name, description) VALUES (?, ?)",
            (name, description)
        )
        conn.commit()
        note_id = cursor.lastrowid
        return note_id


def list_notes() -> List[Dict[str, Optional[str]]]:
    with get_conn() as conn:
        cursor = conn.execute(
            "SELECT id, name, description, created_at FROM notes"
        )
        rows = cursor.fetchall()

    result = [
        {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "created_at": row[3],
        }
        for row in rows
    ]
    return result

def create_note(name: str, description: Optional[str] = None) -> Dict[str, Optional[int or str]]:
    note_id = add_note(name, description)

    note = {
        "id": note_id,
        "name": name,
        "description": description,
    }

    return note


def get_all_notes() -> List[Dict[str, Optional[int or str]]]:
    try:
        notes = list_notes()
        return notes
    except Exception as exc:
        return []


def get_application() -> FastAPI:
    app = FastAPI(
        title="Legacy notes",
        description="Legacy para notes",
        version="0.1.0",
        docs_url="/",
        redoc_url=None,
    )

    @app.on_event("startup")
    def on_startup() -> None:
        init_db()

    return app

app = get_application()

@app.post("/api/note")
def post_note(note: NoteRequest) -> NoteResponse:
    try:
        created = create_note(note.name, note.description)
        return created
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )


@app.get("/api/note")
def get_notes() -> List[NoteResponse]:
    try:
        return get_all_notes()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener notass"
        )

if __name__ == "__main__":
    uvicorn.run(
        "legacy.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
