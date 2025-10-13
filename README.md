# Quant Trader – CoinDCX First (Starter)

A production-ready **starter** for a crypto quant trading project, tailored for **CoinDCX**:
- Data via `ccxt` (CoinDCX REST) and optional `ccxt.pro` (WebSocket).
- Feature engineering (`ta`) and **XGBoost** classifier.
- Backtesting (Backtrader) with dynamic **fee** fallback.
- **Live paper trading** with real model **inference** and strict **precision/lot-size** guards.

> ⚠️ Educational starter only. Crypto is risky. Backtests ≠ future results. Start with **paper** mode.

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env

# create sample data so everything runs locally
python scripts/make_sample.py

# End-to-end pipeline (download -> features -> labels -> train -> backtest)
python -m src.run_pipeline --symbol SOL/USDT --exchange coindcx --tf 1h --lookback_days 120

# Backtest on generated sample
python -m src.backtest.backtest_bt --csv data/SOLUSDT_1h_sample.csv

# Live paper trading (REST polling; safe)
python -m src.run_live --symbol SOL/USDT --exchange coindcx --tf 1h --paper

# Live paper trading (WebSocket, if ccxt.pro installed)
python -m src.run_live --symbol SOL/USDT --exchange coindcx --tf 1m --paper --ws
```

### Notes

* **Symbols**: `SOL/USDT` style works in `ccxt` for CoinDCX. Some pairs can differ; see `src/trade/symbols.py` helper.
* **Precision & lot size**: enforced via market metadata; orders are quantized.
* **Fees**: pulled from `market['taker']` when available; fallback to 0.1% (0.001) for backtests.

### Safety & Compliance

* Keep keys in `.env`; never commit them.
* Use small sizing; enable daily loss caps; model drift is real—retrain regularly.
* This is not financial advice.

## Project layout

```
src/
  config.py
  run_pipeline.py
  run_live.py
  utils/logger.py
  data/collector.py
  features/alpha.py
  strategies/signal_generator.py
  models/xgb_model.py
  backtest/backtest_bt.py
  live/infer.py
  trade/exchange.py
  trade/paper_broker.py
  trade/executor.py
  trade/precision.py
  trade/symbols.py
  risk/risk.py
scripts/
  make_sample.py
data/   (runtime)
models/ (runtime)
```
