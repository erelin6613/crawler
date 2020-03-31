from avvo_parser import get_city_state
import pandas as pd

frame = pd.read_csv('avvo_profiles_1_results.csv')

for i in frame.index:
	try:
		frame.loc[i, 'street'], frame.loc[i, 'streetnumber'], \
		frame.loc[i, 'city'], frame.loc[i, 'state'], \
		frame.loc[i, 'zip_code'] = get_city_state(frame.loc[i, 'address'])
	except Exception as e:
		print(e)

print(frame)
frame.to_csv('temp_file.csv')