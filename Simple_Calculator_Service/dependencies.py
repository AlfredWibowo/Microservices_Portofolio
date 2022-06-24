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