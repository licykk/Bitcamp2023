CREATE TABLE customers (
    discord_id CHAR(50) PRIMARY KEY,
    customer_id CHAR(50)
);

CREATE TABLE accounts (
    account_id CHAR(50) PRIMARY KEY,
    customer_id CHAR(50)
);