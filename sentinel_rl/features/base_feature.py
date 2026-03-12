from abc import ABC, abstractmethod
import pandas as pd


class Feature(ABC):
    name: str

    @abstractmethod
    def compute(self, df: pd.DataFrame) -> pd.DataFrame:
        pass
