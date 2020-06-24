from threading import Thread
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from time import gmtime, strftime, sleep
import pandas as pd

#options = webdriver.ChromeOptions()
#options.add_argument('headless')
#driver = webdriver.Chrome(executable_path='./chromedriver',options=options)


def getDataBBB(frame):
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	#options.add_arguments('disable-dev-shm-usage')
	sleep(0.5)
	driver = webdriver.Chrome(executable_path='./chromedriver',options=options)
	link = frame['LinkOnBBB']
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
		website = soup.find(class_ = 'dtm-url styles__LinkStyled-sc-1yozr49-0 eyfwAI').get('href')
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
	try:
		overview = soup.find('p', class_ = 'jss288 jss296 jss316').text
	except AttributeError:
		overview = None

	data_frame['Name'] = name
	data_frame['Website'] = website
	data_frame['Phone'] = phone
	data_frame['Address'] = address
	data_frame['Overview'] = overview
	data_frame['LinkOnBBB'] = link
	print(data_frame)
	new_frame = new_frame.append(data_frame, ignore_index = True)
	new_frame.to_csv('restaurants_final_2.csv', mode='a', header = False)
	#driver.quit()
	#data_frame.to_csv('restaurants_fin_3.csv')

	return new_frame


def BBB_parser(order, frame):
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	driver = webdriver.Chrome(executable_path='./chromedriver',options=options)
	error = []
	error_no_res = []
	page = 1
	#index = 0
	zip_count = 0
	#for each_zip in all_zips:
	each_zip = order.get()
	each_zip = str(each_zip)
	if len(str(each_zip)) == 3:
		each_zip = '00' + str(each_zip)
	elif len(str(each_zip)) == 4:
		each_zip = '0' + str(each_zip)
		#frame.to_csv('/home/val/restaurants_4_temp.csv')
	while True:
		link = 'https://www.bbb.org/search?find_country=USA&find_entity=20019-000&find_id=20019-000&find_loc={}&find_text=Insurance%20Companies&find_type=Category&page={}&sort=Rating'.format(each_zip, page)
		driver.get(link)
		soup = BeautifulSoup(driver.page_source, 'lxml')
		error = soup.find_all(class_='error')
		#error_no_res = soup.find_all('a', class_ = 'dtm-add-a-business')
		if len(error) > 0:
			zip_count += 1
			print('Done with zip', each_zip)
			#percent = 100*zip_count/(all_zips.shape[0])
			#print(percent, '% done')
			print(strftime("%H:%M:%S", gmtime()))
			page = 1
			#frame.to_csv('/home/val/restaurants_4_temp.csv')
			break
		print(driver.current_url)
		for elem in soup.find_all('a', class_='dtm-search-listing-business-name Name__Link-dpvfia-1 iyzkGZ'):
			print(elem.get('href'))
			print(strftime("%H:%M:%S", gmtime()))
			frame = frame.append({'LinkOnBBB': elem.get('href') }, ignore_index=True)
			frame = frame.apply(getDataBBB, axis = 1)
			frame.to_csv('/home/val/linksonbbb_{}_temp.csv'.format(cat))
			#index += 1
			page += 1
			#frame.to_csv('/home/val/restaurants_4_temp.csv')	#extra copy


	frame.to_csv('/home/val/linksonbbb_{}.csv'.format(cat))
	driver.quit()





