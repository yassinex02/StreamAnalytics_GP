from datetime import datetime, timedelta
import random

import numpy as np
import pandas as pd

from utils import get_n_long_sessions, get_n_short_sessions, \
                    get_sessions, allocate_sessions


class Personality():
    def __init__(self):
        self.familiarity_exploration = random.choice(["F", "E"])
        self.timelessness_newness = random.choice(["T", "N"])
        self.loyalty_variety = random.choice(["L", "V"])
        self.commonality_uniqueness = random.choice(["C", "U"])


class User():
    def __init__(self, user_id, df_artists:pd.DataFrame, df_tracks:pd.DataFrame) -> None:
        self.user_id = user_id
        self.personality = Personality()
        self.previous_artist = random.choice(df_artists.id.unique()).tolist()[0]
        self.previous_artists_list = [self.previous_artist] # simplification: keeping track of only 1 artist

        previous_artist_tracks = df_tracks[df_tracks["artist_id"] == self.previous_artist]
        self.previous_track = random.choice(previous_artist_tracks.track_id.unique())

    def simulate_user_events(self, start_date:datetime=datetime(2024, 1, 1)):
        current_date = datetime.now().date()
        simulation_days = (current_date - start_date.date()).days
        
        simulated_events = []
        for day in range(simulation_days):
            n_long_sessions = get_n_long_sessions()
            n_short_sessions = get_n_short_sessions()

            sessions = get_sessions(self.user)

        return simulated_events
    

class Session():
    def __init__(self, user, type):
        self.user = user
        self.type = type
        self.tracks_list = []
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
        df_tracks["release_date"] = pd.to_datetime(df_tracks["release_date"])
        sorted_tracks = df_tracks.sort_values(by='release_date')
        if self.user.personality.timelessness_newness == "N":
            sorted_tracks = df_tracks.sort_values(by='release_date', ascending=False)

        return sorted_tracks
    
    def sample_from_exponential_distribution(self, df_tracks:pd.DataFrame):
        release_dates = df_tracks.release_date

        intervals = [(release_dates[i + 1] - release_dates[i]).days for i in range(len(release_dates) - 1)]
        lambda_estimate = 1.0 / np.mean(intervals)

        cumulative_probabilities = np.cumsum(np.exp(-lambda_estimate * np.array(intervals)))
        cumulative_probabilities /= cumulative_probabilities[-1]

        random_number = np.random.rand()
        selected_index = np.searchsorted(cumulative_probabilities, random_number)
        selected_song = df_tracks.iloc[selected_index].track_id

        return selected_song

    def get_next_track(self, df_tracks:pd.DataFrame):
        if self.user_is_very_loyal():
            return self.user.previous_track
                
        if self.user_is_loyal():
            df_tracks = df_tracks[df_tracks["artist_id"] == self.user.previous_artist]
        elif self.user_is_familiar():
            df_tracks = df_tracks[df_tracks["artist_id"].isin(self.user.previous_artists_list)]
        
        sorted_tracks = self.sort_tracks(df_tracks)
        next_track = self.sample_from_exponential_distribution(sorted_tracks)
        
        return next_track
       
    def get_tracks_list(self, df_tracks:pd.DataFrame) -> None:
        n_tracks = self.get_n_tracks()

        tracks_list = []
        for _ in range(n_tracks):
            track = self.get_next_track(self, df_tracks)
            self.user.previous_track = track
            self.user.previous_artist = df_tracks[df_tracks["track_id"] == track]["artist_id"].tolist()[0]
            tracks_list.append(track)
        self.tracks_list = tracks_list

    def user_will_skip_track(self):
        random_number = random.randint(0, 2)
        if random_number == 0:
            return True
        return False
    
    def get_listening_time(self, track_duration):
        lambda_param = 1.0 / track_duration
        listening_time = int(np.random.exponential(scale=1.0/lambda_param))

        return min(listening_time, track_duration)
    
    def get_session_listening_times(self, df_tracks) -> dict:
        listening_times = {}

        for track in self.tracks_list:
            track_duration = df_tracks[df_tracks["track_id"] == track]["duration"].item()
            if self.user_will_skip_track():
                listening_time = self.get_listening_time(track_duration)
            else:
                listening_time = track_duration
            listening_times[track] = listening_time

        return listening_times
    
    def update_session_duration(self, listening_times:dict) -> None:
        self.total_duration = sum(listening_times.values())

    def simulate_session(self):
        self.get_tracks_list()
        listening_times = self.get_session_listening_times()
        self.update_session_duration(listening_times)
