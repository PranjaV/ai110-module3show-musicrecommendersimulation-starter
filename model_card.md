# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

This model recommends top songs from a small catalog by matching a user's musical taste profile to song attributes. It is intended for classroom exploration of recommendation logic and explainability, not for production personalization.

The model assumes a user can be described with stable preferences such as genre, mood, energy, tempo, and related audio-style targets.

---

## 3. How the Model Works

The model uses content-based scoring.

1. It reads structured song features from `songs.csv`.
2. It compares each song against a user profile.
3. It adds points for exact matches (genre, mood) and similarity points for numeric features (energy, tempo, valence, danceability, acousticness, popularity, release decade).
4. It adds bonuses when detailed mood tags overlap.
5. It ranks songs by score and applies diversity penalties to reduce repeated artist/genre in top results.

The system supports multiple ranking strategies (`balanced`, `genre_first`, `mood_first`, `energy_similarity`) and always returns reasons explaining each recommendation.

---

## 4. Data

- Catalog size: **22 songs**.
- Core attributes: `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`.
- Added attributes: `popularity`, `release_decade`, `instrumentalness`, `loudness_db`, `liveness`, `mood_tags`.

Genres represented include pop, indie pop, synthpop, rock, jazz, lofi, ambient, acoustic, folk, hip-hop, synthwave, electronic, and edm. Moods include happy, chill, intense, calm, focused, relaxed, moody, euphoric, and melancholic.

Missing aspects: lyrics meaning, cultural context, language preference, and long-term listening behavior.

---

## 5. Strengths

- Transparent: each recommendation includes specific scoring reasons.
- Responsive to user intent: profile changes produce clearly different outputs.
- Flexible ranking: mode switching changes behavior in predictable ways.
- Better variety than naive ranking due to diversity penalties.

In testing, EDM, acoustic/calm, and hip-hop/focus profiles each produced distinct top results that matched expected musical intuition.

---

## 6. Limitations and Bias

1. **Small dataset bias**: with only 22 songs, recommendations can become repetitive.
2. **Feature bias**: the system overweights whichever features are given higher point budgets.
3. **Manual tag bias**: mood tags are hand-authored and subjective.
4. **No collaborative signal**: it cannot learn from similar users, only from fixed content attributes.

Potential filter bubble: if genre weight is too high (for example in `genre_first`), the recommender can ignore diverse but still relevant songs.

Fairness mitigation implemented: artist and genre diversity penalties in final top-k selection.

---

## 7. Evaluation

Profiles tested:

- High-Energy EDM Fan
- Chill Acoustic Listener
- Hip-Hop Focus Profile

What was evaluated:

- Whether top songs matched profile goals.
- Whether explanations reflected actual scoring components.
- Whether diversity penalties reduced repetition.
- How outputs changed under different ranking modes.

Observed behavior:

- EDM profile preferred high-energy/high-BPM tracks with hype/festival tags.
- Acoustic profile shifted to low-energy/high-acousticness songs.
- Hip-hop profile emphasized danceability and focus tags.

All starter tests in `tests/test_recommender.py` pass.

---

## 8. Future Work

1. Add lightweight collaborative filtering signals (for example, synthetic play/skip history).
2. Use learned embeddings rather than only hand-picked scalar features.
3. Add novelty controls (recently heard penalty) and long-term fairness metrics.
4. Expand dataset to hundreds/thousands of songs for more realistic ranking behavior.

---

## 9. Personal Reflection

This project showed that recommendation systems are mostly about feature engineering and ranking design choices. Even simple weighted rules can produce useful personalization when the features are meaningful.

The most interesting discovery was how easy it is to create accidental bias. Small changes in feature weights can dominate outcomes and narrow variety. Adding explainability and diversity logic made the system easier to trust and debug.
