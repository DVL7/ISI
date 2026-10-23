from flask import Blueprint, jsonify, request

products_bp = Blueprint("products", __name__)

# lab1
PRODUCTS = [
    {"id": 1, "nazwa": "Klawiatura mechaniczna", "kategoria": "akcesoria", "cena": 349.99, "opis": "Przełączniki hot-swap, podświetlenie RGB"},
    {"id": 2, "nazwa": "Mysz bezprzewodowa", "kategoria": "akcesoria", "cena": 129.00, "opis": "Ciche przyciski, 4000 DPI"},
    {"id": 3, "nazwa": "Monitor 27 cali", "kategoria": "monitory", "cena": 1099.00, "opis": "Matryca IPS, 144 Hz"},
    {"id": 4, "nazwa": "Słuchawki nauszne", "kategoria": "audio", "cena": 449.00, "opis": "ANC, 40 h pracy na baterii"},
    {"id": 5, "nazwa": "Hub USB-C", "kategoria": "akcesoria", "cena": 199.00, "opis": "HDMI, 3x USB-A, czytnik SD"},
]

@products_bp.route("/api/products")
def getProducts():
    max_price = request.args.get("max_price", type=float)

    if (max_price is None):
        return jsonify(PRODUCTS)
    else:
        filtred = []
        for i in PRODUCTS:
            if (i["cena"] <= max_price):
                filtred.append(i)
        return jsonify(filtred)
    

@products_bp.route("/api/products/<int:product_id>")
def getProductId(product_id):
    item = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if item is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(item)
