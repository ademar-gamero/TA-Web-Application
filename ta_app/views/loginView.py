from django.views import View
from django.shortcuts import render, redirect
from ta_app.models import User
from django.contrib import messages
from django.contrib.messages import get_messages

class login_view(View):
    def get(self, request):
        messages_list = list(get_messages(request))
        latest_message = messages_list[-1] if messages_list else None
        latest_message_text = latest_message.message if latest_message else None

        context = {'messages': latest_message_text}
        return render(request, 'login.html', context)

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
            messages_list = list(get_messages(request))
            latest_message = messages_list[-1] if messages_list else None
            latest_message_text = latest_message.message if latest_message else None
            return render(request, 'login.html', {'messages': latest_message_text})

        # Searches for user in the database
        try:
            user = User.objects.get(username=username, password=password)
            # User is found:
            request.session["role"] = user.role
            request.session["name"] = user.name
            request.session["pk"] = user.pk
            return redirect('Home')  # Ensure this matches the URL name defined in urls.py
        except User.DoesNotExist:
            messages.error(request, 'Invalid username or password.')
            messages_list = list(get_messages(request))
            latest_message = messages_list[-1] if messages_list else None
            latest_message_text = latest_message.message if latest_message else None
            return render(request, 'login.html', {'messages': latest_message_text})