
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from ta_app.models import Course, Section, User
from ta_app.Classes.UserClass import UserClass

class courseSections(View):

    def get(self,request,course_pk):
        usr_role = request.session["role"]
        course = Course.objects.get(pk=course_pk)
        sections = Section.objects.filter(course_parent = course)
        usr_pool = User.objects.all()
        ta_pool = []
        for section in sections:
            ta = User.objects.filter(role="Teacher-Assistant",assigned_section__in=[section])
            for tas in ta:
                ta_pool.append(tas)
        return render(request, "course_sections.html",{"course":course,"sections":sections,
                                                       "usr_pool":usr_pool,"usr_role":usr_role,"ta_pool":ta_pool})
    def post(self,request,course_pk):

        usr_role = request.session["role"]
        course = Course.objects.get(pk=course_pk)
        sections = Section.objects.filter(course_parent = course)
        usr_pool = User.objects.filter(assigned=False)
        ta_pool = []
        
        
        course = Course.objects.get(pk=course_pk)
        for key, value in request.POST.items():
            print(key)
            print(value)
            try:
                acc = User.objects.get(pk = value)
                newacc = UserClass(acc.username, value.password, value.name, value.role, value.email,
                           acc.phone_number, value.address, value.assigned, value.assigned_section)
                sec = Section.objects.get(pk=key)
                newacc.add_section(sec)
            except ValueError as error:
                return render(request, "course_sections.html",{"course":course,"sections":sections,
                                        "usr_pool":usr_pool,"usr_role":usr_role,"ta_pool":ta_pool, "message":error.__str__()})

        usr_role = request.session["role"]
        course = Course.objects.get(pk=course_pk)
        sections = Section.objects.filter(course_parent = course)
        usr_pool = User.objects.filter(assigned=False)
        ta_pool = []
        
        for section in sections:
            ta = User.objects.filter(role="Teacher-Assistant",assigned_section__in=[section])
            for tas in ta:
                ta_pool.append(tas)
        message = "Succesfully assigned user to section"
        return render(request, "course_sections.html",{"course":course,"sections":sections,
                                                       "usr_pool":usr_pool,"usr_role":usr_role,"ta_pool":ta_pool, "message":message})

        


                            
