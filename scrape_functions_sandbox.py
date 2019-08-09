#!/usr/bin/env python3
# Developed by Valentyna Fihurska in collaboration with
# Olha Babich for wiserbrand.com
# Start of developement 22-Jan-2019

# For future developement: functions Bypass_Recaptcha(pageurl, sitekey),
# whole_parser(link), porch_parser (each_zip).
# Temporary solution with recaptcha is implemented with module
# pyautogui (this will most likely not work on other platforms/devices)
# in meantime collecting pictures from recaptcha for further ML.

# Version 1.7.2 from 09-Aug-2019

import requests
from threading import Thread
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.proxy import *
from time import gmtime, strftime, sleep, time
import pandas as pd
import sqlite3
#from fake_useragent import UserAgent
import asyncio
#from nonocaptcha.solver import Solver
import re, csv
from random import uniform, randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pyautogui
import autopy
import pickle





def set_proxy_connection(PROXY):
# Function to set up a proxy for connection if needed.
# Currently malfunctions for chromedriver v72.x and v73.x 
	#PROXY = "170.130.63.35:3128"
	options = webdriver.ChromeOptions()
	options.add_argument('--proxy-server=http://%s' % PROXY)
	options.add_argument('headless')
	driver = webdriver.Chrome(executable_path = './chromedriver', options = options)
	driver.get('https://www.bbb.org/us/category/restaurants')
	soup = BeautifulSoup(driver.page_source, 'lxml')
	for elem in soup.find_all('a', class_='Name__Link-dpvfia-1'):
		print(elem.get('href'))
	return soup



def fill_data_base(frame):
# Automatic filling the data base with scraped information

	connection = sqlite3.connect('./for_hirerush.db')
	cursor = connection.cursor()
	try:
		cursor.execute('CREATE TABLE for_hirerush (Name TEXT, LinkOnPlatform TEXT, Platform TEXT, Category TEXT, Overview TEXT, Website TEXT, Phone TEXT, YearInBusiness INTEGER, Rating DECIMAL, IsPaidCustomer INTEGER, Lisensed TEXT, City TEXT, State TEXT)')
	except:
		pass
	cursor.execute("INSERT INTO for_hirerush VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
		(frame['Name'], frame['LinkOnPlatform'], frame['Platform'], frame['Category'], frame['Overview'], frame['Website'], frame['Phone'], frame['Rating'], frame['Lisensed'], frame['City'], frame['State']))
	connection.commit()
	cursor.close()
	connection.close()

def getDataBBB(link):
# Function to scrape open information about businesses
# on website BBB.org. Note: check CSS selectors might be
# updated betimes by the site, check before using

	options = webdriver.ChromeOptions()
	options.add_argument('headless')

	driver = webdriver.Chrome(executable_path = './chromedriver', options = options)
	#link = frame['LinkOnBBB']

	try:
		driver.get(link)
	except:
		#proxy_num += 1
		driver.get(link)
	soup = BeautifulSoup(driver.page_source, 'lxml')
	data_frame = pd.Series()
	new_frame = pd.DataFrame()
	#name = soup.find('h4', class_ = 'dtm-business-name').text
	try:
		name = soup.find('h4', class_ = 'dtm-business-name').text
	except AttributeError:
		name = None
	try:
		website = soup.find(class_ = 'dtm-url').get('href')
	except AttributeError:
		website = None
	try:
		phone = soup.find(class_ = 'dtm-phone').text
	except AttributeError:
		phone = None
	try:
		address = soup.find(class_ = 'dtm-address').text
	except AttributeError:
		address = None
	try:
		overview = soup.find('p', class_ = 'jss288 jss296 jss316').text
	except AttributeError:
		overview = None

	data_frame['Name'] = name
	data_frame['Website'] = website
	data_frame['Phone'] = phone
	data_frame['Address'] = address
	#data_frame['Overview'] = overview
	data_frame['LinkOnBBB'] = link
	print(data_frame)
	new_frame = new_frame.append(data_frame, ignore_index = True)
	new_frame.to_csv('/home/val/Hotels_data.csv', mode='a', header = False)
	new_frame.apply(fill_data_base, axis = 1)
	fill_data_base(new_frame)
	#new_frame.to_csv('/home/val/insurance-agency.csv', mode='a', header = False)
	#data_frame.to_csv('restaurants_fin_3.csv')
	driver.quit()

	return new_frame


