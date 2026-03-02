from flask import Flask, request, jsonify, g
from flask_cors import CORS
from auth import require_auth
from databaseWrapper import DatabaseWrapper

app = Flask(__name__)
CORS(app)

db = DatabaseWrapper.from_env()

@app.route("/items", methods=["GET"])
@require_auth #eccolo qua il nostro nuovo decoratore
def get_items():
    username = g.user.get("preferred_username")
    try:
        items = db.get_user_items(username)
        return jsonify({"items": items, "user": username})
    except Exception:
        return jsonify({"error": "Errore database nel caricamento"}), 500

@app.route("/items", methods=["POST"])
@require_auth #eccolo qua il nostro nuovo decoratore pt2
def add_item():
    username = g.user.get("preferred_username")
    data = request.get_json(silent=True) or {}
    item = data.get("item", "").strip()

    if not item:
        return jsonify({"error": "Item non può essere vuoto"}), 400

    try:
        db.add_user_item(username, item)
        items = db.get_user_items(username)
        return jsonify({"message": "Aggiunto", "items": items}), 201
    except Exception:
        return jsonify({"error": "Errore database durante l'aggiunta"}), 500

@app.route("/items/<int:item_index>", methods=["DELETE"])
@require_auth
def delete_item(item_index: int):
    username = g.user.get("preferred_username")
    if item_index < 0:
        return jsonify({"error": "Indice elemento non valido"}), 404

    try:
        deleted = db.delete_user_item_by_index(username, item_index)
        if not deleted:
            return jsonify({"error": "Indice elemento non valido"}), 404

        items = db.get_user_items(username)
        return jsonify({"message": "Eliminato", "items": items}), 200
    except Exception:
        return jsonify({"error": "Errore database durante l'eliminazione"}), 500

if __name__ == "__main__":
    app.run(debug=True)
