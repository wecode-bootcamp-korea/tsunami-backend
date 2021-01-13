from django.urls import path

from users.views import (
                         SignUpView, 
                         CheckIdDuplicationView, 
                         CheckEmailDuplicationView
                        )

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/idduplication', CheckIdDuplicationView.as_view()),
    path('/emailduplication', CheckEmailDuplicationView.as_view())
]
