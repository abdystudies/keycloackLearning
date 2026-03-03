from flask import Flask, request, jsonify
from flask_cors import CORS
from auth import require_auth, require_role
from databaseWrapper import DatabaseWrapper

app = Flask(__name__)
CORS(app)

db = DatabaseWrapper.from_env()
SHARED_LIST_OWNER = "__public__"

@app.route("/items", methods=["GET"])
@require_auth #eccolo qua il nostro nuovo decoratore
def get_items():
    try:
        items = db.get_user_items(SHARED_LIST_OWNER)
        return jsonify({"items": items, "scope": "public"})
    except Exception:
        return jsonify({"error": "Errore database nel caricamento"}), 500

@app.route("/items", methods=["POST"])
@require_auth #eccolo qua il nostro nuovo decoratore pt2
@require_role("user_plus") #solo chi ha il ruolo user_plus può aggiungere
def add_item():
    data = request.get_json(silent=True) or {}
    item = data.get("item", "").strip()

    if not item:
        return jsonify({"error": "Item non può essere vuoto"}), 400

    try:
        db.add_user_item(SHARED_LIST_OWNER, item)
        items = db.get_user_items(SHARED_LIST_OWNER)
        return jsonify({"message": "Aggiunto", "items": items}), 201
    except Exception:
        return jsonify({"error": "Errore database durante l'aggiunta"}), 500

@app.route("/items/<int:item_index>", methods=["DELETE"])
@require_auth
@require_role("user_plus") #solo chi ha il ruolo user_plus può eliminare
def delete_item(item_index: int):
    if item_index < 0:
        return jsonify({"error": "Indice elemento non valido"}), 404

    try:
        deleted = db.delete_user_item_by_index(SHARED_LIST_OWNER, item_index)
        if not deleted:
            return jsonify({"error": "Indice elemento non valido"}), 404

        items = db.get_user_items(SHARED_LIST_OWNER)
        return jsonify({"message": "Eliminato", "items": items}), 200
    except Exception:
        return jsonify({"error": "Errore database durante l'eliminazione"}), 500

if __name__ == "__main__":
    app.run(debug=True)
