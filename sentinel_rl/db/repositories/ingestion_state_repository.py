from sentinel_rl.db.models import IngestionState
from sqlalchemy.orm import Session
from datetime import datetime


class IngestionStateRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_cursor(self, source: str) -> datetime | None:
        state = (
            self.session.query(IngestionState)
            .filter(IngestionState.source == source)
            .first()
        )

        if state:
            return state.last_timestamp

        return None

    def update_cursor(self, source: str, timestamp: datetime):
        state = (
            self.session.query(IngestionState)
            .filter(IngestionState.source == source)
            .first()
        )

        if state:
            state.last_timestamp = timestamp
        else:
            state = IngestionState(source=source, last_timestamp=timestamp)
            self.session.add(state)

        self.session.commit()
