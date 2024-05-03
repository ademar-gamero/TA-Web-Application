
from django.shortcuts import render,redirect
from django.views import View
from ta_app.models import Course, User
from django.http import Http404


class accountList(View):

    def get(self,request):
        isAdmin = False
        accounts = User.objects.all()
        if request.session["role"] == "Admin":
            isAdmin = True
        return render(request,"account_list.html", {"account_list": accounts, "isAdmin": isAdmin})

    def post(self,request):
        isAdmin = False
        name = request.POST.get('name', '')
        username = request.POST.get('username', '')
        role = request.POST.get('roles', '')
        accounts = []
        if request.session["role"] == "Admin":
            isAdmin = True
        if request.POST.get('input_button') == "Submit":
            if name != '' and username != '' and role != '':
                accounts = User.objects.filter(name=name, username=username, role=role)
            if name != '' and username != '' and role == '':
                accounts = User.objects.filter(name=name, username=username)
            if name != '' and username == '' and role != '':
                accounts = User.objects.filter(name=name, role=role)
            if name == '' and username != '' and role != '':
                accounts = User.objects.filter(username=username, role=role)
            if name == '' and username == '' and role != '':
                accounts = User.objects.filter(role=role)
            if name == '' and username != '' and role == '':
                accounts = User.objects.filter(username=username)
            if name != '' and username == '' and role == '':
                accounts = User.objects.filter(name=name)
        else:
            accounts = User.objects.all()
        return render(request,"account_list.html", {"account_list": accounts, "isAdmin": isAdmin})
    



























