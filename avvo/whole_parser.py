#!/usr/bin/env python3
# Developed by Valentyna Fihurska in collaboration with
# Olha Babich for wiserbrand.com

# Update from 31-Jul-2019
# Crawler works by crawling over the links of the giving website
# (within one domain); in the future might be designed to
# parse requested information from crawled links
# module is optimized to deal multiple Threads.
# Current elaborations:
# developing custom scraping algorythm

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
from queue import Queue

project='avvo'
url='https://www.avvo.com/'
threads_amount=2

def ultimate_crawler(project, url, threads_amount):

    queue = Queue()
    #project = str(input('What web resource do you want to crawl? (name)'))
    #project = 'homestars'
    #placement = os.path.join(os.getcwd(), project)
    #url = input('Could you give it`s web address, please?')
    #url = 'www.homestars.com' 
    # temporary work around until I`ll figure out why threads work
    # with the same link :)
    #try:
    #    threads_amount = int(input('How much '))
    #threads_amount = 2
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
        except Exception as e:
            print(e)
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
               
    def get_domain_name():
        return 'avvo.com'


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
        #options.add_argument('headless')
        driver = webdriver.Chrome(executable_path = './chromedriver', options = options)
        domain = get_domain_name()
        try:
            driver.get(link)
        except Exception as e:
            print('***Exception: ', link, e)
        to_crawl_list = file_to_list(to_crawl_file)
        crawled_list = file_to_list(to_crawl_file)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        #print(soup)
        #try:
        for elem in soup.find_all('a'):
            url = elem.get('href')
            print(url)
            if url:
                parsed_link = url
            else:
                continue
            if parsed_link.startswith('/'):
                parsed_link = 'https://'+get_domain_name()+parsed_link
            if url.startswith('//www.'):
                if get_domain_name() in url:
                    parsed_link = 'https:'+url
            if url.startswith('//http:'):
                if get_domain_name() in url:
                    parsed_link = url[2:]
            if url.startswith('//https:'):
                if get_domain_name() in url:
                    parsed_link = url[2:]
            if url.startswith('https:') or url.startswith('http:') or url.startswith('www.'):
                if get_domain_name() in url:
                    parsed_link = url
            if parsed_link.startswith('#'):
                continue
            if get_domain_name() not in parsed_link:
                driver.quit()
                return
            print(parsed_link)
            if check_the_link_to_crawl(parsed_link, to_crawl_file) == False and check_the_link_crawled(link, crawled_list) == False:
                to_crawl_list.append(parsed_link)
       	    else:
                to_crawl_list.appended(parsed_link)
            driver.quit()

            if check_the_link_crawled(link, crawled_list) == False:
                crawled_list.append(parsed_link)

            if parsed_link:
                print(parsed_link)
            else:
                print('something is wrong with the link:', link)

            list_to_file(to_crawl_list, to_crawl_file)
            list_to_file(crawled_list, crawled_file)
        #except Exception as e:
        #    print(e)
            driver.quit()


    def create_workers():
        for _ in range(threads_amount):
            t = Thread(target=work)
            t.daemon = True
            t.start()


# Do the next job in the queue
    def work():
        while True:
            url = queue.get()
            whole_parser(url, to_crawl_file, crawled_file)
            queue.task_done()


# Each queued link is a new job
    def create_jobs():
    
        #queue = file_to_list(to_crawl_file)
        for link in file_to_list(to_crawl_file):
            queue.put(link)
        queue.join()
        crawl()


# Check if there are items in the queue, if so crawl them
    def crawl():
        queued_links = file_to_list(to_crawl_file)
        if len(queued_links) > 0:
            print(str(len(queued_links)) + ' links in the queue')
            create_jobs()


  
    
    make_a_dir(project)
    write_file(to_crawl_file, 'https://'+get_domain_name())
    write_file(crawled_file, '')
    create_workers()
    crawl()
    #whole_parser(file_to_list(to_crawl_file)[0], to_crawl_file, crawled_file)


ultimate_crawler(project, url, threads_amount)
