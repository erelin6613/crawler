from bs4 import BeautifulSoup
import requests
import scrapy
import mysql.connector

#bbb_data = mysql.connector.connect(host = 'localhost', user = 'val',
#									passwd = '', database = 'bbb_data')

categories = open('pickle_map', 'rb')
print(categories)

with open('BBB-restuarants-4.html') as html_file:
#source = requests.get('https://www.bbb.org/us/category/restaurants')
	soup = BeautifulSoup(html_file, 'lxml')
#print(soup.prettify())

bbb_data = open('bbb_data.csv', 'a+')

for elem in soup.find_all('a', class_='dtm-search-listing-business-name Name__Link-dpvfia-1 iyzkGZ'):
	bbb_data.write(elem.text+'\n')

#biz_name = elem.a
#print(biz)
#print(type(biz_name))
