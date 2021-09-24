# API Documentation

### 1. Create User

`[POST] /api/v1/user/create/`

Request:
```
{
    "email":"testuser@gmail.com",
    "password": "Test@12345",
    "firstname": "Test",
    "lastname": "User"
}
```

Response:
```
{
    "email":"testuser@gmail.com",
    "firstname": "Test",
    "lastname": "User"
}
```

### 2. Get a token

`[POST] /api/v1/user/token/`

Request:
```
{
    "email":"testuser@gmail.com",
    "password": "Test@12345"
}
```

Response:
```
{
    token: "ae0a11a141ff735937930430a29f9a0fed110e4f"
}
```

### 3. Fetch Movie Details

`[GET] /api/v1/user/me/`

Headers:
Authorization: Token ae0a11a141ff735937930430a29f9a0fed110e4f

Request:
```
{}
```
Response:
```
{
    "email":"testuser@gmail.com",
    "firstname": "Test",
    "lastname": "User"
}
```
