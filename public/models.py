from django.db import models
from log_manager.models import LoginDetails
from my_admin.models import StationDetails,LabourDetails


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
    def __str__(self):
        return self.name



class UserComplaint(models.Model):
    user=models.ForeignKey(UserDetails,null=True,blank=True,on_delete=models.CASCADE)
    station=models.ForeignKey(StationDetails,null=True,blank=True,on_delete=models.CASCADE)
    subject=models.CharField(max_length=100,null=True,blank=True)
    complaint=models.TextField(null=True,blank=True)
    status = models.CharField(max_length=40, default='pending',null=True,blank=True,choices=[
        ('pending', 'pending'),
        ('in progress', 'in progress'),
        ('resolved', 'resolved')
    ])
    phone=models.IntegerField(null=True,blank=True)
    created_at=models.DateField(auto_now_add=True,null=True)
    updated_at=models.DateField(auto_now_add=True,null=True)
    def __str__(self):
        return self.user.name


class RequestLabour(models.Model):
    user_id=models.ForeignKey(LoginDetails,on_delete=models.CASCADE,null=True,blank=True)
    labour_id=models.ForeignKey(LabourDetails,on_delete=models.CASCADE,null=True,blank=True)
    work_date=models.DateField(null=True,blank=True)
    title=models.CharField(max_length=50,null=True,blank=True)
    work_description=models.TextField(null=True,blank=True)
    contact=models.IntegerField(null=True,blank=True)
    status=models.CharField(max_length=30,default='pending',choices=[
        ('pending','pending'),
        ('accepted','accepted'),
        ('rejected', 'rejected'),
        ('completed','completed')
    ])
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


class LabourFeedback(models.Model):
    user=models.ForeignKey(UserDetails,on_delete=models.CASCADE,null=True,blank=True)
    labour=models.ForeignKey(LabourDetails,on_delete=models.CASCADE,null=True,blank=True)
    feedback=models.TextField(null=True,blank=True)
    created_at=models.DateField(auto_now_add=True)
    def __str__(self):
        return f"user about {self.labour.name}"


class Message(models.Model):
    sender = models.ForeignKey(LoginDetails,on_delete=models.CASCADE,related_name='public_sent_messages')
    receiver = models.ForeignKey(LoginDetails,on_delete=models.CASCADE,related_name='public_received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} at {self.timestamp}"



