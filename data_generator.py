from datetime import datetime, timedelta
import random

from faker import Faker
from fastavro import writer
import numpy as np
import pandas as pd
from serializer import get_parsed_track_schema, get_parsed_user_schema, get_parsed_event_schema, get_parsed_artist_schema

from utils import read_avro


def generate_random_birthdates(min_date: datetime, max_date: datetime, n_dates: int):
    total_days = (max_date - min_date).days

    birthdates = []
    for _ in range(n_dates):
        days_offset = int(random.normalvariate(0, 0.5) * total_days)
        birthdate = min_date + timedelta(days=days_offset)
        birthdates.append(birthdate.strftime('%Y-%m-%d'))

    return birthdates


def generate_fake_users(n_users: int):
    fake = Faker()
    usernames_list = [fake.user_name() for _ in range(n_users)]
    locations_list = [fake.country() for _ in range(n_users)]
    birthdates_list = generate_random_birthdates(min_date=datetime(1980, 1, 1),
                                                 max_date=datetime(2011, 1, 1),
                                                 n_dates=n_users)
    genders_list = [random.choice(["M", "F"]) for _ in range(n_users)]

    users = {"usernames": usernames_list, "locations": locations_list,
             "birthdates": birthdates_list, "genders": genders_list}

    return users


def serialize_user_data(users: dict, output_path):
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


def serialize_song_data(tracks_path: str, df_2_path: str, output_path: str):
    parsed_track_schema = get_parsed_track_schema()

    # Read data from the CSV files
    df_tracks = pd.read_csv(tracks_path)
    df_2 = pd.read_csv(df_2_path)

    # Drop duplicates based on the 'name' and 'track_name' columns
    df_tracks = df_tracks.drop_duplicates(subset='name', keep='first')
    df_2 = df_2.drop_duplicates(subset='track_name', keep='first')

    # Drop the missing values
    df_tracks = df_tracks.dropna(subset=['id', 'name', 'popularity'])

    # Clean and preprocess the data
    df_tracks = df_tracks.rename(
        columns={'id': 'track_id', 'duration_ms': 'duration'})
    df_tracks['track_id'] = df_tracks['track_id'].astype('str')
    df_tracks['artist'] = df_tracks['artists'].str.strip()

    # Find common songs
    common_songs = set(df_tracks['name']).intersection(df_2['track_name'])

    # Create datasets with only common songs
    df_common_tracks = df_tracks[df_tracks['name'].isin(common_songs)]
    df_common_2 = df_2[df_2['track_name'].isin(common_songs)]

    # Select columns from df_2
    df_2_selected = df_common_2[['track_name', 'album_name', 'track_genre']]

    # Perform join on common song names
    df_merged = pd.merge(df_common_tracks, df_2_selected,
                         left_on='name', right_on='track_name', how='inner')

    # Drop duplicates based on the 'name' column in the merged dataframe
    df_merged = df_merged.drop_duplicates(subset='name', keep='first')

    # Rename columns to match the Avro schema
    df_merged = pd.merge(df_common_tracks, df_2_selected,
                         left_on='name', right_on='track_name', how='inner')

# Rename the 'artists' column to 'artist'

    avro_records = df_merged.to_dict(orient='records')
    avro_records_with_schema = []
    for record in avro_records:
        avro_record_with_schema = {}
        for field in parsed_track_schema['fields']:
            field_name = field['name']
            avro_record_with_schema[field_name] = record.get(
                field_name, field.get('default', None))
        avro_records_with_schema.append(avro_record_with_schema)

    with open(output_path, 'wb') as out:
        writer(out, parsed_track_schema, avro_records_with_schema)


