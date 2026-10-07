"""
Collin Knowledge Database

Lightweight SQLite storage for Collin's learned procedures.
"""

import json
import sqlite3
from pathlib import Path
from typing import Any


DATABASE_DIR = Path(__file__).resolve().parent.parent / "data"
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_PATH = DATABASE_DIR / "collin.db"


class KnowledgeDatabase:
    """Stores and retrieves Collin's learned knowledge."""

    def __init__(self, database_path: str | None = None) -> None:
        self.database_path = Path(
            database_path or DATABASE_PATH
        ).expanduser().resolve()

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        """Create a database connection."""

        connection = sqlite3.connect(
            self.database_path
        )

        connection.row_factory = sqlite3.Row

        return connection

    def _initialize(self) -> None:
        """Create required database tables."""

        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS procedures (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    description TEXT NOT NULL DEFAULT '',
                    status TEXT NOT NULL DEFAULT 'taught',
                    version INTEGER NOT NULL DEFAULT 1,
                    data TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            connection.commit()

    def save_procedure(
        self,
        procedure: dict[str, Any],
        status: str = "taught",
    ) -> int:
        """Save or update a learned procedure."""

        name = procedure.get("name")

        if not name:
            raise ValueError(
                "Procedure must contain a name."
            )

        description = procedure.get(
            "description",
            "",
        )

        version = procedure.get(
            "version",
            1,
        )

        data = json.dumps(
            procedure,
            ensure_ascii=False,
        )

        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO procedures (
                    name,
                    description,
                    status,
                    version,
                    data
                )
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET
                    description = excluded.description,
                    status = excluded.status,
                    version = excluded.version,
                    data = excluded.data,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (
                    name,
                    description,
                    status,
                    version,
                    data,
                ),
            )

            connection.commit()

            row = connection.execute(
                """
                SELECT id
                FROM procedures
                WHERE name = ?
                """,
                (name,),
            ).fetchone()

        return int(row["id"])

    def get_procedure(
        self,
        name: str,
    ) -> dict[str, Any] | None:
        """Retrieve a procedure by name."""

        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT data
                FROM procedures
                WHERE name = ?
                """,
                (name,),
            ).fetchone()

        if row is None:
            return None

        return json.loads(row["data"])

    def list_procedures(self) -> list[dict[str, Any]]:
        """Return all stored procedures."""

        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    name,
                    description,
                    status,
                    version
                FROM procedures
                ORDER BY name
                """
            ).fetchall()

        return [
            {
                "name": row["name"],
                "description": row["description"],
                "status": row["status"],
                "version": row["version"],
            }
            for row in rows
        ]

    def delete_procedure(
        self,
        name: str,
    ) -> bool:
        """Delete a stored procedure."""

        with self._connect() as connection:
            cursor = connection.execute(
                """
                DELETE FROM procedures
                WHERE name = ?
                """,
                (name,),
            )

            connection.commit()

        return cursor.rowcount > 0


def main() -> None:
    """Safe database test."""

    database = KnowledgeDatabase()

    procedure = {
        "name": "test_procedure",
        "description": "Database test procedure.",
        "version": 1,
        "steps": [
            {
                "action": "open_application",
                "target": "Chrome",
                "details": {},
            }
        ],
    }

    procedure_id = database.save_procedure(
        procedure
    )

    print("Knowledge database: OK")
    print("Database:", database.database_path)
    print("Procedure ID:", procedure_id)
    print("Stored:", database.get_procedure("test_procedure"))
    print("Procedures:", database.list_procedures())

    database.delete_procedure("test_procedure")

    print(
        "Test procedure removed:",
        database.get_procedure("test_procedure") is None,
    )


if __name__ == "__main__":
    main()
