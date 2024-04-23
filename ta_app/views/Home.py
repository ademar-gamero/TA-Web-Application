
from django.shortcuts import render,redirect
from django.views import View

class Home(View):
    def get(self,request):
        curr_role = request.session["role"]
        curr_name = request.session["name"]
        return render(request, "home.html",{"role":curr_role,"name":curr_name})
