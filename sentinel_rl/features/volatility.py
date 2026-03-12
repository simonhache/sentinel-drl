import pandas as pd
from sentinel_rl.features.base_feature import Feature


class VolatilityFeature(Feature):
    name = "volatility"

    def compute(self, df: pd.DataFrame) -> pd.DataFrame:
        df["volatility_20"] = df["return_1"].rolling(20).std()

        return df