def parser (ms = 1):
# scraper for website link = 'https://www.etoa.org/'

	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	driver = webdriver.Chrome(executable_path='./chromedriver',options=options)
	frame = pd.DataFrame()
	ms =1
	#cat = 'insurance-agency'
	error = []
	error_no_res = []
	while True:
		try:
			link = 'https://www.etoa.org/member-search/?ms={}'.format(ms)
			driver.get(link)
		except:
			driver.get(link)
			soup = BeautifulSoup(driver.page_source, 'lxml')
			error = soup.find_all('body', class_='error404')
			#error_no_res = soup.find_all('a', class_ = 'dtm-add-a-business')
			if len(error) > 0:
				print('---------------Done-------------------')
				driver.quit()
				break

			for elem in soup.find_all(class_='row1 600'):
				print(elem.text.split('\n')[1])
				sleep(5)
				frame = frame.append({'Name': elem.text.split('\n')[1]}, ignore_index=True)
			print('done with ms = ', ms)
			ms += 1
			frame.to_csv('/home/val/etoa.csv', mode='a', header = False)	#extra copy


def thumbtack_parser(link):
# Crawler for the website 'https://www.thumbtack.com'

	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	driver = webdriver.Chrome(executable_path = './chromedriver', options = options)
	frame = pd.DataFrame(columns = ['LinkOnPlatform', 'Platform', 'Category', 'City', 'State'])
	cat = link.split('/')[-2]
	city = link.split('/')[-3]
	state = link.split('/')[-4].upper()
	#print(cat)
	try:
		driver.get(link)
	except Exception:
		driver.get(link)

	soup = BeautifulSoup(driver.page_source, 'lxml')
	see_more_button = soup.find(class_ = '_3fJtfoW2Vu3c2PYMWxXBB1 Xt5ZXUkdoAUYIq-qK7wJs KRKjAf4oQklFar4Tw7mNz _3NNIcmSzFH6uHpK23wyWDd')
	try:
		ActionChains(driver).click(see_more_button).perform()

	except Exception:
		pass

	div = soup.find_all(class_ = 'bb b-gray-300 pv3 m_pv4')
	for child in div:
		profile_link = 'https://www.thumbtack.com' + child.find('a').get('href')
		print(profile_link)
		frame = frame.append({'LinkOnCategory': link,'LinkOnPlatform': profile_link, 'Platform': 'Thumbtack', 'Category': cat, 'City': city, 'State': state}, ignore_index=True)

	if len(soup.find_all(class_ = 'error-page')):
		driver.quit()
	frame.drop_duplicates(keep = 'last', inplace = True)
	frame.to_csv('/home/val/all_the_links.csv', mode='a', header = False)
	driver.quit()


def getDataThumbtack(frame):
# Scraper for the website 'https://www.thumbtack.com'
# target: information from business profile

	link = str(frame['LinkOnPlatform'])
	data_frame = pd.Series()
	new_frame = pd.DataFrame()
	options = webdriver.ChromeOptions()
	options.add_argument('headless')

	driver = webdriver.Chrome(executable_path = './chromedriver', options = options)
	driver.get(link)
	soup = BeautifulSoup(driver.page_source, 'lxml')
	try:
		name = soup.find(class_ = '_2wPaClGo34l0C2fSjaTQta').text
	except AttributeError:
		name = None

	try:
		overview = soup.find(class_ = '_4FwCyrCET-9R5PFv6k-Kv tp-body-2').text
		overview = overview.split('Introduction: ')[1]
	except AttributeError:
		overview = None

	try:
		string = []
		try:
			for letter in soup.find(class_ = '_2Xy92SlFYrVrSogOmIy3jk').text.split('years in business ')[0].split('employees')[1]:
				if letter. isnumeric():
					string.append(letter)
		except Exception:
			years_bis = None

		years_bis = ''.join(string)
	
	except AttributeError:
		years_bis = None

	try:
		rating = soup.find(class_ = 'StarRating-numericRating').text
	except AttributeError:
		rating = None

	try:
		if 'License verified' in soup.find(class_ = '_2Xy92SlFYrVrSogOmIy3jk').text:
			licensed = 1
		else:
			licensed = 0
	except AttributeError:
		licensed = None

	data_frame['Name'] = name
	data_frame['Overview'] = overview
	data_frame['YearInBusiness'] = years_bis
	data_frame['Rating'] = rating
	data_frame['LinkOnPlatform'] = link
	data_frame['Phone'] = None
	data_frame['IsPaidCustomer'] = None
	data_frame['Website'] = None
	data_frame['Lisensed'] = licensed
	data_frame['LinkOnPlatform'] = link
	data_frame['Platform'] = frame['Platform']
	data_frame['Category'] = frame['Category']
	data_frame['City'] = frame['City']
	data_frame['State'] = frame['State']
	print(data_frame)
	new_frame = new_frame.append(data_frame, ignore_index = True)
	new_frame.to_csv('/home/val/thumbtack_data.csv')
	new_frame.apply(fill_data_base, axis = 1)
	driver.quit()

	return new_frame



