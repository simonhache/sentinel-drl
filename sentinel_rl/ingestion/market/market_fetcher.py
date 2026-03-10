from ingestion.market.models import normalize_ohlcv, OHLCV
from sentinel_rl.ingestion.market.ccxt_client import ExchangeClient


class MarketDataFetcher:
    def __init__(
        self, exchange_client: ExchangeClient, symbol: str, timeframe: str = "15m"
    ):
        self.exchange = exchange_client
        self.symbol = symbol
        self.timeframe = timeframe

    def fetch_batch(self, since: int | None = None) -> list[OHLCV]:
        candles = self.exchange.fetch_ohlcv(
            symbol=self.symbol, timeframe=self.timeframe, since=since
        )

        rows = [
            normalize_ohlcv(self.symbol, candle, self.timeframe) for candle in candles
        ]

        return rows
