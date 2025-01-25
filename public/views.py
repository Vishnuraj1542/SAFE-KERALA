from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from .forms import *
from .models import *
from log_manager.models import LoginDetails
from django.contrib import messages
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