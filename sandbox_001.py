from scrapy_selenium import SeleniumRequest
import scrapy_selenium
from shutil import which

SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_DRIVER_EXECUTABLE_PATH = which('chromedriver')
SELENIUM_DRIVER_ARGUMENTS=['-headless'] 

class Link:
	name = 'link'
	url = 'https://www.bbb.org/us/category/restaurants'
	def parse(self, response):
		item = []
		#item.append(response.xpath('//a[@class="result-title"/text()').extract())
		#item.append(response.xpath('//a[@class="result-title"/text()').extract())
		#item = CL_Item()
		soup = BeautifulSoup(response.text, 'lxml')
		for elem in soup.find_all('a', class_ = 'dtm-search-listing-business-name Name__Link-dpvfia-1 iyzkGZ'):
		#item['tittle'] = elem.text
			print('***')
			print(elem.text)
			print('***')
		#item['link'] = response.css('a.result-title a::attr(href)').extract_first()
		#return item

	def parse_result(self, response):
		print(response.selector.xpath('//title/@text'))

	#options = scrapy_selenium.ChromeOptions()
	#options.add_argument('headless')
	#driver = scrapy_selenium.Chrome(executable_path='./chromedriver',options=options)

def Main():
	url = Link()
	print('it gets here')
	#url = 'https://www.bbb.org/us/category/restaurants'
	response = SeleniumRequest(url, self.parse_result)

Main()

print('well...')