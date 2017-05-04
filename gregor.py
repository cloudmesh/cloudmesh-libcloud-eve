import requests
from pprint import pprint
import json

print ("services")
url = "http://127.0.0.1:5000"
response = requests.get(url)
pprint (response.json())

print ("flavor")
url = "http://127.0.0.1:5000/aws_flavor"
response = requests.get(url)
pprint (response.json())

print("add")

# hack

def curl(d):
    data = str(d).replace("'",'"') # hacking quoting,
                                   # maybe if we use a real json object not needed
    print (data)
    command = "curl -d '{}' -H 'Content-Type: application/json'  http://127.0.0.1:5000/aws_flavor".format(data)
    print (command)
    os.system(command)
    
flavor = {"bandwidth": "10", "disk": 20, "id": "1", "name": "f1", "price": 1.0, "ram": 40}

# curl(flavor)

print ("REQUEST")

import json

url = 'http://127.0.0.1:5000/aws_flavor'
headers = {"Content-Type": "application/json"}

r = requests.post(url, headers=headers, data=json.dumps(flavor))

print (r.text)
print ("flavor")
url = "http://127.0.0.1:5000/aws_flavor"
response = requests.get(url)
pprint (response.json())
