import pandas as pd
from time import gmtime, strftime, sleep
from scrape_functions_sandbox import whole_parser, getDataHomeflock
from threading import Thread
from queue import Queue

frame = pd.read_csv('./homeflock_profiles.csv')
#print(frame.head(5))




for link in frame['LinkOnPlatform']:
	getDataHomeflock(link)












"""
#parser(ms =1)

threads_amount = 3

#homeflock_parser('https://homeflock.com/dir-contractors/Home+Builders/Laguna+Niguel+CA/6')


#q = Queue()
q = [link for link in frame['LinkOnPlatform']]
print(q)
#threads = []
#for link in to_parse_list:
	#q.put(link)
	#frame.drop([link], axis = 0)
	#i += 1

while len(q)>0:
#while i < 40:
	threads = []
	for i in range(threads_amount):
		t = Thread(target = getDataHomeflock, args=(q[i], ))
		#print('thread ', i, ' has been created')
		#frame.drop
		threads.append(t)
		t.start()
	for t in threads:
		t.join()
		#sleep(30)
	del q[:(threads_amount-1)]

print('Done with this DataFrame')
"""