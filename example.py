from bs4 import BeautifulSoup
import requests
from queue import Queue
from threading import Thread
import re


THREADS_NUM = 3


def ipeds_data(tasks):
    while True:
        ipeds = tasks.get()
        if ipeds is None:
            return
        link = 'https://nces.ed.gov/collegenavigator/?id=' + str(ipeds) + '#admsns'
        search = requests.get(link).text
        soup = BeautifulSoup(search, 'lxml')

        try:
            retention = soup.find(id='divctl00_cphCollegeNavBody_ucInstitutionMain_ctl05').find_all('img')
            if len(retention) > 0:
                retention = retention[0]
                alt_text = retention.get('alt')
                if alt_text:
                    if re.search('Student retention', alt_text):
                        fts = re.findall('Full-time students: \d{1,3}%', alt_text)
                        if fts:
                            fts = re.findall('\d{1,3}%', fts[0])[0]
                        pts = re.findall('Part-time students: \d{1,3}%', alt_text)
                        if pts:
                            pts = re.findall('\d{1,3}%', pts[0])[0]
                        print(ipeds, fts, pts)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    school_ipeds = [100654, 100663, 100690, 100830, 100858, 100937]

    q = Queue()
    for ipeds in school_ipeds:
        q.put(ipeds)

    threads = []
    for i in range(THREADS_NUM):
        t = Thread(target=ipeds_data, args=(q,))
        threads.append(t)
        t.start()

    for _ in range(THREADS_NUM):
        q.put(None)

    for t in threads:
        t.join()

