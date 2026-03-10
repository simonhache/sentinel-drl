from datetime import datetime

from sentinel_rl.ingestion.market.ccxt_client import ExchangeClient
from sentinel_rl.ingestion.market.market_fetcher import MarketDataFetcher
from ingestion.repair.repair_service import MarketDataRepairService
from ingestion.market.historical_backfill import HistoricalBackfillService


def run_backfill_job():
    client = ExchangeClient()

    fetcher = MarketDataFetcher(client, symbol="BTC/USDT", timeframe="15m")

    service = HistoricalBackfillService(fetcher, source_id="binance_btc_usdt_15m")

    service.run(datetime(2020, 1, 1))


def run_repair_job():
    client = ExchangeClient()

    fetcher = MarketDataFetcher(client, symbol="BTC/USDT", timeframe="15m")

    service = MarketDataRepairService(fetcher, symbol="BTC/USDT", timeframe_seconds=900)

    service.repair(datetime(2020, 1, 1), datetime(2024, 1, 1))
