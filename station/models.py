from django.db import models
from my_admin.models import *
from log_manager.models import *

# Create your models here.
class CriminalList(models.Model):
    fullname=models.CharField(max_length=88,null=True,blank=True)
    image=models.ImageField(null=True,blank=True,upload_to='criminal_gallery')
    login_details=models.ForeignKey(LoginDetails,on_delete=models.CASCADE,null=True,blank=True)
    labour=models.ForeignKey(LabourDetails,on_delete=models.CASCADE,null=True,blank=True)
    station=models.ForeignKey(StationDetails,on_delete=models.CASCADE,null=True,blank=True)
    height=models.IntegerField(null=True,blank=True)
    weight=models.IntegerField(null=True,blank=True)
    incident_summary=models.TextField(null=True,blank=True)
    offenses=models.CharField(max_length=100,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
