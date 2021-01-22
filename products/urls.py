from django.urls import path

from .views import (
    ProductListView,
    ProductDetailView,
    MainProductView
)

urlpatterns = [
    path('/', ProductListView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
<<<<<<< HEAD
    path('/main',MainProductView.as_view())

=======
    path('/main',MainProductView.as_view()),
>>>>>>> 326a433f1ca9180058801801fe3d6e43b8f5564e
]
