from datetime import datetime
import pandas as pd

from sentinel_rl.db.session import SessionLocal
from sentinel_rl.db.repositories.ingestion_state_repository import (
    IngestionStateRepository,
)
from sentinel_rl.features.pipeline import FeaturePipeline
from sentinel_rl.features.repository import FeatureRepository


class FeatureGenerationService:
    def __init__(self, symbol: str, pipeline: FeaturePipeline, source_id: str):
        self.symbol = symbol
        self.pipeline = pipeline
        self.source_id = source_id

    def run(self):
        with SessionLocal() as session:
            state_repo = IngestionStateRepository(session)
            feature_repo = FeatureRepository(session)

            cursor = state_repo.get_cursor(self.source_id)

            candles_df = feature_repo.load_candles_after(self.symbol, cursor)

        if candles_df.empty:
            print("No new candles for feature generation")
            return

        features_df = self.pipeline.run(candles_df)

        features = features_df.to_dict("records")

        with SessionLocal() as session:
            feature_repo = FeatureRepository(session)

            feature_repo.upsert_features(features)

            last_timestamp = features_df["timestamp"].max()

            state_repo = IngestionStateRepository(session)

            state_repo.update_cursor(self.source_id, last_timestamp)

        print(f"Generated features up to {last_timestamp}")
