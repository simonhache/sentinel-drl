from datetime import datetime, timezone

from sentinel_rl.db.repositories.ingestion_state_repository import (
    IngestionStateRepository,
)
from sqlalchemy.orm import sessionmaker, Session


def test_cursor_write_and_read(local_db_session_factory: sessionmaker[Session]):
    session = local_db_session_factory()
    repo = IngestionStateRepository(session)

    ts = datetime(2023, 1, 1)

    repo.update_cursor("test_source", ts)

    cursor = repo.get_cursor("test_source")

    assert cursor == ts
