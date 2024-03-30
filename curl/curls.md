# CURL Samples

## Token

```bash
curl -X POST "http://localhost:8000/api/token/" -H "Content-Type: application/json" -d '{
    "username": "your_username",
    "password": "your_password"
}'
```

## Account

```bash
# GET
curl -X GET "http://localhost:8000/accounts/?per_page=10&page=1" -H "Authorization: Bearer your_access_token"

# POST
curl -X POST "http://localhost:8000/accounts/" -H "Authorization: Bearer your_access_token" -H "Content-Type: application/json" -d '{
   "name": "Savings Account",
   "account_type": "savings",
   "balance": 1000
}'

# PUT
curl -X PUT "http://localhost:8000/accounts/" -H "Authorization: Bearer your_access_token" -H "Content-Type: application/json" -d '{
   "id": 1,
   "name": "New Savings Account Name",
   "account_type": "savings",
   "balance": 1500
}'

# DELETE
curl -X DELETE "http://localhost:8000/accounts/" -H "Authorization: Bearer your_access_token" -H "Content-Type: application/json" -d '{
   "id": 1
}'
```

## Category

```bash
# GET
curl -X GET "http://localhost:8000/categories/?per_page=10&page=1" -H "Authorization: Bearer your_access_token"

# POST
curl -X POST "http://localhost:8000/categories/" -H "Authorization: Bearer your_access_token" -H "Content-Type: application/json" -d '{
   "name": "New Category",
   "description": "Category description"
}'

# PUT
curl -X PUT "http://localhost:8000/categories/" -H "Authorization: Bearer your_access_token" -H "Content-Type: application/json" -d '{
   "id": 1,
   "name": "Updated Category Name",
   "description": "Updated category description"
}'

# DELETE
curl -X DELETE "http://localhost:8000/categories/" -H "Authorization: Bearer your_access_token" -H "Content-Type: application/json" -d '{
   "id": 1
}'
```

## Transaction

```bash
# GET
curl -X GET "http://localhost:8000/transactions/?per_page=10&page=1" -H "Authorization: Bearer your_access_token"

# POST
curl -X POST "http://localhost:8000/transactions/" -H "Authorization: Bearer your_access_token" -H "Content-Type: application/json" -d '{
   "account": 1,
   "amount": 100.50,
   "type": "income",
   "category": 1,
   "date": "2022-04-01",
   "description": "New Transaction",
   "metadata": {}
}'

# PUT
curl -X PUT "http://localhost:8000/transactions/" -H "Authorization: Bearer your_access_token" -H "Content-Type: application/json" -d '{
   "id": 1,
   "account": 2,
   "amount": 200.75,
   "type": "expense",
   "category": 2,
   "date": "2022-04-02",
   "description": "Updated Transaction",
   "metadata": {}
}'

# DELETE
curl -X DELETE "http://localhost:8000/transactions/" -H "Authorization: Bearer your_access_token" -H "Content-Type: application/json" -d '{
   "id": 1
}'

```

## User

```bash
# GET
curl -X GET "http://localhost:8000/user/" -H "Authorization: Bearer your_access_token"

# POST
curl -X POST "http://localhost:8000/user/" -H "Content-Type: application/json" -d '{
   "email": "test@example.com",
   "password": "password",
   "password2": "password"
}'

# DELETE
curl -X DELETE "http://localhost:8000/user/" -H "Authorization: Bearer your_access_token"

# GET Request to Reset Password
curl -X GET "http://localhost:8000/reset-password/" -H "Authorization: Bearer your_access_token"

# POST Reset Password
curl -X POST "http://localhost:8000/reset-password/" -H "Authorization: Bearer your_access_token" -H "Content-Type: application/json" -d '{
   "password": "new_password",
   "password2": "new_password"
}'

```
