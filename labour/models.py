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
    labourer = models.ForeignKey(LabourDetails, on_delete=models.CASCADE, related_name="personal_issues")
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.labourer.username}"
