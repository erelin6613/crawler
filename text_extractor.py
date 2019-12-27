import pandas as pd
from bs4 import BeautifulSoup
import re
import time
import requests
import pyap
from urllib.parse import urlparse
from selenium import webdriver
from shutil import which
from scrapy_selenium import SeleniumRequest
from address_parser import Parser
from selenium import webdriver
from shutil import which
from scrapy_selenium import SeleniumRequest

links = ['delivery_link', 'faq_link', 'privacy_link', 'return_link', 'terms_link', 'warranty_link']

database = pd.read_csv('/home/val/coding/scrapy_projects/trustpilot_base_one.csv')

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(executable_path = './chromedriver', options = options)


def text_validator(text):

	chars_to_remove = {"&": " and ", "'":"", "+ ": "plus", "#": "No", 
						"£": "pounds ", "\n": " ", "\r": " ", "\t": " ", "\"": ""}
	for char in chars_to_remove.keys():
		text.replace(char, chars_to_remove[char])

	return text



def extract_text(raw_html):

	soup = BeautifulSoup(raw_html, 'lxml')
	page_contents = ['pagecontent', 'page_contect', 'page-content',
						'PageContent', 'Page_Contect', 'Page-Content']
	contents = ['content', 'Contect', 'page-content']
	page_text = ''
	for class_ in page_contents:
		for tag in soup.find_all('div', class_=class_):
			page_text += tag.get_text().replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')

	if len(page_text) < 50:
		for class_ in page_contents:
			for tag in soup.find_all('div', id=class_):
				try:
					page_text += tag.text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
				except Exception:
					pass

	if len(page_text) < 50:
                for class_ in contents:
                    for tag in soup.find_all('div', class_=class_):
                        page_text += tag.get_text().replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')

	if len(page_text) < 50:
		for class_ in contents:
			for tag in soup.find_all('div', id=class_):
				try:
					page_text += tag.text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
				except Exception:
					pass

	return text_validator(page_text)

for each in links:
	urls = database[each]
	for url in urls:
		data_frame = pd.DataFrame()
		datapoint = {}
		driver.get(url)
		datapoint[each] = url
		field = each.split('_')[0]+'_text'
		datapoint[field] = extract_text(driver.page_source)
		data_frame = data_frame.append(datapoint, ignore_index=True)
		print(datapoint)
		data_frame.to_csv('trustpilot_{}.csv'.format(field), header=False, mode='a')


