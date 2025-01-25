from django import forms
from .models import *


class StationForm(forms.ModelForm):
    class Meta():
        model=StationDetails
        fields = [
            'station_name',
            'station_number',
            'description',
            'address',
            'station_image',
            'phone'
        ]

class LabourForm(forms.ModelForm):
    class Meta:
        model=LabourDetails
        fields = ['name','age','gender','aadhar_no','skills','phone',
                  'alternative_phone','photo','id_image','ration_card']