def porch_parser (each_zip):
# Crawler for website porch.com
# Currently website has many obsticles to overcome for
# Junior DS as myself, hence function undeveloped

	options = webdriver.ChromeOptions()
	driver = webdriver.Chrome(executable_path='./chromedriver',options=options)
	frame = pd.DataFrame()
	page = 1
	error = []
	error_no_res = []
	while True:
			each_zip = str(each_zip)
			if len(str(each_zip)) == 3:
				each_zip = '00' + str(each_zip)
			elif len(str(each_zip)) == 4:
				each_zip = '0' + str(each_zip)
			link = 'https://porch.com/'
			try:
				driver.get(link)
			except:
				driver.get(link)
			soup = BeautifulSoup(driver.page_source, 'lxml')
			error = soup.find_all('body', class_='error')
			error_no_res = soup.find_all('a', class_ = 'dtm-add-a-business')
			if len(error) > 0 or len(error_no_res) > 0:
				print('---------------Done with zip-------------------', each_zip)
				frame.to_csv('/home/val/hotels_links.csv', mode='a', header = False)
				#with open ('visited_zips.csv', 'a') as file:
					#file.write(each_zip+'\n')
				print(strftime("%H:%M:%S", gmtime()))
				page = 1
				driver.quit()
				break
			print('****Page*****', driver.current_url)

			for elem in soup.find_all('a', class_='Name__Link-dpvfia-1'):
				print(elem.get('href'))
				print(strftime("%H:%M:%S", gmtime()))
				#frame.loc[index, 'LinkOnBBB'] = elem.get('href')
				frame = frame.append({'LinkOnBBB': elem.get('href'), 'Zip': each_zip }, ignore_index=True)

				#frame.apply(getDataBBB, axis = 1)
				#frame.to_csv('/home/val/zip-{}.csv', mode='a', header = False).format(str(each_zip))
				frame.drop_duplicates(subset = 'LinkOnBBB', keep = 'last')
				#frame.to_csv('/home/val/insurance_'+each_zip+'_003.csv', mode='a', header = False)
				#frame.to_csv('/home/val/'+cat+'_003/.csv', mode='a', header = False)
				if elem == soup.find_all('a', class_='Name__Link-dpvfia-1')[-1]:
					#print('---------------Done with page----------------------')
					page += 1
				#page += 1
			#frame.apply(getDataBBB, axis = 1)
			frame.drop_duplicates(keep = 'last', inplace = True)
			#frame.to_csv('/home/val/'+cat+'.csv', mode='a', header = False)	#extra copy
			#page += 1



