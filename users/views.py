import json, datetime

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
            birthday        = None
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

            if "birthday" in data:
                birthday = data["birthday"]

                if not utils.validate_date(birthday):
                    return JsonResponse({'MESSAGE': 'INVALID_DATEFORM'}, status=400)

                birthday = int(birthday[:4]), int(birthday[4:6]), int(birthday[6:])
                birthday = datetime.date(*birthday)

            password = utils.hash_password(password)

            # create user account
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
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'MESSAGE': 'VALUE_ERROR'}, status=400)
        except TypeError:
            return JsonResponse({'MESSAGE': 'TYPE_ERROR'}, status=400)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'MESSAGE': 'JSON_DECODE_ERROR'}, status=400)
         
class CheckIdDuplicationView(View):

    def get(self, request):
        try:
            username = request.GET.get("username")

            if utils.check_duplication({"username": username}):
                return JsonResponse({'DUPLICATION': True}, status=200)

            return JsonResponse({'DUPLICATION': False}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'MESSAGE': 'VALUE_ERROR'}, status=400)
        except TypeError:
            return JsonResponse({'MESSAGE': 'TYPE_ERROR'}, status=400)
 
class CheckEmailDuplicationView(View):

    def get(self, request):
        try:
            email = request.GET.get("email")
            
            if utils.check_duplication({"email": email}):
                return JsonResponse({'DUPLICATION': True}, status=200)

            return JsonResponse({'DUPLICATION': False}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'MESSAGE': 'VALUE_ERROR'}, status=400)
        except TypeError:
            return JsonResponse({'MESSAGE': 'TYPE_ERROR'}, status=400)
