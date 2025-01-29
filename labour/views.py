from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.views import View

from .models import *
from .forms import *
from my_admin.models import*
from log_manager import*
from my_admin.forms import *
from log_manager import *
from public.models import RequestLabour
from public.forms import WorkStatus



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
        print('labourid------->',labour)
        log_id=LabourDetails.objects.get(user_details=labour)
        data=PersonalIssueForm(request.POST)
        if data.is_valid():
            log=data.save(commit=False)
            log.labourer=log_id
            log.save()
            return redirect('log_manager:labourhome')
        return render(request,'labour/personal_issue.html')

    #<---------------view issues---------------------->
class ViewIssue(View):
    def get(self,request):
        problem=PersonalIssue.objects.all()
        return render(request,'labour/view_issue.html',{'problem':problem})


    #<----------edit issue---------->
class EditIssue(View):
    def get(self,request,id):
        data=PersonalIssue.objects.get(pk=id)
        return render(request,'labour/edit_issue.html',{'data':data})
    def post(self,request,id):
        data=PersonalIssue.objects.get(pk=id)
        issue=PersonalIssueForm(request.POST,instance=data)
        if issue.is_valid():
            issue.save()
            return redirect('view_issue')
        return render(request,'labour/edit_issue.html',{'data':data})
               #<-------------------------delete issue------------------------>
class DeleteIssue(View):
    def get(self,request,id):
        data = PersonalIssue.objects.get(pk=id)
        return render(request,'labour/confirmation.html',{'data':data})

    def post(self,request,id):
        data=PersonalIssue.objects.get(pk=id)
        data.delete()
        return redirect('view_issue')

# <------------------------send complaint and view reply -------------->
class SubmitComplaint(View):
    def get(self, request):
        form = ComplaintForm()
        return render(request, 'labour/submit_complaint.html', {'form': form})
    def post(self, request):
        user_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('log_manger:userslogin')
        user = get_object_or_404(LoginDetails, id=user_id)
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.sender = user
            complaint.save()
            return HttpResponse(
                '<script>alert("Complaint submitted successfully!"); window.location.href="/labourpage/";</script>')
        return render(request, 'labour/submit_complaint.html', )
                     #-----viewreply------->
class ViewReply(View):
    def get(self,request):
        id=request.session.get('login_id')
        if not id:
            return redirect('log_manager:userslogin')
        content=LabourComplaint.objects.filter(sender_id=id)
        for complaint in content:
            if not complaint.reply:
                complaint.reply="not replied yet"
        return render(request,'labour/complaint_reply.html',{'replies':content})


#                      <------------view work request------------->
class ViewRequest(View):
    def get(self,request):
        worker_id=request.session['login_id']
        if not worker_id:
            return redirect('log_manager:userslogin')
        worker=LabourDetails.objects.get(user_details=worker_id)
        work=RequestLabour.objects.filter(labour_id=worker)
        return render(request,'labour/work_request.html',{'works':work})

    #<----------------------change work status------------------->
class ChangeWorkStatus(View):
    def get(self,request,id):
        work=RequestLabour.objects.get(pk=id)
        return render(request,'labour/change_status.html',{'work':work})
    def post(self,request,id):
        work_request=RequestLabour.objects.get(pk=id)
        new_status=WorkStatus(request.POST,instance=work_request)
        if new_status.is_valid():
            new_status.save()
            return redirect('view_request')
        return render(request,'labour/change_status.html',{'work':work_request})


