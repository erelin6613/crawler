import pandas as pd
from time import gmtime, strftime, sleep
from scrape_functions_sandbox import parser, getDataBBB, getDataHA
from threading import Thread

frame = pd.read_csv('/home/val/links_to_parse_1.csv')
print(frame.head(5))

threads_amount = int(input('How much processes to start?'))

q = [link for link in frame['LinkOnPlatform']]

while len(q) > 0:
	threads = []
	for i in range(threads_amount):
		t = Thread(target = getDataHA, args=(q[i], ))
		#print('thread ', i, ' has been created')
		#frame.drop
		threads.append(t)
		t.start()
	for t in threads:
		t.join()
		#sleep(30)
	del q[0:(threads_amount-1)]