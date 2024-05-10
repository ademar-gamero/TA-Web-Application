from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from ta_app.models import Course, Section, User
from ta_app.Classes.UserClass import UserClass

class accountAssignment(View):

    def get(self,request,pk):
        usr_role = request.session["role"]
        account = User.objects.get(pk=pk)
        usr_sections = account.assigned_section.all()
        sections = Section.objects.all()
        assigned_courses = []
        for sec in usr_sections:
            if sec.type == "lecture":
                assigned_courses.append(sec.course_parent)
        return render(request, "account_assignments.html",{'user':account, 'allSections':sections,
                                            'usr_role':usr_role,'sections':usr_sections,"courses":assigned_courses})

    def post(self,request,pk):
        curr_acc = request.session["role"]
        if curr_acc != "Admin" and curr_acc != "Instructor":
            return redirect("/Home/")
        sec_pk = request.POST.get('section')
        account = User.objects.get(pk=pk)
        newacc = UserClass(username=account.username, password=account.password, name=account.name, role=account.role, email=account.email,
                           phone_number=account.phone_number, address=account.address, assigned=account.assigned, assigned_sections=account.assigned_section.all())
        sections = Section.objects.all()
        try:
            section = Section.objects.get(pk=sec_pk)
            newacc.add_section(section,curr_acc)
        except ValueError as error:
            return render(request,"account_assignments.html",{'user':account,'allSections':sections,'message': error.__str__()})

        return render(request,"account_assignments.html",{'user':newacc,'allSections':sections,'message': 'Section was added successfully!'})


                            
