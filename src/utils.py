from fastavro import reader
import pandas as pd


def read_avro(avro_path: str):
    with open(avro_path, "rb") as f:
        avro_reader = reader(f)
        df = pd.DataFrame(avro_reader)

    return df


def save_to_csv(df, file_path):
    df.to_csv(file_path, index=False)