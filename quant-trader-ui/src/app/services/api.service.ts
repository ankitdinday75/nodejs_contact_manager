import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Candle, Metrics, Position, Signal, Trade } from './api.models';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private http = inject(HttpClient);
  private base = environment.apiBase;

  metrics() {
    return this.http.get<Metrics>(`${this.base}/metrics`);
  }

  trades(limit = 50) {
    return this.http.get<Trade[]>(`${this.base}/trades?limit=${limit}`);
  }

  positions() {
    return this.http.get<Position[]>(`${this.base}/positions`);
  }

  signal() {
    return this.http.get<Signal>(`${this.base}/signal`);
  }

  candles(symbol = 'SOL/USDT', tf = '1h', limit = 200) {
    const params = new URLSearchParams({
      symbol,
      tf,
      limit: String(limit)
    });
    return this.http.get<Candle[]>(`${this.base}/candles?${params.toString()}`);
  }

  order(body: { side: 'buy' | 'sell'; symbol: string; size: number; price?: number }) {
    return this.http.post(`${this.base}/orders`, body);
  }
}
