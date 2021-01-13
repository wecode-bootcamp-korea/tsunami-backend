from django.urls import path

from .views import (
    ProductListView,
    ProductDetailView,
)

urlpatterns = [
    path('/productlist', ProductListView.as_view()),
    path('/productdetail', ProductDetailView.as_view()),
]
