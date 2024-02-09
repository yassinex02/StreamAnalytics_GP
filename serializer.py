from fastavro import parse_schema


def get_parsed_event_schema():
    event_schema = {
        "doc": "Spotify Wrapped Data Feed - User Event",
        "name": "UserEvent",
        "namespace": "com.spotify.wrapped",
        "type": "record",
        "fields": [
            {"name": "id", "type": "long"},
            {"name": "timestamp", "type": "string",
                "logicalType": "timestamp-millis"},
            {"name": "action", "type": {"type": "enum", "name": "event",
                                        "symbols": ["PLAY", "PAUSE", "SKIP", "QUIT",
                                                    "LIKE", "DOWNLOAD", "ADD_TO_PLAYLIST"],
                                        "default": "PLAY"}},
            {"name": "track_id", "type": "string"},
            {"name": "user_id", "type": "long"}
        ]
    }

    return parse_schema(event_schema)


def get_parsed_user_schema():
    user_schema = {
        "doc": "Spotify Wrapped Data Feed - User Info",
        "name": "User",
        "namespace": "com.spotify.wrapped",
        "type": "record",
        "fields": [
            {"name": "user_id", "type": "long"},
            {"name": "username", "type": "string"},
            {"name": "location", "type": "string"},
            {"name": "birthdate", "type": "string", "logicalType": "date"},
            {"name": "gender", "type": "string", "symbols": ["M", "F"]},
            {"name": "favorite_genre", "type": {
                "type": "array", "items": "string"}, "default": []}
        ]
    }

    return parse_schema(user_schema)

# TAKIG EVRTH TO GENERATE THE PERSONALITIES


def get_parsed_track_schema():
    track_schema = {
        "doc": "Spotify Wrapped Data Feed - Track Info",
        "name": "Track",
        "namespace": "com.spotify.wrapped",
        "type": "record",
        "fields": [
            {"name": "track_id", "type": "string"},
            {"name": "duration", "type": "int", "default": 0},
            {"name": "artist", "type": "string"},
            {"name": "name", "type": ["null", "string"], "default": None},
            {"name": "popularity", "type": ["null", "int"], "default": None},
            {"name": "release_date", "type": [
                "null", "string"], "default": None},
            {"name": "danceability", "type": "float", "default": 0.0},
            {"name": "energy", "type": "float", "default": 0.0},
            {"name": "key", "type": "int", "default": 0},
            {"name": "loudness", "type": "float", "default": 0.0},
            {"name": "mode", "type": "int", "default": 0},
            {"name": "speechiness", "type": "float", "default": 0.0},
            {"name": "acousticness", "type": "float", "default": 0.0},
            {"name": "instrumentalness", "type": "float", "default": 0.0},
            {"name": "liveness", "type": "float", "default": 0.0},
            {"name": "valence", "type": "float", "default": 0.0},
            {"name": "tempo", "type": "float", "default": 0.0},
            {"name": "time_signature", "type": "int", "default": 0},
            {"name": "album_name", "type": [
                "null", "string"], "default": None},
            {"name": "track_genre", "type": [
                "null", "string"], "default": None}
        ]
    }

    return parse_schema(track_schema)


def get_parsed_artist_schema():
    artist_schema = {
        "doc": "Spotify Wrapped Data Feed - Artist Info",
        "name": "Artist",
        "namespace": "com.spotify.wrapped",
        "type": "record",
        "fields": [
            {"name": "id", "type": "string"},
            {"name": "followers", "type": ["null", "float"], "default": None},
            {"name": "name", "type": ["null", "string"], "default": None},
            {"name": "popularity", "type": "int", "default": 0}
        ]
    }

    return parse_schema(artist_schema)


parsed_artist_schema = get_parsed_artist_schema()


def print_parsed_schemas():
    parsed_event_schema = get_parsed_event_schema()
    parsed_user_schema = get_parsed_user_schema()
    parsed_track_schema = get_parsed_track_schema()
    parsed_artist_schema = get_parsed_artist_schema()

    print("Parsed Event Schema:")
    print(parsed_event_schema)

    print("\nParsed User Schema:")
    print(parsed_user_schema)

    print("\nParsed Track Schema:")
    print(parsed_track_schema)


if __name__ == "__main__":
    print_parsed_schemas()
