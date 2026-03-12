from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from db.models import MarketOHLCV, FeatureCandle
from sentinel_rl.ingestion.market.models import OHLCV
from datetime import datetime

import pandas as pd


class FeatureRepository:
    def __init__(self, session: Session):
        self.session = session

    def load_candles_after(self, symbol: str, cursor: datetime | None) -> pd.DataFrame:
        query = select(MarketOHLCV).where(MarketOHLCV.symbol == symbol)

        if cursor:
            query = query.where(MarketOHLCV.timestamp > cursor)

        query = query.order_by(MarketOHLCV.timestamp)

        result = self.session.execute(query)

        rows = result.scalars().all()

        data = [
            OHLCV(
                timestamp=r.timestamp,
                symbol=r.symbol,
                open=r.open,
                high=r.high,
                low=r.low,
                close=r.close,
                volume=r.volume,
            )
            for r in rows
        ]

        return pd.DataFrame(data)

    def upsert_features(self, rows):
        if not rows:
            return

        feature_columns = [
            c.name
            for c in FeatureCandle.__table__.columns
            if c.name not in ["timestamp", "symbol"]
        ]

        stmt = insert(FeatureCandle).values(rows)

        stmt = stmt.on_conflict_do_update(
            index_elements=["symbol", "timestamp"],
            set_={col: getattr(stmt.excluded, col) for col in feature_columns},
        )

        self.session.execute(stmt)

        self.session.commit()
