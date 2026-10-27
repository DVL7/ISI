import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

df = pd.read_csv(DATA_DIR / "ratings.csv")

matrix = df.pivot_table(index="user", columns="title", values="rating")
# 12 wierszy (osoby) x 24 kolumny (filmy), NaN = nieoceniony
print(matrix.shape)  # (12, 24)

means = matrix.mean(axis=1)                 # średnia każdej osoby
centered = matrix.sub(means, axis=0).fillna(0)

sim = pd.DataFrame(cosine_similarity(centered),
                   index=matrix.index, columns=matrix.index)
# cosine odchyleń; przy brakach nie jest Pearsonem na przecięciu

def recommend(user, top_n=5, k=3):
    if user not in matrix.index:
        return None
    neighbors = sim[user].drop(user).sort_values(ascending=False).head(k)
    scores = {}
    for movie in matrix.columns:
        if not pd.isna(matrix.loc[user, movie]):
            continue                      # już oceniony. nie polecamy
        num, den = 0.0, 0.0
        for other, w in neighbors.items():
            r = matrix.loc[other, movie]
            if not pd.isna(r):
                num += w * (r - means[other])
                den += abs(w)
        if den > 0:
            scores[movie] = max(1.0, min(5.0, means[user] + num / den))
    best = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return [{"title": t,
                "predicted": round(float(s), 2),
                "because": [o for o, weight in neighbors.items()
                            if weight != 0 and not pd.isna(matrix.loc[o, t])]
               } for t, s in best]