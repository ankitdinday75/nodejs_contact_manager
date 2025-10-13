from __future__ import annotations

import argparse
from typing import Dict

import backtrader as bt
import pandas as pd


class PandasPred(bt.feeds.PandasData):
    lines = ("pred",)
    params = (
        ("datetime", None),
        ("open", "open"),
        ("high", "high"),
        ("low", "low"),
        ("close", "close"),
        ("volume", "volume"),
        ("openinterest", -1),
        ("pred", "pred"),
    )


class ProbSignalStrategy(bt.Strategy):
    params = dict(threshold=0.55, exit_threshold=0.45, sl_pct=0.01, tp_pct=0.02, risk_per_trade=0.01)

    def __init__(self) -> None:
        self.pred = self.datas[0].pred
        self.order = None

    def notify_order(self, order: bt.Order) -> None:
        if order.status in [order.Completed, order.Canceled, order.Rejected]:
            self.order = None

    def next(self) -> None:
        if self.order:
            return

        price = self.data.close[0]
        cash = self.broker.get_cash()

        if not self.position and self.pred[0] >= self.p.threshold:
            risk_cash = cash * self.p.risk_per_trade
            sl_dist = max(self.p.sl_pct, 1e-6)
            size = max(0.0, risk_cash / (price * sl_dist))
            if size <= 0:
                return
            self.order = self.buy_bracket(
                size=size,
                limitprice=price * (1 + self.p.tp_pct),
                stopprice=price * (1 - self.p.sl_pct),
            )
        elif self.position and self.pred[0] <= self.p.exit_threshold:
            self.order = self.close()


def run(
    csv: str,
    start_cash: float = 1000.0,
    threshold: float = 0.55,
    exit_threshold: float = 0.45,
    sl_pct: float = 0.01,
    tp_pct: float = 0.02,
    risk: float = 0.01,
    fee: float = 0.001,
) -> Dict[str, float]:
    df = pd.read_csv(csv, parse_dates=["ts"]).set_index("ts")
    if "pred" not in df.columns:
        df["pred"] = 0.5

    cerebro = bt.Cerebro()
    data = PandasPred(dataname=df)
    cerebro.adddata(data)
    cerebro.addstrategy(
        ProbSignalStrategy,
        threshold=threshold,
        exit_threshold=exit_threshold,
        sl_pct=sl_pct,
        tp_pct=tp_pct,
        risk_per_trade=risk,
    )
    cerebro.broker.setcash(start_cash)
    cerebro.broker.setcommission(commission=fee)
    cerebro.run()
    return {"final_value": float(cerebro.broker.getvalue())}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="CSV with columns ts,open,high,low,close,volume[,pred]")
    parser.add_argument("--cash", type=float, default=1000.0)
    args = parser.parse_args()
    result = run(args.csv, start_cash=args.cash)
    print(result)


if __name__ == "__main__":
    main()
