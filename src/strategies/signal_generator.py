from __future__ import annotations

import pandas as pd


def label_next_move(df: pd.DataFrame, horizon: int = 1, threshold: float = 0.0) -> pd.DataFrame:
    """
    Binary classification target:
    y = 1 if forward return over the horizon exceeds the threshold, else 0.
    """
    df = df.copy()
    df["fwd_ret"] = df["close"].shift(-horizon) / df["close"] - 1.0
    df["y"] = (df["fwd_ret"] > threshold).astype(int)
    df.dropna(inplace=True)
    return df
