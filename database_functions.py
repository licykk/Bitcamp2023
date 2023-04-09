from math import floor
import os
import random
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from models import Customer, CheckingAccount

# The code below inserts new accounts.

def create_customer_db(session, discord_id, customer_id):
    print("Creating new account...")

    new_customer = []
    new_customer.append(Customer(discord_id=discord_id, customer_id=customer_id))
    print(f"Saving new customer with id {discord_id}.")
    session.add_all(new_customer)

def create_account_db(session, customer_id, account_id):
    print("Creating new account...")

    new_account = []
    new_account.append(CheckingAccount(account_id=account_id, customer_id=customer_id))
    print(f"Saving new account with id {new_account} for customer {customer_id}.")
    session.add_all(new_account)


def get_customer_db(session, discord_id):
    print("Getting customer id...")
    try:
        customer = session.query(Customer).filter(Customer.discord_id == discord_id).one()
    except NoResultFound:
        print("No customer was found")
    except MultipleResultsFound:
        print("Multiple customers were found")
    
    return customer.customer_id

def get_account_db(session, customer_id):
    print("Getting account id...")
    try:
        account = session.query(CheckingAccount).filter(CheckingAccount.customer_id == customer_id).one()
    except NoResultFound:
        print("No account was found")
    except MultipleResultsFound:
        print("Multiple accounts were found")

    return account.account_id

# if __name__ == '__main__':
#     # For cockroach demo:
#     # DATABASE_URL=postgresql://demo:<demo_password>@127.0.0.1:26257?sslmode=require
#     # For CockroachCloud:
#     # DATABASE_URL=postgresql://<username>:<password>@<globalhost>:26257/<cluster_name>.defaultdb?sslmode=verify-full&sslrootcert=<certs_dir>/<ca.crt>
#     db_uri = os.environ['DATABASE_URL'].replace("postgresql://", "cockroachdb://")
#     try:
#         engine = create_engine(db_uri, connect_args={"application_name":"docs_simplecrud_sqlalchemy"})
#     except Exception as e:
#         print("Failed to connect to database.")
#         print(f"{e}")

#     seen_account_ids = []

