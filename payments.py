# This is written for PYTHON 3
# Don't forget to install requests package

import requests
import json
import os

customerId = '6431a6c89683f20dd51877d1'
apiKey = os.getenv('CAPITALONEAPI')

url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(customerId,apiKey)
payload = {
  "type": "Savings",
  "nickname": "test",
  "rewards": 10000,
  "balance": 10000,	
}
# Create a Savings Account
response = requests.post( 
	url, 
	data=json.dumps(payload),
	headers={'content-type':'application/json'},
	)

if response.status_code == 201:
	print('account created')

print(response)
print(response.content)
print(response.headers)
