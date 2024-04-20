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

duo_auth_url = "https://api-05cb7de8.duosecurity.com"
auth_link = "https://app.testudo.umd.edu"
chrome_options = Options()
chrome_options.add_argument("--headless=new")
service = Service(executable_path="chromedriver.exe")
pattern = r'([A-Z]+)\s*(\d+)\s*\((\d+)\)'

def get_student_schedule_source(username, pwd):
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(auth_link)

    input_username = driver.find_element(By.NAME, "j_username")
    input_username.send_keys(username)

    input_password = driver.find_element(By.NAME, "j_password")
    input_password.send_keys(pwd + Keys.ENTER)

    time.sleep(2)

    try:
        print("Waiting for Duo Authentication...")
        button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".button--primary--full-width.button--primary.button--xlarge.size-margin-top-xlarge.size-margin-bottom-medium"))
        )
        print("Done!")
        button.click()
        time.sleep(7)
        source = driver.page_source
        driver.quit()
        return source
        

    except TimeoutError:
        print("Authentication failed... ")
        driver.quit()
        return None

def tuplify(raw_lst):
    final_lst = []
    for entry in raw_lst:
        matches = re.findall(pattern, entry)
        final_lst.append((matches[0][0] + matches[0][1],matches[0][2]))

    return final_lst

def get_course_list(uid, pwd):
    source = get_student_schedule_source(uid, pwd)
    if source == None:
        return None
    soup = BeautifulSoup(source, 'html.parser')

    divs = soup.find_all('div',class_='course-card-label ng-binding')
    raw_course_lst = []
    for div in divs:
        raw_course_lst.append(div.get_text(strip=True, separator='\n'))
    return (tuplify(raw_course_lst))