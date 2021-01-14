from django.urls import path

from users.views import (
                         SignUpView, 
                         SignInView,
                         CheckUsernameDuplicationView, 
                         CheckEmailDuplicationView
                        )

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/duplication/username/<str:username>', CheckUsernameDuplicationView.as_view()),
    path('/duplication/email/<str:email>', CheckEmailDuplicationView.as_view())
]