def whole_parser(link):
# Univeral crawler to parse any website given a link
# The next challange: recaptchas

	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	driver = webdriver.Chrome(executable_path = './chromedriver', options = options)

	to_parse = open('/home/val/links_to_parse.csv', 'r+')
	parsed_links = open('/home/val/parsed_links.csv', 'r+')
	to_parse_list = []
	parsed_list = []
	for each in to_parse:
		try:
			to_parse_list.append(each.split('\n')[0])
		except Exception:
			to_parse_list.append(each)


	for each in parsed_links:
		try:
			parsed_list.append(each.split('\n')[0])
		except Exception:
			parsed_list.append(each)

	domain = 'homeadvisor.com'
	if domain in link:
		if link not in parsed_links:
			print('parsing: ', link)
			try:
				driver.get(link)
			except Exception:
				print('Invalid link:', link)
				driver.quit()
				to_parse.close()
				parsed_links.close()
				return 
			#print('parsing: ', link)
			soup = BeautifulSoup(driver.page_source, 'lxml')
			if soup == None:
				#ua = UserAgent(cache=False)
				#userAgent = ua.random
				options = webdriver.ChromeOptions()
				options.add_argument('headless')
				driver = webdriver.Chrome(executable_path = './chromedriver', options = options)
				driver.get(link)
				soup = BeautifulSoup(driver.page_source, 'lxml')
			try:	
				if soup.title.text == 'Verify real user':
					print('Houston, we did not pass a robot test.')
					#sleep(900000)
				for elem in soup.find_all('a'):

					url = str(elem.get('href'))
					if url.startswith('//'):
						url = 'https:' + url
					if url.startswith('/'):
						if domain not in url:
							url = 'https://homeadvisor.com' + url
						else:
							river.quit()
							to_parse.close()
							parsed_links.close()
							return
					if domain in url:
						if url not in to_parse:
							to_parse.write(url + '\n')
							parsed_links.write(driver.current_url+'\n')
							print(url)
			except Exception:
				pass
			#sleep(10)

	driver.quit()
	to_parse.close()
	parsed_links.close()





def homeflock_parser (link, i):
# Crawler for website homeflock.com

	options = webdriver.ChromeOptions()
	#options.add_argument(f'user-agent={userAgent}')	
	options.add_argument('headless')
	driver = webdriver.Chrome(executable_path='./chromedriver',options=options)
	frame = pd.DataFrame()

	#webdriver.common.proxy.Proxy(raw = '173.234.225.7')
	try:
		driver.get(link)
	except:
		driver.get(link)
	soup = BeautifulSoup(driver.page_source, 'lxml')
	#try:
	if len(soup.find_all('a'))>0:
		for elem in soup.find_all('a'):
			try:
				url = elem.get('href').split('/')[1]
				if url == 'contractor':
					url = 'https://homeflock.com/'+url+'/'+elem.get('href').split('/')[2]
					print(url)
					frame = frame.append({'Platform': 'Homeflock', 'LinkOnPlatform': url}, ignore_index = True)
			except Exception:
				pass

	else:
		if soup.title.text == 'Verify real user':
			print('recaptcha_slasher is called out of the loop')
			recaptcha_slasher(i)

	#except Exception:
	#	print('check')
	#	pass

	#finally:
	#	driver.quit()
	frame = frame.drop_duplicates(subset = 'LinkOnPlatform', keep = 'last')
	frame.to_csv('./homeflock_profiles.csv', mode = 'a', header = False)
	print('done with link', link)
	driver.quit()

	#driver.quit()
	#sleep(305)


def getDataHomeflock(link, i):
# Scraper for the website 'https://homeflock.com'
# target: information from business profile

	data = {}
	frame = pd.Series()
	new_frame = pd.DataFrame()
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	driver = webdriver.Chrome(executable_path = './chromedriver', options = options)
	try:
		while True:
			driver.get(link)
			soup = BeautifulSoup(driver.page_source, 'lxml')
			try:
				address = soup.find(class_ = 'profile-city').text
				name = soup.find(itemprop='name').text.strip()
			except Exception:
				recaptcha_slasher(i)
				continue

			for each in soup.find_all(class_ = 'row text'):
				data[str(each.find(class_ = 'col-sm-7 col-md-5 gray-text').text.strip())] = each.find(class_="col-sm-17 col-md-19").text.strip()
	
			frame['Platform'] = 'Homeflock'
			frame['LinkOnPlatform'] = link
			frame['Name'] = name
			try:
					frame['City'] = address.replace('\n', '').split(',')[1]
			except Exception as e:
					frame['City'] = None
					print(e)
			try:
					state = [letter for letter in address.replace('\n', '').split(',')[2] if letter.isalpha()]
					frame['State'] = ''.join(state)
			except Exception as e:
					frame['State'] = None
					print(e)
			try:
					frame['License'] = data['License:']
			except Exception as e:
					frame['License'] = None
					print(e)
			try:
					frame['Phone'] = data['Phone:']
			except Exception as e:
					frame['Phone'] = None
					print(e)
			try:
					frame['Service'] = data['Service:']
			except Exception as e:
					frame['Service'] = None
					print(e)	
			try:
					frame['Status'] = data['Status:']
			except Exception as e:
					frame['Status'] = None
					print(e)
			try:
					frame['Type'] = data['Type:']
			except Exception as e:
					frame['Type'] = None
					print(e)

			try:
					frame['Overview'] = address
			except Exception as e:
					frame['Overview'] = None
					print(e)

			new_frame = new_frame.append(frame, ignore_index = True)
			new_frame.to_csv('./homeflock-data.csv', mode = 'a', header = False)
			print(new_frame)
			break
	
	finally:
		if driver:
			driver.quit()




