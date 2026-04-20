from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    popularity: int = 50
    release_decade: int = 2010
    instrumentalness: float = 0.0
    loudness_db: float = -10.0
    liveness: float = 0.1
    mood_tags: str = ""

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    @staticmethod
    def _score_song_obj(user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        score = 0.0
        reasons: List[str] = []

        if song.genre.lower() == user.favorite_genre.lower():
            score += 2.5
            reasons.append("genre match (+2.50)")

        if song.mood.lower() == user.favorite_mood.lower():
            score += 2.0
            reasons.append("mood match (+2.00)")

        energy_gap = abs(song.energy - user.target_energy)
        energy_points = max(0.0, 2.0 - (energy_gap * 2.0))
        score += energy_points
        reasons.append(f"energy similarity (+{energy_points:.2f})")

        if user.likes_acoustic:
            acoustic_points = song.acousticness * 1.5
            score += acoustic_points
            reasons.append(f"acoustic preference (+{acoustic_points:.2f})")
        else:
            non_acoustic_points = (1.0 - song.acousticness) * 1.0
            score += non_acoustic_points
            reasons.append(f"modern/non-acoustic fit (+{non_acoustic_points:.2f})")

        return score, reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored: List[Tuple[Song, float]] = []
        for song in self.songs:
            score, _ = self._score_song_obj(user, song)
            scored.append((song, score))

        scored.sort(key=lambda item: item[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        score, reasons = self._score_song_obj(user, song)
        return f"score={score:.2f}; " + ", ".join(reasons)


NUMERIC_FIELDS = {
    "id": int,
    "energy": float,
    "tempo_bpm": float,
    "valence": float,
    "danceability": float,
    "acousticness": float,
    "popularity": int,
    "release_decade": int,
    "instrumentalness": float,
    "loudness_db": float,
    "liveness": float,
}


def _to_typed_song_dict(row: Dict[str, str]) -> Dict[str, Any]:
    typed: Dict[str, Any] = {}
    for key, value in row.items():
        converter = NUMERIC_FIELDS.get(key)
        if converter is None:
            typed[key] = value
        else:
            typed[key] = converter(value)
    return typed


def _closeness_score(value: float, target: float, weight: float) -> float:
    return max(0.0, weight - (abs(value - target) * weight))


def _closeness_bpm(value: float, target: float, weight: float) -> float:
    # Tempo ranges are wider than normalized values, so scale by 100 BPM.
    return max(0.0, weight - (abs(value - target) / 100.0 * weight))


def _score_with_mode(user_prefs: Dict[str, Any], song: Dict[str, Any], mode: str) -> Tuple[float, List[str]]:
    score = 0.0
    reasons: List[str] = []

    profile_genre = str(user_prefs.get("genre", "")).lower()
    profile_mood = str(user_prefs.get("mood", "")).lower()
    profile_energy = float(user_prefs.get("energy", 0.5))
    profile_tempo = float(user_prefs.get("tempo_bpm", 110.0))
    profile_valence = float(user_prefs.get("valence", 0.5))
    profile_dance = float(user_prefs.get("danceability", 0.5))
    profile_acoustic = float(user_prefs.get("acousticness", 0.5))
    profile_popularity = float(user_prefs.get("popularity", 60.0))
    profile_decade = int(user_prefs.get("release_decade", 2010))
    preferred_tags = [tag.strip().lower() for tag in user_prefs.get("mood_tags", [])]

    weights_by_mode: Dict[str, Dict[str, float]] = {
        "balanced": {
            "genre": 2.5,
            "mood": 2.0,
            "energy": 1.8,
            "tempo": 1.2,
            "valence": 1.0,
            "dance": 1.0,
        },
        "genre_first": {
            "genre": 3.6,
            "mood": 1.2,
            "energy": 1.2,
            "tempo": 0.8,
            "valence": 0.7,
            "dance": 0.8,
        },
        "mood_first": {
            "genre": 1.1,
            "mood": 3.4,
            "energy": 1.3,
            "tempo": 1.0,
            "valence": 1.4,
            "dance": 0.8,
        },
        "energy_similarity": {
            "genre": 1.0,
            "mood": 1.0,
            "energy": 3.6,
            "tempo": 1.6,
            "valence": 0.7,
            "dance": 0.8,
        },
    }

    weights = weights_by_mode.get(mode, weights_by_mode["balanced"])

    if str(song["genre"]).lower() == profile_genre:
        score += weights["genre"]
        reasons.append(f"genre match (+{weights['genre']:.2f})")

    if str(song["mood"]).lower() == profile_mood:
        score += weights["mood"]
        reasons.append(f"mood match (+{weights['mood']:.2f})")

    energy_points = _closeness_score(float(song["energy"]), profile_energy, weights["energy"])
    score += energy_points
    reasons.append(f"energy similarity (+{energy_points:.2f})")

    tempo_points = _closeness_bpm(float(song["tempo_bpm"]), profile_tempo, weights["tempo"])
    score += tempo_points
    reasons.append(f"tempo similarity (+{tempo_points:.2f})")

    valence_points = _closeness_score(float(song["valence"]), profile_valence, weights["valence"])
    score += valence_points
    reasons.append(f"valence similarity (+{valence_points:.2f})")

    dance_points = _closeness_score(float(song["danceability"]), profile_dance, weights["dance"])
    score += dance_points
    reasons.append(f"danceability similarity (+{dance_points:.2f})")

    acoustic_points = _closeness_score(float(song.get("acousticness", 0.5)), profile_acoustic, 0.8)
    score += acoustic_points
    reasons.append(f"acousticness similarity (+{acoustic_points:.2f})")

    popularity_points = max(0.0, 0.6 - (abs(float(song.get("popularity", 60)) - profile_popularity) / 100.0 * 0.6))
    score += popularity_points
    reasons.append(f"popularity proximity (+{popularity_points:.2f})")

    decade_gap = abs(int(song.get("release_decade", 2010)) - profile_decade)
    decade_points = max(0.0, 0.6 - (decade_gap / 40.0 * 0.6))
    score += decade_points
    reasons.append(f"era proximity (+{decade_points:.2f})")

    if preferred_tags:
        song_tags = [tag.strip().lower() for tag in str(song.get("mood_tags", "")).split("|") if tag.strip()]
        matched_tags = sorted(set(preferred_tags).intersection(song_tags))
        tag_points = min(0.9, len(matched_tags) * 0.3)
        if tag_points > 0:
            score += tag_points
            reasons.append(f"tag match {matched_tags} (+{tag_points:.2f})")

    return score, reasons

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict[str, Any]] = []
    with open(csv_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            songs.append(_to_typed_song_dict(row))
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    mode = str(user_prefs.get("mode", "balanced"))
    return _score_with_mode(user_prefs, song, mode)


def _format_explanation(score: float, reasons: List[str]) -> str:
    return f"final={score:.2f}; " + ", ".join(reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    mode = str(user_prefs.get("mode", "balanced"))
    artist_penalty = float(user_prefs.get("artist_penalty", 0.55))
    genre_penalty = float(user_prefs.get("genre_penalty", 0.25))

    base_scored: List[Tuple[Dict[str, Any], float, List[str]]] = []
    for song in songs:
        base_score, reasons = _score_with_mode(user_prefs, song, mode)
        base_scored.append((song, base_score, reasons))

    # Start from best base scores, then apply diversity/fairness penalties during selection.
    base_scored.sort(key=lambda item: item[1], reverse=True)

    recommendations: List[Tuple[Dict[str, Any], float, str]] = []
    selected_artists: Dict[str, int] = {}
    selected_genres: Dict[str, int] = {}
    remaining = base_scored.copy()

    while remaining and len(recommendations) < k:
        best_idx = 0
        best_adjusted = float("-inf")

        for idx, (song, base_score, _) in enumerate(remaining):
            artist = str(song["artist"])
            genre = str(song["genre"])
            adjusted = base_score
            adjusted -= selected_artists.get(artist, 0) * artist_penalty
            adjusted -= selected_genres.get(genre, 0) * genre_penalty
            if adjusted > best_adjusted:
                best_adjusted = adjusted
                best_idx = idx

        song, base_score, reasons = remaining.pop(best_idx)
        artist = str(song["artist"])
        genre = str(song["genre"])

        artist_repeat_count = selected_artists.get(artist, 0)
        genre_repeat_count = selected_genres.get(genre, 0)
        if artist_repeat_count > 0:
            reasons = reasons + [f"artist diversity penalty (-{artist_penalty * artist_repeat_count:.2f})"]
        if genre_repeat_count > 0:
            reasons = reasons + [f"genre diversity penalty (-{genre_penalty * genre_repeat_count:.2f})"]

        selected_artists[artist] = artist_repeat_count + 1
        selected_genres[genre] = genre_repeat_count + 1

        explanation = _format_explanation(best_adjusted, reasons)
        recommendations.append((song, best_adjusted, explanation))

    return recommendations
