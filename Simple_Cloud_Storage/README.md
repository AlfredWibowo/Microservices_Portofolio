# Simple Cloud Storage

a service that is used to upload and download files on the service

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
   "message": "Register Successful", 
}
```

```json
{
   "status": "Error", 
   "message": "You Need to Login First"
}
```

## Upload File

Merupakan fungsi yang digunakan untuk menaruh sebuah file pada service. Session berguna untuk menandai kepemilikan File. (Login Required) 

### Request

![my badge](https://badgen.net/badge/METHOD/POST/yellow) /storage/upload/

```json
{
   "file": <file>,
}
```

### Response

```json
{
  "status": "Success", 
  "message": "File Uploaded", 
  "data": {
    "id": 3, 
    "owner": "user1", 
    "file_name": "user1_Alfred_resume.docx"
   }
}
```

```json
{
   "status": "Error", 
   "message": "File Duplicate"
}
```

```json
{
   "status": "Error", 
   "message": "You Need to Login First"
}
```

## Download File

Merupakan sebuah fungsi yang digunakan untuk mendownload file yang terdapat pada service. Session digunakan untuk melakukan pengecekan apakah file tersebut dimiliki oleh user yang mengakses. (Login Required)

### Request

![my badge](https://badgen.net/badge/METHOD/GET/green) /storage/download/```<string:file_name>/```

### Response

File

```json
{
   "status": "Error", 
   "message": "Don't Have Access / File Does Not Exsist"
}
```

```json
{
   "status": "Error", 
   "message": "You Need to Login First"
}
```

## Download File

Merupakan sebuah fungsi yang digunakan untuk menshare file yang terdapat pada service agar file dapat didownload orang lain. Session digunakan untuk melakukan pengecekan apakah file tersebut dimiliki oleh user yang mengakses. (Login Required)

### Request

![my badge](https://badgen.net/badge/METHOD/POST/yellow) /storage/share/

```json
{
   "owner": <string>, 
   "share_to": <string>
   "file_name": <string>
}
```

### Response

```json
{
   "status": "Success", 
   "message": "File Already Shared"
   "data": {
       "id": "1", 
       "receiver": "User2"
       "file_name": "user1_Alfred_resume.docx"
    }
}
```

```json
{
   "status": "Error", 
   "message": "User Does Not Exist"
}
```

```json
{
   "status": "Error", 
   "message": "User Does Not Have Access"
}
```

```json
{
   "status": "Error", 
   "message": "File Already Shared"
}
```

