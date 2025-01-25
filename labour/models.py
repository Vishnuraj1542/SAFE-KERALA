from django.db import models
from my_admin.models import*


# Create your models here.
class Feedback(models.Model):
    sender=models.ForeignKey(LabourDetails,null=True,blank=True,on_delete=models.CASCADE)
    feedback=models.TextField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.sender.name