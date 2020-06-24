import json
import pandas as pd
from bs4 import BeautifulSoup
import re
import time
import requests
import xml.etree.ElementTree as etree
import pyap
from urllib.parse import urlparse
from selenium import webdriver
import requests
from shutil import which
import os
import xml.etree.ElementTree as ET
from lxml import etree



parser = etree.XMLParser(recover=True)

data_frame = pd.DataFrame()

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(executable_path = './chromedriver', options = options)

data_base = pd.read_csv('/home/val/coding/scrapy_projects/companies_competitors.csv', encoding = 'unicode_escape')
columns = data_base.columns

def replace_numbers(string):
    numbers = { 'hundred': 100, 'ninety':90, 'eighty': 80, 'seventy': 70, 'sixty': 60, 'fifty': 50, 'forty': 40, 
                'thirty': 30, 'twenty': 20, 'ten': 10, 'nine': 9, 'eight': 8, 'seven': 7, 'six': 6, 'five': 5, 
                'four': 4, 'three': 3, 'two': 2, 'one': 1, 'zero': 0}

    for key in numbers.keys():
        try:
            if key in string:
                string.replace(key, numbers[key])
        except Exception:
            pass

    return string

def numerize_string(string):
    num_string = ''
    nums_in_phone = 0
    #allowed_sym = 
    #article = soup.find('article')
    for character in string:
        if character.isalpha() == False:
            num_string += character
        if character.isnumeric() == True:
            nums_in_phone += 1
    if nums_in_phone > 6 and nums_in_phone <11:
        return num_string
    else:
        return None

def links_to_scrape():
	return [link for link in data_base['url']]

