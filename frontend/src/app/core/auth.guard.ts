import { inject } from '@angular/core';
import { CanActivateFn, ActivatedRouteSnapshot, RouterStateSnapshot } from  '@angular/router';
import Keycloak from 'keycloak-js';
//angular lo esegue automaticamente prima di
//attivare qualsiasi rotta che ha canActivate: [authGuard]
//lo vedremo dopo nell'app.routes.ts
export const authGuard: CanActivateFn = (
    _route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
) => {
    const keycloak = inject(Keycloak);
    //se autenticato,carica il componente
    if (keycloak.authenticated) return true;
    //altrimenti manda al login
    keycloak.login({
        redirectUri: window.location.origin + state.url,
    });
    return false;
};