import json
import bcrypt
from datetime import datetime

from django.http   import JsonResponse
from django.views  import View

from users.models  import User
from users         import utils

class SignUpView(View):

    def post(self, request):
        try:
            data            = json.loads(request.body)
            name            = data["name"]
            username        = data["username"]
            password        = data["password"]
            email           = data["email"]
            phone_number    = data["phone_number"]
            birthday        = data.get("birthday")
            is_sms_agreed   = data["is_sms_agreed"]
            is_email_agreed = data["is_email_agreed"]

            if not utils.validate_username(username):
                return JsonResponse({'MESSAGE': 'INVALID_USERNAME'}, status=400)

            if not utils.validate_password(password, username):
                return JsonResponse({'MESSAGE': 'INVALID_PASSWORD'}, status=400)

            if not utils.validate_email(email):
                return JsonResponse({'MESSAGE': 'INVALID_EMAIL'}, status=400)

            if not utils.validate_phone_number(phone_number):
                return JsonResponse({'MESSAGE': 'INVALID_PHONE_NUMBER'}, status=400)
            
            if not(utils.validate_boolean(is_sms_agreed) and 
                   utils.validate_boolean(is_email_agreed)):
                return JsonResponse({'MESSAGE': 'INVALID_BOOLEAN'}, status=400)
            
            if (utils.check_duplication({"username": username}) or
               utils.check_duplication({"email": email})):
                return JsonResponse({'MESSAGE': 'DUPLICATED_USER'}, status=400)

            if birthday:
                if not utils.validate_date(birthday):
                    return JsonResponse({'MESSAGE': 'INVALID_DATEFORM'}, status=400)

                birthday = datetime.strptime(birthday, '%Y%m%d').date()
            
            # password hashing
            password = bcrypt.hashpw(
                password.encode('utf-8'), 
                bcrypt.gensalt()
            )
            password = password.decode("utf-8")

            created_user = User.objects.create(
                name            = name,
                username        = username,
                password        = password,
                email           = email,
                phone_number    = phone_number,
                birthday        = birthday,
                is_sms_agreed   = is_sms_agreed,
                is_email_agreed = is_email_agreed
            )
            return JsonResponse({'MESSAGE': 'USER_CREATED'}, status=201)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'MESSAGE': 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)
        except TypeError:
            return JsonResponse({'MESSAGE': 'TYPE_ERROR'}, status=400)
        except AttributeError:
            return JsonResponse({'MESSAGE': 'ATTRIBUTE_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'MESSAGE': 'VALUE_ERROR'}, status=400)

class CheckUsernameDuplicationView(View):
    
    def get(self, request, username):
        if not utils.validate_username(username):
            return JsonResponse({'MESSAGE': 'INVALID_USERNAME'}, status=400)
        
        if utils.check_duplication({"username": username}):
            return JsonResponse({'DUPLICATION': True}, status=409)

        return JsonResponse({'DUPLICATION': False}, status=200)
 
class CheckEmailDuplicationView(View):

    def get(self, request, email):
        if not utils.validate_email(email):
            return JsonResponse({'MESSAGE': 'INVALID_EMAIL'}, status=400)

        if utils.check_duplication({"email": email}):
            return JsonResponse({'DUPLICATION': True}, status=409)

        return JsonResponse({'DUPLICATION': False}, status=200)

class SignInView(View):

    def post(self, request):
        try:
            data     = json.loads(request.body)
            username = data['username']
            password = data['password']
            
            if not utils.validate_username(username):
                return JsonResponse({'MESSAGE': 'INVALID_USERNAME'}, status=400)

            if not utils.validate_password(password, username):
                return JsonResponse({'MESSAGE': 'INVALID_PASSWORD'}, status=400)
            
            if not User.objects.filter(username=username).exists():
                return JsonResponse({'MESSAGE': 'WRONG_USERNAME'})
            
            accessing_user  = User.objects.get(username=username)
            password        = password.encode('utf-8')
            hashed_password = accessing_user.password.encode('utf-8')

            if not bcrypt.checkpw(password, hashed_password):
                return JsonResponse({'MESSAGE': 'WRONG_PASSWORD'})
            
            access_token = utils.generate_access_token(accessing_user.id)   
            return JsonResponse(
                {
                    'MESSAGE': "SIGNED_IN",
                    'TOKEN'  : access_token
                }, 
                status=200
            )
        except json.decoder.JSONDecodeError:
            return JsonResponse({'MESSAGE': 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)
        except TypeError:
            return JsonResponse({'MESSAGE': 'TYPE_ERROR'}, status=400)
