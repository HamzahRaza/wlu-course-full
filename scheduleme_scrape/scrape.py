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
import boto3
import pandas as pd


class Student:
    def __init__(self, email):
        self.email = email
    
    def __str__(self):
        return "{}".format(self.email)


class Course:
    def __init__(self, code, full, waitlist, students):
        self.code = code
        self.full = full
        self.waitlist = waitlist
        self.students = students

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.code == other.code
        return False

    def __gt__(self, other):
        if isinstance(other, self.__class__):
            return max(self.code.upper(), other.code.upper()) == self.code
        return False

    def __ge__(self, other):
        if isinstance(other, self.__class__):
            return self.code == other.code or max(
                self.code.upper(), other.code.upper()) == self.code
        return False

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return min(self.code.upper(), other.code.upper()) == self.code
        return False

    def __le__(self, other):
        if isinstance(other, self.__class__):
            return self.code == other.code or min(
                self.code.upper(), other.code.upper()) == self.code
        return False

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.code == other.code
        return False

    def __str__(self):
        return "code: {}, full: {}, waitlist: {}, students: {}".format(self.code, self.full, self.waitlist, self.students)

def aws_scan():
    db = boto3.resource('dynamodb', region_name="us-east-1")
    table = db.Table('wlu-course-full').scan()
    df = pd.DataFrame.from_dict(table["Items"])
    df['course'] = df['course'].str.lower()
    gdf = df.groupby(['course', 'term'])['email'].apply(",".join).reset_index()
    return gdf

def update(): #to pull new data from aws and fill up COURSES_NEW array with course objects based on new data
    df = aws_scan()
    COURSES_NEW = []

    for i in df.index:
        studentsList = df['email'][i].split(",") #list of students emails for course i
        students  = [] #list of student objects
        for student in studentsList:
            students.append(Student(student))
        COURSES_NEW.append(Course(df['course'][i], False, False, students))
        
    COURSES_NEW.sort(key=lambda x: x.code, reverse=False)
    
    # STUDENTS = [test0000, test0001]
    return COURSES_NEW#, STUDENTS

#selenium options
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

# COURSES_NEW, STUDENTS = update()
COURSES_NEW = update()

os = platform.system()

COURSES_OLD = pickle.load(open("courses",
                               "rb"))  #load state from "courses" file

if os == "Windows":
    driver_path = "C:/Users\%s\Downloads\chromedriver_win32\chromedriver.exe" % getpass.getuser(
    )
elif os == "Linux":
    driver_path = "/home/%s/Downloads/chromedriver" % getpass.getuser()
elif os == "Darwin":
    driver_path = "/Users/%s/downloads" % getpass.getuser()
#"darwin" is mac
for course in COURSES_NEW:
    driver = webdriver.Chrome(driver_path, options=options)
    driver.get("https://scheduleme.wlu.ca")
    driver.set_window_size(1920, 1080)  #required even in headless
    driver.implicitly_wait(10)

    winter = driver.find_element_by_id("term_202201")
    winter.click()

    WebDriverWait(driver,
                  10).until(EC.element_to_be_clickable((By.ID, 'code_number')))
    search = driver.find_element_by_id("code_number")
    search.clear()
    search.send_keys(course.code)
    search.send_keys(Keys.RETURN)

    full_classes = driver.find_element_by_id("hide_full")
    full_classes.click()
    #If the course is full, will be hidden at this point

    waitlistable_classes = driver.find_element_by_id("hide_waitlistable")
    waitlistable_classes.click()

    no_results_full = driver.find_element_by_id("no_results_message_div")
    course.full = no_results_full.is_displayed() #if no results message is displayed, the course is full

    waitlistable_classes.click()
    no_results_waitlist = driver.find_element_by_id("no_results_message_div")
    course.waitlist = not no_results_waitlist.is_displayed()

    driver.close()
    driver.quit()

new_index = 0
for old_index in range(
        len(COURSES_OLD)):  #compare old with new, make changes if necessary
    if COURSES_OLD[old_index] != COURSES_NEW[new_index]:
        if len(COURSES_OLD) > len(COURSES_NEW):
            #course removed, skip over COURSES_OLD entry
            continue
        elif len(COURSES_OLD) < len(COURSES_NEW):
            #course(s) added, skip over COURSES_NEW entry/entries
            while COURSES_OLD[old_index] != COURSES_NEW[new_index]:
                new_index += 1

    if COURSES_OLD[old_index].full != COURSES_NEW[
            new_index].full and COURSES_NEW[new_index].full == False:
        #course went from full to not full
        for student in COURSES_NEW[new_index].students:
            print("%s: Space opened up in course %s" %
                  (student.email, COURSES_NEW[new_index].code))
    elif COURSES_OLD[old_index].waitlist != COURSES_NEW[
            new_index].waitlist and COURSES_NEW[
                new_index].waitlist == True and COURSES_OLD[
                    old_index].full == COURSES_NEW[new_index].full:
        #waitlist went from closed to open, and course did not just become full
        #full course just had an opening on the waiting list
        for student in COURSES_NEW[new_index].students:
            print("%s: Space opened up on waiting list for course %s" %
                  (student.email, COURSES_NEW[new_index].code))

    new_index += 1
    if new_index > len(COURSES_NEW) - 1:
        #the case of the newly removed course(s) being the last element(s)
        #the case of newly added course(s) being the last element implicitly handled by COURSES_OLD being smaller, and thus ending where the new course(s) begin
        break

pickle.dump(COURSES_NEW, open("courses",
                              "wb"))  #save courses state to "courses" file
