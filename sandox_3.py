import scrapy
#import requests
#import urllib
#import urllib.error
#import re
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

"""def download(url, retries=3):
	print('Downloading: ', url)
	try:
		html = urllib.request.urlopen(url).read()
	except urllib.error.URLError as error:
		print('Download error: ', error.reason)
		html = None
		if retries > 0:
			if hasattr (error, 'code') and 500 <= error.code < 600:
				return download(url, retries-1)
	return html

def map_crawler(url):
	sitemap = download(url)
	soup = BeautifulSoup(sitemap, 'lxml')
	map_links = []
	links = soup.find_all('loc')

	for link in links:
		#html = download(link)
		#print(link.text)
		map_links.append(link.text + '\n')
	return map_links"""

def getName (page_source):
	soup = BeautifulSoup(page_source, 'lxml')
	for elem in soup.find_all('h4', class_ = 'dtm-business-name'):
		Name = str(elem.renderContents())
		#Name = Name.replace('b"', '', 1)
		if 'b"' in Name:
			Name = Name.replace('b"', '')
			Name = Name.replace('"', '')
		if "b'" in Name:
			Name = Name.replace("b'", "")
			Name = Name.replace("'", "")
		#Name = Name.replace('"', '')
		#Name = Name.replace("'", ' ')
		#b"Lewis' Bar &amp; Grille"
		try:
			return Name.replace('&amp;', '&')
		except:
			return None

def getAdress (page_source):
	soup = BeautifulSoup(page_source, 'lxml')
	#print(soup)

	for elem in soup.find_all('div', class_ = 'dtm-address'): 
		try:
			return elem.text
		except:
			return None


def getWebSite (page_source):
	soup = BeautifulSoup(page_source, 'lxml')
	for elem in soup.find_all('div', class_ = 'styles__DivLayoutWithIcon-sc-47rb2e-0 eRLStY'):
		try:
			return elem.a.get('href')
		except:
			return None


def getPhone (page_source):
	soup = BeautifulSoup(page_source, 'lxml')
	for elem in soup.find_all('p', class_ = 'dtm-phone'):
		return elem.text


def Main():

	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	driver = webdriver.Chrome(executable_path='./chromedriver',options=options)

	restaurants_df = pd.DataFrame(columns = ['Index', 'Name', 'Subcategory', 'LinkOfSubcategory', 'LinkOnBBB', 'WebSite', 'Phone', 'Address'])
	restaurants_df.set_index('Index', inplace = True)
	index = 0
	error = []
	page = 1

	sub_restaurants = {50502: 'Pizza', 50138: 'Carter', 50278: 'Carry Out Food', 50544: 'Breakfast',
				60447: 'Hotels',30062: 'Food and Beverage Services', 50164: 'Coffee and Tea',
				80320: 'Foods', 50055: 'Banquet Facilities', 30790: 'Food Manufacturer',
				50423: 'Mexican Food', 50163:'Cocktail Bar', 85330:'Sports Bar', 
				72102: 'Pub Food', 50555: 'Sandwich', 44031:'Dessert', 50277: 'Food Delivery',
				50202: 'Delicatessen', 50362: 'Italian Food', 80619: 'Salad'}

	for key in sub_restaurants.keys():
		while True:
			link = 'https://www.bbb.org/search?filter_category={}-000&find_country=USA&find_entity=50544-000&find_id=4847_19000&find_text=Restaurants&find_type=Category&page={}&sort=Rating'.format(key, page)
			driver.get(link)
			soup = BeautifulSoup(driver.page_source, 'lxml')
			error = soup.find_all('body', class_='error')
			if len(error) > 0:
				print('Done with subcategory ', sub_restaurants[key])
				page = 1
			#link = None
			#print(urllib.error.reason)
				break
			print(driver.current_url)
			for elem in soup.find_all('a', class_='dtm-search-listing-business-name Name__Link-dpvfia-1 iyzkGZ'):
				print(elem.get('href'))
				restaurants_df.loc[index, 'LinkOfSubcategory'] = link
				bis_link = elem.get('href')
				driver.get(bis_link)
				restaurants_df.loc[index, 'LinkOnBBB'] = bis_link
				#page_source = driver.page_source
				restaurants_df.loc[index, 'WebSite'] = getWebSite(driver.page_source)
				restaurants_df.loc[index, 'Phone'] = getPhone(driver.page_source)
				restaurants_df.loc[index, 'Address'] = getAdress(driver.page_source)
				restaurants_df.loc[index, 'Name'] = getName(driver.page_source)
				restaurants_df.loc[index, 'Subcategory'] = sub_restaurants[key]
				error = soup.find_all('body', class_='error')
				if len(error) > 0:
					print('Done with subcategory ', sub_restaurants[key])
					page = 1
				print(restaurants_df.ix[index, :])

				restaurants_df.to_csv('/home/val/restaurants_df_2_1.csv')	#extra copy in case of crash
				index += 1
			page += 1

	restaurants_df.to_csv('/home/val/restaurants_df_2.2.csv')

if __name__ == '__main__':
	Main()
