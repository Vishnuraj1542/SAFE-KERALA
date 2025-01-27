from django import forms
from .models import *

class FeedbackForm(forms.ModelForm):
    class Meta():
        model=Feedback
        fields=['feedback']

class PersonalIssueForm(forms.ModelForm):
    class Meta:
        model = PersonalIssue
        fields = ['title', 'description']