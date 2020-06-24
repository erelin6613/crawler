from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from scrape_functions_sandbox import parser, getDataBBB
#from multiprocessing import Pool, Process
from threading import Thread
#import sqlite3



#options = webdriver.ChromeOptions()
#options.add_argument('headless')
#driver = webdriver.Chrome(executable_path='./chromedriver',options=options)
#proc = int(input('How much processes to start?'))
threads_amount = int(input('How much threads to start?'))
all_zips = pd.read_csv('chunck_12_1.csv', dtype = 'object')
all_zips = all_zips.ix[:, 'Zip code']
print(all_zips)

#error = []
#error_no_res = []
#page = 1
#index = 0
#frame = pd.DataFrame(columns = ['LinkOnBBB', 'Name', 'Website', 'Phone', 'Address', 'Overview'])
#cat = 'insurance-agency'

#threads = []

q = [each_zip for each_zip in all_zips]

#threads = []
#for link in frame['LinkOnBBB']:
	#q.put(link)
	#frame.drop([link], axis = 0)
	#i += 1

while len(q) > 0:
	threads = []
	for i in range(threads_amount):
		t = Thread(target = parser, args=(q[i], ))
		print('thread ', i, ' has been created')
		#frame.drop
		threads.append(t)
		t.start()
	for t in threads:
		t.join()
		#sleep(30)
	del q[0:(threads_amount-1)]


print('Done with this DataFrame')

"""
p = Pool(proc)
p.map(parser, all_zips)

if __name__ == '__main__':
	Main()
"""
