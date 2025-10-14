import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';

@Component({
  standalone: true,
  selector: 'app-settings',
  imports: [CommonModule],
  templateUrl: './settings.component.html'
})
export class SettingsComponent {
  env = {
    apiBase: 'http://localhost:3000/api',
    symbol: 'SOL/USDT',
    timeframe: '1h',
    thresholds: { enter: 0.55, exit: 0.45 }
  } as const;
}
