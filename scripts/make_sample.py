from __future__ import annotations

import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


def main() -> None:
    os.makedirs("data", exist_ok=True)
    np.random.seed(42)

    num_rows = 300
    base_price = 150.0
    steps = np.random.normal(0, 0.5, size=num_rows).cumsum()
    close = base_price + steps
    open_price = close + np.random.normal(0, 0.2, size=num_rows)
    high = np.maximum(open_price, close) + np.random.rand(num_rows) * 0.3
    low = np.minimum(open_price, close) - np.random.rand(num_rows) * 0.3
    volume = np.random.randint(100, 300, size=num_rows)

    timestamps = [datetime.utcnow() - timedelta(hours=num_rows - i) for i in range(num_rows)]
    df = pd.DataFrame(
        {
            "ts": timestamps,
            "open": open_price,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume,
        }
    )
    path = "data/SOLUSDT_1h_sample.csv"
    df.to_csv(path, index=False)
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
