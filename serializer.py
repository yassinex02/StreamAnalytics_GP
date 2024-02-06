from fastavro import parse_schema


def main():
    event_schema = {
        "doc": "Spotify Wrapped Data Feed - User Event",
        "name": "UserEvent",
        "namespace": "com.spotify.wrapped",
        "type": "record",
        "fields": [
            {"name": "id", "type": "long"},
            {"name": "timestamp", "type": "string",
             "logicalType": "timestamp-millis"},
            {"name": "action",
             "type": {
                 "type": "enum",
                 "name": "event",
                 "symbols": [
                     "PLAY", "PAUSE", "SKIP"
                 ]},
                "default": "PLAY"},
            {"name": "track_id", "type": "long"},
            {"name": "user_id", "type": "long"}
        ]
    }

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
            {"name": "gender", "type": "string", "symbols": ["M", "F", "O"]},
            {"name": "favorite_genre", "type": {
                "type": "array", "items": "string"}, "default": []}
        ]
    }

    track_schema = {
        "doc": "Spotify Wrapped Data Feed - Track Info",
        "name": "Track",
        "namespace": "com.spotify.wrapped",
        "type": "record",
        "fields": [
            {"name": "track_id", "type": "long"},
            {"name": "duration", "type": "int"},  # (in seconds)
            {"name": "artist", "type": "string"},
            {"name": "genre", "type": "string"}
        ]
    }

    parsed_event_schema = parse_schema(event_schema)
    parsed_user_schema = parse_schema(user_schema)
    parsed_track_schema = parse_schema(track_schema)

    print(parsed_event_schema)
    print(parsed_user_schema)
    print(parsed_track_schema)


if __name__ == "__main__":
    main()
