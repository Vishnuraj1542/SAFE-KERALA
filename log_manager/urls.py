from django.urls import path
from .views import *

app_name = 'log_manager'

urlpatterns=[
    path('',ForLogin.as_view(),name='userslogin'),
    path('userpage/',UserPage.as_view(),name='userhome'),
    path('adminpage/',AdminPage.as_view(),name='adminhome'),
    path('stationpage/',StationPage.as_view(),name='stationhome'),
    path('labourpage/',LabourPage.as_view(),name='labourhome'),
]