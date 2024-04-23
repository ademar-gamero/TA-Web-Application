from django.views import View
from django.shortcuts import render, redirect
from ta_app.models import User
from django.contrib import messages

class login_view(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Check for empty inputs and set specific error messages
        if not username and not password:
            messages.error(request, 'Username and password cannot be empty.')
        elif not username:
            messages.error(request, 'Please enter your username.')
        elif not password:
            messages.error(request, 'Please enter your password.')

        # Return to login page if any input checks failed
        if not username or not password:
            return render(request, 'login.html')

        # Searches for user in the database
        try:
            user = User.objects.get(username=username, password=password)
            # User is found:
            request.session["role"] = user.role
            request.session["name"] = user.name
            return redirect('Home')  # Ensure this matches the URL name defined in urls.py
        except User.DoesNotExist:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')
