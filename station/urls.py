from django.urls import path
from .views import *

urlpatterns=[
    path('addcriminals/',AddCriminals.as_view(),name='add_criminals'),
    path('criminalslist/',ViewCriminals.as_view(),name='view_criminals'),
    path('editcriminals/<int:id>',EditCriminals.as_view(),name='editcriminals'),
    path('feedback/',ViewFeedback.as_view(),name='view_feedback'),
    path('complaints/',ViewComplaints.as_view(),name='view_complaints'),
    path('changestatus/<int:id>',ComplaintStatus.as_view(),name='change_status')
]