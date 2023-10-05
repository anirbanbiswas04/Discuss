from django.urls import path

from .views import account

urlpatterns = [
    path('account/', account, name='account'),
]