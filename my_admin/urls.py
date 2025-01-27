from django.urls import path
from .views import *

urlpatterns=[
    path('stationregistration/',StationRegistration.as_view(),name='stationregister'),
    path('labourregistration/',LabourRegistration.as_view(),name='labourregister'),
    path('viewstations/',ViewStation.as_view(),name='viewstations'),
    path('viewlabours/',ViewLabours.as_view(),name='viewlabours'),
    path('criminallist/',ListCriminals.as_view(),name='criminallist'),
    path('sendnotification/', SendNotification.as_view(), name='send_notification'),
]