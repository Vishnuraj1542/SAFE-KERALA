from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.views import View
from django.db.models import Q

from .models import *
from .forms import *
from my_admin.models import*
from log_manager import*
from my_admin.forms import *
from log_manager import *
from public.models import RequestLabour,Message
from public.forms import WorkStatus



# Create your views here.

# <----------send feedback--------------->
class Feedback(View):
    def get(self, request):
        return render(request, 'labour/home.html')

    def post(self, request):
        labour = request.user
        if not labour:
            messages.error(request, "You must be logged in to submit feedback.")
            return redirect('log_manager:userslogin')
        try:
            user = LabourDetails.objects.get(user_details=labour)
        except LabourDetails.DoesNotExist:
            messages.error(request, "no user found.")
            return redirect('log_manager:labourhome')

        data = FeedbackForm(request.POST)
        if data.is_valid():
            feedback = data.save(commit=False)
            feedback.sender = user
            feedback.save()
            messages.success(request, "Feedback shared successfully!")
            return redirect('log_manager:labourhome')
        else:
            messages.error(request, "Invalid feedback submission.")
            return render(request, 'labour/home.html', {'form': data})
#<-------------------add and manage skills ---------------->
class EditSkill(View):
    def get(self,request):
        user_id=request.user
        labour=LabourDetails.objects.get(user_details=user_id)
        return render(request,'labour/manage_skill.html',{'labour':labour})
    def post(self,request):
        user_id = request.user
        labour = get_object_or_404(LabourDetails, user_details=user_id)
        if labour is None:
            return redirect('log_manager:userslogin')
        data=SkillForm(request.POST,instance=labour)
        if data.is_valid():
            data.save()
            return HttpResponse(
                '<script>alert("Skill Updated Sucessfully!"); window.location.href="/labourpage/";</script>')
            return redirect('log_manager:labourhome')
        return render(request,'labour/manage_skill.html',{'labour':labour})

#<----------------add and manage personal issue------------------>
class Personal(View):
    def get(self,request):
        return render(request,'labour/personal_issue.html')
    def post(self,request):
        labour=request.user
        log_id=LabourDetails.objects.get(user_details=labour)
        data=PersonalIssueForm(request.POST)
        if data.is_valid():
            log=data.save(commit=False)
            log.labourer=log_id
            log.save()
            return HttpResponse(
                '<script>alert("Issue Added Sucessfully!"); window.location.href="/labour/viewissue/";</script>')
        return render(request,'labour/personal_issue.html')

    #<---------------view issues---------------------->
class ViewIssue(View):
    def get(self,request):
        problem=PersonalIssue.objects.order_by('-created_at').all()
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
        try:
            user = get_object_or_404(LoginDetails, id=request.user.id)
        except LoginDetails.DoesNotExist:
            messages.error(request, 'Failed to retrieve user details.')
            return redirect('log_manager:userslogin')
        comp = ComplaintForm(request.POST)
        if comp.is_valid():
            complaint = comp.save(commit=False)
            complaint.sender = user
            complaint.save()
            return HttpResponse(
                '<script>alert("Complaint submitted successfully!"); window.location.href="/labourpage/";</script>')
        return render(request, 'labour/submit_complaint.html',{'comp': comp} )
                     #-----viewreply------->
class ViewReply(View):
    def get(self,request):
        id=request.user
        if not id:
            return redirect('log_manager:userslogin')
        content=LabourComplaint.objects.filter(sender_id=id)
        for complaint in content:
            if not complaint.reply:
                complaint.reply="not replied yet"
        return render(request,'labour/complaint_reply.html',{'replies':content})


#                      <------------view work request------------->
class ViewRequest(View):
    def get(self, request):
        worker_id = request.user
        if worker_id is None:
            return redirect('log_manager:userslogin')
        try:
            worker = LabourDetails.objects.get(user_details=worker_id)
            work = RequestLabour.objects.filter(labour_id=worker)
            return render(request, 'labour/work_request.html', {'works': work})
        except LabourDetails.DoesNotExist:
            return redirect('log_manager:userslogin')

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

    #<------messaged peoples list --------------->
class UsersListChat(View):
    def get(self, request):
        labour_id = request.user.id

        if not labour_id:
            return redirect('Manager:login')
        user_ids = Message.objects.filter(
            Q(sender_id=labour_id) | Q(receiver_id=labour_id)
        ).values_list('sender_id', 'receiver_id')
        unique_user_ids = set()
        for sender, receiver in user_ids:
            if sender != labour_id:
                unique_user_ids.add(sender)
            if receiver != labour_id:
                unique_user_ids.add(receiver)
        users = LoginDetails.objects.filter(id__in=unique_user_ids)

        return render(request, 'labour/users_list_chat.html', {'users': users})


#                  <-------------chat with users------------------>
class ChatWithUser(View):
    def get(self, request, user_id):
        labour_id = request.user
        if not labour_id:
            return redirect('log_manager:userslogin')

        messages = Message.objects.filter(
            sender_id=labour_id, receiver_id=user_id
        ) | Message.objects.filter(
            sender_id=user_id, receiver_id=labour_id
        ).order_by('timestamp')

        return render(request, 'labour/user_chat.html', {'messages': messages, 'user_id': user_id})
    def post(self, request, user_id):
        labour_id = request.user.id
        if not labour_id:
            return redirect('log_manager:userslogin')
        message_text = request.POST.get('message')
        if message_text:
            Message.objects.create(sender_id=labour_id, receiver_id=user_id, message=message_text)
        return redirect('user_chat', user_id=user_id)