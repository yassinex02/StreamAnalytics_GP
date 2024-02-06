import os
import pandas as pd
import fastavro
from serializer import get_parsed_track_schema


def main():
    # Retrieve parsed_track_schema from serializer.py
    parsed_track_schema = get_parsed_track_schema()

    # Your existing code for reading CSV, processing DataFrame, and writing Avro
    file_path = '/Users/yassine/Desktop/IE/4th year/2nd sem/stream analytics/datasets/tracks.csv'
    df_tracks_full = pd.read_csv(file_path)

    columns_to_keep = ['id', 'name', 'duration_ms', 'artists']
    df_tracks = df_tracks_full[columns_to_keep]

    df_tracks = df_tracks.dropna(subset=['id'])
    df_tracks = df_tracks.rename(columns={'id': 'track_id'})
    df_tracks['track_id'] = df_tracks['track_id'].astype('str')
    df_tracks['artist'] = df_tracks['artists'].str.strip()
    df_tracks = df_tracks.dropna(subset=['artist'])

    output_directory = 'avro_tables'
    os.makedirs(output_directory, exist_ok=True)

    output_file_path = os.path.join(output_directory, 'tracks.avro')

    with open(output_file_path, 'wb') as avro_output_file:
        fastavro.writer(avro_output_file, parsed_track_schema,
                        df_tracks.to_dict(orient='records'))

    print(
        f"Data has been successfully populated into Avro file at {output_file_path}.")


if __name__ == "__main__":
    main()
