import os
import pandas as pd
import numpy as np

from src.data import get_raw_path_files


def clean_flights_subset():
    flights_csv_paths = get_raw_path_files('raw/flights/')

    path = os.path.join(os.path.dirname(__file__), 'processed/flights/')

    for flights_csv_path in flights_csv_paths:
        print('Reading csv')
        df = pd.read_csv(flights_csv_path, index_col=None, header=0)

        # Divide FL_DATE column into 3 columns: DAY, MONTH and YEAR
        print('Divide FL_DATE column into 3 columns: DAY, MONTH and YEAR')
        df['FL_DATE'] = pd.to_datetime(df['FL_DATE'], format='%m/%d/%Y %I:%M:%S %p')
        df['DAY'] = df['FL_DATE'].dt.day
        df['MONTH'] = df['FL_DATE'].dt.month
        df['YEAR'] = df['FL_DATE'].dt.year

        # Translate 5 delay column into two: DELAY_REASON, DELAY
        print('Translate 5 delay column into two: DELAY_REASON, DELAY')
        delay_columns = ['CARRIER_DELAY', 'WEATHER_DELAY', 'NAS_DELAY', 'SECURITY_DELAY', 'LATE_AIRCRAFT_DELAY']
        df_filled = df[delay_columns].fillna(-np.inf)
        max_delay_values = df_filled.max(axis=1)
        delay_reasons = df_filled.idxmax(axis=1).str.replace('_DELAY', '').str.upper()
        df['DELAY'] = max_delay_values.replace(-np.inf, np.nan)
        delay_mapping = {'CARRIER': 1, 'WEATHER': 2, 'NAS': 3, 'SECURITY': 4, 'LATE_AIRCRAFT': 5}
        df['DELAY_REASON'] = delay_reasons.map(delay_mapping)
        df.loc[df['DELAY'].isnull(), 'DELAY_REASON'] = np.nan
        df['DELAY_REASON'] = df['DELAY_REASON'].astype('Int64')
        df['DELAY'] = df['DELAY'].astype('Int64')

        # Remove unused columns
        print('Remove unused columns')
        df.drop(['FL_DATE', 'OP_CARRIER_FL_NUM', 'ORIGIN_AIRPORT_ID', 'ORIGIN_CITY_NAME', 'ORIGIN_STATE_NM', 'ORIGIN_WAC', 'DEST_AIRPORT_ID', 'DEST_CITY_NAME', 'DEST_STATE_NM', 'DEST_WAC', 'CANCELLATION_CODE', 'CARRIER_DELAY', 'WEATHER_DELAY', 'NAS_DELAY', 'SECURITY_DELAY', 'LATE_AIRCRAFT_DELAY'], axis=1, inplace=True)

        # Reindex and rename columns
        desired_column_order = [
            'DAY', 'MONTH', 'YEAR', 'DAY_OF_WEEK', 'OP_UNIQUE_CARRIER', 'ORIGIN', 'DEST', 'CRS_DEP_TIME',
            'DEP_TIME', 'DEP_DELAY', 'TAXI_OUT', 'TAXI_IN', 'CRS_ARR_TIME', 'ARR_TIME', 'ARR_DELAY',
            'AIR_TIME', 'CANCELLED', 'DIVERTED', 'DELAY', 'DELAY_REASON'
        ]
        df = df.reindex(columns=desired_column_order)
        df.rename(columns={'OP_UNIQUE_CARRIER': 'CARRIER'}, inplace=True)

        # Save processed file
        filename = os.path.basename(flights_csv_path)
        print(f'Save processed file {path}{filename}')
        df.to_csv(f'{path}{filename}', index=False)


if __name__ == '__main__':
    clean_flights_subset()
