from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.views import View
from .forms import *
from .models import *
from labour.models import *
from station.models import*
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
            return redirect('log_manager:stationhome')
        else:
            return render(request, 'my_admin/station_register.html', {'form': form})

                    #<----------viewstations---------->
class ViewStation(View):
    def get(self,request):
        station=StationDetails.objects.select_related('user_details').all()
        return render(request,'my_admin/view_stations.html',{'view':station})

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
        labours=LabourDetails.objects.select_related('user_details').all()
        return render(request,'my_admin/view_labours.html',{'labour':labours})

                   #   <----------- view criminals list------------->
class ListCriminals(View):
    def get(self,request):
        list=CriminalList.objects.all()
        return render(request,'station/view_criminal.html',{'list':list})


    #<----------view complaints-------------->
class ComplaintStatus(View):
    def get(self,request):
        details=Complaint.objects.all()
        return render(request,'my_admin/view_complaint.html',{'list':details})

# <--------------send notification to policestation ---------------->
class SendNotification(View):
    def get(self, request):
        police_stations = StationDetails.objects.all()
        return render(request, 'my_admin/send_notification.html', {'police_stations': police_stations})

    def post(self, request):
        police_station_id = request.POST.get('police_station')
        title = request.POST.get('title')
        message = request.POST.get('message')

        try:
            police_station = StationDetails.objects.get(id=police_station_id)
            Notification.objects.create(
                police_station=police_station,
                title=title,
                message=message
            )
            return HttpResponse('my_admin:send_notification')
        except StationDetails.DoesNotExist:
            return render(request, 'my_admin/send_notification.html', {
                'error': 'Invalid police station selected',
                'police_stations': StationDetails.objects.all(),
            })
#<-----------------------view labour personal problem--------------------------->
class LabourProblems(View):
    def get(self,request):
        problem=PersonalIssue.objects.all()
        return render(request,'my_admin/view_issue.html',{'problem':problem})
