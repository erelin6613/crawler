from threading import Thread
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.proxy import *
from time import gmtime, strftime, sleep, time
import pandas as pd
import sqlite3
from fake_useragent import UserAgent
import asyncio
from nonocaptcha.solver import Solver
import re, csv
from random import uniform, randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException  



options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(executable_path = './chromedriver', options = options)
driver.get('https://homeflock.com/dir-contractors/General+Contractors/Auburn+AL')

soup = BeautifulSoup(driver.page_source, 'lxml')
print(soup.prettify)





def write_stat(loops, time):
    with open('stat.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([loops, time])
def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def wait_between(a,b):
    rand=uniform(a, b) 
    sleep(rand)
    
def dimention(driver): 
    d = int(driver.find_element_by_xpath('//div[@id="rc-imageselect-target"]/table').get_attribute("class")[-1]);
    return d if d else 3  # dimention is 3 by default


# ***** main procedure to identify and submit picture solution	
def solve_images(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID ,"rc-imageselect-target")))
    dim = dimention(driver)
    # ****************** check if there is a clicked tile ******************
    if check_exists_by_xpath('//div[@id="rc-imageselect-target"]/table/tbody/tr/td[@class="rc-imageselect-tileselected"]'):
        rand2 = 0
    else:  
        rand2 = 1 

# wait before click on tiles
    wait_between(0.5, 1.0)		 
    # ****************** click on a tile ****************** 
    tile1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH ,   '//div[@id="rc-imageselect-target"]/table/tbody/tr[{0}]/td[{1}]'.format(randint(1, dim), randint(1, dim )))) )   
    tile1.click()
    if (rand2):
        try:
            driver.find_element_by_xpath('//div[@id="rc-imageselect-target"]/table/tbody/tr[{0}]/td[{1}]'.format(randint(1, dim), randint(1, dim))).click()
        except NoSuchElementException:
            print('\n\r No Such Element Exception for finding 2nd tile')
   
    #****************** click on submit buttion ****************** 
    driver.find_element_by_id("recaptcha-verify-button").click()

start = time()	 
url='https://homeflock.com/dir-contractors/General+Contractors/Auburn+AL'
#driver = webdriver.Firefox()
driver.get(url)

mainWin = driver.current_window_handle  

# move the driver to the first iFrame 
driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0])

# *************  locate CheckBox  **************
CheckBox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID ,"recaptcha-anchor"))
        ) 

# *************  click CheckBox  ***************
wait_between(0.5, 0.7)  
# making click on captcha CheckBox 
CheckBox.click() 
 
#***************** back to main window **************************************
driver.switch_to.window(mainWin)  

wait_between(2.0, 2.5) 

# ************ switch to the second iframe by tag name ******************
driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[1])  
i=1
while i<130:
    print('\n\r{0}-th loop'.format(i))
    # ******** check if checkbox is checked at the 1st frame ***********
    driver.switch_to.window(mainWin)   
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME , 'iframe')))  
    wait_between(1.0, 2.0)
    if check_exists_by_xpath('//span[@aria-checked="true"]'): 
        import winsound
        winsound.Beep(400,1500)
        write_stat(i, round(time()-start) - 1 ) # saving results into stat file
        break 
        
    driver.switch_to.window(mainWin)   
    # ********** To the second frame to solve pictures *************
    wait_between(0.3, 1.5) 
    driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[1]) 
    solve_images(driver)
    i=i+1