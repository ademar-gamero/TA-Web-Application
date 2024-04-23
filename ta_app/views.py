from django.views import View
from django.shortcuts import render

class account_creation_view(View):
    def get(self, request):
        return render(request, "createAccount.html")

    def post(self, request):
        pass