import json
import bcrypt
<<<<<<< HEAD
from datetime        import datetime
=======
from secrets import token_urlsafe
from datetime import datetime
>>>>>>> main

from django.http     import JsonResponse
from django.views    import View

from users.models    import User, UserProductLike
from users           import utils
from products.models import Product

class SignUpView(View):

    def post(self, request):
        try:
            data            = json.loads(request.body)
            print(data)
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
            
            if not birthday:
                birthday = None

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
                return JsonResponse({'MESSAGE': 'WRONG_USERNAME'}, status=400)
            
            accessing_user  = User.objects.get(username=username)
            password        = password.encode('utf-8')
            hashed_password = accessing_user.password.encode('utf-8')

            if not bcrypt.checkpw(password, hashed_password):
                return JsonResponse({'MESSAGE': 'WRONG_PASSWORD'}, status=400)
            
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

class FindUsernameView(View):

    def post(self, request):
        try:
            data  = json.loads(request.body)
            name  = data['name']
            email = data['email']
            
            if not utils.validate_email(email):
                return JsonResponse({'MESSAGE': 'INVALID_EMAIL'}, status=400)
            
            forgotten_users = User.objects.filter(name=name, email=email)
            
            if not forgotten_users.exists():
                return JsonResponse({'MESSAGE': 'WRONG_USER'}, status=400)

            forgotten_user = forgotten_users[0]
            return JsonResponse({
                "USERNAME"  : forgotten_user.username[:-3]+ "*" * 3,
                "CREATED_AT": forgotten_user.created_at
            }, status=200)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'MESSAGE': 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)
        except TypeError:
            return JsonResponse({'MESSAGE': 'TYPE_ERROR'}, status=400)
 
class MakeTemporaryPasswordView(View):

    def post(self, request):
        try:
            data     = json.loads(request.body)
            username = data['username']
            name     = data['name']
            email    = data['email']

            if not utils.validate_username(username):
                return JsonResponse({'MESSAGE': 'INVALID_USERNAME'}, status=400)

            if not utils.validate_email(email):
                return JsonResponse({'MESSAGE': 'INVALID_EMAIL'}, status=400)

            if User.objects.filter(
                    username = username, 
                    name     = name, 
                    email    = email
                ).exists():
                
                forgotten_user  = User.objects.get(username=username)
                new_password = token_urlsafe()[:16]

                forgotten_user.password = bcrypt.hashpw(
                    new_password.encode('utf-8'), 
                    bcrypt.gensalt()
                ).decode("utf-8")

                forgotten_user.save()
                utils.send_temp_password_mail(
                    name     = name,
                    username = username,
                    email    = email,
                    password = new_password,
                )

                return JsonResponse({'MESSEAGE': "MAIL_SENT"}, status=200)
            return JsonResponse({'MESSAGE': 'WRONG_USER'}, status=400)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'MESSAGE': 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)
        except TypeError:
            return JsonResponse({'MESSAGE': 'TYPE_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'MESSAGE': 'VALUE_ERROR'}, status=400)

class UserProductLikeView(View):
    @utils.login_required
    def post(self, request):
        try:
            data    = json.loads(request.body)
            user    = getattr(request,'user',None)
            product = Product.objects.get(id=data['product'])
            like   = UserProductLike.objects.filter(user=user, product=product).first()

            if like:
                like.is_like = not like.is_like
                like.save()
                
                return JsonResponse({'LIKE': like.is_like}, status=200)
            UserProductLike.objects.create(user=user, product=product, is_like=True)

            return JsonResponse({'LIKE': True}, status=200)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'MESSAGE': 'JSON_DECODE_ERROR'}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE':"PRODUCT_DOSENT_EXIST"} ,status=400)
