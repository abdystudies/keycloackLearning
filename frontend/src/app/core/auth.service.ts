import { Injectable, inject } from '@angular/core';
import Keycloak from 'keycloak-js';

@Injectable({ providedIn: 'root' })
export class AuthService {
    private keycloak = inject(Keycloak);
    login(): void {
        this.keycloak.login({ redirectUri: window.location.origin });
    }
    logout(): void {
        this.keycloak.logout({
            redirectUri: window.location.origin,
        });
    }
    //true se user ha completato login
    isLoggedIn(): boolean {
        return !!this.keycloak.authenticated;
    }
    getUsername(): string {
        return this.keycloak.tokenParsed?.['preferred_username'] ?? '';
    }
    //restituisce il token JWT
    //ci servirà x chiamate API autenticate/autorizzate
    getToken(): string | undefined {
            return this.keycloak.token;
        }
}