def serialize_artist_data(artists_path: str, output_path: str):
    parsed_artists_schema = get_parsed_artist_schema()
    # Read data from the Excel file
    df_artists = pd.read_csv(artists_path)

    # Drop rows with missing values in key columns
    df_artists = df_artists.dropna(subset=['id', 'name', 'popularity'])

    # Prepare Avro records with schema
    avro_records = df_artists.to_dict(orient='records')
    avro_records_with_schema = []

    for record in avro_records:
        avro_record_with_schema = {}
        for field in parsed_artists_schema['fields']:
            field_name = field['name']
            avro_record_with_schema[field_name] = record.get(
                field_name, field.get('default', None))
        avro_records_with_schema.append(avro_record_with_schema)

    # Serialize Avro data to the specified output path
    with open(output_path, 'wb') as out:
        writer(out, parsed_artists_schema, avro_records_with_schema)


class User():
    def __init__(self, user_id, tracks) -> None:
        self.actions = ["PLAY", "PAUSE", "SKIP", "QUIT",
                        "LIKE", "DOWNLOAD", "ADD_TO_PLAYLIST"]
        # actions to remove from available actions if same as previous action (user can't quit/pause twice in a row)
        self.simulation_actions = ["PLAY", "PAUSE", "QUIT"]
        self.user_id = user_id
        self.previous_action = random.choice(self.simulation_actions)
        self.tracks = tracks
        # average number of daily events for user
        self.average_n_actions = np.random.normal(100, 25)
        self.std_dev_n_actions = random.randint(10, 30)

    def get_action(self):
        available_actions = self.actions.copy()
        if self.previous_action in ["PAUSE", "QUIT"]:
            available_actions.remove(self.previous_action)

        action = random.choice(available_actions)
        if action in self.simulation_actions:
            self.previous_action = action

        return action

    def get_timestamp(self, start_date, day):
        timestamp = start_date + \
            timedelta(days=day, hours=random.randint(0, 23), minutes=random.randint(0, 59),
                      seconds=random.randint(0, 59))
        return timestamp

    def get_track_id(self):
        return random.choice(self.tracks)

    def simulate_user_events(self, start_date: datetime = datetime(2024, 1, 1)):
        current_date = datetime.now().date()
        simulation_days = (current_date - start_date.date()).days

        simulated_events = []

        for day in range(simulation_days):
            n_actions = int(np.random.normal(
                self.average_n_actions, self.std_dev_n_actions))
            for _ in range(n_actions):
                id = 0
                action = self.get_action()
                timestamp = self.get_timestamp(start_date, day)
                track_id = self.get_track_id()

                event_record = {"id": id, "timestamp": timestamp.isoformat(),
                                "action": action, "track_id": track_id,
                                "user_id": self.user_id}
                simulated_events.append(event_record)

        return simulated_events


def simulate_all_user_events(users_path: str, tracks_path: str):
    df_users = read_avro(users_path)
    df_tracks = read_avro(tracks_path)

    tracks = df_tracks["track_id"].unique()
    user_id_list = df_users["user_id"].unique()

    all_user_events = []
    for user_id in user_id_list:
        user = User(user_id, tracks)
        simulated_events = user.simulate_user_events()
        all_user_events.extend(simulated_events)

    return all_user_events


def serialize_event_data(all_user_events: list, output_path: str):
    parsed_event_schema = get_parsed_event_schema()
    with open(output_path, "wb") as out:
        writer(out, parsed_event_schema, all_user_events)


def main():
    serialize_song_data(
        '/Users/yassine/Desktop/IE/4th year/2nd sem/stream analytics/datasets/tracks.csv',
        '/Users/yassine/Desktop/IE/4th year/2nd sem/stream analytics/datasets/dataset.csv',
        'data/tracks.avro')  # CHAGE WITH PATH TO EXCEL
    serialize_artist_data('/Users/yassine/Desktop/IE/4th year/2nd sem/stream analytics/datasets/artists.csv',
                          'data/artists.avro')  # CHAGE WITH PATH TO EXCEL
    all_user_events = simulate_all_user_events(users_path="data/users.avro",
                                               tracks_path="data/tracks.avro")
    serialize_event_data(all_user_events, output_path="data/events.avro")


if __name__ == "__main__":
    main()
