import pytest
from datetime import datetime, timezone
from sqlalchemy.orm import sessionmaker, Session

from sentinel_rl.db.repositories.market_repository import (
    UpsertMarketData,
    DeleteMarketData,
)
from sentinel_rl.db.models import MarketOHLCV


@pytest.fixture
def sample_rows():
    return [
        {
            "timestamp": datetime(2024, 1, 1, tzinfo=timezone.utc),
            "symbol": "BTC/USDT",
            "open": 50000,
            "high": 50500,
            "low": 49500,
            "close": 50200,
            "volume": 120.5,
        }
    ]


def test_upsert_market_data_calls_execute_and_commit(
    sample_rows, local_db_session_factory: sessionmaker[Session]
):
    # Act
    UpsertMarketData.apply(sample_rows, session_factory=local_db_session_factory)

    with local_db_session_factory() as session:
        result = session.query(MarketOHLCV).first()

    # Assert
    assert result.symbol == "BTC/USDT"
    assert result.close == 50200


def test_upsert_updates_existing_row(local_db_session_factory: sessionmaker[Session]):
    rows1 = [
        {
            "timestamp": datetime(2024, 1, 1, tzinfo=timezone.utc),
            "symbol": "BTC/USDT",
            "open": 50000,
            "high": 50500,
            "low": 49500,
            "close": 50200,
            "volume": 100,
        }
    ]

    rows2 = [
        {
            "timestamp": datetime(2024, 1, 1, tzinfo=timezone.utc),
            "symbol": "BTC/USDT",
            "open": 50000,
            "high": 50500,
            "low": 49500,
            "close": 51000,
            "volume": 150,
        }
    ]

    UpsertMarketData.apply(rows1, local_db_session_factory)
    UpsertMarketData.apply(rows2, local_db_session_factory)

    with local_db_session_factory() as session:
        row = session.query(MarketOHLCV).first()

    assert row.close == 51000
    assert row.volume == 150


def test_delete_market_data_calls_execute_and_commit(
    sample_rows, local_db_session_factory: sessionmaker[Session]
):
    # arrange
    UpsertMarketData.apply(sample_rows, session_factory=local_db_session_factory)
    with local_db_session_factory() as session:
        initial_result = session.query(MarketOHLCV).all()

    assert len(initial_result) == 1

    # Act
    DeleteMarketData.apply(sample_rows, session_factory=local_db_session_factory)

    # Assert

    with local_db_session_factory() as session:
        result = session.query(MarketOHLCV).all()

    assert len(result) == 0
