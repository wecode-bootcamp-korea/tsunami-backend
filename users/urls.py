from django.urls import path

from users.views import (
    SignUpView, 
    SignInView,
    CheckUsernameDuplicationView, 
    CheckEmailDuplicationView,
    FindUsernameView,
    MakeTemporaryPasswordView,
    UserProductLikeView
)

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/duplication/username/<str:username>', CheckUsernameDuplicationView.as_view()),
    path('/duplication/email/<str:email>', CheckEmailDuplicationView.as_view()),
    path('/username', FindUsernameView.as_view()),
    path('/password', MakeTemporaryPasswordView.as_view()),
    path('/like', UserProductLikeView.as_view())
]
