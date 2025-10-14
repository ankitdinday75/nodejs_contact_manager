# Quant Trader UI (Angular) – Starter

A clean Angular **frontend** for a quant-trader backend. Includes:
- Angular 17 (standalone components)
- Tailwind CSS for styling
- ApexCharts for price & volume
- API service layer + **mock backend** (Express) to run locally without Python
- Ready to connect to your Python quant engine at `/api`

## Quickstart

```bash
# 1) Install deps
npm i

# 2) Run the mock backend (serves /api/*)
npm run mock

# 3) In a new terminal, start Angular dev server
npm start
# open http://localhost:4200
```

## Connect to your real backend
Edit `src/environments/environment.ts` and set `apiBase`.
Expected endpoints:

- `GET /api/metrics` → `{ equity, cash, posSize, lastPrice, dayPnL, winRate, sharpe }`
- `GET /api/trades?limit=50` → `Trade[]`
- `GET /api/positions` → `Position[]`
- `GET /api/signal` → `{ symbol, timeframe, proba, action, price, time }`
- `GET /api/candles?symbol=SOL/USDT&tf=1h&limit=200` → `[{t,o,h,l,c,v}]`
- `POST /api/orders` → `{side, symbol, size, price?}`

## Scripts
- `npm start` – Angular dev server
- `npm run mock` – Mock API on http://localhost:3000
- `npm run build` – Production build
- `npm run lint` – Lint

Safe defaults; no secrets. Style with Tailwind via `tailwind.config.js` and `src/styles.scss`.
