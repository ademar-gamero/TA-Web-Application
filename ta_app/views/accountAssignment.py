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
        all_sections = Section.objects.all()
        assigned_courses = []
        selectableSections = []
        lab_check = "False"
        for sec in usr_sections:
            if sec.type == "lecture":
                for secs in Section.objects.filter(course_parent=sec.course_parent):
                    if secs not in usr_sections:
                        selectableSections.append(secs)
                    if secs.course_parent not in assigned_courses:
                        assigned_courses.append(secs.course_parent)
            if sec.type == "lab":
                for secs in Section.objects.filter(course_parent=sec.course_parent):
                    if secs not in usr_sections:
                        selectableSections.append(secs)
                lab_check = "True"
        selectableCourses = []
        for secs in  Section.objects.filter(type="lecture"):
            if secs not in usr_sections:
                selectableCourses.append(secs)
        print(lab_check)
        return render(request, "account_assignments.html",{'curr_user':account,
                                            'usr_role':usr_role,'sections':usr_sections,"courses":assigned_courses,'all_sections':all_sections,
                                            'selectableSections':selectableSections,'selectableCourses':selectableCourses
                                            ,"lab_check":lab_check})

    def post(self,request,pk):
        usr_role = request.session["role"]
        account = User.objects.get(pk=pk)
        usr_sections = account.assigned_section.all()
        sections = Section.objects.all()
        assigned_courses = []
        lab_check = "False"
        selectableSections = []
        for sec in usr_sections:
            if sec.type == "lecture":
                for secs in Section.objects.filter(course_parent=sec.course_parent):
                    if secs not in usr_sections:
                        selectableSections.append(secs)
                    if secs.course_parent not in assigned_courses:
                        assigned_courses.append(secs.course_parent)
            if sec.type == "lab":
                for secs in Section.objects.filter(course_parent=sec.course_parent):
                    if secs not in usr_sections:
                        selectableSections.append(secs)
        selectableCourses = []
        for secs in  Section.objects.filter(type="lecture"):
            if secs not in usr_sections:
                selectableCourses.append(secs)

        if usr_role != "Admin" and usr_role != "Instructor":
            return redirect("/Home/")
        sec_pk = request.POST.get('section')
        account = User.objects.get(pk=pk)
        newacc = UserClass(username=account.username, password=account.password, name=account.name, role=account.role, email=account.email,
                           phone_number=account.phone_number, address=account.address, assigned=account.assigned, assigned_sections=account.assigned_section.all())
        sections = Section.objects.all()
        try:
            section = Section.objects.get(pk=sec_pk)
            newacc.add_section(section)
        except ValueError as error:
            return render(request,"account_assignments.html",{'curr_user':account,'sections':sections,
                                                              'usr_role':usr_role,"courses":assigned_courses,"lab_check":lab_check,
                                                              'selectableSections':selectableSections,'all_sections':sections,
                                                              'selectableCourses': selectableCourses,'message': error.__str__()})
        usr_sections = account.assigned_section.all()
        print(account.assigned_section.all())
        selectableSections = []
        for sec in usr_sections:
            if sec.type == "lecture":
                for secs in Section.objects.filter(course_parent=sec.course_parent):
                    if secs not in usr_sections:
                        selectableSections.append(secs)
                    if secs.course_parent not in assigned_courses:
                        assigned_courses.append(secs.course_parent)
            if sec.type == "lab":
                for secs in Section.objects.filter(course_parent=sec.course_parent):
                    if secs not in usr_sections:
                        selectableSections.append(secs)
                lab_check = "True"
        selectableCourses = []
        for secs in  Section.objects.filter(type="lecture"):
            if secs not in usr_sections:
                selectableCourses.append(secs)

        return render(request,"account_assignments.html",{'curr_user':account,'sections':usr_sections,
                                                          'allSections':sections,'usr_role':usr_role,"courses":assigned_courses,
                                                          "lab_check":lab_check,'selectableSections':selectableSections,
                                                          'selectableCourses':selectableCourses,'all_sections':sections,
                                                          'message': 'Section/Course was added successfully!'})


                            
