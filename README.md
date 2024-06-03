# Library service API

API allows to borrow books and return it. Also admins can create them.
Payments with Stripe

Technologies
Django Rest Framework,
Postgres,
Docker,
Stripe

## Run with Docker
Docker must be already installed

Copy .env-sample to .env and fill with all required data.

```shell 
docker-compose build
docker-compose up
```


Getting access
Creating user: /api/user/register/

Getting access token: /api/user/token/


### Features
- JWT authentication
- Admin panel
- Documentation
- CRUD operations for books
- CRUD operations for borrowing
- Retrieving borrowings by user
