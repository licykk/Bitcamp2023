# This is written for PYTHON 3
# Don't forget to install requests package

import requests
import json
import os

API_KEY = os.getenv('CAPITALONE_API_KEY')
print(API_KEY)
URL_PATH = 'http://api.nessieisreal.com/'

# Create customer, all arguments are strings
def create_customer(first_name, last_name, st_num, st_name, city, state, zip):
    url = '{}customers?key={}'.format(URL_PATH, API_KEY)
    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "address": {
            "street_number": st_num,
            "street_name": st_name,
            "city": city,
            "state": state,
            "zip": zip
        }
    }

    # Create a customer request
    response = requests.post( 
        url, 
        data=json.dumps(payload),
        headers={'content-type':'application/json'},
        )

    if response.status_code == 201:
        print('customer created')
    else: #raise error later 
        print("No customer created")

# Create account, all arguments are strings
def create_account(cust_id, act_type, nickname, rewards, balance, act_num):
    url = '{}customers/{}/accounts?key={}'.format(URL_PATH, cust_id, API_KEY)
    print(url)
    payload = {
        "type": act_type,
        "nickname": nickname,
        "rewards": rewards,
        "balance": balance,
        "account_number": act_num
    }

    # Create an account request
    response = requests.post( 
        url, 
        data=json.dumps(payload),
        headers={'content-type':'application/json'},
        )

    if response.status_code == 201:
        print('account created')
    else: #raise error later 
        print("No account created")
