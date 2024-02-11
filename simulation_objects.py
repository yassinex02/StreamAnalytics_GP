from datetime import datetime, timedelta
import random

import numpy as np
import pandas as pd



class Personality():
    def __init__(self):
        self.familiarity_exploration = random.choice(["F", "E"])
        self.timelessness_newness = random.choice(["T", "N"])
        self.loyalty_variety = random.choice(["L", "V"])
        self.commonality_uniqueness = random.choice(["C", "U"])


class Track():
    def __init__(self, track_id, listening_time):
        self.track_id = track_id
        self.listening_time = listening_time


class Session():
    def __init__(self, user, type):
        self.user = user
        self.type = type
        self.tracks_list = []
        self.listening_times = []
        self.total_duration = 0

    def get_n_tracks(self):
        """
            Returns the number of tracks that will be generated 
            for this instance of Session.
        """

        if self.type not in ["short", "long"]:
            raise ValueError("Type must be either 'short' or 'long'")
        
        if self.type == "long":
            n_tracks = int(np.random.normal(loc=10, scale=2))
        elif self.type == "short":
            n_tracks = int(np.random.normal(loc=5, scale=1))

        return n_tracks
    
    def user_is_very_loyal(self):
        """
            This method determines whether the user will
            play the same song he previously played.
        """
        probability_repeat_song = 0.05
        if self.user.personality.loyalty_variety == "L":
            probability_repeat_song = 0.2
        
        random_float = random.random()
        if random_float < probability_repeat_song:
            return True

        return False
        
    def user_is_loyal(self):
        """
            This method determines whether the user will
            play a song from the same previous artist.
        """
        probability_repeat_same_artist = 0.1
        if self.user.personality.loyalty_variety == "L":
            probability_repeat_same_artist = 0.5

        random_float = random.random()
        if random_float < probability_repeat_same_artist:
            return True
        
        return False
    
    def user_is_familiar(self):
        """
            This method determines whether the user will
            play a song from an artist he previously listened to.
        """
        probability_repeat_artists = 0.5
        if self.user.personality.familiarity_exploration == "F":
            probability_repeat_artists = 0.95
        
        random_float = random.random()
        if random_float < probability_repeat_artists:
            return True
        
        return False
    
    def sort_tracks(self, df_tracks:pd.DataFrame) -> pd.DataFrame:
        """
            This method sorts the tracks by date depending on user personality.
        """
        sorted_tracks = df_tracks.sort_values(by='newness_score')
        if self.user.personality.timelessness_newness == "N":
            sorted_tracks = df_tracks.sort_values(by='newness_score', ascending=False)

        return sorted_tracks
    
    def sample_from_exponential_distribution(self, df_tracks: pd.DataFrame):
        lambda_parameter = 3 / len(df_tracks)
        sample = int(np.random.exponential(scale=1/lambda_parameter))
        track_index = min(sample, len(df_tracks) - 1)
        track_id = df_tracks.iloc[track_index]["track_id"]

        return track_id


    def get_next_track(self, df_tracks:pd.DataFrame):
        if self.user_is_very_loyal():
            return self.user.previous_track
                
        if self.user_is_loyal():
            df_tracks = df_tracks[df_tracks["artist"] == self.user.previous_artist]
        elif self.user_is_familiar():
            df_tracks = df_tracks[df_tracks["artist"].isin(self.user.previous_artists_list)]
        
        sorted_tracks = self.sort_tracks(df_tracks)
        next_track = self.sample_from_exponential_distribution(sorted_tracks)
        
        return next_track
       
    def get_tracks_list(self, df_tracks:pd.DataFrame) -> None:
        n_tracks = self.get_n_tracks()

        tracks_list = []
        for _ in range(n_tracks):
            track = self.get_next_track(df_tracks)
            self.user.previous_track = track
            self.user.previous_artist = df_tracks[df_tracks["track_id"] == track]["artist"].tolist()[0]
            tracks_list.append(track)
        self.tracks_list = tracks_list

        return tracks_list

    def user_will_skip_track(self):
        random_number = random.randint(0, 2)
        if random_number == 0:
            return True
        return False
    
    def get_listening_time(self, track_duration):
        lambda_param = 1.0 / track_duration
        listening_time = int(np.random.exponential(scale=1.0/lambda_param))

        return min(listening_time, track_duration)
    
    def get_session_listening_times(self, df_tracks:pd.DataFrame) -> dict:
        listening_times = {}

        for track in self.tracks_list:
            track_duration = df_tracks[df_tracks["track_id"] == track]["duration"].tolist()[0]
            if self.user_will_skip_track():
                listening_time = self.get_listening_time(track_duration)
            else:
                listening_time = track_duration
            listening_times[track] = listening_time

        return listening_times
    
    def update_session_duration(self, listening_times:dict) -> None:
        self.total_duration = sum(listening_times.values())

    def update_tracks_list(self, tracks_list) -> None:
        self.tracks_list = tracks_list

    def simulate_session(self, df_tracks:pd.DataFrame):
        tracks_list = self.get_tracks_list(df_tracks)
        listening_times = self.get_session_listening_times(df_tracks)
        tracks_objects_list = [Track(tracks_list[i], listening_times[tracks_list[i]]) for i in range(len(tracks_list))]
        self.update_tracks_list(tracks_objects_list)
        self.update_session_duration(listening_times)


