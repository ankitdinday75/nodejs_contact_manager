from __future__ import annotations

import math
from typing import Dict


def quantize_price(price: float, market: Dict) -> float:
    precision = market.get("precision", {}).get("price")
    if precision is None:
        step = (market.get("limits", {}).get("price", {}) or {}).get("min")
        if step:
            return math.floor(price / step) * step
        return float(price)
    factor = 10 ** precision
    return math.floor(price * factor) / factor


def quantize_amount(amount: float, market: Dict) -> float:
    precision = market.get("precision", {}).get("amount")
    if precision is None:
        step = (market.get("limits", {}).get("amount", {}) or {}).get("min")
        if step:
            return math.floor(amount / step) * step
        return float(amount)
    factor = 10 ** precision
    return math.floor(amount * factor) / factor
