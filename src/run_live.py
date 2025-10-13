from __future__ import annotations

import argparse
import inspect
import time
from typing import Any, Dict

import pandas as pd

from .config import settings
from .live.infer import LiveInference
from .trade.exchange import get_exchange
from .trade.executor import Executor
from .trade.symbols import normalize_symbol
from .utils.logger import get_logger

log = get_logger("live")


def _fetch_last_n(ex, symbol: str, tf: str, n: int) -> pd.DataFrame:
    ohlcv = ex.fetch_ohlcv(symbol, timeframe=tf, limit=n)
    df = pd.DataFrame(ohlcv, columns=["ts", "open", "high", "low", "close", "volume"])
    df["ts"] = pd.to_datetime(df["ts"], unit="ms", utc=True)
    return df


async def _ws_loop(ex, symbol: str, tf: str, executor: Executor, infer: LiveInference) -> None:
    while True:
        try:
            ohlcv = await ex.watch_ohlcv(symbol, timeframe=tf)
            if not ohlcv:
                continue
            recent = ohlcv[-settings.feature_window :]
            df = pd.DataFrame(recent, columns=["ts", "open", "high", "low", "close", "volume"])
            df["ts"] = pd.to_datetime(df["ts"], unit="ms", utc=True)
            price = float(df["close"].iloc[-1])
            prob = infer.predict_proba(df)
            res = executor.place_signal(prob, price)
            equity = executor.broker.equity(price)
            log.info("[WS] price=%.4f prob=%.2f action=%s equity=%.2f", price, prob, res["status"], equity)
        except KeyboardInterrupt:
            break
        except Exception as exc:  # pragma: no cover - runtime safety
            log.error("WebSocket loop error: %s", exc)
            await ex.sleep(1)


def _maybe_close_exchange(ex) -> None:
    close_fn = getattr(ex, "close", None)
    if not close_fn:
        return
    if inspect.iscoroutinefunction(close_fn):  # pragma: no cover - async path
        import asyncio

        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.create_task(close_fn())
        else:
            loop.run_until_complete(close_fn())
    else:
        close_fn()


def _load_markets(ex, ws: bool) -> Dict[str, Any]:
    if ws and inspect.iscoroutinefunction(getattr(ex, "load_markets", None)):  # pragma: no cover - async path
        import asyncio

        loop = asyncio.get_event_loop()
        return loop.run_until_complete(ex.load_markets())
    return ex.load_markets()


def run(symbol: str, exchange: str, tf: str, paper: bool = True, ws: bool = False) -> None:
    symbol = normalize_symbol(symbol)
    ex = get_exchange(exchange, pro=ws)
    infer = LiveInference(settings.model_path)

    markets = _load_markets(ex, ws=ws)
    market = markets.get(symbol, {})
    executor = Executor(market=market, paper=paper)

    try:
        if ws and hasattr(ex, "watch_ohlcv"):
            import asyncio

            asyncio.get_event_loop().run_until_complete(_ws_loop(ex, symbol, tf, executor, infer))
            return

        while True:
            try:
                df = _fetch_last_n(ex, symbol, tf, max(settings.feature_window, 60))
                price = float(df["close"].iloc[-1])
                prob = infer.predict_proba(df)
                res = executor.place_signal(prob, price)
                equity = executor.broker.equity(price)
                log.info("[REST] price=%.4f prob=%.2f action=%s equity=%.2f", price, prob, res["status"], equity)
            except KeyboardInterrupt:
                break
            except Exception as exc:  # pragma: no cover - runtime safety
                log.error("REST loop error: %s", exc)
            time.sleep(5)
    finally:
        _maybe_close_exchange(ex)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", default="SOL/USDT")
    parser.add_argument("--exchange", default="coindcx")
    parser.add_argument("--tf", default="1h")
    parser.add_argument("--paper", action="store_true")
    parser.add_argument("--ws", action="store_true", help="Use ccxt.pro websocket if installed")
    args = parser.parse_args()
    run(args.symbol, args.exchange, args.tf, paper=args.paper, ws=args.ws)


if __name__ == "__main__":
    main()
