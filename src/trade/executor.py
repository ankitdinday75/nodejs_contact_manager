from __future__ import annotations

from ..config import settings
from ..trade.paper_broker import PaperBroker
from ..trade.precision import quantize_amount, quantize_price


class Executor:
    def __init__(self, market: dict | None, paper: bool = True) -> None:
        self.paper = paper
        self.market = market or {}
        self.broker = PaperBroker(settings.quote_balance)

    def _size_from_risk(self, price: float) -> float:
        risk_cash = settings.quote_balance * settings.risk_per_trade
        sl_dist = max(settings.sl_pct, 1e-6)
        size = risk_cash / (price * sl_dist) if price > 0 else 0.0
        return max(0.0, size)

    def place_signal(self, prob: float, price: float) -> dict:
        price_q = quantize_price(price, self.market)
        if prob >= settings.pred_threshold and self.broker.pos.size <= 0:
            size = self._size_from_risk(price_q)
            size_q = quantize_amount(size, self.market)
            if size_q <= 0:
                return {"status": "no_action"}
            return self.broker.buy(price_q, size_q)
        if prob <= settings.exit_threshold and self.broker.pos.size > 0:
            return self.broker.sell(price_q, self.broker.pos.size)
        return {"status": "no_action"}
