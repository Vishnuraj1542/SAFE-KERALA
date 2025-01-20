from django.urls import path
from .views import *

urlpatterns=[
    path('stationregistration/',StationRegistration.as_view(),name='stationregister'),
    path('labourregistration/',LabourRegistration.as_view(),name='labourregister'),
    path('viewstations/',ViewStation.as_view(),name='viewstations')
]