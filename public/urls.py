from django.urls import path
from .views import *

urlpatterns=[
    path('registration/',UserRegistration.as_view(),name='userregistration'),
    path('complaint/',Complaint.as_view(),name='complaint'),
    path('searchlabour/', LabourSearch.as_view(), name='search_labour'),
]