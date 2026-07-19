import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone

from . import config


@dataclass
class Document:
    id: int
    title: str
    file_id: str


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(config.CACHE_DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            file_id TEXT NOT NULL,
            file_unique_id TEXT NOT NULL,
            added_at TEXT NOT NULL
        )
        """
    )
    return conn


def upsert_document(title: str, file_id: str, file_unique_id: str) -> None:
    conn = _connect()
    try:
        conn.execute(
            """
            INSERT INTO documents (title, file_id, file_unique_id, added_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(title) DO UPDATE SET file_id=excluded.file_id, file_unique_id=excluded.file_unique_id
            """,
            (title, file_id, file_unique_id, datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()
    finally:
        conn.close()


def list_documents() -> list[Document]:
    conn = _connect()
    try:
        rows = conn.execute("SELECT id, title, file_id FROM documents ORDER BY title COLLATE NOCASE").fetchall()
    finally:
        conn.close()
    return [Document(id=row[0], title=row[1], file_id=row[2]) for row in rows]


def get_document(doc_id: int) -> Document | None:
    conn = _connect()
    try:
        row = conn.execute("SELECT id, title, file_id FROM documents WHERE id = ?", (doc_id,)).fetchone()
    finally:
        conn.close()
    if row is None:
        return None
    return Document(id=row[0], title=row[1], file_id=row[2])
