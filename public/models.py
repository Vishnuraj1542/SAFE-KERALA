from django.db import models
from log_manager.models import LoginDetails

# Create your models here.
class UserDetails(models.Model):
    name=models.CharField(max_length=55,null=True,blank=True)
    dob=models.DateField(null=True,blank=True)
    gender=models.CharField(max_length=33,blank=True,null=True,choices=[
        ('MALE', 'Male'),
        ('FEMALE', 'Female')])
    phone=models.IntegerField(null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    id_proof=models.ImageField(null=True,blank=True,upload_to='public_gallery')
    user_details=models.ForeignKey(LoginDetails,on_delete=models.CASCADE,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
