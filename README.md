# Spotify Wrapped Data Feed 
To set up the environment : run conda env create -f conda.yaml

To actiavte it conda :  e

## Overview
This repository contains the code and documentation for generating synthetic data for Spotify Wrapped using the AVRO format. The synthetic data generation scripts provided here are designed to align with the needs of our project, facilitating data analysis, testing, and development in a controlled environment.

## Introduction 
The objective of this project is to design a data feed for Spotify Wrapped, a feature that provides users with insights into their listening habits over the past year. The data feed includes various aspects such as song plays, pauses, skips, and other relevant data. In this report, we discuss the development process of an AVRO schema for the Spotify Wrapped data feed and the creation of scripts to generate synthetic data mimicking user streaming experiences.

## AVRO Format Choice 
### Datasets 
To finalize the dataset that we were using for the project, we needed to merge two datasets as one included songs but no genre feature. As such, we did an inner join on the common song names between these datasets to keep the songs in the first dataset while introducing the genres column. Additionally, we merged the resulting dataset  with the artist dataset on the common artists to get the artist popularity and the artist number of followers. 

### Transformations
We also had to do some transformations. We applied K Means clustering to audio features in the track table after using StandardScaler to assign each track to one of the clusters based on its audio features and added a new column `audio_features_type` to the dataset indicating the cluster each track belongs to. Furthermore, we created a newness score for each track based on the release date. We created a mask to identify release dates that are represented by 2024 only. For these dates, we calculate the number of months elapsed since the release date up until January 1, 2024 and compute the newness score that falls between 0 and 1 for each track using a normalization function. 0 represents older songs while 1 represents newer songs. 

### Tables 
Our group decided on 4 tables. The AVRO schema defines these entities along with their respective attributes and relationships.
1. **user**: to generate Spotify users, we used the Faker and datetime libraries to provide us with a list of users including their ID, username, location, birthdate, gender, and favorite genre. We defined the type of each variable based on our knowledge of previous similar variables we have seen and used in other datasets.
2. **track**: introduced variables that were included in the dataset we chose, including track ID, duration, artist, name, popularity, release date, and many more. The type of each variable was defined based on the original type of the variable in the dataset provided to us.
3. **artist**: contained the ID, followers, name, and popularity variables, all of which were also defined by the type that was given in the original dataset.
4. **event**: a user event consists of an event ID, timestamp of the event, track ID, user ID, and listening time, which is how long the user plays the song for. The type of the fields was assigned based on patterns seen in similar/ indentical fields in the other tables. We excluded the field action because we chose only to record the action of when a user plays a song instead of recording pauses, skips, etc.

## Design of Synthetic Data Generation Scripts
The synthetic data generation process starts with defining the data schema. The AVRO schema is specified using JSON, describing the structure of the data including data types, field names, and any nested structures. It involves simulating the streaming experiences of both individual users and multiple independent users. We have developed Python scripts to generate realistic, time-series data reflecting typical user interaction patterns with Spotify's streaming service. Key components of the script include:
- **User Profile Generation**: Random generation of user profiles including demographics, preferences, and listening habits.
- **Song Catalog Simulation**: Creation of a simulated song catalog with diverse genres, artists, and popularity metrics.
- **User Interaction Simulation**: Generation of user interactions such as song plays, and playlist creations based on probabilistic models.
- **Data Serialization**: Transformation of generated data into AVRO format adhering to the defined schema.

Listening personalities (are introduced by categorizing songs and user interactions; each user's behavior is simulated with variations introduced to reflect diverse user preferences and interactions. Below is an image outlining the binary attributes we took into account to measure and describe an aspect of how a user listens to music, independent of what music they like. These include familiarity vs. exploration, timelessness vs. newness, loyalty vs. variety, and commonality vs. uniqueness. 

![image](https://github.com/yassinex02/StreamAnalytics_GP/assets/144900363/4690d27c-2f7d-4820-83bd-c69e2b54b3ed)

### Code Structure 
maybe here we can add the order of the scripts and how to run everything?

## Challenges Encountered
Some of the main challenges that we faced were related to the datasets and variables. 
* In the artist dataset, the *Genre* column was empty, therefore we had to drop it. 
* In the first song dataset, the *release date* variable had very odd formats , DD-MM-YYYY, MM-YYYY, YYYY. That required us to do a lot of preprocessing to be able to find the *months_elapsed* variable and calculate the *newness score*. 
* Some songs were featuring more than one artist , so the *artist* column in the songs dataset came occasionally as a list of strings. This caused a problem when we tried to create an inner join between the song dataset and the artists on common artist names. As such, we decided to delete all the rows that had more than 1 artist featured in a song, resulting in the final dataset that contained around 22k rows which is ideal for our simulation. 

## Alignment of the Synthetic Data with Project Needs
The synthetic data generated closely aligns with the project's needs by providing a representative sample of user interactions and streaming experiences. It comprehensively reflects a similar structure to that seen in real-world data. The data feed enables analytics and insights generation for Spotify Wrapped, facilitating personalized user experiences and recommendations. Moving forward, continuous refinement and expansion of the data feed will further enhance its utility and relevance in understanding user preferences and enhancing the Spotify experience.

## Credits
The authors of this project are:
1. Taha Yassine Moumni
2. Mehdi Zaid
3. Mateo Ploquin 
4. Abdallah Ghaddar
5. Talal Shehadeh 
