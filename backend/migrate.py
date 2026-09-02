"""Minimal additive migration for the demo partner-capability fields.

Run once against an existing Postgres/PostGIS database before deploying this
version. It intentionally never drops data.
"""

from sqlalchemy import text

from database import engine


STATEMENTS = [
    "ALTER TABLE channel_partners ADD COLUMN IF NOT EXISTS supported_schemes VARCHAR DEFAULT ''",
    "ALTER TABLE channel_partners ADD COLUMN IF NOT EXISTS overdue_ratio FLOAT DEFAULT 0",
]


def migrate():
    with engine.begin() as connection:
        for statement in STATEMENTS:
            connection.execute(text(statement))
    print("Partner capability fields are ready.")


if __name__ == "__main__":
    migrate()
