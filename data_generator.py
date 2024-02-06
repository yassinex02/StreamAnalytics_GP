import datetime

from faker import Faker
from fastavro import writer
import pandas as pd
from serializer import get_parsed_track_schema


def generate_fake_users(n_users:int):
    fake = Faker()
    for i in n_users:
        username = fake.user_name()
        location = fake.country()
        birthdate = fake.date_between()


def serialize_song_data(tracks_path:str, output_path):
    parsed_track_schema = get_parsed_track_schema()
    df_tracks_full = pd.read_csv(tracks_path)

    columns_to_keep = ['id', 'name', 'duration_ms', 'artists']
    df_tracks = df_tracks_full[columns_to_keep]

    df_tracks = df_tracks.dropna(subset=['id'])
    df_tracks = df_tracks.rename(columns={'id': 'track_id'})
    df_tracks['track_id'] = df_tracks['track_id'].astype('str')
    df_tracks['artist'] = df_tracks['artists'].str.strip()
    df_tracks = df_tracks.dropna(subset=['artist'])

    with open(output_path, 'wb') as avro_output_file:
        writer(avro_output_file, parsed_track_schema,
                        df_tracks.to_dict(orient='records'))


def main():
    #serialize_song_data(tracks_path="data/tracks.csv", output_path="data/tracks.avro")
    pass
    

if __name__ == "__main__":
    main()
