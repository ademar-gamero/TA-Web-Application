from django.shortcuts import render
from django.views import View


# Create your views here.
class AccountCreation(View):
    def get(self, request):
        return render(request, "createAccount.html", {})

    def post(self, request):
        pass