from django.urls import path
from .views import *

urlpatterns=[
    path('feedback/',Feedback.as_view(),name='feedback'),
    path('editskill/',EditSkill.as_view(),name='edit_skill'),
]