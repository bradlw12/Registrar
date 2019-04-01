from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import sys

def login(username, password):
    try:
        driver.find_element_by_id('submit_button')
    except NoSuchElementException:
        print("no sign-in needed")
    enterUser = driver.find_element_by_xpath('//*[@id="weblogin_netid"]')
    enterUser.send_keys(username)
    enterPass = driver.find_element_by_xpath('//*[@id="weblogin_password"]')
    enterPass.send_keys(password)
    signedIn = driver.find_element_by_id('submit_button')
    signedIn.click()

def get_SLN():
    lecture_num = int(input('How many lecture codes: '))
    dictionary = {}
    for i in range(lecture_num):
        lecture_code = input('     Enter Lecture SLN: ')
        quiz_num = int(input('How many quiz codes: '))
        quiz_list = []
        for j in range(quiz_num):
            quiz_sln = input('     Enter Quiz SLN: ')
            quiz_list.append(quiz_sln)
        dictionary[lecture_code] = quiz_list
    return dictionary


def add(depart, dict, username, password):
    driver.get('https://sdb.admin.uw.edu/timeschd/uwnetid/tsstat.asp?QTRYR=SPR+2019&CURRIC=' + depart)
    login(username, password)
    tries = 0
    quit = False
    lecture = ''
    quiz = ''
    while quit == False:
        tries = tries + 1
        print('Looking for ' + depart + ' class...')
        print('      Attempt ', + tries)
        time.sleep(45)
        driver.get('https://sdb.admin.uw.edu/timeschd/uwnetid/tsstat.asp?QTRYR=SPR+2019&CURRIC=' + depart)
        for i in dict:
            seats_l = driver.find_element_by_xpath('//a[contains(text(), \'' + i + '\')]//ancestor::td/following-sibling::th')
            if int(seats_l.text) > 0 and not dict.get(i):
                lecture = i
                quit = True
            elif int(seats_l.text) > 0:
                lecture = i
                for j in dict.get(i):
                    seats_q = driver.find_element_by_xpath('//a[contains(text(), \'' + j + '\')]//ancestor::td/following-sibling::th')
                    if int(seats_q.text) > 0:
                        quiz = j
                        quit = True
    return lecture, quiz

def register(drop_list, lecture, quiz):
    driver.get('https://sdb.admin.uw.edu/students/UWNetID/register.asp')
    enterLecture = driver.find_element_by_xpath('//*[@id="regform"]/p[2]/table/tbody/tr[2]/td[1]/input')
    enterLecture.send_keys(lecture)
    if quiz != '':
        enterQuiz = driver.find_element_by_xpath('//*[@id="regform"]/p[2]/table/tbody/tr[3]/td[1]/input')
        enterQuiz.send_keys(quiz)
    update = driver.find_element_by_xpath('//*[@id="regform"]/input[7]')
    for i in drop_list:
        drop = driver.find_element_by_xpath('//tt[contains(text(), \'' + i + '\')]//ancestor::td/preceding-sibling::td')
        drop.click()
    update.click()
    print('I pressed submit !!! wow this is exciting')

def drop():
    num = int(input('How many classes you do need to drop? '))
    drop_list = []
    for i in range(num):
        drop_list.append(input('     SLN of class to drop: '))
    return drop_list

# run the stuff
username = input('USERNAME? ')
password = input('PASSWORD? ')
sys.stderr.write("\x1b[2J\x1b[H")
depart = input('What is the department name? ').upper()
dict = get_SLN()
sys.stderr.write("\x1b[2J\x1b[H")
drop_list = drop()
sys.stderr.write("\x1b[2J\x1b[H")
driver = webdriver.Chrome()
lecture, quiz = add(depart, dict, username, password)
register(drop_list, lecture, quiz)
