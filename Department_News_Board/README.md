# Department News Board

Application used to provide announcements on mobile applications / websites.

# User Service

## Login

### Request
![my badge](https://badgen.net/badge/METHOD/POST/yellow) /user/login/

```json

```

### Response

```json
{
   "result": <int>
}
```

## Register

![my badge](https://badgen.net/badge/METHOD/POST/yellow) /user/register/

```json
{
   "result": <int>
}
```

# News Service

## Get All News

![my badge](https://badgen.net/badge/METHOD/GET/green) /news/

```json
{
   "result": <int>
}
```

## Get All News by ID

![my badge](https://badgen.net/badge/METHOD/GET/green) /news/```<int:id>```/

```json
{
   "result": <int>
}
```

## Add News

![my badge](https://badgen.net/badge/METHOD/POST/yellow) /news/add/

```json
{
   "result": <int>
}
```

## Edit News

![my badge](https://badgen.net/badge/METHOD/PUT/blue) /news/edit/```<int:id>```/

```json
{
   "result": <int>
}
```

## Delete

![my badge](https://badgen.net/badge/METHOD/DELETE/red) /news/delete/```<int:id>```/

```json
{
   "result": <int>
}
```