def getDataHA(link):
# scraper for the website 'https://www.homeadvisor.com'
# target: information from business profile

	options = webdriver.ChromeOptions()
	options.add_argument('headless')

	driver = webdriver.Chrome(executable_path = './chromedriver', options = options)
	#link = frame['LinkOnBBB']

	try:
		try:
			driver.get(link)
		except:
			#proxy_num += 1
			driver.get(link)
		soup = BeautifulSoup(driver.page_source, 'lxml')
		data_frame = pd.Series()
		new_frame = pd.DataFrame()
		#name = soup.find('h4', class_ = 'dtm-business-name').text
		try:
			name = soup.find(itemprop = 'name').text.strip()
		except AttributeError:
			name = None

		try:
			overview = soup.find(itemprop = 'description').text.replace('\n', ' ')
		except AttributeError:
			overview = None

		try:
			phone = soup.find(class_ = 'sp-company-telephone t-header-big l-header-margin').text.strip()
		except AttributeError:
			phone = None

		try:
			state = soup.find(itemprop='addressRegion').text
		except AttributeError:
			state = None

		try:
			city = soup.find(itemprop='addressLocality').text
		except AttributeError:
			city = None

		try:
			rating = soup.find(itemprop='ratingValue').text
		except AttributeError:
			rating = None


		try:
			for each in soup.find_all(class_ = 'sp-column-header t-header-super t-accent'):
				if 'Website' in each.text:
					website = each.find_next('a').get('href')
		except AttributeError:
			website = None

		try:
			category = soup.find(id = 'profile-services-offered').find('span').text
		except AttributeError:
			category = None

		data_frame['Name'] = name
		data_frame['Website'] = website
		data_frame['Phone'] = phone
		data_frame['State'] = state
		data_frame['City'] = city
		data_frame['Overview'] = overview
		data_frame['LinkOnPlatform'] = link
		data_frame['Service'] = category
		data_frame['Platform'] = 'HomeAdvisor'
		print(data_frame)
		new_frame = new_frame.append(data_frame, ignore_index = True)
		new_frame.to_csv('/home/val/HomeAdvisor.csv', mode='a', header = False)
		#new_frame.apply(fill_data_base, axis = 1)
		#fill_data_base(new_frame)
		#new_frame.to_csv('/home/val/insurance-agency.csv', mode='a', header = False)
		#data_frame.to_csv('restaurants_fin_3.csv')
		driver.quit()

	except Exception as e:
		print(link, '\nAn error: ', e)
		driver.quit()

	return new_frame

def recaptcha_slasher(i):
	browser = pyautogui.position(x=800, y=300)
	pyautogui.leftClick(browser)
	pyautogui.hotkey('f5')
	sleep(3)
	checkbox = pyautogui.position(x=516, y=206)
	pyautogui.leftClick(checkbox)
	sleep(3)
	image = autopy.bitmap.capture_screen()
	path = '/home/val/google_recaptcha_set/captured_{}.png'.format(i)
	image.save(path)
	submit = pyautogui.position(x=518, y=285)
	pyautogui.leftClick(submit)




