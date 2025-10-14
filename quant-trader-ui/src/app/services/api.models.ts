export interface Metrics {
  equity: number;
  cash: number;
  posSize: number;
  lastPrice: number;
  dayPnL: number;
  winRate: number;
  sharpe: number;
}

export interface Trade {
  id: string;
  time: string;
  symbol: string;
  side: 'buy' | 'sell';
  size: number;
  price: number;
  pnl?: number;
}

export interface Position {
  symbol: string;
  size: number;
  entry: number;
  pnl: number;
}

export interface Signal {
  symbol: string;
  timeframe: string;
  proba: number;
  action: string;
  price: number;
  time: string;
}

export interface Candle {
  t: number;
  o: number;
  h: number;
  l: number;
  c: number;
  v: number;
}
