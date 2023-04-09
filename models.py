from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Customer(Base):
    """The Customer class corresponds to the "customer" database table.
    """
    __tablename__ = 'customers'
    discord_id = Column(String, primary_key=True)
    customer_id = Column(String)
    

class CheckingAccount(Base):
    """The Account class corresponds to the "accounts" database table.
    """
    __tablename__ = 'accounts'
    account_id = Column(String, primary_key=True)
    customer_id = Column(String)
