# Library service API

API allows to borrow books and return it. Also admins can create them.

Technologies
Django Rest Framework,
Postgres,
Docker

## Run with Docker
Docker must be already installed

Copy .env-sample to .env and fill with all required data.
#### Note: superuser is created automatically with .env info if no users exist in database.

```shell 
docker-compose build
docker-compose up
```


Getting access
Creating user: /api/user/register/

Getting access token: /api/user/token/


### Features ⭐
- JWT authentication (with logout function)
- Admin panel via /admin/
- Documentation via /api/doc/swagger/
- CRUD operations for books
- CRUD operations for borrowing
- Retrieving borrowings by user
