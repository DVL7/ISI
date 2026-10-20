from flask import Flask, jsonify

from products.routes import products_bp
from recommender.routes import recommender_bp

app = Flask(__name__)
app.register_blueprint(products_bp)
app.register_blueprint(recommender_bp)

@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5001)
