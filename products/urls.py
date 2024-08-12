# products/urls.py

from django.urls import path
from .views import login_view, register_view, logout_view, product_list_view, product_view

urlpatterns = [
    path('', login_view, name='login'),  # Default to login page
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('products/', product_list_view, name='product_list'),
    path('product/<str:product_file>/', product_view, name='product_view'),
]
