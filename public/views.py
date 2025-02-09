from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.contrib import messages
from django.http import HttpResponse
from django.views import View
from django.db.models import Q
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
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('log_manager:userslogin')
        try:
            user_details = get_object_or_404(UserDetails, user_details=request.user.id)
        except:
            return redirect('log_manager:userslogin')
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = user_details
            complaint.save()
            return HttpResponse(
                '''<script>alert("complaint send sucessfully.");window.location="/userpage/"</script>''')

        return render(request, 'user/send_complaint.html', {'form': form})

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
    def get(self, request, id):
        labours = get_object_or_404(LabourDetails, pk=id)
        return render(request, 'user/request_labour.html', {'lab': labours})

    def post(self, request, id):
        if not request.user.is_authenticated:
            messages.error(request, " please login to request labour")
            return redirect('log_manager:userslogin')

        user_pk = request.user.id
        user=LoginDetails.objects.get(pk=user_pk)
        user_details = UserDetails.objects.filter(user_details=user_pk).first()
        if not user_details:
            messages.error(request, "User not found in the system. Please complete registration.")
            return redirect('log_manager:userslogin')
        labours = get_object_or_404(LabourDetails, pk=id)
        data = RequestForm(request.POST)
        if data.is_valid():
            item = data.save(commit=False)
            item.user_id = user
            item.labour_id = labours
            item.save()
            messages.success(request, "Labour request submitted successfully.")
            print(request.user)
            print(request.user.user_type)
            return redirect(reverse('request_status'))
        else:
            messages.error(request, "an error occured so please try again")
        return render(request, 'user/request_labour.html', {'lab': labours, 'form': data})


#<----------------------request status--------------------->
class RequestStatus(View):
    def get(self,request):
        user_id=request.user.id
        user = get_object_or_404(LoginDetails,pk=user_id)
        state=RequestLabour.objects.filter(user_id=user)
        return render(request,'user/request_status.html',{'state':state})

    #<------------- send feedback about labour----------------->
class FeedBack(View):
    def get(self,request,id):
        return render(request,'user/feedback.html')
    def post(self,request,id):
        users_id=request.user.id
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

    #<-------chat with labour


class ChatwithWorker(View):
    def get(self, request, labour_id):
        if not request.user.is_authenticated:
            return redirect('userslogin')

        labour = get_object_or_404(LabourDetails, pk=labour_id)

        messages_list = Message.objects.filter(
            Q(sender_id=request.user.id, receiver_id=labour.user_details.id) |
            Q(sender_id=labour.user_details.id, receiver_id=request.user.id)
        ).order_by('timestamp')

        return render(request, 'user/labour_chat.html', {
            'messages': messages_list,
            'labour_id': labour_id,
            'user_id': request.user.id,
        })

    def post(self, request, labour_id):
        if not request.user.is_authenticated:
            return redirect('userslogin')

        labour = get_object_or_404(LabourDetails, pk=labour_id)

        message_text = request.POST.get('message', '').strip()
        if message_text:
            Message.objects.create(
                sender=request.user,
                receiver=labour.user_details,
                message=message_text
            )
        else:
            messages.error(request, "Message cannot be empty.")

        return redirect('workerchat', labour_id=labour_id)












