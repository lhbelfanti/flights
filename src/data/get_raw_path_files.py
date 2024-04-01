import os


def get_raw_path_files(source_path: str):
    path = os.path.join(os.path.dirname(__file__), source_path)
    folder = os.listdir(path)
    print(f'Retrieving csv files from {path}')
    flights_csv_paths = [f'{path}{file}' for file in folder]
    flights_csv_paths.sort()
    return flights_csv_paths
