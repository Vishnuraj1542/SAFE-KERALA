from django.urls import path
from .views import *

urlpatterns=[
    path('stationregistration/',StationRegistration.as_view(),name='stationregister'),
    path('labourregistration/',LabourRegistration.as_view(),name='labourregister'),
    path('viewstations/',ViewStation.as_view(),name='viewstations'),
    path('editstation/<int:id>/',EditStation.as_view(),name='editstation'),
    path('deletestation/<int:id>/',DeleteStation.as_view(),name='deletestation'),
    path('viewlabours/',ViewLabours.as_view(),name='viewlabours'),
    path('criminallist/',ListCriminals.as_view(),name='criminallist'),
    path('sendnotification/', SendNotification.as_view(), name='send_notification'),
    path('labour-problems/',LabourProblems.as_view(),name='labour_problems'),
    path('labourfeedback',WorkerFeedback.as_view(),name='labour_feed'),
    path('userfeedback',UserFeedback.as_view(),name='user_feed')
]