"""Command line runner for the Music Recommender Simulation."""

from __future__ import annotations

import argparse
from typing import Dict, Any

from tabulate import tabulate

from .recommender import load_songs, recommend_songs


def _build_profiles(selected_mode: str) -> Dict[str, Dict[str, Any]]:
    common = {
        "mode": selected_mode,
        "artist_penalty": 0.55,
        "genre_penalty": 0.25,
    }

    return {
        "High-Energy EDM Fan": {
            **common,
            "genre": "edm",
            "mood": "euphoric",
            "energy": 0.92,
            "tempo_bpm": 132,
            "valence": 0.74,
            "danceability": 0.88,
            "acousticness": 0.10,
            "popularity": 75,
            "release_decade": 2020,
            "mood_tags": ["festival", "night", "hype"],
        },
        "Chill Acoustic Listener": {
            **common,
            "genre": "acoustic",
            "mood": "calm",
            "energy": 0.28,
            "tempo_bpm": 78,
            "valence": 0.55,
            "danceability": 0.38,
            "acousticness": 0.88,
            "popularity": 58,
            "release_decade": 2010,
            "mood_tags": ["study", "sunset", "soft"],
        },
        "Hip-Hop Focus Profile": {
            **common,
            "genre": "hip-hop",
            "mood": "focused",
            "energy": 0.70,
            "tempo_bpm": 95,
            "valence": 0.52,
            "danceability": 0.82,
            "acousticness": 0.25,
            "popularity": 80,
            "release_decade": 2020,
            "mood_tags": ["flow", "grit", "focus"],
        },
    }


def _print_profile_recommendations(profile_name: str, profile: Dict[str, Any], songs: list[Dict[str, Any]]) -> None:
    recommendations = recommend_songs(profile, songs, k=5)
    table_rows = []

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        reasons = explanation.split("; ", 1)[-1]
        table_rows.append(
            [
                rank,
                song["title"],
                song["artist"],
                song["genre"],
                f"{score:.2f}",
                reasons,
            ]
        )

    print(f"\n=== {profile_name} | mode={profile.get('mode', 'balanced')} ===")
    print(
        tabulate(
            table_rows,
            headers=["#", "Song", "Artist", "Genre", "Score", "Why it ranked"],
            tablefmt="github",
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the music recommender simulation")
    parser.add_argument(
        "--mode",
        default="balanced",
        choices=["balanced", "genre_first", "mood_first", "energy_similarity"],
        help="Select ranking strategy mode",
    )
    args = parser.parse_args()

    songs = load_songs("data/songs.csv")
    profiles = _build_profiles(args.mode)

    print(f"Loaded songs: {len(songs)}")
    for name, profile in profiles.items():
        _print_profile_recommendations(name, profile, songs)
