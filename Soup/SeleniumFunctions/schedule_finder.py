import requests
from getpass import getpass
from bs4 import BeautifulSoup
from sel_script import get_student_schedule_source
import re

pattern = r'([A-Z]+)\s*(\d+)\s*\((\d+)\)'

def tuplify(raw_lst):
    final_lst = []
    for entry in raw_lst:
        matches = re.findall(pattern, entry)
        final_lst.append((matches[0][0] + matches[0][1],matches[0][2]))

    return final_lst

def get_course_list(uid, pwd):
    source = get_student_schedule_source(uid, pwd)
    soup = BeautifulSoup(source, 'html.parser')

    divs = soup.find_all('div',class_='course-card-label ng-binding')
    raw_course_lst = []
    for div in divs:
        raw_course_lst.append(div.get_text(strip=True, separator='\n'))
    return (tuplify(raw_course_lst))



