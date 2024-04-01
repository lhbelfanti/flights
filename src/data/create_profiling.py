import os
import pandas as pd
from ydata_profiling import ProfileReport

if __name__ == '__main__':

	print(f'list dir', os.listdir())

	files = [item for item in os.listdir('raw') if item.find('.csv') > 0]

	print(f'Files loaded {files}')

	for file in files:
		print(f'Opening file: {file}')
		df = pd.read_csv(f'raw/{file}', sep=',')
		file = file.replace('.csv', '')
		profile = ProfileReport(df, title="Profiling Report: {file} table")
		profile.to_file(output_file=f"profiling_{file}.html")
		profile.to_file(output_file=f"profiling_{file}.json")
