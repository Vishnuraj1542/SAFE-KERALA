from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from my_admin.models import*
from log_manager import*
from my_admin.forms import *
from log_manager import *
from django.views import View
from .forms import *
from django.contrib import messages

# Create your views here.

# <----------send feedback--------------->
class Feedback (View):
    def get(self,request):
        return render(request,'labour/feedback.html')
    def post(self,request):
        labour=request.session['login_id']
        if not labour:
            return redirect('log_manager:userslogin')
        user=LabourDetails.objects.get(user_details=labour)
        data=FeedbackForm(request.POST)
        if data.is_valid():
            list=data.save(commit=False)
            list.sender=user
            list.save()
            messages.success(request, "Feedback shared successfully!")
            return redirect('log_manager:labourhome')
        return render(request,'log_manager:labour/feedback.html')

#<-------------------add and manage skills ---------------->
class EditSkill(View):
    def get(self,request):
        user_id=request.session['login_id']
        labour=LabourDetails.objects.get(user_details=user_id)
        return render(request,'labour/manage_skill.html',{'labour':labour})
    def post(self,request):
        user_id = request.session['login_id']
        labour = get_object_or_404(LabourDetails, user_details=user_id)
        data=LabourForm(request.POST,instance=labour)
        if data.is_valid():
            data.save()
            return redirect('log_manager:labourhome')
        return render(request,'labour/manage_skill.html',{'labour':labour})

#<----------------add and manage personal issue------------------>
class Personal(View):
    def get(self,request):
        return render(request,'labour/personal_issue.html')
    def post(self,request):
        labour=request.session['login_id']
        log_id=LabourDetails.objects.get(user_details=labour)
        data=PersonalIssueForm(request.POST)
        if data.is_valid():
            log=data.save(commit=False)
            log.labourer=log_id
            log.save()
            return redirect('log_manager:labourhome')
        return render(request,'labour/personal_issue.html')
