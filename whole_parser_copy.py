import os
import sys
from threading import Thread
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.proxy import *
from time import gmtime, strftime, sleep
import pandas as pd
import sqlite3
import time

#project = str(input('What web resource do you want to crawl? (name)'))
project = 'homestars'
placement = os.path.join(os.getcwd(), project)
#url = input('Could you give it`s web address, please?')
url = 'www.homestars.com'
threads_amount = 2
to_crawl_file = os.path.join(project, (project+'_to_crawl.txt'))
crawled_file = os.path.join(project, (project+'_crawled.txt'))

def make_a_dir(directory):
    
    if not os.path.exists(directory):
        print('New project has started: ', directory)
        os.mkdir(directory)
        return
    print('Project already exists: ', directory, '. Proceeding with started crawl.')
        
def links_log(project, url):
    #to_crawl = os.path(project+'_to_crawl.txt')
    #crawled = os.path(project+'_crawled.txt')
    if not os.path.isfile(to_crawl_file):
        with open(to_crawl_file, 'r+') as file:
            write_file(to_crawl_file, url)
    if not os.path.isfile(crawled_file):
        with open(crawled_file, 'r+') as file:
            write_file(crawled_file, '')
    #print('links_log function ran with args: ', str(project), str(url))
            
def write_file(path, data):
    try:
        with open(path, 'w') as file:
            file.write(data)
            #file.close()
    except Exception:
        with open(path, 'w') as file:
            for each in file.readlines():
                file.write(each+'\n')
    #print('write_file ran with args: ', str(path), str(data))

def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')
        #file.close()
    #print('append_to_file with args: ', str(path), str(data))

def delete_file_contents(path):
    with open(path, 'w') as file:
        file.write('')
        #file.close()

def file_to_list(name):
    results = []
    with open(name, 'r') as f:
        for line in f:
            results.append(line)
        #print(results)
    return results

def list_to_file(links, file_name):
    with open(file_name,'a') as f:
        for l in links: 
            #print(l)   
            f.write(l+'\n')
               
def get_domain_name(link):
    #link = 'www.homeadvisor.com'
    try:
        link.split('.')
        if link.startswith('http') or link.startswith('https'):
            if 'www' not in link.split('/')[2]:
                return link.split('/')[2]
            else:
                return link.split('/')[2].split('.')[1]+'.'+link.split('/')[2].split('.')[2]
        elif link.startswith('www'):
            try:
                return link.split('/')[0].split('.')[1]+'.'+link.split('/')[0].split('.')[2]
            except Exception:
                return link.split('.')[1]+'.'+link.split('.')[2]
        else:
            return link
    except ValueError as v:
        print('Invalid url, ', v)
 
        
def crawl():
    
	while len(q)>0:
#while i < 40:
	threads = []
		for i in range(threads_amount):
			t = Thread(target = homeflock_parser, args=(queue[i], to_crawl_file, crawled_file))
			print('thread ', i, ' has been created')
		#frame.drop
			threads.append(t)
			t.start()
		for t in threads:
			t.join()
		#sleep(30)
		del q[:(threads_amount-1)]

    """threads = []
    for i in range(threads_amount):
    	if i > 0 and i <= threads_amount:
    		time.sleep(5*i)

    	queue = file_to_list(to_crawl_file)
    	#print('queue: ', queue)
    	parsed = file_to_list(crawled_file)
    	#print('parsed: ', parsed)
    	t = Thread(target = whole_parser, args=(queue[0], to_crawl_file, crawled_file))
    	print('thread ', i, ' has been created')
    	if queue[0] not in parsed:
    		append_to_file(crawled_file, queue[0])
    	threads.append(t)
    	t.start()
    	write_file(crawled_file, queue[0])
    	del queue[0]
    	for t in threads:
    		t.join()"""
            
def whole_parser(link, to_crawl_file, crawled_file):
    
    print('crawling: '+link)    
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(executable_path = './chromedriver', options = options)
    domain = get_domain_name(link)
    try:
        driver.get(link)
    except Exception as e:
        print('***Exception: ', link)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    for elem in soup.find_all('a'):
        to_crawl_list = file_to_list(to_crawl_file)
        crawled_list = file_to_list(to_crawl_file)
        url = elem.get('href')
        #if domain in url:
        #if 'facebook' or 'twitter' or 'youtube' or 'pintrest' or 'instagram' or 'linkedin' in url:
            #continue
        if url.startswith('#'):
            continue
        if url.startswith('//www.') or url.startswith('//http:') or url.startswith('//https:'):
            continue
        if url.startswith('https://') or url.startswith('http://') or url.startswith('www.'):
            if domain in url:
                parsed_link = url
        elif url.startswith('/'):
            try:
                if url.split('.')[1] == 'com' or url.split('.')[2] == 'com' or url.split('.')[1] == 'co' or url.split('.')[2] == 'co' or url.split('.')[1] == 'uk' or url.split('.')[2] == 'uk' or url.split('.')[1] == 'ru' or url.split('.')[2] == 'ru' or url.split('.')[1] == 'ua' or url.split('.')[2] == 'ua':
                    continue
            except Exception:
                pass

            parsed_link = 'https://'+domain+url
        
        if parsed_link in to_crawl_list:
            print(parsed_link, ' in to_crawl_list')
            continue
            
        else:
            to_crawl_list.append(parsed_link)
            print(parsed_link, ' appended to_crawl_list')
            #append_to_file(to_crawl_file, parsed_link)

        
        if parsed_link in crawled_list:
            print(parsed_link, ' in crawled_list')
            continue
        else:
            print(parsed_link, ' appended to_crawl_list')
            #append_to_file(crawled_file, parsed_link)
            crawled_list.append(parsed_link)

        del to_crawl_list[0]

        print(parsed_link)
        delete_file_contents(to_crawl_file)
        delete_file_contents(crawled_file)
        list_to_file(to_crawl_list, to_crawl_file)
        list_to_file(crawled_list, crawled_file)
                           
    driver.quit()
    
    
make_a_dir(project)
write_file(to_crawl_file, 'https://'+get_domain_name(url))
write_file(crawled_file, '')
#crawl()
whole_parser(file_to_list(to_crawl_file)[0], to_crawl_file, crawled_file)