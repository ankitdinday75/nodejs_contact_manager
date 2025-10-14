import { Routes } from '@angular/router';
import { DashboardComponent } from './pages/dashboard.component';
import { PositionsComponent } from './pages/positions.component';
import { SettingsComponent } from './pages/settings.component';

export const routes: Routes = [
  { path: '', component: DashboardComponent },
  { path: 'positions', component: PositionsComponent },
  { path: 'settings', component: SettingsComponent },
  { path: '**', redirectTo: '' }
];
