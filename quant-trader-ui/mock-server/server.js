const express = require('express');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

const PORT = 3000;
const SYMBOL = 'SOL/USDT';

function nowISO() {
  return new Date().toISOString();
}

let equity = 1000;
let cash = 1000;
let posSize = 0;
let lastPrice = 150;

app.get('/api/metrics', (_req, res) => {
  res.json({
    equity: equity + (Math.random() - 0.5) * 5,
    cash,
    posSize,
    lastPrice,
    dayPnL: +(Math.random() * 2 - 1).toFixed(2),
    winRate: Math.floor(40 + Math.random() * 30),
    sharpe: +(0.5 + Math.random() * 1.5).toFixed(2)
  });
});

app.get('/api/signal', (_req, res) => {
  const proba = +(0.45 + Math.random() * 0.2).toFixed(2);
  const action = proba >= 0.55 ? 'BUY' : proba <= 0.45 ? 'SELL' : 'HOLD';
  lastPrice = +(lastPrice * (1 + (Math.random() - 0.5) / 500)).toFixed(3);
  res.json({ symbol: SYMBOL, timeframe: '1h', proba, action, price: lastPrice, time: nowISO() });
});

const trades = [];
app.get('/api/trades', (req, res) => {
  const limit = Number.parseInt(req.query.limit, 10) || 100;
  res.json(trades.slice(-limit).reverse());
});

app.post('/api/orders', (req, res) => {
  const { side, symbol, size, price } = req.body || {};
  const px = price || lastPrice;
  const trade = {
    id: String(Date.now()),
    time: nowISO(),
    symbol: symbol || SYMBOL,
    side,
    size,
    price: px,
    pnl: 0
  };
  trades.push(trade);

  if (side === 'buy') {
    posSize += size;
    cash -= size * px;
  } else if (side === 'sell') {
    posSize = Math.max(0, posSize - size);
    cash += size * px;
  }
  equity = cash + posSize * px;

  res.json({ status: 'ok', trade });
});

app.get('/api/positions', (_req, res) => {
  res.json([
    {
      symbol: SYMBOL,
      size: posSize,
      entry: lastPrice,
      pnl: +(posSize * 0.01).toFixed(2)
    }
  ]);
});

app.get('/api/candles', (req, res) => {
  const limit = Math.min(Number.parseInt(req.query.limit, 10) || 200, 2000);
  const out = [];
  let t = Date.now() - limit * 60 * 60 * 1000;
  let base = lastPrice;

  for (let i = 0; i < limit; i += 1) {
    const step = (Math.random() - 0.5) * 1.2;
    const close = +(base + i * 0.05 + step).toFixed(3);
    const open = +(close + (Math.random() - 0.5) * 0.3).toFixed(3);
    const high = +(Math.max(open, close) + Math.random() * 0.4).toFixed(3);
    const low = +(Math.min(open, close) - Math.random() * 0.4).toFixed(3);
    const volume = Math.floor(100 + Math.random() * 200);
    out.push({ t, o: open, h: high, l: low, c: close, v: volume });
    t += 60 * 60 * 1000;
    base = close;
  }

  res.json(out);
});

app.listen(PORT, () => {
  console.log(`Mock API running at http://localhost:${PORT}`);
});
