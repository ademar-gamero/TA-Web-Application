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
            if sec.type == "lecture" or sec.type == "lab":
                assigned_courses.append(sec.course_parent)
        return render(request, "account_assignments.html",{'user':account, 'allSections':sections,
                                            'usr_role':usr_role,'sections':usr_sections,"courses":assigned_courses})

    def post(self,request,pk):

        usr_role = request.session["role"]
        account = User.objects.get(pk=pk)
        usr_sections = account.assigned_section.all()
        sections = Section.objects.all()
        assigned_courses = []
        for sec in usr_sections:
            if sec.type == "lecture" or sec.type == "lab":
                assigned_courses.append(sec.course_parent)

        if usr_role != "Admin" and usr_role != "Instructor":
            return redirect("/Home/")
        sec_pk = request.POST.get('section')
        account = User.objects.get(pk=pk)
        newacc = UserClass(username=account.username, password=account.password, name=account.name, role=account.role, email=account.email,
                           phone_number=account.phone_number, address=account.address, assigned=account.assigned, assigned_sections=account.assigned_section.all())
        sections = Section.objects.all()
        try:
            section = Section.objects.get(pk=sec_pk)
            newacc.add_section(section,usr_role)
        except ValueError as error:
            return render(request,"account_assignments.html",{'user':account,'allSections':sections,'usr_role':usr_role,"courses":assigned_courses,'message': error.__str__()})

        usr_sections = account.assigned_section.all()
        assigned_courses = []
        for sec in usr_sections:
            if sec.type == "lecture" or sec.type == "lab":
                assigned_courses.append(sec.course_parent)

        return render(request,"account_assignments.html",{'user':newacc,'sections':usr_sections,'allSections':sections,'usr_role':usr_role,"courses":assigned_courses,'message': 'Section was added successfully!'})


                            
