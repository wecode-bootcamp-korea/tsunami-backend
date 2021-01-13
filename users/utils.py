import re

import bcrypt
import jwt

from django.http   import JsonResponse

from users.models import User
import my_settings

def check_duplication(field_pair):
    if User.objects.filter(**field_pair).exists():
        return True

    return False

def validate_username(username):
    if len(re.findall(r'[a-zA-Z0-9]',username)) != len(username):
        return False

    if not(5 <= len(username) <= 16):
        return False
    
    return True

def validate_password(password, username):
    minimum_length = 6
    maximum_length = 16
    mixed_checker = 0

    if password == username:
        return False
    
    if not(minimum_length <= len(password) <= maximum_length):
        return False
    
    if len(re.findall(r'[!@#$%^?_~a-zA-Z0-9]',password)) != len(password):
        return False

    if re.findall(r'[!@#$%^?_~]',password):
        mixed_checker += 1
    
    if re.findall(r'[a-zA-Z]',password):
        mixed_checker += 1

    if re.findall(r'[0-9]', password):
        mixed_checker += 1

    if not(mixed_checker >= 2):
        return False
    
    return True

def validate_email(email):
    if not re.findall(r"^.+@[0-9a-zA-Z_-]+\..+$", email):
        return False 
    
    return True

def validate_phone_number(phone_number):
    if not re.match(r'[0-9]+', phone_number).group() == phone_number:
        return False 
    
    if not len(re.findall(r'[0-9]', phone_number)) == 11:
        return False

    return True

def validate_date(date_str):
    if not re.match(r'[0-9]+', date_str).group() == date_str:
        return False 
    
    if not len(re.findall(r'[0-9]', date_str)) == 8:
        return False
    
    return True

def validate_boolean(true_or_false):
    if type(true_or_false) != type(True):
        return False

    return True

def hash_password(str_password):
    hashed_password = bcrypt.hashpw(
            str_password.encode('utf-8'), 
            bcrypt.gensalt()
            )
    return hashed_password.decode('utf-8')

def check_password(password, hashed_password):
    password        = password.encode('utf-8')
    hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password, hashed_password)

def login_required(function):
    
    def wrapper(view_self, request, *args, **kwargs):
        try:
            access_token = request.headers["Authorization"]
            header = jwt.decode(
                    access_token,
                    my_settings.SECRET,
                    algorithms = my_settings.ALGORITHM
                    )
            if not User.objects.filter(id = header['user_id']).exists():
                return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=400)
            
            setattr(request, "user", User.objects.get(id = header['user_id']))

            return function(view_self, request, *args, **kwargs)
        except:
            return JsonResponse({'MESSAGE': 'LOGIN_REQUIRED'}, status=401)

    return wrapper