"""def BBB_parser(each_zip, frame):
	error = []
	error_no_res = []
	page = 1
	index = 0
	#zip_count = 0
	while True:
		each_zip = str(each_zip)
		if len(str(each_zip)) == 3:
			each_zip == '00' + str(each_zip)
		elif len(str(each_zip)) == 4:
			each_zip = '0' + str(each_zip)
		while True:
			link = 'https://www.bbb.org/search?find_country=USA&find_entity=70571-000&find_id=70571-000&find_loc={}&find_text=Moving%20Companies&find_type=Category&page={}&sort=Relevance'.format(each_zip, page)
			driver.get(link)
			soup = BeautifulSoup(driver.page_source, 'lxml')
			error = soup.find_all('body', class_='error')
			error_no_res = soup.find_all('a', class_ = 'dtm-add-a-business')
			if len(error) > 0 or len(error_no_res) > 0:
				#zip_count += 1
				print('Done with zip', each_zip)
				#percent = 100*zip_count/(all_zips.shape[0])
				#print(percent, '% done')
				print(strftime("%H:%M:%S", gmtime()))
				page = 1
				#driver.close()
				break
			print(driver.current_url)
			for elem in soup.find_all('a', class_='dtm-search-listing-business-name Name__Link-dpvfia-1 iyzkGZ'):
				#print(elem.get('href'))
				print(strftime("%H:%M:%S", gmtime()))
				frame.loc[index, 'LinkOnBBB'] = elem.get('href')
				if frame.loc[index, 'LinkOnBBB'] != 'None':
					print(frame.loc[index, 'LinkOnBBB'])
					frame = frame.apply(getDataBBB, axis = 1)
					frame.to_csv('/home/val/movers_temp_v3.csv')
					index += 1
					pass
			page += 1
				#movers.to_csv('/home/val/movers_temp_v2.csv')	#extra copy"""

"""def getData(data_frame):
	driver.get(link)
	soup = BeautifulSoup(driver.page_source, 'lxml')
	name = soup.find('h4', class_ = 'dtm-business-name').text
	try:
		website = soup.find('div', class_ = 'styles__DivLayoutWithIcon-sc-47rb2e-0 eRLStY').a.get('href')
	except AttributeError:
		website = None
	try:
		phone = soup.find('p', class_ = 'dtm-phone').text
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

def parse(each_zip):
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	driver = webdriver.Chrome(executable_path='./chromedriver',options=options)
	error = []
	error_no_res = []
	page = 1
	index = 0
	restaurants_23 = pd.DataFrame()
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
				#zip_count += 1
				print('Done with zip', each_zip)
				#percent = 100*zip_count/(all_zips.shape[0])
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
			restaurants_23.to_csv('/home/val/restaurants_8_test_temp.csv')

	return restaurants_23	#extra copy
	driver.close()




options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(executable_path='./chromedriver',options=options)

link = 'https://www.bbb.org/us/nd/bismarck/profile/relocation-services/quality-pack-and-load-llc-0704-1000004352'
driver.get(link)
soup = BeautifulSoup(driver.page_source, 'lxml')
phone = soup.find_all('div', class_ = 'styles__MobileCardText-sc-1tppus8-0 fIMGoe')
if len(phone[3].text) < 15:
	phone = phone[3].text
#phone = phone.findChildren('span')
#phone = phone.find_all('span')
#print(phone)

for el in phone:
	print(el)
	print('')

#li = soup.find('li', {'class': 'text'})
#children = li.findChildren("a" , recursive=False)
#for child in children:
#    print child

"""
"""
#new_df = pd.read_csv('USA-Zip.csv', dtype = 'object')
all_zips = pd.read_csv('USA-Zip.csv', dtype = 'object')
#all_zips = all_zips.dropna()
all_zips = all_zips.ix[:, 'Zip code']
print(all_zips)
#print(all_zips.columns)

error = []
error_no_res = []
page = 1
index = 0
restaurants_23 = pd.DataFrame(columns = ['LinkOnBBB'])
zip_count = 0

processlist = []

for each_zip in all_zips:
	process = Thread(target = parse, args = (each_zip,))
	process.start()
	processlist.append(process)

for proc in processlist:
	proc.join()

restaurants_23.to_csv('/home/val/restaurants_8_test.csv')
#restaurants_23.drop_duplicates(subset = 'LinkOnBBB', inplace = True)
#print(restaurants_23)
#restaurants_23 = restaurants_23.apply(getData, axis = 1)
print(restaurants_23)

#restaurants_23.to_csv('/home/val/restaurants_df_24.csv')
"""
