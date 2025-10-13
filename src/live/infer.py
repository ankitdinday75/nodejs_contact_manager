from __future__ import annotations

import joblib
import pandas as pd

from ..features.alpha import add_tech_indicators
from ..models.xgb_model import FEATURES


class LiveInference:
    def __init__(self, model_path: str) -> None:
        self.model = joblib.load(model_path)

    def predict_proba(self, candles_df: pd.DataFrame) -> float:
        """
        Parameters
        ----------
        candles_df : DataFrame
            Columns: ts, open, high, low, close, volume (UTC timestamps).

        Returns
        -------
        float
            Probability of an upward move on the next candle.
        """
        feats = add_tech_indicators(candles_df)
        if feats.empty:
            return 0.5
        X = feats[FEATURES].values[-1:].copy()
        proba = self.model.predict_proba(X)[0, 1]
        return float(proba)
