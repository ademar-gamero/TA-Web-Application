
from django.shortcuts import render,redirect
from django.views import View
from ta_app.models import Course,User
from django.http import Http404

class accountView(View):
    acc_edit = None

    def get(self,request):
        pass
    def post(self,request):
        pass
