from fastavro import reader
import pandas as pd


def read_avro(avro_path: str):
    with open(avro_path, "rb") as f:
        avro_reader = reader(f)
        df = pd.DataFrame(avro_reader)

    return df


def save_to_csv(df, file_path):
    df.to_csv(file_path, index=False)

def get_n_long_sessions():
    n = random.randint(0, 100)
    if n < 2:
        return 3
    elif n <10:
        return 0
    elif n <50:
        return 1
    else:
        return 2
    

def get_n_short_sessions():
    return int(np.random.normal(loc=5, scale=1))


def get_sessions(user, n_long_sessions:int, n_short_sessions:int):
    sessions = []
    for _ in range(n_long_sessions):
        session = Session(user=user, type="long")
        session.simulate_session()
        sessions.append(session)
    for _ in range(n_short_sessions):
        session = Session(user=user, type="short")
        session.simulate_session()
        sessions.append(session)

    return sessions


def allocate_sessions(sessions:list):
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
        for slot in range(24):
            if all(slots_availability[i] for i in range(slot, slot + n_slots)):
                session_schedule[session] = slot
                for i in range(slot, slot + n_slots):
                    slots_availability[i] = False
                break
            print(f"Could not find a slot for {session}")

    return session_schedule
