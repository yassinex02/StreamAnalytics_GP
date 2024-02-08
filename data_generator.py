from datetime import datetime, timedelta
import random

from faker import Faker
from fastavro import writer
import numpy as np
import pandas as pd
from serializer import get_parsed_track_schema, get_parsed_user_schema



def generate_random_birthdates(min_date:datetime, max_date:datetime, n_dates:int):
    total_days = (max_date - min_date).days

    birthdates = []
    for _ in range(n_dates):
        days_offset = int(random.normalvariate(0, 0.5) * total_days)
        birthdate = min_date + timedelta(days=days_offset)
        birthdates.append(birthdate.strftime('%Y-%m-%d'))

    return birthdates


def generate_fake_users(n_users:int):
    fake = Faker()
    usernames_list = [fake.user_name() for _ in range(n_users)]
    locations_list = [fake.country() for _ in range(n_users)]
    birthdates_list = generate_random_birthdates(min_date=datetime(1980,1,1),
                                            max_date=datetime(2011,1,1),
                                            n_dates=n_users)
    genders_list = [random.choice(["M", "F"]) for _ in range(n_users)]

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
    df_tracks = df_tracks.rename(columns={'id': 'track_id',
                                          'duration_ms': 'duration'})
    df_tracks['track_id'] = df_tracks['track_id'].astype('str')
    df_tracks['artist'] = df_tracks['artists'].str.strip()
    df_tracks = df_tracks.dropna(subset=['artist'])

    with open(output_path, 'wb') as out:
        writer(out, parsed_track_schema,
                        df_tracks.to_dict(orient='records'))


class User():
    def __init__(self, user_id, tracks) -> None:
        self.actions = ["PLAY", "PAUSE", "SKIP", "QUIT", "LIKE", "DOWNLOAD", "ADD TO PLAYLIST"]
        # actions to remove from available actions if same as previous action (user can't quit/pause twice in a row)
        self.simulation_actions = ["PLAY", "PAUSE", "QUIT"]
        self.user_id = user_id                                   
        self.previous_action = random.choice(self.simulation_actions)
        self.tracks = tracks
        self.average_n_actions = np.random.normal(100, 25) # average number of daily events for user
        self.std_dev_n_actions = random.randint(10, 30)

    def get_action(self):
        if self.previous_action == "PAUSE":
            actions = self.actions.remove("PAUSE")
        elif self.previous_action == "QUIT":
            actions = self.actions.remove("QUIT")
        else:
            actions = self.actions
        
        action = random.choice(actions)
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
    
    def simulate_app_sessions(self, start_date:datetime=datetime(2024, 1, 1)):
        current_date = datetime.now().date()
        simulation_days = (current_date - start_date).days
        
        simulated_events = []

        for day in range(simulation_days):
            n_actions = np.random.normal(self.average_n_actions, self.std_dev_n_actions)
            for _ in range(n_actions):
                id = 0
                action = self.get_action()
                timestamp = self.get_timestamp(start_date, day)
                track_id = self.get_track_id()

                event_record = {"id": id, "timestamp": timestamp,
                            "action": action, "track_id": track_id,
                            "user_id": self.user_id}
                simulated_events.append(event_record)






def main():
    current_date = datetime.now().date()
    simulation_time = current_date - datetime(2024, 1, 1).date()
    print(simulation_time.days)


if __name__ == "__main__":
    main()
