from django.urls import path
from .views import *

urlpatterns=[
    path('feedback/',Feedback.as_view(),name='feedback'),
    path('editskill/',EditSkill.as_view(),name='edit_skill'),
    path('personalissue/',Personal.as_view(),name='personal_issue'),
    path('viewissue/',ViewIssue.as_view(),name='view_issue'),
    path('edit-issue/<int:id>',EditIssue.as_view(),name='edit_issue'),
    path('delete-issue/<int:id>',DeleteIssue.as_view(),name='delete_issue'),
    path('submit_complaint/',SubmitComplaint.as_view(), name='submit_complaint'),
    path('complaintreply/',ViewReply.as_view(),name='complaint_reply'),
    path('viewrequests/',ViewRequest.as_view(),name='view_request'),
    path('workstatus/<int:id>/',ChangeWorkStatus.as_view(),name='work_status')
]