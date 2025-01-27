from django.contrib import admin
from .models import StationDetails,LabourDetails,Notification

# Register your models here.
admin.site.register(StationDetails)
admin.site.register(LabourDetails)
admin.site.register(Notification)
