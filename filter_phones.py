import pandas as pd

data_set = pd.read_csv('/home/val/insurance.csv')

data_set_phones = data_set.duplicated(subset=['Phone'])

#data_set_phones = data_set.(data_set[len(data_set.Phone) > 0].index)

#data.loc[data[‘id’] == 9] == data[data[‘id’] == 9] .
#data_set_phones = data_set.loc[len(data_set['Phone']) > 0]
#data_set = data_set.drop_duplicates(subset = 'Phone', keep = 'last')
#data_set = data_set.dropna(how = 'all')
print(data_set_phones.tail(50))
print(data_set_phones.shape)
print(type(data_set))
#data_set.to_csv('/home/val/house_cleaners_1.csv')
