import pandas as pd

from src.data import get_raw_path_files


def inspect_flights_subset():
    flights_csv_paths = get_raw_path_files('raw/flights/')

    for flights_csv_path in flights_csv_paths:
        df = pd.read_csv(flights_csv_path, index_col=None, header=0)
        unique = df['OP_UNIQUE_CARRIER'].unique()
        origin = df['ORIGIN'].unique()
        print(f'{flights_csv_path} unique values: {unique}')
        print(f'{flights_csv_path} origin values: {origin}')


if __name__ == '__main__':
    inspect_flights_subset()