def trustpilot_cats(link):
	categories = {}
	r = requests.get(link)
	soup = BeautifulSoup(r.text, 'lxml')
	for each in soup.find_all(class_='category-object'):
		subcats = []
		#print(each)
		for sub_cat in each.findChildren():
			#each.text.strip()+':'+sub_cat.text.strip())
			subcats.append(sub_cat.text.strip())
		categories[str(each.text.strip())] = subcats

	print(categories)
	pickle_out = open('trustpilot_cats_pickle.pickle', 'wb')
	pickle.dump(obj=categories, file=pickle_out)
	pickle_out.close()
	trustpilot_categories = open('trustpilot_categories.csv', 'a')
	for each in categories.keys():
		trustpilot_categories.write(each.strip()+'\n')
		for sub_cat in each:
			trustpilot_categories.write(sub_cat.strip()+'\n')

	trustpilot_categories.close()
	pickle_out.close()

def trustpilot_parser(link):
	domain = 'https://www.trustpilot.com'
	frame = pd.DataFrame(columns=['CategoryLink', 'ProfileLink', 'Website'])
	dict_biz = {}
	#categories = {}
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	driver = webdriver.Chrome(executable_path = './chromedriver', options = options)
	driver.get(link)
	#print(str(r.text.find('category-business-card card')))
	soup = BeautifulSoup(driver.page_source, 'lxml')
	for each in soup.find_all(class_='category-business-card card'):
		#print(each.get('href'))
		dict_biz['CategoryLink'] = link
		dict_biz['ProfileLink'] = domain+each.get('href')
		print(domain+each.get('href'))
		try:
			dict_biz['Website'] = each.get('href').split('/')[-1].split('?')[0]
		except Exception:
			dict_biz['Website'] = each.get('href').split('/')[-1]
		print(dict_biz)
		frame = frame.append(dict_biz, ignore_index=True)

	frame.to_csv('trustpilot_links.csv', mode='a', header=False)
	driver.quit()


def trustpilot_scraper(link='https://www.trustpilot.com/review/theteaspot.com'):
	#domain = 'https://www.trustpilot.com'
	#frame = pd.DataFrame(columns=['CategoryLink', 'ProfileLink', 'Website'])
	#dict_biz = {}
	#categories = {}
	options = webdriver.ChromeOptions()
	# options.add_argument('headless')
	driver = webdriver.Chrome(executable_path = './chromedriver', options = options)
	driver.get(link)
	sleep(5)
	SCROLL_PAUSE_TIME = 0.5

# Get scroll height
	
	i=0
	while True:
		
	    # Scroll down to bottom
	    driver.execute_script("window.scrollTo(480*{}, ({}+1)*860);".format(i,i))

	    # Wait to load page
	    sleep(SCROLL_PAUSE_TIME)

	    # Calculate new scroll height and compare with last scroll height
	    
	    if i == 10:
	        break
	    i+= 1
	#print(str(r.text.find('category-business-card card')))
	soup = BeautifulSoup(driver.page_source, 'lxml')
	name = soup.find_all(class_='multi-size-header')[0].text.split('\n')[1]
	reviews_number = soup.find_all(class_='header--inline')[0].text.split('\n')[1].strip()
	reviews_score = soup.find_all(class_='header--inline')[0].text.split('\n')[-1].strip()
	profile_site = soup.find_all(class_='badge-card__title')[0].text.strip()
	claim = soup.find_all(class_='badge-card__title')[1].text.strip()
	#print(soup.find_all('trustscore'))
	with open('blah.txt', 'w') as f:
		f.write(soup.prettify())
	print(soup.find_all(class_='contact-point__details'))
	print(name)
	#	#print(each.get('href'))
	#	dict_biz['CategoryLink'] = link
	#	dict_biz['ProfileLink'] = domain+each.get('href')
	#	print(domain+each.get('href'))
	#	try:
	#		dict_biz['Website'] = each.get('href').split('/')[-1].split('?')[0]
	#	except Exception:
	#		dict_biz['Website'] = each.get('href').split('/')[-1]
	#	print(dict_biz)
	#	frame = frame.append(dict_biz, ignore_index=True)

	#frame.to_csv('trustpilot_links.csv', mode='a', header=False)
	# driver.quit()




