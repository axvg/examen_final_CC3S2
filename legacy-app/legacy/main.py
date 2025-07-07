from fastapi import FastAPI
from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from contextlib import contextmanager
import sqlite3
from pathlib import Path
import uvicorn

class ItemRequest(BaseModel):
    name: str = Field(..., example="sample item", description="Nombre único del ítem")
    description: Optional[str] = Field(
        None, example="optional description", description="Descripción opcional del ítem"
    )


class ItemResponse(ItemRequest):
    id: int = Field(..., description="Identificador único del ítem")


DB_PATH = Path("app.db")


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS items (
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


def add_item(name: str, description: Optional[str] = None) -> int:
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO items (name, description) VALUES (?, ?)",
            (name, description)
        )
        conn.commit()
        item_id = cursor.lastrowid
        return item_id


def list_items() -> List[Dict[str, Optional[str]]]:
    with get_conn() as conn:
        cursor = conn.execute(
            "SELECT id, name, description, created_at FROM items"
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

def create_item(name: str, description: Optional[str] = None) -> Dict[str, Optional[int or str]]:
    item_id = add_item(name, description)

    item = {
        "id": item_id,
        "name": name,
        "description": description,
    }

    return item


def get_all_items() -> List[Dict[str, Optional[int or str]]]:
    try:
        items = list_items()
        return items
    except Exception as exc:
        return []


def get_application() -> FastAPI:
    app = FastAPI(
        title="Legacy todos ",
        description="Legacy para lista todos",
        version="0.1.0",
        docs_url="/",
        redoc_url=None,
    )

    @app.on_event("startup")
    def on_startup() -> None:
        init_db()

    return app

app = get_application()

@app.post("/api/item")
def post_item(item: ItemRequest) -> ItemResponse:
    try:
        created = create_item(item.name, item.description)
        return created
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )


@app.get("/api/item")
def get_items() -> List[ItemResponse]:
    try:
        return get_all_items()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al obtener los ítems"
        )

if __name__ == "__main__":
    uvicorn.run(
        "legacy.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
