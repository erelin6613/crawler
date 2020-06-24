import scrapy
import requests
import urllib
import urllib.error
import re
from bs4 import BeautifulSoup
import pickle

def download(url, retries=3):
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
		map_links.append(link.text)
	return map_links

#site = []
print(map_crawler('https://www.bbb.org/sitemap-us-categories-1.xml'))
pickle_out = open('pickle_map', 'wb')
pickle.dump(pickle_out, pickle_map)
pickle_out.close()
