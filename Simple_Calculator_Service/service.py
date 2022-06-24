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