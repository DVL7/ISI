from flask import Blueprint, jsonify, request

from recommender.recommender import recommend, suggestion

recommender_bp = Blueprint("recommender", __name__)

@recommender_bp.route("/api/recommend")
def api_recommend():

    title = request.args.get("title", "").strip()
    if not title:
        return jsonify({"error": "podaj parametr ?title=..."}), 400
    
    n = request.args.get("top_n", type=int) if "top_n" in request.args else 5
    if n is None or not 1 <= n <= 10:
        return jsonify({"error": "top_n musi byc z zakresu 1-10"}), 400

    if "genre" not in request.args:
        genre = None
    else:
        genre = request.args.get("genre").strip()
        if genre == "": return jsonify({"error": "empty parameter"}), 400

    if (genre is None):
        recs = recommend(title, top_n=n)

        if recs is None:
            return jsonify({"error": "no matches found", "suggestions": suggestion(title)}), 404
        return jsonify({"title": title, "count": len(recs), "recommendations": recs})

    recs = recommend(title, top_n=n, genre=genre)

    if recs is None:
        return jsonify({"error": "no matches found", "suggestions": suggestion(title)}), 404
    return jsonify({"title": title, "count": len(recs), "recommendations": recs})

    
