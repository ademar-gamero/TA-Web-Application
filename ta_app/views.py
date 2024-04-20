from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views import View
from .models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseRedirect
# Create your views here.

class login_view(View):
    def get(self, request):
        return render(request, 'login.html')
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Make sure you have a URL name 'home' defined
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')