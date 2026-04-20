# Reflection: Music Recommender Simulation

## Biggest Learning Moment

My biggest learning moment was realizing that recommendation quality depends less on complicated code and more on feature design and weight choices. A simple scoring model can feel very accurate when the features represent the listener's vibe (genre, mood, energy, tempo), but it can also fail quickly when one feature dominates too much.

## How AI Tools Helped (and Where I Double-Checked)

AI tools helped me iterate quickly on scoring strategies, profile design, and output formatting. I still needed to verify every suggestion by running the program with multiple profiles and checking whether the ranking reasons matched the math. The most important double-check was making sure explanations were tied directly to scored features rather than generic text.

## Pairwise Profile Comparisons

1. High-Energy EDM Fan vs Chill Acoustic Listener
   - EDM profile consistently ranked high-energy, high-BPM songs near the top (Festival Circuit, Runway Heat).
   - Acoustic profile shifted toward low-energy, high-acousticness tracks (Golden Hour Strings, Sunday Vinyl).
   - This difference makes sense because the target energy and acousticness preferences point in opposite directions.

2. High-Energy EDM Fan vs Hip-Hop Focus Profile
   - EDM profile prioritized euphoric/night/festival songs and very high tempo.
   - Hip-Hop profile prioritized focused rhythmic tracks with strong danceability and moderate tempo (Concrete Verse, Basement Cipher).
   - Both profiles can like energetic songs, but their genre and mood targets split final rankings.

3. Chill Acoustic Listener vs Hip-Hop Focus Profile
   - Acoustic profile favored calm and relaxed tracks with high acousticness.
   - Hip-Hop profile favored stronger rhythmic intensity and focus tags.
   - The overlap was minimal, which indicates the model is actually sensitive to user taste differences instead of returning static recommendations.

## What Surprised Me

What surprised me most was how "intelligent" recommendations can feel even from a small weighted system. The illusion of intelligence comes from strong alignment between user attributes and song attributes, not from complexity alone.

## What I Would Try Next

If I extend this project, I would add user listening history over time (recency and skip behavior), then blend that with content features. I would also add stronger novelty controls so the top list is both relevant and less repetitive across repeated runs.
