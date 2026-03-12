from datetime import datetime

from sentinel_rl.ingestion.market.ccxt_client import ExchangeClient
from sentinel_rl.ingestion.market.market_fetcher import MarketDataFetcher
from sentinel_rl.db.repositories.repair_repository import RepairRepository
from sentinel_rl.ingestion.repair.repair_service import MarketDataRepairService
from sentinel_rl.ingestion.market.historical_backfill import HistoricalBackfillService
from sentinel_rl.db.session import SessionLocal


def run_backfill_job():
    client = ExchangeClient()

    fetcher = MarketDataFetcher(client, symbol="BTC/USDT", timeframe="15m")

    service = HistoricalBackfillService(fetcher, source_id="binance_btc_usdt_15m")

    service.run(datetime(2020, 1, 1))


def run_repair_job():
    client = ExchangeClient()

    fetcher = MarketDataFetcher(client, symbol="BTC/USDT", timeframe="15m")

    with SessionLocal() as session:
        repo = RepairRepository(session)
        service = MarketDataRepairService(
            fetcher, repo, symbol="BTC/USDT", timeframe_seconds=900
        )

    service.repair(datetime(2020, 1, 1), datetime(2024, 1, 1))
