from fastavro import reader
import pandas as pd


def read_avro(avro_path:str):
    with open(avro_path, "rb") as f:
        avro_reader = reader(f)
        df = pd.DataFrame(avro_reader)

    return df