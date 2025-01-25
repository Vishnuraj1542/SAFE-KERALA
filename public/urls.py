from django.urls import path
from .views import *

urlpatterns=[
    path('registration/',UserRegistration.as_view(),name='userregistration'),
    path('complaint/',Complaint.as_view(),name='complaint')
]