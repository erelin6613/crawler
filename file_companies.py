#from threading import Thread
from bs4 import BeautifulSoup
import pandas as pd
#import os
#import sys
from selenium import webdriver
#from selenium.webdriver.common.proxy import *
from time import gmtime, strftime, sleep
#import sqlite3
#from queue import Queue
#import re
import requests

cities_frame = pd.read_html('https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population')
cities = cities_frame[4]
print(cities)
abbrs = { 'Alaska':	'AK', 'Alabama': 'AL', 'Arkansas': 'AR', 'Arizona': 'AZ', 'California': 'CA', 
			'Colorado': 'CO', 'Connecticut': 'CT', 'District of Columbia': 'DC', 'Delaware': 'DE', 
			'Florida': 'FL', 'Georgia': 'GA', 'Iowa': 'IA', 'Idaho':	'ID', 
			'Illinois': 'IL', 'Indiana': 'IN', 'Kansas': 'KS', 'Kentucky': 'KY', 
			'Louisiana': 'LA', 'Massachusetts': 'MA', 'Maryland':	'MD', 'Maine': 'ME', 
			'Michigan': 'MI', 'Minnesota': 'MN', 'Missouri': 'MO', 'Mississippi': 'MS',
			'Montana': 'MT', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Nebraska': 'NE', 
			'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'Nevada': 'NV', 
			'New York': 'NY', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR',
			'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 
			'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Virginia': 'VA', 
			'Vermont': 'VT', 'Washington': 'WA', 'Wisconsin': 'WI', 'West Virginia': 'WV',
			'Wyoming': 'WY'}

states = pd.read_csv('/home/val/coding/USA-states-cities.csv')
#print(cities)
cities_list = pd.DataFrame()




def crawling(search_url, file_name):

	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	driver = webdriver.Chrome(executable_path = './chromedriver', options = options)
	links = open(file_name, 'a')
	driver.get(search_url)
	print(search_url)
	for i in range(20):
		soup = BeautifulSoup(driver.page_source, 'lxml')
		for each in soup.find_all(class_='iUh30 bc'):
			try:
				print(each.text.split(' ')[0])
				links.write(each.text.split(' ')[0]+'\n')
			except Exception:
				print(each.text)
				links.write(each.text+'\n')
		try:
			driver.find_element_by_class_name('pn').click()
		except Exception:
			return
		print('--------')
		i += 1
		sleep(3)

	links.close()

#print(cities_list)





websites_frame = pd.DataFrame(columns=['state', 'city', 'link'])
#states = states.drop_duplicates(zip('City', 'Abbreviation'))

for i in range(len(cities)):
#	print(states.loc[i]['City'])
#	print(states.loc[i]['City'])
	try:
		city = cities.loc[i]['City'].split('[')[0]
	except Exception:
		city = cities.loc[i]['City']
	try:
		state = abbrs[str(cities.loc[i]['State[c]'])]
	except Exception:
		continue
	search_url = f'https://www.google.com/search?q=File+a+complaint+{state}+{city}'
	#print('-----', search_url, '-----')
	try:
		state = str(cities.loc[i]['State[c]']).strip()
	except Exception:
		continue
	crawling(search_url, 'file_companies_sites.csv')
	search_url = f'https://www.google.com/search?q=File+a+complaint+{state}+{city}+attorney+general'
	crawling(search_url, 'file_companies_sites.csv')
	search_url = f'https://www.google.com/search?q=local+state+agencies+{state}+{city}'
	crawling(search_url, 'local_agencies.csv')
	search_url = f'https://www.google.com/search?q=consumer+protection+{state}+{city}'
	crawling(search_url, 'file_companies_sites.csv')


