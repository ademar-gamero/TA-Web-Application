from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from ta_app.models import Course, Section, User
from ta_app.Classes.UserClass import UserClass

class accountAssignment(View):

    def get(self,request,pk):
        curr_acc = request.session["role"]
        if curr_acc != "Admin" and curr_acc != "Instructor":
            return redirect("/Home/")
        account = User.objects.get(pk=pk)
        sections = Section.objects.all()
        return render(request, "account_assignments.html",{'user':account, 'allSections':sections})

    def post(self,request,pk):
        section = request.POST.get('section')
        account = User.objects.get(pk=pk)
        newacc = UserClass(account.username, account.password, account.name, account.role, account.email,
                           account.phone_number, account.address, account.assigned, account.assigned_section)
        sections = Section.objects.all()
        try:
            newacc.add_section(section)
        except ValueError as error:
            return render(request,"account_assignments.html",{'user':account,'allSections':sections,'message': error.__str__()})

        return render(request,"account_assignments.html",{'user':newacc,'allSections':sections,'message': 'Section was added successfully!'})




