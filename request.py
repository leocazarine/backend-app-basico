import requests

url = "http://192.168.0.14:5001/post_new_consent"

payload = {'name': 'From Test',
           'cpf': '000.000.000-00'}
files = [

]
headers = {}

response = requests.request(
    "POST", url, headers=headers, data=payload, files=files)

print(response.text)
