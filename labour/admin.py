from django.contrib import admin
from .models import Feedback,PersonalIssue

# Register your models here.
admin.site.register(Feedback)
admin.site.register(PersonalIssue)
