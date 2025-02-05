from django import forms
from .models import *

class UserForm(forms.ModelForm):
    class Meta():
        model = UserDetails
        fields = ['name', 'dob', 'gender', 'phone', 'address', 'id_proof', 'user_details']

class ComplaintForm(forms.ModelForm):
    class Meta():
        model = UserComplaint
        fields = ['subject','complaint','phone']
class StatusForm(forms.ModelForm):
    class Meta:
        model=  UserComplaint
        fields=['status','station']

class RequestForm(forms.ModelForm):
    class Meta:
        model = RequestLabour
        fields=['title','work_date','work_description','contact']

class WorkStatus(forms.ModelForm):
    class Meta():
        model = RequestLabour
        fields=['status']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model =LabourFeedback
        fields=['feedback']

