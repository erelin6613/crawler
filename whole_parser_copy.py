#!/usr/bin/env python3
# Developed by Valentyna Fihurska for wiserbrand.com

# Update from 19-Dec-2019
# Crawler works by crawling over the links of the giving website
# (within one domain); in the future might be designed to
# parse requested information from crawled links
# Current elaborations: 1. setting the pipeline to
# switch between requests object and webdriver as needed

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
#import requests

#project = str(input('What web resource do you want to crawl? (name)'))
project = 'homestars'
placement = os.path.join(os.getcwd(), project)
#url = input('Could you give it`s web address, please?')
url = 'www.homestars.com'
# temporary work around until I`ll figure out why threads work
# with the same link :)
threads_amount = 1
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
    with open(file_name,'w') as f:
        for l in links:
        	if len(l) > 0:
        		f.write(l.strip()+'\n')
               
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
    queue = file_to_list(to_crawl_file)
    while len(queue)>0:
        queue = file_to_list(to_crawl_file)
        print('Queue:', queue)
        threads = []
        try:
            for i in range(threads_amount):
                t = Thread(target = whole_parser, args=(queue[i], to_crawl_file, crawled_file))
                print('thread ', i, ' has been created')
                threads.append(t)
                t.start()
                for t in threads:
                    t.join()

            del queue[:(threads_amount-1)]
            list_to_file(queue, to_crawl_file)
            #print('*')

        except Exception:
            pass


def check_the_link_to_crawl(link, to_crawl_list):

	if link in to_crawl_list:
		return True
	return False

def check_the_link_crawled(link, crawled_list):

	if link in crawled_file:
		return True
	return False
            
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
    to_crawl_list = file_to_list(to_crawl_file)
    crawled_list = file_to_list(to_crawl_file)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    for elem in soup.find_all('a'):
        url = elem.get('href')
        #if domain in url:
        #if 'facebook' or 'twitter' or 'youtube' or 'pintrest' or 'instagram' or 'linkedin' in url:
            #continue
        if url.startswith('#') or url.startswith('//'):
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
            print(parsed_link)
        if check_the_link_to_crawl(parsed_link, to_crawl_file) == False and check_the_link_crawled(link, crawled_list) == False:
        	to_crawl_list.append(parsed_link)
            #continue
       	#else:
       		#to_crawl_list.appended(parsed_link)
    driver.quit()

    if check_the_link_crawled(link, crawled_list) == False:
    	crawled_list.append(parsed_link)


    print(parsed_link)

    list_to_file(to_crawl_list, to_crawl_file)
    list_to_file(crawled_list, crawled_file)
        
    
make_a_dir(project)
write_file(to_crawl_file, 'https://'+get_domain_name(url))
write_file(crawled_file, '')
crawl()
#whole_parser(file_to_list(to_crawl_file)[0], to_crawl_file, crawled_file)
