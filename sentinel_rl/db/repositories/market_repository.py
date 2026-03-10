from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import delete
from sentinel_rl.db.session import SessionLocal
from sqlalchemy.orm import sessionmaker, Session
from sentinel_rl.db.models import MarketOHLCV
from abc import ABC, abstractmethod
from sentinel_rl.ingestion.market.models import OHLCV


class BasicCRUD(ABC):
    @classmethod
    def apply(
        cls, rows: list[OHLCV], session_factory: sessionmaker[Session] = SessionLocal
    ):
        with session_factory() as session:
            cls._logic(rows, session)
            session.commit()

    @classmethod
    @abstractmethod
    def _logic(cls, rows: list[OHLCV], session):
        pass


class UpsertMarketData(BasicCRUD):
    @classmethod
    def _logic(cls, rows: list[OHLCV], session: Session):
        stmt = insert(MarketOHLCV).values(
            [
                {
                    "timestamp": row.timestamp,
                    "symbol": row.symbol,
                    "open": row.open,
                    "high": row.high,
                    "low": row.low,
                    "close": row.close,
                    "volume": row.volume,
                }
                for row in rows
            ]
        )

        stmt = stmt.on_conflict_do_update(
            index_elements=["timestamp", "symbol"],
            set_={
                "open": stmt.excluded.open,
                "high": stmt.excluded.high,
                "low": stmt.excluded.low,
                "close": stmt.excluded.close,
                "volume": stmt.excluded.volume,
            },
        )

        session.execute(stmt)


class DeleteMarketData(BasicCRUD):
    @classmethod
    def _logic(cls, rows: list[OHLCV], session: Session):
        for row in rows:
            stmt = delete(MarketOHLCV).where(
                (MarketOHLCV.timestamp == row.timestamp)
                & (MarketOHLCV.symbol == row.symbol)
            )
            session.execute(stmt)
