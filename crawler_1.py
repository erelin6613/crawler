import scrapy
import requests
import urllib
import urllib.error
import re
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

restaurants = pd.read_csv('RestaurantsSubCat.csv')
#links = open('RestaurantsSubCat.csv', 'r')
"""print(type(restaurants))
print(restaurants.head(5))
print(restaurants.tail(5))"""
restaurants_df = pd.DataFrame(columns = ['Name','LinkOfSubcategory', 'LinkOnBBB', 'WebSite', 'Phone', 'Address'])
#restaurants.set_columns = ['LinkOf(Sub)Category']
print(restaurants.columns)
print('ok\n')
index = 1
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(chrome_options=options, executable_path=r'/home/val/chromedriver')

for link in restaurants.loc[:, 'LinkOf(Sub)Category']:

	#print('+1')
	#html_page = urllib.request.urlopen(link)
	driver.get(link)
	print(link)
	#source = requests.get('https://www.bbb.org/us/category/restaurants')
	soup = BeautifulSoup(driver.page_source, 'lxml')
	error = soup.find_all('body', class_='error')
	if len(error) > 0:
		print('Done with the link')
			#link = None
			#print(urllib.error.reason)
		break
	#print(soup.prettify())
	#break
	#print(soup)
	for elem in soup.find_all('a', class_='dtm-search-listing-business-name Name__Link-dpvfia-1 iyzkGZ'):
		print(elem.get('href'))
		restaurants_df.loc[index, 'LinkOfSubcategory'] = link
		restaurants_df.loc[index, 'LinkOnBBB'] = elem.get('href')
		index += 1
	#for elem in soup.find_all('a', class_='dtm-search-listing-business-name'):
	#for el in soup.findAll('h3'):
		#print(el.a.get('href'))
		#print($x('//div[contains(@class,"styles__DivLayoutWithIcon-sc-47rb2e-0")]'))
		#print('The link: ', elem.get('href'))
	print(restaurants_df)

restaurants_df = restaurants_df.drop_duplicates(subset = 'LinkOnBBB', keep = False, inplace = True) 

restaurants_df.to_csv('restaurants_df.csv')
print('Done with the set')
#biz_name = elem.a
#print(biz)
#print(type(biz_name))