from django.db import models
from my_admin.models import*


# Create your models here.
class Feedback(models.Model):
    sender=models.ForeignKey(LabourDetails,null=True,blank=True,on_delete=models.CASCADE)
    feedback=models.TextField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.sender.name

class PersonalIssue(models.Model):
    labourer = models.ForeignKey(LabourDetails, on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.labourer.name

class LabourComplaint(models.Model):
    sender = models.ForeignKey(LoginDetails, on_delete=models.CASCADE, blank=True, null=True)
    complaint_text = models.TextField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reply = models.TextField(null=True, blank=True)
