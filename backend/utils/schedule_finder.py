import requests
from getpass import getpass
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from getpass import getpass
import time
import os

duo_auth_url = "https://api-05cb7de8.duosecurity.com"
auth_link = "https://sso.canvaslms.com/delegated_auth_pass_through?target=https%3A%2F%2Fumd.instructure.com%2F"
chrome_options = Options()
chrome_options.add_argument("--headless=new")
abs_path = os.path.dirname(os.path.abspath(__file__)) + "/chromedriver.exe"
service = Service(executable_path=fr"{abs_path}")
pattern = r'[A-Z]+\d+'

def check_auth(driver):
    try:
        thing = driver.find_element(By.CLASS_NAME, "form-error")
        return False
    except:
        return True
    
def get_student_schedule_source(username, pwd):
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(auth_link)

    input_username = driver.find_element(By.NAME, "j_username")
    input_username.send_keys(username)

    input_password = driver.find_element(By.NAME, "j_password")
    input_password.send_keys(pwd + Keys.ENTER)

    time.sleep(2)

    if(not(check_auth(driver))):
        print("Invalid Password or Username")
        return None
    
    try:
        print("Waiting for Duo Authentication...")
        button = WebDriverWait(driver, 180).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".button--primary--full-width.button--primary.button--xlarge.size-margin-top-xlarge.size-margin-bottom-medium"))
        )
        print("Done!")
        button.click()
        time.sleep(6)
        button2 = driver.find_element(By.ID, "global_nav_courses_link")
        button2.click()
        time.sleep(2)
        source = driver.page_source
        driver.quit()
        return source
        

    except TimeoutError:
        print("Authentication failed... ")
        driver.quit()
        return None

def purify(raw_lst):
    final_lst = []
    for entry in raw_lst:
        string = entry[:7]
        if re.match(pattern, string):
            final_lst.append(string)

    return final_lst

def get_course_list(uid, pwd):
    source = get_student_schedule_source(uid, pwd)
    if source == None:
        return None
    soup = BeautifulSoup(source, 'html.parser')
    
    divs = soup.find_all('a', class_='css-102w4y0-view-link')
    raw_course_lst = []
    for div in divs:
        raw_course_lst.append(div.get_text(strip=True, separator='\n'))

    print(purify(raw_course_lst))
    return (purify(raw_course_lst))

if __name__ == '__main__':
    print(get_course_list("avinod", getpass("Enter PWD: ")))