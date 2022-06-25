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

### Django

Use the package manager pip to install django.

```bash
pip install django
```

### Usage:

- Starting django project

```bash
django-admin startproject <project_name>
```

- Run server

```bash
cd <project_name>
manage.py runserver
```

- Create ```celery.py``` in the project folder where the ```settings.py``` file exists:

```python
import os
from celery import Celery

# setting the Django settings module.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_task.settings')
app = Celery('celery_task')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Looks up for task modules in Django applications and loads them
app.autodiscover_tasks()
```

- Add this code in the ```__init__.py``` file within the package where ```settings.py``` file is located:

```python
from .celery import app as celery_app

__all__ = ['celery_app']
```

- Create celery task at root folder with:

```bash
python manage.py startapp task
```

- Create ```task.py``` in task folder

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

- Create response of result in ```views.py```

```python
from django.shortcuts import render
import json
from django.http import HttpResponse
from task.task import prime_task, palindrome_task, prime_palindrome_task

# Create your views here.

def create_response(result):
    response_data = {
        'result': result
    }
    return json.dumps(response_data)

def prime(request, index):
    result = prime_task.delay(index)
    response = create_response(result)
    return HttpResponse(response, content_type="application/json")

def palindrome(request, index):
    result = palindrome_task.delay(index)
    response = create_response(result,)
    return HttpResponse(response, content_type="application/json")

def prime_palindrome(request, index):
    result = prime_palindrome_task.delay(index)
    response = create_response(result)
    return HttpResponse(response, content_type="application/json")
```

- Create response in ```views.py```

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

- For testing, open ```localhost:8000``` in browser


# Calculator Service

![my badge](https://badgen.net/badge/METHOD/GET/yellow) /prime/```<int:index>```/

```json
{
   "result": <int>
}
```

![my badge](https://badgen.net/badge/METHOD/GET/yellow) /palindrome/```<int:index>```/

```json
{
   "result": <int>
}
```

![my badge](https://badgen.net/badge/METHOD/GET/yellow) /prime_palindrome/```<int:index>```/

```json
{
   "result": <int>
}
```

