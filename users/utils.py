import re
import jwt

from django.http  import JsonResponse

from users.models import User
import my_settings

def check_duplication(field_pair):
    return User.objects.filter(**field_pair).exists()

def validate_username(username):
    return (
        (len(re.findall(r'[a-zA-Z0-9]',username)) == len(username)) and 
        (5 <= len(username) <= 16)
    )

def validate_password(password, username):
    minimum_length = 6
    maximum_length = 16
    mixed_checker  = 0

    if re.findall(r'[!@#$%^?_~]',password):
        mixed_checker += 1
    
    if re.findall(r'[a-zA-Z]',password):
        mixed_checker += 1

    if re.findall(r'[0-9]', password):
        mixed_checker += 1

    mixed              = (mixed_checker >= 2)
    is_not_same        = (password != username) 
    valid_length       = (minimum_length <= len(password) <= maximum_length) 
    allowed_characters = (
        len(re.findall(r'[!@#$%^?_~a-zA-Z0-9]',password)) == 
        len(password)
    )
    return (mixed and is_not_same and valid_length and allowed_characters)

def validate_email(email):
    return re.findall(r"^.+@[0-9a-zA-Z_-]+\..+$", email)

def validate_phone_number(phone_number):
    correct_length = 11
    return (
        (re.match(r'[0-9]+', phone_number).group() == phone_number) and
        (len(re.findall(r'[0-9]', phone_number)) == correct_length)
    )

def validate_date(date_str):
    correct_length = 8
    return (
        (re.match(r'[0-9]+', date_str).group() == date_str) and
        (len(re.findall(r'[0-9]', date_str)) == correct_length)
    )

def validate_boolean(true_or_false):
    return type(true_or_false) == type(True)

def generate_access_token(user_id):
    payload = {
        'user_id' : user_id
    }
    access_token = jwt.encode(
        payload, 
        my_settings.SECRET_KEY, 
        algorithm = my_settings.ALGORITHM
    )
    return access_token

def login_required(function):
    
    def wrapper(view_self, request, *args, **kwargs):
        try:
            access_token = request.headers.get("Authorization")

            if not access_token:
                return JsonResponse({'MESSAGE': 'LOGIN_REQUIRED'}, status=401)
            
            header = jwt.decode(
                access_token, 
                my_settings.SECRET_KEY, 
                algorithms = my_settings.ALGORITHM
            )

            if not User.objects.filter(id = header['user_id']).exists():
                return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=400)
            
            setattr(request, "user", User.objects.get(id = header['user_id']))
            return function(view_self, request, *args, **kwargs)
        except jwt.exceptions.DecodeError:
            return JsonResponse({'MESSAGE': 'JWT_DECODE_ERROR'}, status=400)

    return wrapper

def check_login(function):
    
    def wrapper(view_self, request, *args, **kwargs):
        try:
            access_token = request.headers.get("Authorization")

            if not access_token:
                return function(view_self, request, *args, **kwargs)
            
            header = jwt.decode(
                access_token, 
                my_settings.SECRET_KEY, 
                algorithms = my_settings.ALGORITHM
            )

            if not User.objects.filter(id = header['user_id']).exists():
                return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=400)
            
            setattr(request, "user", User.objects.get(id = header['user_id']))
            return function(view_self, request, *args, **kwargs)
        except jwt.exceptions.DecodeError:
            return JsonResponse({'MESSAGE': 'JWT_DECODE_ERROR'}, status=400)

    return wrapper
