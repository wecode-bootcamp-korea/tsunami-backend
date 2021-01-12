import json

from django.http  import JsonResponse
from django.views import View

from users.models  import User
# from user import utils



# before write this feature, shall be communicate with front-end
class SignUpStep1(View):

    def get(self, request):
        try:
            # sample = request.GET.get("article_id")
 
        return JsonResponse({})

        except:

class SignUpView(View):

    def post(self, request):
        try:
            data      = json.loads(request.body)

            email     = data['email']
            mobile    = data['mobile']
            username  = data['username']
            full_name = data['full_name']
            password  = data['password']
            mobile = ''.join(mobile.split('-'))
#            
#             # validation checking
#             if not utils.validate_email(email):
#                 return JsonResponse({'MESSAGE': 'INVALID_EMAIL'}, status=400)
#             
#             if not utils.validate_password(password):
#                 return JsonResponse({'MESSAGE': 'INVALID_PASSWORD'}, status=400)
#             
#             if mobile and not(utils.validate_mobile(mobile)):
#                 return JsonResponse({'MESSAGE': 'INVALID_MOBILE'}, status=400)
#             
#             if not username:
#                 return JsonResponse({'MESSAGE': 'BLANK_USERNAME'}, status=400)
#             
#             mobile = ''.join(mobile.split('-'))
#             
#             # existence check
#             if User.objects.filter(email = email).exists():
#                 return JsonResponse({'MESSAGE': 'EXISTENCE_ERROR'}, status=400)
#             
#             if User.objects.filter(username = username).exists():
#                 return JsonResponse({'MESSAGE': 'EXISTENCE_ERROR'}, status=400)
#             
#             if mobile and User.objects.filter(mobile_number = mobile).exists():
#                 return JsonResponse({'MESSAGE': 'EXISTENCE_ERROR'}, status=400)
# 
            # create user account
            created_user = User.objects.create(
                name          = name
                username      = username# actual users id_name
                password      = password
                email         = email,
                phone_number  = phone_number,
                birthday      = full_name, # input - frontend calendar
                sms_agree     = username,
                email_agree   = email_agree,
            )
            return JsonResponse({'MESSAGE': 'USER_CREATED'}, status=200)
# 
#         except:
#             return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)

class CheckIdDuplicationView(View):

    def get(self, request):
        
        try:
            username = request.GET.get("username")
            if User.objects.filter(username=username).exist():
                return JsonResponse({'Duplication': 1}, status=200)

            return JsonResponse({'Duplication': 0}, status=200)
        except:
            return JsonResponse({'MESSAGE': 'BAD_REQUEST'}, status=400)

class CheckEmailDuplicationView(View):
    def get(self, resquest):

        try:
            email = request.GET.get("email")
            if User.objects.filter(email=email).exist():
                return JsonResponse({'Duplication': 1}, status=200)

            return JsonResponse({'Duplication': 0}, status=200)
        except:
            return JsonResponse({'MESSAGE': 'BAD_REQUEST'}, status=400)



# def check_duplication()







