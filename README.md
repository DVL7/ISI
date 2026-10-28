# ISI

**Dawid Deryło, 131422**

Serwis REST we Flasku z trzema częściami:

- **Lab 1 — `product-service`**: katalog produktów w pamięci (GET, filtr ceny, GET po id, POST z walidacją).
- **Lab 2 — content-based**: rekomendacje filmów podobnych po opisie (TF-IDF + podobieństwo cosinusowe).
- **Lab 3 — collaborative filtering**: rekomendacje dla użytkownika na podstawie ocen podobnych osób (centrowanie ocen, cosinus między osobami, k sąsiadów).

## Jak to działa

### Lab 2 — TF-IDF
1. Wczytuje `data/movies.csv` (24 filmy) i zamienia opisy na wektory TF-IDF (bez angielskich stop words), co daje macierz 24 × 237.
2. Liczy `cosine_similarity` dla wszystkich par filmów, co daje macierz 24 × 24.
3. Dla podanego tytułu sortuje podobieństwa malejąco, pomija sam film i zwraca `top_n` wyników. Opcjonalnie filtruje po gatunku.
4. Przy literówce zwraca 404 z podpowiedziami (`difflib.get_close_matches`).

### Lab 3 — collaborative filtering
1. Wczytuje `data/ratings.csv` (182 oceny, 12 osób, 24 filmy) i buduje macierz osoby × filmy (`pivot_table`, brak oceny = NaN).
2. Centruje oceny: od każdej oceny odejmuje średnią danej osoby, a braki zamienia na 0.
3. Liczy podobieństwo cosinusowe między osobami i bierze `k` najbardziej podobnych sąsiadów.
4. Dla każdego nieocenionego filmu przewiduje ocenę:
   `predicted = średnia(u) + Σ sim(u,v)·(ocena(v) − średnia(v)) / Σ|sim(u,v)|`
   Sumy obejmują tylko sąsiadów, którzy ocenili film. Wynik jest przycinany do skali 1–5.
5. Pole `because` to lista sąsiadów (z niezerową wagą), którzy ocenili dany film.

Kod CF jest w `recommender/rating.py`, a kod TF-IDF w `recommender/recommender.py`.

## Uruchomienie

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Aplikacja działa na **http://127.0.0.1:5001** (port 5001, bo na macOS port 5000 zajmuje AirPlay). Formularz do rekomendacji po tytule jest pod `/`.

## Endpointy

| Metoda | Adres | Parametry | Opis |
| --- | --- | --- | --- |
| GET | `/api/health` | — | `{"status": "ok"}` |
| GET | `/api/products` | `?max_price=` (opcjonalnie) | lista produktów; zły `max_price` → 400 |
| GET | `/api/products/<id>` | — | produkt albo 404 |
| POST | `/api/products` | JSON: `nazwa`, `kategoria`, `cena`, `opis` | dodaje produkt → 201; złe dane → 400 |
| GET | `/api/recommend` | `?title=`, `?top_n=` (1–10, domyślnie 5), `?genre=` | lab 2: filmy podobne po opisie |
| GET | `/api/recommend` | `?user=`, `?k=` (1–11, domyślnie 3) | lab 3: rekomendacje dla użytkownika |
| GET | `/api/users` | — | lista 12 znanych użytkowników |

Kody błędów dla `/api/recommend`:
- brak parametru → 400;
- zły `top_n` albo `k` → 400;
- nieznany tytuł → 404 z `suggestions`;
- nieznany użytkownik → 404 z `known_users`.

## Przykładowe odpowiedzi

`GET /api/recommend?user=Ania`

```json
{
  "count": 5,
  "recommendations": [
    {"because": ["Celina", "Jacek", "Kasia"], "predicted": 4.31, "title": "Fight Club"},
    {"because": ["Celina"], "predicted": 3.08, "title": "Forrest Gump"},
    {"because": ["Celina", "Jacek", "Kasia"], "predicted": 2.37, "title": "Toy Story"},
    {"because": ["Kasia"], "predicted": 2.24, "title": "The Shawshank Redemption"},
    {"because": ["Celina", "Jacek", "Kasia"], "predicted": 2.13, "title": "Spirited Away"}
  ],
  "user": "Ania"
}
```

`GET /api/recommend?title=Inception&top_n=3`

```json
{
  "count": 3,
  "recommendations": [
    {"genres": "sci-fi|mystery", "rating": 8.0, "score": 0.091, "title": "Blade Runner 2049"},
    {"genres": "action|crime", "rating": 9.0, "score": 0.063, "title": "The Dark Knight"},
    {"genres": "horror|thriller", "rating": 8.4, "score": 0.059, "title": "The Shining"}
  ],
  "title": "Inception"
}
```

`GET /api/recommend?user=Zzz` → **404**

```json
{"error": "nie znam takiego uzytkownika", "known_users": ["Ania", "Bartek", "..."]}
```