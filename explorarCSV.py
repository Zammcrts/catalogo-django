import pandas as pd

df = pd.read_csv('spotify_songs.csv')
print(f"filas:{len(df)}")
print(f"track_id unicos:{len(df['track_id'].unique())}")

repetidas = df[df['track_id'].duplicated(keep=False)].sort_values("track_id")
print(repetidas[["track_id", "track_name", "playlist_name", "playlist_genre"]].head(10))

