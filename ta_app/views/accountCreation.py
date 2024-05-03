from django.core.exceptions import PermissionDenied
from django.views import View
from django.shortcuts import render, redirect, HttpResponse
from ta_app.models import User
from django.contrib import messages
from ta_app.Classes.UserClass import UserClass


class accountCreation(View):

    def get(self, request):
        current = request.session["role"]
        if current == "Admin":
            return render(request, "create_account.html")
        else:
            return redirect('/Home/')

    def post(self, request):
        try:
            user = UserClass(username=request.POST['username'], password=request.POST['password'],
                             name=request.POST['name'], role=request.POST['role'], email=request.POST['email'],
                             phone_number=request.POST['phone_number'], address=request.POST['address'],
                             skills=request.POST['skills'])
            user.create_user()
            return render(request, 'create_account.html',
                          {'message': f'Account \'{user.username}\' created successfully!'})
        except ValueError as error:
            return render(request, 'create_account.html', {'message': error.__str__()})
