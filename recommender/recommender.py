import pandas as pd
from flask import request
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

df = pd.read_csv(DATA_DIR / "movies.csv")
df["overview"] = df["overview"].fillna("")

# czyszczenie danych
print(df.shape)           # (24, 4)
print(df.head(3))         # pierwsze wiersze
print(df.isnull().sum())  # braki w kolumnach

# zamiana tekstu na liczby
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(df["overview"])

print(tfidf_matrix.shape)  

sim_matrix = cosine_similarity(tfidf_matrix)

def suggestion(title, n=3):
    titles = {t.lower(): t for t in df["title"]}
    matches = get_close_matches(title.lower(), titles.keys(), n=n)
    return [titles[m] for m in matches]

def recommend(title, top_n=5, genre=None):
    match = df[df["title"].str.lower() == title.lower()]
    if match.empty:
        return None
    idx = match.index[0]
    scores = sorted(enumerate(sim_matrix[idx]), key=lambda x: x[1], reverse=True)
    if (genre is None):
        return [
            {"title": df["title"][i], "genres": df["genres"][i],
            "rating": round(float(df["rating"][i]), 1),
            "score": round(float(s), 3)}
            for i, s in scores if i != idx
        ][:top_n]
    else:
        return [
            {"title": df["title"][i], "genres": df["genres"][i],
            "rating": round(float(df["rating"][i]), 1),
            "score": round(float(s), 3)}
            for i, s in scores if i != idx and genre.lower() in df["genres"][i].split("|")
            ][:top_n]

if __name__ == "__main__": 
    print(recommend("Ania"))