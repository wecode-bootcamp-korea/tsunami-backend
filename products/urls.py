from django.urls import path

from .views import (
    ProductListView,
    ProductDetailView,
    MainProductView
)

urlpatterns = [
    path('/', ProductListView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/main',MainProductView.as_view()),
]
