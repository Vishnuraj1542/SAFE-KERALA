from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from .forms import *
from .models import *
from django.contrib import messages

# Create your views here.

# <-----------------station registration---------------->
class StationRegistration(View):
    def get(self, request):
        form = StationForm()
        return render(request, 'my_admin/station_register.html', {'form': form})

    def post(self, request):
        form = StationForm(request.POST, request.FILES)
        if form.is_valid():
            item = LoginDetails.objects.create_user(
                username=request.POST['username'],
                email=request.POST['email'],
                password=request.POST['password'],
                status='verified',
                user_type='POLICESTATION'
            )
            station = form.save(commit=False)
            station.user_details = item
            station.save()
            return redirect('stationhome')
        else:
            return render(request, 'my_admin/station_register.html', {'form': form})

                          #--viewstations--
class ViewStation(View):
    def get(self,request):
        station=StationDetails.objects.select_related('user_details').all()
        return render(request,'my_admin/viewstation.html',{'view':station})

  #<-------------labour registration ---------------->

class LabourRegistration(View):
    def get(self,request):
        return render(request,'my_admin/labour_register.html')
    def post(self,request):
        data=LabourForm(request.POST,request.FILES)
        if data.is_valid():
            username=request.POST.get('username')
            if LoginDetails.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose a different one.')
                return render('my_admin/labour_register.html',{'msg':messages})
            item = LoginDetails.objects.create_user(
                username=request.POST['username'],
                email=request.POST['email'],
                password=request.POST['password'],
                status='verified',
                user_type='LABOUR'
            )
            labour=data.save(commit=False)
            labour.user_details=item
            labour.save()
            return redirect('log_manager:labourhome')
        return render(request,'my_admin/labour_register.html',{'det':data})


#    <---------------labours list --------------->

class ViewLabours(View):
    def get(self,request):
        labours=LabourDetails.objects.selected_related('user_details').all()
        return render(request,'my_admin/viewlabours.html')