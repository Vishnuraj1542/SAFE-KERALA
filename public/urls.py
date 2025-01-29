from django.urls import path
from .views import *

urlpatterns=[
    path('registration/',UserRegistration.as_view(),name='userregistration'),
    path('complaint/',Complaint.as_view(),name='complaint'),
    path('searchlabour/', LabourSearch.as_view(), name='search_labour'),
    path('viewlabour/', ViewLabour.as_view(), name='viewlabour'),
    path('sendrequest/<int:id>/',RequestLabours.as_view(),name='request_worker'),
    path('requeststatus/',RequestStatus.as_view(),name='request_status'),
    path('labourfeedback/<int:id>/',FeedBack.as_view(),name='labour_feedback')
]