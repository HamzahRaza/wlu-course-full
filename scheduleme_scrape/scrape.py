"""
------------------------------------------------------------------------
Scrape data from schedule me for given course code
------------------------------------------------------------------------
"""


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import getpass
import platform

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

COURSES = ["MA103", "EM203", "MA122", "BF199"]
os = platform.system()

for course in COURSES:
    if os == "Windows":
        driver_path = "C:/Users\%s\Downloads\chromedriver_win32\chromedriver.exe" % getpass.getuser()
    elif os == "Linux":
        driver_path = "/home/%s/Downloads/chromedriver" % getpass.getuser()
    #"darwin" is mac


    driver = webdriver.Chrome(driver_path, options=options)
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

    waitlistable_classes = driver.find_element_by_id("hide_waitlistable")
    waitlistable_classes.click()
    
    no_results_full = driver.find_element_by_id("no_results_message_div")
    class_full = no_results_full.is_displayed()
    
    print("{} is {}".format(course, "full" if class_full else "not full"), end ="")

    waitlistable_classes.click()
    no_results_waitlist = driver.find_element_by_id("no_results_message_div")

    if class_full and not no_results_waitlist.is_displayed():
        print(", but space on the waitlist is available")
    else:
        print()


    driver.close()
    driver.quit()
    

# time.sleep(1)
driver.quit()
