from datetime import datetime, timedelta
import random

from faker import Faker
from fastavro import writer
import pandas as pd
from serializer import get_parsed_track_schema, get_parsed_user_schema



def generate_random_birthdates(min_date:datetime, max_date:datetime, n_dates:int):
    total_days = (max_date - min_date).days

    birthdates = []
    for _ in range(n_dates):
        days_offset = int(random.normalvariate(0, 0.5) * total_days)
        birthdate = min_date + timedelta(days=days_offset)
        birthdates.append(birthdate.strftime('%Y-%m-%d'))


def generate_fake_users(n_users:int):
    fake = Faker()
    usernames_list = [fake.user_name() for _ in range(n_users)]
    locations_list = [fake.country() for _ in range(n_users)]
    birthdates_list = generate_random_birthdates(min_date=datetime(1970,1,1),
                                            max_date=datetime(2011,1,1),
                                            n_dates=n_users)
    genders_list = [random.choice(["M", "F"] for _ in range(n_users))]

    users = {"usernames": usernames_list, "locations": locations_list,
             "birthdates": birthdates_list, "genders": genders_list}

    return users


def serialize_user_data(users:dict, output_path):
    parsed_user_schema = get_parsed_user_schema()

    records = []
    for i in range(len(users["usernames"])):
        record = {
            "user_id": i,
            "username": users["usernames"][i],
            "location": users["locations"][i],
            "birthdate": users["birthdates"][i],
            "gender": users["genders"][i]
        }
        records.append(record)

    with open(output_path, "wb") as out:
        writer(out, parsed_user_schema, records)


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

    with open(output_path, 'wb') as out:
        writer(out, parsed_track_schema,
                        df_tracks.to_dict(orient='records'))


def main():
    #serialize_song_data(tracks_path="data/tracks.csv", output_path="data/tracks.avro")
    users = generate_fake_users(100)
    serialize_user_data(users, output_path="data/users.avro")
    

if __name__ == "__main__":
    main()
