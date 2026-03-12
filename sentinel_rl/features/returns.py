import numpy as np
import pandas as pd
from sentinel_rl.features.base_feature import Feature


class ReturnsFeature(Feature):
    name = "returns"

    def compute(self, df: pd.DataFrame) -> pd.DataFrame:
        df["return_1"] = np.log(df["close"]).diff()
        df["return_5"] = np.log(df["close"]).diff(5)

        return df
