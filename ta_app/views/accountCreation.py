from django.core.exceptions import PermissionDenied
from django.views import View
from django.shortcuts import render, redirect
from ta_app.models import User
from django.contrib import messages
from ta_app.Classes.UserClass import UserClass


class accountCreation(View):

    def get(self, request):
        pass

    def post(self, request):
        pass