from django.urls import path

from .views import (
    ProductListView,
    ProductDetailView,
    MainpageProductView
)

urlpatterns = [
    path('/', ProductListView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/main',MainpageProductView.as_view())
]
