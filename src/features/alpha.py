from __future__ import annotations

import numpy as np
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, MACD
from ta.volatility import BollingerBands


def add_tech_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Augment OHLCV data with a curated set of technical indicators."""
    df = df.copy()
    df["ret1"] = df["close"].pct_change()
    df["logret1"] = np.log1p(df["ret1"])
    rsi = RSIIndicator(close=df["close"], window=14)
    df["rsi14"] = rsi.rsi()
    ema_fast = EMAIndicator(close=df["close"], window=12)
    ema_slow = EMAIndicator(close=df["close"], window=26)
    df["ema12"] = ema_fast.ema_indicator()
    df["ema26"] = ema_slow.ema_indicator()
    macd = MACD(close=df["close"], window_slow=26, window_fast=12, window_sign=9)
    df["macd"] = macd.macd()
    df["macd_sig"] = macd.macd_signal()
    bb = BollingerBands(close=df["close"], window=20, window_dev=2)
    df["bb_hi"] = bb.bollinger_hband()
    df["bb_lo"] = bb.bollinger_lband()
    df["bb_pct"] = (df["close"] - df["bb_lo"]) / (df["bb_hi"] - df["bb_lo"])
    df["vol"] = df["logret1"].rolling(24).std() * np.sqrt(24)
    df.dropna(inplace=True)
    return df
