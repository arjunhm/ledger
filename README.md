## Setup

To install required packages, run  
`pip install -r requirements.txt`  

Create `.env` file with the following content
```
SECRET_KEY="<your-secret-key>"
DEBUG=True
ALLOWED_HOSTS=[]
DB_NAME="ledger_db"
DB_USER="postgres"
DB_PASSWORD="root"
DB_HOST="localhost"
DB_PORT="5432"
```

Run `python manage.py migrate` to migrate the DB schema

## Running the server

Run `python manage.py runserver` to start the server.

## Features

Supports the following
- Create User
- Create Accounts (Savings, Checking, Credit Card)
- Add/Edit Transactions

## Making API calls

You can find the API calls in `curl/curls.md`

