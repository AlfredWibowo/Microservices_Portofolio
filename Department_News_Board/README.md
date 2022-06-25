# Department News Board

Application used to provide announcements on mobile applications / websites.

# User Service

## Login

Untuk masuk kedalam system dan membuat Session.

### Request

![my badge](https://badgen.net/badge/METHOD/POST/yellow) /user/login/

```json
{
   "username": <str>,
   "password": <str>
}
```

### Response

```json
{
   "status": "Success", 
   "message": "Login Successful", 
   "data": {
      "username": "user1", 
      "password": "passuser1"
   }
}
```

```json
{
   "status": "Error", 
   "message": "Wrong Username & Password"
}
```

```json
{
   "status": "Error", 
   "message": "You Already Login"
}
```

## Register

Untuk membuat akun agar dapat manage news.

### Request

![my badge](https://badgen.net/badge/METHOD/POST/yellow) /user/register/

```json
{
   "username": <str>,
   "password": <str>
}
```

### Response

```json
{
   "status": "Success", 
   "message": "Register Successful", 
   "data": {
      "username": "user3", 
      "password": "passuser3"
   }
}
```

```json
{
   "status": "Error", 
   "message": "Username Already Taken"
}
```

## Logout

Untuk menghapus session.

### Request

![my badge](https://badgen.net/badge/METHOD/GET/green) /user/logout/

### Response

```json
{
   "status": "Success", 
   "message": "Logout Successful", 
}
```

```json
{
   "status": "Error", 
   "message": "You Need to Login First"
}
```

# News Service

## Get All News

Untuk mendapatkan semua News terbaru (30 hari terakhir) dalam bentuk list of news. (Tidak perlu login)

### Request

![my badge](https://badgen.net/badge/METHOD/GET/green) /news/

### Response

```json
{
   "status": "Success",
   "data": [
      {
         "id": 1,
         "timestamp": "2022-06-24T00:00:00",
         "description": "news pertama ole user2"
      },
      {
         "id": 3,
         "timestamp": "2022-06-24T00:00:00",
         "description": "news ketiga oleh user2"
      }
   ]
}
```

```json
{
   "status": "Error", 
   "message": "News Does Not Exist / Archived"
}
```

## Get News by Id

Mendapatkan sebuah news berdasarkan ID yang diberikan. (Tidak perlu login)

### Request

![my badge](https://badgen.net/badge/METHOD/GET/green) /news/```<int:id>```/

### Response

```json
{
   "status": "Success",
   "data": {
      "id": 2,
      "timestamp": "2022-02-24T00:00:00",
      "description": "news kedua oleh user2"
   }
}
```

```json
{
   "status": "Error", 
   "message": "News Does Not Exist"
}
```

## Add News

Menambahkan news baru. (Perlu login)

### Request

![my badge](https://badgen.net/badge/METHOD/POST/yellow) /news/add/

```json
{
   "description": <str>,
}
```

### Response

```json
{
   "status": "Success", 
   "message": "News Added", 
   "data": {
      "id": 4, "timestamp": "2022-06-25T00:00:00", 
      "description": "news pertama oleh user1"
   }
}
```

```json
{
   "status": "Error", 
   "message": "Add News Failed"
}
```

```json
{
   "status": "Error", 
   "message": "You Need to Login First"
}
```

## Edit News

Mengupdate news berdasarkan id. (Perlu login)

### Request

![my badge](https://badgen.net/badge/METHOD/PUT/blue) /news/edit/```<int:id>```

```json
{
   "description": <str>,
}
```

### Response

```json
{
   "status": "Success", 
   "message": "News Edited", 
   "data": 
   {
      "id": 2,
      "timestamp": "2022-06-25T00:00:00",
      "description": "news 2 edited"
   }
}
```

```json
{
   "status": "Error", 
   "message": "Edit News Failed / News Does Not Exist"
}
```

```json
{
   "status": "Error", 
   "message": "You Need to Login First"
}
```

## Delete News

Mendelete news berdasarkan id. (Perlu login)

### Request

![my badge](https://badgen.net/badge/METHOD/DELETE/red) /news/delete/```<int:id>```

### Response

```json
{
   "status": "Success", 
   "message": "News Deleted", 
   "news_id": 1
}
```

```json
{
   "status": "Error", 
   "message": "News Does Not Exist"
}
```

```json
{
   "status": "Error", 
   "message": "You Need to Login First"
}
```
