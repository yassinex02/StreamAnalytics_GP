# Spotify Wrapped Data Feed 
## Steps to run the files
To set up the environment : "run conda env create -f conda.yaml"  
To actiavte it conda :  "conda activate stream_analytics_project"  
To run the simulation and populate the tables :"python data_generator.py" , but first specify the paths to the datasets in the same file at the very bottom in the main function for serialize_song_data('[tracks dataset path](https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-19212020-600k-tracks?select=tracks.csv)', '[songs dataset path](https://www.kaggle.com/datasets/amitanshjoshi/spotify-1million-tracks)' and serialize_artist_data('[artists dataset path](https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-19212020-600k-tracks?select=tracks.csv)')

## Overview
This repository contains the code and documentation for generating synthetic data for Spotify Wrapped using the AVRO format. The synthetic data generation scripts provided here are designed to align with the needs of our project, facilitating data analysis, testing, and development in a controlled environment.

## Introduction 
The objective of this project is to design a data feed for Spotify Wrapped, a feature that provides users with insights into their listening habits over the past year. The data feed includes various aspects such as song plays, skips (implicitely), and other relevant data. In this report, we discuss the development process of an AVRO schema for the Spotify Wrapped data feed and the creation of scripts to generate synthetic data mimicking user streaming experiences.

## AVRO Format Choice 
### Datasets 
To finalize the dataset that we were using for the project, we needed to merge two datasets as one included songs but no genre feature. As such, we did an inner join on the common song names between these datasets to keep the songs in the first dataset while introducing the genres column. Additionally, we merged the resulting dataset  with the artist dataset on the common artists to get the artist popularity and the artist number of followers. 

### Transformations
We also had to do some transformations. We applied K Means clustering to audio features in the track table after using StandardScaler to assign each track to one of the clusters based on its audio features and added a new column `audio_features_type` to the dataset indicating the cluster each track belongs to. Furthermore, we created a newness score for each track based on the release date. We created a mask to identify release dates that are represented by 2024 only. For these dates, we calculate the number of months elapsed since the release date up until January 1, 2024 and compute the newness score that falls between 0 and 1 for each track using a normalization function. 0 represents older songs while 1 represents newer songs. 

### Tables 
Our group decided on 4 tables. The AVRO schema defines these entities along with their respective attributes and relationships.
1. **user**: to generate Spotify users, we used the Faker and datetime libraries to provide us with a list of users including their ID, username, location, birthdate, gender and listening time per song. We defined the type of each variable based on our knowledge of previous similar variables we have seen and used in other datasets.
2. **track**: introduced variables that were included in the dataset we chose, including track ID, duration, artist, name, popularity, release date, and many more. The type of each variable was defined based on the original type of the variable in the two datasets we used to generate data.
3. **artist**: contained the ID, followers, name, and popularity variables, all of which were also defined by the type that was given in the original artist dataset.
4. **event**:   

## Design of Synthetic Data Generation Scripts
The synthetic data generation process starts with defining the data schema. This AVRO schema describes the structure of the data including data types, field names, and any nested structures. It involves simulating the streaming experiences of n (10000 in our case ) individual users . 

We have developed Python scripts to generate realistic, time-series data reflecting typical user interaction patterns with Spotify's streaming service. Key components of the script include:
- **User Profile Generation**: Random generation of user profiles including demographics, preferences, and listening habits (data_generator.py).
- **Song Catalog Simulation**: Creation of a simulated song catalog with diverse genres, artists, and popularity metrics (main.py).
- **User Interaction Simulation**: Generation of user interactions such as song plays, skips, likes, and playlist creations based on probabilistic models (main.py).
- **Data Serialization**: Transformation of generated data into AVRO format adhering to the defined schema (serializer.py).

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