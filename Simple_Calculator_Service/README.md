# Simple Calculator Service

This calculator application is used to display numbers (prime/palindrome/prime&palindrome) at the nth index.

## Technology

- [Celery](https://docs.celeryq.dev/en/stable/)
- [Django](https://www.djangoproject.com/)

## Installation

### Celery

Use the package manager pip to install celery.

```bash
pip install celery
```

Usage:

```python
from celery import shared_task

def is_prime(num):
    factor = 0
    for i in range(1, num + 1):
        if num % i == 0:
            factor += 1

    return factor == 2

def is_palindrome(num):
    original = num
    reverse = 0
    tmp = int(num)

    while tmp != 0:
        left = tmp % 10
        reverse = reverse * 10 + left
        tmp = int(tmp / 10)

    return original == reverse

@shared_task
def prime_task(index):
    result = []
    n = 0
    counter = 0
    while n != index + 1:
        if is_prime(counter):
            result.append(counter)
            n += 1
        counter += 1

    return result[index]

@shared_task
def palindrome_task(index):
    result = []
    n = 0
    counter = 0
    while n != index + 1:
        if is_palindrome(counter):
            result.append(counter)
            n += 1
        counter += 1

    return result[index]

@shared_task
def prime_palindrome_task(index):
    result = []
    n = 0
    counter = 0
    while n != index + 1:
        if is_prime(counter) and is_palindrome(counter):
            result.append(counter)
            n += 1
        counter += 1

    return result[index]
```

### Django

Use the package manager pip to install django.

```bash
pip install django
```

Usage:

- Starting django project

```bash
django-admin startproject <project_name>
```

- Run server

```bash
cd <project_name>
manage.py runserver
```

- Create response service

```python
import json
from django.http import HttpResponse
from dependencies import prime_task, palindrome_task, prime_palindrome_task

def create_response(result):
    response_data = {
        'result': result
    }
    return json.dumps(response_data)

def prime(request, index):
    result = prime_task(index)
    response = create_response(result)
    return HttpResponse(response, content_type="application/json")

def palindrome(request, index):
    result = palindrome_task(index)
    response = create_response(result,)
    return HttpResponse(response, content_type="application/json")

def prime_palindrome(request, index):
    result = palindrome_task(index)
    response = create_response(result)
    return HttpResponse(response, content_type="application/json")
```

- Create url path

```python
from django.urls import path
from service import prime, palindrome, prime_palindrome

urlpatterns = [
    #path('admin/', admin.site.urls),

    path('prime/<int:index>/', prime),
    path('palindrome/<int:index>/', palindrome),
    path('prime_palindrome/<int:index>/', prime_palindrome),
]
```

# Calculation Service

![my badge](https://badgen.net/badge/METHOD/GET/yellow) /```(prime/palindrome/prime_palindrome)```/```<int:index>```/

```json
{
   "result": <int>
}
```


