from django.views import View
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from.models import *
from public.forms import *
from public.models import *
from labour.models import *
from station.models import *
from .forms import *
from log_manager.models import *
from my_admin.models import *
from django.contrib import messages



  # <----------------add criminal ----------->
class AddCriminals(View):
    def get(self,request):
        CriminalForm()
        return render(request,'station/add_criminal.html')
    def post(self,request):
        user_id=request.session['login_id']
        name=StationDetails.objects.get(user_details=user_id)
        data=CriminalForm(request.POST,request.FILES)
        if data.is_valid():
            item=data.save(commit=False)
            item.station=name
            item.save()
            return HttpResponse('criminal added sucessfully')
        return render(request,'station/add_criminal.html')

    # <------------view criminal list----------------->

class ViewCriminals(View):
    def get(self,request):
        list=CriminalList.objects.all()
        return render(request,'station/view_criminal.html',{'list':list})

#<----------------------edit criminals list---------->
class EditCriminals(View):
    def get(self,request,id):
        data=CriminalList.objects.get(pk=id)
        return render(request,'station/edit_criminal.html',{'list':data})
    def post(self,request,id):
        data=CriminalList.objects.get(pk=id)
        details=CriminalForm(request.POST,request.FILES,instance=data)
        if details.is_valid():
            details.save()
            return redirect('view_criminals')
        return render(request,'station/edit_criminal.html',{'list':data})

# <--------------------viewfeedback------------------>
class ViewFeedback(View):
    def get(self,request):
        list=Feedback.objects.all()
        return render(request,'station/view_feedback.html',{'list':list})

    # <--------------users complaints------------------->
class ViewComplaints(View):
    def get(self,request):
        complaint=UserComplaint.objects.all()
        return render(request,'station/view_complaint.html',{'complaint':complaint})

    # <-------------change status of complaint ---------------->
class ComplaintStatus(View):
    def get(self,request,id):
        complaint=UserComplaint.objects.get(pk=id)
        return render(request,'station/changestatus.html',{'complan':complaint})
    def post(self,request,id):
        user_id = request.session['login_id']
        if not user_id:
            messages.error("Please login for make changes")
            return redirect('log_manager:userslogin')
        stations=StationDetails.objects.get(user_details=user_id)
        complaint=UserComplaint.objects.get(pk=id)
        data=StatusForm(request.POST,instance=complaint)
        if data.is_valid():
            item=data.save(commit=False)
            item.station=stations
            item.save()
            return redirect('view_complaints')
        return render(request,'station/changestatus.html')

 #<------------view notification------------>
class ViewNotifications(View):
    def get(self, request):
        police_station_id = request.session['login_id']
        station=StationDetails.objects.get(user_details=police_station_id)
        notifications = Notification.objects.filter(police_station_id=station).order_by('-sent_at')
        return render(request, 'station/view_notifications.html', {'notifications': notifications})

    #<----------------labour complaint view and reply--------------------->
class ViewComplaints(View):
    def get(self, request):
        complaints = LabourComplaint.objects.filter(reply__isnull=True).order_by('-created_at')
        for complaint in complaints:
            print("jakjdljalj",complaint.complaint_text)
        return render(request, 'station/view_complaints.html', {'complaints': complaints})

                   # <----reply  to complaints-------->

class ReplyComplaint(View):
    def get(self, request, pk):
        complaint = LabourComplaint.objects.get(pk=pk)
        return render(request, 'station/reply_complaint.html', {'complaint': complaint})

    def post(self, request, pk):
        complaint = LabourComplaint.objects.get(pk=pk)
        reply = request.POST.get('reply')
        if reply:
            complaint.reply = reply
            complaint.save()
            return redirect('view_complaints')
        return render(request, 'station/view_complaints.html', {'complaint': complaint})



