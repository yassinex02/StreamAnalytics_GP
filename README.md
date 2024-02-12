# Spotify Wrapped Data Feed 
## Steps to run the files
To set up the environment: `run conda env create -f conda.yaml`  
To activate it: `conda activate stream_analytics_project`  
  
Make sure to have `artists.csv`, `tracks.csv` and `tracks_extended.csv` in the data folder, or specify the paths to the datasets in the main function of `src/data_generator.py` for the functions `serialize_song_data`('[tracks.csv dataset path](https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-19212020-600k-tracks?select=tracks.csv), '[tracks_extended.csv dataset path](https://www.kaggle.com/datasets/amitanshjoshi/spotify-1million-tracks)'), and `serialize_artist_data`('[artists dataset path](https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-19212020-600k-tracks?select=tracks.csv)')  
  
To run the simulation and populate the tables: `python3 main.py`


## Overview
This repository contains the code and documentation for generating synthetic data for Spotify Wrapped using the AVRO format. The synthetic data generation scripts provided here are designed to align with the needs of our project, facilitating data analysis, testing, and development in a controlled environment.

## Introduction 
The objective of this project is to design a data feed for Spotify Wrapped, a feature that provides users with insights into their listening habits over the past year. The data feed includes various aspects such as song plays, skips (implicitly), and other relevant data. In this report, we discuss the development process of an AVRO schema for the Spotify Wrapped data feed and the creation of scripts to generate synthetic data mimicking user streaming experiences.

## AVRO Format Choice 
### Datasets 
To finalize the dataset that we were using for the project, we needed to merge two datasets as one included songs but no genre feature. As such, we did an inner join on the common song names between these datasets to keep the songs in the first dataset while introducing the genres column. Additionally, we merged the resulting dataset  with the artist dataset on the common artists to get the artist popularity and the artist number of followers. 

### Transformations
We also had to do some transformations. We applied K Means clustering to audio features in the track table after using StandardScaler to assign each track to one of the clusters based on its audio features and added a new column `audio_features_type` to the dataset indicating the cluster each track belongs to. Furthermore, we created a newness score for each track based on the release date. We created a mask to identify release dates that are represented by 2024 only. For these dates, we calculate the number of months elapsed since the release date up until January 1, 2024 and compute the newness score that falls between 0 and 1 for each track using a normalization function. 0 represents older songs while 1 represents newer songs. 

### Tables 
Our group decided on 4 tables. The AVRO schema defines these entities along with their respective attributes and relationships.
1. **User**: to generate Spotify users, we used the Faker and datetime libraries to provide us with a list of users including a `user_id`, `username`, `location`, `birthdate` and `gender`. We defined the type of each variable based on our knowledge of previous similar variables we have seen and used in other datasets.
2. **Track**: introduced variables that were included in the dataset we chose, including `track_id`, `duration`, `artist`, `name`, `popularity`, `release date`, and many more. The type of each variable was defined based on the original type of the variable in the two datasets we used to generate data.
3. **Artist**: contained the `id`, `followers`, `name`, and `popularity` variables, all of which were also defined by the type that was given in the original artist dataset.
4. **UserEvent**: This table records whenever a track is played by a user. It contains an `id` for the record, a `timestamp` for when this record occured, the `track_id` of the track that was played, the `user_id` of the user that played the track, and the `listening_time`, expressed in miliseconds.

## Design of Synthetic Data Generation Scripts
The synthetic data generation process starts with defining the data schema. The AVRO schema of the previous tables were defined in the file `src/serializer.py`.  
Our synthetic data generation scripts involves simulating the streaming experiences of n individual users (in our cases 10,000 users). 

We have developed Python scripts to generate realistic, time-series data reflecting typical user interaction patterns with Spotify's streaming service. Key components of the script include:
- **User Profile Generation**: Random generation of n user profiles including demographics (birthdate, gender, location). `src/data_generator.py`: `generate_fake_users(n_users=10000)`.
- **User Events Simulation**: Generation of user-events (song plays) based on randomly assigned personalities and on probabilistic models `src/data_generator.py`: `generate_all_user_events()`.

## User Events Simulation
The Events simulation uses 4 classes that were defined in `src/simulation_objects.py`:
- `Personality()`: This object contains a randomly generated personality that will influence the user events in the simulation.
- `Track()`: This object stores the `track_id` and `listening_time` variables.
- `Session()`: This object represents a "session" of listening to music.
- `User()`: This object represents individual users, and contains the methods to simulate their listening behavior.  
  
The simulation works by looping through every user that was generated in the users.avro table, and running the method `simulate_user_events()` of the `User()` class. The `simulate_user_events()` takes a start_date as an argument, which by default is the 1st of January 2024. It will then simulate the daily listening behaviour for the given user, every day starting from the start_date until the current date.  
  
Regarding the daily simulations, we have decided to group them into sessions, because in reality, it is more common to listen to several songs in a row than to randomly play songs with pauses in-between throughout the day.  
Every day, every user initializes a number of sessions (long sessions and short sessions). Each one of these sessions initializes a number of songs that will be played, by drawing from a normal distribution with different parameters depending on the type of session.

Once we have the sessions and the number of songs for each one of them, we need to decide on which songs will be played (we will come back to this in a moment). Then, we schedule these sessions throughout the day for a given user with the method `allocate_sessions()` of the User object.  
  
Going back to the choice of songs, the main challenge here was to generate some data that will allow us to classify the users along one of the 16 personality types of Spotify. These 16 personalities are built on the following 4 dimensions:  
![spotify four dimensions screenshot](data/4_dimensions.png)
  
Looking at these 4 dimensions, we can think about them as two seperate groups in the way we approach the selection of the tracks that will be played by the user:
- **Dimensions that modify the subset of songs that we draw from**: Familiarity/Exploration, Loyalty/Variety
- **Dimensions that modify the weights or the order of the songs that we draw**: Timelessness/Newness, Commonality/Uniqueness.
  
In our approach, we define the 8 characteristics as follows:  
  
- Familiarity: If a user has the familiarity trait, it means that he will have a higher chance of listening to an artist he has already played before.
- Exploration: If a user has the exploration trait, he will have a lower chance of listening to an artist he has already played before (lower in relative terms compared to a user with familiarity)
  
- Loyalty: If a user has the loyalty trait, he will be more likely to listen to the same artist he listened to previously, or to listen to the exact same song he previously played.
- Variety: By contrast to loyalty, will have a lower probability of playing same song or same artist.
  
- Timelessness: The user will be more likely to play older songs all else equal.
- Newness: The user will be more likely to play newer songs all else equal.
  
- Commonality: The user listens to mainstream songs/artists.
- Uniqueness: The user listens to more niche songs/artists.

Regarding the first category, we do the following checks:
- If has the 

## Challenges Encountered


## Alignment of the Synthetic Data with Project Needs
The synthetic data generated closely aligns with the project's needs by providing a representative sample of user interactions and streaming experiences. It comprehensively reflects a similar structure to that seen in real-world data. The data feed enables analytics and insights generation for Spotify Wrapped, facilitating personalized user experiences and recommendations. Moving forward, continuous refinement and expansion of the data feed will further enhance its utility and relevance in understanding user preferences and enhancing the Spotify experience.

## Credits
The authors of this project are:
1. Taha Yassine Moumni
2. Mehdi Zaid
3. Maria Sawalha
4. Mateo Ploquin 
5. Abdallah Ghaddar
6. Talal Shehadeh