from django.shortcuts import render, redirect
from django.views import View
from ta_app.models import Course, User, Section
from django.http import Http404


class accountList(View):

    def get(self, request):
        isAdmin = False
        accounts = User.objects.all()
        role = request.session["role"]
        if role == "Admin":
            isAdmin = True
        return render(request, "account_list.html", {"account_list": accounts, "isAdmin": isAdmin,"usr_role": role})

    def post(self, request):
        isAdmin = False
        user = User.objects.get(pk=request.session['pk'])
        name = request.POST.get('name', '')
        username = request.POST.get('username', '')
        role = request.POST.get('roles', '')
        accounts = []
        role = request.session["role"]
        if role == "Admin":
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
        elif request.POST.get('input_button') == "Show Users Assigned To Your Courses":
            assigned_sections = user.assigned_section.all()
            courselist = []
            accounts = []
            for secs in assigned_sections:
                courselist.append(secs.course_parent)
            for course in courselist:
                secs = Section.objects.filter(course_parent = course)
                for sec in secs:
                    for usr in sec.assigned_users.all():
                        accounts.append(usr)
        else:
            accounts = User.objects.all()
        return render(request, "account_list.html", {"account_list": accounts, "isAdmin": isAdmin, "usr_role": role})
























