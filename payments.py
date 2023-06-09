# This is written for PYTHON 3
# Don't forget to install requests package

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('CAPITALONE_API_KEY')
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
        resp = response.json()
        cust_id = resp['objectCreated']['_id']
        return cust_id
    else: #raise error later 
        print("No customer created")

    return None #error occurred
    
    

# Create account, all arguments are strings except rewards and balance are int
#checking accounts only
def create_account(cust_id, act_type, nickname, rewards, balance, act_num):
    url = '{}customers/{}/accounts?key={}'.format(URL_PATH, cust_id, API_KEY)
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
        resp = response.json()
        acct_id = resp['objectCreated']['_id']
        return acct_id
    else: #raise error later 
        print("No account created")

    return None #error occurred



# Initiate transaction, all arguments are strings
# medium usually 'balance'
# all arguments are string except amt as int (this must be int! mb double allowed)
def create_transaction(src_act_id, medium, dest_act_id, description, amt):
    # balance checking of sender and amt to send
    url = '{}accounts/{}?key={}'.format(URL_PATH, src_act_id, API_KEY)
    response = requests.get( 
        url, 
        headers={'content-type':'application/json'},
        )

    if response.status_code == 200:
        resp = response.json()
        if resp['balance'] >= amt:
            url = '{}accounts/{}/transfers?key={}'.format(URL_PATH, src_act_id, API_KEY)
            payload = {
                "medium": medium,
                "payee_id": dest_act_id,
                "transaction_date": "2023-04-08",
                "description": description,
                "amount": amt
            }

            # Create an account request
            response = requests.post( 
                url, 
                data=json.dumps(payload),
                headers={'content-type':'application/json'},
                )

            if response.status_code == 201:
                print('transaction created')
                resp = response.json()
                transaction_id = resp['objectCreated']['_id']
                return transaction_id
            else: #raise error later 
                print("No transaction created")

        # end if
        else:
            print('Insufficient funds to transfer')
    else:
        print('Error checking failed')

    return None #error occurred

# obtain a dictionary from account number to balance of a specified customer
def get_cust_accounts(cust_id: str):
    url = '{}customers/{}/accounts?key={}'.format(URL_PATH, cust_id, API_KEY)

    response = requests.get( 
        url, 
        headers={'content-type':'application/json'},
        )


    if response.status_code == 200:
        print('Successful retrieval')
        acct_balc = {}
        resp = response.json()

        for i in resp:
            acct = i['_id']
            balance = i['balance']
            acct_balc[acct] = balance

        return acct_balc
    
    return None #error ocurred

def count_cust_accounts(cust_id: str):
    url = '{}customers/{}/accounts?key={}'.format(URL_PATH, cust_id, API_KEY)

    response = requests.get( 
        url, 
        headers={'content-type':'application/json'},
        )

    if response.status_code == 200:
        print('Successful retrieval')
        resp = response.json()
        return len(resp)
    
    else:
        return -1
    