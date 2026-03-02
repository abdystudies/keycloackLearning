from flask import Flask, request, jsonify, g
from flask_cors import CORS
from auth import require_auth

app = Flask(__name__)
CORS(app)

#niente db per ora (ve lo lascio come esercizio)
shopping_lists: dict[str, list] = {}

@app.route("/items", methods=["GET"])
@require_auth #eccolo qua il nostro nuovo decoratore
def get_items():
    username = g.user.get("preferred_username")
    items = shopping_lists.get(username, [])
    return jsonify({"items": items, "user": username})

@app.route("/items", methods=["POST"])
@require_auth #eccolo qua il nostro nuovo decoratore pt2
def add_item():
    username = g.user.get("preferred_username")
    data = request.get_json()
    item = data.get("item", "").strip()

    if not item:
        return jsonify({"error": "Item non può essere vuoto"}), 400

    if username not in shopping_lists:
        shopping_lists[username] = []

    shopping_lists[username].append(item)
    return jsonify({"message": "Aggiunto", "items": shopping_lists[username]}), 201

if __name__ == "__main__":
    app.run(debug=True)
