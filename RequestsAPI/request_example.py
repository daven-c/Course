import requests
from getpass import getpass
import json 

my_email = input("enter ur user email: ")
my_password = getpass("enter ur pwd: ")

data = {
    'email': my_email,
    'password': my_password
}

response = requests.post("https://dozuki.umd.edu/api/2.0/user/token", data=json.dumps(data))

if response.status_code == 200:
    print(response.text)
else:
    print("Error:", response.status_code)
    print("Response body:", response.text)