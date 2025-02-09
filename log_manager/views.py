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
        response_dict = {"success": False}
        user = authenticate(username=username, password=password)
        if user is None:
            response_dict["reason"] = "Invalid credentials."
            messages.error(request, response_dict["reason"])
            return render(request, 'log_manager/login.html', {"error_message": response_dict["reason"]})

        if not user.is_active:
            response_dict["reason"] = "Your account is inactive. Contact support."
            messages.error(request, response_dict["reason"])
            return render(request, 'log_manager/login.html', {"error_message": response_dict["reason"]})

        login(request, user)

        print("user loged in:", request.user)
        print("authenticated:", request.user.is_authenticated)
        print('user_type:',request.user.user_type)
        user_type = request.user.user_type
        landing_page_url = {
            "ADMIN": "log_manager:adminhome",
            "USER": "log_manager:userhome",
            "LABOUR": "log_manager:labourhome",
            "POLICESTATION": "log_manager:stationhome",
        }
        if user_type in landing_page_url:
            return redirect(landing_page_url[user_type])

        response_dict["reason"] = "Invalid user type."
        messages.error(request, response_dict["reason"])
        return render(request, 'log_manager/login.html', {"error_message": response_dict["reason"]})


class LogoutUser(View):
    def get(self, request):
        logout(request)
        return redirect('log_manager:userslogin')

