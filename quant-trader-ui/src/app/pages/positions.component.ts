import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';
import { Position, Trade } from '../services/api.models';

@Component({
  standalone: true,
  selector: 'app-positions',
  imports: [CommonModule],
  templateUrl: './positions.component.html'
})
export class PositionsComponent implements OnInit {
  positions: Position[] = [];
  trades: Trade[] = [];

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.api.positions().subscribe((p) => (this.positions = p));
    this.api.trades(100).subscribe((t) => (this.trades = t));
  }
}
