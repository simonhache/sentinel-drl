import time
from datetime import datetime

from sentinel_rl.db.session import SessionLocal
from sentinel_rl.db.repositories.ingestion_state_repository import (
    IngestionStateRepository,
)
from sentinel_rl.db.repositories.market_repository import UpsertMarketData
from sentinel_rl.ingestion.market.market_fetcher import MarketDataFetcher
from sentinel_rl.ingestion.market.models import OHLCV


MAX_RETRIES = 5


class HistoricalBackfillService:
    def __init__(self, fetcher: MarketDataFetcher, source_id: str):
        self.fetcher = fetcher
        self.source_id = source_id

    def run(self, initial_start: datetime):
        with SessionLocal() as session:
            state_repo = IngestionStateRepository(session)

            cursor = state_repo.get_cursor(self.source_id)

            if cursor is None:
                since = int(initial_start.timestamp() * 1000)
            else:
                since = int(cursor.timestamp() * 1000)

        while True:
            for attempt in range(MAX_RETRIES):
                try:
                    rows = self.fetcher.fetch_batch(since)

                    if not rows:
                        print("Ingestion complete")
                        return

                    self.detect_gap(rows, 900)

                    # Insert data
                    UpsertMarketData.apply(rows, SessionLocal)

                    last_timestamp = rows[-1].timestamp

                    # Update cursor AFTER successful insert
                    with SessionLocal() as session:
                        state_repo = IngestionStateRepository(session)

                        state_repo.update_cursor(self.source_id, last_timestamp)

                    since = int(last_timestamp.timestamp() * 1000)

                    print("Cursor updated:", last_timestamp)

                    time.sleep(1)

                except Exception as e:
                    print("Fetch failed:", e)

                    if attempt == MAX_RETRIES - 1:
                        raise

                    time.sleep(2**attempt)

    def detect_gap(self, rows: list[OHLCV], expected_interval_seconds: int):
        for i in range(1, len(rows)):
            delta = (rows[i].timestamp - rows[i - 1].timestamp).total_seconds()

            if delta != expected_interval_seconds:
                raise ValueError(
                    f"Data gap detected: {rows[i - 1].timestamp} -> {rows[i].timestamp}"
                )

    def validate_candle(self, rows: list[OHLCV]):
        for row in rows:
            if row.high < row.low:
                raise ValueError("Invalid candle")

            if row.volume < 0:
                raise ValueError("Invalid volume")
