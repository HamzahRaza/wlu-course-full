"""
------------------------------------------------------------------------
Scrape data from schedule me for given course code
------------------------------------------------------------------------
Author: Hamzah Raza
Email:  Raza5760@mylaurier.ca
__updated__ = "2018-07-27"
------------------------------------------------------------------------
"""


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import getpass

COURSES = ["MA103", "EM203", "MA122"]

for course in COURSES:
    driver = webdriver.Chrome("C:/Users\%s\Downloads\chromedriver_win32\chromedriver.exe" % getpass.getuser())

    driver.get("https://scheduleme.wlu.ca")
    driver.set_window_size(1920,1080)
    driver.implicitly_wait(10)

    spring = driver.find_element_by_id("term_202105")
    spring.click()
    
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'code_number')))
    search = driver.find_element_by_id("code_number")
    search.clear()
    search.send_keys(course)
    search.send_keys(Keys.RETURN)
    
    full_classes = driver.find_element_by_id("hide_full")
    full_classes.click()
    
    no_results = driver.find_element_by_id("no_results_message_div")
    
    print("{} is {}".format(course, "full" if no_results.is_displayed() else "not full"))
    
    driver.close()
    driver.quit()
    

# time.sleep(1)
driver.quit()
