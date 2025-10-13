from __future__ import annotations


def volatility_target_size(equity: float, vol: float, target_vol: float = 0.2) -> float:
    if vol <= 0:
        return 0.0
    fraction = min(target_vol / vol, 1.0)
    return equity * fraction


def kelly_fraction(win_rate: float, win_loss_ratio: float) -> float:
    b = win_loss_ratio
    p = win_rate
    q = 1 - p
    if b <= 0:
        return 0.0
    f = (b * p - q) / b
    return max(0.0, min(f, 1.0))
