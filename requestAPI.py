import requests
import ast

while True:
    APIlogout = requests.post('http://145.24.22.43:8050/logout', data={'IBAN:output'}).status_code
    if APIlogout == 208:
        break
