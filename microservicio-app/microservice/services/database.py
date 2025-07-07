from contextlib import contextmanager
from pathlib import Path
from typing import Dict, List, Optional

import sqlite3

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
        item_id = cursor.lastrowid
        return item_id


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
