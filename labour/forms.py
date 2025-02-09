from django import forms
from .models import *
from my_admin.models import LabourDetails

class FeedbackForm(forms.ModelForm):
    class Meta():
        model=Feedback
        fields=['feedback']

class PersonalIssueForm(forms.ModelForm):
    class Meta:
        model = PersonalIssue
        fields = ['title', 'description']

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = LabourComplaint
        fields = ['complaint_text']
        widgets = {
            'complaint_text': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
class SkillForm(forms.ModelForm):
    class Meta():
        model=LabourDetails
        fields=['skills']