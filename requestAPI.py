import requests
import ast

response = requests.post('http://127.0.0.1:5000/checkBalance?IBAN=NI99ABNA01234567')
D2 = ast.literal_eval(response.text)
print(response)
print(D2.get('data'))