import pandas as pd

filename = 'avvo_profiles_1_results_extended.csv'
frame = pd.read_csv(filename)
frame = frame.drop_duplicates(subset='url', keep='last')
print(frame)
frame.to_csv(filename)
