from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.views import View
from .forms import *
from django.contrib import messages

# Create your views here.
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



