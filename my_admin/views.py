from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.views import View
from .forms import *
from .models import *
from public.models import LabourFeedback
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
            username = request.POST.get('username')
            if LoginDetails.objects.filter(username=username).exists():
                messages.error(request,'username already exist', extra_tags='labour')
                return render(request, 'my_admin/station_register.html')
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
            messages.success(request,'station added sucessfully',extra_tags='labour')
            return redirect('log_manager:stationhome')
        else:
            messages.error(request,'an error occured please try again',extra_tags=labour)
            return render(request, 'my_admin/station_register.html', {'form': form})

                    #<----------viewstations---------->
class ViewStation(View):
    def get(self,request):
        station=StationDetails.objects.select_related('user_details').all()
        return render(request,'my_admin/view_stations.html',{'view':station})

#<----------------edit station----------------->
class EditStation(View):
    def get(self,request,id):
        data=StationDetails.objects.get(pk=id)
        return render(request,'my_admin/edit_station.html',{'let':data})
    def post(self,request,id):
        data=StationDetails.objects.get(pk=id)
        items=StationForm(request.POST,instance=data)
        if items.is_valid():
            items.save()
            return redirect('viewstations')
        return render(request,'my_admin/edit_station.html',{'let':data})

    #<----------delete station---------------->

class DeleteStation(View):
    def get(self,request,id):
        return render(request,'my_admin/confirmation.html')
    def post(self,request,id):
        data=StationDetails.objects.get(pk=id)
        data.delete()
        return redirect('viewstations')
    


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
                return render(request,'my_admin/labour_register.html')
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
            messages.success(request,'labour added sucessfully')
            return redirect('log_manager:adminhome')
        return render(request,'my_admin/labour_register.html',{'det':data})


#          <---------------labours list --------------->

class ViewLabours(View):
    def get(self,request):
        labours=LabourDetails.objects.select_related('user_details').all()
        return render(request,'my_admin/view_labours.html',{'labour':labours})

                   #   <----------- view criminals list------------->
class ListCriminals(View):
    def get(self,request):
        list=CriminalList.objects.all()
        return render(request,'my_admin/view_criminal.html',{'list':list})


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
            messages.success(request,'notification sent sucessfully',extra_tags='labour')
            return redirect('log_manager:adminhome')
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

#<-----------------------view feedback--------------------->
class WorkerFeedback(View):
    def get(self,request):
        data=Feedback.objects.all()
        return render(request,'my_admin/view_feedback.html',{'feed':data})
#     <-------------------feedback from the user about labour--------------->
class UserFeedback(View):
    def get(self,request):
        data=LabourFeedback.objects.all()
        return render(request,'my_admin/view_feedback.html',{'back':data})