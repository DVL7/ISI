from flask import Flask, jsonify, request
from recommender import recommend

app = Flask(__name__)

# lab1
PRODUCTS = [
    {"id": 1, "nazwa": "Klawiatura mechaniczna", "kategoria": "akcesoria", "cena": 349.99, "opis": "Przełączniki hot-swap, podświetlenie RGB"},
    {"id": 2, "nazwa": "Mysz bezprzewodowa", "kategoria": "akcesoria", "cena": 129.00, "opis": "Ciche przyciski, 4000 DPI"},
    {"id": 3, "nazwa": "Monitor 27 cali", "kategoria": "monitory", "cena": 1099.00, "opis": "Matryca IPS, 144 Hz"},
    {"id": 4, "nazwa": "Słuchawki nauszne", "kategoria": "audio", "cena": 449.00, "opis": "ANC, 40 h pracy na baterii"},
    {"id": 5, "nazwa": "Hub USB-C", "kategoria": "akcesoria", "cena": 199.00, "opis": "HDMI, 3x USB-A, czytnik SD"},
]

@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/api/products")
def getProducts():
    return jsonify(PRODUCTS)

@app.route("/api/products/<int:product_id>")
def getProductId(product_id):
    item = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if item is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(item)

# lab2
@app.route("/api/recommend")
def api_recommend():
    title = request.args.get("title", "").strip()
    if not title:
        return jsonify({"error": "podaj parametr ?title=..."}), 400
    n = request.args.get("top_n", type=int) if "top_n" in request.args else 5
    if n is None or not 1 <= n <= 10:
        return jsonify({"error": "top_n musi byc z zakresu 1-10"}), 400
    recs = recommend(title, top_n=n)
    if recs is None:
        return jsonify({"error": "nie znam takiego filmu"}), 404
    return jsonify({"title": title, "count": len(recs), "recommendations": recs})


if __name__ == "__main__":
    app.run(debug=True, port=5001)