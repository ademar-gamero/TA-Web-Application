from django.shortcuts import render, redirect
from django.views import View
from ta_app.models import User, Section, Course
from classes import UserClass

# Create your views here.
class AccountCreation(View):
    def get(self, request):
        return render(request, "createAccount.html", {})

    def post(self, request):
        pass