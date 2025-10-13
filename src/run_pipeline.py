from __future__ import annotations

import argparse
import os

import pandas as pd

from .backtest.backtest_bt import run as run_backtest
from .data.collector import fetch_ohlcv
from .features.alpha import add_tech_indicators
from .models.xgb_model import evaluate, train_model
from .strategies.signal_generator import label_next_move
from .utils.logger import get_logger

log = get_logger("pipeline")


def run(symbol: str, exchange: str, tf: str, lookback_days: int) -> None:
    candles_requested = lookback_days * 24
    df = fetch_ohlcv(symbol, exchange, tf, lookback_candles=min(2000, candles_requested))
    feats = add_tech_indicators(df)
    labeled = label_next_move(feats, horizon=1, threshold=0.0)
    if labeled.empty:
        raise ValueError("No labeled data generated; increase lookback or adjust parameters.")

    os.makedirs("data", exist_ok=True)
    feature_csv = f"data/{symbol.replace('/', '')}_{tf}_features.csv"
    labeled.to_csv(feature_csv, index=False)
    log.info("Saved features and labels to %s", feature_csv)

    os.makedirs("models", exist_ok=True)
    model_path = f"models/xgb_{symbol.replace('/', '')}_{tf}.pkl"
    model, cv_auc = train_model(labeled, save_path=model_path)
    metrics = evaluate(model, labeled)
    log.info("Model saved to %s (CV AUC=%.3f)", model_path, cv_auc)
    log.info("In-sample metrics: %s", metrics)

    bt_df = labeled.copy()
    bt_df["pred"] = 0.5
    backtest_csv = f"data/{symbol.replace('/', '')}_{tf}_backtest.csv"
    bt_df[["ts", "open", "high", "low", "close", "volume", "pred"]].to_csv(backtest_csv, index=False)
    perf = run_backtest(backtest_csv, start_cash=1000.0)
    log.info("Backtest result: %s", perf)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", default="SOL/USDT")
    parser.add_argument("--exchange", default="coindcx")
    parser.add_argument("--tf", default="1h")
    parser.add_argument("--lookback_days", type=int, default=120)
    args = parser.parse_args()
    run(args.symbol, args.exchange, args.tf, args.lookback_days)


if __name__ == "__main__":
    main()
