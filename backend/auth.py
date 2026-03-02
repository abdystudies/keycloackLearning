from flask import request, jsonify, g
from functools import wraps
import jwt
import requests

#queti ovviamente li ho messi qua
#per comodità, ma sapete dove vanno :)
KEYCLOAK_URL = "https://3cfkbzcd-8080.euw.devtunnels.ms"
REALM        = "prova"
CLIENT_ID    = "provapp"
JWKS_URL     = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/certs"


#scarica la chiave pubblica di Keycloak
#per verificare che il JWT non sia stato alterato
def get_keycloak_public_key(token: str):
    #1)legge l'header del token SENZA verificarne la firma
    #serve solo per leggere il campo 'kid' (key ID)
    #un identificatore che dice quale chiave pubblica usare
    unverified_header = jwt.get_unverified_header(token)
    kid = unverified_header.get("kid")

    #2)scarica tutte le chiavi pubbliche attive dal realm di Keycloak.
    #Keycloak le ruota periodicamente, quindi possono essercene più di una.
    response = requests.get(JWKS_URL)
    jwks = response.json()

    #3)trova la chiave con il kid corrispondente a quello del token
    #e la converte dal formato JWKS a un oggetto RSA utilizzabile da PyJWT.
    for key_data in jwks["keys"]:
        if key_data["kid"] == kid:
            return jwt.algorithms.RSAAlgorithm.from_jwk(key_data)

    raise Exception("Chiave pubblica non trovata")

#creiamo un nuovo decoratore
#@require_auth lo usiamo dopo nell'app.py
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        #legge l'header Authorization dalla richiesta HTTP.
        #Angular lo manda così: "Authorization: Bearer <token>"
        auth_header = request.headers.get("Authorization", "")

        #se l'header manca o non inizia con "Bearer " blocca subito con 401.
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token mancante"}), 401

        #rimuove "Bearer " e tiene solo il token grezzo.
        token = auth_header.split(" ")[1]

        try:
            #ottiene la chiave pubblica giusta per questo token.
            public_key = get_keycloak_public_key(token)

            #verifica e decodifica il token
            payload = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                audience=CLIENT_ID,
                options={"verify_exp": True},
            )

            #salva il payload decodificato in g.user.
            #g è un oggetto Flask locale alla richiesta corrente
            #ogni richiesta ha il suo g, non condiviso con altre
            #le route protette leggono g.user per sapere chi è l'utente.
            g.user = payload

        #gestione degli errori
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token scaduto"}), 401
        except jwt.InvalidTokenError as e:
            return jsonify({"error": f"Token non valido: {str(e)}"}), 401
        except Exception as e:
            return jsonify({"error": str(e)}), 401

        #token valido, esegue la route originale.
        #da qui in poi la route può usare g.user liberamente.
        return f(*args, **kwargs)

    return decorated