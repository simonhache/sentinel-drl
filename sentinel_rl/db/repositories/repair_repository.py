from sqlalchemy import text
from datetime import datetime
from sqlalchemy.orm import Session


class RepairRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_missing_candles(
        self, symbol: str, start: datetime, end: datetime, timeframe="15 minutes"
    ):
        query = text("""
        SELECT expected_ts
        FROM generate_series(
            :start,
            :end,
            interval :tf
        ) AS expected_ts
        LEFT JOIN market_ohlcv m
        ON m.timestamp = expected_ts
        AND m.symbol = :symbol
        WHERE m.timestamp IS NULL
        ORDER BY expected_ts
        """)

        result = self.session.execute(
            query, {"start": start, "end": end, "tf": timeframe, "symbol": symbol}
        )

        return [r[0] for r in result]
