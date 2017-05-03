import requests
from pprint import pprint


print ("services")
url = "http://127.0.0.1:5000"
response = requests.get(url)
pprint (response.json())

print ("flavors")




print ("flavor")
url = "http://127.0.0.1:5000/aws_flavor"
response = requests.get(url)
pprint (response.json())

