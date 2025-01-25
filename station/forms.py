from django import forms
from .models import *

class CriminalForm(forms.ModelForm):
    class Meta:
        model=CriminalList
        fields=['fullname','height','weight','offenses','incident_summary','image']