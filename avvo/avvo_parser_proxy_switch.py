import os
import sys
from threading import Thread
from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from time import gmtime, strftime, sleep
import pandas as pd
import time
import re
from queue import Queue
from fake_useragent import UserAgent
from tqdm import tqdm
import usaddress

ua = UserAgent()
ua_list = [ua.ie, ua.msie, ua.chrome, ua.google, 
			ua.firefox, ua.ff, ua.safari]
blacklist = ['youtube', 'facebook', 'linkedin',
			'internetbrands', 'twitter', 'pinterest',
			'avvo']
not_active = 'This attorney is not active on Avvo.'
pseudomin = 'also known as'

classes = {'phone': 'js-v-phone-replace-text', 
			'address': 'js-context js-address col-xs-12'}
website_regex = r'www\.[0-9a-zA-Z]*\.[a-zA-Z]{2,3}'

link = 'https://www.avvo.com/attorneys/10020-ny-timothy-plunkett-1787474.html'

def get_city_state(string):

	address = usaddress.parse(string)

	str_num, zip_code = None, None
	state, city, street = '', '', ''

	for tup in address:
		if tup[1] == 'StateName':
			state += tup[0]+' '
		if tup[1] == 'PlaceName':
			city += tup[0]+' '
		if tup[1] == 'AddressNumber':
			street = tup[0] + ' '
		if tup[1] == 'OccupancyIdentifier':
			str_num = tup[0]
		if tup[1] == 'StreetNamePreType':
			street += tup[0]+' '
		if tup[1] == 'StreetName':
			street += tup[0]+' '
		if tup[1] == 'ZipCode':
			zip_code = tup[0]
	try:
		assert len(zip_code.split('-')) > 1
		zip_code = zip_code.split('-')[0]
	except Exception:
		pass

	return (street, str_num, city, state, zip_code)


def scarpe_info(link, fake_user=None):

	info = dict()
	options = webdriver.ChromeOptions()
	
	if not fake_user:
		fake_user = ua.safari
	options.add_argument("user-agent={fake_user}")

	options.add_argument('headless')
	options.add_argument('no-gpu')
	driver = webdriver.Chrome(executable_path = './chromedriver', options = options) 
	driver.execute_script("return navigator.userAgent")

	try:
		driver.get(link+'#contact') #headers={'User-Agent': ua})
	except Exception as e:
		print('Link raised exaption:', link, ':', e)
		driver.close()
		driver.quit()
		return None
	try:
		info['url'] = link
		soup = BeautifulSoup(driver.page_source, 'lxml')
		for script in soup(["script", "style"]):
			script.extract()
		if not_active in soup.get_text():
			driver.close()
			driver.quit()
			return False
			
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
		if info['address']:
			addr_str = ''
			for each in info['address']:
				try:
					addr_str += each.get_text()+' '
				except Exception:
					pass
			info['address'] = addr_str
			try:
				info['street'], info['streetnumber'], info['city'], \
				info['state'], info['zip_code'] = get_city_state(addr_str)
			except Exception as e:
				print(e)
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

			try:
				assert len(info['phone']) > 0
			except Exception:
				info['phone'] = None
				info['fax'] = None
		if pseudomin in soup.get_text():
			try:
				info['pseudomin'] = soup.find(attrs={'itemprop': 'alternatename'}).get_text()
			except Exception as e:
				print(e)
		else:
			info['pseudomin'] = None

		for each in soup.find_all(class_='profile-card'):
			for link in each.find_all(class_='text-truncate'):
				try:
					if link.text.split('.')[-2] in ''.join(blacklist):
						continue
					else:
						info['website'] = link.text
						break
				except Exception as e:
					pass
		try:
			assert len(info['website']) > 0
		except Exception as e:
			info['website'] = None
		driver.close()
		driver.quit()
		return info
	except Exception as e:
		print('Link does not exist:', link, e)
		if driver:
			driver.close()
			driver.quit()

def scrape_all(link, filename):
	info = scarpe_info(link, ua_list[-3])
	if info == False:
		return
	if info:
		count_nans = len([x for x in info.values() if x is None])
		if info['name'] == 'One more step':
			print('seems like we are blocked')
			with open('proxies.txt', 'w+') as file:
				proxies = file.readlines()
				os.system(f'export http_proxy={proxies[0]}')
				os.system(f'export https_proxy={proxies[0]}')
				os.system(f'export ftp_proxy={proxies[0]}')
				os.system(f'echo "http_proxy={proxies[0]}\n\
							https_proxy={proxies[0]}\n\
							ftp_proxy={proxies[0]}" >> /etc/environment')
				file.write(proxies[1:])
				os.system('sudo reboot')
			#exit()
			return
		df = pd.DataFrame()
		df = df.append(info, ignore_index=True)
		df.to_csv(filename.split('.')[0]+'_results_extended.csv', mode='a', header=False)

if __name__ == '__main__':

	filename = 'avvo_profiles_1.csv'
	df = pd.read_csv(filename)
	results = pd.DataFrame()

	q = [link for link in df['url']]
	print(filename)

	threads_amount = 2

	for each in tqdm(q):
		scrape_all(each, filename)
"""
	while len(q) > 0:
		threads = []
		for i in range(threads_amount):
			#print(filename)
			print('scraping:', q[0])
			t = Thread(target = scrape_all, args=(q[0], filename))
			del q[0]
			#print('thread ', i, ' has been created')
			#frame.drop
			threads.append(t)
			t.start()

		for t in threads:
			t.join()
			#sleep(30)
		print(len(q), ' links to go')
"""