import math
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
    if ("max_price" not in request.args):
        return jsonify(PRODUCTS)

    raw_price = request.args.get("max_price")

    try:
        max_price = float(raw_price)
    except ValueError:
        return jsonify({"error": "max_price must be a number"}), 400
    
    if (max_price < 0 or not math.isfinite(max_price)):
        return jsonify({"error": "max_price out of scope"}), 400
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

@products_bp.route("/api/products", methods=["POST"])
def postProduct():
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not {"nazwa", "kategoria", "cena", "opis"} <= data.keys():
        return jsonify({"error": "expected JSON object with nazwa, kategoria, cena, opis"}), 400
    
    if "id" in data:
        return jsonify({"error": "id is assigned by the server"}), 400
    
    if any(not isinstance(data[key], str) or not data[key].strip() for key in ("nazwa", "kategoria", "opis")):
        return jsonify({"error": "text fields must be non-empty strings"}), 400
    
    price = data["cena"]
    
    if type(price) not in (int, float) or (type(price) is float and not math.isfinite(price)) or price < 0:
        return jsonify({"error": "cena must be a finite non-negative number"}), 400
    
    new_id = max((p["id"] for p in PRODUCTS), default=0) + 1

    product = {key: data[key] for key in ("nazwa", "kategoria", "cena", "opis")}

    product["id"] = new_id

    PRODUCTS.append(product)

    return jsonify(product), 201