#import scrapy
#import requests
#import urllib
#import urllib.error
#import io
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from time import gmtime, strftime

def getData(data_frame):
	link = data_frame['LinkOnBBB']
	driver.get(link)
	soup = BeautifulSoup(driver.page_source, 'lxml')
	name = soup.find('h4', class_ = 'dtm-business-name').text
	try:
		website = soup.find('div', class_ = 'styles__DivLayoutWithIcon-sc-47rb2e-0 eRLStY').a.get('href')
	except AttributeError:
		website = None
	try:
		phone = soup.find(class_ = 'dtm-phone').text
	except AttributeError:
		phone = None
	try:
		address = soup.find('div', class_ = 'dtm-address').text
	except AttributeError:
		address = None

	data_frame['Name'] = name
	data_frame['Website'] = website
	data_frame['Phone'] = phone
	data_frame['Address'] = address
	print(data_frame)

	return data_frame

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(executable_path='./chromedriver',options=options)

#new_df = pd.read_csv('USA-Zip.csv', dtype = 'object')
all_zips = pd.read_csv('USA-Zip.csv', dtype = 'object')
#all_zips = all_zips.dropna()
all_zips = all_zips.ix[:, 'Zip code']
all_zips = all_zips.drop_duplicates(keep = 'last')
print(all_zips)
#print(all_zips.columns)

error = []
error_no_res = []
page = 1
index = 0
restaurants_23 = pd.DataFrame(columns = ['LinkOnBBB'])
zip_count = 0

for each_zip in all_zips:
	each_zip = str(each_zip)
	if len(str(each_zip)) == 3:
		each_zip == '00' + str(each_zip)
	elif len(str(each_zip)) == 4:
		each_zip = '0' + str(each_zip)
	while True:
			link = 'https://www.bbb.org/search?find_country=USA&find_entity=50544-000&find_id=50544-000&find_loc={}&find_text=Restaurants&find_type=Category&page={}&sort=Relevance'.format(each_zip, page)
			driver.get(link)
			soup = BeautifulSoup(driver.page_source, 'lxml')
			error = soup.find_all('body', class_='error')
			error_no_res = soup.find_all('a', class_ = 'dtm-add-a-business')
			if len(error) > 0 or len(error_no_res) > 0:
				zip_count += 1
				print('Done with zip', each_zip)
				percent = 100*zip_count/(all_zips.shape[0])
				print(percent, '% done')
				print(strftime("%H:%M:%S", gmtime()))
				page = 1
				break
			print(driver.current_url)
			for elem in soup.find_all('a', class_='dtm-search-listing-business-name Name__Link-dpvfia-1 iyzkGZ'):
				print(elem.get('href'))
				print(strftime("%H:%M:%S", gmtime()))
				restaurants_23.loc[index, 'LinkOnBBB'] = elem.get('href')
				index += 1
			page += 1
			restaurants_23.to_csv('/home/val/restaurants_14_temp.csv')	#extra copy


restaurants_23.to_csv('/home/val/restaurants_14.csv')
#restaurants_23.drop_duplicates(subset = 'LinkOnBBB', inplace = True)
#print(restaurants_23)
#restaurants_23 = restaurants_23.apply(getData, axis = 1)
print(restaurants_23)

#restaurants_23.to_csv('/home/val/restaurants_df_24.csv')
