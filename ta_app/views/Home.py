from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse


class Home(View):
    def get(self, request):
        if 'role' not in request.session or 'name' not in request.session:
            messages.error(request, "You are not logged in.")
            return redirect('login')

        curr_role = request.session["role"]
        curr_name = request.session["name"]
        curr_pk = request.session["pk"]
        response = render(request, "home.html", {"role": curr_role, "name": curr_name, "user_id": curr_pk})
        response['Cache-Control'] = 'no-store'
        return response

    def post(self, request):
        if 'logout' in request.POST:
            request.session.flush()
            messages.success(request, "You have been logged out successfully.")
            response = redirect('login')
            response['Cache-Control'] = 'no-store'
            return response
        return self.get(request)