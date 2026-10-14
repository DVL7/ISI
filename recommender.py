import pandas as pd 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("movies.csv")
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

def recommend(title, top_n=5):
    match = df[df["title"].str.lower() == title.lower()]
    if match.empty:
        return None
    idx = match.index[0]
    scores = sorted(enumerate(sim_matrix[idx]), key=lambda x: x[1], reverse=True)
    return [
        {"title": df["title"][i], "genres": df["genres"][i],
         "rating": round(float(df["rating"][i]), 1),
         "score": round(float(s), 3)}
        for i, s in scores if i != idx
    ][:top_n]