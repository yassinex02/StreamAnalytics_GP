import pandas as pd

# Assuming df_common_tracks and df_2 have been created previously
# ...

# Read df_2 from the CSV file
df_2 = pd.read_csv(
    '/Users/yassine/Desktop/IE/4th year/2nd sem/stream analytics/datasets/dataset.csv')
df_tracks = pd.read_csv(
    '/Users/yassine/Desktop/IE/4th year/2nd sem/stream analytics/datasets/tracks.csv')

df_tracks = df_tracks.drop_duplicates(subset='name', keep='first')
df_2 = df_2.drop_duplicates(subset='track_name', keep='first')

common_songs = set(df_tracks['name']).intersection(df_2['track_name'])

df_common_tracks = df_tracks[df_tracks['name'].isin(common_songs)]
df_common_2 = df_2[df_2['track_name'].isin(common_songs)]

df_2_selected = df_common_2[['track_name', 'album_name', 'track_genre']]

df_merged = pd.merge(df_common_tracks, df_2_selected,
                     left_on='name', right_on='track_name', how='inner')

print(df_merged.artists.dtype)
