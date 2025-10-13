from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Position:
    size: float = 0.0
    entry: float = 0.0


class PaperBroker:
    def __init__(self, quote_balance: float = 1000.0) -> None:
        self.cash = quote_balance
        self.pos = Position()

    def buy(self, price: float, size: float) -> dict:
        if size <= 0:
            return {"status": "rejected", "reason": "non_positive_size"}
        cost = price * size
        if cost > self.cash and price > 0:
            size = self.cash / price
            cost = price * size
        if size <= 0:
            return {"status": "rejected", "reason": "insufficient_cash"}
        self.cash -= cost
        if self.pos.size <= 0:
            self.pos.entry = price
        else:
            total_size = self.pos.size + size
            self.pos.entry = (self.pos.entry * self.pos.size + price * size) / total_size
        self.pos.size += size
        return {"status": "filled", "side": "buy", "size": size, "price": price}

    def sell(self, price: float, size: float) -> dict:
        if self.pos.size <= 0:
            return {"status": "rejected", "reason": "no_position"}
        size = min(size, self.pos.size)
        proceeds = price * size
        self.cash += proceeds
        self.pos.size -= size
        if self.pos.size <= 0:
            self.pos.entry = 0.0
        return {"status": "filled", "side": "sell", "size": size, "price": price}

    def equity(self, last_price: float) -> float:
        return self.cash + self.pos.size * last_price
