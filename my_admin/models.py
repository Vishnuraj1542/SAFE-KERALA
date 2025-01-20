from django.db import models
from log_manager.models import LoginDetails

# Create your models here.
class StationDetails(models.Model):
    station_name=models.CharField(max_length=88,null=True,blank=True)
    station_number=models.IntegerField(null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    address=models.CharField(max_length=300,null=True,blank=True)
    station_image=models.ImageField(null=True,blank=True,upload_to='station_images')
    user_details=models.OneToOneField(LoginDetails,on_delete=models.CASCADE)
    phone=models.CharField(max_length=90,null=True,blank=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.station_name


class LabourDetails(models.Model):
    gender=[
        ('MALE','male'),
        ('FEMALE','female'),
        ('OTHER','other')

    ]
    name=models.CharField(max_length=50,null=True,blank=True)
    age=models.IntegerField(null=True,blank=True)
    gender=models.CharField(max_length=50,null=True,blank=True,choices=gender)
    aadhar_no=models.IntegerField(null=True,blank=True)
    skills=models.CharField(max_length=600,null=True,blank=True)
    phone=models.CharField(max_length=20,null=True,blank=True)
    alternative_phone=models.CharField(max_length=20,null=True,blank=True)
    user_details=models.OneToOneField(LoginDetails,models.CASCADE,null=True,blank=True)
    photo = models.ImageField(null=True, blank=True, upload_to='labour_gallery')
    id_image = models.ImageField(null=True, blank=True, upload_to='labour_gallery')
    ration_card = models.ImageField(null=True, blank=True, upload_to='labour_gallery')
    updated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Station: {self.name} (ID: {self.id})"