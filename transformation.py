import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from utils import read_avro, save_to_csv


def calculate_newness_score(df_tracks):
    mask = df_tracks['release_date'].astype(str).apply(len) == 4
    df_tracks.loc[mask, 'months_elapsed'] = (2024 - pd.to_numeric(
        df_tracks.loc[mask, 'release_date']) + 1) * 12
    reference_date = pd.to_datetime('2024-01-01')

    try:
        months_elapsed, _ = divmod((reference_date - pd.to_datetime(
            df_tracks.loc[~mask, 'release_date'], errors='coerce')).dt.days, 30)
        df_tracks.loc[~mask, 'months_elapsed'] = months_elapsed.fillna(0)
    except ValueError as e:
        print(f"Error: {e}")
        print("Problematic values:")
        print(df_tracks.loc[~mask, 'release_date'])
        df_tracks.loc[~mask, 'months_elapsed'] = np.nan

    df_tracks['newness_score'] = 1 - (df_tracks['months_elapsed'] - df_tracks['months_elapsed'].min()) / (
        df_tracks['months_elapsed'].max() - df_tracks['months_elapsed'].min())
    df_tracks['newness_score'] = df_tracks['newness_score'].clip(0, 1)


def cluster_audio_features(df_tracks):
    audio_features = df_tracks[['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                                'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']]
    scaler = StandardScaler()
    scaled_audio_features = scaler.fit_transform(audio_features)
    num_clusters = 3
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    df_tracks['audio_features_type'] = kmeans.fit_predict(
        scaled_audio_features)


def merge_artists(df_tracks, df_artists):
    df_tracks['artist'] = df_tracks['artist'].astype(
        str).str.strip("[]").str.replace("'", "")
    common_artists = set(df_tracks['artist']).intersection(df_artists['name'])
    df_common_artists = df_tracks[df_tracks['artist'].isin(common_artists)]
    df_common_2 = df_artists[df_artists['name'].isin(common_artists)]
    return pd.merge(df_common_artists, df_common_2, left_on='artist', right_on='name', how='inner')


def create_final_dataframe(df_merged):
    columns_to_keep = ['track_id', 'duration', 'artist', 'popularity_x', 'album_name', 'track_genre', 'newness_score',
                       'audio_features_type', 'followers', 'popularity_y']
    df_final = df_merged[columns_to_keep]
    df_final = df_final.rename(columns={
        'popularity_x': 'song_popularity',
        'followers': 'artist_followers',
        'popularity_y': 'artist_popularity'
    })
    return df_final


def main():
    df_tracks = read_avro('data/tracks.avro')
    df_artists = read_avro('data/artists.avro')

    calculate_newness_score(df_tracks)
    cluster_audio_features(df_tracks)
    df_merged = merge_artists(df_tracks, df_artists)
    df_final = create_final_dataframe(df_merged)

    save_to_csv(df_final, 'df_final_songs.csv')
    return df_final


if __name__ == "__main__":
    main()