"""def Bypass_Recaptcha(pageurl, sitekey):
	pageurl = "https://homeflock.com/dir-contractors/Home+Builders/Annapolis+MD"
	sitekey = "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-"

	#proxy = "170.130.63.35:3128"
	proxy = ''
	auth_details = {
	"username": "user",
	"password": "pass"
					}
	args = ["--timeout 5"]
	options = {"ignoreHTTPSErrors": True, "args": args}
	client = Solver(pageurl, sitekey, options=options,
     				proxy=proxy, proxy_auth=auth_details)
	

	solution = asyncio.get_event_loop().run_until_complete(client.start())
	if solution:
     		print(solution)"""



#def Bypass_captcha:
#	pass
"""
	def write_stat(loops, time):
		with open('stat.csv', 'a', newline='') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=',',
								quotechar='"', quoting=csv.QUOTE_MINIMAL)
			spamwriter.writerow([loops, time])  	 
	
	def check_exists_by_xpath(xpath):
    	try:
        	driver.find_element_by_xpath(xpath)
    	except NoSuchElementException:
        	return False
    	return True
	
	def wait_between(a,b):
		rand=uniform(a, b) 
		sleep(rand)
 
	def dimention(driver): 
		d = int(driver.find_element_by_xpath('//div[@id="rc-imageselect-target"]/table').get_attribute("class")[-1]);
		return d if d else 3  # dimention is 3 by default
	
	# ***** main procedure to identify and submit picture solution	
	def solve_images(driver):	
		WebDriverWait(driver, 10).until(
        	EC.presence_of_element_located((By.ID ,"rc-imageselect-target"))) 		
		dim = dimention(driver)	
	# ****************** check if there is a clicked tile ******************
		if check_exists_by_xpath('//div[@id="rc-imageselect-target"]/table/tbody/tr/td[@class="rc-imageselect-tileselected"]'):
			rand2 = 0
		else:  
			rand2 = 1 

		# wait before click on tiles 	
		wait_between(0.5, 1.0)		 
		# ****************** click on a tile ****************** 
		tile1 = WebDriverWait(driver, 10).until(
        	EC.element_to_be_clickable((By.XPATH ,   '//div[@id="rc-imageselect-target"]/table/tbody/tr[{0}]/td[{1}]'.format(randint(1, dim), randint(1, dim )))))   
		tile1.click() 
		if (rand2):
			try:
				driver.find_element_by_xpath('//div[@id="rc-imageselect-target"]/table/tbody/tr[{0}]/td[{1}]'.format(randint(1, dim), randint(1, dim))).click()
			except NoSuchElementException:          		
		    	print('\n\r No Such Element Exception for finding 2nd tile')
   
	 
		#****************** click on submit buttion ****************** 
	driver.find_element_by_id("recaptcha-verify-button").click()

	start = time()	 
	url='...'
	driver = webdriver.Firefox()
	driver.get(url)

	mainWin = driver.current_window_handle  

	# move the driver to the first iFrame 
	driver.switch_to_frame(driver.find_elements_by_tag_name("iframe")[0])

	# *************  locate CheckBox  **************
	CheckBox = WebDriverWait(driver, 10).until(
        	EC.presence_of_element_located((By.ID ,"recaptcha-anchor"))
        )	 

	# *************  click CheckBox  ***************
	wait_between(0.5, 0.7)  
	# making click on captcha CheckBox 
	CheckBox.click() 
 
	#***************** back to main window **************************************
	driver.switch_to_window(mainWin)  

	wait_between(2.0, 2.5) 

	# ************ switch to the second iframe by tag name ******************
	driver.switch_to_frame(driver.find_elements_by_tag_name("iframe")[1])  
	i=1
	while i<130:
		print('\n\r{0}-th loop'.format(i))
		# ******** check if checkbox is checked at the 1st frame ***********
		driver.switch_to_window(mainWin)   
		WebDriverWait(driver, 10).until(
        	EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME , 'iframe'))
        	)  
		wait_between(1.0, 2.0)
		if check_exists_by_xpath('//span[@aria-checked="true"]'): 
                	import winsound
			winsound.Beep(400,1500)
			write_stat(i, round(time()-start) - 1 ) # saving results into stat file
			break 
		
		driver.switch_to_window(mainWin)   
		# ********** To the second frame to solve pictures *************
		wait_between(0.3, 1.5) 
		driver.switch_to_frame(driver.find_elements_by_tag_name("iframe")[1]) 
		solve_images(driver)
		i=i+1
"""