def parse(response, current_url, status_code):
	frame = {}
	internal_links = {'contact_link': r'contact.*', 
						'privacy_link': r'privacy.*policy', 
						'delivery_link': r'(deliver|ship).*(policy)*', 
						'terms_link': r'term.*(condition|use|service)', 
						'faq_link': r'(faq)|(frequently.*asked.*question)', 
						'return_link': r'return.*', 
						'warranty_link': r'(warrant)|(certif)|(guarant)'}
	
	external_links = {'twitter': 'twitter.com', 
						'facebook': 'facebook.com',
						'linkedin': 'linkedin.com',
						'instagram': 'instagram.com',
						'pinterest':'pinterest.com', 
						'youtube': 'youtube.com',
						'linkedin': 'linkedin.com'}

	def find_phones(response, contact_link, retries=0):
		#r = requests.get(contact_link)
		soup = BeautifulSoup(response, 'lxml')
		for script in soup(["script", "style"]):
			script.extract()
			text = soup.get_text().split('\n')
			phones = []
			i=0
			for item in text:
				if len(item) <=1:
					continue
				phone_numbers = re.findall(r"([\+, \(, \), \-, \_, 0-9]{,20})", item)
				phone_numbers_text = re.findall(r"([\+, \(, \), \-, \_, 0-9]{,20}-[a-z, A-Z]{3,5})", item)
				phone_numbers = phone_numbers + phone_numbers_text
				if item.__contains__('@'):
					phones.append(['@', item])
				if len(phone_numbers) == 0:
					continue
				selected = []
				for phone in phone_numbers:
					tmp = phone.replace(' ','').replace('(', '').replace(')', '').replace('-','').replace('_', '')
					if len(tmp)>=7:
						selected.append(phone)

				if len(selected) > 0:
					phones.append(selected + [item])
				i+=1
			for each in phones:
				for i in range(len(each)):
					each[i] = numerize_string(replace_numbers(each[i]))
			phone_list = ''
			for dim in phones:
				for num in dim:
					try:
						if sum(c.isdigit() for c in num) > 6 and sum(c.isdigit() for c in num) < 11:
							phone_list = phone_list+num+'\n'
					except Exception:
						pass
			try:
				assert len(contact_link) > 0
				#retries = 0
				if len(phone_list) == 0 and retries == 0:
					retries+=1
					phone_list = find_phones(requests.get(contact_link).text, contact_link=None, retries=retries)					
				if len(phone_list) == 0 and retries == 1:
					phone_list = find_phones(driver.get(contact_link).page_source, contact_link=None, retries=retries)
			except Exception:
				pass

			return phone_list

	def find_address(response, contact_link, retries=0):
			soup = BeautifulSoup(response, 'lxml')
			for script in soup(["script", "style"]):
				script.extract()

			try:
				address = str(pyap.parse(soup.text, country='US')[0])
			except Exception as e:
				address = None
			try:
				assert len(contact_link) > 0
				#retries = 0
				if len(address) == 0 and retries == 0:
					retries+=1
					address = find_address(requests.get(contact_link).text, contact_link=None, retries=retries)					
				if len(address) == 0 and retries == 1:
					retries+=1
					address = find_address(driver.get(contact_link).page_source, contact_link=None, retries=retries)
			except Exception:
				pass
	
	def find_email(response, contact_link, retries=0):
		email_pattern = '[A-Za-z0-9]*@{1}[A-Za-z0-9]*\.(com|org|de|edu|gov|uk){1}'
		soup = BeautifulSoup(response, 'lxml')
		for script in soup(["script", "style"]):
			script.extract()
		for each in soup.get_text().split('\n'):
			try:
				email_re = re.search(email_pattern, each)
				if len(email_re.group(0)) > 5 and len(email_re.group(0)) < 75:
					email = email_re.group(0)

			except Exception as e:
				try:
					assert len(contact_link) > 0
					if len(email) == 0 and retries == 0:
						retries+=1
						email = find_email(requests.get(contact_link).text, contact_link=None, retries=retries)					
						if len(email) == 0 and retries == 1:
							retries+=1
							email = find_email(driver.get(contact_link).page_source, contact_link=None, retries=retries)
				except Exception:
					pass
	def validate_link(link, current_url):
		discovered_bugs = {'/#/': '/', '.com/@': '.com/', '.org/@': '.org/','.edu/@': '.edu/', 
							'.uk/@': '.uk/', '.com#': '.com/', '.org#': '.org/', 
							'.edu#': '.edu/', '.uk#': '.uk/', '.com//': '.com/', 
							'.org//': '.org/', '.edu//': '.edu/', '.uk//': '.uk/'}
		if link.startswith('https://') == True or link.startswith('http://') == True or link.startswith('www.') == True:
			return link
		else:
			if link.startswith('/') == True:
				return current_url+link.replace('/', '')
			for bug in discovered_bugs.keys():
				if bug in link:
					link = link.replace(bug, discovered_bugs[bug])

			return link

	def find_links(response, contact_link):
		#r = requests.get(link)
		links = {}
		soup = BeautifulSoup(response, 'lxml')
		for each in soup.find_all('a'):
			for ext_key, ext_val in external_links.items():
				if ext_val in str(each.get('href')):
					links[ext_key] = validate_link(str(each.get('href')), current_url)
			for int_key, int_val in internal_links.items():
				try:
					url = re.findall(int_val, each.get('href'))
					if len(url) > 0:
						links[int_key] = validate_link(str(each.get('href')), current_url)
				except Exception as e:
					pass
		for ext_key, ext_val in external_links.items():
			try:
				assert len(links[ext_key]) > 0
			except Exception:
				links[ext_key] = None
		for int_key, int_val in internal_links.items():
			try:
				assert len(links[int_val]) > 0
			except Exception:
				links[int_key] = None

		return links
	print(status_code, '---', current_url)
	if status_code == 200:
		soup = BeautifulSoup(response, 'lxml')
		#root = etree.fromstring(response, parser=parser)
		#re_contact = re.compile(r'.+?contact.+?')
		for url in soup.find_all('a'):
			#print(url)
		#.re(r'.+?contact.+?'):
			urls = re.match(r'.+?contact.+?', str(url.get('href')))
			try:
				#print(urls.group(0))
				if str(urls.group(0)).__contains__('http'):
					contact_link = validate_link(urls.group(0), current_url)
				else:
					if str(urls.group(0)).startswith('/'):
						contact_link = current_url+str(urls.group(0))[1:]
					else:
						contact_link = current_url+str(urls.group(0))
				print(contact_link)
			except Exception:
				pass
			try:
				assert len(contact_link) > 0
			except Exception:
				contact_link = ''
		frame['url'] = current_url
		print(current_url)
		print(contact_link)
		try:
			frame['phones'] = find_phones(response, contact_link)
		except Exception:
			frame['phones'] = find_phones(response, current_url)
		try:
			frame['address'] = find_address(response, contact_link)
		except Exception:
			frame['address'] = find_address(response, current_url)
		try:
			frame['email'] = find_email(response, contact_link)
		except Exception:
			frame['email'] = find_email(response, current_url)
		try:
			frame['facebook'] = find_links(response, contact_link)['facebook']
		except Exception:
			frame['facebook'] = find_links(response, current_url)['facebook']
		try:
			frame['instagram'] = find_links(response, contact_link)['instagram']
		except Exception:
			frame['instagram'] = find_links(response, current_url)['instagram']
		try:
			frame['pinterest'] = find_links(response, contact_link)['pinterest']
		except Exception:
			frame['pinterest'] = find_links(response, current_url)['pinterest']
		try:
			frame['linkedin'] = find_links(response, contact_link)['linkedin']
		except Exception:
			frame['linkedin'] = find_links(response, current_url)['linkedin']
		try:
			frame['youtube'] = find_links(response, contact_link)['youtube']
		except Exception:
			frame['youtube'] = find_links(response, current_url)['youtube']
		try:
			frame['twitter'] = find_links(response, contact_link)['twitter']
		except Exception:
			frame['twitter'] = find_links(response, current_url)['twitter']
		try:
			try:
				if len(contact_link) > 0:
					frame['contact_link'] = contact_link
			except Exception:
				frame['contact_link'] = find_links(response, contact_link)['contact_link']
		except Exception:
			frame['contact_link'] = find_links(response, current_url)['contact_link']
		try:
			frame['faq_link'] = find_links(response, contact_link)['faq_link']
		except Exception:
			frame['faq_link'] = find_links(response, current_url)['faq_link']
		try:
			frame['privacy_link'] = find_links(response, contact_link)['privacy_link']
		except Exception:
			frame['privacy_link'] = find_links(response, current_url)['privacy_link']
		try:
			frame['delivery_link'] = find_links(response, contact_link)['delivery_link']
		except Exception:
			frame['delivery_link'] = find_links(response, current_url)['delivery_link']
		try:
			frame['terms_link'] = find_links(response, contact_link)['terms_link']
		except Exception:
			frame['terms_link'] = find_links(response, current_url)['terms_link']
		try:
			frame['return_link'] = find_links(response, contact_link)['return_link']
		except Exception:
			frame['return_link'] = find_links(response, current_url)['return_link']
		try:
			frame['warranty_link'] = find_links(response, contact_link)['warranty_link']
		except Exception:
			frame['warranty_link'] = find_links(response, current_url)['warranty_link']

	else:
		try:
			parse(driver.get(response.url).page_source, driver.get(response.url).current_url)
		except Exception:
			frame['url'] = current_url
			frame['phones'] = None
			frame['address'] = None
			frame['email'] = None
			frame['facebook'] = None
			frame['instagram'] = None
			frame['pinterest'] = None
			frame['linkedin'] = None
			frame['youtube'] = None
			frame['twitter'] = None
			frame['contact_link'] = None
			frame['faq_link'] = None
			frame['privacy_link'] = None
			frame['delivery_link'] = None
			frame['terms_link'] = None
			frame['return_link'] = None
			frame['warranty_link'] = None

	parse_internal_links(frame)


        #print(frame)
        #data_frame = data_frame.append(frame, ignore_index=True)
        #data_frame.to_csv('companies_v2.csv')


