import { CommonModule } from '@angular/common';
import { Component, OnDestroy, OnInit, computed, signal } from '@angular/core';
import { NgApexchartsModule } from 'ng-apexcharts';
import { ApiService } from '../services/api.service';

@Component({
  standalone: true,
  selector: 'app-dashboard',
  imports: [CommonModule, NgApexchartsModule],
  templateUrl: './dashboard.component.html'
})
export class DashboardComponent implements OnInit, OnDestroy {
  private refreshTimer: ReturnType<typeof setInterval> | null = null;

  loading = signal(true);
  metrics = signal<any>(null);
  signalInfo = signal<any>(null);
  priceSeries = signal<{ x: number; y: number }[]>([]);
  volumeSeries = signal<{ x: number; y: number }[]>([]);

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.refresh();
    this.refreshTimer = setInterval(() => this.refreshLite(), 5000);
  }

  ngOnDestroy(): void {
    if (this.refreshTimer) {
      clearInterval(this.refreshTimer);
    }
  }

  refresh(): void {
    this.loading.set(true);
    this.api.metrics().subscribe((m) => this.metrics.set(m));
    this.api.signal().subscribe((s) => this.signalInfo.set(s));
    this.api.candles().subscribe((c) => {
      this.priceSeries.set(c.map((k) => ({ x: k.t, y: k.c })));
      this.volumeSeries.set(c.map((k) => ({ x: k.t, y: k.v })));
      this.loading.set(false);
    });
  }

  refreshLite(): void {
    this.api.metrics().subscribe((m) => this.metrics.set(m));
    this.api.signal().subscribe((s) => this.signalInfo.set(s));
  }

  priceChart = computed(() => ({
    chart: { type: 'line', height: 300, animations: { enabled: true } },
    series: [{ name: 'Close', data: this.priceSeries() }],
    xaxis: { type: 'datetime' as const },
    yaxis: { decimalsInFloat: 2 }
  }));

  volumeChart = computed(() => ({
    chart: { type: 'bar', height: 120, animations: { enabled: true } },
    series: [{ name: 'Volume', data: this.volumeSeries() }],
    xaxis: { type: 'datetime' as const, labels: { show: false } },
    yaxis: { labels: { show: false } }
  }));
}
