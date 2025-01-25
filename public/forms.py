from django import forms
from .models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ['name', 'dob', 'gender', 'phone', 'address', 'id_proof', 'user_details']

class ComplaintForm(forms.ModelForm):
    class Meta():
        model = UserComplaint
        fields = ['subject','complaint','phone']

