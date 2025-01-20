from django.urls import path
from .views import *

urlpatterns=[
    path('registration/',UserRegistration.as_view(),name='userregistration')
]