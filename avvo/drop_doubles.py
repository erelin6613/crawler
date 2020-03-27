import pandas as pd

filename = 'avvo_profiles_2_results.csv'
frame = pd.read_csv(filename)
frame = frame.drop_duplicates(subset='url', keep='last')
print(frame)
frame.to_csv(filename)
