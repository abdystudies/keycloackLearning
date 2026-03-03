import { Routes } from '@angular/router';
import { Home } from './pages/home/home';
import { Profile } from './pages/profile/profile';
import { authGuard, userPlusGuard } from './core/auth.guard';
import { ListaSpesa } from './pages/lista-spesa/lista-spesa';
import { Plus } from './pages/plus/plus';

export const routes: Routes = [
    { path: '', component: Home },
    { path: 'profile', component: Profile, canActivate: [authGuard] },
    { path: 'spesa', component: ListaSpesa, canActivate: [authGuard] },
    { path: 'plus', component: Plus, canActivate:[userPlusGuard]},
    { path: '**', redirectTo: '' },
];
