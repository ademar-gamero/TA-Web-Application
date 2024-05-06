
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from ta_app.models import Course, Section, User
from ta_app.Classes.UserClass import UserClass

class courseSections(View):

    def get(self,request,pk):
        pass

    def post(self,request,pk):
        pass


                            
