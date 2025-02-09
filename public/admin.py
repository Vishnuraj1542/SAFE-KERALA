from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserDetails)
admin.site.register(UserComplaint)
admin.site.register(RequestLabour)
admin.site.register(LabourFeedback)
admin.site.register(Message)


