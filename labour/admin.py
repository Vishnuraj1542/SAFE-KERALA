from django.contrib import admin
from .models import Feedback,PersonalIssue,LabourComplaint

# Register your models here.
admin.site.register(Feedback)
admin.site.register(PersonalIssue)
admin.site.register(LabourComplaint)
