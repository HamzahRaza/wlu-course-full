"""
import requests
from bs4 import BeautifulSoup

URL = 'https://scheduleme.wlu.ca/vsb/s/emhnupw'

page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(id = 'requirements')

job_elems = results.find_all('div', class_='warningMessageDiv')

for item in job_elems:
    warning = item.find('span', class_ = 'warningMessage')

    print(page.content)
 """
 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome("C:/Users\hamza\Downloads\chromedriver_win32\chromedriver.exe")

driver.get("https://scheduleme.wlu.ca/vsb/s/zwktuqj")
driver.set_window_size(1920,1080)
driver.implicitly_wait(10)
check = driver.find_element_by_name("ignore_check")
check.click()
print(check)