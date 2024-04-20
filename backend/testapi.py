import requests as rq

root = "http://127.0.0.1:5000"
resp = rq.get(root + "/get_student/dchangiz")
print(resp)