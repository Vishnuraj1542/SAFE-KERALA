from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.views import View
from public.models import*
from .forms import *
from .models import *
from log_manager .models import LoginDetails
from my_admin.models import *

# Create your views here.

# <----------------user registration------------------->
class UserRegistration(View):
    def get(self,request):
        return render(request,'user/registration.html')

    def post(self, request):
        form = UserForm(request.POST, request.FILES)
        username = request.POST.get('username')
        if LoginDetails.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken. Please try something else.')
            return render(request, 'user/registration.html', {'form': form})
        if form.is_valid():
            item = LoginDetails.objects.create_user(
                username=username,
                email=request.POST['email'],
                password=request.POST['password'],
                status='verified',
                user_type='USER'
            )
            sent = form.save(commit=False)
            sent.user_details = item
            sent.save()

            messages.success(request, 'Registration successful!')
            return redirect('log_manager:userhome')
        return render(request, 'user/registration.html', {'form': form})


#           <-------------------send complaints ----------------->

class Complaint(View):
    def get(self,request):
        return render(request,'user/send_complaint.html')
    def post(self,request):
        user_id=request.session['login_id']
        user_name=UserDetails.objects.get(user_details=user_id)
        if not user_id:
            return redirect('log_manager:userslogin')
        data=ComplaintForm(request.POST)
        if data.is_valid():
            field=data.save(commit=False)
            field.user=user_name
            field.save()
            return redirect('log_manager:userhome')
        return render(request,'user/send_complaint.html',{'data':data})


                #<------search labour based on the skills ------------>
class LabourSearch(View):
    def get(self, request):
        skill = request.GET.get('skill')
        context = {}
        if skill:
            persons = LabourDetails.objects.filter(skills__icontains=skill)
            context['persons'] = persons
            context['skill'] = skill
        else:
            context['error'] = "Please provide a skill to search."
        return render(request, 'user/view_labours.html', context)

#<--------------------------view all the labours ------------------------>
class ViewLabour(View):
    def get(self,request):
        labours=LabourDetails.objects.select_related('user_details').all()
        return render(request,'user/view_labours.html',{'labour':labours})

#<-------------------requestlabour----------------------->
class RequestLabours(View):
    def get(self,request,id):
        labours = get_object_or_404(LabourDetails, pk=id)
        return render(request, 'user/request_labour.html', {'lab': labours})
    def post(self,request,id):
        user_pk=request.session['login_id']
        if 'login_id' not in request.session:
            messages.error(request, "You must be logged in to request labour.")
            return redirect('log_manager:userslogin')
        user=get_object_or_404(LoginDetails,pk=user_pk)
        labours = get_object_or_404(LabourDetails, pk=id)
        data=RequestForm(request.POST)
        if data.is_valid():
            item=data.save(commit=False)
            item.user_id=user
            item.labour_id=labours
            item.save()
            return redirect('request_status')
        return render(request,'user/request_labour.html')
#<----------------------request status--------------------->
class RequestStatus(View):
    def get(self,request):
        user_id=request.session['login_id']
        user = get_object_or_404(LoginDetails,pk=user_id)
        state=RequestLabour.objects.filter(user_id=user)
        return render(request,'user/request_status.html',{'state':state})

    #<------------- send feedback about labour----------------->
class FeedBack(View):
    def get(self,request,id):
        return render(request,'user/feedback.html')
    def post(self,request,id):
        users_id=request.session['login_id']
        user_name = UserDetails.objects.get(user_details=users_id)
        labours=LabourDetails.objects.get(pk=id)
        text=FeedbackForm(request.POST)
        if text.is_valid():
            obj=text.save(commit=False)
            obj.user=user_name
            obj.labour=labours
            obj.save()
            return redirect('viewlabour')
        return render(request,'user/feedback.html')