class User():
    def __init__(self, user_id, artists:list, df_tracks:pd.DataFrame) -> None:
        self.user_id = user_id
        self.personality = Personality()
        self.previous_artist = random.choice(artists)
        self.previous_artists_list = [self.previous_artist]

        previous_artist_tracks = df_tracks[df_tracks["artist"] == self.previous_artist]
        self.previous_track = random.choice(previous_artist_tracks.track_id.unique())

    def get_n_long_sessions(self):
        n = random.randint(0, 100)
        if n < 2:
            return 3
        elif n <10:
            return 0
        elif n <50:
            return 1
        else:
            return 2
        
    def get_n_short_sessions(self):
        return int(np.random.normal(loc=5, scale=1))
    
    def get_sessions(self, n_long_sessions:int, n_short_sessions:int, df_tracks:pd.DataFrame):
        sessions = []
        for _ in range(n_long_sessions):
            session = Session(user=self, type="long")
            session.simulate_session(df_tracks)
            sessions.append(session)
        for _ in range(n_short_sessions):
            session = Session(user=self, type="short")
            session.simulate_session(df_tracks)
            sessions.append(session)

        return sessions

    def allocate_sessions(self, sessions:list):
        """
            Algorithm that divides the day into 24 hour-long slots,
            and allocates each session to one or more slots depending
            on its duration. This method returns a session schedule dict
            of the form: {session: start_time} where start_time is the
            index of the hour-long slot where the session starts.
        """
        slots_availability = {i:True for i in range(24)}

        session_schedule = {}
        for session in sessions:
            n_slots = int(session.total_duration / (1000 * 60 * 60)) + 1
            available_slots = [slot for slot, availability in slots_availability.items() if availability]
            random.shuffle(available_slots)
            for slot in available_slots:
                if all(slots_availability[i] for i in range(slot, slot + n_slots)):
                    session_schedule[session] = slot
                    for i in range(slot, slot + n_slots):
                        slots_availability[i] = False
                    break
            if session not in session_schedule:
                print(f"Could not find a slot for {session}")

        return session_schedule

    def get_daily_schedule(self, df_tracks):
        n_long_sessions = self.get_n_long_sessions()
        n_short_sessions = self.get_n_short_sessions()
        sessions = self.get_sessions(n_long_sessions, n_short_sessions, df_tracks)
        session_schedule = self.allocate_sessions(sessions)
        sorted_schedule = dict(sorted(session_schedule.items(), key=lambda item: item[1]))

        return sorted_schedule
    
    def get_timestamp(self, start_date, day, hour, miliseconds):
        timestamp = start_date + \
                    timedelta(days=day, hours=hour, milliseconds=miliseconds)
        
        return timestamp
    
    def simulate_daily_events(self, day, df_tracks, start_date, simulated_events, id):
        sorted_schedule = self.get_daily_schedule(df_tracks)
        for session in sorted_schedule:
            hour = sorted_schedule[session]
            miliseconds = 0
            for track in session.track_list:
                miliseconds += track.listening_time
                timestamp = self.get_timestamp(start_date, day, hour, miliseconds)
                
                event_record = {"id": id, "timestamp": timestamp.isoformat(),
                                "track_id": track.track_id, "user_id": self.user_id,
                                "listening_time": track.listening_time}
                simulated_events.append(event_record)
                id += 1

        return simulated_events, id

    def simulate_user_events(self, df_tracks:pd.DataFrame, start_date:datetime=datetime(2024, 1, 1)):
        current_date = datetime.now().date()
        simulation_days = (current_date - start_date.date()).days
        
        simulated_events = []
        id = 0
        for day in range(simulation_days):
            simulated_events, id = self.simulate_daily_events(day, df_tracks, start_date, simulated_events, id)
        
        return simulated_events