from sentinel_rl.features.base_feature import Feature
import pandas as pd


class FeaturePipeline:
    def __init__(self, features: list[Feature]):
        self.features = features

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        for f in self.features:
            df = f.compute(df)

        return df
