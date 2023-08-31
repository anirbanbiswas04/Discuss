from django.urls import path

from .views import my_account, else_account

urlpatterns = [
    path('my-account/', my_account, name='my-account'),
    path('<str:username>/', else_account, name='else-account'),
]