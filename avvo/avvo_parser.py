import os
import sys
from threading import Thread
from bs4 import BeautifulSoup
#import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.proxy import *
from time import gmtime, strftime, sleep
import pandas as pd
#import sqlite3
import time
import re
from queue import Queue
from fake_useragent import UserAgent

ua = UserAgent()

ua_list = [ua.ie, ua.msie, ua.chrome, ua.google, 
			ua.firefox, ua.ff, ua.safari]

#ua = UserAgent(family='chrome')
#print(ua.family)

blacklist = ['youtube', 'facebook', 'linkedin',
			'internetbrands', 'twitter', 'pinterest',
			'avvo']

not_active = 'This attorney is not active on Avvo.'
pseudomin = 'also known as'

classes = {'phone': 'js-v-phone-replace-text', 
			'address': 'js-context js-address col-xs-12'}

website_regex = r'www\.[0-9a-zA-Z]*\.[a-zA-Z]{2,3}'


#link = 'https://www.avvo.com/attorneys/60606-il-thomas-hyland-4258221.html'
#options = webdriver.ChromeOptions()
#options.add_argument('headless')
#driver = webdriver.Chrome(executable_path = './chromedriver', options = options)

info = dict()

def scarpe_info(link, fake_user=None):

	options = webdriver.ChromeOptions()
	
	if not fake_user:
		fake_user = ua.safari
	#fake_user = 'Opera/9.80 (X11; Linux i686; U; ru) Presto/2.8.131 Version/11.11'
	#fake_user = 'Chrome/42.0.2311.135'
	#fake_user = ua['google chrome']
	#print(fake_user)
	options.add_argument("user-agent={fake_user}")

	options.add_argument('headless')
	driver = webdriver.Chrome(executable_path = './chromedriver', options = options)
	driver.execute_script("return navigator.userAgent")

	try:
		driver.get(link+'#contact') #headers={'User-Agent': ua})

		#r = requests.get(link+'#contact', headers={'User-Agent': str(ua.family[0])})
		#print(r.status_code)
	except Exception as e:
		print('Link raised exaption:', link, ':', e)
		#print('raw html')
		driver.quit()
		return None
	try:
		info['url'] = link
		soup = BeautifulSoup(driver.page_source, 'lxml')
		for script in soup(["script", "style"]):
			script.extract()
		if not_active in soup.get_text():
			info['active'] = 0
		else:
			info['active'] = 1
		info['name'] = soup.find('h1').get_text()
		try:
			info['phone'] = soup.find(attrs={'class': 'hidden', 'itemprop': 'telephone'}).get_text()
		except Exception:
			pass
		try:
			info['fax'] = soup.find(attrs={'class': 'hidden', 'itemprop': 'faxNumber'}).get_text()
		except Exception:
			info['fax'] = None
		try:
			info['address'] = soup.find(attrs={'class': 'hidden', 'itemprop': 'address'})
		except Exception:
			info['address'] = None
		try:
			info['company_name'] = info['address'].find(attrs={'itemprop':'name'}).get_text()
		except Exception:
			info['company_name'] = None
		#info['address'] = info['address'].get_text()
		if info['address']:
			addr_str = ''
			for each in info['address']:
				try:
					addr_str += each.get_text()+' '
				except Exception:
					pass
			info['address'] = addr_str
		try:
			assert len(info['phone'])>0
		except Exception:
			phones = soup.find_all(class_=classes['phone'])
			if phones:
				if len(phones) > 1:
					info['phone'] = phones[0].get_text()
					info['fax'] = phones[2].get_text()
				else:
					info['phone'] = phones[0].get_text()
					info['phone'] = None

			if not info['phone']:
				info['phone'] = None
				info['fax'] = None
		if pseudomin in soup.get_text():
			try:
				info['pseudomin'] = soup.find(attrs={'itemprop': 'alternatename'}).get_text()
			except Exception as e:
				print(e)
		else:
			info['pseudomin'] = None

		for each in soup.find_all('a'):
			try:
				site = re.search(website_regex, each.get('href'))
				if site:
					site = site.group(0)
					if site.split('.')[1] in blacklist:
						continue
					info['website'] = site

			except Exception as e:
				pass
		try:
			assert len(info['website']) > 0
		except Exception as e:
			info['website'] = None
		#print(info)
		driver.quit()
		return info
	except Exception:
		#print('Raw source: \n', driver.page_source)
		print('Link does not exist:', link)

def scrape_all(link, filename):
	info = scarpe_info(link, ua_list[-1])
	#info['url'] = link
	if info:
		if info['name'] == 'One more step':
			print('well we are blocked')
			#del ua_list[0]
			exit()
		df = pd.DataFrame()
		df = df.append(info, ignore_index=True)
		#count_nans = [x for x in info.values() if x is None]
		#if len(count_nans) > 
		print(df.tail())
		df.to_csv(filename.split('.')[0]+'_results.csv', mode='a', header=False)
	#return df

if __name__ == '__main__':
	filename = 'avvo_profiles_2.csv'
	df = pd.read_csv(filename)
	results = pd.DataFrame()
	#for each in df['url']:
		#results = results.append(scarpe_info(each), ignore_index=True)
		#print(results.tail())
	#results.to_csv(filename[:-4]+'results'+'.csv')

	threads_amount = 2

	q = [link for link in df['url']]

	while len(q) > 0:
		threads = []
		for i in range(threads_amount):
			#print(filename)
			t = Thread(target = scrape_all, args=(q[0], filename))
			print('scraping:', q[0])
			del q[0]
			#print('thread ', i, ' has been created')
			#frame.drop
			threads.append(t)
			t.start()
		for t in threads:
			t.join()
			#sleep(30)
		print(len(q), ' links to go')