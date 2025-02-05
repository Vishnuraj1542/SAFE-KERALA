from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import authenticate,login,logout

from django.contrib import messages
from .models import *

# Create your views here.
class UserPage(View):
    def get(self,request):
        return render(request,'user/home.html')
class AdminPage(View):
    def get(self,request):
        return render(request,'my_admin/home.html')
class StationPage(View):
    def get(self,request):
        return render(request,'station/home.html')
class LabourPage(View):
    def get(self,request):
        return render(request,'labour/home.html')

class ForLogin(View):
    def get(self, request):
        return render(request, 'log_manager/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        response_dict = {"sucess":False}
        landing_page_url = {
            "ADMIN": "log_manager:adminhome",
            "USER": "log_manager:userhome",
            "LABOUR": "log_manager:labourhome",
            "POLICESTATION": "log_manager:stationhome",
        }
        user = authenticate(username=username, password=password)

        if user is None:
            response_dict["reason"] = "Invalid credentials."
            messages.error(request, response_dict["reason"])
            return render(request, 'log_manager/login.html', {"error_message": response_dict["reason"]})

        try:
            login_details = LoginDetails.objects.get(username=username)
            request.session['login_id'] = user.id
            print("kja;lskdjl",user.id)
        except LoginDetails.DoesNotExist:
            response_dict["reason"] = "No account found for this username. Please signup."
            messages.error(request, response_dict["reason"])
            return render(request, 'log_manager/login.html', {"error_message": response_dict["reason"]})


        request.session["data"] = {
            "user_id": user.id,
            "user_type": user.user_type,
            "username": user.username,
            "status": user.is_active,
        }
        request.session["user"] = user.username
        request.session["status"] = user.is_active
        user_type = user.user_type
        if user_type in landing_page_url:
            return redirect(landing_page_url[user_type])
            print(request.user.is_authenticated)
        else:
            response_dict["reason"] = "Invalid user type."
            messages.error(request, response_dict["reason"])
            return render(request, 'log_manager/login.html', {"error_message": response_dict["reason"]})
class LogoutUser(View):
    def get(self, request):
        logout(request)
        return redirect('log_manager:userslogin')