########## parse #2
def parse_internal_links(frame):
	data_frame = pd.DataFrame()
	def text_validator(text):
		chars_to_remove = {"&": " and ", "'":"", "+": "(plus)", "#": "No", 
							"£": "pounds ", "\n": " ", "\r": " ", "\t": " ", "\"": ""}
			
		for char in chars_to_remove.keys():
			text.replace(char, chars_to_remove[char])
		return text
	def extract_text(link, JavaScript=False):

		if JavaScript == True:
			r = driver.get(link)
			soup = BeautifulSoup(driver.page_source, 'lxml')
		else:
			r = requests.get(link)
			soup = BeautifulSoup(r.text, 'lxml')

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

		if 'JavaScript' in text:
			page_text = extract_text(link, JavaScript=True)

		return text_validator(page_text)

	try:
		frame['faq_text'] = extract_text(frame['faq_link'])
	except Exception as e:
		frame['faq_text'] = None
	try:
		frame['privacy_text'] = extract_text(frame['privacy_link'])
	except Exception as e:
		frame['privacy_text'] = None
	try:
		frame['delivery_text'] = extract_text(frame['delivery_link'])
	except Exception as e:
		frame['delivery_text'] = None
	try:
		frame['terms_text'] = extract_text(frame['terms_link'])
	except Exception as e:
		frame['terms_text'] = None
	try:
		frame['return_text'] = extract_text(frame['return_link'])
	except Exception as e:
		frame['return_text'] = None
	try:
		frame['warranty_text'] = extract_text(frame['warranty_link'])
	except Exception as e:
		frame['warranty_text'] = None
	#print(frame)
	data_frame = data_frame.append(frame, ignore_index=True)
	print(data_frame)
	data_frame.to_csv('companies_v2.csv', header=False, mode='a')

def crawl():
	for each in links_to_scrape():
		print(each)
		r = requests.get(each)
		parse(r.text, r.url, r.status_code)

crawl()