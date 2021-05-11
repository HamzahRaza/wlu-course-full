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
import pickle

class Student:
    def __init__(self, email):
        self.email = email

class Course:
    def __init__(self, code, full, waitlist, students):
        self.code = code
        self.full = full
        self.waitlist = waitlist
        self.students = students

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

test0000 = Student("test0000@mylaurier.ca") #test student
test0001 = Student("test0001@mylaurier.ca")

MA103 = Course("MA103", False, False, [test0000, test0001])
EM203 = Course("EM203", False, False, [test0000])
BF199 = Course("BF199", False, False, [test0000, test0001])
BU111 = Course("BU111", False, False, [test0001])
CS202 = Course("CS202", False, False, [test0001])
COURSES_NEW = [MA103, EM203, BF199, BU111, CS202]

STUDENTS = [test0000, test0001]
os = platform.system()

COURSES_OLD = pickle.load(open("courses", "rb")) #load state from "courses" file

if os == "Windows":
    driver_path = "C:/Users\%s\Downloads\chromedriver_win32\chromedriver.exe" % getpass.getuser()
elif os == "Linux":
    driver_path = "/home/%s/Downloads/chromedriver" % getpass.getuser()
#"darwin" is mac
for course in COURSES_NEW:
    driver = webdriver.Chrome(driver_path, options=options)
    driver.get("https://scheduleme.wlu.ca")
    driver.set_window_size(1920,1080) #required even in headless
    driver.implicitly_wait(10)

    winter = driver.find_element_by_id("term_202101")
    winter.click()
    
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'code_number')))
    search = driver.find_element_by_id("code_number")
    search.clear()
    search.send_keys(course.code)
    search.send_keys(Keys.RETURN)
    
    full_classes = driver.find_element_by_id("hide_full")
    full_classes.click()

    waitlistable_classes = driver.find_element_by_id("hide_waitlistable")
    waitlistable_classes.click()
    
    no_results_full = driver.find_element_by_id("no_results_message_div")
    course.full = no_results_full.is_displayed()
    
    waitlistable_classes.click()
    no_results_waitlist = driver.find_element_by_id("no_results_message_div")
    course.waitlist = not no_results_waitlist.is_displayed()
    
    driver.close()
    driver.quit()

if len(COURSES_OLD) == len(COURSES_NEW): #assumes ordering remains the same
    for x in range(len(COURSES_OLD)):
        if COURSES_OLD[x].full != COURSES_NEW[x].full and COURSES_NEW[x].full == False:
            #course went from full to not full
            for student in COURSES_NEW[x].students:
                print("%s: Space opened up in course %s" % (student.email, COURSES_NEW[x].code))
        elif COURSES_OLD[x].waitlist != COURSES_NEW[x].waitlist and COURSES_NEW[x].waitlist == True and COURSES_OLD[x].full == COURSES_OLD[x].full:
            #waitlist went from closed to open, and course did not just become full
            #full course just had an opening on the waiting list
            for student in COURSES_NEW[x].students:
                print("%s: Space opened up on waiting list for course %s" % (student.email, COURSES_NEW[x].code))

pickle.dump(COURSES_NEW, open("courses", "wb")) #save courses state to "courses" file
