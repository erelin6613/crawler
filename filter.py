import pandas as pd

#data_set = pd.read_csv('/home/val/parsed_links.csv')
#data_set = pd.read_csv('/home/val/links_to_parse.csv')
#data_set = pd.read_csv('/home/val/HomeAdvisor.csv')
#data_set = pd.read_csv('/home/val/homeflock_profiles.csv')
data_set = pd.read_csv('/home/val/test-homeflock-1.csv')
data_set = data_set.drop_duplicates(subset = 'LinkOnPlatform', keep = 'last')
#data_set = data_set.drop_duplicates(keep = 'last')
#data_set = data_set.dropna(how = 'all')
print(data_set)
print(data_set.shape)
#print(type(data_set))
#data_set.to_csv('parsed_links.csv')
#data_set.to_csv('links_to_parse.csv')
#data_set.to_csv('HomeAdvisor.csv')
#data_set.to_csv('homeflock_profiles.csv')
data_set.to_csv('/home/val/test-homeflock-1.csv')
