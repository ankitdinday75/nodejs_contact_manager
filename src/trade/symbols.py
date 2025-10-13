from __future__ import annotations


def normalize_symbol(symbol: str) -> str:
    """
    Adjust symbols if the exchange uses alternate naming conventions.
    For CoinDCX via ccxt, 'SOL/USDT' typically works out of the box.
    """
    return symbol
