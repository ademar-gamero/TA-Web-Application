from django.core.exceptions import PermissionDenied
from django.views import View
from django.shortcuts import render, redirect
from ta_app.models import User
from django.contrib import messages
from ta_app.Classes.UserClass import UserClass


class accountCreation(View):

    def get(self, request):
        current = request.session["role"]
        if current == "Admin":
            return render(request, "create_account.html")
        else:
            raise PermissionDenied

    def post(self, request):
        try:
            user = UserClass(request.POST['username'], request.POST['password'],
                             request.POST['name'], request.POST['role'], request.POST['email'],
                             request.POST['phone_number'], request.POST['address'])
            user.create_user()
            return render(request, 'create_account.html')
        except ValueError as error:
            return render(request, 'create_account.html', {'message': error.__str__()})
